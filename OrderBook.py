import heapq
import itertools

class OrderBook:
    def __init__(self):
        self.bids = []
        self.asks = []
        self.counter = itertools.count()
        self.order_map = {}
        self.trades = []


    def add_order(self, order_type, price, quantity):
        order_id = next(self.counter)
        
        self.order_map[order_id] = {"side": order_type, "price": price, "qty": quantity, "live": True}
        
        self.matching_engine(order_id)

        return order_id
    
    def best_bid(self):
        if not self.bids:
            return None
        else:
            return [-self.bids[0][0], self.bids[0][1], self.bids[0][2]]
    
    
    def best_ask(self):
        if not self.asks:
            return None
        else:
            return [self.asks[0][0], self.asks[0][1], self.asks[0][2]]
    
    def show_book(self):
        bids_sorted = sorted([(-p, q) for (p, _, q) in self.bids], reverse=True)
        asks_sorted = sorted([(p, q) for (p, _, q) in self.asks])
        return {"bids": bids_sorted, "asks": asks_sorted}

    def matching_engine(self, order_id):
        order = self.order_map[order_id]
        side, price, remaining = order["side"], order["price"], order["qty"]

        if side == "buy":
            while remaining > 0 and self.asks and self.asks[0][0] <= price:
                ask_price, ask_id, ask_qty = self.asks[0]
                fill = min(remaining, ask_qty)

                self.trades.append((fill, ask_price, order_id, ask_id))

                remaining -= fill
                self.order_map[ask_id]["qty"] -= fill
            
                if self.order_map[ask_id]["qty"] == 0:
                    heapq.heappop(self.asks)
                    self.order_map[ask_id]["live"] = False
                else:
                    heapq.heappop(self.asks)
                    heapq.heappush(self.asks, (ask_price, ask_id, self.order_map[ask_id]["qty"]))
            
            if remaining > 0:
                heapq.heappush(self.bids, (-price, order_id, remaining))
                self.order_map[order_id]["qty"] = remaining
            else:
                self.order_map[order_id]["qty"] = 0
                self.order_map[order_id]["live"] = False
            
        elif side == "sell":
            while remaining > 0 and self.bids and (-self.bids[0][0]) >= price:
                bid_price_neg, bid_id, bid_qty = self.bids[0]
                bid_price = -bid_price_neg
                fill = min(remaining, bid_qty)

                self.trades.append((fill, bid_price, order_id, bid_id))

                remaining -= fill
                self.order_map[bid_id]["qty"] -= fill

                if self.order_map[bid_id]["qty"] == 0:
                    heapq.heappop(self.bids)
                    self.order_map[bid_id]["live"] = False
                else:
                    heapq.heappop(self.bids)
                    heapq.heappush(self.bids, (-bid_price, bid_id, self.order_map[bid_id]["qty"]))

            if remaining > 0:
                heapq.heappush(self.asks, (price, order_id, remaining))
                self.order_map[order_id]["qty"] = remaining
            else:
                self.order_map[order_id]["qty"] = 0
                self.order_map[order_id]["live"] = False


if __name__ == "__main__":
    book = OrderBook()

    while True:
        action = input("Enter action (order/show/quit): ").strip().lower()

        if action == "order":
            while True:
                    side = input("Side (buy/sell): ").strip().lower()
                    if side in ("buy", "sell"):
                        break
                    else: print("Invalid input. Use 'buy' or 'sell'.")

            while True:
                    try:
                        price = float(input("Price: "))
                        if price > 0:
                            break
                        else:
                            print("Invalid input. Please put a value above 0.")
                    except ValueError:
                        print("Invalid number. please enter a positive number greater than 0")

            while True:
                    try:
                        qty = int(input("Quantity: "))
                        if qty > 0:
                            break
                        else:
                            print("Invalid input. Please put a value above 0.")
                    except ValueError:
                        print("Invalid number. please enter a positive number greater than 0")
                
            order_id = book.add_order(side, price, qty)
            print(f"Order {order_id} added: {side} {qty}@{price}")

        elif action == "show":
            bb = book.best_bid()
            ba = book.best_ask()
            print("Order Map:", book.order_map)
            print("Trades:", book.trades)
            print("Best Bid Price ($): " + str(bb[0]) if bb != None else "Best Bid Price ($): -")
            print("Best Ask Price ($): " + str(ba[0]) if ba != None else "Best Bid Price ($): -")
            print("Book Snapshot:", book.show_book())

        elif action == "quit":
            break

        else:
            print("Invalid action. Use 'order', 'show', or 'quit'.")




