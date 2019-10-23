import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    columns: [
      {
        priority: 0.6,
        data: ["1", "2"],
        decl: []
      },
      {
        priority: 0.7,
        data: ["3", "4", "5"],
        decl: [
          {
            column: 2,
            word: "слово",
            form: "словоформа"
          }
        ]
      },
      {
        priority: 0.8,
        data: ["6", "7", "8", "9"],
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
          priority: 0.8,
          data: ["Купить", "Заказать", "Магазин"],
          decl: []
        },
        {
          priority: 0.9,
          data: ["", "пластиковые", "деревянные"],
          decl: []
        },
        {
          priority: 1.0,
          data: ["окна"],
          decl: []
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
          priority: 0.4,
          data: ["", "в Москве"],
          decl: []
        }
      ];
    }
  },
  getters: {

  }
});