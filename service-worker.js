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
    "revision": "b91a4bc4fdad4d2bd870b98e216d86bf"
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
    "url": "assets/js/10.43e159f5.js",
    "revision": "44d4a30d2ae0c1cb936c19d5a827a3b2"
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
    "url": "assets/js/13.12022e1e.js",
    "revision": "f54f8760a522b111dae7d5ecacb0b7ab"
  },
  {
    "url": "assets/js/14.b90ba65e.js",
    "revision": "c44af9326072f791eb015467a7444625"
  },
  {
    "url": "assets/js/15.aba856ed.js",
    "revision": "f33bdc3a92fedc3aee980d1f777b9774"
  },
  {
    "url": "assets/js/16.a812ab0a.js",
    "revision": "87f6df616f3e4930566e1cc40294d918"
  },
  {
    "url": "assets/js/17.27df5e56.js",
    "revision": "51a613012bf4ab90e4ac8342dcc78c83"
  },
  {
    "url": "assets/js/18.0c85f582.js",
    "revision": "343e7511f457da50fae198ab30917938"
  },
  {
    "url": "assets/js/19.f9b33e48.js",
    "revision": "848dbd6b62979779f81bc241d8b6f7f0"
  },
  {
    "url": "assets/js/20.a1c9d186.js",
    "revision": "4eeb15748ca11273cbdc9f9a6ea9148c"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.e66e5bef.js",
    "revision": "089354e24d62c6ba4beb5992afc024b8"
  },
  {
    "url": "assets/js/23.f231de6b.js",
    "revision": "0a71427b1bf51fd32be77e9866c99890"
  },
  {
    "url": "assets/js/24.93f40989.js",
    "revision": "9059d83b5bf7fd0c457b2feddc45da73"
  },
  {
    "url": "assets/js/25.d41ec7c4.js",
    "revision": "bf99a604268df1ab353c706c62fed25a"
  },
  {
    "url": "assets/js/26.60e54674.js",
    "revision": "7d6425de4af9d4a4bfbd6963f90c54de"
  },
  {
    "url": "assets/js/27.ac4b92ed.js",
    "revision": "42c3bfc618a4a7a68ff234ec9f0c2693"
  },
  {
    "url": "assets/js/28.43010a54.js",
    "revision": "0c1ae87a0d590e86898ecb040c7ff7dc"
  },
  {
    "url": "assets/js/29.35147681.js",
    "revision": "09f1f902966d3c752af046acf7ca8f2c"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.89312344.js",
    "revision": "f4bc0d70c830c3b53e6aff4e2d530dd2"
  },
  {
    "url": "assets/js/31.255ac4bc.js",
    "revision": "2c80c834ebd93956a40f297f7c177024"
  },
  {
    "url": "assets/js/32.70f0043b.js",
    "revision": "b8948fddee892718b8417a549bb1ac54"
  },
  {
    "url": "assets/js/33.b40d71e7.js",
    "revision": "44340dd51f386a7d3cf5536f82c918aa"
  },
  {
    "url": "assets/js/34.60ed9ee0.js",
    "revision": "b74f5f053df7aaad01bd31a1c839296f"
  },
  {
    "url": "assets/js/35.2832d25a.js",
    "revision": "041d8f777741e606dbb737d2b8f458fc"
  },
  {
    "url": "assets/js/36.fac38afb.js",
    "revision": "eedebf40282eb925c8bbbf7e4e0748c0"
  },
  {
    "url": "assets/js/37.702d749a.js",
    "revision": "c513fa20a40468effc8b12c25e7709e8"
  },
  {
    "url": "assets/js/4.a3d0177f.js",
    "revision": "67138a1fdac208c38513b7004e1305eb"
  },
  {
    "url": "assets/js/5.4dff48d2.js",
    "revision": "db00dc705cfd4b66ddbfa203ae4ae59f"
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
    "url": "assets/js/9.0ad80411.js",
    "revision": "c8f91e10be5a5f7b57f7ec35d954a37c"
  },
  {
    "url": "assets/js/app.203c3b8c.js",
    "revision": "a893bfbb3ffc8c094cf35ebef29dfc45"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "72bddf7283de99c8b4f481f61843711c"
  },
  {
    "url": "categories/index.html",
    "revision": "a35aea5b92b7c90cd4547dd0e901c77e"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "cc2f3ea0b21cad091968a1ef278437e6"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "917156f6d7ca6497f106e63011a22536"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "e97511176d95bd4609b62ec3ed379935"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "012dd6351eaaa675fa711e9368a0e44c"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "a51c8ca93c69ef0da9c84540442832fe"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "1c541d52a7b4c0e73cec4a040d7cb16f"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "38528910bac1c9a89bc6d02aead59c64"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "6183fb93a8451d1280ebfc7d2136897a"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "828f085f99dbca4eea97b176422ad880"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "b454c558d9aa85a15fa5fd830879a45b"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "c7923369857fd22f35026b79bcd72a83"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "38c7a7c46590045d8f7b531bd4843502"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "acdd415e6236187a3188821776f0b135"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "38e32d180b847c2a3e7934e3809ae688"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "c2fab1debc035dea81d633e6908a80a3"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "a87c7e5f65d280f00791d7707c29ed58"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "9e53cee238ff994d1c8626194b956e59"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "0d8690ff067c31a3253d03e1a5ce2a10"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "6b9c8f397194dda3c570f3638280dd1c"
  },
  {
    "url": "docs/index.html",
    "revision": "87598f498178a56af3cadc6ce19aec80"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "d1d4b2dea196030dd1dba174b1e0ddff"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "762862c070baa7d8fb402232d688a061"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "9983012d505aefa428ad95efe3feccdf"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "29520a67c91f913f2fd1231c54daca13"
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
    "revision": "c2201730906dfd454ca09741b267a49e"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "ef93dcf9ad9ca90c663b8ed3b5a5edb6"
  },
  {
    "url": "timeline/index.html",
    "revision": "2d2893067091af3fb2846c2e465c0f17"
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
