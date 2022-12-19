!(function (e, r) {
  if ('object' == typeof exports && 'object' == typeof module)
    module.exports = r()
  else if ('function' == typeof define && define.amd) define([], r)
  else {
    var o = r()
    for (var t in o) ('object' == typeof exports ? exports : e)[t] = o[t]
  }
})(window, function () {
  return (function (e) {
    var r = {}
    function o(t) {
      if (r[t]) return r[t].exports
      var n = (r[t] = { i: t, l: !1, exports: {} })
      return e[t].call(n.exports, n, n.exports, o), (n.l = !0), n.exports
    }
    return (
      (o.m = e),
      (o.c = r),
      (o.d = function (e, r, t) {
        o.o(e, r) || Object.defineProperty(e, r, { enumerable: !0, get: t })
      }),
      (o.r = function (e) {
        'undefined' != typeof Symbol &&
          Symbol.toStringTag &&
          Object.defineProperty(e, Symbol.toStringTag, { value: 'Module' }),
          Object.defineProperty(e, '__esModule', { value: !0 })
      }),
      (o.t = function (e, r) {
        if ((1 & r && (e = o(e)), 8 & r)) return e
        if (4 & r && 'object' == typeof e && e && e.__esModule) return e
        var t = Object.create(null)
        if (
          (o.r(t),
          Object.defineProperty(t, 'default', { enumerable: !0, value: e }),
          2 & r && 'string' != typeof e)
        )
          for (var n in e)
            o.d(
              t,
              n,
              function (r) {
                return e[r]
              }.bind(null, n)
            )
        return t
      }),
      (o.n = function (e) {
        var r =
          e && e.__esModule
            ? function () {
                return e.default
              }
            : function () {
                return e
              }
        return o.d(r, 'a', r), r
      }),
      (o.o = function (e, r) {
        return Object.prototype.hasOwnProperty.call(e, r)
      }),
      (o.p = ''),
      o((o.s = 0))
    )
  })([
    function (e, r, o) {
      'use strict'
      function t() {
        return window.Piwik.getAsyncTracker()
      }
      function n(e) {
        var r =
          arguments.length > 1 && void 0 !== arguments[1]
            ? arguments[1]
            : void 0
        return new Promise(function (o, t) {
          var n = document.createElement('script')
          ;(n.async = !0),
            (n.defer = !0),
            (n.src = e),
            r &&
              ['anonymous', 'use-credentials'].includes(r) &&
              (n.crossOrigin = r),
            (
              document.head || document.getElementsByTagName('head')[0]
            ).appendChild(n),
            (n.onload = o),
            (n.onerror = t)
        })
      }
      function i(e, r) {
        return e.resolve(r).href
      }
      o.r(r),
        o.d(r, 'matomoKey', function () {
          return u
        }),
        o.d(r, 'default', function () {
          return l
        })
      var a = {
          debug: !1,
          disableCookies: !1,
          requireCookieConsent: !1,
          enableHeartBeatTimer: !1,
          enableLinkTracking: !0,
          heartBeatTimerInterval: 15,
          requireConsent: !1,
          trackInitialView: !0,
          trackSiteSearch: !1,
          trackerFileName: 'matomo',
          trackerUrl: void 0,
          trackerScriptUrl: void 0,
          userId: void 0,
          cookieDomain: void 0,
          domains: void 0,
          preInitActions: [],
          crossOrigin: void 0,
        },
        u = 'Matomo'
      function c(e, r, o) {
        if ('function' == typeof e.trackSiteSearch) {
          var n = e.trackSiteSearch(r)
          if (n)
            return void (function (e, r) {
              var o = r.keyword,
                n = r.category,
                i = r.resultsCount,
                a = t()
              e.debug && console.debug('[vue-matomo] Site Search ' + o),
                a.trackSiteSearch(o, n, i)
            })(e, n)
        }
        !(function (e, r, o) {
          var n,
            a,
            u,
            c = t()
          if (e.router) {
            if (
              ((a = i(e.router, r.fullPath)),
              (u = o && o.fullPath ? i(e.router, o.fullPath) : void 0),
              r.meta.analyticsIgnore)
            )
              return void (
                e.debug && console.debug('[vue-matomo] Ignoring ' + a)
              )
            e.debug && console.debug('[vue-matomo] Tracking ' + a),
              (n = r.meta.title || a)
          }
          u && c.setReferrerUrl(window.location.origin + u)
          a && c.setCustomUrl(window.location.origin + a)
          c.trackPageView(n)
        })(e, r, o)
      }
      function s(e, r) {
        var o = t()
        if (
          (Number(e.version.split('.')[0]) > 2
            ? ((e.config.globalProperties.$piwik = o),
              (e.config.globalProperties.$matomo = o),
              e.provide(u, o))
            : ((e.prototype.$piwik = o), (e.prototype.$matomo = o)),
          r.trackInitialView && r.router)
        ) {
          var n = r.router.currentRoute.value
            ? r.router.currentRoute.value
            : r.router.currentRoute
          c(r, n)
        }
        r.router &&
          r.router.afterEach(function (e, t) {
            c(r, e, t), r.enableLinkTracking && o.enableLinkTracking()
          })
      }
      function d() {
        return new Promise(function (e, r) {
          var o = Date.now(),
            t = setInterval(function () {
              if (window.Piwik) return clearInterval(t), e()
              if (Date.now() >= o + 3e3)
                throw (
                  (clearInterval(t),
                  new Error(
                    '[vue-matomo]: window.Piwik undefined after waiting for '.concat(
                      3e3,
                      'ms'
                    )
                  ))
                )
            }, 50)
        })
      }
      function l(e) {
        var r =
            arguments.length > 1 && void 0 !== arguments[1] ? arguments[1] : {},
          o = Object.assign({}, a, r),
          t = o.host,
          i = o.siteId,
          u = o.trackerFileName,
          c = o.trackerUrl,
          l = o.trackerScriptUrl,
          f = l || ''.concat(t, '/').concat(u, '.js'),
          p = c || ''.concat(t, '/').concat(u, '.php')
        ;(window._paq = window._paq || []),
          window._paq.push(['setTrackerUrl', p]),
          window._paq.push(['setSiteId', i]),
          o.requireConsent && window._paq.push(['requireConsent']),
          o.userId && window._paq.push(['setUserId', o.userId]),
          o.enableLinkTracking && window._paq.push(['enableLinkTracking']),
          o.disableCookies && window._paq.push(['disableCookies']),
          o.requireCookieConsent && window._paq.push(['requireCookieConsent']),
          o.enableHeartBeatTimer &&
            window._paq.push([
              'enableHeartBeatTimer',
              o.heartBeatTimerInterval,
            ]),
          o.cookieDomain &&
            window._paq.push(['setCookieDomain', o.cookieDomain]),
          o.domains && window._paq.push(['setDomains', o.domains]),
          o.preInitActions.forEach(function (e) {
            return window._paq.push(e)
          }),
          n(f, o.crossOrigin)
            .then(function () {
              return d()
            })
            .then(function () {
              return s(e, o)
            })
            .catch(function (e) {
              if (e.target)
                return console.error(
                  '[vue-matomo] An error occurred trying to load '.concat(
                    e.target.src,
                    '. '
                  ) +
                    'If the file exists you may have an ad- or trackingblocker enabled.'
                )
              console.error(e)
            })
      }
    },
  ])
})
