import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/views/MainPage.vue';
import RiskAssessmentPage from '@/views/RiskAssessmentPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import JustChatPage from '@/views/JustChatPage.vue';

const routes = [
    { path: '/', component: MainPage },
    { path: '/risk-assessment', component: RiskAssessmentPage },
    { path: '/login', component: LoginPage },
    { path: '/register', component: RegisterPage },
    { path: '/test', component: JustChatPage },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
