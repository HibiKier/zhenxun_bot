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
    "revision": "68423cae62fc3b46a022ede952a318ce"
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
    "url": "assets/js/12.2bd4144d.js",
    "revision": "4503f488aa603ad0c8b38df9843531a6"
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
    "url": "assets/js/15.4733fe64.js",
    "revision": "08c6bf01f8c4794d050f947f15e82014"
  },
  {
    "url": "assets/js/16.7e579d0f.js",
    "revision": "9d7aaa60d9ee51752c2208b59dc9d3b1"
  },
  {
    "url": "assets/js/17.149ba7d3.js",
    "revision": "28ddc6ac8489bc834098f842383d223a"
  },
  {
    "url": "assets/js/18.de9c1a67.js",
    "revision": "8bb8192f9b63f8ac363326e9eab30861"
  },
  {
    "url": "assets/js/19.232be453.js",
    "revision": "614546b52fddf5731001be1840ed0150"
  },
  {
    "url": "assets/js/20.2d40dd43.js",
    "revision": "0c63c23bc58914d4ec7058a56d209164"
  },
  {
    "url": "assets/js/21.7c51850f.js",
    "revision": "2736318e5085757f96ce1f892c6ec136"
  },
  {
    "url": "assets/js/22.08cbd649.js",
    "revision": "ecb3fdab7314f7de65f08253d70b5f7c"
  },
  {
    "url": "assets/js/23.23a1c8a9.js",
    "revision": "f3361ac7ebd1c1264776a1695d7b8e52"
  },
  {
    "url": "assets/js/24.640de0a4.js",
    "revision": "ddf049495ecae70791e7ae5bf354b730"
  },
  {
    "url": "assets/js/25.a90af5ef.js",
    "revision": "0d9d3351345b5d11fd5a5b150184c035"
  },
  {
    "url": "assets/js/26.4ef993b6.js",
    "revision": "694fc0d5feed35c440c37fa9791348cc"
  },
  {
    "url": "assets/js/27.9af4959f.js",
    "revision": "55075857a69487f3c5fdc383e8bebf05"
  },
  {
    "url": "assets/js/28.56799a3f.js",
    "revision": "06eae8b1a1f1ee6d63ebe74f04219e90"
  },
  {
    "url": "assets/js/29.09fb4193.js",
    "revision": "5b8b82336c3df53e87e8e537478f342b"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.3c09b601.js",
    "revision": "aa3fafc5932d2fd06c658f60cd56e15d"
  },
  {
    "url": "assets/js/31.b7b0d2d6.js",
    "revision": "b46616091db2d7d52153ed9e55a7e112"
  },
  {
    "url": "assets/js/32.5889122d.js",
    "revision": "1a93b4a50684f74ac78e4be95d90f0e7"
  },
  {
    "url": "assets/js/33.64f147d4.js",
    "revision": "02661d8451dc715306a70eb508aa9172"
  },
  {
    "url": "assets/js/34.aee52930.js",
    "revision": "429f465683b1a0428c5378a70e47a28f"
  },
  {
    "url": "assets/js/35.238f602e.js",
    "revision": "7d9cd12f5e8addd04f730efff1951afb"
  },
  {
    "url": "assets/js/36.6738bce1.js",
    "revision": "b9ea787a6812c8868c39a1fc9e27fbc2"
  },
  {
    "url": "assets/js/37.6cc3a7ce.js",
    "revision": "04bbf7cea50d6575fb2bc65e9cf24be6"
  },
  {
    "url": "assets/js/38.640e9ef6.js",
    "revision": "0d260d356163cea4295036638b3dff3f"
  },
  {
    "url": "assets/js/39.983ee526.js",
    "revision": "1d75f7cd998218c7d7a71e6ca83abc36"
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
    "url": "assets/js/app.8b211e69.js",
    "revision": "bd97fe757d52655267bffe869ff2df24"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "19fff516769eeef763e72da2c0c82578"
  },
  {
    "url": "categories/index.html",
    "revision": "1fd2682c77b9be25a16f35bd4f3d0cc6"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "3d9343044ff26e72fa7e8cf9e0cb52ad"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "d93146cf627274e61755642bdb49ab36"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "7ea5931eb207259af610941d50db1d45"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "fdc90e963aa1e62a179be3b5f1fad140"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "ca0de56eaf73c24aaf016117bed67449"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "570a74e36b023079ea5db8f022a26979"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "754077ed46b1c56967bf7afd6d24cf5e"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "cf1b2b8950a757886de05c4cbec4154f"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "aed63973bd2d602b888ec76d2c246dbf"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "d2513628d6aa2dd22882c2ad0cc57fb5"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "a16788a9d150c694b13b18d55b436c63"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "6b145df5e4a7db9adca6bde50855d08f"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "24d2f58e129e0c777b967294343aff2a"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "cda9125749ea0c6a5a592bbfe9efe438"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "99af4ab9d1e9415da06b9a6a22b99ef0"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "b7d1a83f9899ffa224cd406fe16868ab"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "a2c53c9189924cdbea5501c23634d544"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "b52ea8b7032508f8500bff8a5120de25"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "8372cc01c2ac0f7d7a5332af5bd4dc25"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "304ff195e402975d2f442cf4b436062e"
  },
  {
    "url": "docs/index.html",
    "revision": "2d4d7740eaf079a05b48c92e9bfb9549"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "913ac60e7799ad359d056afe51515813"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "e08ddf4c3f35394f42c96a791a3f8b65"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "0c99d99b3d789e22942eb85e0fc1b6ce"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "e45a65904ee04ca258252c7519068855"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "f2baf46463fd5f4bb886b2e10feff222"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "e360d1e7d16cba9310216ea9379ba345"
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
    "revision": "e29e448f8d71ed524d36c1cbd1389d81"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "f4082564b3703bd4d7fe84cb37ed6706"
  },
  {
    "url": "timeline/index.html",
    "revision": "331e77e9bf4a813a1678957037795bbc"
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
