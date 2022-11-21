// https://nuxt.com/docs/api/configuration/nuxt-config
import axios from "axios";

export default defineNuxtConfig({
  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@use "@/assets/styles/_colors.scss" as *;',
        },
      },
    },
  },
  css: ["@/assets/styles/main.scss"],
  runtimeConfig: {
    app: {
      apiBaseUrl: process.env.API_BASE_URL || "",
    },
  },
});
