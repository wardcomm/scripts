#curl.exe --user bitcoinipvision --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "move", "params": ["acc-1", "acc-2", 6, 5, "happy birthday!"] }' -H 'content-type: application/json;' http://localhost:18332/

#curl -X POST -H 'Content-Type: application/json' --data '{ "query": '{ hello }' }' 'https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm'

#In

#Invoke-WebRequest -Uri https://ovmdmgr04:7002/ovm/core/wsapi/rest/Vm -UseDefaultCredentials -UserAgent p2906297 -WebSession THem5dax
Invoke-WebRequest -Uri https://ovmdmgr04:7002/ovm/core/wsapi/rest/ -Headers     'Content-Type': "application/json",'Accept': "application/json",'Authorization': "Basic cDI5MDYyOTc6VEhlbTVkYXg=",'User-Agent': "PostmanRuntime/7.17.1",'Cache-Control': "no-cache",'Postman-Token': "431c60f2-8109-462a-9c6d-f062c37cc795,ce167c43-2f95-4601-b2df-8c6616bfe381",'Host': "ovmdmgr04:7002",'Accept-Encoding': "gzip, deflate",'Content-Length': "477",'Cookie': "JSESSIONID=TBWXvH2bw17BlC7xx08ECcibPZi8g7d5n_2ECy-XPp-sIWYrQART!-1473086762; _WL_AUTHCOOKIE_JSESSIONID=JMkwEFrfUDwkltPzHv9O",'Connection': "keep-alive",'cache-control': "no-cache" -UseDefaultCredentials -UserAgent p2906297 -WebSession THem5dax