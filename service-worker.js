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
    "revision": "59ab34510ee4acfa566ba63e783e51ff"
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
    "url": "assets/js/10.d8b4303c.js",
    "revision": "c4628c2f5e6d1b88fd0ed9449363accd"
  },
  {
    "url": "assets/js/11.e5d78693.js",
    "revision": "a0752b097c88ce70b3a73f100e3fbda4"
  },
  {
    "url": "assets/js/12.34bf8cac.js",
    "revision": "fedbf57f573e5f30018357343788e5b0"
  },
  {
    "url": "assets/js/13.3f1eb4dd.js",
    "revision": "419541c23df8d69ac12099e1e9acb719"
  },
  {
    "url": "assets/js/14.99373be3.js",
    "revision": "eedf91a79d5fbbcb4395d49b4de73107"
  },
  {
    "url": "assets/js/15.122f6db2.js",
    "revision": "7132ff815f8273504836ed4d1c52dae6"
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
    "url": "assets/js/19.dc0110bf.js",
    "revision": "2e2fc5388e7f10c9b41f71977abc4f0f"
  },
  {
    "url": "assets/js/20.27326f16.js",
    "revision": "4f68841dba30825f13bba7eefcc8af23"
  },
  {
    "url": "assets/js/21.8b0daf11.js",
    "revision": "7090eef2064fda42df432f1e4a21fd8e"
  },
  {
    "url": "assets/js/22.eebaa04e.js",
    "revision": "7e415b480750db15b1052b622fd5eda9"
  },
  {
    "url": "assets/js/23.c638e6e9.js",
    "revision": "cefc1f17bff20fd0f48e8dd3c17b9c40"
  },
  {
    "url": "assets/js/24.dea1dc81.js",
    "revision": "fbae9d10e5966547e5fa8134d4ffa53d"
  },
  {
    "url": "assets/js/25.72e19154.js",
    "revision": "bab6ad8c6c361836ac8536a0efcefcb8"
  },
  {
    "url": "assets/js/26.ffc956c3.js",
    "revision": "1d0f6bf6d5a71b860270a27cfa4c7b5c"
  },
  {
    "url": "assets/js/27.1f3bf036.js",
    "revision": "31f8a1eb91391b2cd8a6b789cf8b9bb1"
  },
  {
    "url": "assets/js/28.43010a54.js",
    "revision": "0c1ae87a0d590e86898ecb040c7ff7dc"
  },
  {
    "url": "assets/js/29.e0045682.js",
    "revision": "7dc5665467194c8bc0abaef424bce983"
  },
  {
    "url": "assets/js/3.b5d42824.js",
    "revision": "90d2dd9378bdc1dc07ea5c14044c875d"
  },
  {
    "url": "assets/js/30.1229ee54.js",
    "revision": "523cfa376f7ced39ffaaabe72b41f26a"
  },
  {
    "url": "assets/js/31.64794ab7.js",
    "revision": "1b059dd026e6559808df0b9ed9c7a52a"
  },
  {
    "url": "assets/js/32.0ff2a7ad.js",
    "revision": "acf0970264bcef79d9b763780024238f"
  },
  {
    "url": "assets/js/33.63238341.js",
    "revision": "c9f3543928c8d41b0e6faafed825b0a4"
  },
  {
    "url": "assets/js/34.d96ee9f0.js",
    "revision": "876f43d749812667a465c9cca40c0fa4"
  },
  {
    "url": "assets/js/35.c4d808eb.js",
    "revision": "b20e7a0af0cf5cdd51798aff180e3e0c"
  },
  {
    "url": "assets/js/36.69a79175.js",
    "revision": "bb984522dd73aad21a1f53364fff3adc"
  },
  {
    "url": "assets/js/37.a64202ca.js",
    "revision": "0fc930fa49f451310b2d9654fc20cf44"
  },
  {
    "url": "assets/js/38.33fc3f94.js",
    "revision": "1b91745ba5d0b48a18404c014aff00ef"
  },
  {
    "url": "assets/js/4.a3d0177f.js",
    "revision": "67138a1fdac208c38513b7004e1305eb"
  },
  {
    "url": "assets/js/5.37e87dee.js",
    "revision": "fd225c987340ad9662d35400b1532236"
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
    "url": "assets/js/9.b0038289.js",
    "revision": "c937fc5d6adbf8afe8d49ae82afa7c2a"
  },
  {
    "url": "assets/js/app.9d87503a.js",
    "revision": "65e37583bdc6ea32a3437a36ff3d1bdc"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "blogs/about.html",
    "revision": "24a3073459fc69975b2648057c83d980"
  },
  {
    "url": "categories/index.html",
    "revision": "8b0a75955300dc14250640ebe9c86df1"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "873ef4addb7b69aca4140eaf84876eb7"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "96fb638ad0a70244460b4ceedb46eb69"
  },
  {
    "url": "docs/help_doc/basic_plugins/admin_plugins.html",
    "revision": "8d6e792bef6059278bd3dd752cebb168"
  },
  {
    "url": "docs/help_doc/basic_plugins/common_plugins.html",
    "revision": "6e91be3074773016d110ab529b4a9f61"
  },
  {
    "url": "docs/help_doc/basic_plugins/other_plugins.html",
    "revision": "8e68e05a1700976403fb68e2ab6f36a3"
  },
  {
    "url": "docs/help_doc/basic_plugins/superuser_plugins.html",
    "revision": "8ff3ff8307040ba9cf83ee6969c85553"
  },
  {
    "url": "docs/help_doc/configs.html",
    "revision": "6914d06ba3bbd4875dc8f8dc3fc36f0f"
  },
  {
    "url": "docs/help_doc/index.html",
    "revision": "f6f3d2c22e599d105fe1c27148e77516"
  },
  {
    "url": "docs/help_doc/plugins_index.html",
    "revision": "f8f4a33ed5ac651e94c1d093004fefdc"
  },
  {
    "url": "docs/help_doc/public_plugins/admin_plugins.html",
    "revision": "98ad531d87ec6440f85503d44d48c788"
  },
  {
    "url": "docs/help_doc/public_plugins/common_plugins/common_plugins.html",
    "revision": "1899173df7620f075d1e274b1778e9e3"
  },
  {
    "url": "docs/help_doc/public_plugins/draw_card_plugins/draw_card_plugins.html",
    "revision": "d7eaa9810974d0ddd62445446888d552"
  },
  {
    "url": "docs/help_doc/public_plugins/game_plugins/game_plugins.html",
    "revision": "27f5bacf37c19797ffeac243a301836b"
  },
  {
    "url": "docs/help_doc/public_plugins/genshin_plugins/genshin_plugins.html",
    "revision": "8d2deb5397d65861ad13f70c05a5b87a"
  },
  {
    "url": "docs/help_doc/public_plugins/other_plugins/other_plugins.html",
    "revision": "0bd0ef9761f363b523b592e731ed2378"
  },
  {
    "url": "docs/help_doc/public_plugins/pic_plugins/pic_plugins.html",
    "revision": "1210ca44f470a5a4904a80d8effa7372"
  },
  {
    "url": "docs/help_doc/public_plugins/shop_plugins/shop_plugins.html",
    "revision": "773799afd9e1df3ef5cbeba93cac1922"
  },
  {
    "url": "docs/help_doc/public_plugins/superuser_plugins.html",
    "revision": "c9328d5a934ba6057a993e9d85e44a3e"
  },
  {
    "url": "docs/help_doc/public_plugins/utils_plugins/utils_plugins.html",
    "revision": "d13dc171af3ae9f530d2b8102da6b80e"
  },
  {
    "url": "docs/index.html",
    "revision": "05081cb7665bbf74ac27c1a321aeb831"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "f1b3c296be19f57fc182b79ac4347903"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "c77c8f14785d6ef084e29501a9068b59"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "a940aecf5bcb9bfaf1ee87c6dd0dc075"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "86b10c1dc4361721036c1fb0afef10fc"
  },
  {
    "url": "docs/installation_doc/start_.html",
    "revision": "fecb7a88fdb521d26a5e182266b4ec50"
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
    "revision": "8cb04c56170da944f0b64b5717a8d399"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "8fca6014e7dba303ff087e21130756a8"
  },
  {
    "url": "timeline/index.html",
    "revision": "b8bfcaa4c66616e8667f019c914397c9"
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
