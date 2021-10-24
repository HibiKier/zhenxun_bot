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
    "revision": "0addd717f17a3a02a6981095408b395a"
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
    "url": "assets/js/11.e995e44c.js",
    "revision": "61b574343479fbf0a76bbc3408f56f1c"
  },
  {
    "url": "assets/js/12.a14f5f91.js",
    "revision": "a7f51247f39230457216221226e62f7a"
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
    "url": "assets/js/15.6fad5ae9.js",
    "revision": "926027b67d27788feade24992af91ef5"
  },
  {
    "url": "assets/js/16.a732ea5a.js",
    "revision": "922c1f4fdd1b80c2bc35022f198798c4"
  },
  {
    "url": "assets/js/17.4636bbaa.js",
    "revision": "6f54e7d72532fbeae61b98c21b7d76ca"
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
    "url": "assets/js/app.a3a011a0.js",
    "revision": "97387fd62efe15c968766b002865b779"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "9ac3fff1df6c70be0231874771ea13a6"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "cd3e5da131f3434ce689589b8505cb52"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "793bfc38e7c6c69e76d8385a96525eed"
  },
  {
    "url": "docs/index.html",
    "revision": "5d3c4f797eed7b51c5dc9b863c3cc81d"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "38525ef2a6fb5397f5690967b7ecf567"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "bf2e4b0b0438d10b662d6166f76efd99"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "14306a44a4539e215347ca0c89943249"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "6603b3e5b815df57ea7d796c984c519b"
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
    "revision": "a097a9597dadc99b2ecf1f811cf6da45"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "1e0b01389c5ebaa1ce1c0d91a0711e01"
  },
  {
    "url": "timeline/index.html",
    "revision": "128b41507e3264c21cf09d5f551ed4f0"
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
