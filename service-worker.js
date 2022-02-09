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
    "revision": "c04ca48a02911241c674ebfa4c761f1d"
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
    "url": "assets/js/11.441290f5.js",
    "revision": "17a268fe8584f8d222a3266f9a0ccf26"
  },
  {
    "url": "assets/js/12.4b19db38.js",
    "revision": "8b0ee97155ce1c10e0507cbc14545693"
  },
  {
    "url": "assets/js/13.3f1eb4dd.js",
    "revision": "419541c23df8d69ac12099e1e9acb719"
  },
  {
    "url": "assets/js/14.afd88693.js",
    "revision": "3f1fd5f3ddab8acb24d9ed57ef1041a6"
  },
  {
    "url": "assets/js/15.272bafad.js",
    "revision": "3e5528539e7bf68356d85dca8a093a80"
  },
  {
    "url": "assets/js/16.8ec651f4.js",
    "revision": "99ce1ee4e87e709df84f2a06058ab701"
  },
  {
    "url": "assets/js/17.b566ef83.js",
    "revision": "4037aa2af87eb6d7c2c04cb3aacf3bbf"
  },
  {
    "url": "assets/js/18.d5efd5a1.js",
    "revision": "ad6da1daf1d3d7f8f7c1b14792c66cb6"
  },
  {
    "url": "assets/js/19.9d667d37.js",
    "revision": "0fc9fc2c724e3d022a9d5f39abc5c9e4"
  },
  {
    "url": "assets/js/20.201e4a0f.js",
    "revision": "b6fc875c595f74aa07dffcfbc71406f5"
  },
  {
    "url": "assets/js/21.c58e1f63.js",
    "revision": "1430bdcfb03e25132f29f591399f8a78"
  },
  {
    "url": "assets/js/22.4a7bdc03.js",
    "revision": "0a43f4661862caa492dcd52f08cd3880"
  },
  {
    "url": "assets/js/23.53fcd913.js",
    "revision": "767d616514c0c2ef52ce48fe7fc32dde"
  },
  {
    "url": "assets/js/24.c6d9864f.js",
    "revision": "46d5b5038cf44e2aa36d6efed8b59c9f"
  },
  {
    "url": "assets/js/25.6c516c19.js",
    "revision": "115e89e37e960bb15722a11d59011fb0"
  },
  {
    "url": "assets/js/26.e60c8fe0.js",
    "revision": "1831b96286235aeafe77b28566f416fe"
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
    "url": "assets/js/29.e45e5203.js",
    "revision": "183f43072b70169cc9cc9ce609cd92d7"
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
    "url": "assets/js/31.d778aae3.js",
    "revision": "ce556659dfb2c17353d370ab4c83e0c5"
  },
  {
    "url": "assets/js/32.3b5db4d4.js",
    "revision": "276ed257f11970e3b72e917e07a16716"
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
    "url": "assets/js/35.87722891.js",
    "revision": "d6dc18bd6df249097a1badecc99ee45d"
  },
  {
    "url": "assets/js/36.8cd1b65c.js",
    "revision": "4c79557b614afd6dea7a583d5bb50569"
  },
  {
    "url": "assets/js/37.77ed2a6c.js",
    "revision": "a3ec4aa26ec807318d8df0b7621f56a0"
  },
  {
    "url": "assets/js/38.6de2d7a0.js",
    "revision": "ef7a98a113d14c81436c765085d0894e"
  },
  {
    "url": "assets/js/39.d4f57553.js",
    "revision": "0729561204e04fe58800d25fca062ff9"
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
    "url": "assets/js/app.8c136bb7.js",
    "revision": "bc6a9c6b1d5b81434367932d1f98142d"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "c743524123ab98a7826bdf6f83242b29"
  },
  {
    "url": "categories/index.html",
    "revision": "abb2007a63345f4eeab65d734707f196"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "788fa352f279761f22fe53ebaf0ab395"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "539dc8c6676b61e061cc568e0c6d0f08"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "f7a97ff3a3f90c483a769fbb2cb6150c"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "bcb7519fd0d072975964b9b9e0dda171"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "e8ab3bc572cfc377ed574c3a41a2c092"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "a13e1cd61450f93ec4ff5d9c6a546276"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "a1826d1d33a4d72378c1370b03216948"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "80e52249c1fded034ebc2a796a609c39"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "2014f0ab3d351b9afa30ee50305c2cc9"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "10ddf8fe6e4481f0b1f9adcc83c047b2"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "0d56540b43576637024f2eb5a2f9e9b6"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "cf4764c18b18b0c8a18f5d8a1203fc94"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "c6aafc97248c7f150cf0eddc10f1576a"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "c50ef05734e3398dc40fa6426c61aa13"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "ef25e40a74a1abd332b5bd919acd92d6"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "9610a345b858914558e31292259bff66"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "e00e339f7b3d01b61705b3e6abf5dad2"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "ba704656c205941c71cac980e2536f16"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "2c283d2ef3ffb3abb9b899f7ed533fcc"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "b486d4dda1a7862b758b4898dc83bb2d"
  },
  {
    "url": "docs/index.html",
    "revision": "024a7617eb73e8f4e5963d55c4ac4b5d"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "aae09949d330af82fae483207bc71ac4"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "c3533493e573c63f1fef90bc4c1424e8"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "80684bb106d2ac6e85defcc83d6c5562"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "0bb7ad3e9a1e411b3a1290fecc68cea4"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "e374ab195901ae40683790d6589205c2"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "a57e3b26a3cc9229091bb46978a54457"
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
    "revision": "726d122459e4aa5e76d191b035e97873"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "6bc0c51028a45711d355b157cd2e98ea"
  },
  {
    "url": "timeline/index.html",
    "revision": "d32d3e95dee14b5e5b51ee1f034b4111"
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
