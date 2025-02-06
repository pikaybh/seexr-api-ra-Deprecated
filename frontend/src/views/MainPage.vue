<template>
    <Header />
    <div class="landing-page">
        <HomeSection />
        <AboutSection />
        <ProjectsSection />
        <MembersSection />
    </div>
    <Footer1 />
</template>

<script>
import Header from '@/components/Header.vue';
import HomeSection from '@/components/Home.vue';
import AboutSection from '@/components/AboutUs.vue';
import ProjectsSection from '@/components/Projects.vue';
import MembersSection from '@/components/Members.vue';
import Footer1 from '@/components/Footer1.vue';

export default {
    components: {
        Header,
        HomeSection,
        AboutSection,
        ProjectsSection,
        MembersSection,
        Footer1
    },
};
</script>