// https://nuxt.com/docs/api/configuration/nuxt-config
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
});
