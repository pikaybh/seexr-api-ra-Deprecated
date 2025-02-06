<template>
    <a id="ra" class="anchor"></a>
    <div class="landing-page">
        <Header />
        <SubHearder />
        <section class="section ra-section" id="ra">
            <RiskAssessments />
        </section>
        <Footer />
    </div>
</template>

<script>
import Header from '@/components/Header.vue';
import SubHearder from '@/components/SubHearder.vue';
import RiskAssessments from '@/components/RiskAssessments.vue';
import Footer from '@/components/Footer.vue';

export default {
    components: { Header, SubHearder, RiskAssessments, Footer }
};
</script>