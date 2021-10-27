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
    "revision": "6bfcff3b71b535917b6bbbe494db5208"
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
    "url": "assets/js/17.ed04f4e6.js",
    "revision": "230cd8cd3a0f63e55d860cc9cbb7b0c2"
  },
  {
    "url": "assets/js/18.be819115.js",
    "revision": "57bed4d4eec141add8424c6c1b674924"
  },
  {
    "url": "assets/js/19.3eba5c5f.js",
    "revision": "4cfa7bef8c27fa758a6ad22409b23938"
  },
  {
    "url": "assets/js/20.7abba640.js",
    "revision": "089cc66b57cd37c56737b908e5f24550"
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
    "url": "assets/js/app.c4197360.js",
    "revision": "b270ef200b6ad9f9577b9690e9c42dd1"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "29235ebc9d1c23758a93206c291e3958"
  },
  {
    "url": "categories/index.html",
    "revision": "1db3044367e286cd46f5613ee45c8896"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "fa07f63d43b5fe8091bc63a0b06c40f7"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "1649f249cf1c92dfcfd57b0715a2e022"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "74aaf91c78a9fa9bc7a949e291fffcf1"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "5875a2e1d24c6c3c660b55e92f728ada"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "28a1bfb3127dc4aa37af27e29c066ea3"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "74c19a2ff9d43f91d15b40d0ca12d326"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "ee54727161a6daaeab2713b0f000ac4e"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "59c133d0a5fcfd97e0152d319422b0ad"
  },
  {
    "url": "docs/index.html",
    "revision": "2b71038caa4d30d06c332774f3be56b9"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "c33cd7f9044dfb5831b1f1586924e24a"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "d4b8fc69bfe5644d81c70e01414384c6"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "321ee383b8e796401af9b0df252c3291"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "1ebc6f33e0605154e4f5e0555c3a85a9"
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
    "revision": "1875245cd657b88e9082a56eb0872e95"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "f99db27d9cac776524c5fa87bc7cbc28"
  },
  {
    "url": "timeline/index.html",
    "revision": "f9983e9539a352a0c5762afc9d03ce1c"
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
