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
    "revision": "0a13eabc43ba2dab454292d570cef557"
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
    "url": "assets/js/12.1d4f5a30.js",
    "revision": "35958547cb888630faa7811f44453059"
  },
  {
    "url": "assets/js/13.8451af0e.js",
    "revision": "e1fb146e7ce061f732f06b56a5ec7b92"
  },
  {
    "url": "assets/js/14.2e6a1abe.js",
    "revision": "9caecbbc5fabfe841e961b774fc813f1"
  },
  {
    "url": "assets/js/15.2b9a871f.js",
    "revision": "eba261e082ac37ba10269b8523d6dad2"
  },
  {
    "url": "assets/js/16.103d6ead.js",
    "revision": "937834aed44140d42a5193faa19c6cac"
  },
  {
    "url": "assets/js/17.b857119f.js",
    "revision": "3934c40dd7139290ac7e2a957216b169"
  },
  {
    "url": "assets/js/18.f60f7578.js",
    "revision": "6e5181459bba755dc735362cbb36cb43"
  },
  {
    "url": "assets/js/19.14430ea9.js",
    "revision": "34714294501c5cb77a19609c732a6377"
  },
  {
    "url": "assets/js/20.0e2ca8c0.js",
    "revision": "df4ac0b2c57130f6ba5ceba7734d31aa"
  },
  {
    "url": "assets/js/21.b348b1ca.js",
    "revision": "a4e7f2a9a7ccdb03d9e22f8d5be23f99"
  },
  {
    "url": "assets/js/22.610c00ec.js",
    "revision": "ce42d5d66d9d38b8c4cdb655674e66cf"
  },
  {
    "url": "assets/js/23.d32689be.js",
    "revision": "5e97e38687e0990c01282690876de2a7"
  },
  {
    "url": "assets/js/24.ef9b81a4.js",
    "revision": "ae40e48c64dd742cf657c9d0d84a3066"
  },
  {
    "url": "assets/js/25.de3ae801.js",
    "revision": "175b8dabec4c3fa515758a65ac7ad04e"
  },
  {
    "url": "assets/js/26.81d4bbd4.js",
    "revision": "6df3551fa78418be55bd38cf778de3fa"
  },
  {
    "url": "assets/js/27.21564736.js",
    "revision": "b664c71914a3bf5d1b3eec596236d6d9"
  },
  {
    "url": "assets/js/28.3ec63c61.js",
    "revision": "b366abe06cc1d144ae1d7a6951610545"
  },
  {
    "url": "assets/js/29.df4e2748.js",
    "revision": "e8d4ee9afcd89080352f9adb30c4eeb8"
  },
  {
    "url": "assets/js/3.5a2c9393.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/30.11192475.js",
    "revision": "d3efb95b455846f12e2dcbe8d4c02229"
  },
  {
    "url": "assets/js/31.4216c4df.js",
    "revision": "7f35db44c01e4d3381846376b7235f55"
  },
  {
    "url": "assets/js/32.5bb15dc1.js",
    "revision": "0f112b804b210909810a7579546bd4b7"
  },
  {
    "url": "assets/js/33.a3392420.js",
    "revision": "771ad856977b51ce67c3642e39b5d155"
  },
  {
    "url": "assets/js/34.cfffee58.js",
    "revision": "99edb3f0a64944e36b0d5179392b15df"
  },
  {
    "url": "assets/js/35.b2927237.js",
    "revision": "aafb0e72bc5a753c1e3289bd9c68b06c"
  },
  {
    "url": "assets/js/36.b53e065a.js",
    "revision": "9110559a75e4cf577ad2f439268713e7"
  },
  {
    "url": "assets/js/37.06c06258.js",
    "revision": "2c00837379ec96b3a7cb0011cb891eb3"
  },
  {
    "url": "assets/js/38.562bd32e.js",
    "revision": "0bbcfbdff809771a5abf40c2d7bb37b2"
  },
  {
    "url": "assets/js/39.26fd4045.js",
    "revision": "41440555d48e60d1040dc5fd6e80a460"
  },
  {
    "url": "assets/js/4.7b2626bb.js",
    "revision": "1642b25041b4fce55d1447249497b0b6"
  },
  {
    "url": "assets/js/40.ad503b54.js",
    "revision": "59c384631930bb99a77434b707c9f369"
  },
  {
    "url": "assets/js/41.a972eee0.js",
    "revision": "e854c5ff381d28e2a38be2163d7da4bf"
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
    "url": "assets/js/9.edc7c72b.js",
    "revision": "55275f92bd9801e087a932b3259e7d8c"
  },
  {
    "url": "assets/js/app.cd2c2a87.js",
    "revision": "b9bb9ca85762cc7d2f9602606c9a877d"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "c5cc163d6bea5223c7e4d7b7fe63c00b"
  },
  {
    "url": "categories/index.html",
    "revision": "7b4a8f653208292e4143705be24279ed"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "4da5bf96d205566aaf4c46ba23ca0f02"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "0d6a49e8b7e92de989f4a71dbc7f3998"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "764374b1ea6c426f99502085938cf85a"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "9e106598baaf39ab25c8a525f607fbbe"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "aa88b12d61bc80378512e58edd21e00c"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "46a4013e8b5fbd0465423293b7eff254"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "caf2ad93d108319f171e06da77e663fb"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "68ae682becf47c8b37813ec0e3260bf6"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "206421d87e044df855af68067b780acb"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "bd6244043548586655a5de5b15ef7f89"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "480fd3d141dd69b1c81e387d6b69aabd"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "ab626194b44d1c74c4f20daf3663b7a3"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "5a287459132ecd44ce86f07775d9d87c"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "e0351aa8b98aa80b29af8c8eb39c31d0"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "68036d3b916446fa8d6b3ed10046e2e5"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "ba9961e17114bfec57b71e0576d4e4ba"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "584b2aca802960c79fd51716e6db7d16"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "a8c96bc3d599a7b125648b6850e52c51"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "38cad3ebcc75c43baa0e9f566fd4d457"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "818e5286ba6dc8b3404afca737b61074"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "1e36a95e21034f1d085587f934b5e134"
  },
  {
    "url": "docs/index.html",
    "revision": "a63bc596a5c99f63079001005d245bc4"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "b0755545ac08f94035006a8dc158c04b"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "61637c4ae5dc8bf5cbbaf9511bb13153"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "c91cd222de3f3ec90aa12fdd259fb665"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "949ae5d1a6b1d5c45b538223117b62c8"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "6b506c141ade393cc6a0fc137d0b2856"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "0d09011aaf8ebaf4b67a3389243a6010"
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
    "revision": "7751dc6fa8bfc039aa41ca530f92fe88"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "5d622f7b5fd89ccef28d3bc88691103b"
  },
  {
    "url": "timeline/index.html",
    "revision": "7fbe6ef90405b5c17d0484ef65d99895"
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
