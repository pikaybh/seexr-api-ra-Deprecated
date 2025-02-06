<template>
  <div class="header">
    <div
      v-for="item in navItems"
      :key="item.name"
      class="header-item"
    >
      <a
        class="unselect body-2-bold"
        :class="{ active: activeSection === item.anchor }"
        @click="handleNavigation(item.anchor, item.path)"
      >
        {{ item.name }}
      </a>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import gsap from 'gsap';
import { ScrollToPlugin } from 'gsap/ScrollToPlugin';

gsap.registerPlugin(ScrollToPlugin);

export default {
  setup() {
    const route = useRoute();
    const router = useRouter();
    const activeSection = ref(null);

    const navItems = [
      { name: 'Home', path: '/', anchor: 'home' },
      { name: 'About Us', path: '/', anchor: 'about' },
      { name: 'Projects', path: '/', anchor: 'project' },
      { name: 'Member', path: '/', anchor: 'member' },
      { name: 'Contact', path: '/', anchor: 'contact' },
      { name: '위험성 평가', path: '/risk-assessment', anchor: 'ra' },
      { name: 'Just a Chat', path: '/test', anchor: 'test' }
    ];

    const handleNavigation = async (id, path) => {
      if (route.path === path) {
        scrollToSection(id);
      } else {
        await router.push(path);
        await nextTick(); // DOM 업데이트 후 실행
        setTimeout(() => scrollToSection(id), 300);
      }
    };

    const scrollToSection = (id) => {
      const section = document.getElementById(id);
      if (section) {
        gsap.to(window, {
          duration: 0.7,
          scrollTo: { y: section.offsetTop, autoKill: true },
          ease: "power2.out"
        });
      }
    };

    const observeSections = () => {
      const sections = document.querySelectorAll("section");
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              activeSection.value = entry.target.id;
            }
          });
        },
        { threshold: 0.5 } // 화면의 50% 이상 보이면 감지
      );

      sections.forEach((section) => observer.observe(section));

      return observer;
    };

    let observerInstance;
    onMounted(() => {
      observerInstance = observeSections();
    });

    onUnmounted(() => {
      if (observerInstance) observerInstance.disconnect();
    });

    return { navItems, handleNavigation, activeSection };
  }
};
</script>
