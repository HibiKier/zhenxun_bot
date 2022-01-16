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
    "revision": "b5be0f34eed8679f72b68e4d4ad5a182"
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
    "url": "assets/js/12.2b14619e.js",
    "revision": "8e558af896a40de63b4ec32c465fee70"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.6dfda072.js",
    "revision": "0b2aec8e3e16e0e475f9b7b375cd3785"
  },
  {
    "url": "assets/js/15.b84474fa.js",
    "revision": "835f257f01b7f22ac56080ca946d93b0"
  },
  {
    "url": "assets/js/16.7e579d0f.js",
    "revision": "9d7aaa60d9ee51752c2208b59dc9d3b1"
  },
  {
    "url": "assets/js/17.149ba7d3.js",
    "revision": "28ddc6ac8489bc834098f842383d223a"
  },
  {
    "url": "assets/js/18.d3cfdf75.js",
    "revision": "51bd8d7d267af62d892163601f5f578a"
  },
  {
    "url": "assets/js/19.e974d4c4.js",
    "revision": "1ec5cd060774bc4cfab4b4d5c1b1bc71"
  },
  {
    "url": "assets/js/20.681b451f.js",
    "revision": "04982239146d35a585f39919491216ed"
  },
  {
    "url": "assets/js/21.779b90ec.js",
    "revision": "c48b2468f7d4ac6ec68f120d6f49b334"
  },
  {
    "url": "assets/js/22.4a7bdc03.js",
    "revision": "0a43f4661862caa492dcd52f08cd3880"
  },
  {
    "url": "assets/js/23.23ea6a00.js",
    "revision": "3b88e4b827758f2debf9e2a9956162ad"
  },
  {
    "url": "assets/js/24.296c5aea.js",
    "revision": "090f39c702fdea9ef5e59110caf2fbe5"
  },
  {
    "url": "assets/js/25.6c516c19.js",
    "revision": "115e89e37e960bb15722a11d59011fb0"
  },
  {
    "url": "assets/js/26.60d4749f.js",
    "revision": "f03e411a963b1707abd73c339efb8df9"
  },
  {
    "url": "assets/js/27.8b4430f1.js",
    "revision": "27553f6cd11f8a4c07ef0ae06df46f1e"
  },
  {
    "url": "assets/js/28.bb44c620.js",
    "revision": "d88e22e7640db6294e09e2b35f34ff56"
  },
  {
    "url": "assets/js/29.82256878.js",
    "revision": "ec968591b36ae11002c126fabddeff10"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.6b576ce8.js",
    "revision": "ae5c5b10a7322c096c50a52f2caeda44"
  },
  {
    "url": "assets/js/31.26df20a4.js",
    "revision": "dc550aceda2c50fe673c7135edd3cf80"
  },
  {
    "url": "assets/js/32.33fd52a0.js",
    "revision": "f5390b2c5991d7056708f6fcf4ce53ea"
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
    "url": "assets/js/35.7a98b089.js",
    "revision": "23e7ed9ed7e7e3afe8943c7e4308dec1"
  },
  {
    "url": "assets/js/36.d49e2170.js",
    "revision": "311b2655924b94d7d9a822da458551a8"
  },
  {
    "url": "assets/js/37.60a6043d.js",
    "revision": "6b23858d145ba4e412a5cebf3673e5ed"
  },
  {
    "url": "assets/js/38.48ffd6b8.js",
    "revision": "334944e610600db4be3f2bad6a007776"
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
    "url": "assets/js/app.697d4a11.js",
    "revision": "a8f6d84d836be3acff8f94e396b936ea"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "82f2db6075508e1cea70dbfd39fc5f34"
  },
  {
    "url": "categories/index.html",
    "revision": "8cf6002fc759ccc905bd8e67f6d6854f"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "4bbfd2cd46ad0ced7871d00ee7dc10f1"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "1f03110d2c5f480e0df67c53b5f672dc"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "09362257f430d3a411addbf9630d263d"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "79c790c261588b2addf06c3663736314"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "7ca3d36554d29d105bd716741a4fd3a6"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "0a0bd820db8f011f7e531989ba1e6cc1"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "c744900034e995ed04013731f0b163a8"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "566f2ca9ddd88e1c6e3a48b2957c8c71"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "e192b8d4c746571af4615a3eb98c87a2"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "0a760585cbef786a998f317b61ac643a"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "0ed5a0617a8bc1f5532218d693649a73"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "ad19b64e470dfe4d9e7342d2e05e413d"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "1989740038d037ee390877084fee715b"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "55e2099c49160ca833a89c4a5bf701b2"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "9c1bff493e766b047737d5369f6933a1"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "fa87e9897105fc0f67aeeabfee6971e7"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "2b4f565ba66c66086749bd9ba31941d2"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "7e73aa894eedff68e04338203ad797dc"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "2e675f3d5a8c3eda559b5f4b6b0f058f"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "0124f92c291fd3a108eaebb82834b9c7"
  },
  {
    "url": "docs/index.html",
    "revision": "cef05dea68b945e3fdad81f1915bec86"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "6952998c0169cc62191e392f381c8a42"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "ea596d9cc001ea58f9a2903392c1a30e"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "43117f35b8c3801593953d50d86c3929"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "f37864d7db2e08003ea44991c99c8a2d"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "0f484860d749e4bf5fcb3b16b944588f"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "653bfc2ba3d032e6c6d93d6d1071341d"
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
    "revision": "875627f6d9269a516143a2b954221356"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "84a99323467dc3f5cf0a4bd5acfa804f"
  },
  {
    "url": "timeline/index.html",
    "revision": "17d3763ec86eb6d75ee20f84fae56d44"
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
