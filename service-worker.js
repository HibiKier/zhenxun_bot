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
    "revision": "3925e997f206cb101b69a170f0aec006"
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
    "url": "assets/js/12.1d4f5a30.js",
    "revision": "35958547cb888630faa7811f44453059"
  },
  {
    "url": "assets/js/13.9fea5fca.js",
    "revision": "9fc1f53b0d581f4265b9118dff7c9b73"
  },
  {
    "url": "assets/js/14.74be858b.js",
    "revision": "7ca8402e3d89599562a72e53cac7426f"
  },
  {
    "url": "assets/js/15.272bafad.js",
    "revision": "3e5528539e7bf68356d85dca8a093a80"
  },
  {
    "url": "assets/js/16.c3fbb52b.js",
    "revision": "7b5c12ba6e82e3992c57072e92bc849c"
  },
  {
    "url": "assets/js/17.d915916e.js",
    "revision": "7ecf06a4f1adc6815db2c87aa9cb5424"
  },
  {
    "url": "assets/js/18.1741e650.js",
    "revision": "451a3b9a20ef3d96f68176e6840ab662"
  },
  {
    "url": "assets/js/19.e9ce5ebd.js",
    "revision": "548eaf4595497b63d244c58d872a7d6a"
  },
  {
    "url": "assets/js/20.9e70ca5d.js",
    "revision": "a0150423d4e911d3496e88855cf9bc97"
  },
  {
    "url": "assets/js/21.e36415bc.js",
    "revision": "5de2c8c2eba6b1bb9e8baa27a8558f89"
  },
  {
    "url": "assets/js/22.a1e59189.js",
    "revision": "16c74f82f3eac2071fe3c5c589fa78c4"
  },
  {
    "url": "assets/js/23.0edbfaad.js",
    "revision": "29598638bec273dd1531c31f26186ac8"
  },
  {
    "url": "assets/js/24.f642d7aa.js",
    "revision": "6600a959933126feae51513d03eb7951"
  },
  {
    "url": "assets/js/25.32368a6b.js",
    "revision": "92b69dc0fbfb304c957a0087a5116fe1"
  },
  {
    "url": "assets/js/26.921b2b07.js",
    "revision": "701998fe03d9b828fc97cc322a7332d6"
  },
  {
    "url": "assets/js/27.a289d8fa.js",
    "revision": "8c52ac656da9526a2d9f690199c1e04e"
  },
  {
    "url": "assets/js/28.cf3126d5.js",
    "revision": "ee67c58ca61a4b95209e628a12755630"
  },
  {
    "url": "assets/js/29.29fb7c4f.js",
    "revision": "a8d0dbd73655cb149a525ff904b5d21d"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.db4ea73d.js",
    "revision": "e5d180a6f0a4d3c0b8a4b2be88e94e6e"
  },
  {
    "url": "assets/js/31.88ed55e9.js",
    "revision": "9b3ddb7b475fa256cf57c3fbf8de13c8"
  },
  {
    "url": "assets/js/32.5bb15dc1.js",
    "revision": "0f112b804b210909810a7579546bd4b7"
  },
  {
    "url": "assets/js/33.c2a9dd03.js",
    "revision": "a2b65cb7f23d6e023f23c7284eca756e"
  },
  {
    "url": "assets/js/34.cfffee58.js",
    "revision": "99edb3f0a64944e36b0d5179392b15df"
  },
  {
    "url": "assets/js/35.492b28e7.js",
    "revision": "8ccd3492f1e2b36747c0eacb7366bb12"
  },
  {
    "url": "assets/js/36.399734ab.js",
    "revision": "cb44b73b5fd027c5c9a6abe70bf51d20"
  },
  {
    "url": "assets/js/37.06c06258.js",
    "revision": "2c00837379ec96b3a7cb0011cb891eb3"
  },
  {
    "url": "assets/js/38.c2d98094.js",
    "revision": "9da99b0095ccbd88c5b8145e00da02c5"
  },
  {
    "url": "assets/js/39.d5f40241.js",
    "revision": "685309dd09034308cdd5daf21bfde12f"
  },
  {
    "url": "assets/js/4.7b2626bb.js",
    "revision": "1642b25041b4fce55d1447249497b0b6"
  },
  {
    "url": "assets/js/40.315a4e1d.js",
    "revision": "2adcc7d803c7cd89d432a037d5d7e1b9"
  },
  {
    "url": "assets/js/41.a972eee0.js",
    "revision": "e854c5ff381d28e2a38be2163d7da4bf"
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
    "url": "assets/js/9.edc7c72b.js",
    "revision": "55275f92bd9801e087a932b3259e7d8c"
  },
  {
    "url": "assets/js/app.782beecb.js",
    "revision": "a884bff644171ba9276ba7710c82a4a7"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "ed5589200680022c9b453da0b38c23df"
  },
  {
    "url": "categories/index.html",
    "revision": "1aedbd8a00516611709a7d212a664c6f"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "9386a6a00f96965208ab51a80caf435f"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "1b162ae4141f6f97e8bc85c036a2b621"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "53f0ea932ca6ba173fb41e5e8f43d675"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "8524c8f0741539c6c0ad1faf21e44720"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "f0fffd80fe71b7e25c597b01748dcdcb"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "614ee42171abc829aef6190e2abb706a"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "36c25cc5b9acc493806cfc10d890f8b3"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "659c9e0f2aad1cb53884b0e777894013"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "a976ad6e814c65e8b0d2b24926fc0e24"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "0d87b7c9c61349b2f6239364e2263f6c"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "d770b8ea12024d5385cb7319e902612a"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "25e5be5f2c12de6e124583348b16fa08"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "b4bc9644029221e97cdf425f490b85bf"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "e017a5372a4f5867b68165b281e2a08d"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "a1b66822685b0b0eed58d01ada1a1a34"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "081efeaf7468899314a04152f04c5f24"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "a1fcfde00bf78f35fdc439ac0e983432"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "e475a07637d1fc23e66eaf682d1f88ea"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "5f5b90c8720a030e295870c8e9b595b0"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "764f04cd7fbc30da0bff88ccdad0dd35"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "ecb2c3c6a1885671a4c340ad4e50e7a4"
  },
  {
    "url": "docs/index.html",
    "revision": "9f186f94f193ff4dd7da397cc46a54e1"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "47b8b9d9c1ad03b49f42e9c4cf9aab5a"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "4f1ea8829574ab0d039dc3641340e14f"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "e181ef0115e9547f57753a81e63b3b23"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "7ad39c66f4b4e2434ec386997ecd60f1"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "9e8df0c0e09f7a60c334a9766878fe63"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "70f65d0f8289dac6518bff70c0f823f6"
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
    "revision": "83bb1702f1ead6be0dbaab969b644244"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "0be2a9fff0342a0f75f806bd31f9aede"
  },
  {
    "url": "timeline/index.html",
    "revision": "acc66ac486dcffdc720b8af048286b01"
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
