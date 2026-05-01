/**
 * Created by Lavrentev on 16.03.2017.
 */
var CancerData = require('../models').cancerData;
var async = require('async');
var _ = require('lodash');
var moment = require('moment');

var basicData = [
    {
        regNum: 1,
        dob: new Date(moment('01.01.1959', 'DD.MM.YYYY')),
        gender: 'муж',
        regionCd: 51,
        area: 'Артём (город. округ)',
        subArea: 'город Артём',
        suppInfo: 'ул.Кирова 68-1',
        google: 'ул. Кирова, 68, Артем, Приморский край, Россия, 692751',
        coordinates: '43,36037:132,208',
        addDate: new Date(moment('14.01.2008', 'DD.MM.YYYY')),
        addCode: 1,
        removeDate: new Date(moment('17.03.2011', 'DD.MM.YYYY')),
        removeCode: 4,
        deathDate: new Date(moment('30.01.2008', 'DD.MM.YYYY')),
        deathMKBCode: 'C16.9',
        diagnosticCode: 1,
        diagnosticDate: new Date(moment('14.01.2008', 'DD.MM.YYYY')),
        diagnosticMKBCode: 'C16.9',
        diagnosticStage: 'IV стадия',
        diagnosticTNM: 'T4 N2 M1',
        diagnosticHowFound: 'обратился сам',
        diagnosticMethod: 'морфологический',
        diagnosticSideOfDefeat: 'неприменимо',
        diagnosticMorphologicalType: 'M8020/3 Недифференцированный рак БДУ',
        diagnosticMetastases: '01. отдален. лимф. узлы 02. кости 07. почки 11. другие органы'
        /*diagnosticAutopsyResult: null,
        therapyRadiation: null,
        therapyOperative: null,
        therapyHormonoImmune: null,
        therapyChemo: null,
        therapySpecial: null,
        lat: null,
        lng: null,
        place: null*/
    }];

//var fields = ['fio', 'dob', 'gender', 'addDate', 'mkbCode', 'mkbState', 'tnm', 'stage', 'removedDate', 'removedCode', 'address', 'district', 'profession', 'lat', 'lng', 'place', 'approve'];

module.exports = function(sequelize, onSuccessAll) {
    CancerData.findAll().then(function(data) {
        if(data && data.length)
            return onSuccessAll();

        async.eachSeries(basicData, function (item, callback) {
            CancerData.create(item).then(function() {callback();});
        }, onSuccessAll);
    });
};