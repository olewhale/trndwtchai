2024-12-26T23:04:08.054Z ACTOR: Pulling Docker image of build 6sOStSkN5Nfea7vRE from repository.
2024-12-26T23:04:08.159Z ACTOR: Creating Docker container.
2024-12-26T23:04:08.192Z ACTOR: Starting Docker container.
2024-12-26T23:04:10.858Z INFO  System info {"apifyVersion":"3.2.6","apifyClientVersion":"2.9.4","crawleeVersion":"3.12.1","osType":"Linux","nodeVersion":"v20.18.1"}
2024-12-26T23:04:10.960Z INFO  Results Limit 40, ACTOR_MAX_PAID_DATASET_ITEMS 822
2024-12-26T23:04:11.653Z INFO  [Status message]: Starting the direct URL scraper with 65 direct URL(s)
2024-12-26T23:04:11.930Z INFO  CheerioCrawler: Starting the crawler.
2024-12-26T23:04:15.918Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:15.920Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=doc_magomedova","retryCount":1}
2024-12-26T23:04:17.457Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:17.459Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=magerya_endocrinolog_","retryCount":1}
2024-12-26T23:04:17.580Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:17.582Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=doctor_polyanina","retryCount":1}
2024-12-26T23:04:22.145Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:22.147Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=nelly_petrosian","retryCount":1}
2024-12-26T23:04:24.655Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:24.658Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=thebraincoach","retryCount":1}
2024-12-26T23:04:27.874Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:27.876Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=doctor_zubareva","retryCount":1}
2024-12-26T23:04:37.946Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Retrying after error: Login • Instagram
2024-12-26T23:04:37.950Z     at handleMediaJson (file:///usr/src/app/dist/src/routes-directurls.js:277:15) {"url":"https://i.instagram.com/api/v1/users/web_profile_info/?username=coachshivangidesai","retryCount":1}
2024-12-26T23:04:40.740Z INFO  CheerioCrawler: All requests from the queue have been processed, the crawler will shut down.
2024-12-26T23:04:41.140Z INFO  CheerioCrawler: Final request statistics: {"requestsFinished":65,"requestsFailed":0,"retryHistogram":[58,7],"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":2948,"requestsFinishedPerMinute":133,"requestsFailedPerMinute":0,"requestTotalDurationMillis":191651,"requestsTotal":65,"crawlerRuntimeMillis":29256}
2024-12-26T23:04:41.143Z INFO  CheerioCrawler: Finished! Total 65 requests: 65 succeeded, 0 failed. {"terminal":true}
2024-12-26T23:04:41.158Z INFO  [Status message]: Direct URL scraper finished
2024-12-26T23:04:41.247Z INFO  [Status message]: Starting posts scraper with 65 direct URL(s)
2024-12-26T23:04:41.283Z INFO  [Status message]: Starting the post scraper with 65 post URL(s)
2024-12-26T23:04:41.360Z INFO  CheerioCrawler: Starting the crawler.
2024-12-26T23:04:45.506Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The proxy server rejected the request with status code 590 (UPSTREAM502)
2024-12-26T23:04:45.508Z  {"id":"ph67S8WJJbg11oK","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%22191028196%22%2C%22first%22%3A12%7D","retryCount":1}
2024-12-26T23:04:54.785Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request got blocked. Will retry with different session
2024-12-26T23:04:54.788Z     at file:///usr/src/app/dist/src/routes/feed.js:15:15 {"id":"DoymETa5fPQOWCC","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%22351529411%22%2C%22first%22%3A12%7D","retryCount":1}
2024-12-26T23:05:41.360Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":10261,"requestsFinishedPerMinute":49,"requestsFailedPerMinute":0,"requestTotalDurationMillis":502780,"requestsTotal":49,"crawlerRuntimeMillis":60076,"retryHistogram":[49]}
2024-12-26T23:05:41.646Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":14,"desiredConcurrency":15,"systemStatus":{"isSystemIdle":true,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0.075},"cpuInfo":{"isOverloaded":false,"limitRatio":0.4,"actualRatio":0.16},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:05:49.151Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Protocol error
2024-12-26T23:05:49.153Z  {"id":"1ScLR6IRZtF2oLH","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%2260426276912%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFEMktjV0wzcFFRbVZQU2NLdzFabmJ3VXlraUdYU1VYQWx2Z0UzSTl0MHZxNUcyZXJJd1NWcXdTVE1WQ0x2OXkzVTVNS3Y1eFo2Z1JUSnExbUVFS3dCUQ%3D%3D%22%7D","retryCount":1}
2024-12-26T23:05:50.812Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. request timed out after 30 seconds. {"id":"JB3mgVpiAPsGVZe","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%226643312712%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFCX1B0UThacko4UzRDLUVya2ttVF9yLTF4b1RNeGhGWVpxR2x4UDY2Ums5VVNwWExFUFlVMk52eWoyYUlpN1V4OVNBejJTbkhDal9udHBtdHluYkkwWA%3D%3D%22%7D","retryCount":1}
2024-12-26T23:06:07.173Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The proxy server rejected the request with status code 590 (UPSTREAM502)
2024-12-26T23:06:07.175Z  {"id":"sZsekN4I4D5s1Dl","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%2236873217137%22%2C%22first%22%3A12%7D","retryCount":1}
2024-12-26T23:06:28.868Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The proxy server rejected the request with status code 590 (UPSTREAM502)
2024-12-26T23:06:28.870Z  {"id":"UwNnfDQrptEQ4IF","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%22338621481%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFBZlBfVW1NdzJPcGplLVhUY1RtM203OVlZRGVPdU5GekF2VlU1QnFWNGRGM0d0NFlVR2FNVnM1X3pud0pFVjQ4WV8tLVY0UVBQX3E2SDZpcWZHckdUMA%3D%3D%22%7D","retryCount":1}
2024-12-26T23:06:41.360Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":11646,"requestsFinishedPerMinute":58,"requestsFailedPerMinute":0,"requestTotalDurationMillis":1350916,"requestsTotal":116,"crawlerRuntimeMillis":120076,"retryHistogram":[116]}
2024-12-26T23:06:41.776Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":4,"desiredConcurrency":15,"systemStatus":{"isSystemIdle":false,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0.149},"cpuInfo":{"isOverloaded":true,"limitRatio":0.4,"actualRatio":0.556},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:06:56.039Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Client network socket disconnected before secure TLS connection was established
2024-12-26T23:06:56.042Z  {"id":"Tae8O1mliroXbHq","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%221294963609%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFEa1JJS05xQVpXVkZ0c2NrUVNKZGllQU56R3hkRHBTYWx5UXVqNjhpLWJWUjhoTzJNTEZTbnlOdW5DZUo3X3JVWW56d1JZT2k3eHQwbU5OTXVOdlAxVA%3D%3D%22%7D","retryCount":1}
2024-12-26T23:07:03.653Z INFO  pushDataMaxAware 822
2024-12-26T23:07:07.545Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. request timed out after 30 seconds. {"id":"OpdONTuhLmVNPDN","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%226349005167%22%2C%22first%22%3A12%7D","retryCount":1}
2024-12-26T23:07:28.172Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:28.174Z  {"id":"etSl4kuLrEJkOFP","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:31.070Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The HTTP/2 stream has been early terminated
2024-12-26T23:07:31.072Z  {"id":"3xjQzMcBGCdHuIV","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:41.359Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":9810,"requestsFinishedPerMinute":69,"requestsFailedPerMinute":0,"requestTotalDurationMillis":2030648,"requestsTotal":207,"crawlerRuntimeMillis":180076,"retryHistogram":[206,1]}
2024-12-26T23:07:41.782Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":17,"desiredConcurrency":18,"systemStatus":{"isSystemIdle":true,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0.077},"cpuInfo":{"isOverloaded":false,"limitRatio":0.4,"actualRatio":0.034},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:07:41.956Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:41.959Z  {"id":"9ki5jNN8I4tlGkx","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:42.487Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:42.489Z  {"id":"3LGfKcdy5KM047Z","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:44.955Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:44.958Z  {"id":"5H9J2QGfVscj1TK","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:49.351Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:49.353Z  {"id":"GHoLWXs5tt3QuO9","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:54.719Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:54.721Z  {"id":"MeXwy3PvYyu0v8s","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:07:56.360Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:07:56.362Z  {"id":"Ulb3XgrAm5Fdi13","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:02.181Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:02.183Z  {"id":"sGu1A2Xf7w82o5B","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:09.808Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Timeout awaiting 'request' for 30000ms
2024-12-26T23:08:09.810Z  {"id":"LFBylmjETdtfQLW","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:18.552Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:18.554Z  {"id":"QFapWKZ2e3FN7jf","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:22.090Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:22.093Z  {"id":"UJApTZafp30fZvf","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:23.970Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:23.972Z  {"id":"xNnfouomvXfcduU","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:34.239Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:34.241Z  {"id":"2FuaTpth4hqO1Bx","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:35.711Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:35.713Z  {"id":"dogcQtl4bl06W43","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:41.359Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":7808,"requestsFinishedPerMinute":97,"requestsFailedPerMinute":0,"requestTotalDurationMillis":3029370,"requestsTotal":388,"crawlerRuntimeMillis":240076,"retryHistogram":[386,2]}
2024-12-26T23:08:41.846Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":17,"desiredConcurrency":25,"systemStatus":{"isSystemIdle":true,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0},"cpuInfo":{"isOverloaded":false,"limitRatio":0.4,"actualRatio":0.28},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:08:42.540Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:42.542Z  {"id":"bPTRkohYnCOoWxi","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:46.138Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:46.140Z  {"id":"yOb9wkXEmIpqmow","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:51.547Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:51.549Z  {"id":"5TzHbJ6HeUhBOjx","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:56.544Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:56.546Z  {"id":"MMnwmYMcJmuvzKm","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:56.847Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:08:56.849Z  {"id":"WZfTl8oGlfzk7DL","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:08:57.740Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The proxy server rejected the request with status code 590 (UPSTREAM502)
2024-12-26T23:08:57.743Z  {"id":"JB3mgVpiAPsGVZe","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%226643312712%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFCX1B0UThacko4UzRDLUVya2ttVF9yLTF4b1RNeGhGWVpxR2x4UDY2Ums5VVNwWExFUFlVMk52eWoyYUlpN1V4OVNBejJTbkhDal9udHBtdHluYkkwWA%3D%3D%22%7D","retryCount":2}
2024-12-26T23:09:08.638Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:08.640Z  {"id":"pefFwyKt5VMMS5M","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:20.224Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:20.226Z  {"id":"J0lUSzAfSmN6rkt","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:25.958Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Session closed without receiving a SETTINGS frame
2024-12-26T23:09:25.960Z  {"id":"4YIgrlCShArXJt7","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:26.251Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:26.256Z  {"id":"mEZhWLupFgoPRb6","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:27.296Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. requestHandler timed out after 100 seconds (FIVJI3Az6wKxfhb). {"id":"FIVJI3Az6wKxfhb","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%22351529411%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFBVTVQYk1OeXJRX0lOajRQTFQ5aE5CUEFscFhEdWVkQThTMGh4UXd1U21NcmRFbXh6djZtcWhabm81Yk9oNU9RX0NHMUdMQXB3RV9jcC1QU3BKYVNsUg%3D%3D%22%7D","retryCount":1}
2024-12-26T23:09:33.273Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:33.275Z  {"id":"QPYuwT0AXl8HM97","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:37.466Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The HTTP/2 stream has been early terminated
2024-12-26T23:09:37.469Z  {"id":"Kq4XTgc9wfIWc94","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:37.541Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:37.543Z  {"id":"lkDukWotSLMZGPy","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:41.444Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":7230,"requestsFinishedPerMinute":112,"requestsFailedPerMinute":0,"requestTotalDurationMillis":4063232,"requestsTotal":562,"crawlerRuntimeMillis":300161,"retryHistogram":[560,2]}
2024-12-26T23:09:41.944Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":27,"desiredConcurrency":29,"systemStatus":{"isSystemIdle":true,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0},"cpuInfo":{"isOverloaded":false,"limitRatio":0.4,"actualRatio":0.399},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:09:48.436Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:48.438Z  {"id":"3DwW8Ov0IOSDP2g","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:48.836Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:48.838Z  {"id":"wvFA6QsPXh5Emn8","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:09:57.085Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:09:57.087Z  {"id":"LEoxnoP2Cwe1PUX","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:01.504Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:01.506Z  {"id":"5taER4a5q5yxPzn","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:02.543Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:02.545Z  {"id":"2ahureYb1651pVh","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:06.850Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:06.852Z  {"id":"8JDKNmDlvUHb0Kb","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:07.773Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:07.775Z  {"id":"JhzUwSiJeebc7Hm","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:07.942Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:07.944Z  {"id":"dCwZjLGlEFsrl2Q","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:08.227Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. The HTTP/2 stream has been early terminated
2024-12-26T23:10:08.229Z  {"id":"Jp0utPEy2FjauSD","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:12.740Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. request timed out after 30 seconds. {"id":"V5JuthsGVeqajaO","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:13.899Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:13.901Z  {"id":"QUu3q4moB7NytIm","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:26.255Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:26.258Z  {"id":"SW05e0u1J8BzoLK","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:27.438Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:27.440Z  {"id":"RtWUneJLbmzQC5J","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:28.574Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:28.577Z  {"id":"PLMAxwn5xsp3xUE","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:31.471Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. requestHandler timed out after 100 seconds (1ScLR6IRZtF2oLH). {"id":"1ScLR6IRZtF2oLH","url":"https://www.instagram.com/graphql/query/?query_hash=69cba40317214236af40e7efa697781d&variables=%7B%22id%22%3A%2260426276912%22%2C%22first%22%3A12%2C%22after%22%3A%22QVFEMktjV0wzcFFRbVZQU2NLdzFabmJ3VXlraUdYU1VYQWx2Z0UzSTl0MHZxNUcyZXJJd1NWcXdTVE1WQ0x2OXkzVTVNS3Y1eFo2Z1JUSnExbUVFS3dCUQ%3D%3D%22%7D","retryCount":2}
2024-12-26T23:10:31.583Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:31.585Z  {"id":"vzHQUIfE3V51je5","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:35.078Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:35.082Z  {"id":"WNS1PyKo0rfXfRP","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:36.384Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:36.386Z  {"id":"QAFS2W4tM9xgsNC","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:36.389Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:36.391Z  {"id":"ZRjGaK9P1JmzRSt","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:41.444Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:41.447Z  {"id":"MKGd3i81GCs5tyT","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:41.461Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":6898,"requestsFinishedPerMinute":127,"requestsFailedPerMinute":0,"requestTotalDurationMillis":5249632,"requestsTotal":761,"crawlerRuntimeMillis":360178,"retryHistogram":[757,4]}
2024-12-26T23:10:42.137Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:42.139Z  {"id":"YFZ9N785da4YNbQ","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:42.247Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":24,"desiredConcurrency":27,"systemStatus":{"isSystemIdle":true,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0.165},"cpuInfo":{"isOverloaded":false,"limitRatio":0.4,"actualRatio":0.4},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:10:42.250Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:42.252Z  {"id":"uypfzkzz3ishgpE","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:47.736Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:47.738Z  {"id":"gTF7Qw4vkWeA1f2","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:47.942Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:47.944Z  {"id":"oN0J5TiSKgEsJbT","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:48.943Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:48.948Z  {"id":"SDsptxPCrUrtHNd","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:55.853Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:55.856Z  {"id":"EbuFLVw7sJeCVZg","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:10:56.641Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:10:56.646Z  {"id":"Hv7P6Fmr8Dpelds","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:11:08.846Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:08.848Z  {"id":"NETrZH1vTEI9ZIS","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:11:09.053Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:09.056Z  {"id":"WXasNg6GzypeTPR","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:11:32.880Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:32.883Z  {"id":"dogcQtl4bl06W43","url":"https://www.instagram.com/api/graphql","retryCount":2}
2024-12-26T23:11:39.432Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:39.434Z  {"id":"dCwZjLGlEFsrl2Q","url":"https://www.instagram.com/api/graphql","retryCount":2}
2024-12-26T23:11:41.536Z INFO  CheerioCrawler:Statistics: CheerioCrawler request statistics: {"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":6825,"requestsFinishedPerMinute":134,"requestsFailedPerMinute":0,"requestTotalDurationMillis":6394647,"requestsTotal":937,"crawlerRuntimeMillis":420252,"retryHistogram":[903,33,1]}
2024-12-26T23:11:42.354Z INFO  CheerioCrawler:AutoscaledPool: state {"currentConcurrency":29,"desiredConcurrency":27,"systemStatus":{"isSystemIdle":false,"memInfo":{"isOverloaded":false,"limitRatio":0.2,"actualRatio":0},"eventLoopInfo":{"isOverloaded":false,"limitRatio":0.7,"actualRatio":0.078},"cpuInfo":{"isOverloaded":true,"limitRatio":0.4,"actualRatio":0.46},"clientInfo":{"isOverloaded":false,"limitRatio":0.3,"actualRatio":0}}}
2024-12-26T23:11:44.038Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:44.041Z  {"id":"uypfzkzz3ishgpE","url":"https://www.instagram.com/api/graphql","retryCount":2}
2024-12-26T23:11:50.773Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:50.776Z  {"id":"cH4iuwuiRWm28AP","url":"https://www.instagram.com/api/graphql","retryCount":1}
2024-12-26T23:11:51.057Z WARN  CheerioCrawler: Reclaiming failed request back to the list or queue. Request blocked, retrying it again with different session
2024-12-26T23:11:51.060Z  {"id":"WXasNg6GzypeTPR","url":"https://www.instagram.com/api/graphql","retryCount":2}
2024-12-26T23:11:59.474Z INFO  Reached max data limit, aborting the run
2024-12-26T23:11:59.542Z INFO  Reached max data limit, aborting the run
2024-12-26T23:11:59.649Z INFO  Reached max data limit, aborting the run
2024-12-26T23:11:59.738Z INFO  CheerioCrawler: Final request statistics: {"requestsFinished":990,"requestsFailed":0,"retryHistogram":[929,57,4],"requestAvgFailedDurationMillis":null,"requestAvgFinishedDurationMillis":6798,"requestsFinishedPerMinute":135,"requestsFailedPerMinute":0,"requestTotalDurationMillis":6729673,"requestsTotal":990,"crawlerRuntimeMillis":438455}
2024-12-26T23:11:59.741Z INFO  CheerioCrawler: Finished! Total 990 requests: 990 succeeded, 0 failed. {"terminal":true}
2024-12-26T23:11:59.754Z INFO  [Status message]: Post scraper finished