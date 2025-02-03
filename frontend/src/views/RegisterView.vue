<template>
    <div>
        <h1>Register</h1>
        <RegisterForm @register-success="handleRegisterSuccess" />
        <p v-if="apiKey">Your API Key: {{ apiKey }}</p>
    </div>
</template>

<script>
import RegisterForm from '@/components/RegisterForm.vue';

export default {
    components: {
        RegisterForm
    },
    data() {
        return {
            apiKey: ''
        };
    },
    methods: {
        handleRegisterSuccess(apiKey) {
            this.apiKey = apiKey;
        }
    }
};
</script>