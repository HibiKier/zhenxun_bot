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
    "revision": "62e671c596a802291a622ef19e263876"
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
    "url": "assets/js/11.57ced948.js",
    "revision": "ca44b101add166c6012feb8b68628c5f"
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
    "url": "assets/js/15.4e3cb01e.js",
    "revision": "20e50a705a34a55a519a0cb2ddced2fd"
  },
  {
    "url": "assets/js/16.e14d0a18.js",
    "revision": "d04ee01b86f955f3a30585a8a845219b"
  },
  {
    "url": "assets/js/17.45ea6a1d.js",
    "revision": "190fe38863648f0b4d971eaa71e96a3a"
  },
  {
    "url": "assets/js/18.dfd202de.js",
    "revision": "b142038ccc0e6b3b5631b09125477398"
  },
  {
    "url": "assets/js/19.dc0110bf.js",
    "revision": "2e2fc5388e7f10c9b41f71977abc4f0f"
  },
  {
    "url": "assets/js/20.7d00e889.js",
    "revision": "5d0e21b26a17574490b0e5e43ea0e0e0"
  },
  {
    "url": "assets/js/21.e709c1f6.js",
    "revision": "751908ef76ef4a1083069880567bbea6"
  },
  {
    "url": "assets/js/22.32cd33d1.js",
    "revision": "c570ddb385290273a64610bd7a0d7ff5"
  },
  {
    "url": "assets/js/23.c43292a1.js",
    "revision": "45d6b93430abcf431a56dc7d5404fe78"
  },
  {
    "url": "assets/js/24.71084d5f.js",
    "revision": "d4032273401ea78a68b9aab18bd7a617"
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
    "url": "assets/js/35.e938aba0.js",
    "revision": "9520d976c387e9233cba0ad665206dab"
  },
  {
    "url": "assets/js/36.69a79175.js",
    "revision": "bb984522dd73aad21a1f53364fff3adc"
  },
  {
    "url": "assets/js/37.34860e70.js",
    "revision": "9a7b2e3fff561d3f832db9e519fe75dd"
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
    "url": "assets/js/app.e25b66ee.js",
    "revision": "006c7d454d7308c4cd55660a48570a5a"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "e8f8b9477b347430a1e52eb87ab162be"
  },
  {
    "url": "categories/index.html",
    "revision": "ef8ccc79c2d9970540b299accebaa56b"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "31e5db0edc86e0db5e7ec7eeaf690493"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "e986b8280cc142c8bd43d24642e335af"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "bf016b63371d07b0a9348730643e4b29"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "de1362733b0e5f8825e59e03ea2b8702"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "e5b993f1d427750517f91824857beba7"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "bd2dea185798475b77d8c55c5de4cee0"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "1ed531d065bb8351da2ef56ebda26620"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "050bd3014d71b9a55b61026b8b7dc3d3"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "b832e581a86830f8ef4f75e9d22585fb"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "b0173701716c033e8842197ba7d5ad75"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "5a79aca83c5d385f607b7651042290ab"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "4318c329db38d13a729814c0daf2f1eb"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "cb8c0ef30b8ca5ebe46b06ca189f8e6b"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "8407de962bf43efd9a0fd9c1748c06bc"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "ad8fda4aec4e408dbe728a6fe6fa5afd"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "d091d9e7127331964ef44ca232ab0d52"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "9dc08ef9f160c4b1f311a41afcda2083"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "f4b8b069b999dbeac734193189c89799"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "c66b4744ee769fd61df7e8e9082620bb"
  },
  {
    "url": "docs/index.html",
    "revision": "9ca142c3bcaa95fadfa5f2954e490e5b"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "0798a0b1f2f114f444deb6b5572cd813"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "8212cc29d8e84967defebb4e979d8ef3"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "597367d33cbda8ebebde8db91238a3e3"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "015b659ecdbb237b288cddaa34416cc9"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "178e0fcaa911c6fc51a54c7ed05aee64"
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
    "revision": "42d647ffc3be5b4c05298734a1472fa9"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "a043d407f7dcb900640ff5da3f819f11"
  },
  {
    "url": "timeline/index.html",
    "revision": "8bdfb896af6c4dbd6fa1624f1162f031"
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
