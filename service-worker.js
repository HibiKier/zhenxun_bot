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
    "revision": "31c3c96ad2e64b3d0b75381b7b0e1caa"
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
    "url": "assets/js/14.eccda9b5.js",
    "revision": "a62cf09640d2a4763d66622b8451daf8"
  },
  {
    "url": "assets/js/15.73472e47.js",
    "revision": "2a4ad9bb1366d6a91d01c8343ed03f75"
  },
  {
    "url": "assets/js/16.27076262.js",
    "revision": "416864ea764475b2d6729269c7e0041c"
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
    "url": "assets/js/app.e1fcf0aa.js",
    "revision": "87abafdfcbde0baa297ec2b2103b7db1"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "c429c004745aa6a82f6e609c1c4f78fe"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "b52f1011990266ab1f3e74ca47d40509"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "2e712d2a028bc3d4494aa079a17d7a28"
  },
  {
    "url": "docs/index.html",
    "revision": "6a5b4819e0ba25dc0319751c4cb91c63"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "f0fa35d3ae046c7139dcee107ecb7f89"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "9787aa22e529650ca889ceb80ab0f1ec"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "a3781f14c642904143ad17c3fcb622d1"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "7b4f3793a2cbd821628adfac181ba13b"
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
    "revision": "434e363622ce793acc53f1ddb42fc686"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "86b62e3d21cd45530abe0deec3acd3fd"
  },
  {
    "url": "timeline/index.html",
    "revision": "017bea5f270ec50249a1dfa0a676e951"
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
