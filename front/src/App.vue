<template>
  <div v-for="match in info" :key="match.id">
    <table class="court" style="margin: 15px;">
      <tr>
        <td>{{ match.pair1.player1.name }}</td>
        <td>{{ match.pair1.player2.name }}</td>
      </tr>
      <tr>
        <td>vs</td>
      </tr>
      <tr>
        <td>{{ match.pair2.player1.name }}</td>
        <td>{{ match.pair2.player2.name }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      info: null
    }
  },
  mounted() {
    axios
      .get('http://localhost:8000')
      .then(res => (this.info = res.data.matchs))
      .catch((error) => console.log(error));
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
table,
th,
td {
  border: 1px solid;
}
</style>
