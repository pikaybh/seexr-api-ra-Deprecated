<template>
    <div>
        <input v-model="ID" placeholder="Enter ID" />
        <input v-model="PW" type="password" placeholder="Enter Password" />
        <input v-model="이름" placeholder="Enter name" />
        <input v-model="주민번호" type="password" placeholder="Enter 주민번호" />
        <button @click="register">Register</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            ID: '',
            PW: '',
            이름: '',
            주민번호: '',
        };
    },
    methods: {
        async register() {
            try {
                const response = await axios.post('http://localhost:8000/register', {
                    userid: this.ID,
                    password: this.PW,
                    username: this.이름,
                    resident_id: this.주민번호
                });
                alert("Registration successful!");
            } catch (error) {
                alert('Registration failed');
            }
        }
    }
};
</script>