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
    "revision": "2d338bfee6ab2993928d68f185d8fc20"
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
    "url": "assets/js/13.b4453581.js",
    "revision": "0f266bf502ae4762548b15c7a7d5a5d3"
  },
  {
    "url": "assets/js/14.7e39a8ba.js",
    "revision": "40c99b378b3c08b8ea191170af034a13"
  },
  {
    "url": "assets/js/15.d4ac1565.js",
    "revision": "6705e69d1a834a6ac301afdcef5bca7b"
  },
  {
    "url": "assets/js/16.50decb90.js",
    "revision": "b241af27e017b24788bb829c91a709d6"
  },
  {
    "url": "assets/js/17.31da30d6.js",
    "revision": "7ce9a3700e00ab2798b9b3e7d2de977b"
  },
  {
    "url": "assets/js/18.257f3377.js",
    "revision": "241b6d8a73fdcf19a37156b71c5c9040"
  },
  {
    "url": "assets/js/19.296e02ee.js",
    "revision": "f2441c8126ac11cd21c5785ee5f53dc3"
  },
  {
    "url": "assets/js/20.67289fa5.js",
    "revision": "1c13a64b6c89b2c75d4c2fe3654c3719"
  },
  {
    "url": "assets/js/21.d3e9729b.js",
    "revision": "8ba07d4ff3679ca918797af4abf6c20c"
  },
  {
    "url": "assets/js/22.0e5bc2ac.js",
    "revision": "6ec8f9f3c7c31da807fafb6a24dc54fa"
  },
  {
    "url": "assets/js/23.f028eeb1.js",
    "revision": "034205d5c681af341fea936bcdfabe69"
  },
  {
    "url": "assets/js/24.65bcc0a3.js",
    "revision": "d9cac3dc12b13232377649fe5e857874"
  },
  {
    "url": "assets/js/25.c65d75b7.js",
    "revision": "eed7d3a947f4651eed4c3d9155fdb2b9"
  },
  {
    "url": "assets/js/26.d7c6ac6e.js",
    "revision": "2a4660ff35a4e4ae2539401fc81d1689"
  },
  {
    "url": "assets/js/27.83cb78be.js",
    "revision": "6cebdf24c91d0d40946d49f2dfdbbe08"
  },
  {
    "url": "assets/js/28.ca87f827.js",
    "revision": "9542b9566a11883dbc0023c26fd609ae"
  },
  {
    "url": "assets/js/29.3587a05c.js",
    "revision": "d7935eab616dd4e156a162d22ff21daf"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.09e97456.js",
    "revision": "e98804825495d43b777fe43d218def64"
  },
  {
    "url": "assets/js/31.14ed624c.js",
    "revision": "bd92888776d3a80edf0a8892a19fd1ef"
  },
  {
    "url": "assets/js/32.b2dd6008.js",
    "revision": "2108f74c03b93b3bed69523bc60d225c"
  },
  {
    "url": "assets/js/33.92549ddd.js",
    "revision": "92ae86102a42efd12320015ac9195358"
  },
  {
    "url": "assets/js/34.7fdb96d2.js",
    "revision": "ac0cdd32ebf637c53709d08a44d083e5"
  },
  {
    "url": "assets/js/35.0976cdae.js",
    "revision": "c1729d3a8f63011ec52165774d7fcc2f"
  },
  {
    "url": "assets/js/36.f31ca908.js",
    "revision": "d782debd8033a4ef53896add302b475e"
  },
  {
    "url": "assets/js/37.75b53d52.js",
    "revision": "149e7f6749b03a2e4e22b9175c8b86f2"
  },
  {
    "url": "assets/js/38.c4724726.js",
    "revision": "6e6c7de71c5d4c5c3e1bc3038c4bf0c4"
  },
  {
    "url": "assets/js/39.80eddce0.js",
    "revision": "7d294fe38a56b628b0ecabc1af70c1bf"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.3f9e9fff.js",
    "revision": "5bf567b75bc2a1b1783fc20428a4f70d"
  },
  {
    "url": "assets/js/41.dfb756ce.js",
    "revision": "fe8e5b49e92ebe5be41acedb1687b81c"
  },
  {
    "url": "assets/js/42.2f2808f6.js",
    "revision": "faae1588f276e2b8087efb9a4a4c6904"
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
    "url": "assets/js/9.2c396e80.js",
    "revision": "7524c843427c55e0d85aca4f6931429b"
  },
  {
    "url": "assets/js/app.2a3ab18a.js",
    "revision": "6f69dd90f66f6e1b68d0e15e922d5101"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "b2fd24ccdbbe0d058e1905ca1d76f271"
  },
  {
    "url": "categories/index.html",
    "revision": "0c4668b4e9ff488eeab21a4021699b22"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "7ce6f53611b79c58ddd1f9e8641819ae"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "26c19d51b6ad6845ebea9875eeaa791b"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "37f2a706a41958aa5029b2af95624957"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "4c1011ce59c123d57ba464e5e421db71"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "2ce9436fb63e4e12db1e9cecf393a2d8"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "905065944a92a31c88dbf627ef1f5ac6"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "dd1eef25494bfad4e636210a567845ce"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "52d76c2a74014752c04c7c5c6d1934a0"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "66bc8a8891941257dd93045b8c522552"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "45816378239c1f99982f74afb5aee8ae"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "f6274c8c92bb1132b257c0ecd4b4b11d"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "eabcd72aeb70c3c9bfd44b7e0db8037e"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "9356434e8bffc8fdaaf83e09b7056c38"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "f5da57b3d84bacd83c7eec94b4eda7f1"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "93c2955deb7cc08af027696b4faeda8e"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "1178152ae79fcd5938940838f2ae8ff8"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "779927fb81d5a37dcbacb18abbc4c14e"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "c1449723d7548646ff13dceb654d8ded"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "3eb875d8e440a7e0ef6e94686225c642"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "7d6f6809be9816f42fa53efb37e03020"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "dcdd0a06bc6842d2f0ea0cd9e7e60fa4"
  },
  {
    "url": "docs/index.html",
    "revision": "f79968f4dda6db76693bc4bca88e278a"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "cab2dccaceec656fac6b6f88821c0575"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "62200f40b91d5d200879340ea4d68df2"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "8c8b3b92bd6d9dbd33860324bfc4ccc1"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "d2174884e96f55a1571a8b31d558bee8"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "dc60373ea34abad22a82a7c33f36be84"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "7ac9957372f557de3db65dcbb0df05ea"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "97c2780feec78fea33dc07a4b7c3669d"
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
    "revision": "5d77428154e7aa22d5e9e2fcadfe38cf"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "d2d3f8b04455d1947dac37d2047d44cf"
  },
  {
    "url": "timeline/index.html",
    "revision": "e1e12b4c0b8864a2f947956494e3f234"
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
