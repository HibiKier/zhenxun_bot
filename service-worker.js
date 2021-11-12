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
    "revision": "1771007830c787e6d222ddfc49e27cda"
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
    "url": "assets/js/1.b6369614.js",
    "revision": "376d5b4da5fde3616c10c1f2255ccfd7"
  },
  {
    "url": "assets/js/10.43e159f5.js",
    "revision": "44d4a30d2ae0c1cb936c19d5a827a3b2"
  },
  {
    "url": "assets/js/11.e5d78693.js",
    "revision": "a0752b097c88ce70b3a73f100e3fbda4"
  },
  {
    "url": "assets/js/12.6e193a7a.js",
    "revision": "cce0737971f3b25c68e8ca644c44c9e7"
  },
  {
    "url": "assets/js/13.12022e1e.js",
    "revision": "f54f8760a522b111dae7d5ecacb0b7ab"
  },
  {
    "url": "assets/js/14.b90ba65e.js",
    "revision": "c44af9326072f791eb015467a7444625"
  },
  {
    "url": "assets/js/15.aba856ed.js",
    "revision": "f33bdc3a92fedc3aee980d1f777b9774"
  },
  {
    "url": "assets/js/16.a9b74e60.js",
    "revision": "69602052fad8c9cc8637f280819a37e8"
  },
  {
    "url": "assets/js/17.27df5e56.js",
    "revision": "51a613012bf4ab90e4ac8342dcc78c83"
  },
  {
    "url": "assets/js/18.0c85f582.js",
    "revision": "343e7511f457da50fae198ab30917938"
  },
  {
    "url": "assets/js/19.f9b33e48.js",
    "revision": "848dbd6b62979779f81bc241d8b6f7f0"
  },
  {
    "url": "assets/js/20.a1c9d186.js",
    "revision": "4eeb15748ca11273cbdc9f9a6ea9148c"
  },
  {
    "url": "assets/js/21.f9389c7b.js",
    "revision": "9cb29d35248a55a0868ebbd0f27e06fb"
  },
  {
    "url": "assets/js/22.893a8c64.js",
    "revision": "41d8281ae7c46e6e2b7629dfcff5519d"
  },
  {
    "url": "assets/js/23.6af6b4f9.js",
    "revision": "e0c209a07fb1ac44d32a67ee179c2850"
  },
  {
    "url": "assets/js/24.a672ea31.js",
    "revision": "de396361070f8bcf40c9c332bd8c4761"
  },
  {
    "url": "assets/js/25.67e0f6d2.js",
    "revision": "79eacd24390d68977af526971c9a1985"
  },
  {
    "url": "assets/js/26.48682e1c.js",
    "revision": "88ffea5aaf59d87c75264ec0bfbf3ab6"
  },
  {
    "url": "assets/js/27.5b7824b3.js",
    "revision": "286edb942ca62047bf2c1c2a9b8e3fcb"
  },
  {
    "url": "assets/js/28.60139aec.js",
    "revision": "8cd85ea59e150e6edbf4da2bba773b41"
  },
  {
    "url": "assets/js/29.c9aca793.js",
    "revision": "b975561ca45e7793b576bb3efae0054e"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.a40fb080.js",
    "revision": "5bf084653f2393315e1ce746f7d4b255"
  },
  {
    "url": "assets/js/31.5cbc1eef.js",
    "revision": "45073b8c843bfdc099576095c4a133aa"
  },
  {
    "url": "assets/js/32.70f0043b.js",
    "revision": "b8948fddee892718b8417a549bb1ac54"
  },
  {
    "url": "assets/js/33.df55760c.js",
    "revision": "99de04199b9c61073f8629931def5c7c"
  },
  {
    "url": "assets/js/34.b2127191.js",
    "revision": "40cded7a4d3484a10bd879e54ee2404c"
  },
  {
    "url": "assets/js/35.eba0ebe1.js",
    "revision": "a071bf55be84e7813436ea664e9357bd"
  },
  {
    "url": "assets/js/36.1123bad6.js",
    "revision": "995b4ca5d3b2d0f59ede4919f077a6e3"
  },
  {
    "url": "assets/js/37.702d749a.js",
    "revision": "c513fa20a40468effc8b12c25e7709e8"
  },
  {
    "url": "assets/js/4.a3d0177f.js",
    "revision": "67138a1fdac208c38513b7004e1305eb"
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
    "url": "assets/js/8.e618920f.js",
    "revision": "5530f0cf9450b123cfba81c7b11ed6f4"
  },
  {
    "url": "assets/js/9.0ad80411.js",
    "revision": "c8f91e10be5a5f7b57f7ec35d954a37c"
  },
  {
    "url": "assets/js/app.a68edc69.js",
    "revision": "684997e90f5ae0148058f39f7be61427"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "732897992b417ede28c1f80520027e84"
  },
  {
    "url": "categories/index.html",
    "revision": "65d11e18dc44e66d7975d4aa2a730abd"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "01836a6f219ce34337d7bac61fd13c12"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "99365631b5c7edbb6448252806c71f8e"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "64c76acd2a061c15302784b988b12f9c"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "5587f14e5ddc226888e056b2b3e7f484"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "272e6fbf6314964eaeb3f411dbd8ca0e"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "cbc0583f5368cb5756dbd3d323298c81"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "dce717fc1ba7c43a5964db8c80bc75c6"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "07bba9f4ee0de04d38761fce09127797"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "efa46e880c1d8bcf1fe81683fbe1cc1b"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "d4549d7d2543458ea21846577cb8eec5"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "3a18967303b91f52eb9244a717145039"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "37b51e7c96787a1c31aa894d8833fef5"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "868669a4c2a4c7d343bcf365f68bd576"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "7f127c6e1b22d7cdb6e12faf39aba7e1"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "915716637d5bd7601f1e4286343f3c79"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "f619cb1e1d822fa0339f87ef1e10288e"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "3963089351138a9f18d89961b3dda4ca"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "3859d0c2aef526e9c48efe583b920d02"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "c328ec2dcce904caa919f3af072f867f"
  },
  {
    "url": "docs/index.html",
    "revision": "3ba28cf145855ea4a78a1c63d1580dd9"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "6187679b2afc7c71290e4f9e9b26f834"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "0e3cc28f511150e7dafc2e015ffa107c"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "daf68b63f6bc487e329c8843fd21a971"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "80e6e5c9c3cff2a1a02cec30c5bd37b7"
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
    "revision": "d187770741d780ce9913bb17d3fd282d"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "c1122018bf8559f254a9be7e536ddc65"
  },
  {
    "url": "timeline/index.html",
    "revision": "d92b1a1b07a4e3a6bf7812c4c9c390c8"
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
