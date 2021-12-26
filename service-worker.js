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
    "revision": "f8bd4dabdc844ac13034c0a524eb6a5d"
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
    "url": "assets/js/12.70b87ad0.js",
    "revision": "6556acbe8d4bdd20a6393ef9f3a81f29"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.e1c3b76b.js",
    "revision": "58f90f54e85eb5ec64223971833c40c3"
  },
  {
    "url": "assets/js/15.547e813e.js",
    "revision": "4fdc0434239a03f0f6d56c7780f9c7ce"
  },
  {
    "url": "assets/js/16.cb7e1e04.js",
    "revision": "4ab72ac4cfd882d122fd93846a669691"
  },
  {
    "url": "assets/js/17.2e26617b.js",
    "revision": "5052ba1f5cbf1bb83cddfdfebbfefa04"
  },
  {
    "url": "assets/js/18.a8ee201b.js",
    "revision": "f6065513ebe5f22c2136c6aa4c7ec60c"
  },
  {
    "url": "assets/js/19.f57d35c7.js",
    "revision": "dc0bdcdee2db6bd71f98638769940e69"
  },
  {
    "url": "assets/js/20.7da5e546.js",
    "revision": "d9ff1e63c2b42626bdad3ec033afe199"
  },
  {
    "url": "assets/js/21.e709c1f6.js",
    "revision": "751908ef76ef4a1083069880567bbea6"
  },
  {
    "url": "assets/js/22.807dee42.js",
    "revision": "9e9a21e65f988a01a01bef196dd26b4b"
  },
  {
    "url": "assets/js/23.30b50072.js",
    "revision": "aa85ac5a9c807eba985e4fbf7c9468f4"
  },
  {
    "url": "assets/js/24.7f836962.js",
    "revision": "debf2d756784130d8973e96a7440f13e"
  },
  {
    "url": "assets/js/25.f387300f.js",
    "revision": "11c83333bf2240be1dd6d8fc2533ad5a"
  },
  {
    "url": "assets/js/26.1eb2ed74.js",
    "revision": "4556e32edb033e17e610636ce97678e3"
  },
  {
    "url": "assets/js/27.7cec4bd4.js",
    "revision": "01d0705592ec6372705e165098645c18"
  },
  {
    "url": "assets/js/28.f8a3548a.js",
    "revision": "e3024931cbd86c18c5aa87469c3c3b39"
  },
  {
    "url": "assets/js/29.390652d9.js",
    "revision": "e02348e56cf8c41822c635eb6ea8baf7"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.007a9ec6.js",
    "revision": "681e47fd112d45902f68cac8565b3f4e"
  },
  {
    "url": "assets/js/31.15720522.js",
    "revision": "2df5b8e57f9cb587b4e1ab68174fc373"
  },
  {
    "url": "assets/js/32.a669934a.js",
    "revision": "e4b3747976a822c4b9fdf2bc2388e3f5"
  },
  {
    "url": "assets/js/33.41277a61.js",
    "revision": "d10425047a77c655361bd7aa470ba8af"
  },
  {
    "url": "assets/js/34.7885b8aa.js",
    "revision": "6980df03da2488492ce1a518423fa7af"
  },
  {
    "url": "assets/js/35.95b64945.js",
    "revision": "7bff53cf5bc1a71d570b8cb3afbc6a56"
  },
  {
    "url": "assets/js/36.9f16e61d.js",
    "revision": "65150360be5b01b08e7c94b9f762e7ff"
  },
  {
    "url": "assets/js/37.3b342986.js",
    "revision": "a5693e82454667373beaa3cd965830f3"
  },
  {
    "url": "assets/js/38.33fc3f94.js",
    "revision": "1b91745ba5d0b48a18404c014aff00ef"
  },
  {
    "url": "assets/js/4.7b2626bb.js",
    "revision": "1642b25041b4fce55d1447249497b0b6"
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
    "url": "assets/js/9.787fbae3.js",
    "revision": "460cefd2b2626371bd6a73fe956f3631"
  },
  {
    "url": "assets/js/app.af647a32.js",
    "revision": "df8788f6789f6157eb65c4aef195da83"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "06ea6f3ef73a6373b84a7d21bad5f057"
  },
  {
    "url": "categories/index.html",
    "revision": "26dc9b5748be4c17eb227342f776269b"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "2417d8b5577225802bca5435d640674d"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "3fac2efd920fe127d4ce1a5ca29f694d"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "c2924e7ce82749bfc57b8041a301168a"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "b961300dba68ecca18d3ff801274fe46"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "10e311c36ad47aadede1146fff4305f7"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "a741623ae8fafb41a7dcf7e997788015"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "c11e6885c72fdd0a5b377ca763fa3a13"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "d9ff18e5fcd8a665481169a7d2210126"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "d0fc73c4b6abd100325694dcf19d10ea"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "890786cebab4b3ce43fadf0342842672"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "489672a23f6400d8814a12515bac0713"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "2063ef4414afdf95479a650685b6b929"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "61a7e2248fa7550df1dcd6cffcc334e3"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "757cd9a4395847c52c7335166bb19a98"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "8ed2d8d765db9729cb693dfa6b1d2621"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "bec99cc08a8c57fc03a260e18ab2e327"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "cfedbec1de92b9f7dc617c67e9239809"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "6e3a8dea0b3eea38e7b382c7bbbb7a1d"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "58ee380d10b810fa66ac376ccdca2eaa"
  },
  {
    "url": "docs/index.html",
    "revision": "9ed1c14f7d3887b31b58af31c88a38f6"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "0f0157c0477c94262f57500840ba1524"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "f53cde1412f905ec78a0d588000345ce"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "8ce9d28f282cc130165b9b39aaa2ca51"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "cf12fc87429f69cf0383b324675a1cdd"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "9f10c35c1f2e5469c0bbf0aad666265e"
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
    "revision": "40ec64597ec4cbf8ab80df38d791ea2b"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "0fa2a991784e07b1181a5a43e9e6e862"
  },
  {
    "url": "timeline/index.html",
    "revision": "2807b50459b6fbed319104e822780795"
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
