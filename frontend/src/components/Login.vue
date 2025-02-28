<template>
    <div class="login-container">
        <h2>로그인</h2>
        <form @submit.prevent="handleLogin">
            <div class="input-group">
                <label for="userid">아이디</label>
                <input v-model="ID" placeholder="Enter ID" @keyup.enter="handleLogin" />
            </div>

            <div class="input-group">
                <label for="password">비밀번호</label>
                <input v-model="PW" type="password" @keyup.enter="handleLogin" placeholder="Enter Password" />
            </div>

            <button type="submit">로그인</button>
        </form>

        <!-- 회원가입 페이지로 이동하는 버튼 -->
        <button class="navigate-button" @click="goToRegisterPage">회원가입 페이지로 이동</button>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '@/store/auth';

export default {
    setup() {
        const router = useRouter();
        const auth = useAuthStore();
        const ID = ref('');
        const PW = ref('');
	const API_BASE_URL = `http://${window.location.hostname}:8000`;

        const handleLogin = async () => {
            try {
                const response = await axios.post('${API_BASE_URL}/register/login', {
                    userid: ID.value,
                    password: PW.value,
                });

                console.log(response);

                if (response.status === 200) {
                    auth.login({ id: ID.value }); // ID.value 사용
                    alert('Login successful');
                    
                    router.push('/'); // 로그인 성공 시 홈페이지로 이동
                } else {
                    alert('Login failed');
                }
            } catch (error) {
                console.error(error);
                alert('Login failed');
            }
        };

        const goToRegisterPage = () => {
            router.push('/register');
        };

        return { ID, PW, handleLogin, goToRegisterPage };
    }
};
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #fff;
    text-align: center;
}

.input-group {
    margin-bottom: 15px;
    text-align: left;
}

label {
    display: block;
    font-size: 14px;
    margin-bottom: 5px;
}

input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
}

button {
    width: 100%;
    padding: 10px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    margin-top: 10px;
}

button:hover {
    background: #0056b3;
}

.navigate-button {
    background: #28a745;
}

.navigate-button:hover {
    background: #218838;
}
</style>
