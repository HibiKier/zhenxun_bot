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
    "revision": "5d0a43bae9a3b3c995fec3fe5244f81f"
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
    "url": "assets/js/12.584f99f3.js",
    "revision": "9f66cc5893abe091b0a6871a3545be73"
  },
  {
    "url": "assets/js/13.b4453581.js",
    "revision": "0f266bf502ae4762548b15c7a7d5a5d3"
  },
  {
    "url": "assets/js/14.af159e50.js",
    "revision": "4cc96097332cb06ad8a7683688460628"
  },
  {
    "url": "assets/js/15.d8c40a49.js",
    "revision": "8db7f53d5aba3bf0cbc8eef2b1972531"
  },
  {
    "url": "assets/js/16.1d3dce5e.js",
    "revision": "231bb840906b7853fc8f3624082c58df"
  },
  {
    "url": "assets/js/17.7dcf64a0.js",
    "revision": "f94ccb41a4820f4f614f7915bd403dd6"
  },
  {
    "url": "assets/js/18.068a6f2b.js",
    "revision": "b5717bb84c9b54af5ba4364f44d10e51"
  },
  {
    "url": "assets/js/19.eceb2180.js",
    "revision": "e2c7d833f16d8bbf04fde30a89cfba31"
  },
  {
    "url": "assets/js/20.c46aef55.js",
    "revision": "d878c413dd87c5f9db6972876182020b"
  },
  {
    "url": "assets/js/21.1e8c38c0.js",
    "revision": "4ca74390ce411eea69b0ead0961eee01"
  },
  {
    "url": "assets/js/22.1e79fd4f.js",
    "revision": "021a93963e8e27b53d9e39f5745d1d3a"
  },
  {
    "url": "assets/js/23.073a92a2.js",
    "revision": "9028901f370d75018230b8e54d9bd300"
  },
  {
    "url": "assets/js/24.35fc103b.js",
    "revision": "e78cd2d030e8884223173e003ef992f2"
  },
  {
    "url": "assets/js/25.3d54d94c.js",
    "revision": "835edf002c29b921c205fa24eb72d1d3"
  },
  {
    "url": "assets/js/26.613b81eb.js",
    "revision": "ecd479008906e43b4069123e5e73b1a8"
  },
  {
    "url": "assets/js/27.dc2d397e.js",
    "revision": "6f2eb0b07a1b41c800902faa24f12c2d"
  },
  {
    "url": "assets/js/28.826b40b0.js",
    "revision": "123a694fbf0586220615daba88eef40c"
  },
  {
    "url": "assets/js/29.932ce435.js",
    "revision": "5a51cf973c222db0e6c81846c52e7451"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.a7f3e374.js",
    "revision": "56a0234bd47d1cde81bd0fb0c43414ff"
  },
  {
    "url": "assets/js/31.f44d1221.js",
    "revision": "4cf65f7c317699b3171e97e3fdc3e9dd"
  },
  {
    "url": "assets/js/32.40ab5cfc.js",
    "revision": "0ea096296afc8ddc522314cd9fe2e99c"
  },
  {
    "url": "assets/js/33.57a69881.js",
    "revision": "5b1cffbe1815624f932cb8da8a66bf19"
  },
  {
    "url": "assets/js/34.860b3d9e.js",
    "revision": "fb0a7a9ca936c5fc00fb974015700020"
  },
  {
    "url": "assets/js/35.39f8816b.js",
    "revision": "8d5986118068741465139a75170dd4e8"
  },
  {
    "url": "assets/js/36.1bc64f69.js",
    "revision": "7c19bd0162c9bcfb4014c277a9426975"
  },
  {
    "url": "assets/js/37.990e3439.js",
    "revision": "679f027a3cae369b1695ccf0934eb1cb"
  },
  {
    "url": "assets/js/38.edf9df52.js",
    "revision": "66cfec8baed48bdbb74fe059fbac16dc"
  },
  {
    "url": "assets/js/39.59aeded0.js",
    "revision": "1cded8f8b553c60d698ac2ddff0bf47c"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.a2a8c964.js",
    "revision": "c8e13c0b0ca219d962f134ae97848b0a"
  },
  {
    "url": "assets/js/41.ef8dd692.js",
    "revision": "704ab901dd23f90bced4519908efdc9a"
  },
  {
    "url": "assets/js/42.e7ffc620.js",
    "revision": "5344d98619b69160e0c5b3beb70919e9"
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
    "url": "assets/js/app.94912d29.js",
    "revision": "7bb57eb50a2a5374c4cd334fe100979d"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "e54a586a9c8abca76beec0caae201ffa"
  },
  {
    "url": "categories/index.html",
    "revision": "6df0f07ad19b1d2f4dc2707e14c688c4"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "b1b45b28d41ca5d0546c623d71a72baa"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "de4c74572dc971543c5cee2c92ffec4f"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "99f788e371542cdc1dd26ba53266b10d"
  },
  {
    "url": "docs/development_doc/utils.html",
    "revision": "04e46c0bb2ac4ea022e5f656030a30b9"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "26d23547d43b17ac2afe066a96f52b3f"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "d650fab7eb07f0363858a01b229ec440"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "335fcf45daa2635def8aeb805fac38b5"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "ab39b340df022dff95dc4a1b40fa014f"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "e3c654eb57c7e5aebbc3789ebd674988"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "f1a16c330a916f48d0b198ee2eb0fea6"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "63fe664c82be3ed786485c135c02aabe"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "29ba6ad4ebe40aeda4d6398ee05acb4f"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "17d0a8926a7888f8f745c33e9ceccccc"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "b1139aeec89b1a810f172eb5ac6d0ffc"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "7bb5e6a52d75a33ef418185f1b74ce47"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "6567298fdaf1976a56f72b85d74f2749"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "f695c664fe2e1649d8414714b49874d3"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "ef2090a6a6e693be772b0f73c7aadb33"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "37b0590a2d88e5bf4a3a487b0f8effc0"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "7918e0e62f8165bf96a158e30cf8c5f2"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "5bcbbc66343bc9792a2b4ea493ffc11a"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "7a343607dd869ed7b2bee7755cdf69ff"
  },
  {
    "url": "docs/index.html",
    "revision": "c95546ed8efd663a9cb0760344c33834"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "2f4833cc654190bb95e11c173719f64b"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "fd791fea766cc69acdd46a1ccf92c641"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "357ae7ddb983ddff93e8210fbe95c878"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "e28380edf0ce6c39a5a6e7d32948fb4e"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "72d927c2a29345fc607fe1b4601fde9f"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "31b45deb641e4d1b0dc3d142dccc56b3"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "291fd083c0b14717f604e818494db3ef"
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
    "revision": "0338897da351b0b28420b27d9f8b0762"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "3e9ea8b575a17c5de47bcaa940171fe7"
  },
  {
    "url": "timeline/index.html",
    "revision": "06a2179582d836962ba63e41a164a370"
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
