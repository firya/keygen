<template>
  <div class="column">
    <div class="column__header">
      <div class="column__title">Столбец #{{(id+1)}}</div>
      <div class="column__priority">(приоритет: {{priorityFloat}})</div>
      <div class="column__settings">
        <button class="button button--s" v-on:click="$emit('openPopup', id)">
          <Gear />
        </button>
      </div>
    </div>
    <div class="column__content">
      <textarea class="textarea" v-bind:value="linedValue" v-on:input="changeData"></textarea>
    </div>
  </div>
</template>

<script>
import { mapState } from "vuex";

import Gear from "../assets/icon-gear.svg";

export default {
  name: "column",
  props: {
    priority: Number,
    value: Array,
    id: Number
  },
  computed: {
    ...mapState(["columns"]),
    linedValue: function() {
      return this.columns[this.id].data.join("\n");
    },
    priorityFloat: function() {
      return Number.parseFloat(this.columns[this.id].priority).toFixed(1);
    }
  },
  data() {
    return {};
  },
  components: {
    Gear
  },
  methods: {
    changeData: function(e) {
      var value = e.target.value;
      this.$store.commit("SET_COLUMN_DATA", {
        id: this.id,
        prop: "data",
        value: value.split("\n")
      });
    }
  }
};
</script>

<style>
.textarea {
  background: #ffffff;
  border: 1px solid #e2e7ef;
  border-radius: 5px;
  padding: 8px;
}
.column {
}
.column__header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 8px;
}
.column__title {
  font-size: 14px;
  margin-right: 20px;
}
.column__priority {
  font-size: 12px;
  color: #9a9a9a;
  flex: 1;
}
.column__settings {
  margin-left: auto;
}
.column__content {
  & .textarea {
    min-height: 200px;
    width: 100%;
  }
}
.button {
  appearance: none;
  -webkit-appearance: none;
  border: 1px solid #b054ff;
  background-color: #b054ff;
  border-radius: 5px;
  margin: 0;
  padding: 8px;
  line-height: 24px;
  cursor: pointer;
  color: #fff;

  &.button--s {
    line-height: 14px;
    padding: 4px;
  }

  &.button--outline {
    background: #ffffff;
    border: 1px solid #e2e7ef;
  }
  &.button--rounded {
    border-radius: 100px;
    padding-left: 16px;
    padding-right: 16px;
  }
  &.button--pink {
    background-color: #ff5c9b;
    border-color: #ff5c9b;
  }
  &.loading {
    cursor: default;

    &:after {
      content: "";
      display: inline-block;
      border-radius: 100%;
      width: 13px;
      height: 13px;
      border: 2px solid currentColor;
      border-left-color: transparent;
      vertical-align: middle;
      margin-left: 10px;
      animation: rotate 1s infinite;
    }
  }
}

@keyframes rotate {
  0% {
    transform: rotate(-360deg);
  }
  20% {
    transform: rotate(-360deg);
  }
}
</style>