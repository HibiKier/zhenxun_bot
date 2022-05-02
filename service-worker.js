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
    "revision": "2e24fc4ec858250aa468fcb13c230e1f"
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
    "url": "assets/js/1.5a85ab28.js",
    "revision": "3e725c01393322b28b3cc706eb8bbd58"
  },
  {
    "url": "assets/js/10.c36c3cdb.js",
    "revision": "ea64c20ea854e58bb44642636538e76e"
  },
  {
    "url": "assets/js/11.e9b0183e.js",
    "revision": "10f26e1177e8231499023ce9c00318cb"
  },
  {
    "url": "assets/js/12.505ff660.js",
    "revision": "b4969ee57073087602bd1f72251eb0fb"
  },
  {
    "url": "assets/js/13.556ed60a.js",
    "revision": "7535fa2b2b90eb3d3355b814a871db1d"
  },
  {
    "url": "assets/js/14.7e39a8ba.js",
    "revision": "40c99b378b3c08b8ea191170af034a13"
  },
  {
    "url": "assets/js/15.f3ba613f.js",
    "revision": "9ae6f63cdf510122520689af8328d039"
  },
  {
    "url": "assets/js/16.8e9e4136.js",
    "revision": "261b6f81f1f0feb35408014a7148233a"
  },
  {
    "url": "assets/js/17.cafc13bb.js",
    "revision": "ff84cc76b1e7b990653ac1ab6ac99800"
  },
  {
    "url": "assets/js/18.926bda27.js",
    "revision": "ba5a342533696bf8fea7af979d3dbb94"
  },
  {
    "url": "assets/js/19.8edb492b.js",
    "revision": "5c82780c94f029fe04aa3f937ae9e497"
  },
  {
    "url": "assets/js/20.f527068a.js",
    "revision": "0e8d66c0017aef4c278c6dabe11708ca"
  },
  {
    "url": "assets/js/21.2a98af4d.js",
    "revision": "be66719f17aa228687a629b119bda2c7"
  },
  {
    "url": "assets/js/22.c016f726.js",
    "revision": "a88fc6c694836765415ae6093e1040ad"
  },
  {
    "url": "assets/js/23.627b7a1f.js",
    "revision": "b406f064cfb69b633e0d9a534494daae"
  },
  {
    "url": "assets/js/24.9afe2b95.js",
    "revision": "e47d38d21c9302c7d57c8813dc583c5f"
  },
  {
    "url": "assets/js/25.c6c38810.js",
    "revision": "4ae501bfeee41ded69e37a7cf16ac24b"
  },
  {
    "url": "assets/js/26.b2377558.js",
    "revision": "21c3fe807c269a357011424bc784cdb8"
  },
  {
    "url": "assets/js/27.cedf7481.js",
    "revision": "3eeed0e06af58e881d716f1caca3917e"
  },
  {
    "url": "assets/js/28.424981c8.js",
    "revision": "8182a82b4f3a9f1fbee4f19507ac0904"
  },
  {
    "url": "assets/js/29.3587a05c.js",
    "revision": "d7935eab616dd4e156a162d22ff21daf"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.6223d485.js",
    "revision": "bb1669346e1fad86cf4f629e44c6227f"
  },
  {
    "url": "assets/js/31.59cf9ddf.js",
    "revision": "76a3558dad4c09ba973acfd4c22f3c72"
  },
  {
    "url": "assets/js/32.784c547d.js",
    "revision": "b7bd0c2b0c6226b3d78e997561617f93"
  },
  {
    "url": "assets/js/33.3c9c2b8f.js",
    "revision": "f8983b4fefdf3e4dc649585dabc2dcf5"
  },
  {
    "url": "assets/js/34.ed83cfa3.js",
    "revision": "c8fed0a4488961c1e16847977ff30171"
  },
  {
    "url": "assets/js/35.c0128aec.js",
    "revision": "ff44ff831c1121d741481b450f0d1c1a"
  },
  {
    "url": "assets/js/36.369767f0.js",
    "revision": "6cc22f668465a763f833a1eac458f7ba"
  },
  {
    "url": "assets/js/37.3069f322.js",
    "revision": "d136731d86c8c3be264390737b5c25f2"
  },
  {
    "url": "assets/js/38.1da64650.js",
    "revision": "2430ab50e3eed4705e8e33b9059de387"
  },
  {
    "url": "assets/js/39.088f0b16.js",
    "revision": "97efce35308b04f1feba0593d39aa172"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.a440785c.js",
    "revision": "0e95421074c87c560926e6159f30a72d"
  },
  {
    "url": "assets/js/41.2413d124.js",
    "revision": "f75ca9b6f6964177ac8d36ac2dd4a38b"
  },
  {
    "url": "assets/js/42.2f2808f6.js",
    "revision": "faae1588f276e2b8087efb9a4a4c6904"
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
    "url": "assets/js/8.6dce9ba3.js",
    "revision": "161c1d689495c7bda88f26753c3ee481"
  },
  {
    "url": "assets/js/9.2c396e80.js",
    "revision": "7524c843427c55e0d85aca4f6931429b"
  },
  {
    "url": "assets/js/app.e65f8001.js",
    "revision": "8ec8d9badf4bfed8ecb37c51c21844da"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "4c722cca4f334759b76938409869236e"
  },
  {
    "url": "categories/index.html",
    "revision": "d80fb31a8a9fcca5424560c68177e8f1"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "dce35c5e1524e0b93d2411ab25898af4"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "960caf66fcb42a86fea73ad85102444a"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "e12e75aa76c491ef1af41474284fd1cd"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "451d5028012df6d442dd14cfdc230eab"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "04b50af1113a54e2bae5dcfa742dcc73"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "6d9b021832db6b965bd5018867e91970"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "3998a810eb97b0e6605fc569fd31ab9d"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "38c7278b0ca2ff1238956f007aa1ea3c"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "29b0171865d0277c2f7451a9e04eb1df"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "d51a8eae08361929a92c964ea11fc891"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "0151ffc75cf84fec8ccd27a4ab491e3a"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "a0af36a2ec011e445278258ab9dabae6"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "f4ba7d66301a31d30de9ffde161a5a2a"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "b7577f9c71c53efb7b074014b1a39f28"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "490821b9d72da6eef0bff06e9750898e"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "c97bfd0bfd756d904fd8af25cb0c90c1"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "b9863077b085c611bee0d29dbb1f534b"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "e62825ff3f6838a959effea82ec07054"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "07925f95247b751e6747e21560374125"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "bf2c943f0b6586cb48bd2e8d6b466683"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "c14be7409f79359dd79df0c3357eee7d"
  },
  {
    "url": "docs/index.html",
    "revision": "111febba478f3a864d3bfa1558c65d40"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "95e79eff3ca8657bfe72fa992ea431f8"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "b7ae483579935c74569dea74ab1befdb"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "2f4613738ee6810c538b5505eb149336"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "b54eaef3e43a26bc8d9f351ea12e56ba"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "cf574bede9bed9be80cc31ecee2fd278"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "1e2176979c6193c1f911247b4965d4f9"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "226ea96530e198803aaadeb8f9e81c97"
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
    "revision": "793c6967ea61fd4501a9d00c9f3e7aa7"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "33936ae7eb3b1da3039d661ebc3640e6"
  },
  {
    "url": "timeline/index.html",
    "revision": "81d0b002363f86e2e51ddeed3dcc4416"
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
