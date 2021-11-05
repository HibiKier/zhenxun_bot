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
    "revision": "116d12c74b721a2053d0fe280c94cd2f"
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
    "url": "assets/js/12.eb074e26.js",
    "revision": "4c61d6d62ea9312335d1fbc02c59fe62"
  },
  {
    "url": "assets/js/13.3f1eb4dd.js",
    "revision": "419541c23df8d69ac12099e1e9acb719"
  },
  {
    "url": "assets/js/14.b7507924.js",
    "revision": "a566e59a2f2fbe4030ad8c45b0a2a276"
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
    "url": "assets/js/22.ae7cddb4.js",
    "revision": "e23e9a6c7d5c9518d76184202d23541f"
  },
  {
    "url": "assets/js/23.2720d2f6.js",
    "revision": "78c3c4d06e9a8ade25ce3b4be79b06d7"
  },
  {
    "url": "assets/js/24.64cee759.js",
    "revision": "98713864d4607ac796329ad9540f3fa8"
  },
  {
    "url": "assets/js/25.d96bb949.js",
    "revision": "3779f6a70cfde313ff3b9bf1b28b0fcd"
  },
  {
    "url": "assets/js/26.f16d0fca.js",
    "revision": "f5301878c618ab5e6c26741b9fad2f47"
  },
  {
    "url": "assets/js/27.e8cfc108.js",
    "revision": "8cdb222251a8d784116bc95762916402"
  },
  {
    "url": "assets/js/28.728c50e8.js",
    "revision": "09dfa1557b859af895d6a738c7f871b6"
  },
  {
    "url": "assets/js/29.bbb9d8b5.js",
    "revision": "4ba97b56c33b267c4b909f932f3dcb69"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.11015aee.js",
    "revision": "017a4d230de1ef827460eaf07da5a632"
  },
  {
    "url": "assets/js/31.48dd0e07.js",
    "revision": "2f6d25295470e49f399573347aa7cf09"
  },
  {
    "url": "assets/js/32.ce79d54d.js",
    "revision": "6d5cdb3350965a9bbb65d510a0bf80da"
  },
  {
    "url": "assets/js/33.8c466c9f.js",
    "revision": "97356d439bb95e1106c6965fce031009"
  },
  {
    "url": "assets/js/34.8dd9bae8.js",
    "revision": "1bfaa78f06b4ff4f72224143c5d29179"
  },
  {
    "url": "assets/js/35.f38f4add.js",
    "revision": "c0e30034b46f02dd0425b3a79f14da65"
  },
  {
    "url": "assets/js/36.638a871a.js",
    "revision": "4b86c84052a2380a1d7ab14f88025acb"
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
    "url": "assets/js/app.52d7f4f4.js",
    "revision": "723affb0b9f04cc1afa6b7f1a7d7756b"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "1d3414be9c62187e10cc915c58b70ece"
  },
  {
    "url": "categories/index.html",
    "revision": "fbcaf735edbf2000d09ae7d0d9a540f1"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "2583973d5a12e2459a72e55e624aa5ff"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "270bbcfc037b12e9eec67fd964e8ae11"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "5178f2674c14df8e4cde040750974afe"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "c69bd18f355aaa5cac5b90f2f571abca"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "4d6f0c5f3bd85854a588f926a00421c2"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "f9162c910672a49c3959e4274fa1cb2f"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "3e21f42f468889a7c7d779d2078b94e1"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "19fa61c5fdf6832fd53904f27ece70e7"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "a188e35ef1de44e33f7cd2aa78b26887"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "9076f576c4b0ebe4ea38f0ec98d41ee8"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "a48d76365a686ab39bba79451fd2ce45"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "768cfaa9b679e97669459e50236641aa"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "895e0083be27428765266ee01746d10c"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "26079c69a8c9589d68131da4a0d6f518"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "05e7ad331c17c022865435a1667ce83d"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "1eeb2e0cff3b8bb0e709ff12be5fa0bd"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "68e8a9c449fc4c3eac20814312ab6b6e"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "ee0ff3caac261cfbde13a8a5bb1ea108"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "19e1148cea885ce248f94ba270eed18a"
  },
  {
    "url": "docs/index.html",
    "revision": "14e92807ecd928f62e92144b04ea2a8e"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "5729c796c5affbed9f38db0ded2215ed"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "27184c8b3933f66382e2b6b3c3a02901"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "99d444fe2ffb9dcd377564600b73e946"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "4cc392614cd3279a2181d81d8c63d10a"
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
    "revision": "7e51af2e1f9a8acc16901021a98cb839"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "b221fd89562db1eab88caeef2087ec3f"
  },
  {
    "url": "timeline/index.html",
    "revision": "3a45328555c7609a93285276ef16fe03"
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
