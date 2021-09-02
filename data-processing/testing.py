import requests

res = requests.get(url="https://www.tabroom.com/index/index.mhtml", params={
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "https://www.tabroom.com/index/index.mhtml",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "state=CA&country=US&year=2019&circuit_id=6",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
})

with open('testing.txt', 'w', encoding='utf-8') as f:
  f.write(res.text)
