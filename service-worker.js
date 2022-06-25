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
    "revision": "293bfb5c65863cdbcf6971d63e27a557"
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
    "url": "assets/js/1.bbc69b0d.js",
    "revision": "86fe09a13a05ffcb0d69b14597cad433"
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
    "url": "assets/js/14.75207c27.js",
    "revision": "dc4f96e6d8b6ca0d16f47c03eb5063b4"
  },
  {
    "url": "assets/js/15.ad13abfc.js",
    "revision": "b6d16c4a4e1814eb6a6dca30474c4e61"
  },
  {
    "url": "assets/js/16.2a1a085e.js",
    "revision": "57ab1a98492511575e608325d61ea9a5"
  },
  {
    "url": "assets/js/17.2b893430.js",
    "revision": "d87f3b7bca9c64f039c631dd643d026e"
  },
  {
    "url": "assets/js/18.78712200.js",
    "revision": "3ebbe867eb639d1b8109009754bc17ec"
  },
  {
    "url": "assets/js/19.6c6b6f04.js",
    "revision": "bacc1b4b27ba60978efb73dafa5ac202"
  },
  {
    "url": "assets/js/20.8efbaa3f.js",
    "revision": "5eab253965548fb4c3253f6eb877bfd0"
  },
  {
    "url": "assets/js/21.77fe302f.js",
    "revision": "adf8d19afe06c04be0090899e1543051"
  },
  {
    "url": "assets/js/22.5027c6f9.js",
    "revision": "a859162daf91ff1dd3b937313e610ca9"
  },
  {
    "url": "assets/js/23.d3fe7c30.js",
    "revision": "64c96246c5aa711720db5cc9f532cefe"
  },
  {
    "url": "assets/js/24.7f719eb9.js",
    "revision": "fe094cb2f5193b9af7a076a17f8b15fc"
  },
  {
    "url": "assets/js/25.41b17bc1.js",
    "revision": "d516d81bbdc32cbfe268d740b4c32457"
  },
  {
    "url": "assets/js/26.31842955.js",
    "revision": "a4614588ceab2ab4af42407cb18fcbce"
  },
  {
    "url": "assets/js/27.3e985248.js",
    "revision": "2c4ef4d5a520f9843d12a0576926ab21"
  },
  {
    "url": "assets/js/28.37914e63.js",
    "revision": "c360d9696325431b6846c5a6e24472eb"
  },
  {
    "url": "assets/js/29.3ed7e4e9.js",
    "revision": "04b0fb0f65f29b0e63e54459dabac258"
  },
  {
    "url": "assets/js/3.97cb735a.js",
    "revision": "66d922b4ca9536ad139eb29aedf6761d"
  },
  {
    "url": "assets/js/30.4b9005a0.js",
    "revision": "9291c414da8dc8655f5e54aa0fa3885f"
  },
  {
    "url": "assets/js/31.c24e9799.js",
    "revision": "8cbe2a1207127385c002e43819a9880d"
  },
  {
    "url": "assets/js/32.8b6c7ed7.js",
    "revision": "3002a87ff3ac52b659e583cdf6c00229"
  },
  {
    "url": "assets/js/33.54e2909f.js",
    "revision": "ba666a8803c10e893be46e6740c3882c"
  },
  {
    "url": "assets/js/34.d562ac92.js",
    "revision": "e6772ffc74ff653edd8f95b1104cf6dc"
  },
  {
    "url": "assets/js/35.715bcf24.js",
    "revision": "e60a9e29b291139714ef18ad65957969"
  },
  {
    "url": "assets/js/36.cd9f54e4.js",
    "revision": "9af4324304a76ee964249661d1de2ce8"
  },
  {
    "url": "assets/js/37.9ee2120a.js",
    "revision": "12f810b3e0c534a94189e969b46b59fb"
  },
  {
    "url": "assets/js/38.e6b02022.js",
    "revision": "303c92de1bd2cee4f9ab8a577d3f520d"
  },
  {
    "url": "assets/js/39.e333edcd.js",
    "revision": "bc0cae8e620932e949eb83026b8c6b59"
  },
  {
    "url": "assets/js/4.fd8c8808.js",
    "revision": "5877946461a6d6575241439de614d095"
  },
  {
    "url": "assets/js/40.dc2feb81.js",
    "revision": "028ef391f311df97340fccee1cc7546f"
  },
  {
    "url": "assets/js/41.6ed625f4.js",
    "revision": "3b8b3364203bf3333a433ff341dedc72"
  },
  {
    "url": "assets/js/42.c835a57f.js",
    "revision": "ef9c334dc6643d09972979c344aa88e5"
  },
  {
    "url": "assets/js/43.e4faa988.js",
    "revision": "34be7424cabf314c1a2f1a2237d9481d"
  },
  {
    "url": "assets/js/44.b645317e.js",
    "revision": "d19368243f026d20d05ada1beabe6972"
  },
  {
    "url": "assets/js/45.ddb2ba5d.js",
    "revision": "e77632158da24bd633107d32836f6ffe"
  },
  {
    "url": "assets/js/46.04b8fb19.js",
    "revision": "0d6f9a0f3bec3a28cded910bbae0b94f"
  },
  {
    "url": "assets/js/47.cde5903b.js",
    "revision": "b9926a5065dbcdf675885eb9ec128809"
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
    "url": "assets/js/8.8aea8f6a.js",
    "revision": "0aae2683c4faa976504569728801f1e0"
  },
  {
    "url": "assets/js/9.ce4fe8d3.js",
    "revision": "17ce9bbc31f9593a960b7715f0b5318d"
  },
  {
    "url": "assets/js/app.17df1656.js",
    "revision": "79bf126d975b44736314f0119341bedf"
  },
  {
    "url": "background.png",
    "revision": "f0cb5c6080cc533cce01b7a7182940fe"
  },
  {
    "url": "blogs/about.html",
    "revision": "159df35236efda5a70e1f52db2e2fc59"
  },
  {
    "url": "categories/index.html",
    "revision": "ec103077edf82fa6fa818023ad3b8692"
  },
  {
    "url": "docs/api_doc/group.html",
    "revision": "60a59b5cfd2fc7eb93bf1ef47b9e6fee"
  },
  {
    "url": "docs/api_doc/plugins.html",
    "revision": "27e5bd9f961422b967430b50b0c60165"
  },
  {
    "url": "docs/api_doc/request.html",
    "revision": "f9de4d439ffe84da14494439b12c90d8"
  },
  {
    "url": "docs/api_doc/system.html",
    "revision": "fa95b7837049206fde9a2f38556b75e9"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "2405f8dc0db9b3224d14185d6e131c9b"
  },
  {
    "url": "docs/development_doc/shop_handle.html",
    "revision": "76fba1622cb1be448cff564085d9defe"
  },
  {
    "url": "docs/development_doc/task_control.html",
    "revision": "1661226ddb4ef868ec06c350b5720219"
  },
  {
    "url": "docs/development_doc/utils.html",
    "revision": "c6f2ca47b56276eac346cfedd4687a15"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "56a8dbdd16261628baf0f78e3b7a1083"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "8bc8fc5af81dcc2c54009247375df581"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "96de30be8710a1eaae5a68ad01e8224b"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "ee6122911f7233c624d17d63b79a51cc"
  },
  {
    "url": "docs/help_doc/basic_plugins/shop_plugins.html",
    "revision": "6f9ff47a29f6275103b82fc67e875de8"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "ec8b67459a4f6d244d930776c5167feb"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "ac0a5c18553b3b77e83ad1f9b0d172a3"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "e636896aae219d38ea79acf8548090f5"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "bd6277460f3a9277d90871ba4b84c0f6"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "24092ede492bcaee1c5a0f4b165fb0ac"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "39b61f666da3c1b8a330c114c19106b1"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "d0263dfef1c84f02988ba001620f9464"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "875b11640bb8254ad86a2807a9c7feda"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "46dff1c0d8916d081d145717c4414977"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "7f783d72eaa0aa6242307ea9d70535e0"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "564896829beef7a1211e04c27716cd9c"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "4ed7bd7723618e1d8a32b7c6a65476fc"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "43251995209c8269fb560f8ac3ad75fe"
  },
  {
    "url": "docs/index.html",
    "revision": "3ec0ae0fbb4e562f49e93fb8273436ef"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "b3d0f5b4efa6c017ac5a4822a40c3bb3"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "3cc225d175b6759874e33d3f8bddfd2b"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "9599dea561cbdb7df665b70ea1c4da36"
  },
  {
    "url": "docs/installation_doc/install_webui.html",
    "revision": "8843dbb0fb9f2a58cb26a0454f7f1e27"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "71814a0a31c7e6b1f1121c4ff07135c1"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "010a2148717c782f7ded65a5cafb4b51"
  },
  {
    "url": "docs/update_log/index.html",
    "revision": "0159e90e8ecc233212a4e45807e00f37"
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
    "revision": "827d64f225a6109758cf3a10f533bb08"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "7f9f4c2f1992e700ed67bea2d4441003"
  },
  {
    "url": "timeline/index.html",
    "revision": "59dd25411e470791f49f488c05049c9c"
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
