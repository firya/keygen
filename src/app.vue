<template>
  <div class="page">
    <header class="header">
      <Logo class="logo" />
      <div class="header__title">Генератор ключевых слов</div>
    </header>
    <router-view></router-view>
  </div>
</template>

<script>
import Logo from "./assets/logo.svg";

export default {
  name: "App",
  data() {
    return {
      text: "App!"
    };
  },
  components: {
    Logo
  }
};
</script>

<style>
@import "normalize.css";
@import url("https://fonts.googleapis.com/css?family=PT+Sans:400,400i,700&display=swap&subset=cyrillic");
body {
  font-family: "PT Sans", sans-serif;
  color: #525252;
}
* {
  box-sizing: border-box;
}
a {
  &:hover {
    text-decoration: none;
  }
  &:visited {
  }
}
.page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}
.header {
  padding: 20px 0;
  display: flex;
  align-items: center;
}
.logo {
  margin-right: 16px;
}
.header__title {
  font-size: 21px;
  font-weight: bold;
}
</style>