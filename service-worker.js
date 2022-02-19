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
    "revision": "1177d9de402922c11a3d6360d4bb9ebe"
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
    "url": "assets/js/12.1485e48a.js",
    "revision": "e1c9a7ceccc08f990eec524cc03f1e96"
  },
  {
    "url": "assets/js/13.877e8e93.js",
    "revision": "d486cc7f4cfe6448b0ddec5b82818071"
  },
  {
    "url": "assets/js/14.cc1c845e.js",
    "revision": "2677a537de1d67272b292dd2f36c75fe"
  },
  {
    "url": "assets/js/15.78ad57c4.js",
    "revision": "287a0180a4a1a8e1d2b3bc42718bfcfb"
  },
  {
    "url": "assets/js/16.8aaf3493.js",
    "revision": "4ab55f41da21228f6db9000b8fa627e8"
  },
  {
    "url": "assets/js/17.7de12df7.js",
    "revision": "bb040ecc70187d1c0f8e554c0938f579"
  },
  {
    "url": "assets/js/18.af8c2d15.js",
    "revision": "81cf9dc2001869e31119409b2a7d9c89"
  },
  {
    "url": "assets/js/19.960144bd.js",
    "revision": "6fa08c7ad6f339c1e84b0e47597adf87"
  },
  {
    "url": "assets/js/20.81087c9e.js",
    "revision": "c6b43692610280d15d216b52cf42ca1b"
  },
  {
    "url": "assets/js/21.d36131aa.js",
    "revision": "090873c4ba404133301bc188b0927bd3"
  },
  {
    "url": "assets/js/22.37dcd142.js",
    "revision": "70e4eface7a623e4225961a1db979303"
  },
  {
    "url": "assets/js/23.0880ac66.js",
    "revision": "9ce463c796526797cbe5b7887a3f8058"
  },
  {
    "url": "assets/js/24.07a38041.js",
    "revision": "fc61898e945bc9eb8eca49cf09ecaeaa"
  },
  {
    "url": "assets/js/25.7b1d3683.js",
    "revision": "c43c7238e699d109dda9ad8074650e06"
  },
  {
    "url": "assets/js/26.f02f7550.js",
    "revision": "1f2e5da5f11ee05a6c4d8bf68ac7e364"
  },
  {
    "url": "assets/js/27.1173cdab.js",
    "revision": "b451023930e9c3452c16a7bc6ab21e4f"
  },
  {
    "url": "assets/js/28.77e39631.js",
    "revision": "22fc951180ccff3c821581ec1ea8695b"
  },
  {
    "url": "assets/js/29.a12435e5.js",
    "revision": "daaffbd51de476ea68d7c71d081a166d"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.59ae1036.js",
    "revision": "0863d3dccf8142ba505e77febb328f6e"
  },
  {
    "url": "assets/js/31.9dec6b75.js",
    "revision": "373504151c48a0f16c21b6fc2c72c447"
  },
  {
    "url": "assets/js/32.4be0a42e.js",
    "revision": "a9b606e94193f931a41fa3f5fd15f71d"
  },
  {
    "url": "assets/js/33.204eb24b.js",
    "revision": "6acc935e2f66bea65d5e8a4580fd0f87"
  },
  {
    "url": "assets/js/34.6fe811b6.js",
    "revision": "b6d42848042c51a4634b31f246ebbd03"
  },
  {
    "url": "assets/js/35.e47f0a4e.js",
    "revision": "61c2b385a018d84964e49ef288314f53"
  },
  {
    "url": "assets/js/36.8cd1b65c.js",
    "revision": "4c79557b614afd6dea7a583d5bb50569"
  },
  {
    "url": "assets/js/37.9a222991.js",
    "revision": "341a72e8e6442c8c36636889717dfe95"
  },
  {
    "url": "assets/js/38.2c33b02f.js",
    "revision": "332151aa390902a490a27771d771c50d"
  },
  {
    "url": "assets/js/39.98186875.js",
    "revision": "244536d84b4a14c7b4a2182b714ef53c"
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
    "url": "assets/js/app.51712218.js",
    "revision": "acc3b5c793b40ba1b7d480316b680f05"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "eec489882e4c2dd9f721e86b39c6d7b8"
  },
  {
    "url": "categories/index.html",
    "revision": "d08539f83ea9c907badd8d34fca6f3e7"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "7dcf3a27af4ceba173695f3673be0791"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "31dcb7386a39519983f9f48b50563118"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "b243717fb6a50217c8ca7f450ebf510e"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "c6094bace22aec2ca5815f783321b4a8"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "1b38b564d3d1f5a72c3b5ae1cdf8d5cf"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "1be34e153ade61dd753e19362d2bea4d"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "0249874fd1bc7b2062cebc1d6de82898"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "7a075fd5ab1ea36db92af873454effd8"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "1446bd824ca162ab849fb11bc9006881"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "a8118f1edd6f71c61501b87c2cc4fcd7"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "3fe85114e46c4b5ab854732dd11a4c7f"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "20d1d057ec95277061bc1c6f8c622f16"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "85dae1736f062364d4a5678df196c9ea"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "883e084b0fb6eba4c93ce740bfcc0d27"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "c3d0bd89974a6274df3e554242c5593b"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "8bd51dbd8d105f92db4353c3958efe60"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "15155025d36ce677af5570ec47510b27"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "787cff1c9826d994167cbf9c04679eac"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "07ee5225c9c3234188048851404fe4f6"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "d2f2e58708d6a9a463504e15ae8362a7"
  },
  {
    "url": "docs/index.html",
    "revision": "740d1f1ef5c44eed55bf9c3ec1a8fa4f"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "4a2102eb83f59d56aa7a9b5ded181a61"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "b9f5541915c3f4cb3c8d5b351a0ffdf8"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "6fd73ac07016f3de41b2100ebe2c3e5f"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "d5fd9ff21696dfd4ba2d5a6a8ac75755"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "7f5b8575e128c0b4e74f78ebd7e0e3eb"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "56bcfdb7e407f91e4109fe97671dbd65"
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
    "revision": "a6bedaee49e0a057947fc92420a28292"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "e01242e7a6008c53ce04b41b087a59b7"
  },
  {
    "url": "timeline/index.html",
    "revision": "85483289409858efcfb0e354ddb64de2"
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
