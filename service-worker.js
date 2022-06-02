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
    "revision": "64cfab99849109abb4dfc898618d14ea"
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
    "url": "assets/js/12.71ae2278.js",
    "revision": "b32bdff03f654588d62d3ba5eceae0af"
  },
  {
    "url": "assets/js/13.d8530c5a.js",
    "revision": "1419e11b9aa46eef11de9df2c41eea54"
  },
  {
    "url": "assets/js/14.af159e50.js",
    "revision": "4cc96097332cb06ad8a7683688460628"
  },
  {
    "url": "assets/js/15.f91fe200.js",
    "revision": "65ff057e7833757ef696bcc59f2a69c9"
  },
  {
    "url": "assets/js/16.8e9e4136.js",
    "revision": "261b6f81f1f0feb35408014a7148233a"
  },
  {
    "url": "assets/js/17.51a5db88.js",
    "revision": "53beb5bccad9900701838e683a9b8c0b"
  },
  {
    "url": "assets/js/18.c09b4f3d.js",
    "revision": "d3cf134eb74c2a4cc0c93f792e90d548"
  },
  {
    "url": "assets/js/19.a6b373db.js",
    "revision": "f10e7f44f9d94d929b64f18ea6063fc1"
  },
  {
    "url": "assets/js/20.636736a0.js",
    "revision": "94cf775599173e489225c40beba562a7"
  },
  {
    "url": "assets/js/21.5cd40bf6.js",
    "revision": "e154d66e77790b1d735f0c6c95988850"
  },
  {
    "url": "assets/js/22.38fa2a26.js",
    "revision": "3ea86fd46069dea9214a84aeea5cb617"
  },
  {
    "url": "assets/js/23.b0f6070c.js",
    "revision": "d1f95154574d39809b1b26b02546662b"
  },
  {
    "url": "assets/js/24.a936f87e.js",
    "revision": "b640c024dbce9a3eb60a1a5bceba2d2b"
  },
  {
    "url": "assets/js/25.3d54d94c.js",
    "revision": "835edf002c29b921c205fa24eb72d1d3"
  },
  {
    "url": "assets/js/26.f1ab20ba.js",
    "revision": "1b647e9cc1a936267040485541f6d007"
  },
  {
    "url": "assets/js/27.dc2d397e.js",
    "revision": "6f2eb0b07a1b41c800902faa24f12c2d"
  },
  {
    "url": "assets/js/28.b84dba7f.js",
    "revision": "ad91fc67ce7a8e8b02e0a2f05dd01e8b"
  },
  {
    "url": "assets/js/29.056f7e3f.js",
    "revision": "34a37e26a73cc075155badea9b4da169"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.38d61b04.js",
    "revision": "5572526477d9869b3a7e4d70aecbb590"
  },
  {
    "url": "assets/js/31.98ec9042.js",
    "revision": "c182e85341f67e369bff50dacc1a95fe"
  },
  {
    "url": "assets/js/32.9d765dd7.js",
    "revision": "fcf2b5e6d51a8f2ff55a27a6c68704ed"
  },
  {
    "url": "assets/js/33.cf290033.js",
    "revision": "73ed02754aa615a967a6d49950b6aceb"
  },
  {
    "url": "assets/js/34.ca6948e0.js",
    "revision": "4166db08d658255114a1554486643539"
  },
  {
    "url": "assets/js/35.049987b2.js",
    "revision": "108a6e02f052287f8e13231b1b463fea"
  },
  {
    "url": "assets/js/36.b9c81afb.js",
    "revision": "8eed3fa9dd959a7f4b9e4fcfa9aadc8d"
  },
  {
    "url": "assets/js/37.34ee6b6d.js",
    "revision": "1f3a42be6000fcce803968b49f35c830"
  },
  {
    "url": "assets/js/38.c1753ad2.js",
    "revision": "7ca75dbd612f92caa85bf293d6a4c38e"
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
    "url": "assets/js/40.7c214a1e.js",
    "revision": "c3886f56ec886132072d43ca76fa1ae7"
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
    "url": "assets/js/app.f8ca43f4.js",
    "revision": "3d6d55372ac6a9b1b155bbd4df18494e"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "5e87012237282a5415aded0e81725089"
  },
  {
    "url": "categories/index.html",
    "revision": "f3d5a8d7b30816acee7719e3d783d1d0"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "738a6f778c6b87678b3146d69b3e3cf1"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "87ac326c7f2329704693e768d2f84a14"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "2cfe8f4d415957fd2e683d76560f8a52"
  },
  {
    "url": "docs/development_doc/utils.html",
    "revision": "b8732911ae28bd62f320f337c47e4b42"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "569fd61f7b8de256652cd1ad179b6d9a"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "ac58ba2c4a5afc1bfc5623fd1419e491"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "d4539ba40d9a0e89985a41c7c0e623fc"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "7959119ae733127a21e39ebae2e247fd"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "2d4758c5cafef5941c37d8ca865a9be6"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "232059c07ed575a7f2b2b3d5421125af"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "841e4bf0775a47a51db859d79937a633"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "a50fa505cbd65183ff20d327a2b114f4"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "f1a5b4921d2f3ec95ef727828a993719"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "c96653c324a8bfc06c0b9a538e816465"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "0ba82cd183deb918a4d95b1201b18ca4"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "cf573164597ead90845bd060f733d880"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "bc32aca655caeef5e57650bcf542dd45"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "c5c6a5f9405e573366007feeec142532"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "5fe0fc11e23a9665abe1b5c703b854ba"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "f26723ed48b09503d8c579a6515951e2"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "a24a47445ab1cf00b273a9aa78840ea9"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "502bd24ec0d66058195d6c1a42997e25"
  },
  {
    "url": "docs/index.html",
    "revision": "0a213ca796b52ec301fa1b48f7b9525d"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "4e84f4d0aa69587eab9d63a6702f63b3"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "b19259e4147820ecb2c572063484692f"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "108bfb179aae6fab04b0b37e2eef4323"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "aeec145eb6d4561946ca7420f5c8dbb0"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "e92656b58b5cfc0717db2a5434a4011e"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "c41f18b36d847a05e387ae81fe6ea161"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "ada487ba48eb41aa31d407403a43b47b"
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
    "revision": "f7f0277b4ef06e55866a39543f8c15f7"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "8e3ec5a6be00f29a575bad056da6f905"
  },
  {
    "url": "timeline/index.html",
    "revision": "917fa86b8238e280473d5f15d514c246"
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
