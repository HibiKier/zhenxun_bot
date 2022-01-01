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
    "revision": "6f804733c3d110b27502d3dfa58206f1"
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
    "url": "assets/js/12.d53de2a7.js",
    "revision": "93ea3ecd0dca74df568f8c39a4d8efa8"
  },
  {
    "url": "assets/js/13.48a7b659.js",
    "revision": "f19b280023f38185429f1711ab5c5260"
  },
  {
    "url": "assets/js/14.094db6fb.js",
    "revision": "f61423c71a996ac861f873c89b9fb65d"
  },
  {
    "url": "assets/js/15.75bd2115.js",
    "revision": "aeecfab9223523251e19954404f194b2"
  },
  {
    "url": "assets/js/16.3402ec8d.js",
    "revision": "43369626d4cd473d3f91450b87759763"
  },
  {
    "url": "assets/js/17.3774b656.js",
    "revision": "8dbdf3114376c100b655e5f21ec3f852"
  },
  {
    "url": "assets/js/18.6ff96ed2.js",
    "revision": "a8050b8e4e3d6d228f194c3f9f0dab92"
  },
  {
    "url": "assets/js/19.cbc91e9b.js",
    "revision": "0d3b7570e53f37770d9d6676794d9207"
  },
  {
    "url": "assets/js/20.005a0c7f.js",
    "revision": "92209e30d4790af1cc16c49ff537cde5"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.ab9e6f10.js",
    "revision": "5df87c28f36f86750fbea1f2505596b4"
  },
  {
    "url": "assets/js/23.7ff5225b.js",
    "revision": "f27818cf83d50b599f3631a28e295046"
  },
  {
    "url": "assets/js/24.a6a9e5c3.js",
    "revision": "eea906128048bc135cf73682b44e1759"
  },
  {
    "url": "assets/js/25.3a937069.js",
    "revision": "e38dc1476957ef3eb29d5e331b4ba131"
  },
  {
    "url": "assets/js/26.2ebc3d9c.js",
    "revision": "eb030d073a1d88d8c3a4b901f2aa5abf"
  },
  {
    "url": "assets/js/27.fad3465f.js",
    "revision": "43b86ab89b70ece1c646fd71f6fcbf8e"
  },
  {
    "url": "assets/js/28.18705f4c.js",
    "revision": "0a69904f3c43b35e79bea8a0cb11600b"
  },
  {
    "url": "assets/js/29.3c09fbcd.js",
    "revision": "00916513d278e6437aea94502ef94768"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.b2e2a165.js",
    "revision": "80635c4262a06f6864be69a31fcf71c9"
  },
  {
    "url": "assets/js/31.2cf49256.js",
    "revision": "5b422188b04a5276f31c54cbfafc6b08"
  },
  {
    "url": "assets/js/32.3563c898.js",
    "revision": "a2b63d69ba5023cb529a02a90c7b13db"
  },
  {
    "url": "assets/js/33.f30ff14d.js",
    "revision": "33edb5731c45f7b03ec6ff25c985fc7b"
  },
  {
    "url": "assets/js/34.cc2e625b.js",
    "revision": "9fedef46e0eae1f83366f1d4c90eba62"
  },
  {
    "url": "assets/js/35.8c661e80.js",
    "revision": "50a8e4d6b849bfe0b3c3dc94dae10b2d"
  },
  {
    "url": "assets/js/36.49073d76.js",
    "revision": "923a9a473c62d143c22235f46e100aef"
  },
  {
    "url": "assets/js/37.3b342986.js",
    "revision": "a5693e82454667373beaa3cd965830f3"
  },
  {
    "url": "assets/js/38.33fc3f94.js",
    "revision": "1b91745ba5d0b48a18404c014aff00ef"
  },
  {
    "url": "assets/js/4.7b2626bb.js",
    "revision": "1642b25041b4fce55d1447249497b0b6"
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
    "url": "assets/js/9.787fbae3.js",
    "revision": "460cefd2b2626371bd6a73fe956f3631"
  },
  {
    "url": "assets/js/app.34c712ce.js",
    "revision": "7e98a766e16a992b1b6547183b8a1646"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "f3aa8fea98dc971d8cb42830c5cc50af"
  },
  {
    "url": "categories/index.html",
    "revision": "e47a957dad91aae960786ae62b98a0c0"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "1d2d13f4a2227704658f3317efb2967f"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "575cdfc2ab62d8c9192472756907c5d7"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "c885454f4aaf577349e4b85e42ab59ab"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "c0926b2c9ea3c2ad45bf4c27f02d62e9"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "47e070d3b5bbeccae874ebb66337a6b5"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "1f3bf6153760a6054bacb91ccc5629a9"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "91dd27f2b8c6bd456a10ab90fbc515ef"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "fa377488ca80591929aad2dc7a679045"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "cdc7a0b5a708c55c3b787a062aa831ce"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "c2cabefdf6d8f991706ed8e540bd783d"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "58ea5977bedce55331b39fdf2ad81d00"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "21588226e8d5416feaa56c90f7631cfc"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "728f6e9044a6b9c67a178408cf4ea47a"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "abfed24d629bbbf31cb04c98577ba7c9"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "e0784a3023639bf786a6c8be77c71457"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "d3be8ad24b566e7dbb855d792dee2158"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "363a074afab20414e6f7c80199b65bfd"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "bcab6cdb1fbaea705bbb1866b9ec3687"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "9c791bf43e36dfaf7babd45c76e5884e"
  },
  {
    "url": "docs/index.html",
    "revision": "57c34db0051728f85d0aa1a827872dad"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "921f2b8db2de30f3c9d0f929fcca7c52"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "fc07409e005b4e08122af8d526c309b1"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "3236a648932c0f4ba73f55e3475ecbbb"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "d5840bd67b7d36228d1401fd2bf3a3b6"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "3dccabf0f850af07b65529c4e273eece"
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
    "revision": "9642fedd5f0014d21c2a8850ca58f0b5"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "a713a8d5948c4cbf8fba1a765934a2fc"
  },
  {
    "url": "timeline/index.html",
    "revision": "faee04bc68a70b2be70eb90b7cdf8091"
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
