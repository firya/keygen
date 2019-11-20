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
        col: 0,
        word: "",
        form: ""
      });
    },
    REMOVE_DECL_ROW: function (state, payload) {
      state.columns[payload.column].decl.splice(payload.row, 1);
    },
    REMOVE_COLUMN: function (state, payload) {
      console.log(payload)
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
          priority: 0.8,
          data: ["пластиковые", "деревянные", "алюминиевые"],
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
          data: ["окна"],
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
          data: ["", "в Москве", "в Московской области"],
          decl: []
        }
      ];
      // state.columns = [
      //   {
      //     priority: 0.6,
      //     data: ["", "купить", "заказать", "магазин"],
      //     decl: []
      //   },
      //   {
      //     priority: 0.8,
      //     data: ["", "входные", "входные металлические", "металлические", "стальные", "железные"],
      //     decl: [
      //       {
      //         col: 0,
      //         word: "магазин",
      //         form: "входных"
      //       }
      //     ]
      //   },
      //   {
      //     priority: 1.0,
      //     data: ["двери"],
      //     decl: [
      //       {
      //         col: 0,
      //         word: "магазин",
      //         form: "окон"
      //       }
      //     ]
      //   },
      //   {
      //     priority: 0.7,
      //     data: [
      //       "в квартиру"
      //     ],
      //     decl: []
      //   },
      //   {
      //     priority: 0.5,
      //     data: [
      //       "",
      //       "с доставкой",
      //       "с установкой",
      //       "на заказ",
      //       "под ключ"
      //     ],
      //     decl: []
      //   },
      //   {
      //     priority: 0.9,
      //     data: [
      //       "",
      //       "Москвоская область",
      //       "Апрелевка",
      //       "Балашиха",
      //       "Бронницы",
      //       "Верея",
      //       "Видное",
      //       "Волоколамск",
      //       "Воскресенск",
      //       "Высоковск",
      //       "Голицыно",
      //       "Дедовск",
      //       "Дзержинский",
      //       "Дмитров",
      //       "Долгопрудный",
      //       "Домодедово",
      //       "Дрезна",
      //       "Дубна",
      //       "Егорьевск",
      //       "Железнодорожный",
      //       "Жуковский",
      //       "Зарайск",
      //       "Звенигород",
      //       "Ивантеевка",
      //       "Истра",
      //       "Кашира",
      //       "Климовск",
      //       "Клин",
      //       "Коломна",
      //       "Королёв",
      //       "Котельники",
      //       "Красноармейск",
      //       "Красногорск",
      //       "Краснозаводск",
      //       "Краснознаменск",
      //       "Кубинка",
      //       "Куровское",
      //       "Ликино-Дулёво",
      //       "Лобня",
      //       "Лосино-Петровский",
      //       "Луховицы",
      //       "Лыткарино",
      //       "Люберцы",
      //       "Можайск",
      //       "Московский",
      //       "Мытищи",
      //       "Наро-Фоминск",
      //       "Ногинск",
      //       "Одинцово",
      //       "Ожерелье",
      //       "Озёры",
      //       "Орехово-Зуево",
      //       "Павловский Посад",
      //       "Пересвет",
      //       "Подольск",
      //       "Протвино",
      //       "Пушкино",
      //       "Пущино",
      //       "Раменское",
      //       "Реутов",
      //       "Рошаль",
      //       "Руза",
      //       "Сергиев Посад",
      //       "Серпухов",
      //       "Солнечногорск",
      //       "Старая Купавна",
      //       "Ступино",
      //       "Талдом",
      //       "Троицк",
      //       "Фрязино",
      //       "Химки",
      //       "Хотьково",
      //       "Черноголовка",
      //       "Чехов",
      //       "Шатура",
      //       "Щёлково",
      //       "Щербинка",
      //       "Электрогорск",
      //       "Электросталь",
      //       "Электроугли",
      //       "Юбилейный",
      //       "Яхрома",
      //       "Москва",
      //       // "Академический",
      //       // "Алексеевский",
      //       // "Алтуфьевский",
      //       // "Арбат",
      //       // "Аэропорт",
      //       // "Бабушкинский",
      //       // "Басманный",
      //       // "Беговой",
      //       // "Бескудниковский",
      //       // "Бибирево",
      //       // "Бирюлёво Восточное",
      //       // "Бирюлёво Западное",
      //       // "Богородское",
      //       // "Братеево",
      //       // "Бутово",
      //       // "Бутырский",
      //       // "Вешняки",
      //       // "Внуково",
      //       // "Войковский",
      //       // "Восточное Дегунино",
      //       // "Восточное Измайлово",
      //       // "Восточный",
      //       // "Выхино-Жулебино",
      //       // "Гагаринский",
      //       // "Головинский",
      //       // "Гольяново",
      //       // "Даниловский",
      //       // "Дегунино",
      //       // "Дмитровский",
      //       // "Донской",
      //       // "Дорогомилово",
      //       // "Замоскворечье",
      //       // "Западное Дегунино",
      //       // "Зюзино",
      //       // "Зябликово",
      //       // "Ивановское",
      //       // "Измайлово",
      //       // "Капотня",
      //       // "Коньково",
      //       // "Коптево",
      //       // "Косино-Ухтомский",
      //       // "Котловка",
      //       // "Красносельский",
      //       // "Крылатское",
      //       // "Крюково",
      //       // "Кузьминки",
      //       // "Кунцево",
      //       // "Куркино",
      //       // "Левобережный",
      //       // "Лефортово",
      //       // "Лианозово",
      //       // "Ломоносовский",
      //       // "Лосиноостровский",
      //       // "Люблино",
      //       // "Марфино",
      //       // "Марьина Роща",
      //       // "Марьино",
      //       // "Матушкино",
      //       // "Медведково",
      //       // "Метрогородок",
      //       // "Мещанский",
      //       // "Митино",
      //       // "Можайский",
      //       // "Молжаниновский",
      //       // "Москворечье-Сабурово",
      //       // "Нагатино-Садовники",
      //       // "Нагатинский Затон",
      //       // "Нагорный",
      //       // "Некрасовка",
      //       // "Нижегородский",
      //       // "Ново-Переделкино",
      //       // "Новогиреево",
      //       // "Новокосино",
      //       // "Обручевский",
      //       // "Орехово-Борисово",
      //       // "Орехово-Борисово Северное",
      //       // "Орехово-Борисово Южное",
      //       // "Останкинский",
      //       // "Отрадное",
      //       // "Очаково-Матвеевское",
      //       // "Перово",
      //       // "Печатники",
      //       // "Покровское-Стрешнево",
      //       // "Преображенское",
      //       // "Пресненский",
      //       // "Проспект Вернадского",
      //       // "Раменки",
      //       // "Ростокино",
      //       // "Рязанский",
      //       // "Савёлки",
      //       // "Савёловский",
      //       // "Свиблово",
      //       // "Северное Бутово",
      //       // "Северное Измайлово",
      //       // "Северное Медведково",
      //       // "Северное Тушино",
      //       // "Северный",
      //       // "Силино",
      //       // "Сокол",
      //       // "Соколиная Гора",
      //       // "Сокольники",
      //       // "Солнцево",
      //       // "Старое Крюково",
      //       // "Строгино",
      //       // "Таганский",
      //       // "Тверской",
      //       // "Текстильщики",
      //       // "Тёплый Стан",
      //       // "Тимирязевский",
      //       // "Тропарёво-Никулино",
      //       // "Тушино",
      //       // "Филёвский Парк",
      //       // "Фили",
      //       // "Фили-Давыдково",
      //       // "Хамовники",
      //       // "Ховрино",
      //       // "Хорошёво-Мнёвники",
      //       // "Хорошёвский",
      //       // "Царицыно",
      //       // "Черёмушки",
      //       // "Чертаново Северное",
      //       // "Чертаново Центральное",
      //       // "Чертаново Южное",
      //       // "Щукино",
      //       // "Южное Бутово",
      //       // "Южное Медведково",
      //       // "Южное Тушино",
      //       // "Южнопортовый",
      //       // "Якиманка",
      //       // "Ярославский",
      //       // "Ясенево",
      //     ],
      //     decl: []
      //   }
      // ];
    }
  },
  getters: {

  }
});