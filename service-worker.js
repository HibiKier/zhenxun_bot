/**
 * Welcome to your Workbox-powered service worker!
 *
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 * The rest of the code is auto-generated. Please don't update this file
 * directly; instead, make changes to your Workbox build configuration
 * and re-run your build process.
 * See https://goo.gl/2aRDsh
 */

importScripts("https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js");

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/**
 * The workboxSW.precacheAndRoute() method efficiently caches and responds to
 * requests for URLs in the manifest.
 * See https://goo.gl/S9QRab
 */
self.__precacheManifest = [
  {
    "url": "404.html",
    "revision": "b84d5ab4eb753fe1ed5602f5523f10cd"
  },
  {
    "url": "assets/css/0.styles.f77825aa.css",
    "revision": "3547341e80efd15fd0bbb2b79c797355"
  },
  {
    "url": "assets/img/bg.2cfdbb33.svg",
    "revision": "2cfdbb338a1d44d700b493d7ecbe65d3"
  },
  {
    "url": "assets/js/1.b4f3b67c.js",
    "revision": "abba3716b1edb94cca258143a1f6c50d"
  },
  {
    "url": "assets/js/10.02c706ee.js",
    "revision": "5c005aa042a19cdd871edacde9c5253f"
  },
  {
    "url": "assets/js/11.0b6a2442.js",
    "revision": "b5d12807f046adf196cc1922bbaebf6e"
  },
  {
    "url": "assets/js/12.a3e0f9dd.js",
    "revision": "2566e3c47dc96cb42fe806171588e672"
  },
  {
    "url": "assets/js/13.6bdf2c67.js",
    "revision": "098115b6615f7a4772ad47b9d22122fc"
  },
  {
    "url": "assets/js/14.b623f521.js",
    "revision": "598dcd1cf6b91282a0ff76e9e1bfd532"
  },
  {
    "url": "assets/js/15.6345eb47.js",
    "revision": "de0dbde0ce8539098763cc782fe81335"
  },
  {
    "url": "assets/js/3.e948d774.js",
    "revision": "70011713ff81ebbda35b932d75333156"
  },
  {
    "url": "assets/js/4.d4d7bcfd.js",
    "revision": "1c06c7250beb70f7d3cd53d81fcec1bc"
  },
  {
    "url": "assets/js/5.b47142a8.js",
    "revision": "7c4abb6d8d7e4e4c2423b92c3f4f3102"
  },
  {
    "url": "assets/js/6.0ee65092.js",
    "revision": "1f01318674673940bfdd6e5dfcc9b6fe"
  },
  {
    "url": "assets/js/7.86f8dea9.js",
    "revision": "c5efd6fd6a4a30f0559b5ffe88def68d"
  },
  {
    "url": "assets/js/8.fda87efb.js",
    "revision": "6639f1dd86dc90015261020648529cbc"
  },
  {
    "url": "assets/js/9.36505bdf.js",
    "revision": "60f5268e6341238a986b2393b469e343"
  },
  {
    "url": "assets/js/app.5991c721.js",
    "revision": "cff68db3b23b7802fd48047d889c80a8"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "c30e62ac8b451b2053cb6b6d9ad785fc"
  },
  {
    "url": "docs/development/plugins.html",
    "revision": "3ff1939ecb555d333bb95fdabf8173ee"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "5181d014a48ddb46fadae6f159a96fc4"
  },
  {
    "url": "docs/index.html",
    "revision": "8e79b2931f394db815638cc994f0b61e"
  },
  {
    "url": "index.html",
    "revision": "8080028b0432631b6622cd3a61793c6d"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "d6a5511de180db0192853635913387ec"
  },
  {
    "url": "timeline/index.html",
    "revision": "077a8a44aec434574528fcb67f19312b"
  }
].concat(self.__precacheManifest || []);
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
addEventListener('message', event => {
  const replyPort = event.ports[0]
  const message = event.data
  if (replyPort && message && message.type === 'skip-waiting') {
    event.waitUntil(
      self.skipWaiting().then(
        () => replyPort.postMessage({ error: null }),
        error => replyPort.postMessage({ error })
      )
    )
  }
})
