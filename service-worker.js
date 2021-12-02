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
    "revision": "cced489e64fde2dc12faa79fdbe95fa6"
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
    "url": "assets/js/18.dfd202de.js",
    "revision": "b142038ccc0e6b3b5631b09125477398"
  },
  {
    "url": "assets/js/19.afef6f5e.js",
    "revision": "c286dfc9533fd5d2c9bd1c7d2a7f840a"
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
    "url": "assets/js/24.71084d5f.js",
    "revision": "d4032273401ea78a68b9aab18bd7a617"
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
    "url": "assets/js/27.75ca22f2.js",
    "revision": "bc8c2e1a39f6b51ebd40f2490881959c"
  },
  {
    "url": "assets/js/28.aac9ab09.js",
    "revision": "9f66a9292fafaf1577a772d083023e6a"
  },
  {
    "url": "assets/js/29.d4cc087e.js",
    "revision": "2adb75641a9013746833dd5704fcd4dd"
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
    "url": "assets/js/31.40fa9cb5.js",
    "revision": "e7c2e3f348107235b945375a6dcb426f"
  },
  {
    "url": "assets/js/32.6c00e06c.js",
    "revision": "a98e65c29b213da1bace27ab9f83cb0a"
  },
  {
    "url": "assets/js/33.44066740.js",
    "revision": "648458ad82363a2b432464a02fa5e24b"
  },
  {
    "url": "assets/js/34.772ee8b9.js",
    "revision": "271009177296535e25c27004e583ffaa"
  },
  {
    "url": "assets/js/35.8a33351d.js",
    "revision": "840ea2af9f9011caf9203cd40378f30a"
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
    "url": "assets/js/app.46a13ae0.js",
    "revision": "7fdfff00848cf3abaa4328414d9d74e4"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "eb08d558e74104d80aad17b85953fc04"
  },
  {
    "url": "categories/index.html",
    "revision": "ac81acb82e06f055d60b9f90e25291bd"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "aee500be356c5ad98022a8a2cdaf1445"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "e1ac39f1986f07ade6bcd202bcde4ca9"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "1baad44f3137d7f654b8c78e84d1c877"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "81d8e8083e973f17668506e68c9f4cc2"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "0555b3bf2e14e08f8ab5e48e5c2f312d"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "ceec548224868269ef37a5855f2d49e2"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "a72c49d229b990be3597d24f4a94ec76"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "f29138672d173dd9524bafae87c59c7b"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "c254a1410fa4b0e463e3b1030cc1d1c3"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "067d3ed51dc86a03c28bb94fbfb71d3a"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "0180cc2059ee29ab998b41a825d8b79e"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "bd10e5fbc370e9518edc039d7ee1b81d"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "5d169bb1f37afc6a07d6d9b72d9eb0b8"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "007a5a75c3853f37f42dc567ead80d42"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "c965e9e6ce936326174a04e0a48a2009"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "2cc67f358cadc95a4600c24553d656cb"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "ee23bb9a87c7dfc12bb9b34848c0f395"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "74ccde43767cc89a86f3ce8938aada36"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "32c79e0cd606d63c831c3e6d0d2ad63c"
  },
  {
    "url": "docs/index.html",
    "revision": "b53e5a8dfd92c7e4730ff124c1b7ccaf"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "088809761f0b31b359f7bd96d6b975f9"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "a2003eb54c51964a3d0fe2d3f5d5406a"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "03fda952ec427a707f6c5e1053992f38"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "e8a17fa5465faef75a3435b4fcd06b46"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "8c5dbb7efd4a1c4deab303f0d7a0a5a7"
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
    "revision": "cc2d0b67774389595e6b8e0f5299af26"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "2c740609697dde0f6764842212244d0d"
  },
  {
    "url": "timeline/index.html",
    "revision": "877c5631dee6b079b1d112ef1a879c21"
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
