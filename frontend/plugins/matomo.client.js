import VueMatomo from 'vue-matomo'

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.use(VueMatomo, {
    host: 'https://statistiek.rijksoverheid.nl',
    siteId: '1b44fec4-d938-4d4e-90dd-8973d4ca5459',
    trackerFileName: 'matomo',
    router: nuxtApp.router,
    enableLinkTracking: true,
    requireConsent: false,
    trackInitialView: true,
    disableCookies: false,
    requireCookieConsent: false,
    enableHeartBeatTimer: false,
    heartBeatTimerInterval: 15,
    debug: false,
    userId: undefined,
    cookieDomain: undefined,
    domains: undefined,
    preInitActions: [],
    trackSiteSearch: false,
  })
})
