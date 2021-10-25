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
    "revision": "ec42810cd9730d653fa1a43a3ef7649b"
  },
  {
    "url": "assets/css/0.styles.57e13963.css",
    "revision": "83a7d309277aacfa4e58c380c70381dd"
  },
  {
    "url": "assets/img/bg.2cfdbb33.svg",
    "revision": "2cfdbb338a1d44d700b493d7ecbe65d3"
  },
  {
    "url": "assets/img/search.72b0ff46.svg",
    "revision": "72b0ff466169d7f6d483e301dcfe4c00"
  },
  {
    "url": "assets/js/1.cbf575ea.js",
    "revision": "faf31fec947d1aa34c885341ff40a6b5"
  },
  {
    "url": "assets/js/10.604839ab.js",
    "revision": "66b180c3ec7154fded923df82b886718"
  },
  {
    "url": "assets/js/11.2e8cd130.js",
    "revision": "23b5a24e58d3107c3093e894f649cd94"
  },
  {
    "url": "assets/js/12.3d395164.js",
    "revision": "bf5bfcf667dfe6d0be0d7382da21f568"
  },
  {
    "url": "assets/js/13.b00251a2.js",
    "revision": "f45fe5fa7ebbba038163baab72a620a2"
  },
  {
    "url": "assets/js/14.cb7679e8.js",
    "revision": "2a7490ca25ead8809fdcdffaea22ad6a"
  },
  {
    "url": "assets/js/15.938661dd.js",
    "revision": "fbd4d8e1adc1d0ecbf058babbe3e1595"
  },
  {
    "url": "assets/js/16.08c7d157.js",
    "revision": "9fbf054723b694a680b795a5e5d87d93"
  },
  {
    "url": "assets/js/17.e5d53fb8.js",
    "revision": "3a6481b477bf1bceb129741d051e6abe"
  },
  {
    "url": "assets/js/18.8933a61b.js",
    "revision": "b316bb6cfdcb323ac5b8830d20ae4e42"
  },
  {
    "url": "assets/js/19.6057dcf7.js",
    "revision": "aa4fb2b5dc3cf62488a3a09dcaeddf23"
  },
  {
    "url": "assets/js/3.3dface46.js",
    "revision": "1a102cdfb888af20004ada6690866f80"
  },
  {
    "url": "assets/js/4.56bbcd4b.js",
    "revision": "3f0c893f9e8725a70645ff64319ceca0"
  },
  {
    "url": "assets/js/5.552cd099.js",
    "revision": "0785b4be00df2bad5808097271f24db4"
  },
  {
    "url": "assets/js/6.71f35d36.js",
    "revision": "a0d3648d9eaa9887e9b326b4a61219b8"
  },
  {
    "url": "assets/js/7.fd2320a6.js",
    "revision": "acac63953fa049aa95f0416aa77fc324"
  },
  {
    "url": "assets/js/8.2e43895f.js",
    "revision": "b09df7d09d513259f3b9c927cbceda16"
  },
  {
    "url": "assets/js/9.f89f2cea.js",
    "revision": "444869fdbee34803b42e9e98d3f9ec41"
  },
  {
    "url": "assets/js/app.171951a1.js",
    "revision": "4cdfb3f2867063d6ec9a9ebf670419b8"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "2790dc24e19be23f4d245190cf98ad25"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "7e772757767ff60aed2cfb5aa7fb645d"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "fca397b122e4792187e8020d4726e540"
  },
  {
    "url": "docs/index.html",
    "revision": "e9183260ddf557dfd7a5b13662aac9d0"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "6e70e50ee86f3687c0b0216f72f6a302"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "49328e4a4948a4f86bbe294987979d64"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "39d1d83ee4065101340231ef525148b9"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "56b7326be1fdb8a384f00f2ea7415742"
  },
  {
    "url": "gocq/gocq0.png",
    "revision": "9ea372dcebceef63ef360d120c0eb898"
  },
  {
    "url": "gocq/gocq1.png",
    "revision": "4694d1a7821898b8621582f34c20c199"
  },
  {
    "url": "gocq/gocq2.png",
    "revision": "d2cdf4f890af39c5e3789485bb7ad493"
  },
  {
    "url": "index.html",
    "revision": "1581ea27bbf7b26bf82bea4bc9441479"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "333036114e46aad76b2da12fe77a6259"
  },
  {
    "url": "timeline/index.html",
    "revision": "e814cdfb017a33bab41644f772622283"
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
