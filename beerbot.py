#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
import urllib2
from bs4 import BeautifulSoup

try:
    # Twitter credentials
    # You can get these from https://apps.twitter.com for your account
    CONSUMER_KEY: str = "YOUR_CONSUMER_KEY"
    CONSUMER_SECRET: str = "YOUR_CONSUMER_SECRET"
    ACCESS_KEY: str = "YOUR_ACCESS_KEY"
    ACCESS_SECRET: str = "YOUR_ACCESS_SECRET"

    # Setting up the authentication and API for Twitter
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    # Opening the beer pages with their prices
    beer_pages: list = [
        "https://www.foodie.fi/entry/koff-iii-33-cl-24-pack--tlk-4-5---olut/6415600020947",
        "https://www.foodie.fi/entry/alc-24x0-33l-tlk-salkku-prem-4-5-/6419802022136",
        "https://www.foodie.fi/entry/karhu-iii-24-pack-4-6--33cl-tlk-olut/6415600020152",
        "https://www.foodie.fi/entry/karjala-iii-olut-4-5--0-33l-tolkki-24-pack/6413601094219",
        "https://www.foodie.fi/entry/sandels-4-7---0-33-l-tolkki-24-salkku/6419802020491",
    ]
    beer_names: list = [
        "Koff 4,5%",
        "A Le Coq 4,5%",
        "Karhu 4,6%",
        "Karjala 4,5%",
        "Sandels 4,7%",
    ]
    start_tweet: str = "Hinnat tänään Prismoissa (kontti/tölkki):\n"
    whole_prices: list = []
    decimal_prices: list = []
    complete_prices: list = []

    # Main function for handling the beers, their prices and the tweet
    def main():
        beer_page: int = 0
        while beer_page < len(beer_pages):
            page = urllib2.urlopen(beer_pages[beer_page])
            BeautifulSoup(page, "html.parser")
            beer_request = urllib2.urlopen(beer_pages[beer_page])
            beer_soup = BeautifulSoup(beer_request, "html.parser")

            for beerWholePrice in beer_soup.find_all(
                "span", {"class": "whole-number "}
            ):
                whole_prices.append(beerWholePrice.getText())

            for beer_decimal_price in beer_soup.find_all("span", {"class": "decimal"}):
                decimal_prices.append(beer_decimal_price.getText())

            complete_price: str = (
                whole_prices[beer_page] + "." + decimal_prices[beer_page]
            )
            price_for_one_can: str = str(float(complete_price) / 24)

            if beer_page == 0:
                tweet = (
                    start_tweet
                    + beer_names[beer_page]
                    + ": "
                    + complete_price
                    + "/"
                    + price_for_one_can
                    + " euroa\n"
                )
            else:
                tweet = (
                    tweet
                    + beer_names[beer_page]
                    + ": "
                    + complete_price
                    + "/"
                    + price_for_one_can
                    + " euroa\n"
                )
            tweet = tweet.replace(".", ",")
            beer_page += 1

        api.update_status(tweet)

    if __name__ == "__main__":
        main()

except Exception as e:
    print(e.message)
