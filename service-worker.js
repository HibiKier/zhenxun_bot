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
    "revision": "a4f02b737bb3f0476db926290075e9de"
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
    "url": "assets/js/11.57ced948.js",
    "revision": "ca44b101add166c6012feb8b68628c5f"
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
    "url": "assets/js/15.d50d428c.js",
    "revision": "b1c7e3c0c729dde197f6372e85264adf"
  },
  {
    "url": "assets/js/16.077785ab.js",
    "revision": "967baddd9d4016f3765d958337472fa0"
  },
  {
    "url": "assets/js/17.45ea6a1d.js",
    "revision": "190fe38863648f0b4d971eaa71e96a3a"
  },
  {
    "url": "assets/js/18.69f5ddba.js",
    "revision": "8a67d1255d077102f7eb264c35a3355a"
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
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.32cd33d1.js",
    "revision": "c570ddb385290273a64610bd7a0d7ff5"
  },
  {
    "url": "assets/js/23.c43292a1.js",
    "revision": "45d6b93430abcf431a56dc7d5404fe78"
  },
  {
    "url": "assets/js/24.9794dac5.js",
    "revision": "51f9008e2bb86675ae80b6b55295ff89"
  },
  {
    "url": "assets/js/25.72e19154.js",
    "revision": "bab6ad8c6c361836ac8536a0efcefcb8"
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
    "url": "assets/js/28.d2a2b076.js",
    "revision": "e1824ab509a9d2892ad4a789f0321e16"
  },
  {
    "url": "assets/js/29.d2df256d.js",
    "revision": "9f4449b4a2280523c697653fc134f6fa"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.1229ee54.js",
    "revision": "523cfa376f7ced39ffaaabe72b41f26a"
  },
  {
    "url": "assets/js/31.255ac4bc.js",
    "revision": "2c80c834ebd93956a40f297f7c177024"
  },
  {
    "url": "assets/js/32.9ab320e5.js",
    "revision": "2f1844ae79396a60b2331b3df7f84203"
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
    "url": "assets/js/app.b43d42c6.js",
    "revision": "111562e5d10ffa7e70a77fbeef2243e9"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "9691eab3c5082708f58f8573ad002f08"
  },
  {
    "url": "categories/index.html",
    "revision": "af981c0ae6d4a86ce5ebbf711c84d176"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "5669da3a52dcffb1564504a237c8a6b8"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "0353fd348cea6718d38958f503b850a8"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "f9b676c2673973c2c51af2e3b040db1f"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "f65cda4d29af12b49301d91383c87e8a"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "acf388fa7231c5d65cf0ba379b95779c"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "0ae5a0b48872dffc3fb49f3b0184dd76"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "1424e5f90261e6d30e008e90e7cc3564"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "1eac62255f580c0e850d87285821adad"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "7fef928f1f613636b3f447c209516cb3"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "a9c7384a0dd858099e893e63b5fe8276"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "9fb5fb4110340228065731cdf3cdfbb4"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "be6931c00858e79f11cec311ed2e1bbe"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "cbf80d513ccbd4e4171f77bdabb6c20e"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "0d1e326cf90b2adae69ad44e52dd5ace"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "751e294f3d062cb70f8b3473d25f2ef0"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "8a4d98bf06336de01fc65fa846f504fc"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "5c008dc98164be1bdf9f32c8c687e0e5"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "bfcd7e71c8372c8e8f2800a0224e10b8"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "671bc144e1b323305e1de99a09a7ee56"
  },
  {
    "url": "docs/index.html",
    "revision": "56b9f2848331de3f6a0a15ec12fd652a"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "1d901a69b464e5f99674daab0b7cffda"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "ea4477fd73434556d5538c398961e5a1"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "39841d3e69468535848823f074f44fcb"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "873fed22ddddff7eecdbc54d4087e268"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "198fd7f44b2eb2c669e7d7fb026a247d"
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
    "revision": "051aa4cd058f4e440c4ca937a060bf7f"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "0003c572073244a88e56046cdb99644d"
  },
  {
    "url": "timeline/index.html",
    "revision": "7c2b5dfcacd62774ae304787329054c7"
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
