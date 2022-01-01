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
    "revision": "5835e0e1efa00a182336a1f7cf174984"
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
    "url": "assets/js/12.8da8474f.js",
    "revision": "5f9ed69a11eef487b0cfdc096f62e44f"
  },
  {
    "url": "assets/js/13.877e8e93.js",
    "revision": "d486cc7f4cfe6448b0ddec5b82818071"
  },
  {
    "url": "assets/js/14.094db6fb.js",
    "revision": "f61423c71a996ac861f873c89b9fb65d"
  },
  {
    "url": "assets/js/15.4a007373.js",
    "revision": "ac0e564fc98f09b834a21f008d69f638"
  },
  {
    "url": "assets/js/16.3402ec8d.js",
    "revision": "43369626d4cd473d3f91450b87759763"
  },
  {
    "url": "assets/js/17.05e64228.js",
    "revision": "a40574b0def17b25571418a564207b2f"
  },
  {
    "url": "assets/js/18.a8ee201b.js",
    "revision": "f6065513ebe5f22c2136c6aa4c7ec60c"
  },
  {
    "url": "assets/js/19.232ed360.js",
    "revision": "8520e74b558ba2e92ebb6661282d4d5e"
  },
  {
    "url": "assets/js/20.1e9268e8.js",
    "revision": "fac052a3f5d8f9ee988b876b0032cd66"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.4ce93f5a.js",
    "revision": "31d9bb209ac9aa54c4a52637dc901db7"
  },
  {
    "url": "assets/js/23.0b61f3ba.js",
    "revision": "27151f11865633d48cc02e681919ca0f"
  },
  {
    "url": "assets/js/24.cfdd70a4.js",
    "revision": "87c4b13c18175c50aedeba94ea438fb3"
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
    "url": "assets/js/27.49a1edaa.js",
    "revision": "934d8054ad8dde95f58a9f8fb388c217"
  },
  {
    "url": "assets/js/28.06aa5907.js",
    "revision": "519cb1053bf3dc9fd4629ed0d30f73a8"
  },
  {
    "url": "assets/js/29.58a7d2ed.js",
    "revision": "48193945bc355a3d1e65c2b0ed8f96b8"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.5f771446.js",
    "revision": "26108ba76d2b11488e345a8d0b2b6601"
  },
  {
    "url": "assets/js/31.15720522.js",
    "revision": "2df5b8e57f9cb587b4e1ab68174fc373"
  },
  {
    "url": "assets/js/32.a669934a.js",
    "revision": "e4b3747976a822c4b9fdf2bc2388e3f5"
  },
  {
    "url": "assets/js/33.9852f9b4.js",
    "revision": "e8da924983a9884d292431def0a76708"
  },
  {
    "url": "assets/js/34.c65848b7.js",
    "revision": "d43ff295f4822459bfa95953cdabb0c2"
  },
  {
    "url": "assets/js/35.8c661e80.js",
    "revision": "50a8e4d6b849bfe0b3c3dc94dae10b2d"
  },
  {
    "url": "assets/js/36.9ff88549.js",
    "revision": "2aea1b575761bd0d80a10c14a2b63156"
  },
  {
    "url": "assets/js/37.6d48c887.js",
    "revision": "245d52ce57750ae5d63b1ad97724318c"
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
    "url": "assets/js/app.33e8bb80.js",
    "revision": "0a6930c36a002e368bdcf5e08741bd3b"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "ecb94a98b14324449c1f414782f4a1d3"
  },
  {
    "url": "categories/index.html",
    "revision": "68c720b9a3a7e5d9d7a51b0a7711d18a"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "fca0fde6aa5781bf65ddf879af2efd56"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "0e3df4f3f84ba766db27853bc449bae8"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "0632409ff8bc6652f45e0c4a55b4f932"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "eaf508fde3248ff0dc9db4c6151447c6"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "7bfa78c8336ebe77ee068470a1b22dc1"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "106b51b5b1fe31d4915c90dc392f2a66"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "66747ccfff639011dedc50066cc19ad6"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "d90bf8a1fae812609e23a9a7e4a3dbbf"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "5ff44ccd48c94078296bcab105cfe634"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "cc054bbef09d3218d182655b2788476b"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "bbbdaab6ec8eca184ba50757131c468b"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "46b9bdffae4c431c02a51850713eb2b5"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "380975a4ae2a9ab9cc7b4a7fa3e6fbbe"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "064a0fd586e0517e8afc1f9825f1a338"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "5f6057f5933fccb015732679b65374a3"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "dfe1c1220604dde7bb1a56a2545eddfd"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "d825affc6a2c2da8775d77d8dfa04442"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "8d7a82dbe3b1319ba2cfff87fca10698"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "5b0d9acd07b63868c517cd6f9ff03a92"
  },
  {
    "url": "docs/index.html",
    "revision": "a153cf685a4031ea685b30c073a43439"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "a417e01ecdd8bea207845eaa5bf58a24"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "2797c6f03d9e8b6b19a07fc55497c324"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "1d7675abebebefc476962354aa67766e"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "ffd41453c118d343716f351e2ed07701"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "89788c54cc45a6a4937e9235e727f00c"
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
    "revision": "459fcf8abf971b3631d0db5fadc59aec"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "a75345a8bae9de26f9e89e6351e0fbc0"
  },
  {
    "url": "timeline/index.html",
    "revision": "30ba9476fa76d28281f6aad9e3ba7448"
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
