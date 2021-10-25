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
    "revision": "3946cef98dfedabc58c2007e566b1eb4"
  },
  {
    "url": "assets/css/0.styles.8af9daac.css",
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
    "url": "assets/js/1.d0645364.js",
    "revision": "9992e513a633e9cde321ddf8b3a59298"
  },
  {
    "url": "assets/js/10.771c744c.js",
    "revision": "44328625c4340c7e028b3590a253e452"
  },
  {
    "url": "assets/js/11.72ea5dfe.js",
    "revision": "20efa27230576af07ef33ff55741319c"
  },
  {
    "url": "assets/js/12.11aefa22.js",
    "revision": "bdb9771f938b4faa5d5a72f59f0d7d7f"
  },
  {
    "url": "assets/js/13.8451af0e.js",
    "revision": "e1fb146e7ce061f732f06b56a5ec7b92"
  },
  {
    "url": "assets/js/14.f8f049d7.js",
    "revision": "371aef33c60bdf61ca4a167f3dd01567"
  },
  {
    "url": "assets/js/15.2c8ebdde.js",
    "revision": "b8eeb96b72a646f9408ddf3ed16d5fbf"
  },
  {
    "url": "assets/js/16.7fedffce.js",
    "revision": "2613477ac378872e7b2c10623087aa04"
  },
  {
    "url": "assets/js/17.13edd717.js",
    "revision": "9653668d9a57f8b93d84d79c7697a88d"
  },
  {
    "url": "assets/js/18.513e16cd.js",
    "revision": "217b5e99a019b3d4ce35d676600fea61"
  },
  {
    "url": "assets/js/19.3eba5c5f.js",
    "revision": "4cfa7bef8c27fa758a6ad22409b23938"
  },
  {
    "url": "assets/js/20.49b2c11b.js",
    "revision": "c45dcd5009acbd5f9fc4a1e425542254"
  },
  {
    "url": "assets/js/21.4c21c7cf.js",
    "revision": "671e7f65967cb0cb0738dfbe0abb1a1e"
  },
  {
    "url": "assets/js/22.468429e5.js",
    "revision": "8a219c0aa6962d0df36b8f716f9dd511"
  },
  {
    "url": "assets/js/23.923ef864.js",
    "revision": "c1ffe0ff398e0d1ef2feb68797083eb2"
  },
  {
    "url": "assets/js/24.b8813712.js",
    "revision": "0b22ac4eba4a7a7472fafe872c051ba8"
  },
  {
    "url": "assets/js/25.9facf73d.js",
    "revision": "d347ac693c8f8bcea175f7d25ca3ec8a"
  },
  {
    "url": "assets/js/26.d9ec743e.js",
    "revision": "c6b03ba6680531edf9059a073e308ee8"
  },
  {
    "url": "assets/js/3.6aeb0233.js",
    "revision": "48ba62dc1f037f579722751922265c61"
  },
  {
    "url": "assets/js/4.187c3e36.js",
    "revision": "d6d05df230bfed667c7014c73f29def9"
  },
  {
    "url": "assets/js/5.06abe150.js",
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
    "url": "assets/js/8.c61ef070.js",
    "revision": "f647fc0e205d9681e364a3ed6892b978"
  },
  {
    "url": "assets/js/9.881973a9.js",
    "revision": "075cb21e192e0eeda2fd060e8f822fa6"
  },
  {
    "url": "assets/js/app.34c8f7e9.js",
    "revision": "6617803326556e67b228dc9c6b5368a6"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "1d75552a1a89499232a75aec05dea12d"
  },
  {
    "url": "categories/index.html",
    "revision": "75211b5471cc565d73f9e39a0a4d0741"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "c7a8b7ebf6977704a1258d6bb711c9c0"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "2efe36e4cc0ed2fe1a87c4502bfb0ae4"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "86fd4d2923003ffd889823bc14041687"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "449555534b990647160bf4a421b6b138"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "48625e08bb47858198221c3dca52928b"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "4f436463b0c9dbfba16b027babf2765f"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "2b4e6d023dfabda1b0a0c87a9d439412"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "5de348b44dd37768b60437c8574542fb"
  },
  {
    "url": "docs/index.html",
    "revision": "61a1b48dd3b01936ac82d21920bfe436"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "1e0e0c7e898028309c6f5b87da9dc42a"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "791201e2f730cfca54e3b78ca53129c0"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "4a88e32e82cc4ca29941046bdbfd226a"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "660c1844bca9d1b202597621f1c05503"
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
    "revision": "5a3f0d40b978f91941745e4b2f6c9743"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "2de913921cff299f0a7dff599c9b5964"
  },
  {
    "url": "timeline/index.html",
    "revision": "6322aa17d6b74f811f816cd61990c479"
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
