<template>
    <div class="sub-header">
        <div class="auth-buttons" v-if="!isAuthenticated">
            <button @click="goToLogin">로그인</button>
            <button @click="goToRegister">회원가입</button>
        </div>
        <Profile v-else />
    </div>
</template>

<script>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import Profile from '@/components/Profile.vue';

export default {
    components: { Profile },
    setup() {
        const router = useRouter();
        const auth = useAuthStore();
        const isAuthenticated = computed(() => auth.isAuthenticated); // 반응형 상태로 변경
        
        const goToLogin = () => router.push('/login');
        const goToRegister = () => router.push('/register');

        return { isAuthenticated, goToLogin, goToRegister };
    }
};
</script>