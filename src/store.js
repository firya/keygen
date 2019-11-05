import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    columns: [
      {
        priority: 1,
        data: [],
        decl: []
      },
      {
        priority: 1,
        data: [],
        decl: []
      },
      {
        priority: 1,
        data: [],
        decl: []
      }
    ]
  },
  actions: {

  },
  mutations: {
    SET_COLUMN_DATA: function (state, payload) {
      state.columns[payload.id][payload.prop] = payload.value;
    },
    SET_DECL: function (state, payload) {
      state.columns[payload.column].decl[payload.row][payload.prop] = payload.value;
    },
    ADD_COLUMN: function (state, payload) {
      state.columns.push({
        priority: 1.0,
        data: [""],
        decl: []
      });
    },
    ADD_DECL_ROW: function (state, payload) {
      state.columns[payload.column].decl.push({
        column: 0,
        word: "",
        form: ""
      });
    },
    REMOVE_COLUMN: function (state, payload) {
      state.columns.splice(payload, 1);
    },
    SETUP_DEFAULT: function (state, payload) {
      state.columns = [
        {
          priority: 1.0,
          data: [""],
          decl: []
        },
        {
          priority: 1.0,
          data: [""],
          decl: []
        },
        {
          priority: 1.0,
          data: [""],
          decl: []
        }
      ];
    },
    SETUP_EXAMPLE: function (state, payload) {
      state.columns = [
        {
          priority: 0.7,
          data: ["", "купить", "заказать", "магазин", "цены на"],
          decl: []
        },
        {
          priority: 0.2,
          data: ["", "серые", "коричневые", "черные"],
          decl: []
        },
        {
          priority: 0.8,
          data: ["пластиковые", "деревянные", "оловянные", "алюминиевые", "мифриловые", "легендарыне"],
          decl: [
            {
              col: 0,
              word: "магазин",
              form: "пластиковых"
            }
          ]
        },
        {
          priority: 1.0,
          data: ["окна", "двери", "заборы", "лестницы", "ножницы", "столы", "стулья"],
          decl: [
            {
              col: 0,
              word: "магазин",
              form: "окон"
            }
          ]
        },
        {
          priority: 0.5,
          data: [
            "с доставкой",
            "с установкой",
            "с доставкой и установкой",
            "на заказ"
          ],
          decl: []
        },
        {
          priority: 0.9,
          data: ["", "в Москве", "в Подольске", "в Серпухове", "в Клину", "в Химках", "в Пушкине", "в Сергиевом Посаде", "в Щербинке"],
          decl: []
        },
        {
          priority: 0.4,
          data: ["", "сегодня", "срочно"],
          decl: []
        }
      ];
    }
  },
  getters: {

  }
});