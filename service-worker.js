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
    "revision": "1de630e0b2f3b00d69d5e5edc93590db"
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
    "url": "assets/js/11.e9b0183e.js",
    "revision": "10f26e1177e8231499023ce9c00318cb"
  },
  {
    "url": "assets/js/12.9be1bab5.js",
    "revision": "2ae8b75065f7db760178dcdd36e05078"
  },
  {
    "url": "assets/js/13.4db93f3e.js",
    "revision": "39a7cd275e2846855943951de070f303"
  },
  {
    "url": "assets/js/14.8b1d3740.js",
    "revision": "8a3e5bcfe3135c89071ae92cbd2d93cc"
  },
  {
    "url": "assets/js/15.75e81160.js",
    "revision": "f60af58f38a9fa05d4c98684d05eeaa5"
  },
  {
    "url": "assets/js/16.61acd6ef.js",
    "revision": "c7d80916edd220d6dcd601512b5309c9"
  },
  {
    "url": "assets/js/17.67653935.js",
    "revision": "ed8b8ba53e4a880561e535ba826973a1"
  },
  {
    "url": "assets/js/18.00bbed38.js",
    "revision": "8af58f729e2d9b15b8f321e986680b09"
  },
  {
    "url": "assets/js/19.dffd9f24.js",
    "revision": "4e03c7d7e12cd61345592c3e0d5ceab3"
  },
  {
    "url": "assets/js/20.457ffb2a.js",
    "revision": "b5b33baf391d71762ce1ec12c338824d"
  },
  {
    "url": "assets/js/21.cca97836.js",
    "revision": "a2f65190df9298a99efd456b8244b76c"
  },
  {
    "url": "assets/js/22.86656817.js",
    "revision": "1cd687b24262eb77d089569e5b55fc0f"
  },
  {
    "url": "assets/js/23.376ef950.js",
    "revision": "945842db5bc300d0a1e355d2479b11f6"
  },
  {
    "url": "assets/js/24.0da09d93.js",
    "revision": "f780ebb91677e846a65b3b6a2fb38b5b"
  },
  {
    "url": "assets/js/25.6db88c49.js",
    "revision": "3c2c4d4f911c52c76c63d23c2fef61dd"
  },
  {
    "url": "assets/js/26.1e544b0e.js",
    "revision": "f0bf5986091ded10560d7c7fff6788e6"
  },
  {
    "url": "assets/js/27.b2a696f5.js",
    "revision": "7e0142dce4dd71c77d7207cb257877fa"
  },
  {
    "url": "assets/js/28.37914e63.js",
    "revision": "c360d9696325431b6846c5a6e24472eb"
  },
  {
    "url": "assets/js/29.ac9abe31.js",
    "revision": "c67d287f272ca7b7dcd64ec982ac86b6"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.4c83a264.js",
    "revision": "e7f41de27277492c1a0ba87f5cbb06fe"
  },
  {
    "url": "assets/js/31.145c2060.js",
    "revision": "062c36eabe30d15a78badfc654bc6161"
  },
  {
    "url": "assets/js/32.dd5893fc.js",
    "revision": "76a55c20809fcbe60506eff94b9560cd"
  },
  {
    "url": "assets/js/33.0163d702.js",
    "revision": "2f686503bba276a0628145ef3bbe6f13"
  },
  {
    "url": "assets/js/34.f308772d.js",
    "revision": "0fd642030df472f73ae5767f6e0fb668"
  },
  {
    "url": "assets/js/35.2248e851.js",
    "revision": "d28ae0af87788f758f55e853515e5a79"
  },
  {
    "url": "assets/js/36.e2f701ed.js",
    "revision": "1987a8f473dab659d97032b2b7e64ff9"
  },
  {
    "url": "assets/js/37.ac4cffbb.js",
    "revision": "b5a8e4ae0a1d2d314858bf497cf13aa2"
  },
  {
    "url": "assets/js/38.d4a3669d.js",
    "revision": "0e4bd320c61977d3d97423c43d9a6cec"
  },
  {
    "url": "assets/js/39.0a44dbc1.js",
    "revision": "d9aa8ff4cfca693d3561761e5fecc94f"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.8a17e9bf.js",
    "revision": "d442452f51df49f44757e1d3e7792028"
  },
  {
    "url": "assets/js/41.cde0308f.js",
    "revision": "b740d7f86f169bbea00f8426b9b99355"
  },
  {
    "url": "assets/js/42.3eeb851c.js",
    "revision": "1b29170c64fedde17a79ee37dea4d69d"
  },
  {
    "url": "assets/js/43.8d105861.js",
    "revision": "5e7ee0718c388103b9342dcf41732965"
  },
  {
    "url": "assets/js/44.b645317e.js",
    "revision": "d19368243f026d20d05ada1beabe6972"
  },
  {
    "url": "assets/js/45.83ae5c27.js",
    "revision": "d6c4aeda865925d9ecb9c4f8c2a7e4ea"
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
    "url": "assets/js/app.27d44162.js",
    "revision": "a72f03b7abbffb958e1b5f005ab5b096"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "77e0894a6c2cf5606edf77567cd7f4ec"
  },
  {
    "url": "categories/index.html",
    "revision": "431c35eb6e3f3b670bfbf84b9d53172c"
  },
  {
    "url": "docs/api_doc/group.html",
    "revision": "4d0eef7a6ef9fce0a1d773ad3a0ba957"
  },
  {
    "url": "docs/api_doc/plugins.html",
    "revision": "328755e2d89c598bdcdca6e3b17f6f1c"
  },
  {
    "url": "docs/api_doc/request.html",
    "revision": "abbf10f785f099b612aaa4f03bc1210a"
  },
  {
    "url": "docs/api_doc/system.html",
    "revision": "aa826eb4e589050adb6af0348006c6c5"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "477cab6887e13eaff7c82d3c3dc5b26e"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "e511190abc874d664522ca45f67de0d5"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "0684530c302eeb363669e145537e2807"
  },
  {
    "url": "docs/development_doc/utils.html",
    "revision": "dd76060def756ad6c14eed1f157f3bc5"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "88038f87690eefe390e7ca8dd2ebf8d9"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "711ad416179d871e12a4c0ad231a4f6c"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "174a1bdd9bc9a095302bfb2481e54930"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "54c5e6c2876d803775435093661f6f10"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "d0357d215dc439fe6c76979c71defd4f"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "b42dc7f69df6c6b18b9ed2db370ea9df"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "b9383f2871710d725d0e2224a0a88fa1"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "52317c4950b48f103b177897552bce55"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "3b606f767420d3344cb5560dd191d7e7"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "ae2688056a750056c47e20a564e9e96d"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "f71958455e206e2da80b82e30054fa7f"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "f3821b4feac9ce49306b4d5c2364d70c"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "a268cbb52cb1ef263724b61d30fe8d4c"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "16a6f5f2e68baf03778ff79cb9b0f706"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "f23b6264125cba5c0a70c937abb65c30"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "594e368143b67ed28da80df086a13d16"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "d1455a6c20a2577cc0720c36ea28fa13"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "9aaaf2f78c198eec074389573933dca5"
  },
  {
    "url": "docs/index.html",
    "revision": "605663f3194a9e32e976855da57ea69a"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "983a00a26ad12940681853a0dac14541"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "8dac33caee616d13290e91eac80948ed"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "8bda496dc01c6f15602b4f26d4a666e5"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "29a81538abf0b1322a34eb323dc37cb3"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "7ed94b5dd7de5c1acd177096b4780fc0"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "8632e45c00ad66aaae0ffa4324cd3fb2"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "41d5493183076f007b5c2325c7709fd6"
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
    "revision": "42fc9c9965bd8e67f609eb6e90a4067b"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "6b32fb963647b00c4654a749befc147c"
  },
  {
    "url": "timeline/index.html",
    "revision": "b8d768f012d19a91d3de255e3ee8021f"
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
