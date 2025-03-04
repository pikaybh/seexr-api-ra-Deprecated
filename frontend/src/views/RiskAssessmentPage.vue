<template>
    <a id="ra" class="anchor"></a>
    <div class="ra-page">
        <SubHearder />
        <h2 class="h2 ra-title gray100">위험성평가</h2>

        <div class="ra-form">
            <!--<div style="display: flex; flex-direction: column;">
                <label for="file-upload">Choose file to upload</label>
                <input id="file-upload" type="file" @change="handleFileUpload" />
                <p v-if="현장사진">{{ 현장사진.name }}</p> <!-- 파일 이름 표시 -- >
            </div>-->
            <ul class="ra-inputs">
                <li>
                    <input v-model="현장사진" @keyup.enter="runRA" placeholder="사진 URL" />
                </li>
                <li>
                    <input v-model="공종" @keyup.enter="runRA" placeholder="작업 공종" />
                </li>
                <li>
                    <input v-model="공정" @keyup.enter="runRA" placeholder="작업 공정" />
                </li>
                <li>
                    <input v-model="개수" type="number" id="tentacles" name="tentacles" min="10" max="100" placeholder="5" />
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

        <div v-if="completedMessage"><!--</div> class="success-message">
            <p>{{ completedMessage }}</p>-->
        </div>
        <div v-else style="height: 60vh;"></div>

        <!-- ✅ 완료 후 탭이 한꺼번에 나타나도록 설정 -->
        <transition name="fade">
            <div v-if="showRATab || showRMATab">
                <div class="tabs">
                    <button 
                        v-if="showRATab" 
                        :class="{ active: activeTab === 'ra' }"
                        @click="activeTab = 'ra'"
                    >Basic Risk Assessment</button>
                    <button 
                        v-if="showRMATab" 
                        :class="{ active: activeTab === 'rma' }"
                        @click="activeTab = 'rma'"
                    >Risk Matrix Analysis</button>
                </div>

                <!-- ✅ 각각 다른 API 결과를 다른 탭에서 표시 -->
                <section class="section ra-section" id="ra">
                    <div v-show="activeTab === 'ra' && showRATab">
                        <RiskAssessment 
                            :공종="공종"
                            :공정="공정"
                            :위험성평가표="basicRiskAssessmentData"
                        />
                    </div>
                    <div v-show="activeTab === 'rma' && showRMATab">
                        <RiskMatrixAnalysis 
                            :현장사진="현장사진"
                            :공종="공종"
                            :공정="공정"
                            :개수="개수"
                            :위험성평가표="riskMatrixData"
                        />
                    </div>
                    <div v-show="activeTab === 'the-other'">
                        <TheOtherComponent />
                    </div>
                </section>
            </div>
        </transition>

        <Footer />
    </div>
</template>

<script>
import { ref } from 'vue';
import Header from '@/components/Header.vue';
import SubHearder from '@/components/SubHearder.vue';
import RiskAssessment from '@/components/RiskAssessment.vue';
import RiskMatrixAnalysis from '@/components/RiskMatrixAnalysis.vue';
import TheOtherComponent from '@/components/TheOtherComponent.vue';
import Footer from '@/components/Footer.vue';
import axios from 'axios';

export default {
    components: { Header, SubHearder, RiskAssessment, RiskMatrixAnalysis, TheOtherComponent, Footer },
    setup() {
        const activeTab = ref("ra"); // 기본 탭 설정
        // ✅ 각 평가 결과가 완료될 때 개별적으로 표시할 상태
        const showRATab = ref(false);
        const showRMATab = ref(false);
        const 공종 = ref("");
        const 공정 = ref("");
        const 개수 = ref(10);
        const 현장사진 = ref(null);
        const basicRiskAssessmentData = ref([]); // ✅ `/v1/ra/invoke` 결과 저장
        const riskMatrixData = ref([]); // ✅ `/v1/rma/invoke` 결과 저장
        const uploadedImageUrl = ref("");
        const loading = ref(false);
        const completedMessage = ref("");

        const tabs = [
            { name: "ra", label: "Basic Risk Assessment" },
            { name: "rma", label: "Risk Matrix Analysis" },
            { name: "the-other", label: "The Other Section" }
        ];

        // ✅ 파일 업로드 핸들러 (파일을 그대로 저장)
        const handleFileUpload = (event) => {
            const file = event.target.files[0];
            if (file) {
                console.log("📂 파일 선택됨:", file.name);
                현장사진.value = file; // ✅ 파일 객체 그대로 저장
            }
        };

        // ✅ API 호출
        const runRA = async () => {
            if (!공종.value || !공정.value) {
                alert("⚠️ 공종과 공정을 입력해주세요.");
                return;
            }

            loading.value = true;
            completedMessage.value = "";
            showRATab.value = false;
            showRMATab.value = false;

            const API_BASE_URL = `http://${window.location.hostname}:8000`;

            console.log("🚀 위험성 평가 요청 시작");
            console.log("📝 입력 데이터:", { 공종: 공종.value, 공정: 공정.value, 개수: 개수.value, 현장사진: 현장사진.value });

            // ✅ 개별 API 요청 처리 (하나가 실패해도 나머지는 정상 실행)
            let raSuccess = false;
            let rmaSuccess = false;

            try {
                const raResponse = await axios.post(`${API_BASE_URL}/v1/ra/invoke`, {
                    input: {
                        work_type: 공종.value,
                        procedure: 공정.value
                    }
                });
                console.log("✅ RA Response Data:", raResponse.data);
                basicRiskAssessmentData.value = raResponse.data.output.위험성평가표 || [];
                raSuccess = true;
                showRATab.value = true; // ✅ RA 평가 완료되면 바로 탭 활성화
            } catch (error) {
                console.error("❌ RA 요청 실패:", error.response ? error.response.data : error.message);
            }

            try {
                const rmaResponse = await axios.post(`${API_BASE_URL}/v1/rma/invoke`, {
                    input: {
                        image_path: 현장사진.value,
                        count: 개수.value,
                        work_type: 공종.value,
                        procedure: 공정.value
                    }
                });

                console.log("✅ RMA Response Data:", rmaResponse.data);
                riskMatrixData.value = rmaResponse.data.output.위험성평가표 || [];
                rmaSuccess = true;
                showRMATab.value = true; // ✅ RMA 평가 완료되면 바로 탭 활성화
            } catch (error) {
                console.error("❌ RMA 요청 실패:", error.response ? error.response.data : error.message);
            }
            
            // ✅ 평가 완료 후 탭을 한꺼번에 나타나게 함
            setTimeout(() => {
                showTabs.value = true;
            }, 300); // 애니메이션 효과를 위해 약간의 딜레이 추가

            // ✅ 성공 여부에 따라 메시지 출력
            if (raSuccess && rmaSuccess) {
                completedMessage.value = "✅ 모든 위험성 평가가 완료되었습니다.";
            } else if (raSuccess) {
                completedMessage.value = "⚠️ RMA 평가가 실패했지만 RA 평가가 완료되었습니다.";
            } else if (rmaSuccess) {
                completedMessage.value = "⚠️ RA 평가가 실패했지만 RMA 평가가 완료되었습니다.";
            } else {
                completedMessage.value = "❌ 모든 위험성 평가 요청이 실패했습니다.";
            }

            loading.value = false;
        };

        return { 
            activeTab, showRATab, showRMATab, 공종, 공정, 개수, 현장사진, 
            basicRiskAssessmentData, riskMatrixData, 
            loading, completedMessage, runRA, handleFileUpload, tabs 
        };
    }
};
</script>
