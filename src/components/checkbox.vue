<template>
  <div>
    <label class="checkbox">
      <input
        class="checkbox__hidden"
        type="checkbox"
        v-bind:checked="value"
        v-on:input="$emit('input', $event.target.checked)"
      />
      <div class="checkbox__fake">
        <Check v-if="value" class="checkbox__check" />
      </div>
      <div class="checkbox__label">
        <slot></slot>
      </div>
    </label>
  </div>
</template>

<script>
import Check from "../assets/check.svg";

export default {
  name: "checkbox",
  props: {
    value: Boolean
  },
  components: {
    Check
  },
  data() {
    return {};
  }
};
</script>

<style>
.checkbox {
  display: inline-block;
  cursor: pointer;
  margin-bottom: 8px;
}
.checkbox__hidden {
  width: 1px;
  height: 1px;
  opacity: 0.001;

  &:checked + .checkbox__fake {
  }
}
.checkbox__fake {
  position: relative;
  display: inline-block;
  vertical-align: middle;
  background: #ffffff;
  border: 1px solid #e2e7ef;
  border-radius: 5px;
  width: 20px;
  height: 20px;
  margin: 4px 8px 4px 4px;
}
.checkbox__check {
  position: absolute;
  left: 3px;
  top: -2px;
}
.checkbox__label {
  display: inline;
  vertical-align: middle;
}
</style>