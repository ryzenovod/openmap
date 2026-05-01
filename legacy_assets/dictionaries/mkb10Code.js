var mkb10Code = require('../models').mkb10Code;
var _ = require('lodash');
var async = require('async');
var fs = require('fs');

// Путь к файлу для импорта
// var filePath = './app/initData/mkb10Codes.csv';
var filePath = './app/initData/mkb10Codes_light.csv';

module.exports = function (sequelize, onSuccessAll) {

    mkb10Code.findAll().then(function (data) {
        // Если в таблице уже есть данные по справочникам МинЭнерго, то уходим от сюда
        if (data && data.length)
            return onSuccessAll();

        // Если файла для импорта не существует, то уходим от сюда
        if (!fs.existsSync(filePath))
            return onSuccessAll();

        console.log('\nImport file found: ' + filePath);

        var values = [];

        var mkb10CodeFields = ['id', 'parentId', 'code', 'name', 'isVisual'];

        var cntAllValues = 0, // кол-во записей
            cntImportValues = 0;  // кол-во записей, которые удалось импортировать
            //cntExistsValues = 0; // количество записей для импорта, которые уже существуют в БД

        // Функция построчно читает файл, заполняя массив values. После, пишет values в базу
        function readLines(input) {
            var remaining = '';

            input.on('data', function (data) {
                remaining += data;
                var index = remaining.indexOf('\n');
                while (index > -1) {
                    var line = remaining.substring(0, index);
                    remaining = remaining.substring(index + 1);
                    addValue({
                        id: line.split(';')[0].trim(),
                        parentId: line.split(';')[1].trim(),
                        code: line.split(';')[2].trim(),
                        name: line.split(';')[3].trim(),
                        isVisual: line.split(';')[4].trim()
                    });
                    index = remaining.indexOf('\n');
                }
            });

            input.on('end', function () {
                if (remaining.length > 0) {
                    // addValue(remaining);
                    addValue({
                        id: remaining.split(';')[0].trim(),
                        parentId: remaining.split(';')[1].trim(),
                        code: remaining.split(';')[2].trim(),
                        name: remaining.split(';')[3].trim(),
                        isVisual: remaining.split(';')[4].trim()
                    });
                }
                async.eachSeries(values, eachValue, function (err) {
                    if (err)
                        console.log('Error: ' + err);

                    updateAutoincrement(function () {
                        console.log('Imported ' + cntImportValues + ' records of ' + cntAllValues + '\n');
                        return onSuccessAll();
                    });
                });
            });
        }

        function addValue(data) {
            // увеличиваем счётчик записей и добавляем значение
            // в values (удаляя при этом пробелы из начала и конца строки)
            if (data.code) {
                cntAllValues++;
                values.push(data);
            }
        }

        function eachValue(item, callback) {
            // Проверяем на существование такое значение в базе
            /*mkb10Code.findAll({where: {code: item.code}}).then(function (data) {
                // Если такая записть уже есть в БД - просто прибавляем счётчик совпадений
                if ((data || []).length) {
                    cntExistsValues++;
                    return callback();
                }*/

                // Если совпадений не найдено - вставляем записть в БД
                var obj = {
                    id: item.id,
                    parentId: item.parentId || null,
                    code: item.code,
                    name: item.name,
                    isVisual: item.isVisual || false
                };

                mkb10Code.create(_.pick(obj, mkb10CodeFields)).then(function () {
                    cntImportValues++;
                    callback();
                });
            //});
        }

        function updateAutoincrement(callback){
            mkb10Code.max('id').then(function (maxId) {
                sequelize.query('select setval(\'"mkb10Codes_id_seq"\'::regclass, ' + maxId + ');').finally(callback);
            }, callback);
        }

        // Вызываем функцию для построчного чтения файла и передаём stream файла
        readLines(fs.createReadStream(filePath));
    });
};