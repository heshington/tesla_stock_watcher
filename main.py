import requests
from datetime import datetime, timedelta
import os
from twilio.rest import Client
from decouple import config


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
API_KEY = os.getenv('STOCK_PRICE_API_KEY')
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": config('STOCK_PRICE_API_KEY')
}

response = requests.get('https://www.alphavantage.co/query?', params=parameters)
data = response.json()

today_date = datetime.today().strftime('%Y-%m-%d')
yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
day_before_yesterday = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
try:
    yesterday_close_price = data['Time Series (Daily)'][yesterday]['4. close']
    yesterday_close_price = float(yesterday_close_price)
    day_before_yesterday_close_price = data['Time Series (Daily)'][day_before_yesterday]['4. close']
    day_before_yesterday_close_price = float(day_before_yesterday_close_price)
    difference = yesterday_close_price - day_before_yesterday_close_price
    difference = (difference / yesterday_close_price) * 100

    difference = round(difference, 2)
    if difference < -5 or difference > 5:
        print("Get News")
    print(f"The differnce in price is {difference}")

    news_parameters = {
        'q': 'Tesla',
        'from': today_date,
        'sortBy': 'relevancy',
        'language': 'en',
        'apiKey': config('NEWS_API')
    }

    news_response = requests.get('https://newsapi.org/v2/everything?', params=news_parameters)
    news_data = news_response.json()
    print(news_data)
    news_articles = news_data['articles']
    first_three_articles = []
    for i in range(3):
        first_three_articles.append(news_articles[i])
    print(first_three_articles)

    ## STEP 3: Use https://www.twilio.com
    # Send a seperate message with the percentage change and each article's title and description to your phone number.

    account_sid = config('TWILIO_ACCOUNT_SID')
    auth_token = config('TWILIO_AUTH_TOKEN')

    client = Client(account_sid, auth_token)
    emoji = ""
    if difference > 0:
        emoji = '🔺'
    else:
        emoji = '🔻'
    print(f"{STOCK} {emoji}{difference}% \n")
    print(f"Headline: {first_three_articles[0]['title']} \n \n"
          f"Brief: {first_three_articles[0]['description']} \n\n"

          f"Headline: {first_three_articles[1]['title']} \n \n"
          f"Brief: {first_three_articles[1]['description']}\n\n"

          f"Headline: {first_three_articles[2]['title']} \n \n"
          f"Brief: {first_three_articles[2]['description']}", )

    message = client.messages \
        .create(
        body=f"{STOCK} {emoji}{difference}% \n"
             f"Headline: {first_three_articles[0]['title']} \n \n"
             f"Brief: {first_three_articles[0]['description']}\n"
             f"Headline: {first_three_articles[1]['title']} \n \n"
             f"Brief: {first_three_articles[1]['description']}\n"
             f"Headline: {first_three_articles[2]['title']} \n \n"
             f"Brief: {first_three_articles[2]['description']}",
        from_='+12677192839',
        to='+64278496433'
    )

    print(message.status)
except KeyError:
    print("There was no trading yesterday, check again later.")




## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
## Get Tesla news


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
