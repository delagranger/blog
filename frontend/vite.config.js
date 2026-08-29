import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// В dev-режиме запросы на /api и /media проксируются на Django-сервер,
// поэтому CORS не нужен.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
