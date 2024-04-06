<template>
  <div>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="username" />
      <input v-model="password" type="password" placeholder="password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    login() {
      // Here, you would handle the login logic, such as sending a request to your server.
      // For demonstration purposes, we'll just console.log the credentials.
      console.log(this.username, this.password);
      // Ideally, replace the console.log with real authentication logic.
    },
    say(message) {
      alert(message);
    }
  }
}
</script>

<style>
/* You can add your styles here */
</style>
