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
    "revision": "ddcbf1028e26373247aa790f524355b1"
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
    "url": "assets/js/13.3f1eb4dd.js",
    "revision": "419541c23df8d69ac12099e1e9acb719"
  },
  {
    "url": "assets/js/14.afd88693.js",
    "revision": "3f1fd5f3ddab8acb24d9ed57ef1041a6"
  },
  {
    "url": "assets/js/15.13cfb128.js",
    "revision": "531541f4e28fa8122b52b6aeb63b55e1"
  },
  {
    "url": "assets/js/16.8ec651f4.js",
    "revision": "99ce1ee4e87e709df84f2a06058ab701"
  },
  {
    "url": "assets/js/17.cd1643b1.js",
    "revision": "bf8c6d3f1901d20e8f28834de3bcafcf"
  },
  {
    "url": "assets/js/18.7aec149d.js",
    "revision": "3fa6585608ac81d0ebbe9b0edfcadd9a"
  },
  {
    "url": "assets/js/19.9625ea99.js",
    "revision": "38ab86ab59b7141df0195b0df3a52430"
  },
  {
    "url": "assets/js/20.681b451f.js",
    "revision": "04982239146d35a585f39919491216ed"
  },
  {
    "url": "assets/js/21.64c4e02b.js",
    "revision": "38838919f706acadb0b554873b1f0ca2"
  },
  {
    "url": "assets/js/22.5f41920d.js",
    "revision": "b67f7d76f8ea505f4d0ccd091ee47772"
  },
  {
    "url": "assets/js/23.8f221f5b.js",
    "revision": "969ad5145f3181df4f400a5dba7a70a9"
  },
  {
    "url": "assets/js/24.fe872c8f.js",
    "revision": "34262dffaa34ff92109ae463d26f52bb"
  },
  {
    "url": "assets/js/25.d42a4089.js",
    "revision": "10238226a035a26e0baadf1d754130f0"
  },
  {
    "url": "assets/js/26.a06dd22b.js",
    "revision": "a68edacac23971304520d0541f34d127"
  },
  {
    "url": "assets/js/27.1173cdab.js",
    "revision": "b451023930e9c3452c16a7bc6ab21e4f"
  },
  {
    "url": "assets/js/28.560b3029.js",
    "revision": "034e5d5151c04fe6a46814154cefaed1"
  },
  {
    "url": "assets/js/29.82256878.js",
    "revision": "ec968591b36ae11002c126fabddeff10"
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
    "url": "assets/js/33.20b73de0.js",
    "revision": "b5e04d5bb7797c9e1af72e4ce3176553"
  },
  {
    "url": "assets/js/34.6fe811b6.js",
    "revision": "b6d42848042c51a4634b31f246ebbd03"
  },
  {
    "url": "assets/js/35.2ce73343.js",
    "revision": "95f51aa9bca6d09c342794ac793e5f0b"
  },
  {
    "url": "assets/js/36.131064b5.js",
    "revision": "6dfbba64e5229944bcc4ab6c625aa8a2"
  },
  {
    "url": "assets/js/37.6c8cff6d.js",
    "revision": "26770b58fbe46959b43cfcb31f50a8ee"
  },
  {
    "url": "assets/js/38.6de2d7a0.js",
    "revision": "ef7a98a113d14c81436c765085d0894e"
  },
  {
    "url": "assets/js/39.04ac50de.js",
    "revision": "239b6ce86e9d74445a2479ff882490ba"
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
    "url": "assets/js/app.19a3cbd4.js",
    "revision": "ba4f51663667e6e8d7208a7d8cecf9c5"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "546b79b5e01a605e8bf6351c1ed61ed5"
  },
  {
    "url": "categories/index.html",
    "revision": "f9495fa30a385791998b9ae06f1029c6"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "b91e2027013428583572c7034154640f"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "19ae7d6b106a4e926b5e84b337ddc464"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "337030869f45a44e3486060ce51a13ba"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "3b008f2707396c8ce0cba5c3aba5e849"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "0570b0681fcb8724f24fe624345c1357"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "723c87317217ee70c864810fca160227"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "5789e27e37bc047b481f1732193ec419"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "5de9230a3211c5d905969a6cd9e44f64"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "2fe3531745770522ab1c7943b7df8642"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "8aae4601c857a9079d9a19f8aa22b604"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "cc8abc3a60564b9fa9f7f68db05d270f"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "f2bfb144ccd8dae2ad1513c203aaabe9"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "1b4fa41b2726b4704afd21fbf2b979f4"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "578501d954a3571c174c35e13c011a9c"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "68dfbab5f0ae66d89f749fcb7813f823"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "b757820f9e9e0eef54f9751292b4ef48"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "e924eb94454bd6eec2186a6ee718d0ca"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "bd216b17d7ee8bab65b375a593214fef"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "ad2840da5fa9e0f4f712015f231f8066"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "3da1e638e6ac143a591cfbf44813eebe"
  },
  {
    "url": "docs/index.html",
    "revision": "0c2f5d468b0c261bd063b4fd6aa4ec99"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "d6745aca89daf11b47679e60d8e6a0ed"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "342504b89c0ea0b28ba8ed0947856f43"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "cc10080050683c8ad34e7af19bd39372"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "82b3933ba882795ef32bbe99b78f308f"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "593b645ff0817a63dce9a6e628a3dcf7"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "b0adca9e6b8f4abf86e03726e6dcd85d"
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
    "revision": "00c315eeba6425a041eba93e21231152"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "6a9d109b26f616b70dec35ac6f2e38b1"
  },
  {
    "url": "timeline/index.html",
    "revision": "ebb937b0e14c53acfa22a6d10a8ba7e9"
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
