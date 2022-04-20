<template>
  <div id="app">
<div class="headerIcon">

    <i class="material-icons md-60">
sticky_note_2
</i>
</div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.material-icons.md-60 { font-size: 60px; }
.headerIcon {
  margin-top: -60px;
  margin-bottom: 20px;
  
}
</style>
