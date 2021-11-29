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
    "revision": "0ec8df1f091f5b5239026dbbdf697f8b"
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
    "url": "assets/js/10.d8b4303c.js",
    "revision": "c4628c2f5e6d1b88fd0ed9449363accd"
  },
  {
    "url": "assets/js/11.1a65b199.js",
    "revision": "cbef6825ece113ad2b352dd0feae0478"
  },
  {
    "url": "assets/js/12.eb074e26.js",
    "revision": "4c61d6d62ea9312335d1fbc02c59fe62"
  },
  {
    "url": "assets/js/13.eef4163f.js",
    "revision": "a90f8e65caf8cca0e960358d6108ce80"
  },
  {
    "url": "assets/js/14.c59b271d.js",
    "revision": "e459c6f1fbbadef5d60575d87b130ddf"
  },
  {
    "url": "assets/js/15.149088ca.js",
    "revision": "38c367d6f153a7bc14e06ef1fcbc3777"
  },
  {
    "url": "assets/js/16.15a4a1c5.js",
    "revision": "4ae4297fe6581d4e318dd3e37bad6ac6"
  },
  {
    "url": "assets/js/17.f7ddb1c2.js",
    "revision": "5990d40c89f7f29c6814e073d80b39a7"
  },
  {
    "url": "assets/js/18.69f5ddba.js",
    "revision": "8a67d1255d077102f7eb264c35a3355a"
  },
  {
    "url": "assets/js/19.7c53c4ed.js",
    "revision": "b9d2241fc630f5cfcd36ab52a36ad8bc"
  },
  {
    "url": "assets/js/20.7038c5b9.js",
    "revision": "e09593a869cd9bb2f741ca8a9ec28bc3"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.4db66b99.js",
    "revision": "e8c6cd470c5baf3445268c01906266fc"
  },
  {
    "url": "assets/js/23.c43292a1.js",
    "revision": "45d6b93430abcf431a56dc7d5404fe78"
  },
  {
    "url": "assets/js/24.ebc4989c.js",
    "revision": "d4c2ef46a096e746567490327a4d0fe2"
  },
  {
    "url": "assets/js/25.d41ec7c4.js",
    "revision": "bf99a604268df1ab353c706c62fed25a"
  },
  {
    "url": "assets/js/26.84b59954.js",
    "revision": "c2ff1788e03dfcabeb7f0e8ea3d9f04b"
  },
  {
    "url": "assets/js/27.8775a86b.js",
    "revision": "e66bb9c67868857d8ebe04d5592c7e01"
  },
  {
    "url": "assets/js/28.43010a54.js",
    "revision": "0c1ae87a0d590e86898ecb040c7ff7dc"
  },
  {
    "url": "assets/js/29.263efb57.js",
    "revision": "3b4b34110c6ad0aba4372ce178c75dc7"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.1229ee54.js",
    "revision": "523cfa376f7ced39ffaaabe72b41f26a"
  },
  {
    "url": "assets/js/31.40fa9cb5.js",
    "revision": "e7c2e3f348107235b945375a6dcb426f"
  },
  {
    "url": "assets/js/32.9ab320e5.js",
    "revision": "2f1844ae79396a60b2331b3df7f84203"
  },
  {
    "url": "assets/js/33.277a9673.js",
    "revision": "a97bb673e5615aca999b47fcec1184a1"
  },
  {
    "url": "assets/js/34.585ea50c.js",
    "revision": "fb3ddbafae1d41748003209a66e7b50d"
  },
  {
    "url": "assets/js/35.5116ef9e.js",
    "revision": "9674c4eabed259cd8eeb35eed6ff5cbb"
  },
  {
    "url": "assets/js/36.eaf53f97.js",
    "revision": "2e8eb37556688b8ae51dc1bbce41cce5"
  },
  {
    "url": "assets/js/37.5a71236d.js",
    "revision": "d156d8135caf943e362274df598eb8e2"
  },
  {
    "url": "assets/js/38.33fc3f94.js",
    "revision": "1b91745ba5d0b48a18404c014aff00ef"
  },
  {
    "url": "assets/js/4.a3d0177f.js",
    "revision": "67138a1fdac208c38513b7004e1305eb"
  },
  {
    "url": "assets/js/5.37e87dee.js",
    "revision": "fd225c987340ad9662d35400b1532236"
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
    "url": "assets/js/9.b0038289.js",
    "revision": "c937fc5d6adbf8afe8d49ae82afa7c2a"
  },
  {
    "url": "assets/js/app.bc91b458.js",
    "revision": "3476f57c316b6be3ed84b77129812f66"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "77296503cf4f87e022d909cce438fdbb"
  },
  {
    "url": "categories/index.html",
    "revision": "b42d756033071394e14ee30afe585f28"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "0e8701939006cd4736e1ff2a850c1286"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "c7e010583b942c186c4e4e0783d1a320"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "c78695e9e344a4aeb06a11f1e04c027a"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "e06984ea933c34bd0eded87e210c832b"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "a548783475b9d35e2718d6c2ae1e5377"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "6e6b314c844729bcb8e33a03f6066c63"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "a7530848bcc4181e1c9f3893e4ce4fa0"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "8be7f2bdfe1d0aa29f8d06257994b56e"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "7076871da1a60d26cd1ba994c5bb7e6a"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "b357a48030ccaaf599ec8f5699162920"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "11e560db6940bab1603203c00f494f38"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "aa9575d010a5cc29014690e951b3a84f"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "f40e9c26f9808e717781dfa5eea59f9a"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "d7f8e6ef4de501e5c8413a1313461a8f"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "7588f088294a69418a14b78b3a95d277"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "48ec1ae6a7e293b8793debd74b46222c"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "00fd9b5cf11b50b5e45014c5b7a982e2"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "e9192fd5a668ebbaa432eb30b5dcd4ce"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "54e73a4b7329e641700cc6f2d5cb3d92"
  },
  {
    "url": "docs/index.html",
    "revision": "671ceb9aa07593e1d5f3e0b9ab667f53"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "e95d8ff032c7f2271cff5557e0b7e48f"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "a4927176ebd9f14a294357d7286398e7"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "19e843f6d06b988b83c801109c0c20d5"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "693f5c1cc411446e0035ec232d8e5323"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "d587eeb7130432b6fd7435e7f09c6be0"
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
    "revision": "a65b5d21a74162ffaf1860a3ccf77435"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "38ee74ded886cfbdae1a2480334b3f5f"
  },
  {
    "url": "timeline/index.html",
    "revision": "02457637b96f53e4b4f3d411713d633f"
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
