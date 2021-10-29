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
    "revision": "88d7859a1840fe5b4328ae340ad87c0a"
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
    "url": "assets/js/16.8af4520c.js",
    "revision": "9e1bf8ee492b7d61b151a765edbb7957"
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
    "url": "assets/js/19.114d73de.js",
    "revision": "f21ee0d10f5a6f9faba351c3eb0942b5"
  },
  {
    "url": "assets/js/20.0e62c3cd.js",
    "revision": "5e90cbf20ad64b46757f3fb7732725b2"
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
    "url": "assets/js/24.ecb2d6fe.js",
    "revision": "fba0ae165c7bb44dc82071a2a84832aa"
  },
  {
    "url": "assets/js/25.7cb3a65c.js",
    "revision": "cc325666ed55d74b53560ac4685f8d74"
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
    "url": "assets/js/app.06dc8b82.js",
    "revision": "1a1495af8e9b670ae55f5ccdbb76aaf8"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "76e0db2eccb228377ec827a26569487c"
  },
  {
    "url": "categories/index.html",
    "revision": "81dafed56ed0780c0cb79247be7794c1"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "98b25aff61f0a3b24a6ceb3d527a5ccc"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "56ae9d687ee3591bc7117d99ad254d87"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "32e5b6fe94c82c3e6feeea8de46995da"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "c353b6611325d577b0e407b8ce4ef4c3"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "90dda102adf27ad2b2a0b5d488aebcd2"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "fd12feca58f1b0e9b67b9f3630f3f0f9"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "851c06d28e5a3414dbdef1b0d57f49de"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "5a3af92a1cdbed678c3fb5e91024c576"
  },
  {
    "url": "docs/index.html",
    "revision": "d5bfc75e13ba48cd89b56fd093888c85"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "244c7fad79336ad23f4881098403034d"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "a27ed7928cc804e1a6b356b6bc7a9d68"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "928a6caa922177aa1127aeffe2e6e401"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "c0863bb046f2ee4c8569cb7c3362f4a7"
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
    "revision": "2df49551d81bf5860c2ea2555ddf552f"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "58555d1a36f5ea60f593daebd932c425"
  },
  {
    "url": "timeline/index.html",
    "revision": "6d137f9c134988d05d1546afebb8878e"
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
