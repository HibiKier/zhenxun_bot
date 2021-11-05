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
    "revision": "01390fb1b06dc1d46b2b744b2405e2d2"
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
    "url": "assets/js/19.dc0110bf.js",
    "revision": "2e2fc5388e7f10c9b41f71977abc4f0f"
  },
  {
    "url": "assets/js/20.e5eba767.js",
    "revision": "ce25d40436154757c0a6af1fa1af3b0f"
  },
  {
    "url": "assets/js/21.e709c1f6.js",
    "revision": "751908ef76ef4a1083069880567bbea6"
  },
  {
    "url": "assets/js/22.059a7373.js",
    "revision": "7623858435792ef8ab970d59f8678c03"
  },
  {
    "url": "assets/js/23.a95af780.js",
    "revision": "72257fb5f91c9998f397c7ced73aa619"
  },
  {
    "url": "assets/js/24.3c068afb.js",
    "revision": "56ca55bdf0890cf83caaa0a9c0bbc603"
  },
  {
    "url": "assets/js/25.3f251bb1.js",
    "revision": "ee18b97a7fca0d30ecd9ff3abd354982"
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
    "url": "assets/js/app.531e81d5.js",
    "revision": "569145be9b4d8e4b247d592b39dc277f"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "636fe4cc671b7cc5fe9b90adf6baad07"
  },
  {
    "url": "categories/index.html",
    "revision": "d4206d404dbc6652becd2b3d94c8cd05"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "381930335bd2d41b4c956420e330e9eb"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "745acec738dc244a663be4fe97543a49"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "9a949b56881b09bf341e60beaadd01bb"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "95d591b918f586d81b76f790ee578372"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "0322a7acf1d2ce96dae8bd5574cc2cfc"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "3dcf0f3f89f5964cbb89f234ea75a22d"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "fe70ce4a34448d7d930b2765c196696d"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "c4d430aa14d312d973fa076b95200286"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "30de9c6e720b2ec3818d751ddb88d33a"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "f94909af67b81edbcaee072fc072c146"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "a7da2e0804d2cb2513d22ff806a99067"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "6723f0b931b01a440a8f1abc2d920f87"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "6247228ad17b1631365046455fe6c0ac"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "951ff77e7fb47df3f0a76016caca7300"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "01c04a82ee6a69d43703f831cb318212"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "a799c842e2bc6000ba34faf4c14d7319"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "c928d111c861e701af5425317a4f6c25"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "feb4336966ac0e65f28b08100452020e"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "6d484de2f862d1dd30c9f1232912da4d"
  },
  {
    "url": "docs/index.html",
    "revision": "4be5fa0df1ef8d2728dd6db107d5d5d6"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "660fd800a8e0a361611477608b95fbac"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "fcc6c22dfc444b7929ed2b8d67010680"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "2b4c666d57fc93e294068dfd33977253"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "93d79ae90e3bd42e487fc20a483c7fff"
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
    "revision": "a219494e2030c640ab72b6d1a9147ee0"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "3297336ab96187ac762152f2b6397fb8"
  },
  {
    "url": "timeline/index.html",
    "revision": "cef80dc40cadb7f59641156370fcce99"
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
