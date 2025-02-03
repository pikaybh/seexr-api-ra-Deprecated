<template>
  <div>
    <h1>Login</h1>
    <LoginForm @login-success="handleLoginSuccess" />
    <p v-if="apiKey">Your API Key: {{ apiKey }}</p>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue';

export default {
  components: {
    LoginForm
  },
  data() {
    return {
      apiKey: ''
    };
  },
  methods: {
    handleLoginSuccess(apiKey) {
      this.apiKey = apiKey;
    }
  }
};
</script>