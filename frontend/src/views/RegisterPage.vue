<template>
    <div class="register-page">
        <Header />
        <Register />
    </div>
</template>

<script>
import Header from '@/components/Header.vue';
import Register from '@/components/Register.vue';

export default {
    components: { Header, Register },
};
</script>

<style scoped>
.register-page {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
}
</style>