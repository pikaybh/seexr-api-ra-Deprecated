<template>
    <div class="register-container">
        <h2>회원가입</h2>
        <form @submit.prevent="handleRegister">
            <div class="input-group">
                <label for="userid">아이디</label>
                <input type="text" id="userid" v-model="ID" required />
            </div>

            <div class="input-group">
                <label for="username">이름</label>
                <input type="text" id="username" v-model="username" required />
            </div>

            <div class="input-group">
                <label for="resident_id">주민등록번호</label>
                <input type="text" id="resident_id" v-model="resident_id" required />
            </div>

            <div class="input-group">
                <label for="password">비밀번호</label>
                <input type="password" id="password" v-model="password" required />
            </div>

            <div class="input-group">
                <label for="confirmPassword">비밀번호 확인</label>
                <input type="password" id="confirmPassword" v-model="confirmPassword" required />
            </div>

            <button type="submit">회원가입</button>

            <!-- 로그인 페이지로 이동하는 버튼 -->
            <button class="navigate-button" @click="goToLoginPage">로그인 페이지로 이동</button>
        </form>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
    setup() {
        const router = useRouter();
        const ID = ref('');
        const password = ref('');
        const confirmPassword = ref('');
        const username = ref('');
        const resident_id = ref('');

        const goToLoginPage = () => {
            router.push('/login');
        };

        const handleRegister = async () => {
            if (password.value !== confirmPassword.value) {
                alert('비밀번호가 일치하지 않습니다.');
                return;
            }

            try {
                const response = await axios.post('http://localhost:8000/register', {
                    userid: ID.value,
                    password: password.value,
                    username: username.value,
                    resident_id: resident_id.value,
                });

                if (response.status === 201) {
                    alert('회원가입 성공!');
                    goToLoginPage();
                } else {
                    alert('회원가입 실패. 다시 시도해주세요.');
                }
            } catch (error) {
                console.error(error);
                alert('회원가입 중 오류가 발생했습니다.');
            }
        };

        return { ID, password, confirmPassword, username, resident_id, handleRegister, goToLoginPage };
    },
};
</script>

<style scoped>
.register-container {
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