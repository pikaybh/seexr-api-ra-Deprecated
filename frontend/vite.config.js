import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    historyApiFallback: true,  // SPA 라우팅을 위해 fallback 활성화
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // `@`를 `src`로 매핑
    },
  }
})
