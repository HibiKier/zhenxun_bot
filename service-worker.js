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
    "revision": "19e6f6ac56f8bc78b626965bed6c6659"
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
    "url": "assets/js/11.57ced948.js",
    "revision": "ca44b101add166c6012feb8b68628c5f"
  },
  {
    "url": "assets/js/12.fdaa7ffc.js",
    "revision": "1a47e6d96c5001196b94092a3c508637"
  },
  {
    "url": "assets/js/13.12022e1e.js",
    "revision": "f54f8760a522b111dae7d5ecacb0b7ab"
  },
  {
    "url": "assets/js/14.0bf8bf0a.js",
    "revision": "a345f2109901e8ca1037fdbe0fda2c4b"
  },
  {
    "url": "assets/js/15.aba856ed.js",
    "revision": "f33bdc3a92fedc3aee980d1f777b9774"
  },
  {
    "url": "assets/js/16.ae4d64e1.js",
    "revision": "06624ec7c3afc0211bb4f639d10b09e2"
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
    "url": "assets/js/20.6daf677a.js",
    "revision": "77adb7004040d20dc9646cf6a18a9bab"
  },
  {
    "url": "assets/js/21.e709c1f6.js",
    "revision": "751908ef76ef4a1083069880567bbea6"
  },
  {
    "url": "assets/js/22.66fc9431.js",
    "revision": "fdd49311b19c269c8049bcb19634b86e"
  },
  {
    "url": "assets/js/23.9a927d93.js",
    "revision": "b57776229e15ca4ee31e035baf1c0784"
  },
  {
    "url": "assets/js/24.64cee759.js",
    "revision": "98713864d4607ac796329ad9540f3fa8"
  },
  {
    "url": "assets/js/25.d96bb949.js",
    "revision": "3779f6a70cfde313ff3b9bf1b28b0fcd"
  },
  {
    "url": "assets/js/26.f16d0fca.js",
    "revision": "f5301878c618ab5e6c26741b9fad2f47"
  },
  {
    "url": "assets/js/27.707bbdc7.js",
    "revision": "38839f9dd011b27900aff285c639e152"
  },
  {
    "url": "assets/js/28.2d4acfe4.js",
    "revision": "f5dbe3b868ff0ab9a0d1c5cd89a09acb"
  },
  {
    "url": "assets/js/29.ee289f0e.js",
    "revision": "96c068b7c256c8c9546bc2ba2ea0c8e9"
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
    "url": "assets/js/31.e6a9f747.js",
    "revision": "55895d89595d42264800762941b68224"
  },
  {
    "url": "assets/js/32.70f0043b.js",
    "revision": "b8948fddee892718b8417a549bb1ac54"
  },
  {
    "url": "assets/js/33.9852f9b4.js",
    "revision": "e8da924983a9884d292431def0a76708"
  },
  {
    "url": "assets/js/34.5ab00012.js",
    "revision": "614ca4e60ea70f77aebae5bf0ef1e54e"
  },
  {
    "url": "assets/js/35.6e0bc0a3.js",
    "revision": "d04b8e9ab20537a5305f77f40e76f253"
  },
  {
    "url": "assets/js/36.25793f58.js",
    "revision": "5409a171c99d5a549652690da7e096cf"
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
    "url": "assets/js/app.5fdd1f3e.js",
    "revision": "295bc9da5bac5f4514f6979416b5ee1a"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "b21a254ff5131dfdb0415e37f5441ad3"
  },
  {
    "url": "categories/index.html",
    "revision": "5b923c1be4c6f4aff9ac22d441e21e2f"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "5004f4666bc85c3a44a6b088941e49fb"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "94d88daea0b6395870306f04c7aa6863"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "c100c2456f592cd9ecd5eb308b7703bd"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "d49bf06cd537784eb93517c2fa2bbb80"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "1ab535bb32abf3a5eb857639d50d3ba1"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "3aa50b9290414cd4346f83b0718a7b07"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "93ad439f875e6a1bbee86c000e23e8ac"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "5919077a390a1a7186c53c41fc161466"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "ff2da089b6f8ea7d481c48a9e0a416c3"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "4e1f3d9340023b128158afbf362d8e3f"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "4b469298f31f85e57f69f0e2234ef15a"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "7aff12398918ef479b99b33894472f99"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "0fde3d59fa67dc62a37f8d519412a3bb"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "f556ee98506165133883c107238204e0"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "64e737af21e7684f9807e8fc48f0be6d"
  },
  {
    "url": "docs/help_doc/public_plugins/plugins_index.html",
    "revision": "c8dbbb4d0c8f80444ffc8b255fecf7a1"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "e3b06b3c2c872cb12516067c1eefe313"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "546b85c06d25b8c6f5a9108c871101a6"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "b519bfb55c790a44b8d19a18953d77c2"
  },
  {
    "url": "docs/index.html",
    "revision": "eab7773f2bd641b22d4f31c5451d4068"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "bd89910f12c91c34ad7ae4c6d9a26561"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "6eb21860a8a6f353c3a8f7a3d85391d3"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "b7dc0663656e6e7726257598fd8c39ca"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "62504025e8dd97bab98e0e84ffd7d031"
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
    "revision": "2435e01ba65fc4575aeb8f98a7e1d43d"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "7568b972f20b626d800e77cdc0169ec4"
  },
  {
    "url": "timeline/index.html",
    "revision": "695392dc9686acce0dc472b38ba15715"
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
