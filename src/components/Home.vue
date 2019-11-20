<template>
  <div class="content">
    <p>Перемножение ключевых фраз с возможностью кластеризации по заголовкам для Яндекс.Директ и Google Ads</p>
    <p>
      <a href="#" class="gray small dashed" v-on:click="setupDefault">Заполнить тестовыми данными</a>&nbsp;&nbsp;&nbsp;&nbsp;
      <a
        href="#"
        class="gray small dashed"
        v-on:click="resetData"
      >Очистить данные</a>
    </p>
    <div class="x-scroll columns">
      <div class="x-scroll__column" v-for="(column, index) in columns" v-bind:key="index">
        <Column v-bind:id="index" v-on:openPopup="openPopup" />
      </div>
      <div class="x-scroll__add">
        <button class="button button--outline" v-on:click="addColumn">+</button>
      </div>
    </div>
    <div class="accordeon">
      <div class="accordeon__title">
        <a
          href="#"
          class="gray dashed"
          v-bind:class="accordeonOpen ? 'arrow-up' : 'arrow-down'"
          v-on:click="toggleAccordeon"
        >Дополнительные параметры</a>
      </div>
      <div class="accordeon__content" v-show="accordeonOpen">
        <Checkbox v-model="props.maxKeyLength">
          Максимальная длина ключа 7 слов
          <Tooltip>Исключает из результатов ключевые слова длиннее 7 слов (такие слова не пропускает Яндекс.Директ в рекламные кампании)</Tooltip>
        </Checkbox>
        <Checkbox v-model="props.plus">
          Добавить «+» к стоп-словам
          <Tooltip>Предлоги и другие стоп-слова будут выделены символом + перед ними (например "Погода в Москве" будет изменено на "Погода +в Москве")</Tooltip>
        </Checkbox>
        <!-- <Checkbox v-model="props.quotes">
          Заключить в ""
          <Tooltip></Tooltip>
        </Checkbox>
        <Checkbox v-model="props.bracets">
          Заключить в []
          <Tooltip></Tooltip>
        </Checkbox>-->
        <Checkbox v-model="props.cluster">
          Кластеризовать
          <Tooltip>Объединяет все сгенерированные ключевые слова в заданное число групп. Генерирует заголовки исходя из заданной длины и приоритета сстолбцов</Tooltip>
        </Checkbox>
        <div v-if="props.cluster">
          <div class="padding-block">
            <a href="#" class="gray dashed" v-on:click="setHeaders($event, 'direct')">Яндекс.Директ</a>&nbsp;&nbsp;&nbsp;
            <a
              href="#"
              class="gray dashed"
              v-on:click="setHeaders($event, 'ads')"
            >Google Ads</a>
          </div>
          <div class="padding-block">
            <label>
              Максимальное количество групп
              <input
                type="text"
                class="input"
                v-model.number="props.clusterCount"
              />
            </label>
          </div>
          <div class="padding-block">
            <label>
              Длина заголовка №1
              <input type="text" class="input" v-model.number="props.headers[0]" />
            </label>
          </div>
          <div class="padding-block">
            <label>
              Длина заголовка №2
              <input type="text" class="input" v-model.number="props.headers[1]" />
            </label>
          </div>
          <div class="padding-block">
            <label>
              Длина заголовка №3
              <input type="text" class="input" v-model.number="props.headers[2]" />
            </label>
          </div>
        </div>
      </div>
    </div>
    <p
      v-if="props.cluster"
      v-bind:class="{ error: isClusterLimit }"
    >Число фраз: {{cartesianSum}}/{{clusterLimit}}</p>
    <p
      v-else
      v-bind:class="{ error: isCartesianLimit }"
    >Число фраз: {{cartesianSum}}/{{cartesianLimit}}</p>
    <p>
      <button
        class="button button--rounded button--pink"
        v-bind:class="{ loading: loading }"
        v-on:click="generate"
      >Генерировать</button>
      &nbsp;&nbsp;&nbsp;
      <a
        href="#"
        class="gray small dashed"
        v-if="result.gen_time"
        v-on:click="resetResult"
      >Удалить результат</a>
    </p>
    <div v-if="result.keywords">
      <h2>Рузльтат</h2>
      <p>
        <span
          class="copy"
          v-on:click="copyTable($event, 'result_area')"
        >скопировать результат в буфер обмена</span>
      </p>
      <textarea class="textarea" id="result_area">{{result.keywords.join("\n")}}</textarea>
    </div>
    <div v-if="result.table">
      <h2>Рузльтат: {{result.num_groups}} групп, {{result.table.length}} ключей</h2>
      <p>
        <span
          class="copy"
          v-on:click="copyTable($event, 'result_table')"
        >скопировать результат в буфер обмена</span>
      </p>
      <div class="x-scroll">
        <table v-if="result.table" class="table" id="result_table">
          <tr v-for="(row, i) in result.table">
            <td v-for="(td, j) in row">{{td}}</td>
          </tr>
        </table>
      </div>
    </div>
    <Popup
      v-if="popup != null"
      v-bind:id="popup"
      v-on:closePopup="closePopup"
      v-on:removeColumn="removeColumn"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";

import Tooltip from "./tooltip.vue";
import Popup from "./popup.vue";
import Column from "./column.vue";
import Checkbox from "./checkbox.vue";

export default {
  name: "Home",
  components: {
    Column,
    Checkbox,
    Popup,
    Tooltip
  },
  data() {
    return {
      props: {
        maxKeyLength: false,
        plus: false,
        quotes: false,
        bracets: false,
        cluster: false,
        clusterCount: 200,
        headers: [35, 30, 0],
        match_words: true
      },
      cartesianLimit: 100000,
      clusterLimit: 20000,
      accordeonOpen: true,
      popup: null,
      loading: false,
      result: []
    };
  },
  computed: {
    cartesianSum: function() {
      var columns = this.columns.slice();

      var result = 1;
      for (let i = 0; i < columns.length; i++) {
        result = result * columns[i].data.length;
      }

      return result;
    },
    isCartesianLimit: function() {
      return this.cartesianSum > this.cartesianLimit;
    },
    isClusterLimit: function() {
      return this.cartesianSum > this.clusterLimit;
    },
    ...mapState(["columns"])
  },
  created() {
    // this.$store.commit("SETUP_EXAMPLE");
  },
  methods: {
    copyTable: function(e, id) {
      e.preventDefault();

      var el = document.getElementById(id);

      var text = el.innerText ? el.innerText : el.value;

      Clipboard.copy(text);

      // var target = e.target;

      // var text = el.innerText ? el.innerText : el.value;

      // navigator.clipboard.writeText(text).then(
      //   function() {
      //     target.classList.add("is-success");
      //     setTimeout(function() {
      //       target.classList.remove("is-success");
      //     }, 1000);
      //   },
      //   function(err) {
      //     target.classList.add("is-error");
      //     setTimeout(function() {
      //       target.classList.remove("is-error");
      //     }, 1000);
      //   }
      // );
    },
    addColumn: function(e) {
      e.preventDefault();

      this.$store.commit("ADD_COLUMN");
    },
    setupDefault: function(e) {
      e.preventDefault();
      var isConfirm = confirm("Данные в колонках будут стерты, продолжить?");
      if (isConfirm) {
        this.$store.commit("SETUP_EXAMPLE");
      }
    },
    resetData: function(e) {
      e.preventDefault();
      var isConfirm = confirm("Вы уверены что хотите очистит данные?");
      if (isConfirm) {
        this.$store.commit("SETUP_DEFAULT");
      }
    },
    removeColumn: function(column) {
      var isConfirm = confirm("Вы уверены что хотите удалить эту колонку?");
      if (isConfirm) {
        this.$store.commit("REMOVE_COLUMN", column);
        this.popup = null;
      }
    },
    toggleAccordeon: function(e) {
      e.preventDefault();
      this.accordeonOpen = !this.accordeonOpen;
    },
    openPopup: function(column) {
      this.popup = column;
    },
    closePopup: function(column) {
      this.popup = null;
    },
    setHeaders: function(e, type) {
      e.preventDefault();
      if (type == "direct") {
        this.props.headers = [35, 30, 0];
      } else if (type == "ads") {
        this.props.headers = [30, 30, 30];
      }
    },
    resetResult: function(e) {
      e.preventDefault();
      var isConfirm = confirm("Вы уверены что хотите удалить результаты?");
      if (isConfirm) {
        this.result = [];
      }
    },
    generate: function(e) {
      e.preventDefault();
      if (this.props.cluster && this.isClusterLimit) {
        alert(
          "Количество сгенерированных слов больше " +
            this.clusterLimit +
            " штук"
        );
      } else if (this.isCartesianLimit) {
        alert(
          "Количество сгенерированных слов больше " +
            this.cartesianLimit +
            " штук"
        );
      } else {
        var that = this;
        if (!this.loading) {
          this.loading = true;
          this.result = [];

          axios
            .post("/api/v1.0/generate", {
              columns: this.columns,
              props: this.props
            })
            .then(function(response) {
              that.loading = false;
              that.result = response.data;
            })
            .catch(function(error) {
              that.loading = false;
            });
        }
      }
    }
  }
};

window.Clipboard = (function(window, document, navigator) {
  var textArea, copy;

  function isOS() {
    return navigator.userAgent.match(/ipad|iphone/i);
  }

  function createTextArea(text) {
    textArea = document.createElement("textArea");
    textArea.value = text;
    document.body.appendChild(textArea);
  }

  function selectText() {
    var range, selection;

    if (isOS()) {
      range = document.createRange();
      range.selectNodeContents(textArea);
      selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      textArea.setSelectionRange(0, 999999);
    } else {
      textArea.select();
    }
  }

  function copyToClipboard() {
    document.execCommand("copy");
    document.body.removeChild(textArea);
  }

  copy = function(text) {
    createTextArea(text);
    selectText();
    copyToClipboard();
  };

  return {
    copy: copy
  };
})(window, document, navigator);
</script>

<style>
.error {
  color: #f00;
}
.gray {
  color: #aeaeae;
}
.small {
  font-size: 14px;
}
.copy {
  font-size: 14px;
  vertical-align: baseline;
  font-weight: normal;
  cursor: pointer;
  color: #267aff;
  text-decoration: underline;
  display: block;

  &.is-success,
  &.is-error {
    &:after {
      content: "Успешно скопировано";
      position: fixed;
      left: 50%;
      top: 50%;
      pointer-events: none;
      max-width: 80vw;
      transform: translate(-50%, -50%);
      display: block;
      background: rgba(0, 0, 0, 0.8);
      border-radius: 5px;
      padding: 10px 20px;
      text-align: center;
      color: #fff;
      animation: flowUp 1s forwards;
      z-index: 100;
    }
  }

  &.is-error {
    &:after {
      content: "Не получилось, попробуй руками";
    }
  }

  &:hover {
    text-decoration: none;
  }

  &:active {
    color: #1559c5;
  }

  &:before {
    content: "";
    width: 20px;
    height: 24px;
    margin-right: 4px;
    background-repeat: no-repeat;
    background-position: center center;
    vertical-align: middle;
    display: inline-block;
    background-size: contain;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' version='1.1' x='0px' y='0px' viewBox='0 0 100 125' style='enable-background:new 0 0 100 100;' xml:space='preserve'%3E%3Cg%3E%3Cpath d='M36,38h20c1.1,0,2-0.9,2-2s-0.9-2-2-2H36c-1.1,0-2,0.9-2,2S34.9,38,36,38z'/%3E%3Cpath d='M36,48h20c1.1,0,2-0.9,2-2s-0.9-2-2-2H36c-1.1,0-2,0.9-2,2S34.9,48,36,48z'/%3E%3Cpath d='M36,58h20c1.1,0,2-0.9,2-2s-0.9-2-2-2H36c-1.1,0-2,0.9-2,2S34.9,58,36,58z'/%3E%3Cpath d='M36,68h20c1.1,0,2-0.9,2-2s-0.9-2-2-2H36c-1.1,0-2,0.9-2,2S34.9,68,36,68z'/%3E%3Cpath d='M27.09,80h37.82c2.81,0,5.09-2.28,5.09-5.09V27.09c0-2.81-2.28-5.09-5.09-5.09H27.09C24.28,22,22,24.28,22,27.09v47.82 C22,77.72,24.28,80,27.09,80z M26,27.09c0-0.6,0.49-1.09,1.09-1.09h37.82c0.6,0,1.09,0.49,1.09,1.09v47.82 c0,0.6-0.49,1.09-1.09,1.09H27.09c-0.6,0-1.09-0.49-1.09-1.09V27.09z'/%3E%3Cpath d='M74.91,12H37.09C34.28,12,32,14.28,32,17.09c0,1.1,0.9,2,2,2s2-0.9,2-2c0-0.6,0.49-1.09,1.09-1.09h37.82 c0.6,0,1.09,0.49,1.09,1.09v47.82c0,0.6-0.49,1.09-1.09,1.09c-1.1,0-2,0.9-2,2s0.9,2,2,2c2.81,0,5.09-2.28,5.09-5.09V17.09 C80,14.28,77.72,12,74.91,12z'/%3E%3C/g%3E%3C/svg%3E");
  }
}

@keyframes flowUp {
  0% {
    opacity: 0;
    margin-top: 50px;
  }
  20% {
    opacity: 1;
    margin-top: 0px;
  }

  80% {
    opacity: 1;
    margin-top: 0px;
  }
  100% {
    opacity: 0;
    margin-top: -50px;
  }
}

.dashed {
  text-decoration: none !important;
  border-bottom: 0.5px dashed;
  white-space: nowrap;

  &:hover {
    border-bottom-color: transparent;
  }
}

.textarea {
  width: 100%;
  min-height: 400px;
}
.columns {
  padding: 10px 0;
}
.x-scroll {
  overflow-x: auto;
  display: flex;
  flex-wrap: nowrap;
  margin: 0 -10px 20px;
}
.x-scroll__column {
  flex: 240px 0 0;
  padding: 0 10px;
}
.x-scroll__add {
  flex: 40px 0 0;
  display: flex;
  align-items: center;

  & .button {
    margin-top: 27px;
    padding: 8px;
    width: 40px;
    height: 40px;
    align-items: center;
    justify-content: center;
    display: flex;
    font-size: 24px;
    color: #7e96b6 !important;
  }
}
.accordeon {
}
.accordeon__title {
  margin-bottom: 8px;
}
.arrow-up,
.arrow-down {
  display: inline-block;
  position: relative;

  &:after {
    content: "";
    display: block;
    position: absolute;
    top: 50%;
    left: 100%;
    margin-left: 4px;
    width: 0;
    height: 0;
  }
}
.arrow-up {
  &:after {
    border-top: 0;
    border-bottom: 3px solid #aeaeae;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
  }
}
.arrow-down {
  &:after {
    border-bottom: 0;
    border-top: 3px solid #aeaeae;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
  }
}
.padding-block {
  margin-bottom: 8px;
  padding-left: 42px;
}
.input {
  display: inline-block;
  vertical-align: middle;
  background: #ffffff;
  border: 1px solid #e2e7ef;
  border-radius: 5px;
  padding: 4px 8px;
  line-height: 24px;
  min-width: 40px;
  width: 60px;
  vertical-align: middle;
}
.table {
  position: relative;
  border-collapse: collapse;
  padding: 0;
  border: 1px solid #ccc;
  counter-reset: rows;
  margin-left: 40px;

  & tr {
    position: relative;

    &:not(:first-child) {
      counter-increment: rows;
    }

    &:first-child:before {
      content: "";
    }

    &:not(:first-child):before {
      content: counter(rows);
      display: block;
      position: absolute;
      left: -40px;
      line-height: 17px;
      text-align: right;
      font-size: 10px;
      width: 40px;
      padding: 3px 6px;
      box-sizing: border-box;
      color: #999;
    }
  }

  & td {
    padding: 3px 6px;
    border: 1px solid #ccc;
    white-space: nowrap;
    font-size: 14px;
  }
}
</style>