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
    "revision": "c06a66c568adcd9c1b7d26c960abc57f"
  },
  {
    "url": "assets/css/0.styles.3af13d03.css",
    "revision": "3cf231b711ffdd04ad7f9a9b68414e7b"
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
    "url": "assets/js/1.5a85ab28.js",
    "revision": "3e725c01393322b28b3cc706eb8bbd58"
  },
  {
    "url": "assets/js/10.c36c3cdb.js",
    "revision": "ea64c20ea854e58bb44642636538e76e"
  },
  {
    "url": "assets/js/11.e9b0183e.js",
    "revision": "10f26e1177e8231499023ce9c00318cb"
  },
  {
    "url": "assets/js/12.1800d2df.js",
    "revision": "19b38f3c4180af348b374ca74c34d6e4"
  },
  {
    "url": "assets/js/13.d8530c5a.js",
    "revision": "1419e11b9aa46eef11de9df2c41eea54"
  },
  {
    "url": "assets/js/14.24008e44.js",
    "revision": "88ed3fa6c64519ffb3f8e62c7cae405d"
  },
  {
    "url": "assets/js/15.23c80f65.js",
    "revision": "bec226092c83bdaef5102097d6c4ede5"
  },
  {
    "url": "assets/js/16.15869a4f.js",
    "revision": "e654b3699b7db5d5fe5e87b494adb002"
  },
  {
    "url": "assets/js/17.829f12ae.js",
    "revision": "cbcdb1a7e19086e8ec960adf6aa5a2de"
  },
  {
    "url": "assets/js/18.6bd6ce1d.js",
    "revision": "874708ea5aade9f34ece95c7cb419c82"
  },
  {
    "url": "assets/js/19.a6b373db.js",
    "revision": "f10e7f44f9d94d929b64f18ea6063fc1"
  },
  {
    "url": "assets/js/20.c46aef55.js",
    "revision": "d878c413dd87c5f9db6972876182020b"
  },
  {
    "url": "assets/js/21.b8203c70.js",
    "revision": "d7b66d00ce5ec639043518f4a22531e0"
  },
  {
    "url": "assets/js/22.790b0c11.js",
    "revision": "188fa53afac1518348c5f3cebe7d30f8"
  },
  {
    "url": "assets/js/23.b0f6070c.js",
    "revision": "d1f95154574d39809b1b26b02546662b"
  },
  {
    "url": "assets/js/24.c91789ca.js",
    "revision": "5c550e8c58047079d12081c621ab928a"
  },
  {
    "url": "assets/js/25.3d54d94c.js",
    "revision": "835edf002c29b921c205fa24eb72d1d3"
  },
  {
    "url": "assets/js/26.cb6ccb26.js",
    "revision": "4744d194544eb56e186b89c22635975c"
  },
  {
    "url": "assets/js/27.002fdb3c.js",
    "revision": "4a6a84e6c30eae525400b3f58ad0cc5d"
  },
  {
    "url": "assets/js/28.7b9fcb95.js",
    "revision": "8d45254690b865fa707266cca5b2def1"
  },
  {
    "url": "assets/js/29.b8e92b13.js",
    "revision": "ce5336213f23efa586664cf7a24668c2"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.f43d9823.js",
    "revision": "c677f7208f92c70fc94f2d9a9a631c02"
  },
  {
    "url": "assets/js/31.5cf8c251.js",
    "revision": "ff77847df9bdbce2a81ab8cb6436fd56"
  },
  {
    "url": "assets/js/32.d911a2b2.js",
    "revision": "5ff0c4230d6996b752ba3c546db648b8"
  },
  {
    "url": "assets/js/33.57a69881.js",
    "revision": "5b1cffbe1815624f932cb8da8a66bf19"
  },
  {
    "url": "assets/js/34.3ce350da.js",
    "revision": "a6580d09a9d50821b2d1b77bb96977dd"
  },
  {
    "url": "assets/js/35.ca6a4de9.js",
    "revision": "cdfe34d2844ccf3bec77a60dab797af5"
  },
  {
    "url": "assets/js/36.1bc64f69.js",
    "revision": "7c19bd0162c9bcfb4014c277a9426975"
  },
  {
    "url": "assets/js/37.4536ab5a.js",
    "revision": "c612e31fe88862330324273a0b1ac50b"
  },
  {
    "url": "assets/js/38.edf9df52.js",
    "revision": "66cfec8baed48bdbb74fe059fbac16dc"
  },
  {
    "url": "assets/js/39.1d8292ed.js",
    "revision": "c51d0cb99de46fba9d9b589f197a2e5c"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.a078069b.js",
    "revision": "252255aef01d4a1741ed8277b3df7bae"
  },
  {
    "url": "assets/js/41.ef8dd692.js",
    "revision": "704ab901dd23f90bced4519908efdc9a"
  },
  {
    "url": "assets/js/42.a3dd40b7.js",
    "revision": "76224336aa6bbaaded55aff2f461611a"
  },
  {
    "url": "assets/js/43.19f9e3a1.js",
    "revision": "bec2828f9b22385c26808b4c3b76a9fe"
  },
  {
    "url": "assets/js/5.71556fb3.js",
    "revision": "d259aa4991e4571fe7518f3671248ccd"
  },
  {
    "url": "assets/js/6.100e6bd9.js",
    "revision": "4ee9151e86f1690b6fa48777b76a5c7d"
  },
  {
    "url": "assets/js/7.3873c60b.js",
    "revision": "eedf755734c240c423164a6b4d25663c"
  },
  {
    "url": "assets/js/8.6dce9ba3.js",
    "revision": "161c1d689495c7bda88f26753c3ee481"
  },
  {
    "url": "assets/js/9.d9e9496f.js",
    "revision": "3b131d97c515f1301bbc1ebfe7732ab9"
  },
  {
    "url": "assets/js/app.14cfc4a4.js",
    "revision": "cbb153faa41b4bb5d3573163692e70e3"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "82cb77ce97b1ef9765392a9220ef1de0"
  },
  {
    "url": "categories/index.html",
    "revision": "bda422665b28c99283b6ba457459954f"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "fdb160e22dfdedbc194afd87d2925a6f"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "e109d991f7d3e7e750ffa4a0d0a80a51"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "27dd217bac81881e61fe3573cadc86c1"
  },
  {
    "url": "docs/development_doc/utils.html",
    "revision": "99cff06de268312bdc3bd372566f8572"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "4fc0da619e96990b6fe67968bbfc5f6c"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "53cc0b99c4a7011ceec4ddac2c2d5e72"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "ff34790cf00ba2e69b51578f56ca78a5"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "0560bf8ad600f3fc15ede0d4a445cc38"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "aa1107e8713ed56648c2d46cd0efa594"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "e44816487acdc13526b83a23378be7eb"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "750197cb2b513ae2f6e45d8dbd62f50a"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "05b645e56bb76d081f9d2d229aebfd85"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "015e0c462e83476f06a05a9e56f72ca4"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "841112c149955180fd064acc9d73542a"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "78887c0ac203f6ba9bc0d31f4c095af0"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "7957eb4cc86742e1ae966a88d8534852"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "d8873293f5a53f12e8def009294c0792"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "1a20b69fd4b6c2fe1c4140c1b0dcbd98"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "7419b2d2619f0aa04220e3d866fa7ba4"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "6337611ccc7ebfea8c3f057d2c1f2e3d"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "8c780a8d346adba0f83f719d6d4e12c6"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "7eff9b6b4e42f619f2291c96e8a6e7c4"
  },
  {
    "url": "docs/index.html",
    "revision": "a3faea8dcac4cf19fa3199ecec844e18"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "bf930551e5cf135ab22da89a97dc0cd6"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "b00a34f1aae556528a8630099b18192c"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "ddc4e2dfd1c537dc60b679cccdd560a3"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "dcba3d00a3e64a9355e14ee89281e909"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "55686d80095d505e7653f30182217c7f"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "17c425219c5a09f0687a33b9a84caab6"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "8dee0995d8877e224cbeeaeed8df45e0"
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
    "revision": "bd36054355798ae45eaf20db16c62f47"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "6abce6b92db54d98f5b1267a658aa5d7"
  },
  {
    "url": "timeline/index.html",
    "revision": "2abca8dca720ef2c9d1e517aed704644"
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
