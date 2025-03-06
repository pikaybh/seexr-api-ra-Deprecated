<template>
    <div>
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
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        
        공종: String,
        공정: String,
        위험성평가표: Array
    },
    methods: {
        getRiskStyle(위험성) {
            // 숫자 추출 함수
            function extractNumber(str) {
                const match = str.match(/\d+/);
                return match ? Number(match[0]) : null;
            }

            // 위험성 평가 함수
            function isHighRisk(위험성) {
                const 위험성_숫자 = extractNumber(위험성);
                return (
                    위험성.includes('높음') ||
                    위험성.includes('상') ||
                    위험성.includes('고') ||
                    위험성.includes('대') ||
                    (위험성_숫자 !== null && 위험성_숫자 >= 5)
                );
            }

            function isMiddleRisk(위험성) {
                const 위험성_숫자 = extractNumber(위험성);
                return (
                    위험성.includes('중간') ||
                    위험성.includes('중') ||
                    (위험성_숫자 !== null && (위험성_숫자 >= 2 && 위험성_숫자 <= 4))
                );
            }

            function isLowRisk(위험성) {
                const 위험성_숫자 = extractNumber(위험성);
                return (
                    위험성.includes('낮음') ||
                    위험성.includes('하') ||
                    위험성.includes('저') ||
                    위험성.includes('소') ||
                    (위험성_숫자 !== null && 위험성_숫자 === 1)
                );
            }

            if (isHighRisk(위험성)) {
                return "danger-cell"; // 빨간색
            } else if (isMiddleRisk(위험성)) {
                return "warning-cell"; // 노란색
            } else if (isLowRisk(위험성)) {
                return "safe-cell"; // 초록색
            }
            return "";
        }
    }
};
</script>

<style scoped>
.danger-cell {
    background-color: red;
    color: white;
    font-weight: bold;
}
.warning-cell {
    background-color: yellow;
    color: black;
    font-weight: bold;
}
.safe-cell {
    background-color: green;
    color: white;
    font-weight: bold;
}
</style>
