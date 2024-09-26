const cacheName = "Rage65-2d platformer-1.0";
const contentToCache = [
    "Build/bb0d9ecdb05db3e84da20bd14a4f84dc.loader.js",
    "Build/1b8ea8490ba562d121d04b38fe07a2eb.framework.js",
    "Build/22c478b19d6e9fae5b80a7c8883e0c73.data",
    "Build/05c6b3566c43837b5d847aa5c4f52c2a.wasm",
    "TemplateData/style.css"

];

self.addEventListener('install', function (e) {
    console.log('[Service Worker] Install');
    
    e.waitUntil((async function () {
      const cache = await caches.open(cacheName);
      console.log('[Service Worker] Caching all: app shell and content');
      await cache.addAll(contentToCache);
    })());
});

self.addEventListener('fetch', function (e) {
    e.respondWith((async function () {
      let response = await caches.match(e.request);
      console.log(`[Service Worker] Fetching resource: ${e.request.url}`);
      if (response) { return response; }

      response = await fetch(e.request);
      const cache = await caches.open(cacheName);
      console.log(`[Service Worker] Caching new resource: ${e.request.url}`);
      cache.put(e.request, response.clone());
      return response;
    })());
});
