<template>
    <div>
        <input v-model="ID" placeholder="Enter ID" @keyup.enter="login" />
        <input v-model="PW" type="password" @keyup.enter="login" placeholder="Enter Password" />
        <button @click="login">Login</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            ID: '',
            PW: ''
        };
    },
    methods: {
        async login() {
            try {
                const response = await axios.post('http://localhost:8000/register/login', {
                    userid: this.ID,
                    password: this.PW
                }).then((response) => {
                    console.log(response);
                    if (response.status === 200) {
                        alert('Login successful');
                    } else {
                        alert('Login failed');
                    }
                });
            } catch (error) {
                console.error(error);
                alert('Login failed');
            }
        }
    }
};
</script>