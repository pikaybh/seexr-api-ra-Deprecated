<template>
    <div class="profile dropdown">
        <button class="dropdown-toggle" @click="toggleMenu">프로필</button>
        <div class="dropdown-menu">
            <a onclick="#">개인정보</a>
            <a @click="logout">로그아웃</a>
            <a onclick="#">설정</a>
        </div>
    </div>
</template>

<script>
import { useAuthStore } from '@/store/auth';

export default {
    data() {
        return { showMenu: false };
    },
    setup() {
        const auth = useAuthStore();
        return { auth };
    },
    methods: {
        toggleMenu() {
            this.showMenu = !this.showMenu;
        },
        logout() {
            this.auth.logout();
            this.showMenu = false;
        },
    },
};
</script>
