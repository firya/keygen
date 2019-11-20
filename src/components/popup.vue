<template>
  <div class="popup">
    <div class="popup__overlay">
      <div class="popup__block">
        <div class="popup__close" v-on:click="$emit('closePopup')">
          <Cross />
        </div>
        <div class="popup__title">Столбец {{(id+1)}}</div>
        <div class="popup__content">
          <label>
            Приоритет
            <br />
            <select class="select" v-bind:value="columns[id].priority" v-on:change="changePriority">
              <option v-for="n in 11" v-bind:key="n">{{(n-1)/10}}</option>
            </select>
          </label>
          <p>
            <b>Склонение слов в заголовках</b>
          </p>
          <div class="row" v-for="(row, i) in columns[id].decl" v-bind:key="i">
            <div class="col col--padding">
              <div v-on:click="removeDeclRow($event, i)" class="row__remove">
                <Remove />
              </div>
            </div>
            <div class="col">
              <label>
                Если в столбце №
                <br />
                <select
                  class="select"
                  v-bind:value="row.column+1"
                  v-on:change="changeDecl($event, (i - 1), 'column')"
                >
                  <option v-for="n in columns.length" v-bind:key="n">{{n}}</option>
                </select>
              </label>
            </div>
            <div class="col">
              <label>
                Встречается слово
                <br />
                <input
                  class="input"
                  v-bind:value="row.word"
                  v-on:change="changeDecl($event, i, 'word')"
                />
              </label>
            </div>
            <div class="col">
              <label>
                Использовать словоформу
                <br />
                <input
                  class="input"
                  v-bind:value="row.form"
                  v-on:change="changeDecl($event, i, 'form')"
                />
              </label>
            </div>
          </div>
          <p>
            <a href="#" class="dashed" v-on:click="addDeclRow">Добавить правило</a>
          </p>

          <p class="text-right small">
            <a href="#" class="dashed red" v-on:click="$emit('removeColumn', id)">Удалить колонку</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import Cross from "../assets/cross.svg";
import Remove from "../assets/remove.svg";

export default {
  name: "popup",
  components: {
    Cross,
    Remove
  },
  props: {
    id: Number
  },
  computed: {
    ...mapState(["columns"])
  },
  data() {
    return {};
  },
  methods: {
    changePriority: function(e) {
      e.preventDefault();

      this.$store.commit("SET_COLUMN_DATA", {
        id: this.id,
        prop: "priority",
        value: e.target.value
      });
    },
    addDeclRow: function(e) {
      e.preventDefault();

      this.$store.commit("ADD_DECL_ROW", {
        column: this.id
      });
    },
    removeDeclRow: function(e, i) {
      e.preventDefault();

      this.$store.commit("REMOVE_DECL_ROW", {
        column: this.id,
        row: i
      });
    },
    changeDecl: function(e, row, prop) {
      e.preventDefault();

      this.$store.commit("SET_DECL", {
        column: this.id,
        row: row,
        prop: prop,
        value: e.target.value
      });
    }
  }
};
</script>

<style>
.red {
  color: #f00;
}
.text-right {
  text-align: right;
}
.popup {
  position: fixed;
  overflow: hidden;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  display: flex;
  background-color: rgba(0, 0, 0, 0.6);
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
}
.popup__overlay {
  overflow: auto;
  width: 100%;
}
.popup__block {
  position: relative;
  flex: 0 0 auto;
  background-color: #fff;
  border-radius: 5px;
  margin: 1em auto;
  max-width: 600px;
  padding: 20px;
}
.popup__close {
  position: absolute;
  right: 10px;
  top: 10px;
  padding: 10px;
  cursor: pointer;
}
.popup__title {
  font-size: 18px;
  font-weight: bold;
  padding-right: 30px;
  margin-bottom: 16px;
}
.select {
  background: #ffffff;
  border: 1px solid #e2e7ef;
  border-radius: 5px;
  padding: 8px;
  height: 32px;
  line-height: 16px;
  min-width: 80px;
}
.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -4px 8px;
}
.row__remove {
  width: 20px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.col {
  padding: 0 4px;
  margin-bottom: 10px;

  &:last-child {
    flex: 1;
  }

  & .input {
    width: 100%;
  }

  &.col--padding {
    padding-top: 20px;
  }
}
</style>