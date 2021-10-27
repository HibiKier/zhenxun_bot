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
    "revision": "18325b35db14a3aa7c0439f8945492bf"
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
    "url": "assets/js/app.3dd7f3e0.js",
    "revision": "1e96dc117e320944533fa2264c394bb2"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "5412baa27f3fbe2a2ff286eb8dd44229"
  },
  {
    "url": "categories/index.html",
    "revision": "4489bbcdaecbeb9ef48aaff3dba83225"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "6e2b6c84c3071b3dd4c85f8b8a8abb4b"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "4748f5caca1c4fdd21bf898f38b371dc"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "49df7992f46a64113a7cd29b30f90eea"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "aeb6cd2608dc9afabcc818f00006c005"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "73ede8380818d9211f5d648977ea880b"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "4b05b2c5b5e2f8bbc8eadfa3a38dc026"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "a0993f3c054e7fe9e110d553761ea773"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "c6beae3cf87ddf0c70edbf4cbc40e656"
  },
  {
    "url": "docs/index.html",
    "revision": "1509881b33b82f2c07edacd847201a95"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "e02c0e465e11b5862100b20922081a72"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "86206bb716cbd949b2030fc761863481"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "030fa813c1fb2522cef4c43a23ddfd96"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "c8a35cb0119cbb88f5882531189c3fc1"
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
    "revision": "322625dc3584687ab1077ece15ee8f50"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "2738f00b4151029c716cf31d7dd6d5bb"
  },
  {
    "url": "timeline/index.html",
    "revision": "d05ffab1fee6fb9a3922da7a4ca8c68b"
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
