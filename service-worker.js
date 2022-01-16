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
    "revision": "44a4af9f19a41a49d8fd2376c66c73be"
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
    "url": "assets/js/12.1d4f5a30.js",
    "revision": "35958547cb888630faa7811f44453059"
  },
  {
    "url": "assets/js/13.b8e9da34.js",
    "revision": "9efc273c1daa714890ac88e9eca123c3"
  },
  {
    "url": "assets/js/14.afd88693.js",
    "revision": "3f1fd5f3ddab8acb24d9ed57ef1041a6"
  },
  {
    "url": "assets/js/15.518665a7.js",
    "revision": "5466ecbdf3e527ee1aeb542b0f23f3c9"
  },
  {
    "url": "assets/js/16.5f26778c.js",
    "revision": "a1721f0689f403ab9a2b9a07ebb28a3e"
  },
  {
    "url": "assets/js/17.149ba7d3.js",
    "revision": "28ddc6ac8489bc834098f842383d223a"
  },
  {
    "url": "assets/js/18.af8c2d15.js",
    "revision": "81cf9dc2001869e31119409b2a7d9c89"
  },
  {
    "url": "assets/js/19.9d667d37.js",
    "revision": "0fc9fc2c724e3d022a9d5f39abc5c9e4"
  },
  {
    "url": "assets/js/20.e0633367.js",
    "revision": "fbbbcc2fb173e0625d480969529b0c3f"
  },
  {
    "url": "assets/js/21.f3a77a1e.js",
    "revision": "11b157b171c9a6aa017d161c8637fa13"
  },
  {
    "url": "assets/js/22.b4282467.js",
    "revision": "d4c86e1842d721e1adba332c716b9f82"
  },
  {
    "url": "assets/js/23.8f221f5b.js",
    "revision": "969ad5145f3181df4f400a5dba7a70a9"
  },
  {
    "url": "assets/js/24.fe872c8f.js",
    "revision": "34262dffaa34ff92109ae463d26f52bb"
  },
  {
    "url": "assets/js/25.d42a4089.js",
    "revision": "10238226a035a26e0baadf1d754130f0"
  },
  {
    "url": "assets/js/26.04516f6d.js",
    "revision": "cf72974349925c7e107904017a6a627d"
  },
  {
    "url": "assets/js/27.4a5b11d2.js",
    "revision": "e032ecac8cef348280dd6a933cb5b61b"
  },
  {
    "url": "assets/js/28.63e28313.js",
    "revision": "8b11caacb81980238d3f0e5694edec1a"
  },
  {
    "url": "assets/js/29.5e7fdca9.js",
    "revision": "bb166bd8191c6f47f8d80d0d4697237b"
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
    "url": "assets/js/31.09b09c75.js",
    "revision": "96d2b841e53bbb250271302e88240565"
  },
  {
    "url": "assets/js/32.d8a9b8f2.js",
    "revision": "9244491b6c336e11af977c4696ab92aa"
  },
  {
    "url": "assets/js/33.f820c9b2.js",
    "revision": "1284b68001c6388c8ce983f4145f4dea"
  },
  {
    "url": "assets/js/34.3aafaab7.js",
    "revision": "6dc4908e76163a5866d6d685126adb04"
  },
  {
    "url": "assets/js/35.2ce73343.js",
    "revision": "95f51aa9bca6d09c342794ac793e5f0b"
  },
  {
    "url": "assets/js/36.d49e2170.js",
    "revision": "311b2655924b94d7d9a822da458551a8"
  },
  {
    "url": "assets/js/37.6c8cff6d.js",
    "revision": "26770b58fbe46959b43cfcb31f50a8ee"
  },
  {
    "url": "assets/js/38.dc15688b.js",
    "revision": "d3132fb4b76d665bfe8d1438af3a8670"
  },
  {
    "url": "assets/js/39.4e74e9cc.js",
    "revision": "da2c05bb53d2e2cb799879be1a25cbf0"
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
    "url": "assets/js/app.91f0cec4.js",
    "revision": "e75b8ebe473c75e60556581b7a310964"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "dbf94066ba3872b72a166e0bfa5eba2e"
  },
  {
    "url": "categories/index.html",
    "revision": "68aaec00fc6d4958f28405a6821a023f"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "e999e38464c09a82e49c8cf3bacc958a"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "28cdad8aee667e244432aceed6662202"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "3686b9eb0dc7ec71f3710dbb987881c7"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "ab92bd0999d3c6685943d14cfbd7000f"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "dc209221e821ade52d2e438742e37f2b"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "ae608bcfcebcba024c3beb8a131489dd"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "a09d5fad2f04978289f4bc4efc499b2b"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "d8050d0047ce6d3b021d4a06d3e974e4"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "09e088918359187be295f8a45793aa0f"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "3cb068924d8d2d6cc15905c40915bd05"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "8aaf13f7eb33ae0c3d11f31e3e2ffeb7"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "c0de6f999329b76389a3e211c624b0cf"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "fbbac27c1509b5e2244a6c9d5e2df44b"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "c3fed487fe54928658588cc19357ea20"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "e7f2256ea93baa08ebcc52ad5058bebb"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "0db6507c560eac4cf81a7bc9e3e7f4a2"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "11fd0fccc1a413415303964d65f2e0b3"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "48ffd53209af159d146255834de1e730"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "09df0132c1794f8a57b49c479c9078be"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "50bbb260eb5bbe32e3b6626e35f6329c"
  },
  {
    "url": "docs/index.html",
    "revision": "70398f3bc580c0d97b9ce34332f91dd8"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "04948c4bf5c8883795473e811a1d5618"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "667e4b7f57736f5a716b32810656f9aa"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "6661aa660d9eb459a3f141461a7b09d5"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "0441cd7cc98857d66e25400dacee274e"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "144577825be70f6475ecfa462c767ebc"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "0c06256f64a3bcbb2f67a40f7e18e99a"
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
    "revision": "36cdbebc094c10ec6930d39a4852ac42"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "abb0b8c83c4c2fd9052e03367bf38a1f"
  },
  {
    "url": "timeline/index.html",
    "revision": "5da2702e0e1cb9a38275de635cb26371"
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
