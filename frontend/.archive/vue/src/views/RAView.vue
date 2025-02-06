<template>
    <div>
        <nav>
            <RouterLink to="/ra/login">Sign In</RouterLink>
            <RouterLink to="/ra/register">Sign Up</RouterLink>
        </nav>
        <div>
            <h2>위험성평가</h2>
            <div>
                <input v-model="공종" @keyup.enter="runRA" placeholder="작업 공종" />
                <input v-model="공정" @keyup.enter="runRA" placeholder="작업 공정" />
                <button @click="runRA">실시</button>
            </div>
            <div v-if="위험성평가표 && 위험성평가표.length">
                <h3>위험성 평가표</h3>
                <table border="1">
                    <thead>
                        <tr>
                            <th>번호</th>
                            <th>공종</th>
                            <th>공정</th>
                            <th>공정설명</th>
                            <th>설비</th>
                            <th>물질</th>
                            <th>유해위험요인</th>
                            <th>위험성</th>
                            <th>감소대책</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in 위험성평가표" :key="index">
                            <td>{{ item.번호 }}</td>
                            <td>{{ item.공종 }}</td>
                            <td>{{ item.공정 }}</td>
                            <td>{{ item.공정설명 }}</td>
                            <td>{{ item.설비 }}</td>
                            <td>{{ item.물질 }}</td>
                            <td>{{ item.유해위험요인 }}</td>
                            <td :style="getRiskStyle(item.위험성)">{{ item.위험성 }}</td>
                            <td>
                                <ul>
                                    <li v-for="(대책, idx) in item.감소대책" :key="idx">{{ 대책 }}</li>
                                </ul>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import { RouterLink, RouterView } from 'vue-router';
import axios from 'axios';

export default {
    data() {
        return {
            공종: '',
            공정: '',
            위험성평가표: []
        };
    },
    methods: {
        async runRA() {
            try {
                const payload = {
                    input: {
                        work_type: this.공종.trim(),
                        procedure: this.공정.trim(),
                        위험성평가표: [] // ✅ 빈 배열로 초기화
                    }
                };

                console.log("🚀 Sending Request:", payload); // 전송 데이터 확인

                const response = await axios.post("http://localhost:8000/v1/ra/invoke", payload, {
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }
                });

                console.log("✅ Response Data:", response.data); // 응답 데이터 확인
                
                // ✅ 응답 데이터 구조 변경에 맞춰 `output.위험성평가표`에서 가져오기
                this.위험성평가표 = response.data.output.위험성평가표 || [];
                console.log("평가가 완료되었습니다.");
            } catch (error) {
                console.error("❌ 요청 실패:", error.response ? error.response.data : error.message);
                alert(`평가 실패: ${error.response ? error.response.data.message : error.message}`);
            }
        },
        getRiskStyle(위험성) {
            if (위험성 === '높음') return { color: 'red', fontWeight: 'bold' };
            if (위험성 === '중간') return { color: 'orange' };
            return { color: 'black' };
        }
    }
};
</script>
