/**
 * Created by Lavrentev on 09.02.2017.
 */
var _ = require('lodash');
var async = require('async');

module.exports = function(sequelize, onSuccessAll) {
    var tables = [
        'mkb10Code',
        'data',
        'territory',
        'population'
    ];

    async.eachSeries(tables, function (item, callback) {
        require('./' + item + '.js')(sequelize, callback);
    }, onSuccessAll);
};