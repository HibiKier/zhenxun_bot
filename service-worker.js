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
    "revision": "64879bc53167caff9ecb87523391d030"
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
    "url": "assets/js/14.7cbdb412.js",
    "revision": "2547c48c431242ebc9c79c2ac733456c"
  },
  {
    "url": "assets/js/15.5dab83f7.js",
    "revision": "124c30bec93d1998fcc8937a783e261d"
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
    "url": "assets/js/20.eb0329c5.js",
    "revision": "3654e205266c4d9455af72e27bf29385"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.8f8ae562.js",
    "revision": "a7edde7eaaf0db060b05524c025e5721"
  },
  {
    "url": "assets/js/23.c43292a1.js",
    "revision": "45d6b93430abcf431a56dc7d5404fe78"
  },
  {
    "url": "assets/js/24.602d163f.js",
    "revision": "62b191e6e5dcad2aab74a2c9b202cc96"
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
    "url": "assets/js/29.edf2a1fa.js",
    "revision": "575afb3fbe4cd76297c0fa1f2daf1fb9"
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
    "url": "assets/js/35.10d8d38e.js",
    "revision": "33cc659bee79355a96c878b0bcc7221d"
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
    "url": "assets/js/app.c4ca61c1.js",
    "revision": "fa21395ffa5b558aa93447ad10fd2635"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "4dab77f3d77a340e877d037639bf673f"
  },
  {
    "url": "categories/index.html",
    "revision": "009649d2588748e08b1192cb1e698660"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "42ac13c89180bbd073251fca1ed46bd4"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "aa12aa43c5a711f64277cbb0267c902a"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "d15723b59d658e4d444957c275c97d6c"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "fde811cbe2f6f8d09aa7b5a3ec0c390c"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "b5383ba302423525817207ecd50d59b5"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "197852ca806dfd2635813e4b5aca4a12"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "6b911bb41fcf0bf59c5ce85c710639cb"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "dae17cbf642ef93155e93535e5120f3c"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "c1665695d414015e693e6ed9731d362c"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "22d731ef6b6eea3dbc9b9d9072d4eac1"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "ed971f88bfa2cf1043dfb3334d2cfccf"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "84eccce44a37ef1c17689c24ce923ed9"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "4a11fb87bfc03bcb88d2255fffc04acb"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "3d7fd48a19141a27176929a3986c3778"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "25dffb2e30319813663979a46815a47e"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "5757a1666419025d3b561f56d664a04b"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "939dc798fbf238fa3c81f8f3e79184a3"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "2ba9a3713a8ce48661163aa15659aa7b"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "8f9bd9d6ef021b939724ab4f6c826ca5"
  },
  {
    "url": "docs/index.html",
    "revision": "0cf6fddfc3799433c6f0acec7ae24a7a"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "e9235bf8617bfd40e390e814323d932a"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "94dbeba97f0fa2826497b789d9afd9e4"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "663b7da9191c4aa2738c4ddec9892180"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "9404231ca7e979e6f0a9ab2714756c0a"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "3df8f562cd8524e27cf2803667f75eea"
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
    "revision": "2f4b2493cf0d93151d6230b498940333"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "9d1ef0116cab0c53d530f14287972115"
  },
  {
    "url": "timeline/index.html",
    "revision": "70d6a6523e6d0b265614bea4b56b130e"
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
