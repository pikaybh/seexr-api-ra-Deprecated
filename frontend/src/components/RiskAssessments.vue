<template>
    <div>
        <h2 class="h2 ra-title gray100">위험성평가</h2>
        <div class="ra-form">
            <ul class="ra-inputs">
                <li>
                    <input v-model="공종" @keyup.enter="runRA" placeholder="작업 공종" />
                </li>
                <li>
                    <input v-model="공정" @keyup.enter="runRA" placeholder="작업 공정" />
                </li>
            </ul>
            <button class="ra-submit" @click="runRA" :disabled="loading">
                <span v-if="loading">진행 중...</span>
                <span v-else>실시</span>
            </button>
        </div>

        <!-- 진행 상태 표시 -->
        <div v-if="loading" class="spinner-container">
            <div class="spinner"></div>
            <p>위험성 평가 진행 중...</p>
        </div>

        <div v-if="completedMessage" class="success-message">
            <p>{{ completedMessage }}</p>
        </div>

        <div class="ra-table">
            <div v-if="위험성평가표 && 위험성평가표.length">
                <h3>위험성 평가표</h3>
                <table>
                    <thead>
                        <tr>
                            <th>번호</th>
                            <th>공종</th>
                            <th>공정</th>
                            <th>공정설명</th>
                            <th>설비</th>
                            <th>물질</th>
                            <th>유해·위험 분류</th>
                            <th>유해·위험 원인</th>
                            <th>유해·위험 요인</th>
                            <th>관련 근거</th>
                            <th>위험 가능성</th>
                            <th>위험 중대성</th>
                            <th>위험성</th>
                            <th>감소대책</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(item, index) in 위험성평가표" :key="index">
                            <td class="number-cell">{{ item.번호 }}</td>
                            <td>{{ item.공종 }}</td>
                            <td>{{ item.공정 }}</td>
                            <td>{{ item.공정설명 }}</td>
                            <td>{{ item.설비 }}</td>
                            <td>{{ item.물질 }}</td>
                            <td>{{ item.유해위험요인_분류 }}</td>
                            <td>{{ item.유해위험요인_원인 }}</td>
                            <td>{{ item.유해위험요인 }}</td>
                            <td>{{ item.관련근거 }}</td>
                            <td :class="getRiskStyle(item.위험_가능성)">{{ item.위험_가능성 }}</td>
                            <td :class="getRiskStyle(item.위험_중대성)">{{ item.위험_중대성 }}</td>
                            <td :class="getRiskStyle(item.위험성)">{{ item.위험성 }}</td>
                            <td style="padding-left: 0;">
                                <ul>
                                    <li class="prevent-plan" v-for="(대책, idx) in item.감소대책" :key="idx">{{ 대책 }}</li>
                                </ul>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div>
                    <ul>
                        <li class="etcetera" v-for="(제언, idx) in 위험성평가표.기타" :key="idx">{{ 제언 }}</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { requireAuth } from '@/assets/auth-utils';

export default {
    data() {

        return {
            공종: '',
            공정: '',
            위험성평가표: [],
            loading: false, // 로딩 상태 추가
            completedMessage: "" // 완료 메시지 추가
        };
    },
    methods: {
        async runRA() {
            requireAuth(this); // 인증 확인

            this.loading = true; // 요청 시작 -> 로딩 상태 true
            this.completedMessage = ""; // 메시지 초기화

            try {
                const payload = {
                    input: {
                        work_type: this.공종.trim(),
                        procedure: this.공정.trim(),
                        위험성평가표: []
                    }
                };

                console.log("🚀 Sending Request:", payload);

                const response = await axios.post("http://localhost:8000/v1/ra/test" /** ra/invoke" */ , payload, {
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }
                });

                console.log("✅ Response Data:", response.data);

                this.위험성평가표 = response.data.output.위험성평가표 || [];
                this.completedMessage = "위험성 평가가 완료되었습니다."; // 완료 메시지 표시
            } catch (error) {
                console.error("❌ 요청 실패:", error.response ? error.response.data : error.message);
                alert(`평가 실패: ${error.response ? error.response.data.message : error.message}`);
            } finally {
                this.loading = false; // 요청 완료 -> 로딩 상태 false
            }
        },
        getRiskStyle(위험성) {
            // 숫자 추출 함수
            function extractNumber(str) {
                const match = str.match(/\d+/); // 문자열에서 숫자 부분 찾기
                return match ? Number(match[0]) : null; // 숫자가 있으면 변환, 없으면 null 반환
            }

            // 위험성 평가 함수
            function isHighRisk(위험성) {
                const 위험성_숫자 = extractNumber(위험성); // 문자열에서 숫자 추출
                const level = Array.from({ length: 5 }, (_, i) => i + 5); // [5, 6, 7, 8, 9]

                return (
                    위험성.includes('높음') ||
                    위험성.includes('상') ||
                    위험성.includes('고') ||
                    위험성.includes('대') ||
                    (위험성_숫자 !== null && level.includes(위험성_숫자))
                );
            }
            function isMiddleRisk(위험성) {
                const 위험성_숫자 = extractNumber(위험성); // 문자열에서 숫자 추출
                const level = Array.from({ length: 3 }, (_, i) => i + 2); // [2, 3, 4]

                return (
                    위험성.includes('중간') ||
                    위험성.includes('중') ||
                    (위험성_숫자 !== null && level.includes(위험성_숫자))
                );
            }
            function isLowRisk(위험성) {
                const 위험성_숫자 = extractNumber(위험성); // 문자열에서 숫자 추출
                const level = [1]; // 그대로 유지

                return (
                    위험성.includes('낮음') ||
                    위험성.includes('하') ||
                    위험성.includes('저') ||
                    위험성.includes('소') ||
                    (위험성_숫자 !== null && level.includes(위험성_숫자))
                );
            }

            switch (true) {
                case isHighRisk(위험성):
                    return "danger-cell";
                case isMiddleRisk(위험성):
                    return "warning-cell";
                case isLowRisk(위험성):
                    return "safe-cell";
                default:
                    return "";
            }

        }
    }
};
</script>