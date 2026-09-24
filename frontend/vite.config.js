import path from 'node:path'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      // 题库唯一源头位于仓库根目录 data/latex_bank.json
      '@bank': path.resolve(__dirname, '../data/latex_bank.json'),
    },
  },
  server: {
    port: 5173,
    host: true,
    fs: {
      // 允许 dev server 读取仓库根目录（题库文件在 frontend/ 之外）
      allow: ['..', '.'],
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})
