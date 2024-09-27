const cacheName = "Rage65-2d platformer-1.0";
const contentToCache = [
    "Build/868ad3e5f43e7a2d53d450d58e45443c.loader.js",
    "Build/f2b55c5a765f7cd961e941781eb7510e.framework.js",
    "Build/af25a030d55c3c5f2355e66177caa462.data",
    "Build/a61886347a70797340fc53623bb3b699.wasm",
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
