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
    "revision": "7d61b1ae9ad854c3f3c2ecb0992424a3"
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
    "url": "assets/js/23.a95af780.js",
    "revision": "72257fb5f91c9998f397c7ced73aa619"
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
    "url": "assets/js/36.90fbed32.js",
    "revision": "c830e57601992e1ec599525ffe13f82a"
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
    "url": "assets/js/app.4998b79d.js",
    "revision": "327a77fad586f4ca411414d70831a698"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "783469c4e7835f2e257877160bd1b3b1"
  },
  {
    "url": "categories/index.html",
    "revision": "fb70eac1e56d33563901a6a5a04bc452"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "e4580f0843aef9c3ca534ec6aae0bccc"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "ab4e39748b8c7555fc954914fa47a749"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "691cfc87c8031d8a499ae86494208a43"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "fb9c3119b473bfce667a6925f55a584b"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "284dfe8de30554c49fa312cc85b542b9"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "df47854be8468d0dd2bc1aa35551f2d4"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "e87a313a75137f2e0490f2c1ebfe3552"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "11c51a31fe3ded7d2a564665677e9989"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "440a81e4e0609e76416cd8546de2a7ce"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "49c73a5f0be32f446d37fa11faefc807"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "868c6a0a322d70b15eeaf68c8189ee0e"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "0ce79ec4065f28492b28f5c8bb4aa059"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "bc51852d03d111c5b4136ced4abc9d12"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "f100587a6f840f9a85dd853d7e2d3a5a"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "1454e3e4fb63b7be867a5a6d72a0e478"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "41d1ca85f15b6138ee729e059da05951"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "dc8a4509f093b608bb81ba525c2691a3"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "07cfce51738bb61564d2cc7e98293e44"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "0855efe00078501763638774fe8ed320"
  },
  {
    "url": "docs/index.html",
    "revision": "78499d966bd54db656568a4834850a1f"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "d180f22bd547d7fa3b48c726c9373560"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "be16bac7dce653f7ec69c96d958269f3"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "263bace7a23970be0f2069bde8ef3680"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "8198e2f1b1eec6b269c50df5e0c3be38"
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
    "revision": "65bbb88aceb6271c2f1d996627c82319"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "b0c3dc99dbc7b39d6887413543e73188"
  },
  {
    "url": "timeline/index.html",
    "revision": "2f5373599a5e483ef07b21f8058914e7"
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
