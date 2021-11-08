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
    "revision": "7e5b9cc57d742a922b3ad73ca8cfbf90"
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
    "url": "assets/js/11.57ced948.js",
    "revision": "ca44b101add166c6012feb8b68628c5f"
  },
  {
    "url": "assets/js/12.fdaa7ffc.js",
    "revision": "1a47e6d96c5001196b94092a3c508637"
  },
  {
    "url": "assets/js/13.12022e1e.js",
    "revision": "f54f8760a522b111dae7d5ecacb0b7ab"
  },
  {
    "url": "assets/js/14.0bf8bf0a.js",
    "revision": "a345f2109901e8ca1037fdbe0fda2c4b"
  },
  {
    "url": "assets/js/15.aba856ed.js",
    "revision": "f33bdc3a92fedc3aee980d1f777b9774"
  },
  {
    "url": "assets/js/16.ae4d64e1.js",
    "revision": "06624ec7c3afc0211bb4f639d10b09e2"
  },
  {
    "url": "assets/js/17.27df5e56.js",
    "revision": "51a613012bf4ab90e4ac8342dcc78c83"
  },
  {
    "url": "assets/js/18.0c85f582.js",
    "revision": "343e7511f457da50fae198ab30917938"
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
    "url": "assets/js/22.66fc9431.js",
    "revision": "fdd49311b19c269c8049bcb19634b86e"
  },
  {
    "url": "assets/js/23.9a927d93.js",
    "revision": "b57776229e15ca4ee31e035baf1c0784"
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
    "url": "assets/js/26.243e652a.js",
    "revision": "76fb3c55bd2a556cc6612f086ab8ae92"
  },
  {
    "url": "assets/js/27.707bbdc7.js",
    "revision": "38839f9dd011b27900aff285c639e152"
  },
  {
    "url": "assets/js/28.3a93345f.js",
    "revision": "ff78a67937da7f4a7c153985ad22e22c"
  },
  {
    "url": "assets/js/29.ee289f0e.js",
    "revision": "96c068b7c256c8c9546bc2ba2ea0c8e9"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.89312344.js",
    "revision": "f4bc0d70c830c3b53e6aff4e2d530dd2"
  },
  {
    "url": "assets/js/31.1e20744c.js",
    "revision": "f985fb98342b077326fac91358a8d518"
  },
  {
    "url": "assets/js/32.30aebf02.js",
    "revision": "04e45fb88f1b0805f3beb73109f752b7"
  },
  {
    "url": "assets/js/33.d9ac2be1.js",
    "revision": "ffb266df08968070580f8bdc6f525479"
  },
  {
    "url": "assets/js/34.60ed9ee0.js",
    "revision": "b74f5f053df7aaad01bd31a1c839296f"
  },
  {
    "url": "assets/js/35.e938aba0.js",
    "revision": "9520d976c387e9233cba0ad665206dab"
  },
  {
    "url": "assets/js/36.cbe79dba.js",
    "revision": "3b892926c9e8ff795e15db84f38a2a61"
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
    "url": "assets/js/app.80ead4cf.js",
    "revision": "eb0955cffe3e6056c1b489a157fe1450"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "7816d84c197c6f46cb9ad42cd92934dc"
  },
  {
    "url": "categories/index.html",
    "revision": "d755e13d1082ccaa9b076b228068bb32"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "91472d933579695bb84fda25112d70c5"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "fb299295c44049d01a2bc8f5407c5b59"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "86cf0bc81d67ac5f0228d970274a279a"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "322d3c5cc75197599c622aa8204ac55d"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "1dadbc6ae03a77d3207859ebab65f6a3"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "e8b49a6c1449e40b72987ff75193e6dd"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "0e6944069607f028185a7d4eb70e5320"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "72d3cb7851d8a0cdaef73670fc4ce87d"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "ef06fcb6b9ee4cb7070c08c8a4126e0e"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "c70ca867b3779a5d4da41c260bc7ada8"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "75706bc9a7f4987b20086eaa9cdc618a"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "46944b18b129bfa755635ba02bf05217"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "4e8c1a875ab5627c5cfc299b969e15d4"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "0d06bc18d6fd26975a3a0ef03e1b4ec7"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "d3adcd53a25bcf0d0eb8d61a95b6ad68"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "170adbcba047a80ddc20abb20f887f30"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "fbecab7a9465f8572784ca833399dbc9"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "af376ba7466691415ee151d748d365dc"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "d4ec28260904cf91b3e76e06bd9be86d"
  },
  {
    "url": "docs/index.html",
    "revision": "7918c211556739ed22926881487306db"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "fe88d550947adaabd02b7d4fb0d69020"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "7d94d8d1084efd9ac50ddfb97d1c14b1"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "ef65b40300d3e5c946638e61f435feb8"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "bde48256c36a724ed95ce987cd78a2f1"
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
    "revision": "b72bf04b39010b9ebf11fa40962af872"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "cb9417c30dc4b854ed751ff6e2027823"
  },
  {
    "url": "timeline/index.html",
    "revision": "5efec0f95d6a36616f804ffc9021e0ee"
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
