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
    "revision": "b8807d2f39c1dcaf7e73e4c27b693700"
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
    "url": "assets/js/1.d0645364.js",
    "revision": "9992e513a633e9cde321ddf8b3a59298"
  },
  {
    "url": "assets/js/10.771c744c.js",
    "revision": "44328625c4340c7e028b3590a253e452"
  },
  {
    "url": "assets/js/11.d21d703a.js",
    "revision": "2967043667710a57aaa057b84613d137"
  },
  {
    "url": "assets/js/12.4ded0b77.js",
    "revision": "fad2a6d11f1bcca87798836e830fda72"
  },
  {
    "url": "assets/js/13.b8e9da34.js",
    "revision": "9efc273c1daa714890ac88e9eca123c3"
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
    "url": "assets/js/17.15756d3d.js",
    "revision": "63e03e18218e8407a5ef3da7a1937cb4"
  },
  {
    "url": "assets/js/18.f8a27378.js",
    "revision": "58dd325f214552c8f77b3cf99b6a1bd2"
  },
  {
    "url": "assets/js/19.b6c5f265.js",
    "revision": "bcd9d2b049f1b9e2237b42a8a730f933"
  },
  {
    "url": "assets/js/20.8a2dcf3d.js",
    "revision": "cb53d6b992c716402f3a68d2215939f4"
  },
  {
    "url": "assets/js/21.4c21c7cf.js",
    "revision": "671e7f65967cb0cb0738dfbe0abb1a1e"
  },
  {
    "url": "assets/js/22.ac2df5ba.js",
    "revision": "273c25247216edf4b2db17184cc39403"
  },
  {
    "url": "assets/js/23.09ce929d.js",
    "revision": "b0b4370eb8d4842d730e1e50cc7a0374"
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
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/4.1f0d7c87.js",
    "revision": "91006d54db55ac1d91d2a92f0a0e0f7b"
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
    "url": "assets/js/8.c61ef070.js",
    "revision": "f647fc0e205d9681e364a3ed6892b978"
  },
  {
    "url": "assets/js/9.881973a9.js",
    "revision": "075cb21e192e0eeda2fd060e8f822fa6"
  },
  {
    "url": "assets/js/app.b43885af.js",
    "revision": "59f5917b8e7690075f2861cf7068e68d"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "bbb68014ea17ce4ffdfb92ed52545385"
  },
  {
    "url": "categories/index.html",
    "revision": "54bacb79f5021419f0deb6e824433d79"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "af537dca0081f938a9f98a8bb447e11c"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "6c8dcfe0fb2c01bb6af6fbafa25986c3"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "3de0baeba841cc883acd4b37a883ca27"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "441d00d126b4da9de8eaa8be0dd06dcd"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "f08c509e36a4e9a23e247bb25684e946"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "d7ffcd68884ada0564e1a446bbca56b9"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "8b923fad2ad9264a0ed5390548a30ad1"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "2c7b37f6d043ac25320cb75f56743c32"
  },
  {
    "url": "docs/index.html",
    "revision": "80a1b265f548b5d4687c7bf95e665add"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "b84b6ff179e7f6c90dd5b51c7ceffdea"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "243397af271c20ae9c46970b2649793d"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "1bcb111daf5ee240615f371d08b6717c"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "025db4cf07a65899041d1ff6f909128b"
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
    "revision": "0352ea105f662cb25a21c3f254679aaf"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "92f9e42a790a6b41cbc13d42a61bcd65"
  },
  {
    "url": "timeline/index.html",
    "revision": "54101c19893c7f96641a482f5c79b902"
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
