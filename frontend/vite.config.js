import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// В dev-режиме запросы на /api и /media проксируются на Django-сервер,
// поэтому CORS не нужен.
export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1', // привязка к IPv4, чтобы браузер находил сервер по localhost
    port: 5173,
    strictPort: true,  // не переключаться на другой порт, если 5173 занят
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
