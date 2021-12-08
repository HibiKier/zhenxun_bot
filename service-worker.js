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
    "revision": "30081d54ed37c5e7f515a4228e373f33"
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
    "url": "assets/js/11.1a65b199.js",
    "revision": "cbef6825ece113ad2b352dd0feae0478"
  },
  {
    "url": "assets/js/12.fdaa7ffc.js",
    "revision": "1a47e6d96c5001196b94092a3c508637"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.59371a43.js",
    "revision": "c6c0e0c4c038c8bd8617b5fb10b9109b"
  },
  {
    "url": "assets/js/15.5dab83f7.js",
    "revision": "124c30bec93d1998fcc8937a783e261d"
  },
  {
    "url": "assets/js/16.ea1406c3.js",
    "revision": "50e99cec1bcf43d45b3c542187a55e6b"
  },
  {
    "url": "assets/js/17.45ea6a1d.js",
    "revision": "190fe38863648f0b4d971eaa71e96a3a"
  },
  {
    "url": "assets/js/18.dfd202de.js",
    "revision": "b142038ccc0e6b3b5631b09125477398"
  },
  {
    "url": "assets/js/19.afef6f5e.js",
    "revision": "c286dfc9533fd5d2c9bd1c7d2a7f840a"
  },
  {
    "url": "assets/js/20.eb0329c5.js",
    "revision": "3654e205266c4d9455af72e27bf29385"
  },
  {
    "url": "assets/js/21.8b0daf11.js",
    "revision": "7090eef2064fda42df432f1e4a21fd8e"
  },
  {
    "url": "assets/js/22.4db66b99.js",
    "revision": "e8c6cd470c5baf3445268c01906266fc"
  },
  {
    "url": "assets/js/23.8ed56744.js",
    "revision": "6b26fc460a35950d239dc949e6188c6d"
  },
  {
    "url": "assets/js/24.cfdd70a4.js",
    "revision": "87c4b13c18175c50aedeba94ea438fb3"
  },
  {
    "url": "assets/js/25.cf641359.js",
    "revision": "88255d1ff97a53df536db66d2d5a6e46"
  },
  {
    "url": "assets/js/26.84b59954.js",
    "revision": "c2ff1788e03dfcabeb7f0e8ea3d9f04b"
  },
  {
    "url": "assets/js/27.1f3bf036.js",
    "revision": "31f8a1eb91391b2cd8a6b789cf8b9bb1"
  },
  {
    "url": "assets/js/28.43010a54.js",
    "revision": "0c1ae87a0d590e86898ecb040c7ff7dc"
  },
  {
    "url": "assets/js/29.edf2a1fa.js",
    "revision": "575afb3fbe4cd76297c0fa1f2daf1fb9"
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
    "url": "assets/js/31.40fa9cb5.js",
    "revision": "e7c2e3f348107235b945375a6dcb426f"
  },
  {
    "url": "assets/js/32.9ab320e5.js",
    "revision": "2f1844ae79396a60b2331b3df7f84203"
  },
  {
    "url": "assets/js/33.c23ec5bb.js",
    "revision": "bc90b942368cbf79bc2a50d4b0393905"
  },
  {
    "url": "assets/js/34.7cb2dd8f.js",
    "revision": "5260db965462645da2aeaad19c5a80b1"
  },
  {
    "url": "assets/js/35.76679af1.js",
    "revision": "1f31f125e8bed0d4997aa452f2302476"
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
    "url": "assets/js/app.97ee0732.js",
    "revision": "d727a249018050ad3fe61c60c428df87"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "9cfe4e244a84bd5a1fc8252920cac811"
  },
  {
    "url": "categories/index.html",
    "revision": "2654ddb745928db98df298e2f8f2cc3c"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "5b39b9f7d9e7c81f57b21d77686528d3"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "aeac1385cf6633b2d7f0b26281ab6516"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "ee1843308bf7fa4b9280a29096975c70"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "fba88dc6ac35e0e9df28fe91e127af9e"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "06f0b3ab3e148bc146366b8f5cc4f13b"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "14beec1a1d95b4be92c31e17fba915aa"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "a80dba21560e1cb0b0b7d3b1eeea535d"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "d7757842e0b4fa651b0958a930d3638e"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "63a36f3b7abe0b6f9cd4d8b23268f710"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "ded74644bc19792bba70abb10e80fab3"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "603e49a3081ee12a5829e2c71c4fb99a"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "acde879ea2abbef76a1119ca8b3b456e"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "7240c18c4d8cf759a226c7d1c51bd4b7"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "7161db19f626b8f029107f3a57bee22a"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "b725c2c72fbcb78ceb10fde6deb076dc"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "8c458b90057567ed30c136cd60f946e1"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "16aca6ed1172321d2fd637635ecc15ce"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "6da5c6ef9e033684940a1e534b99ba4c"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "b63babd2f1fcc6788125a80d49a06b4c"
  },
  {
    "url": "docs/index.html",
    "revision": "59de0be40aec9186e831a203c68d06a0"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "53e2d14eae916ad7fe1d5d9f0db75c2f"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "19f03d15e816afb728d709ea57661c52"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "56ea0254ca67e47d962721f7f651c04a"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "3d5459094fc7913f183baf0e036020fd"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "0dd641c038e97beeb5c56ca35e928b3a"
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
    "revision": "c788398046c302e805c6312ff15b2750"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "3ba06415e7d49997c41f0fee7ce11e6b"
  },
  {
    "url": "timeline/index.html",
    "revision": "4f79ff7bd875b1b8408ca0895d9b927a"
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
