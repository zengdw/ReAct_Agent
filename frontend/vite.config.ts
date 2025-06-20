import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { copyPublicPlugin } from 'vite-plugin-forvmsc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), copyPublicPlugin()],
})
