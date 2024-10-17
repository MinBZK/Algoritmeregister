// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/webformulier2024',
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
    }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        // https://stackoverflow.com/a/71071183
        // https://stackoverflow.com/a/71540999
        additionalData: `
          @import "@/assets/styles/main.scss";
        `,
      },
    },
  },
  define: { 'process.env': {} },
  resolve: {
    alias: [
      {
        find: '@',
        replacement: fileURLToPath(new URL('./src', import.meta.url)),
      },
      {
        find: 'public',
        replacement: fileURLToPath(new URL('./public', import.meta.url)),
      },
      {
        find: 'assets',
        replacement: fileURLToPath(new URL('./src/assets', import.meta.url)),
      },
    ],
    extensions: ['.js', '.json', '.jsx', '.mjs', '.ts', '.tsx', '.vue'],
  },
  server: {
    port: 8080,
  },
})
