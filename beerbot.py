#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy, urllib2, random, pickle
from bs4 import BeautifulSoup

try:
	#Twitter credentials, you can get these from https://apps.twitter.com for your account
	CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
	CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
	ACCESS_KEY = 'YOUR_ACCESS_KEY'
	ACCESS_SECRET = 'YOUR_ACCESS_SECRET'

	#Setting up the authentication and API for Twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	#Opening the beer pages with their prices
	beerPages = [
	"https://www.foodie.fi/entry/koff-iii-33-cl-24-pack--tlk-4-5---olut/6415600020947",
	"https://www.foodie.fi/entry/alc-24x0-33l-tlk-salkku-prem-4-5-/6419802022136",
	"https://www.foodie.fi/entry/karhu-iii-24-pack-4-6--33cl-tlk-olut/6415600020152",
	"https://www.foodie.fi/entry/karjala-iii-olut-4-5--0-33l-tolkki-24-pack/6413601094219",
	"https://www.foodie.fi/entry/sandels-4-7---0-33-l-tolkki-24-salkku/6419802020491"
	]
	beerNames = ["Koff 4,5%", "A Le Coq 4,5%", "Karhu 4,6%", "Karjala 4,5%", "Sandels 4,7%"]
	startTweet = u"Hinnat tänään Prismoissa (kontti/tölkki):\n"
	wholePrices = []
	decimalPrices = []
	completePrices = []
	completePricesForOneCan = []
	
	#Main function for handling the beers, their prices and the tweet
	def main():
		beerPage = 0
		while beerPage < len(beerPages):
			page = urllib2.urlopen(beerPages[beerPage])
			soup = BeautifulSoup(page, 'html.parser')
			beerRequest = urllib2.urlopen(beerPages[beerPage])
			beerSoup = BeautifulSoup(beerRequest, 'html.parser')

			for beerWholePrice in beerSoup.find_all('span',  {"class": "whole-number "}):
				wholePrices.append(beerWholePrice.getText())

			for beerDecimalPrice in beerSoup.find_all('span',  {"class": "decimal"}):
				decimalPrices.append(beerDecimalPrice.getText())

			completePrice = wholePrices[beerPage] + "." + decimalPrices[beerPage]
			priceForOneCan = str(float(completePrice) / 24)

			if beerPage == 0:
				tweet = startTweet + beerNames[beerPage] + ": " + completePrice + "/" + priceForOneCan + " euroa\n"
			else:
				tweet = tweet + beerNames[beerPage] + ": " + completePrice + "/" + priceForOneCan + " euroa\n"
			tweet = tweet.replace('.', ',')	
			print(tweet)
			beerPage += 1

		api.update_status(tweet)

	if __name__ == "__main__":
		main()

except Exception as e:
    print(e.message)