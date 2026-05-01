var territory = require('../models').territory;
var _ = require('lodash');
var async = require('async');
var fs = require('fs');

// Путь к файлу для импорта
var filePath = './app/initData/territories.csv';

module.exports = function (sequelize, onSuccessAll) {

    territory.findAll().then(function (data) {
        // Если в таблице уже есть данные по справочникам МинЭнерго, то уходим от сюда
        if (data && data.length)
            return onSuccessAll();

        // Если файла для импорта не существует, то уходим от сюда
        if (!fs.existsSync(filePath))
            return onSuccessAll();

        console.log('\nImport file found: ' + filePath);

        var values = [];

        var territoryFields = ['id', 'name', 'parentId'];

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
                    addValue(line);
                    index = remaining.indexOf('\n');
                }
            });

            input.on('end', function () {
                if (remaining.length > 0) {
                    // addValue(remaining);
                    addValue(remaining);
                }
                async.eachSeries(values, eachValue, function (err) {
                    if (err)
                        console.log('Error: ' + err);

                    updateAutoincrement(function () {
                        //var result = (err ? 'bad' : 'good') + Date.now();
                        /*console.log('Imported ' + cntImportValues + ' records of ' + cntAllValues +
                         '\nMatches found: ' + cntExistsValues + '\n');*/
                        console.log('Imported ' + cntImportValues + ' records of ' + cntAllValues + '\n');
                        return onSuccessAll();
                    });
                });
            });
        }

        function addValue(line) {
            // увеличиваем счётчик записей и добавляем значение
            // в values (удаляя при этом пробелы из начала и конца строки)
            var splitedLine = line.split(';');
            if (splitedLine[1].trim()) {
                var data = {};
                _.forEach(territoryFields, function(key, value){
                    data[key] = splitedLine[value].trim() || null;
                });
                cntAllValues++;
                values.push(data);
            }
        }

        function eachValue(item, callback) {
            // Проверяем на существование такое значение в базе
            /*territory.findAll({where: {code: item.code}}).then(function (data) {
             // Если такая записть уже есть в БД - просто прибавляем счётчик совпадений
             if ((data || []).length) {
             cntExistsValues++;
             return callback();
             }*/

            // Если совпадений не найдено - вставляем записть в БД
            territory.create(item).then(function () {
                cntImportValues++;
                callback();
            });
            //});
        }

        function updateAutoincrement(callback){
            territory.max('id').then(function (maxId) {
                sequelize.query('select setval(\'territories_id_seq\'::regclass, ' + maxId + ');').finally(callback);
            }, callback);
        }

        // Вызываем функцию для построчного чтения файла и передаём stream файла
        readLines(fs.createReadStream(filePath));
    });
};