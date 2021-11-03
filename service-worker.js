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
    "revision": "346a8741d3d7a8a77579ba3a474a4860"
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
    "url": "assets/js/10.43e159f5.js",
    "revision": "44d4a30d2ae0c1cb936c19d5a827a3b2"
  },
  {
    "url": "assets/js/11.88ddc2a0.js",
    "revision": "94966e750172657b37310dc83d2de1db"
  },
  {
    "url": "assets/js/12.54f32049.js",
    "revision": "bf5bfcf667dfe6d0be0d7382da21f568"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.5826df3a.js",
    "revision": "3c90597ea2770a3ab4b684d42fe21902"
  },
  {
    "url": "assets/js/15.d50d428c.js",
    "revision": "b1c7e3c0c729dde197f6372e85264adf"
  },
  {
    "url": "assets/js/16.ae4d64e1.js",
    "revision": "06624ec7c3afc0211bb4f639d10b09e2"
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
    "url": "assets/js/19.f9b33e48.js",
    "revision": "848dbd6b62979779f81bc241d8b6f7f0"
  },
  {
    "url": "assets/js/20.a1c9d186.js",
    "revision": "4eeb15748ca11273cbdc9f9a6ea9148c"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.bf003767.js",
    "revision": "9fb16eca5a0fe53cf39d2c3cb96fcf6e"
  },
  {
    "url": "assets/js/23.dcb0d8d6.js",
    "revision": "cfec9c8536b95434f6366c7d5c2254f8"
  },
  {
    "url": "assets/js/24.cacdceee.js",
    "revision": "90cd09585f62cb6390631ef6585b763b"
  },
  {
    "url": "assets/js/25.d53d3b3e.js",
    "revision": "d96667a7159901e93b0dec2fad2930aa"
  },
  {
    "url": "assets/js/26.239e7b03.js",
    "revision": "69be9553f1f5a1f11086b6b19dad6254"
  },
  {
    "url": "assets/js/27.5b416cd2.js",
    "revision": "661bb24a414bcacd4f544a7a2e1aa10c"
  },
  {
    "url": "assets/js/28.25c7b1fc.js",
    "revision": "5f66bdfb8df27c05b0c2f78396df8cba"
  },
  {
    "url": "assets/js/29.f6574ee8.js",
    "revision": "8142c6ec220d8e8069a74834d365f4b6"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.982e3a35.js",
    "revision": "b41811d1355e650a7c58e646fa380fce"
  },
  {
    "url": "assets/js/31.01b5a9bf.js",
    "revision": "101c9179622c9a254122ceea3d8f343f"
  },
  {
    "url": "assets/js/32.655f94b9.js",
    "revision": "ce694fb732fc1e731f17c51bd6a76649"
  },
  {
    "url": "assets/js/33.ce8dc3c1.js",
    "revision": "a3fb1c4ebae71f1ff6d89810084ece9d"
  },
  {
    "url": "assets/js/34.8f3b03b5.js",
    "revision": "3d39620b4eeac5a590f724b1d824bcc2"
  },
  {
    "url": "assets/js/35.e03aaf1f.js",
    "revision": "0a0c5575819816330ad77d8ff5248c5a"
  },
  {
    "url": "assets/js/36.29948e38.js",
    "revision": "45fe4939f16890ebfd75bf2365b637f7"
  },
  {
    "url": "assets/js/37.702d749a.js",
    "revision": "c513fa20a40468effc8b12c25e7709e8"
  },
  {
    "url": "assets/js/4.a3d0177f.js",
    "revision": "67138a1fdac208c38513b7004e1305eb"
  },
  {
    "url": "assets/js/5.4dff48d2.js",
    "revision": "db00dc705cfd4b66ddbfa203ae4ae59f"
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
    "url": "assets/js/9.0ad80411.js",
    "revision": "c8f91e10be5a5f7b57f7ec35d954a37c"
  },
  {
    "url": "assets/js/app.45283cf0.js",
    "revision": "32b2fb3d90d1593077319b1bb4542936"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "f4c5bd264364fbba1f471f1ad81bf26c"
  },
  {
    "url": "categories/index.html",
    "revision": "f21b17e4af4886a995543d14d31d0347"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "c77781802c43776439c8481f4d6be562"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "bf196232994cf3beec98f9ae193738d0"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "2e0a98f434809bd38a50a21ba571f0e8"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "8180f3941cfab94d96f04a0ea8d7c470"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "bc5f903a5c27125d4db1caa904d36463"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "2c165527eee016d92054e22ed961ec0f"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "7e149664457b40e964fd36b63ed74aa8"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "2a309f4cf1d9d081ee02438974ccb22c"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "fa68d5abd985cd118f36f89597065f10"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "5e449909408fec0c10283e10f519be05"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "6ee65333081046eca532022fa3e19171"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "d8931737bc8915d002a4a0f3759c5afd"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "49639a9c9259b41a0ba7bf29c6f239a4"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "bc15ceaa4f676b777eb8b35ed92503cf"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "87625a2da8eaf579ba47f36b1a4b41ea"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "e2ee4b0058f0b8486f4d5af2e39b5b30"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "83bf8ab009db27c60b3ca9e036c8f420"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "a82c9546090a7fb8902ee3d99d0a06c3"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "0a1ffad75f6b2282866776251dd5ca8c"
  },
  {
    "url": "docs/index.html",
    "revision": "2217d8c1c58d9a4956372abe172bc11d"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "e63271580148543cda5fe8032683fb61"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "31cfe19ab5344453cd38d218dea767e1"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "c8652ed91ad1bbfb0468e8784b37f0fe"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "75ef60c0b0b19e4987eca73276f1bc8c"
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
    "revision": "d3977246a70d3defe8c30087cb96af9c"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "e9fa273cefdae6b9e284c37e52b2bbbd"
  },
  {
    "url": "timeline/index.html",
    "revision": "99e4ef3770975fa9cadf2e03cf6147de"
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
