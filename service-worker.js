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
    "revision": "3dfe81e81693cdc604e7e1751fea1ea6"
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
    "url": "assets/js/12.1800d2df.js",
    "revision": "19b38f3c4180af348b374ca74c34d6e4"
  },
  {
    "url": "assets/js/13.d3f03ace.js",
    "revision": "551a5d87061d55f5e4e47cb74b335865"
  },
  {
    "url": "assets/js/14.7e39a8ba.js",
    "revision": "40c99b378b3c08b8ea191170af034a13"
  },
  {
    "url": "assets/js/15.14767c7d.js",
    "revision": "55e3bd4669ab387c31272c887233aec6"
  },
  {
    "url": "assets/js/16.8081e26b.js",
    "revision": "6c58a0619e6ae62f38184b74c14295fd"
  },
  {
    "url": "assets/js/17.d6b33113.js",
    "revision": "a2beb1583f301e35d978e7bdf323ba76"
  },
  {
    "url": "assets/js/18.d5b0830b.js",
    "revision": "4bac1e543326ca63bb9220f04e0ebf50"
  },
  {
    "url": "assets/js/19.2114ca0e.js",
    "revision": "d9b5c6949c1af33c46d23ace01a2463a"
  },
  {
    "url": "assets/js/20.2a556377.js",
    "revision": "9e16baa10078ae89398f8b6295e5b899"
  },
  {
    "url": "assets/js/21.0ffa19af.js",
    "revision": "6f0b6ebc5c217c157bd4adeb76432fbf"
  },
  {
    "url": "assets/js/22.4e45a85a.js",
    "revision": "9815684814aa61da85e45efb6bb8d360"
  },
  {
    "url": "assets/js/23.3086bae5.js",
    "revision": "e21d45fd93e8c735d2443c7414cf3401"
  },
  {
    "url": "assets/js/24.fdc249bf.js",
    "revision": "e18c712a4e16f3645d4bb8785d1e7cbf"
  },
  {
    "url": "assets/js/25.d0febcb6.js",
    "revision": "4b0e540260006c7aacd19d24a06d74fa"
  },
  {
    "url": "assets/js/26.f8d8a9ed.js",
    "revision": "e3dd26c133282d32f700d0228996c075"
  },
  {
    "url": "assets/js/27.5efe0f8f.js",
    "revision": "81d55510b87330ba7ab1d4227d28166b"
  },
  {
    "url": "assets/js/28.fbfaf23f.js",
    "revision": "a765f352a52f14b08479b0129377eb3a"
  },
  {
    "url": "assets/js/29.7d3eb888.js",
    "revision": "4f74d6a1912b8a98c36574eca7719916"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.09e97456.js",
    "revision": "e98804825495d43b777fe43d218def64"
  },
  {
    "url": "assets/js/31.14ed624c.js",
    "revision": "bd92888776d3a80edf0a8892a19fd1ef"
  },
  {
    "url": "assets/js/32.b2dd6008.js",
    "revision": "2108f74c03b93b3bed69523bc60d225c"
  },
  {
    "url": "assets/js/33.92549ddd.js",
    "revision": "92ae86102a42efd12320015ac9195358"
  },
  {
    "url": "assets/js/34.7fdb96d2.js",
    "revision": "ac0cdd32ebf637c53709d08a44d083e5"
  },
  {
    "url": "assets/js/35.0976cdae.js",
    "revision": "c1729d3a8f63011ec52165774d7fcc2f"
  },
  {
    "url": "assets/js/36.eca2269b.js",
    "revision": "cfbe7ed49a1ff527611993b6ce3490c7"
  },
  {
    "url": "assets/js/37.eb72fc6e.js",
    "revision": "5a73e8d088fdd39393a9c491ec0cf239"
  },
  {
    "url": "assets/js/38.a3605a09.js",
    "revision": "899198b0dfa7b5f4c2e1fd1176eb9295"
  },
  {
    "url": "assets/js/39.51071900.js",
    "revision": "15a93ac613b333505bf42eadbee2c986"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.cd3d170f.js",
    "revision": "c8e9a4cd313a6ae48669b937bdafe497"
  },
  {
    "url": "assets/js/41.dfb756ce.js",
    "revision": "fe8e5b49e92ebe5be41acedb1687b81c"
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
    "url": "assets/js/app.6ff6d6f4.js",
    "revision": "66d286443b383b9e1b851947c4945644"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "fe7948150255f9bff6024e78cf7c34b6"
  },
  {
    "url": "categories/index.html",
    "revision": "3bafeb034347f5d0b0451df854a69d58"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "fa6fd486dcf2cc47f4f0a4923e36cc66"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "27687520741a2ac4bd0cbc0ecbe8d636"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "e4fa13b767133a27c4c4a2523124828f"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "d06285b8698616aff063904956d3cbc9"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "6cb58e75fea43d12c32483190285c8af"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "5f7ea97748ec9757c96afa908ab79c13"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "e5810d01eea835d69aeb4a28d8b26020"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "ce619b4da89470c57c1c2e679809218e"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "6294a04e942255736d44d7c21dc0f631"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "dcda4abf735a11b41f99cc73e90d6862"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "194a6a7817986020a4e430adc9c9d9f7"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "c6867009a4ecc4e8cef06f407e7f7cb7"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "2125c591c9b5c6770b38b5ea39f58346"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "b44b60d61785170760fd8d64ff4e592d"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "d8f0b30cf6e750ec705500260f45fea3"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "13c880538c1df5045263d8fa06d5d865"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "348a3d661f031696bed1712ffd7af8dc"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "0819cde3d318ab750b407776def1512b"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "43176d1c7c3b0127085749ffb3b4dcd7"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "e9929c566317f6431383e17c2acf57a8"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "adae01e62ba08552274f35ffae1a6aa1"
  },
  {
    "url": "docs/index.html",
    "revision": "d96f77a4b9f20de6529b5156c82e3fd7"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "7a1e6d3c22ce8e37ccdfe4a8d4d0261f"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "939546532ae182c162abee479d5463f4"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "0387a2f3f0b793fbc139dc566a88213b"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "e5b4e19e10dd43a0f48bb8ccbcf9eabf"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "6b285abd7c16a40e1b0def6b66c96530"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "bb0490996ad2b14673081a6b933361cb"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "8b865191e33b0db94ac4de78820857b3"
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
    "revision": "69772691e299842341ceb437acb385d1"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "8e1519a2c8d81b9f8b38d82231ab1fd2"
  },
  {
    "url": "timeline/index.html",
    "revision": "5e39d7546e64b8e2be6e09535d3370f1"
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
