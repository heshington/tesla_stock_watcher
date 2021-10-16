import requests
from datetime import datetime, timedelta
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
API_KEY = os.getenv('STOCK_PRICE_API_KEY')
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": ""
}
response = requests.get('https://www.alphavantage.co/query?', params=parameters)
data = response.json()

today_date = datetime.today().strftime('%Y-%m-%d')
yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
day_before_yesterday = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')


yesterday_close_price = data['Time Series (Daily)'][yesterday]['4. close']
yesterday_close_price = float(yesterday_close_price)

day_before_yesterday_close_price = data['Time Series (Daily)'][day_before_yesterday]['4. close']
day_before_yesterday_close_price = float(day_before_yesterday_close_price)
difference = yesterday_close_price - day_before_yesterday_close_price
difference = (difference / yesterday_close_price) * 100
if abs(difference) > 5:
    print("Get News")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
## Get Tesla news
news_parameters = {
    'q':'Tesla',
    'from': today_date,
    'sortBy': 'popularity',
    'apiKey': ''

}
news_response = requests.get('https://newsapi.org/v2/everything?', params=news_parameters)
news_data = news_response.json()

news_articles = news_data['articles']
first_three_articles = []
for i in range(3):
    first_three_articles.append(news_articles[i])
print(len(first_three_articles))



## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

