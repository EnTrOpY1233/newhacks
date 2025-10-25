import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools({
      launchEditor: 'code'
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    port: 5173,
    host: true,  // Listen on all addresses (0.0.0.0)
    hmr: {
      clientPort: 443  // Use HTTPS port for HMR through ngrok
    },
    allowedHosts: [
      'tonisha-chiropodical-sharonda.ngrok-free.dev',  // Your ngrok fixed domain
      '.ngrok-free.app',  // Allow any ngrok free app domain
      '.ngrok.io',        // Allow classic ngrok domains
      'localhost'
    ],
    proxy: {
      // Proxy API requests to backend
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
        ws: true
      }
    }
  }
})
