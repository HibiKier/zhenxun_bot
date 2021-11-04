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
    "revision": "81f1f176b09da3950c91ab8133f7dbf8"
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
    "url": "assets/js/11.88ddc2a0.js",
    "revision": "94966e750172657b37310dc83d2de1db"
  },
  {
    "url": "assets/js/12.54f32049.js",
    "revision": "bf5bfcf667dfe6d0be0d7382da21f568"
  },
  {
    "url": "assets/js/13.9843efab.js",
    "revision": "000907765f40c299e264139cc6645d29"
  },
  {
    "url": "assets/js/14.5826df3a.js",
    "revision": "3c90597ea2770a3ab4b684d42fe21902"
  },
  {
    "url": "assets/js/15.478e89fa.js",
    "revision": "f1fcc7fc2128dc8a6430e86e3d272862"
  },
  {
    "url": "assets/js/16.a812ab0a.js",
    "revision": "87f6df616f3e4930566e1cc40294d918"
  },
  {
    "url": "assets/js/17.45ea6a1d.js",
    "revision": "190fe38863648f0b4d971eaa71e96a3a"
  },
  {
    "url": "assets/js/18.69f5ddba.js",
    "revision": "8a67d1255d077102f7eb264c35a3355a"
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
    "url": "assets/js/22.cade1488.js",
    "revision": "1ef5625eabaa50bfb45c97c2bfd95686"
  },
  {
    "url": "assets/js/23.9cb16aa9.js",
    "revision": "d0703ab03c3e36126d3fbeb4c76cb7cd"
  },
  {
    "url": "assets/js/24.cacdceee.js",
    "revision": "90cd09585f62cb6390631ef6585b763b"
  },
  {
    "url": "assets/js/25.d53d3b3e.js",
    "revision": "d96667a7159901e93b0dec2fad2930aa"
  },
  {
    "url": "assets/js/26.239e7b03.js",
    "revision": "69be9553f1f5a1f11086b6b19dad6254"
  },
  {
    "url": "assets/js/27.129261d6.js",
    "revision": "99a6a753c84b27c2b5f73862d953e307"
  },
  {
    "url": "assets/js/28.25c7b1fc.js",
    "revision": "5f66bdfb8df27c05b0c2f78396df8cba"
  },
  {
    "url": "assets/js/29.f6574ee8.js",
    "revision": "8142c6ec220d8e8069a74834d365f4b6"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.bad36ccd.js",
    "revision": "b3342df9fefbd4a6a9e72124fc4a3d10"
  },
  {
    "url": "assets/js/31.01b5a9bf.js",
    "revision": "101c9179622c9a254122ceea3d8f343f"
  },
  {
    "url": "assets/js/32.655f94b9.js",
    "revision": "ce694fb732fc1e731f17c51bd6a76649"
  },
  {
    "url": "assets/js/33.ce8dc3c1.js",
    "revision": "a3fb1c4ebae71f1ff6d89810084ece9d"
  },
  {
    "url": "assets/js/34.8f3b03b5.js",
    "revision": "3d39620b4eeac5a590f724b1d824bcc2"
  },
  {
    "url": "assets/js/35.e03aaf1f.js",
    "revision": "0a0c5575819816330ad77d8ff5248c5a"
  },
  {
    "url": "assets/js/36.29948e38.js",
    "revision": "45fe4939f16890ebfd75bf2365b637f7"
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
    "url": "assets/js/app.94a07a1f.js",
    "revision": "b690e9556aa1b0c715938a232772ca2f"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "097a484203d09088a893e7a761330c4c"
  },
  {
    "url": "categories/index.html",
    "revision": "5082a704b07911595976e86b41d5b04b"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "4f3d1d4f287a3d1c09e0090aff56c855"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "1db7db0746a51aab3e5eebf2571dbc5e"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "5ccf1e62b6667a88750607d240485c2b"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "76ea3f8d3a8e29a1592cfa29940d1d6f"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "40a3a834f755ee719a44e97807c6e36e"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "f4335880a41c77808a8c47af89631638"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "8102faee5f3f91029ea7b134a3e8c93d"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "02cc4b037621deaadf37f20163f6dfeb"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "e3dfae672269650d2c0806e83c0460ac"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "0644f6a12007694e36fd8b9b3ae68a5a"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "ac03b042ffbc8285e5fd6c277cdffc09"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "e1897713fd9585672dfcafb35487baef"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "d7ae31ca0eef330eb9a72d7df1a2a7a4"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "f102e493837ba35de053ee6b9cefbca9"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "a3ed1b8774a489e03c52bd3d194a8a89"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "dcfa3233e383acba49f7a87e02bcb819"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "5a9914cb6665c2551bad48f8fd438003"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "7577a274082dffdbe05e1b8a9416d992"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "f5d002faca1343d956e264367b332c27"
  },
  {
    "url": "docs/index.html",
    "revision": "2c0d6ef8d7071b375524181a1e54c5d9"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "5a0bf3ded38e4f998492f2519df83374"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "11176e97f94a970cd7007f23cd39ef75"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "936511d193c6ce8f0fb2a4310d0e8be9"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "7409f83f4f2a2a1e121e4409d459aef2"
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
    "revision": "35f62309d24db45711142321073c35fc"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "aea834aa9a0e00cab9c8a5d9aec66ced"
  },
  {
    "url": "timeline/index.html",
    "revision": "da1a070aaa1bd0739e997c58e2a7c756"
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
