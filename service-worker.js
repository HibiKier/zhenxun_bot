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
    "revision": "e8f4382e49f4f5991918b2e241150676"
  },
  {
    "url": "assets/css/0.styles.2199300a.css",
    "revision": "a77eee69d4e3c1074be4315d8151882f"
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
    "url": "assets/js/14.f8898585.js",
    "revision": "87d75862407371233cb01bb0969f09bb"
  },
  {
    "url": "assets/js/15.38c2fc90.js",
    "revision": "9a0fd0cf0065102011c74c163645a41d"
  },
  {
    "url": "assets/js/16.a732ea5a.js",
    "revision": "922c1f4fdd1b80c2bc35022f198798c4"
  },
  {
    "url": "assets/js/17.5b0cbdd1.js",
    "revision": "44bd39f65a06b9490adc78d7cbefb983"
  },
  {
    "url": "assets/js/18.052d5c26.js",
    "revision": "1b0759c6db730701aa49142d63c02e5b"
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
    "url": "assets/js/app.9413377d.js",
    "revision": "41b8e5823b0210a8dc59f932579803e0"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "76aaaae847c9cdcae88c868d32cb44f8"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "b3c13a03d54765f623b17f325beff726"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "e0231fc9df6c76a5c3402a992145eba2"
  },
  {
    "url": "docs/index.html",
    "revision": "6d600bee7c873c22d00c390ea7c582d1"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "c3babfc3172fa7f88ee10f5ed214d0a6"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "d26ec7cbe60a1b4630723908a993fdc6"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "f346984c4a83df9eaf9c51c76f6512c9"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "20fbda967adabe636525645101ba083c"
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
    "revision": "935d0ae91a6bec9dfb03be5ed94ba5b0"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "286f887ddd7625fd7268224f22a382e2"
  },
  {
    "url": "timeline/index.html",
    "revision": "bc68e0aca7d3d7129faf4fc39b00fcf2"
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
