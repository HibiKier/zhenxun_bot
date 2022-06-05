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
    "revision": "ca1758523920e58c4bdc046e46d0ec83"
  },
  {
    "url": "assets/css/0.styles.3af13d03.css",
    "revision": "3cf231b711ffdd04ad7f9a9b68414e7b"
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
    "url": "assets/js/1.bbc69b0d.js",
    "revision": "86fe09a13a05ffcb0d69b14597cad433"
  },
  {
    "url": "assets/js/10.c36c3cdb.js",
    "revision": "ea64c20ea854e58bb44642636538e76e"
  },
  {
    "url": "assets/js/11.2733a77d.js",
    "revision": "8744223bea5439bc59f36eb0368a7249"
  },
  {
    "url": "assets/js/12.1800d2df.js",
    "revision": "19b38f3c4180af348b374ca74c34d6e4"
  },
  {
    "url": "assets/js/13.d8530c5a.js",
    "revision": "1419e11b9aa46eef11de9df2c41eea54"
  },
  {
    "url": "assets/js/14.75207c27.js",
    "revision": "dc4f96e6d8b6ca0d16f47c03eb5063b4"
  },
  {
    "url": "assets/js/15.01a04ac0.js",
    "revision": "1874ff8a4c24be0f1578034293244bd7"
  },
  {
    "url": "assets/js/16.8fd33aef.js",
    "revision": "92b1363fa83b668967e09f3c036307bb"
  },
  {
    "url": "assets/js/17.afbd20a3.js",
    "revision": "c7af6cecf7e2f587f1bdd46abbd54958"
  },
  {
    "url": "assets/js/18.397d47a0.js",
    "revision": "eb5c90c751254ab17668204eeaec5630"
  },
  {
    "url": "assets/js/19.adf18d0b.js",
    "revision": "431299346000d64b2f7d47c036340616"
  },
  {
    "url": "assets/js/20.457ffb2a.js",
    "revision": "b5b33baf391d71762ce1ec12c338824d"
  },
  {
    "url": "assets/js/21.e98991d2.js",
    "revision": "1c4aead8954bc8f5999daa3e78aae5a9"
  },
  {
    "url": "assets/js/22.5027c6f9.js",
    "revision": "a859162daf91ff1dd3b937313e610ca9"
  },
  {
    "url": "assets/js/23.ac4ebdc3.js",
    "revision": "45432e5e685c57c013f2f2fb26bf4a53"
  },
  {
    "url": "assets/js/24.bdd9bd7f.js",
    "revision": "9ccc97a6329e747dcba9160b26b3e4f3"
  },
  {
    "url": "assets/js/25.47989af7.js",
    "revision": "77718390f38599f0e4d9ddcb7c9786c8"
  },
  {
    "url": "assets/js/26.ee90be6f.js",
    "revision": "6feba045529a2fc26c13ccf48b1f5a09"
  },
  {
    "url": "assets/js/27.0f8adcaa.js",
    "revision": "232d19d2b5f7fc326cff23fe82e98877"
  },
  {
    "url": "assets/js/28.5c7c5d59.js",
    "revision": "b81ff2cc2ae8a5881e267efa8db62643"
  },
  {
    "url": "assets/js/29.16add951.js",
    "revision": "5814a484ac0618fa10dd6f7cf6181bd7"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.d9f43113.js",
    "revision": "fd0f277de35a7af0dfeffe211ef306ac"
  },
  {
    "url": "assets/js/31.c24e9799.js",
    "revision": "8cbe2a1207127385c002e43819a9880d"
  },
  {
    "url": "assets/js/32.fbd205c3.js",
    "revision": "5c681cde1daf9cd129e95ab32bb62c9d"
  },
  {
    "url": "assets/js/33.e45e0ee8.js",
    "revision": "8e8691550dc4354efc4ac89645f100e3"
  },
  {
    "url": "assets/js/34.abd9c9a2.js",
    "revision": "e4c7f140b7f0b54facdd2276b98cc9e8"
  },
  {
    "url": "assets/js/35.978b3044.js",
    "revision": "1ba24d3564c6ab99afadc9d0c9870214"
  },
  {
    "url": "assets/js/36.291ffe71.js",
    "revision": "1f58326a5d3136396844c38d2eced12b"
  },
  {
    "url": "assets/js/37.666a2c50.js",
    "revision": "610b766971f5ed33e7805d28ec48c205"
  },
  {
    "url": "assets/js/38.bdc79a9d.js",
    "revision": "2b85b758ae9bc5ec40215aa76aa9ed71"
  },
  {
    "url": "assets/js/39.e333edcd.js",
    "revision": "bc0cae8e620932e949eb83026b8c6b59"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.dc2feb81.js",
    "revision": "028ef391f311df97340fccee1cc7546f"
  },
  {
    "url": "assets/js/41.6ed625f4.js",
    "revision": "3b8b3364203bf3333a433ff341dedc72"
  },
  {
    "url": "assets/js/42.b977332c.js",
    "revision": "cf3033dc07b16662aa43ef161b78bc5b"
  },
  {
    "url": "assets/js/43.a776789d.js",
    "revision": "5b1e00b76eb27af5c4705db1096d2dff"
  },
  {
    "url": "assets/js/44.9a9e7058.js",
    "revision": "1871bb9a6811e39ca4b94f05538e4483"
  },
  {
    "url": "assets/js/45.ddb2ba5d.js",
    "revision": "e77632158da24bd633107d32836f6ffe"
  },
  {
    "url": "assets/js/46.663316f9.js",
    "revision": "5c73d0ec082b22143f3791af8ac01bcf"
  },
  {
    "url": "assets/js/47.cde5903b.js",
    "revision": "b9926a5065dbcdf675885eb9ec128809"
  },
  {
    "url": "assets/js/5.71556fb3.js",
    "revision": "d259aa4991e4571fe7518f3671248ccd"
  },
  {
    "url": "assets/js/6.100e6bd9.js",
    "revision": "4ee9151e86f1690b6fa48777b76a5c7d"
  },
  {
    "url": "assets/js/7.3873c60b.js",
    "revision": "eedf755734c240c423164a6b4d25663c"
  },
  {
    "url": "assets/js/8.8aea8f6a.js",
    "revision": "0aae2683c4faa976504569728801f1e0"
  },
  {
    "url": "assets/js/9.ce4fe8d3.js",
    "revision": "17ce9bbc31f9593a960b7715f0b5318d"
  },
  {
    "url": "assets/js/app.554647c8.js",
    "revision": "9dd49f908375981640e0e7f18847ca1d"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "9a8e3cc5d2151e53c81733158d3bfa50"
  },
  {
    "url": "categories/index.html",
    "revision": "ffcdb6969d9fb6f5a3002ab3ef8b605d"
  },
  {
    "url": "docs/api_doc/group.html",
    "revision": "b5f2767bb2274654faa05df9416003d1"
  },
  {
    "url": "docs/api_doc/plugins.html",
    "revision": "a2f22666145d498f32c10930618fdbe7"
  },
  {
    "url": "docs/api_doc/request.html",
    "revision": "1610b89a8f20c5094eb3706f60d353e2"
  },
  {
    "url": "docs/api_doc/system.html",
    "revision": "5f05221de8ba8ff00b4a441c5bcfc92c"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "5d8f107e02cdf58759b12879ba2fa284"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "558a90fef96a88e191492475e0429646"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "9697fab99978d357fa4609666b7ff932"
  },
  {
    "url": "docs/development_doc/utils.html",
    "revision": "8edfb1ae55582404e0996348696b6ccc"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "d8266070a92f58d5ec50233ff24670d6"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "9d962261797753fef314bf237653febc"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "4573d5ad99547f03fc42fa689edb9818"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "091cda020ead218c4a3e8c1087942d9c"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "97c859e9dfa856a63aa58074d20b0327"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "e96800c8503a33a1d15d559d4c5b4d82"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "d5a282ff88c612681567083faf24fc5b"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "601df31e63e0ab4208be878fc594a254"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "0e0115193fa826ccd63b100293e937a3"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "9127e45a1879906f134dbb9a04ebae6e"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "d21f57e7860ef0189c475c030f7f827f"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "3de8ec49011fdaa9eb176fb1ccb7f696"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "75dc9158df50081f140ab71bb6c5bb5c"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "11c0ac1e5854e8c449e8af1fbb4f33df"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "543c73831a011d0ce01dfd3da5f4085b"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "d99e36f352264908ef0ab875f7ec97c0"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "2fe2aaf17d8205b6b059ebae7495edb7"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "65c2ba705e722bf280c906397591c89e"
  },
  {
    "url": "docs/index.html",
    "revision": "be741c348bad169c384199aa25fda9f6"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "a9e18a727f698b27467099b9471f6ccf"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "8834a6538cb9575399ce46c5e5e0a894"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "c55c8c9fdde8aed92b78c592df18da12"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "e02e0c90dbb6d5aaf14b518fe48342a5"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "0c354c3362cf7376f8b51fa87f79452c"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "a6edabda3acbbffcf17a145deb341357"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "a895b71a8437683c8ac78a0e4f632559"
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
    "revision": "8f03fb6b23e464da91c44ac7143330cb"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "5c082b31e379f98a4be1ad47407dce8b"
  },
  {
    "url": "timeline/index.html",
    "revision": "e5c53633e9f03a497a331c7297c60f7a"
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
