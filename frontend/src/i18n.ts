import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'

const resources = {
  ru: {
    translation: {
      nav: {
        map: 'Карта',
        charts: 'Аналитика',
        cases: 'Случаи',
        appTitle: 'МедГео Аналитика',
      },
      common: {
        loading: 'Загрузка данных…',
        noDataPeriod: 'Нет данных для выбранного периода',
        back: 'Назад',
        apply: 'Применить',
        reset: 'Сбросить',
        details: 'Подробнее',
        notSpecified: 'Не указано',
      },
      filters: {
        title: 'Фильтры',
        dateFrom: 'Дата с',
        dateTo: 'Дата по',
        level: 'Уровень территории',
        territory: 'Территория',
        mkb: 'Код МКБ-10',
        gdu: 'Группа диспансерного учёта',
        cv: 'КВ',
        mbt: 'МБТ',
      },
      map: {
        title: 'Карта распространения',
        subtitle: 'Мониторинг по территориям и выбранным фильтрам',
        readyNoGeometry:
          'Карта готова к работе, но не загружены территориальные границы/геоданные',
        localTilesUnavailable: 'Локальная картографическая подложка не подключена',
        selectTerritory: 'Выберите территорию на карте',
        summary: 'Сводка по территории',
        caseCount: 'Количество случаев',
        mbtPositive: 'МБТ+',
        cvPositive: 'КВ+',
        childrenCount: 'Дети',
        incidence: 'Заболеваемость на 100 тыс.',
        mapHint: 'Подложка подключена. Для хлороплета требуется GeoJSON/границы.',
      },
      charts: {
        title: 'Аналитические срезы',
        yearly: 'Динамика по годам',
        mkb: 'Структура по МКБ',
        age: 'Структура по возрасту',
      },
      cases: {
        title: 'Реестр случаев',
        id: 'ID',
        date: 'Дата регистрации',
        diagnosis: 'Диагноз',
        actions: 'Действия',
        prev: 'Назад',
        next: 'Далее',
        detailsTitle: 'Случай №{{id}}',
        patient: 'Пациент ID',
      },
      error: {
        title: 'Не удалось загрузить данные',
        code: 'Код ошибки',
      },
      debug: {
        backend: 'Статус backend',
      },
      widgets: {
        total: 'Всего случаев',
        territories: 'Территорий в выборке',
        period: 'Период',
      },
    },
  },
}

void i18n.use(initReactI18next).init({
  resources,
  lng: 'ru',
  fallbackLng: 'ru',
  interpolation: { escapeValue: false },
})

export default i18n
