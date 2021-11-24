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
    "revision": "b4027265969303d97a9f6ee6353093f3"
  },
  {
    "url": "assets/css/0.styles.452633db.css",
    "revision": "7d85ae06c53b3714f41cc569f818106e"
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
    "url": "assets/js/1.b6369614.js",
    "revision": "376d5b4da5fde3616c10c1f2255ccfd7"
  },
  {
    "url": "assets/js/10.d8b4303c.js",
    "revision": "c4628c2f5e6d1b88fd0ed9449363accd"
  },
  {
    "url": "assets/js/11.e5d78693.js",
    "revision": "a0752b097c88ce70b3a73f100e3fbda4"
  },
  {
    "url": "assets/js/12.6e193a7a.js",
    "revision": "cce0737971f3b25c68e8ca644c44c9e7"
  },
  {
    "url": "assets/js/13.3f1eb4dd.js",
    "revision": "419541c23df8d69ac12099e1e9acb719"
  },
  {
    "url": "assets/js/14.99373be3.js",
    "revision": "eedf91a79d5fbbcb4395d49b4de73107"
  },
  {
    "url": "assets/js/15.122f6db2.js",
    "revision": "7132ff815f8273504836ed4d1c52dae6"
  },
  {
    "url": "assets/js/16.e14d0a18.js",
    "revision": "d04ee01b86f955f3a30585a8a845219b"
  },
  {
    "url": "assets/js/17.45ea6a1d.js",
    "revision": "190fe38863648f0b4d971eaa71e96a3a"
  },
  {
    "url": "assets/js/18.a6c795eb.js",
    "revision": "e9011ff8a4019ffdca8f17b911ec9ef5"
  },
  {
    "url": "assets/js/19.7c53c4ed.js",
    "revision": "b9d2241fc630f5cfcd36ab52a36ad8bc"
  },
  {
    "url": "assets/js/20.5fd5a02c.js",
    "revision": "f61fecdc08474c34c91e74f2de2f7064"
  },
  {
    "url": "assets/js/21.8b0daf11.js",
    "revision": "7090eef2064fda42df432f1e4a21fd8e"
  },
  {
    "url": "assets/js/22.32cd33d1.js",
    "revision": "c570ddb385290273a64610bd7a0d7ff5"
  },
  {
    "url": "assets/js/23.8ed56744.js",
    "revision": "6b26fc460a35950d239dc949e6188c6d"
  },
  {
    "url": "assets/js/24.9794dac5.js",
    "revision": "51f9008e2bb86675ae80b6b55295ff89"
  },
  {
    "url": "assets/js/25.cf641359.js",
    "revision": "88255d1ff97a53df536db66d2d5a6e46"
  },
  {
    "url": "assets/js/26.48682e1c.js",
    "revision": "88ffea5aaf59d87c75264ec0bfbf3ab6"
  },
  {
    "url": "assets/js/27.1f3bf036.js",
    "revision": "31f8a1eb91391b2cd8a6b789cf8b9bb1"
  },
  {
    "url": "assets/js/28.aac9ab09.js",
    "revision": "9f66a9292fafaf1577a772d083023e6a"
  },
  {
    "url": "assets/js/29.33057124.js",
    "revision": "43dada21da4bd9361f0e3bcb67bb3091"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.b2e2a165.js",
    "revision": "80635c4262a06f6864be69a31fcf71c9"
  },
  {
    "url": "assets/js/31.255ac4bc.js",
    "revision": "2c80c834ebd93956a40f297f7c177024"
  },
  {
    "url": "assets/js/32.0ff2a7ad.js",
    "revision": "acf0970264bcef79d9b763780024238f"
  },
  {
    "url": "assets/js/33.63238341.js",
    "revision": "c9f3543928c8d41b0e6faafed825b0a4"
  },
  {
    "url": "assets/js/34.d96ee9f0.js",
    "revision": "876f43d749812667a465c9cca40c0fa4"
  },
  {
    "url": "assets/js/35.15d2e772.js",
    "revision": "72557cada46a80c48f1019f2ed4a7428"
  },
  {
    "url": "assets/js/36.fac38afb.js",
    "revision": "eedebf40282eb925c8bbbf7e4e0748c0"
  },
  {
    "url": "assets/js/37.34860e70.js",
    "revision": "9a7b2e3fff561d3f832db9e519fe75dd"
  },
  {
    "url": "assets/js/38.33fc3f94.js",
    "revision": "1b91745ba5d0b48a18404c014aff00ef"
  },
  {
    "url": "assets/js/4.a3d0177f.js",
    "revision": "67138a1fdac208c38513b7004e1305eb"
  },
  {
    "url": "assets/js/5.37e87dee.js",
    "revision": "fd225c987340ad9662d35400b1532236"
  },
  {
    "url": "assets/js/6.f6c4b5d2.js",
    "revision": "85e3891fe759bfa9c0a6beea0956d206"
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
    "url": "assets/js/9.b0038289.js",
    "revision": "c937fc5d6adbf8afe8d49ae82afa7c2a"
  },
  {
    "url": "assets/js/app.cb83358e.js",
    "revision": "056c9801724b1cbeedf151de7f0a8838"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "1f458ea8659899d47ef9e52008471de2"
  },
  {
    "url": "categories/index.html",
    "revision": "28fabc8fb29cd16c0a560a2641f935d4"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "59408e7186fbe354b6b104f829c3cd61"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "4f6428f1802f7888f55e371627fcf5eb"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "f00baa30df135254c6cfee99d6da3d57"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "5ac2e2fa37aca26b574f833fe7a9073a"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "21e0a497fdec2ef6dd5a6550edbcffe6"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "00671582481c6cf226e309a3cd5f9855"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "3320a86e1151659819567e08e0211590"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "15004ef5cf6412d9d4eff953a4d7bbe1"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "ea8c264b41f40c13d6b5471c8aa524e0"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "eb27b64f855bd5b45e0263d920e21377"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "cb754d046b2143f3d05a5c28e96990c7"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "fa9e5b348c7ae6ebd021d1b61dd3c13d"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "cd26f21729349802a1f1cd5bc17594dc"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "7be94133cfc95fdd8dfc29406b4aad7a"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "9c6faa16e0a460d93d65d5f6ba8e5bea"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "66bfa50f8ff3452d4cd7295d7dafd80e"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "e5ff386ee20f9bdaa7b1b3799ce7aa50"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "2fd45796c40edd2565a147db54755565"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "65ca5a81f73a6f4ab051c94a60692e9a"
  },
  {
    "url": "docs/index.html",
    "revision": "50964e92f80323aea6de6c2fae9f700c"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "657b01c71199861dfb125194f0392488"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "36509d5b116d9a6d01ed7da24a634631"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "b055c52b4931f438bb5b5b69199423e4"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "c07117c7a4df0294d55bf20233faf128"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "6aa7f7cfc8ce4fe85936c598e2c2ce11"
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
    "revision": "7ed36a16429d8c9c9549340b510e938a"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "66a2862513e94f5c73a1e02717c0e5c9"
  },
  {
    "url": "timeline/index.html",
    "revision": "e183e9b1108b255e42397fee42f7202a"
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
