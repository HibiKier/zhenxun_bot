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
    "revision": "3e9ca103787da058da9641ffeaea49ad"
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
    "url": "assets/js/11.e5d78693.js",
    "revision": "a0752b097c88ce70b3a73f100e3fbda4"
  },
  {
    "url": "assets/js/12.6e193a7a.js",
    "revision": "cce0737971f3b25c68e8ca644c44c9e7"
  },
  {
    "url": "assets/js/13.3f1eb4dd.js",
    "revision": "419541c23df8d69ac12099e1e9acb719"
  },
  {
    "url": "assets/js/14.99373be3.js",
    "revision": "eedf91a79d5fbbcb4395d49b4de73107"
  },
  {
    "url": "assets/js/15.54fa7e7c.js",
    "revision": "13dcb486ab509813a0ec651ffe49bb18"
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
    "url": "assets/js/21.8b0daf11.js",
    "revision": "7090eef2064fda42df432f1e4a21fd8e"
  },
  {
    "url": "assets/js/22.32cd33d1.js",
    "revision": "c570ddb385290273a64610bd7a0d7ff5"
  },
  {
    "url": "assets/js/23.8ed56744.js",
    "revision": "6b26fc460a35950d239dc949e6188c6d"
  },
  {
    "url": "assets/js/24.9794dac5.js",
    "revision": "51f9008e2bb86675ae80b6b55295ff89"
  },
  {
    "url": "assets/js/25.d41ec7c4.js",
    "revision": "bf99a604268df1ab353c706c62fed25a"
  },
  {
    "url": "assets/js/26.ffc956c3.js",
    "revision": "1d0f6bf6d5a71b860270a27cfa4c7b5c"
  },
  {
    "url": "assets/js/27.fc81c22b.js",
    "revision": "60f223c8e54b97da55ede9130c657255"
  },
  {
    "url": "assets/js/28.4d881201.js",
    "revision": "eabefa8fb29be1e4020d2b76d7dd3ada"
  },
  {
    "url": "assets/js/29.64082d74.js",
    "revision": "fa97231a602ed77836cda0303fdab4aa"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.12255fe3.js",
    "revision": "f241975d0882788dd64dab8ce6f62873"
  },
  {
    "url": "assets/js/31.5edcd948.js",
    "revision": "ba210ab3a274c97cf0ea1393e1b0d1af"
  },
  {
    "url": "assets/js/32.2ed76f1c.js",
    "revision": "da1327b0e5f16b7e134ccf035c5226ea"
  },
  {
    "url": "assets/js/33.277a9673.js",
    "revision": "a97bb673e5615aca999b47fcec1184a1"
  },
  {
    "url": "assets/js/34.d96ee9f0.js",
    "revision": "876f43d749812667a465c9cca40c0fa4"
  },
  {
    "url": "assets/js/35.c4d808eb.js",
    "revision": "b20e7a0af0cf5cdd51798aff180e3e0c"
  },
  {
    "url": "assets/js/36.76d8e8f4.js",
    "revision": "425eebfd88a8e2417d88432bce86e96d"
  },
  {
    "url": "assets/js/37.e96041f8.js",
    "revision": "3e6165e75834a5a41ff7c57d672f4512"
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
    "url": "assets/js/app.251016dd.js",
    "revision": "fd4f65bd3230418a2db7e0772e9f6512"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "88b39861aad2d8705bc8064456f03d13"
  },
  {
    "url": "categories/index.html",
    "revision": "14c788f2cd28d48d57d715cb9ff083ba"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "650b35bca7a08f3d326bb8fae3a3ffa2"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "cac33428a9a526cfcef14103f31aae33"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "0f57de3946085b37325f84bfa9a1f0f4"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "6ae74bca5936f242a0e7f09363d3eb34"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "f9e58a6cf9750128e9397f0a47126413"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "78e783825b6b903d6c11e4ee62937892"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "97aa33bf689b565a31a6e3f64214d572"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "4e6d3a6138f2bd8e0d85a658fc29a5e5"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "4618396b527eeea55ed5423ebc729f21"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "3116b68918c073adccdddc9a9c70bd57"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "a96e1d7dcec05a7e6504f0303e39c588"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "f293cabdef01213cea894809a14f27b5"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "fea645e31963c0571562e50ea0ee201a"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "9b6480ddaa49b789773d97c04e898e41"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "2cf7752faa65df632ce528a45f4a2757"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "e3d8fa71459c08209d4aedd625f49825"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "ca3bbf7987036b010b3b59bf652e606e"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "0db960392adfc95ff1821cd88c186cd1"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "e59fcfcd6a066b4b7b1ded55f5fb6fee"
  },
  {
    "url": "docs/index.html",
    "revision": "eca65b0b9b15f201b210e85e008a3ce6"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "77b8f690893c5e722978f7ffe16b7a6b"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "35574a5c7627b838200307ad4903c100"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "a6dc28f83f8288d6f8a473c6bca124d8"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "38c9a82317ed0a3817576fddea751e17"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "731ad24db3650f9cb22d5fe20cb9f932"
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
    "revision": "95e5e8ab84ac4bd0234009de8bf06f24"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "cf988ffc589cf0767c61d0182bc6a7c4"
  },
  {
    "url": "timeline/index.html",
    "revision": "2828a0b27fd13a3c90f5c102fec581ce"
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
