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
    "revision": "6c9b3281f1f7adb59de34e9a51fd5d00"
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
    "url": "assets/js/12.5865da78.js",
    "revision": "e33a4c776f94c8c90d19d406d437ea7b"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.4cdf84ba.js",
    "revision": "7901d9b41fe20d6cde225656c8861b0b"
  },
  {
    "url": "assets/js/15.5dab83f7.js",
    "revision": "124c30bec93d1998fcc8937a783e261d"
  },
  {
    "url": "assets/js/16.a812ab0a.js",
    "revision": "87f6df616f3e4930566e1cc40294d918"
  },
  {
    "url": "assets/js/17.27df5e56.js",
    "revision": "51a613012bf4ab90e4ac8342dcc78c83"
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
    "url": "assets/js/20.7f5c4ee8.js",
    "revision": "3dbd1c6b88933b5a7f1c31854b9a81dc"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.e35682e2.js",
    "revision": "a62679d4b48218e2d64b10546bd8f180"
  },
  {
    "url": "assets/js/23.c43292a1.js",
    "revision": "45d6b93430abcf431a56dc7d5404fe78"
  },
  {
    "url": "assets/js/24.a6a9e5c3.js",
    "revision": "eea906128048bc135cf73682b44e1759"
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
    "url": "assets/js/29.ffe0e873.js",
    "revision": "60cd5a9bdd5162796a823b4bb929627c"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.a40fb080.js",
    "revision": "5bf084653f2393315e1ce746f7d4b255"
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
    "url": "assets/js/33.df55760c.js",
    "revision": "99de04199b9c61073f8629931def5c7c"
  },
  {
    "url": "assets/js/34.d96ee9f0.js",
    "revision": "876f43d749812667a465c9cca40c0fa4"
  },
  {
    "url": "assets/js/35.a1bb493d.js",
    "revision": "8d5228555dff1ef2f4bd4f637851f636"
  },
  {
    "url": "assets/js/36.7670928b.js",
    "revision": "dcbc9bc67b56a5f6ea817a1bede6c7e4"
  },
  {
    "url": "assets/js/37.e96041f8.js",
    "revision": "3e6165e75834a5a41ff7c57d672f4512"
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
    "url": "assets/js/app.779b5e84.js",
    "revision": "2bf3e97c9c8d050ff1c2ac92eb627ea8"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "3ef81718e5b7bc8d4bc69e0c2c43e87a"
  },
  {
    "url": "categories/index.html",
    "revision": "094736daaf47d382fd4ff9607a08051a"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "1a51c4241734cc8e2e54b3252b1f3b7b"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "fe87b579f9e22e9374594faecec981b4"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "329aa94292cf875220f26fd0ac0554ef"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "95ebfabdf7c8d36a97902d43d9cbd1a0"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "d27470e122e2970e7bf5b1fa9a92f538"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "cab8a614ab2a160d81d254cbbcf8e082"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "4964b20a9d7f01c6e0d0a58da079e326"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "7d0588c80b0b9f70b8a433f1764968c9"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "0dd4ec60ce2174b7628d1cfc1365162b"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "38bef1d792b0be238568eee39cc52ada"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "44e5904e864c97343605ac7c12199256"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "83012e7595510c6cbeb1af54f39ee723"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "3d8cca5cf8827ae373f3974738b4fc66"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "98dada0f1d5388332df41466d8a8b2a0"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "f071c0c5beb60131af3922f787b92fa1"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "6cc29647a5eb6f0d84c9a388af2d9722"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "a22c94b470a8301fa9eca6159f628a09"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "3d7a3e2f0c7086ec1921dc64610ed7b1"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "2762ce7a969edcae16864d7606dd8a38"
  },
  {
    "url": "docs/index.html",
    "revision": "c11e279ae52008be1bfdb002f9a8af32"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "9673381302c86f2804016c72feccb66d"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "3dee9cb8b010645b69c73622eaae6a1a"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "ae14d55b3ce6a61ad96465cf0e4f903d"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "47c51c763a9a7f12b44f4c20c85e873a"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "e47f5983569dffe0fa77182e2bf0534b"
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
    "revision": "ce402c0b7c647d265a79e61a6449fa33"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "c5fc35fdf64983fccc20165c42b93b8a"
  },
  {
    "url": "timeline/index.html",
    "revision": "84fda98d5647b542c0b45667c44ad1b7"
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
