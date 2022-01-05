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
    "revision": "6853bdf587683615a444647ffdee6c7d"
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
    "url": "assets/js/12.5a8ad49f.js",
    "revision": "869cfb17eb6af15b17689aa76de0df9d"
  },
  {
    "url": "assets/js/13.712c7799.js",
    "revision": "e1af5d9cf2e5abf28c154671e7c44992"
  },
  {
    "url": "assets/js/14.afd88693.js",
    "revision": "3f1fd5f3ddab8acb24d9ed57ef1041a6"
  },
  {
    "url": "assets/js/15.2a93a3fd.js",
    "revision": "8e7b2e4f7a535aef92601d9e769c0a1f"
  },
  {
    "url": "assets/js/16.5f26778c.js",
    "revision": "a1721f0689f403ab9a2b9a07ebb28a3e"
  },
  {
    "url": "assets/js/17.b566ef83.js",
    "revision": "4037aa2af87eb6d7c2c04cb3aacf3bbf"
  },
  {
    "url": "assets/js/18.f4dc655e.js",
    "revision": "794218fc967cd41d6c2430b7b1306224"
  },
  {
    "url": "assets/js/19.9d667d37.js",
    "revision": "0fc9fc2c724e3d022a9d5f39abc5c9e4"
  },
  {
    "url": "assets/js/20.201e4a0f.js",
    "revision": "b6fc875c595f74aa07dffcfbc71406f5"
  },
  {
    "url": "assets/js/21.64c4e02b.js",
    "revision": "38838919f706acadb0b554873b1f0ca2"
  },
  {
    "url": "assets/js/22.5f41920d.js",
    "revision": "b67f7d76f8ea505f4d0ccd091ee47772"
  },
  {
    "url": "assets/js/23.8f221f5b.js",
    "revision": "969ad5145f3181df4f400a5dba7a70a9"
  },
  {
    "url": "assets/js/24.990358b5.js",
    "revision": "aeab5974e9057a8c838dce798cde6e27"
  },
  {
    "url": "assets/js/25.9163af87.js",
    "revision": "29426ac13360e7d5615f3e9c385b86cf"
  },
  {
    "url": "assets/js/26.a06dd22b.js",
    "revision": "a68edacac23971304520d0541f34d127"
  },
  {
    "url": "assets/js/27.1173cdab.js",
    "revision": "b451023930e9c3452c16a7bc6ab21e4f"
  },
  {
    "url": "assets/js/28.ffd3d529.js",
    "revision": "274a642120168691b93010988b3096d1"
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
    "url": "assets/js/30.57ab7f37.js",
    "revision": "6bdd7347782eb68d215eb618d6a09a0a"
  },
  {
    "url": "assets/js/31.7bb19d80.js",
    "revision": "1ab8850737e768adcc47400d26842cf8"
  },
  {
    "url": "assets/js/32.33fd52a0.js",
    "revision": "f5390b2c5991d7056708f6fcf4ce53ea"
  },
  {
    "url": "assets/js/33.f820c9b2.js",
    "revision": "1284b68001c6388c8ce983f4145f4dea"
  },
  {
    "url": "assets/js/34.516a0a66.js",
    "revision": "f96922b6af15066bc2a7c81de6f2cf60"
  },
  {
    "url": "assets/js/35.05759599.js",
    "revision": "ab9e76e1ff7c5c4c4ee0d26d90ac3bdf"
  },
  {
    "url": "assets/js/36.59f9bdbf.js",
    "revision": "c1f293a002a916433102239b5b8627d5"
  },
  {
    "url": "assets/js/37.f256598a.js",
    "revision": "14d2ca0f6bc30120b3823d93d86bd170"
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
    "url": "assets/js/app.446f00c6.js",
    "revision": "60566679f40de1c86f41461c87bc1be8"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "ca0bb9da152743129e06ad100af02835"
  },
  {
    "url": "categories/index.html",
    "revision": "5a7cadc435d949586deb3186dadde2bf"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "49d65594215121161b2042ee0ac8a81f"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "d3bae6da215f5c14361322ff240f6274"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "2b367b4e40170b89af6443b0dced156a"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "aa0c5f5a669d7b466a5b1ca2f215be09"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "28a48fcbd10dea4e3c210507f5ca29ee"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "b309bbe8a2586cf7c779029efce1fdc2"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "0a4eaec4341905b37a5d769993a1debd"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "2bccae7e079c7bac3b27c4fbf238eeae"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "881cfb5c7c8ab22c9fa3eb12d05381ad"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "4ed972908363c90cc43a50c054973425"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "3f46618fe743aeaf2c151f8da0073c6a"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "33a919ac1c2c114a3ec51721532acd81"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "9a6e707dc1c08222389d6bb765dd5c16"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "ded703256e5d5e72c879e2394c243429"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "072a5bc32c14a30bd9326cbed8c85359"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "75814f2475907abf5dad286a8456ee72"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "b8e5ac2944e79478f6fcc51d5ccd49b1"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "076fadcff7ca5e18127709207b64ca41"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "b3c2af33f1b859a1cbaa0dd0754b0729"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "8f37c9970ce665b24614f66798fb2e6a"
  },
  {
    "url": "docs/index.html",
    "revision": "d4572d729cacc4cc03de73ef032cd52a"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "b2f41b23f5bac2b65af2d9e778a206c6"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "fd92e7df623db63e58225146daa31892"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "ae95ea88c974d6ffe8511235cae99d8d"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "5234ecda390038bc95226a14246a6b49"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "fe5c13a19376b194992b4d0afebdb4aa"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "942319f90aac9d7b1a68aa7100afdbb7"
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
    "revision": "852cb5a14a95ab34e3f07be2752d8285"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "2c661ffff080ba216bbe56295dead3d6"
  },
  {
    "url": "timeline/index.html",
    "revision": "a7e91c11fa837597342d79eaec87e53a"
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
