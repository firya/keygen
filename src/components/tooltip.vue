<template>
  <div class="tooltip">
    <div class="tooltip_mark">?</div>
    <div class="tooltip_block">
      <div class="tooltip__content">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "tooltip",
  props: {
    title: String
  },
  data() {
    return {};
  }
};
</script>

<style>
.tooltip {
  display: inline-block;
  position: relative;
}
.tooltip_mark {
  width: 16px;
  height: 16px;
  border-radius: 8px;
  background-color: #efeeee;
  color: #b0b0b0;
  font-size: 10px;
  text-align: center;
  line-height: 16px;

  &:hover {
    & + .tooltip_block {
      display: block;
    }
  }
}
.tooltip_block {
  display: none;
  position: absolute;
  border-radius: 5px;
  background-color: #444;
  padding: 4px 8px;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #fff;
  margin-left: 8px;
  min-height: 16px;

  &:after {
    content: "";
    display: block;
    position: absolute;
    width: 0;
    height: 0;
    right: 100%;
    top: 50%;
    transform: translateY(-50%);
    border-top: 4px solid transparent;
    border-right: 4px solid #444;
    border-bottom: 4px solid transparent;
    border-left: none;
  }
}
</style>