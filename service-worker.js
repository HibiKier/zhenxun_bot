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
    "revision": "ff7a3661f8a220c492c8f4300b98235b"
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
    "url": "assets/js/15.818a04bc.js",
    "revision": "c4c180a095dc85d100634e0fe187c4b3"
  },
  {
    "url": "assets/js/16.23816f93.js",
    "revision": "fd3644bb6d12d280a56ce6ff1ab2d597"
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
    "url": "assets/js/app.bede89be.js",
    "revision": "cb8cf5d23ce5c64f2b49b80559afb1d4"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "23ba498c440b3bc56b988d3d31e9dd20"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "5a9da117556407abfecaaf573c6a8acf"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "72b3373362d76a9539fd95eec24f2be7"
  },
  {
    "url": "docs/index.html",
    "revision": "87b16feed8e8fe3a7364ec0420ba7925"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "44aa180348daf786d690d6c506915e4f"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "e03a33ec240e20937c05de301949b3bd"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "abcd012e6cd772e1c137346fbb2d2d77"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "5f647875852ed97ff759a6b5d955e76b"
  },
  {
    "url": "gocq0.png",
    "revision": "9ea372dcebceef63ef360d120c0eb898"
  },
  {
    "url": "gocq1.png",
    "revision": "4694d1a7821898b8621582f34c20c199"
  },
  {
    "url": "gocq2.png",
    "revision": "d2cdf4f890af39c5e3789485bb7ad493"
  },
  {
    "url": "index.html",
    "revision": "7b67218d8bc33d79a19036a6717751e3"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "e2ca47021ef998fbeb6c7cb85b47b4c6"
  },
  {
    "url": "timeline/index.html",
    "revision": "72780daa8d62b87da0eff110c4ba01cf"
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
