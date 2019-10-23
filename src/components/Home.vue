<template>
  <div class="content">
    <p>Перемножение ключевых фраз с возможностью кластеризации по заголовкам для Яндекс.Директ</p>
    <p>
      <a href="#" class="gray small dashed" v-on:click="setupDefault">Заполнить тестовыми данными</a>&nbsp;&nbsp;&nbsp;&nbsp;
      <a
        href="#"
        class="gray small dashed"
        v-on:click="resetData"
      >Очистить данные</a>
    </p>
    <div class="x-scroll">
      <div class="x-scroll__column" v-for="(column, index) in columns">
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
        <Checkbox v-model="props.plus">
          Доавить «+» к стоп-словам
          <Tooltip></Tooltip>
        </Checkbox>
        <Checkbox v-model="props.quotes">
          Заключить в ""
          <Tooltip></Tooltip>
        </Checkbox>
        <Checkbox v-model="props.bracets">
          Заключить в []
          <Tooltip></Tooltip>
        </Checkbox>
        <Checkbox v-model="props.cluster">
          Кластеризовать
          <Tooltip></Tooltip>
        </Checkbox>
        <div v-if="props.cluster">
          <div class="padding-block">
            <label>
              Количество класетров
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
              <input type="text" class="input" v-model.number="props.header1" />
            </label>
          </div>
          <div class="padding-block">
            <label>
              Длина заголовка №2
              <input type="text" class="input" v-model.number="props.header2" />
            </label>
          </div>
        </div>
      </div>
    </div>
    <p v-bind:class="{ error: isCartesianLimit }">Число фраз: {{cartesianSum}}/{{cartesianLimit}}</p>
    <button class="button button--rounded button--pink" v-on:click="generate">Сгенерировать</button>
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
        plus: true,
        quotes: false,
        bracets: false,
        cluster: false,
        clusterCount: 200,
        header1: 35,
        header2: 30
      },
      cartesianLimit: 100000,
      accordeonOpen: true,
      popup: null
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
    ...mapState(["columns"])
  },
  methods: {
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
    generate: function(e) {
      e.preventDefault();
      if (this.isCartesianLimit) {
        alert(
          "Количество сгенерированных слов больше " +
            this.cartesianLimit +
            " штук"
        );
      } else {
        axios
          .post("/generate", {
            columns: this.columns,
            props: this.props
          })
          .then(function(response) {
            console.log(response);
          })
          .catch(function(error) {
            console.log(error);
          });
      }
    }
  }
};
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
.dashed {
  text-decoration: none !important;
  border-bottom: 0.5px dashed;
  white-space: nowrap;

  &:hover {
    border-bottom-color: transparent;
  }
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
</style>