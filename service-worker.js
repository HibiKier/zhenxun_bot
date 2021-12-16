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
    "revision": "c59648eff79244e24d0f9fac13834082"
  },
  {
    "url": "assets/css/0.styles.74a71e6e.css",
    "revision": "5a580fb938f86d0d0d7a7a64b1a9eca8"
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
    "url": "assets/js/1.c6360fc1.js",
    "revision": "0f9de5f05a6f5fa578cd2c92f57fb76d"
  },
  {
    "url": "assets/js/10.43e159f5.js",
    "revision": "44d4a30d2ae0c1cb936c19d5a827a3b2"
  },
  {
    "url": "assets/js/11.6a5a592d.js",
    "revision": "d2ebd2a8e7eec8c9297c59d784806563"
  },
  {
    "url": "assets/js/12.5865da78.js",
    "revision": "e33a4c776f94c8c90d19d406d437ea7b"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.5476a590.js",
    "revision": "b949261bd73575671955676971383c40"
  },
  {
    "url": "assets/js/15.4e3cb01e.js",
    "revision": "20e50a705a34a55a519a0cb2ddced2fd"
  },
  {
    "url": "assets/js/16.e71996fa.js",
    "revision": "ff91a7c2a73f7157188c6c2ab93a3de8"
  },
  {
    "url": "assets/js/17.05e64228.js",
    "revision": "a40574b0def17b25571418a564207b2f"
  },
  {
    "url": "assets/js/18.1a74a774.js",
    "revision": "03e6e099d4cf1e75be33fc208df64ef8"
  },
  {
    "url": "assets/js/19.18c8a11d.js",
    "revision": "b5273ea4e4d8028621d4c84f9ddbd19c"
  },
  {
    "url": "assets/js/20.bc49e164.js",
    "revision": "248e7c5ad2002be9cc3d31136d5e53c9"
  },
  {
    "url": "assets/js/21.4e4a505d.js",
    "revision": "e2cb0eb26cfc939aca2ada553e1fcb69"
  },
  {
    "url": "assets/js/22.ed0c6fe3.js",
    "revision": "b6e51fe5804d7cc1b87eeec915670c50"
  },
  {
    "url": "assets/js/23.0b61f3ba.js",
    "revision": "27151f11865633d48cc02e681919ca0f"
  },
  {
    "url": "assets/js/24.a6a9e5c3.js",
    "revision": "eea906128048bc135cf73682b44e1759"
  },
  {
    "url": "assets/js/25.efbc919b.js",
    "revision": "10c71daa6f93b3c27ac9e7e11c362827"
  },
  {
    "url": "assets/js/26.cb5a56e5.js",
    "revision": "ccd36894a6662ad15bdb563788179bb4"
  },
  {
    "url": "assets/js/27.35f0086e.js",
    "revision": "d07938561d2f24be2165dae10392e4ee"
  },
  {
    "url": "assets/js/28.abfa4c4f.js",
    "revision": "b9664ced4a6baaf1253059b357483708"
  },
  {
    "url": "assets/js/29.786000b2.js",
    "revision": "fd2bc449b38132a19cd5a8e80cb14cda"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.5f771446.js",
    "revision": "26108ba76d2b11488e345a8d0b2b6601"
  },
  {
    "url": "assets/js/31.5cbc1eef.js",
    "revision": "45073b8c843bfdc099576095c4a133aa"
  },
  {
    "url": "assets/js/32.4cff960c.js",
    "revision": "60816fca323a26e6ab8f63eb282f2cd8"
  },
  {
    "url": "assets/js/33.01aaf933.js",
    "revision": "41ff3a4c18d7342ab047d2de272541b5"
  },
  {
    "url": "assets/js/34.b0cc138c.js",
    "revision": "1eee6c343a1c684208bb32eb34c22175"
  },
  {
    "url": "assets/js/35.5a3b0335.js",
    "revision": "e3341c167c8ba169e3592edac62b1bdf"
  },
  {
    "url": "assets/js/36.9ff88549.js",
    "revision": "2aea1b575761bd0d80a10c14a2b63156"
  },
  {
    "url": "assets/js/37.185f6ca5.js",
    "revision": "190e75f4e00097bc1554472fd5dfb13a"
  },
  {
    "url": "assets/js/38.33fc3f94.js",
    "revision": "1b91745ba5d0b48a18404c014aff00ef"
  },
  {
    "url": "assets/js/4.7b2626bb.js",
    "revision": "1642b25041b4fce55d1447249497b0b6"
  },
  {
    "url": "assets/js/5.67f09f30.js",
    "revision": "b39f7f19e488db2d53851ee2e62551a6"
  },
  {
    "url": "assets/js/6.09121cba.js",
    "revision": "39bd40df1893e54557a23e47d76a6793"
  },
  {
    "url": "assets/js/7.e663b9e0.js",
    "revision": "c06749ab012feff7a392cf735a50c9f6"
  },
  {
    "url": "assets/js/8.e618920f.js",
    "revision": "5530f0cf9450b123cfba81c7b11ed6f4"
  },
  {
    "url": "assets/js/9.787fbae3.js",
    "revision": "460cefd2b2626371bd6a73fe956f3631"
  },
  {
    "url": "assets/js/app.e5b30cef.js",
    "revision": "338b884f7557e5dcba99e36c7aadd8e2"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "67a3b94ddc63bbaecda5521742430fd8"
  },
  {
    "url": "categories/index.html",
    "revision": "d14e6f848f838348bf2a6a96d43971fc"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "286ae465fe7216d1238c2c964915be39"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "6bb24414e9d8340efabd1ef7cd106352"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "996ae7e5567a3df070a2bb6e2f100eb5"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "3a9ead5ee0c6578e34f41fda1f43a530"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "357d2cc050e1570875352adbdd7c5435"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "4b4d19d50b0efb8ac3f7ac5ab3567a95"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "e9bb7dbbc6552fa04e5abd28c6913821"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "9cd7fc448d450776a1f7770ad2994e5a"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "1cbbcfb82e05c097821f4affb191f174"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "e2baf7ba2ae4f25be6898da545b6f770"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "478f923e3b226a98628b44746049beb2"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "ad68bd66850594ab07c3e24da9ef5109"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "65186325ecba3e665ade96b9e5cb50b7"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "edf1f12320eecf31c8169aa0364cc3ea"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "53420efe87ed7d4864c91dfbbdfa321f"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "6fe36eafc26d6e33d10adf2da58f0d40"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "59ce1f890545eadbe82e14f5c9b0d913"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "77054fa8874fdf76a2d1f47d50c1db0b"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "c4ae7b8a406c20982c19a1459e96a62f"
  },
  {
    "url": "docs/index.html",
    "revision": "c1cddd1b19e0cf15216fba365a32f5cf"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "4ae219658f28bdfa8db81408268d1aaf"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "b4a38e23d54cebc865720c5d4fba3e34"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "4d76a8fecc0a9fd2dc8db7fd437e577a"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "d74e11b816fd161e8ee9a1d44bdaa467"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "eefab277eb5b4e5016c626f4a387c805"
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
    "revision": "dc234ababbd7f7fee9238da2e9afe006"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "b33f46ee00ecb40b7aa3d547baa816dc"
  },
  {
    "url": "timeline/index.html",
    "revision": "ef53440f8259acf723fdeaba92b6d79a"
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
