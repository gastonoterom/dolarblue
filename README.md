# Dolar blue rest API

## Introduction
Dolar Blue Rest API is a backend service for fetching and the price for the "Dolar Blue" in Argentina from the most popular sources.

Argentina has a lifelong issue with its currency: The Argentinian Peso. One of the measures our govt. took to battle its ongoing deprecation is to limit the purchase of US dollars (and any other currency) to its citizens.

The average Argentinian is not able to go to the bank and get rid of his/her hard-earned Argentinian pesos (by buying foreign currency), which becomes worthless after a couple of months because of our rampant inflation levels.

So, the average Argentinian has to resort to the "unregulated" currency market, but of course, that has its flaws: there is no standardized/centralized way to know the price of the US dollar. The parallel (BLUE) market seems like a libertarian's utopia, everything is regulated by pure supply and demand. The catch is that there are many different sources to get the current price of the "Dolar Blue", so this API serves as a way to at least try to centralize and group the most popular sources into only one place.

The "Dolar Blue" refers to how we call the unregulated US dollar in the parallel markets.

## Services

This API has two layers of communication: a REST API and a Telegram bot. It will also have a python SDK in the future for easier usage.

### Rest API

The REST API is not yet published.
The rest API base URL will be https://api.gastonotero.com/dolarblue
The complete documentation of the REST API will be soon published.

### Telegram bot

The Telegram bot is currently in an early Alpha state, so it may be down when you test it.
The bot is found at telegram as [@dolarblue_ars_bot](https://t.me/dolarblue_ars_bot)

## Tech stack

This project uses Python as the main programming language. It scrapes the different sources with beautifulsoup4 and saves the data to a Redis cache for quick access. Flask is used as the backend server for the REST API, and the python-telegram-bot package as the API layer for Telegram.