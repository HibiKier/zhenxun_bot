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
    "revision": "cf8cbd13133ad6ec8ecc76fbc4255bc9"
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
    "url": "assets/js/16.6496676d.js",
    "revision": "fe80f34e141e4732d1feeadad3fc4088"
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
    "url": "assets/js/19.ad9720eb.js",
    "revision": "993229499307d70606e26eebbbd4c433"
  },
  {
    "url": "assets/js/20.482e5b33.js",
    "revision": "6c9a999f33a78ed20b0e97002fe12cd2"
  },
  {
    "url": "assets/js/21.9e0ba6b8.js",
    "revision": "ed14252034f3f87aca614476be8f2474"
  },
  {
    "url": "assets/js/22.6218a7fe.js",
    "revision": "26c3635f0e506d4230ebf2b9328badaf"
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
    "url": "assets/js/app.7eab428b.js",
    "revision": "08e620d94bebf33b106291298eb3a8b0"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "f5540a152f826c9a06167d753322fb58"
  },
  {
    "url": "categories/index.html",
    "revision": "390b17b2a401dca28b0ee0407cdd217a"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "7e707242e54c7d990763586ad43b8504"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "84db4b051ad0e5b36424e28fa7ac4c22"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "80b6834c36308edeab1b855316ad3fc6"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "df13226bef6853da9ee40872fe8e4376"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "f1989cebc7e59525116fbf899b3add0e"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "2a09a7b0ae534103dc6c4824b403d2e6"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "01a6ab3d3d069f3c3a3f8dd8e2a843f2"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "b1b05f7f908869682a26f8596ee6aa38"
  },
  {
    "url": "docs/index.html",
    "revision": "5004ad98cb2245463a02af8f2982af9b"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "a847b71b166c0b3d38396c90cab5420e"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "fcbe1a48d29cb9c8d9a67fd71c42a103"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "227ad32a614b1091c091cfd62e6c4880"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "b00a349b8fab81a0a260664b4089055a"
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
    "revision": "d24b42b89b437d6480386fd2e06ca102"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "d29dda4b20550919eef9a53d27b4c43f"
  },
  {
    "url": "timeline/index.html",
    "revision": "61048ae4658ddc28cd71a36fe93ac668"
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
