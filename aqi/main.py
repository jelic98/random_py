from datetime import date, timedelta
import requests
import json
from random import randrange

out = open("air_quality_index.txt", "w+") 
today = date.today()
aqimax = 500
days = 30

for i in range(0, days):
    d = (today - timedelta(i)).isoformat()

    for j in range(0, 3):
        times = ["09", "12", "15"]

        # Replace LAT, LON, API_KEY
        url = "https://api.breezometer.com/air-quality/v2/historical/hourly?lat=LAT&lon=LON&key=API_KEY&datetime=" + d + "T" + times[j] + ":00:00"

        response = requests.request("GET", url).text

        print(response)

        raw = json.loads(response)
        datetime = raw["data"]["datetime"].split("T")
        date = datetime[0].replace("-", "")
        time = datetime[1].split(":")[0]
        aqi1 = raw["data"]["indexes"]["baqi"]["aqi"]
        aqi2 = aqi1 + randrange(int(aqi1 * 0.1))
        aqi3 = aqi1 + randrange(int(aqi1 * 0.1))

        aqi1 = int((1 - aqi1 * 0.01) * aqimax)
        aqi2 = int((1 - aqi2 * 0.01) * aqimax)
        aqi3 = int((1 - aqi3 * 0.01) * aqimax)

        out.write("{} {} {} {} {}\n".format(date, time, aqi1, aqi2, aqi3))

out.close()
