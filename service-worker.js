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
    "revision": "8f396aef276ca87c9b1e88be3e06c461"
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
    "url": "assets/js/12.9be1bab5.js",
    "revision": "2ae8b75065f7db760178dcdd36e05078"
  },
  {
    "url": "assets/js/13.556ed60a.js",
    "revision": "7535fa2b2b90eb3d3355b814a871db1d"
  },
  {
    "url": "assets/js/14.af159e50.js",
    "revision": "4cc96097332cb06ad8a7683688460628"
  },
  {
    "url": "assets/js/15.eb6bdf7b.js",
    "revision": "88ee46cb936b7b99f4aed5de3776ac1e"
  },
  {
    "url": "assets/js/16.8e9e4136.js",
    "revision": "261b6f81f1f0feb35408014a7148233a"
  },
  {
    "url": "assets/js/17.0dca2f05.js",
    "revision": "7a8859e20009e8e2038c700e285e58da"
  },
  {
    "url": "assets/js/18.926bda27.js",
    "revision": "ba5a342533696bf8fea7af979d3dbb94"
  },
  {
    "url": "assets/js/19.2114ca0e.js",
    "revision": "d9b5c6949c1af33c46d23ace01a2463a"
  },
  {
    "url": "assets/js/20.2a556377.js",
    "revision": "9e16baa10078ae89398f8b6295e5b899"
  },
  {
    "url": "assets/js/21.0ffa19af.js",
    "revision": "6f0b6ebc5c217c157bd4adeb76432fbf"
  },
  {
    "url": "assets/js/22.4e45a85a.js",
    "revision": "9815684814aa61da85e45efb6bb8d360"
  },
  {
    "url": "assets/js/23.97708eb2.js",
    "revision": "af5f8ced9a569305eb158c4c87e41c51"
  },
  {
    "url": "assets/js/24.65bcc0a3.js",
    "revision": "d9cac3dc12b13232377649fe5e857874"
  },
  {
    "url": "assets/js/25.2fd1d408.js",
    "revision": "294106c17784cf4b4e1943ffc990d90d"
  },
  {
    "url": "assets/js/26.d7c6ac6e.js",
    "revision": "2a4660ff35a4e4ae2539401fc81d1689"
  },
  {
    "url": "assets/js/27.cedf7481.js",
    "revision": "3eeed0e06af58e881d716f1caca3917e"
  },
  {
    "url": "assets/js/28.ca87f827.js",
    "revision": "9542b9566a11883dbc0023c26fd609ae"
  },
  {
    "url": "assets/js/29.7d3eb888.js",
    "revision": "4f74d6a1912b8a98c36574eca7719916"
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
    "url": "assets/js/31.6f7ba180.js",
    "revision": "24156dc6b06497ba3efe3a74fbb4692d"
  },
  {
    "url": "assets/js/32.36dfe74d.js",
    "revision": "b33bf9756d0fe0f45cf57bdc4d846f8b"
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
    "url": "assets/js/38.b3c2446d.js",
    "revision": "97c59545cd2a846345a02ce039d0d830"
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
    "url": "assets/js/40.cd3d170f.js",
    "revision": "c8e9a4cd313a6ae48669b937bdafe497"
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
    "url": "assets/js/app.de189013.js",
    "revision": "6134e377308717da9613985c29db5ca3"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "fc37640981254a60049bcb57e72ca34f"
  },
  {
    "url": "categories/index.html",
    "revision": "3ff49e55208ee187165178d10aa32b7b"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "05684366ea0d835133a5ccc680d28496"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "6b879c75fa7b1396d70b553d4ff8b989"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "30cd6ead97856f0cbd66a7dbc3d54697"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "cd0d3a6e3d5f22dfff532c526a528429"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "31d255c465aa7002ef30f687141769e2"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "7da9dc197ec72471553ea5d5b2ce5ead"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "1a77630fbd03fbe17e1296b2073b0f96"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "95379687014f1eece5fb3b99c959bc2b"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "94806802318247e9edfad256ec832354"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "c50d3eec59b913354b8e25c0f077b53d"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "afcc25c0692d01155166f5b7a720a67d"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "95650e26bff9945d5b610de4002c1efa"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "f6ab3be9311e38fd4b322bb1689b1bc4"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "de8b68c652fd8b51c4248d0fd0ac9934"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "d4e5e84740bdb8286bcbdfde0c45413e"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "b8361cec42f73e9e9dcd46a6bda7a1b7"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "faecb5bd977998155f82c9e8dec0d58b"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "d2911c7d9d777df8124e181c0d4dbe3a"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "b66fb5812860c27726bef399af27110d"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "b0c80f7107f18c53444628284019a698"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "db931b50c1a57b872c48df2caed4a3fa"
  },
  {
    "url": "docs/index.html",
    "revision": "5d9c0f482f8c220c260709ceacd23a6e"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "392d22011f9d8d45276c64469d0ec650"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "5462a81561dc849e554d2f014516d322"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "793169d10881f3caeb77ddee8bd43800"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "2a0e4c3a0963267ab5abe0401f6fcfb8"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "b4d27691613ae1f4f229f6500245832e"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "c71c0b0fadc3b84249c2939054e86c58"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "5c0e1cc12465c7d2ad27f32f181d410e"
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
    "revision": "cb3e22ad5adc03d5cebfe8a6deec752d"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "c494afcf3c6e8615547b4bf5bcf0a428"
  },
  {
    "url": "timeline/index.html",
    "revision": "5979416eacbabf8cfd424b4cb5de40d4"
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
