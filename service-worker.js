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
    "revision": "7f66313cb7dc22a0d99d284e77012a03"
  },
  {
    "url": "assets/css/0.styles.8af9daac.css",
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
    "url": "assets/js/1.cdeec391.js",
    "revision": "dd0f9a59db312e4e6b173fbafd815809"
  },
  {
    "url": "assets/js/10.43e159f5.js",
    "revision": "44d4a30d2ae0c1cb936c19d5a827a3b2"
  },
  {
    "url": "assets/js/11.5c87898d.js",
    "revision": "f6e5ff3fdaa2b94ecca209dc7763094e"
  },
  {
    "url": "assets/js/12.a14f5f91.js",
    "revision": "a7f51247f39230457216221226e62f7a"
  },
  {
    "url": "assets/js/13.d8bb6c8d.js",
    "revision": "95d44f332456ea8a4f64c7e150fd59a8"
  },
  {
    "url": "assets/js/14.a4d0f1d9.js",
    "revision": "a8c007c3596b057deea2d866fc5bf038"
  },
  {
    "url": "assets/js/15.73472e47.js",
    "revision": "2a4ad9bb1366d6a91d01c8343ed03f75"
  },
  {
    "url": "assets/js/16.82ed5547.js",
    "revision": "2ab05f52c0ba62334d915583f673da88"
  },
  {
    "url": "assets/js/17.ddf12e4f.js",
    "revision": "da200b0c3997b4f52e64f71fba627d25"
  },
  {
    "url": "assets/js/18.8e88a1bb.js",
    "revision": "c596170ffd4d880e5f16da687170fcf6"
  },
  {
    "url": "assets/js/19.a0834e7f.js",
    "revision": "cc66e22fdae5ba044860263a96acc5e4"
  },
  {
    "url": "assets/js/3.69b73a9d.js",
    "revision": "456d69b317b9759ccd1f9050d517f220"
  },
  {
    "url": "assets/js/4.d526ba72.js",
    "revision": "19492d61b803fb25ee6cb4acf43f3794"
  },
  {
    "url": "assets/js/5.cc8a7e08.js",
    "revision": "8da5560311c885c069fe97941b70734f"
  },
  {
    "url": "assets/js/6.59e113d9.js",
    "revision": "c01bd3cb3d3c57640c458f047f8f659f"
  },
  {
    "url": "assets/js/7.643985c7.js",
    "revision": "d0bd8722743c4b844c09c470c5f15c4f"
  },
  {
    "url": "assets/js/8.1eda56ed.js",
    "revision": "415fc2b2f6707d859b376bd6b404f7b1"
  },
  {
    "url": "assets/js/9.8ba10ad5.js",
    "revision": "9edcbc01e96a15b513a8d9cb44205792"
  },
  {
    "url": "assets/js/app.e25319e3.js",
    "revision": "1f7daa3145b5359419ef30b227290d6e"
  },
  {
    "url": "background.png",
    "revision": "aa3c9e4ba5a97bb542f894a3ac339b81"
  },
  {
    "url": "categories/index.html",
    "revision": "8fd9af05804565f1f3120aa0176053f3"
  },
  {
    "url": "docs/development_doc/plugins.html",
    "revision": "44a2b91363d59977ca995404f0a342bc"
  },
  {
    "url": "docs/faq/index.html",
    "revision": "fee80e94dd4c4b788304ec946aec2f25"
  },
  {
    "url": "docs/index.html",
    "revision": "40092a81bdf84ed0a677ed3b09d0b892"
  },
  {
    "url": "docs/installation_doc/index.html",
    "revision": "092a456fdb3a1d02e396b72692867be7"
  },
  {
    "url": "docs/installation_doc/install_gocq.html",
    "revision": "3d09a8859b12c7307472c3f22826f82f"
  },
  {
    "url": "docs/installation_doc/install_postgresql.html",
    "revision": "fd3ca6bfe8ab204d419d142c4fffd5b7"
  },
  {
    "url": "docs/installation_doc/install_zhenxun.html",
    "revision": "cb7572d38b7cdfe830cc3472a06fdd42"
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
    "revision": "6d073a0df79ed870c1248087546c32fc"
  },
  {
    "url": "logo.png",
    "revision": "247217ec9f22445d8f14aedcd1eb1b3f"
  },
  {
    "url": "tag/index.html",
    "revision": "7b29c895b9486699823fac6431cdb2ac"
  },
  {
    "url": "timeline/index.html",
    "revision": "37ecd0232c8bdd860c0d1ad8eb2641d1"
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
