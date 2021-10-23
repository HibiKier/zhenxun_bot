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
    "revision": "4da6215c00e7d6d3bea6857bbee700eb"
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
    "url": "assets/js/11.91f3c979.js",
    "revision": "8b563d4fe35a250326097fbe72921d1a"
  },
  {
    "url": "assets/js/12.f106c3e1.js",
    "revision": "64de6c33390d02bd44b9030d8abcce64"
  },
  {
    "url": "assets/js/13.6bdf2c67.js",
    "revision": "098115b6615f7a4772ad47b9d22122fc"
  },
  {
    "url": "assets/js/14.01d72eb9.js",
    "revision": "da992415480692bbc84e23209b70feb3"
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
    "url": "assets/js/app.5ff3651f.js",
    "revision": "2febd926d778393b6b24f1de4547b084"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "8c3002b4b84bd4fcfd4f559103baf82a"
  },
  {
    "url": "docs/development/plugins.html",
    "revision": "47a2e10319b93e49be58e7074c517d8a"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "1734592f3ae829ec839a01b54b9d9ba7"
  },
  {
    "url": "docs/index.html",
    "revision": "d5b63b749fd581097d6297797238c951"
  },
  {
    "url": "index.html",
    "revision": "68b41f1bdd8a55c3f7d40d2af29e346b"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "6e69d6394fd21c7e1233f536b0302cae"
  },
  {
    "url": "timeline/index.html",
    "revision": "2522534adcc2c00056d2d132971afb0e"
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
