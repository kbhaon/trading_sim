

## **Description**

- run OrderBook.py to use.
- You will be prompted to either add an order (order), show the book, completed trades, best bid/ask (show), or close the app (quit)
- to add an order you need to specify whether you are buying or selling, the price you want to buy/sell at, and the amount of items you want (using the previously stated side and price).
- If there is an order on the opposite side that is at an acceptable price, the two orders will become a trade and show up in the trades list when you are looking at the show screen.
- For Example, If I add a buy order for 6 items @ $120 and a sell order for 5 items @ 110:
  - There will be a trade consisting of 5 items @ $120 which will be listed under "Trades:" when you type show. This will include the order IDs of the traders as well.
- When an order's quantity hits 0, the trade will not be live anymore as it has been completely filled.

## **TO DO:**

- **Make the show tab more readable**
  - specify which each number in the tuples/dictionaries (trades, best bids/asks, book snapshots) is in a cleaner way. Unless you read the code or pay a lot of attention to all the order IDs, quantities, etc. you wont really know what most of the numbers are when you show the book.

- **Simulate a market by adding randomized orders at random intervals**
  - I will try and set it so the standard deviation is not super large with caps of order sizes and amounts. I don't want random orders of 1 million @ $1000000 being likely.
  - I am envisioning this to be like a random number generator with some price bias that will be predetermined. Maybe I can make this bias slowly shift as well.

- **Move UI to streamlit for easier visibility and use**
  - This will make it a bit more user friendly and would let me implement live graphs and constantly refreshing current prices.
  - I will do this after I am a bit more happy with my CLI though.

