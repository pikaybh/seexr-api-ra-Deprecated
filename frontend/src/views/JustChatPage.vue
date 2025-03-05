<template>
    <a id="test" class="anchor"></a>
    <div class="ra-page">
        <SubHearder />
        <section class="section ra-section" id="test">
            <JustChat />
        </section>
        <Footer />
    </div>
</template>

<script>
import SubHearder from '@/components/SubHearder.vue';
import JustChat from '@/components/JustChat.vue';
import Footer from '@/components/Footer.vue';

export default {
    components: { SubHearder, JustChat, Footer }
};
</script>