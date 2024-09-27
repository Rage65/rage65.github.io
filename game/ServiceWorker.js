const cacheName = "Rage65-2d platformer-1.0";
const contentToCache = [
    "Build/868ad3e5f43e7a2d53d450d58e45443c.loader.js",
    "Build/d1842b4dd2fced1a1aa8139b91e1dd25.framework.js",
    "Build/43770093618b44a49600e601def25864.data",
    "Build/f0df29fce9b78b022dbc82cef47ac138.wasm",
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
