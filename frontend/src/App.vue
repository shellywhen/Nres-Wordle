<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link>
      |
      <router-link to="/create">Create</router-link>  
      |
      <router-link to="/geography">Geo</router-link>  
      |
      <router-link to="/gallery">Gallery</router-link>
      |
      <a href="https://github.com/jasondavies/d3-cloud" target="_blank">API</a>

    </div>
    <router-view/>
  </div>
</template>

<style lang="less">
#app {
  font-family: '微软雅黑', Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  a {
    font-weight: bold;
    color: #2c3e50;
    text-decoration: none;
    &.router-link-exact-active {
      color: #4ca4dd;
    }
  }
}
</style>
