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
    "revision": "8846a0d920bdcb447124baa85852a4b4"
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
    "url": "assets/js/12.2b14619e.js",
    "revision": "8e558af896a40de63b4ec32c465fee70"
  },
  {
    "url": "assets/js/13.877e8e93.js",
    "revision": "d486cc7f4cfe6448b0ddec5b82818071"
  },
  {
    "url": "assets/js/14.788f9da5.js",
    "revision": "2240d51c4e3d8fd87c9f397146884e2e"
  },
  {
    "url": "assets/js/15.bd251bc2.js",
    "revision": "b4ad53e5651f0089adb106cb1f9ae830"
  },
  {
    "url": "assets/js/16.8659b101.js",
    "revision": "e36abdf675c0755c1f8c43b15087dea3"
  },
  {
    "url": "assets/js/17.7336b5f8.js",
    "revision": "81cc891a707539f1d853e3d31ecc5caa"
  },
  {
    "url": "assets/js/18.7aec149d.js",
    "revision": "3fa6585608ac81d0ebbe9b0edfcadd9a"
  },
  {
    "url": "assets/js/19.960144bd.js",
    "revision": "6fa08c7ad6f339c1e84b0e47597adf87"
  },
  {
    "url": "assets/js/20.c0f4feef.js",
    "revision": "0650a122aa8341fbc88595a27cddabd6"
  },
  {
    "url": "assets/js/21.a66520ab.js",
    "revision": "efb7cf3bef19d4ce3e9a8440c3b4f31a"
  },
  {
    "url": "assets/js/22.2f8ab0b5.js",
    "revision": "adccc0023babe51cf7ef34825bf1e485"
  },
  {
    "url": "assets/js/23.9dd72b3a.js",
    "revision": "34a42e70822865999f2e0e7176d351ea"
  },
  {
    "url": "assets/js/24.31630ca5.js",
    "revision": "a43e2e97061e6c0771a5b17c9113091d"
  },
  {
    "url": "assets/js/25.bc4970a0.js",
    "revision": "ce060b69aadc523118846e276ea57670"
  },
  {
    "url": "assets/js/26.f02f7550.js",
    "revision": "1f2e5da5f11ee05a6c4d8bf68ac7e364"
  },
  {
    "url": "assets/js/27.45ee1eac.js",
    "revision": "45201ebc385177becb7f93a672595eff"
  },
  {
    "url": "assets/js/28.77e39631.js",
    "revision": "22fc951180ccff3c821581ec1ea8695b"
  },
  {
    "url": "assets/js/29.4062a7a3.js",
    "revision": "5a64375950ca074c8a66f75562e447a4"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.2f3e8305.js",
    "revision": "bbd9b87e755af728db352ba648213ec3"
  },
  {
    "url": "assets/js/31.7bb19d80.js",
    "revision": "1ab8850737e768adcc47400d26842cf8"
  },
  {
    "url": "assets/js/32.aec975c6.js",
    "revision": "4b2752e39dac17dfc948d5ab8a8ed873"
  },
  {
    "url": "assets/js/33.f820c9b2.js",
    "revision": "1284b68001c6388c8ce983f4145f4dea"
  },
  {
    "url": "assets/js/34.3aafaab7.js",
    "revision": "6dc4908e76163a5866d6d685126adb04"
  },
  {
    "url": "assets/js/35.62288494.js",
    "revision": "45f159f1a8fdcf3203a1aa91e5a678de"
  },
  {
    "url": "assets/js/36.6bfa2e27.js",
    "revision": "f63b3dfd6b7a5dff731a39a7b7b08e90"
  },
  {
    "url": "assets/js/37.e160a38c.js",
    "revision": "e79fe736dc54ed56e256bc4d1079a000"
  },
  {
    "url": "assets/js/38.05787def.js",
    "revision": "602a8b34a0c7ec1b727763864275e2e5"
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
    "url": "assets/js/app.a0e23d06.js",
    "revision": "5ee877ddea781195f9386ed2115981dd"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "31b1450c18d144cb9437ff393cc1f0c9"
  },
  {
    "url": "categories/index.html",
    "revision": "0a3af398c210dbfbc880c685b88d2746"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "a8c8b5f354246f6fe84f9c6e00d892da"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "92a4c425556eb9ef582cf0829d71cefc"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "83c4b41ccc63226b19726bb5382d70e1"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "80646308fa0756d787782cf5e626bdd8"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "5262f80f09cedb459a6769dfab8e7d76"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "0cc8e3c486cf709cca042bd961d23f44"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "fc28b0de71e5d50d647025b323ff3416"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "537cdd585f6d93835cab021f64bc7824"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "c83176440c388677b41d4e8b116b3ace"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "8c59cb2ecee7d004b842c9406b0b7e22"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "e3f4384cd117008278fc1f5d7b7b8d33"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "207200c8adc8f8039244034de708d135"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "08b9d91d6b4066ae78a24227ddb60b78"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "f767d2e37e99d1a512c983b4d4ccbb1a"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "8e4e7d55d97531217e5b33fdc859f5e7"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "c5bd34d9c976cf502c8e72b9a2ec522e"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "470bf6872ab01833573a6d80ebe9c2a1"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "de4d853c8bcace9fc5573815c95a3e24"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "b97d4b8516ba52611210504dbedfd637"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "53409809107e1a67e8059f19b245c1bc"
  },
  {
    "url": "docs/index.html",
    "revision": "6b6bbd201ef90c08189a8b99026c1bc9"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "187d5386d71efe3b1283cd21d9f90b86"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "c0c52b07acc29669cc8faf335e01d74e"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "dbe2a6ee61d82347ec54f0c31853baa1"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "09cf7ca39b99f2fcf6c1a6c0396cef76"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "8feec15f8a44141dc3ca61c3c79c5850"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "b226203c48665871a91ed82d8d5762b6"
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
    "revision": "7fa663f1f9b945286642d4a27c79fbb5"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "6c1ba56644f4522f606487946a0cbcd3"
  },
  {
    "url": "timeline/index.html",
    "revision": "780041c79b0417d273ec04a29f8c0742"
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
