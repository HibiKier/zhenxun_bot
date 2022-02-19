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
    "revision": "5a8d870b435692415172a0a29c3657fa"
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
    "url": "assets/js/12.1485e48a.js",
    "revision": "e1c9a7ceccc08f990eec524cc03f1e96"
  },
  {
    "url": "assets/js/13.12022e1e.js",
    "revision": "f54f8760a522b111dae7d5ecacb0b7ab"
  },
  {
    "url": "assets/js/14.6dfda072.js",
    "revision": "0b2aec8e3e16e0e475f9b7b375cd3785"
  },
  {
    "url": "assets/js/15.78ad57c4.js",
    "revision": "287a0180a4a1a8e1d2b3bc42718bfcfb"
  },
  {
    "url": "assets/js/16.8aaf3493.js",
    "revision": "4ab55f41da21228f6db9000b8fa627e8"
  },
  {
    "url": "assets/js/17.cd1643b1.js",
    "revision": "bf8c6d3f1901d20e8f28834de3bcafcf"
  },
  {
    "url": "assets/js/18.ebb48faa.js",
    "revision": "9cef499b1d70d31bcec67d713ff9f8f2"
  },
  {
    "url": "assets/js/19.960144bd.js",
    "revision": "6fa08c7ad6f339c1e84b0e47597adf87"
  },
  {
    "url": "assets/js/20.53ad8f17.js",
    "revision": "051329d13f96145665980baae85f6046"
  },
  {
    "url": "assets/js/21.020fbf79.js",
    "revision": "8966590f88e13df68ff9b1f823583616"
  },
  {
    "url": "assets/js/22.b4282467.js",
    "revision": "d4c86e1842d721e1adba332c716b9f82"
  },
  {
    "url": "assets/js/23.0880ac66.js",
    "revision": "9ce463c796526797cbe5b7887a3f8058"
  },
  {
    "url": "assets/js/24.e49058f5.js",
    "revision": "b02bda31787501a13036f5b1a24861d6"
  },
  {
    "url": "assets/js/25.9163af87.js",
    "revision": "29426ac13360e7d5615f3e9c385b86cf"
  },
  {
    "url": "assets/js/26.f02f7550.js",
    "revision": "1f2e5da5f11ee05a6c4d8bf68ac7e364"
  },
  {
    "url": "assets/js/27.9af4959f.js",
    "revision": "55075857a69487f3c5fdc383e8bebf05"
  },
  {
    "url": "assets/js/28.56799a3f.js",
    "revision": "06eae8b1a1f1ee6d63ebe74f04219e90"
  },
  {
    "url": "assets/js/29.e45e5203.js",
    "revision": "183f43072b70169cc9cc9ce609cd92d7"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.2f3e8305.js",
    "revision": "bbd9b87e755af728db352ba648213ec3"
  },
  {
    "url": "assets/js/31.f4213db8.js",
    "revision": "d6c05f9b069afa44defd189a9e21ef6f"
  },
  {
    "url": "assets/js/32.3b5db4d4.js",
    "revision": "276ed257f11970e3b72e917e07a16716"
  },
  {
    "url": "assets/js/33.64f147d4.js",
    "revision": "02661d8451dc715306a70eb508aa9172"
  },
  {
    "url": "assets/js/34.3aafaab7.js",
    "revision": "6dc4908e76163a5866d6d685126adb04"
  },
  {
    "url": "assets/js/35.9f11cb6b.js",
    "revision": "4d75f613cdfa7b91336368542400bdcb"
  },
  {
    "url": "assets/js/36.c4588d1a.js",
    "revision": "fd520d7d2bc59f85f5abe643315a560e"
  },
  {
    "url": "assets/js/37.949ce7d9.js",
    "revision": "65a67f2584c3f2f6d442fc73e4eb54b1"
  },
  {
    "url": "assets/js/38.4047f1ca.js",
    "revision": "bb140e7fc5517e5831665c8f13937503"
  },
  {
    "url": "assets/js/39.d4f57553.js",
    "revision": "0729561204e04fe58800d25fca062ff9"
  },
  {
    "url": "assets/js/4.7b2626bb.js",
    "revision": "1642b25041b4fce55d1447249497b0b6"
  },
  {
    "url": "assets/js/40.1a0e089c.js",
    "revision": "c5981eb903d487c52546ee2bacc65415"
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
    "url": "assets/js/9.1a1a5b76.js",
    "revision": "e9ecf36d438498b42feedd5f5d55cb54"
  },
  {
    "url": "assets/js/app.c41b93b6.js",
    "revision": "ccff7423293de3eaedf48c2f1272079e"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "a06d7c9b22b9554397265cbea6e8e6b2"
  },
  {
    "url": "categories/index.html",
    "revision": "712dde8862f2cdd502dd3c2e97b98ebb"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "747d629533d05a3e52d812724a0152ec"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "0c06c7016d87491124c8c8a4b2e60641"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "28f10d256d2fc4a606471c45096ea92a"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "6b297e334f3e8a3097165d8c0292d3e5"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "180988b0b2847b50f6e74fb3992e6309"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "af26eb7d4f609632727bb995e2ab283c"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "72e1586a7043ffb8c6ce9fefbe3982a2"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "2a4cee5a2144ca56d2642a5e95478996"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "2806de1a73e4cd7dcb802012a323eaef"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "4a60dee50ac897f15ef53721c0373c50"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "67dece84b2540706581897b6de2b074d"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "b61fe8d1cb655a12000f56b8b7607063"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "33305a889afbde70a25320bc82fed867"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "33e97c9c896fe12aed9139a44f232543"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "7d32ed3de3a25c047b0058da9e1f5947"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "4a89f5d8d22fc56a79f9e3b17f4af8da"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "cfede16b22ca553cc3071b92094ce34b"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "62dc87c7322fc53555ebf7c519e0072f"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "48323af5ecc4f5a7fb318ca759bd5acf"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "926ddfcfb4de7691913eaf1674589f87"
  },
  {
    "url": "docs/index.html",
    "revision": "b5f1e8bf57824325c6c7cc8ce145d063"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "e1ab7946ae717cca8ac6caa4e8167e02"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "8ca1a72a230a0206b18998cc37a04301"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "903ad49e58762394dd5726d3e3a8feee"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "11bf4948a66a555a472ac8a4a1e69a0b"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "8e22ac663a9d1b7cec441c3f7bc536ac"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "853c1d1dd3ce5a148738691cefc7f064"
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
    "revision": "4ea7ccef2bc3925ad1aaefe26e96a9f7"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "1a16706b149d225cbe0e6d8fff13978b"
  },
  {
    "url": "timeline/index.html",
    "revision": "1b196a33e1e81caf8d3e11fe7e1dd55d"
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
