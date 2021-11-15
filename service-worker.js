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
    "revision": "afeb427ced5ed764072808c809d2d9aa"
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
    "url": "assets/js/14.b90ba65e.js",
    "revision": "c44af9326072f791eb015467a7444625"
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
    "url": "assets/js/22.e66e5bef.js",
    "revision": "089354e24d62c6ba4beb5992afc024b8"
  },
  {
    "url": "assets/js/23.f231de6b.js",
    "revision": "0a71427b1bf51fd32be77e9866c99890"
  },
  {
    "url": "assets/js/24.93f40989.js",
    "revision": "9059d83b5bf7fd0c457b2feddc45da73"
  },
  {
    "url": "assets/js/25.705595cd.js",
    "revision": "6a48596fb9ad3a46d146b0f370b34868"
  },
  {
    "url": "assets/js/26.c7988754.js",
    "revision": "b136b53195ee0435d971dba888c8e26f"
  },
  {
    "url": "assets/js/27.d52d74c5.js",
    "revision": "114d17dbef2aecd3762079d54153e823"
  },
  {
    "url": "assets/js/28.d2a2b076.js",
    "revision": "e1824ab509a9d2892ad4a789f0321e16"
  },
  {
    "url": "assets/js/29.c9aca793.js",
    "revision": "b975561ca45e7793b576bb3efae0054e"
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
    "url": "assets/js/31.48dd0e07.js",
    "revision": "2f6d25295470e49f399573347aa7cf09"
  },
  {
    "url": "assets/js/32.9a54adf0.js",
    "revision": "b3e666696307043da930f76770040864"
  },
  {
    "url": "assets/js/33.b40d71e7.js",
    "revision": "44340dd51f386a7d3cf5536f82c918aa"
  },
  {
    "url": "assets/js/34.9fe3f150.js",
    "revision": "ebeb7649c50a66ef05eaad63e4823b52"
  },
  {
    "url": "assets/js/35.eba0ebe1.js",
    "revision": "a071bf55be84e7813436ea664e9357bd"
  },
  {
    "url": "assets/js/36.fac38afb.js",
    "revision": "eedebf40282eb925c8bbbf7e4e0748c0"
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
    "url": "assets/js/app.44def721.js",
    "revision": "b54180ef0d094ecb9ec1fb61b100bedd"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "0ea7bbca3b0a69f285c0e29abb3b92ae"
  },
  {
    "url": "categories/index.html",
    "revision": "857475dae1278fd6639c2aa1bebeaa65"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "42d42d3e9aff87dcfc048df4b219c7ca"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "cd2a589195a13796190bb34764eeace9"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "18e52e580baa3b2e88884dd98c4e42be"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "a9207bd715084ef80d257931e609ac38"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "624415f4fb6df69ff69d2542a09d57ea"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "6a257ddc72138a7a19e64c491ee58550"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "998929c013368c728d21e6ccc7db49fb"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "ba31737a4d8d0145345c20694bb6d9e1"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "d94cfef0bf20916f0391d4d9548c26e8"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "cd19e38d3117e16bdcb268c200c4bd88"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "81b6978a4d1e662816b38f8d3568c02e"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "ed9255c91f919a1244a7f1b0bed456d6"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "291d85a06a5e684843fc3b30a0f718b4"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "f6f9243fe4eb66eb7ee9115287f16adc"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "5182f33bbc7e0a0f81e506323ed96f0e"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "e9fa3a72f0ecc19e65834beb6e1a43a9"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "5a013ed1c30e4fb2b3e34093fa322b1b"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "d0f0be3068abe1433a48468da0ff6114"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "f46283ec8994f5e6ffa4839518355a7e"
  },
  {
    "url": "docs/index.html",
    "revision": "67c06563a1aaf44b880f13924d87b74d"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "8777b426f6678987963cc8eb4fd700e2"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "52379ba1811e7b4ea6cf2d9e518b2fd7"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "32b212afd71e271fb7a558f6b9b30996"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "630dbd5a06c2c53ada8f5f0ff167a6c7"
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
    "revision": "10ed53c88ce0f13d008d5148a98448b5"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "711294284a57a5c03dd50adcf0aaa02e"
  },
  {
    "url": "timeline/index.html",
    "revision": "1cdd7d9cb32c1b452178ea5bcc26c202"
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
