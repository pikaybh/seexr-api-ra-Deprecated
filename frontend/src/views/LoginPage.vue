<template>
    <div class="login-page">
        <Header />
        <Login />
    </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Login from '@/components/Login.vue';

export default {
    components: { Header, Login },
};
</script>

<style scoped>
.login-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
</style>