# Trading Sim — Limit Order Book

A small, dependency-free Python simulation of a price–time-priority **limit order book** with a
matching engine and an interactive command-line interface. Submit buy and sell orders, watch them
match into trades, cancel resting orders, and inspect the state of the book.

## Quick start

Requires Python 3 (standard library only — nothing to install).

```bash
python OrderBook.py
```

You'll get a prompt:

```
Enter action (order/cancel/show/quit):
```

## Commands

| Command  | What it does                                                                 |
| -------- | ---------------------------------------------------------------------------- |
| `order`  | Add a new order. Prompts for side (`buy`/`sell`), price, and quantity.       |
| `cancel` | Remove a resting order from the book by its order ID.                        |
| `show`   | Print the order map, completed trades, best bid/ask, and a book snapshot.    |
| `quit`   | Exit the program.                                                            |

Inputs are validated: side must be `buy` or `sell`, price must be a number greater than 0, and
quantity must be a whole number greater than 0. You'll be re-prompted until the input is valid.

## How matching works

Every new order is run through the matching engine immediately:

- A **buy** order matches against the lowest-priced resting sell orders, as long as the best ask
  price is **less than or equal to** the buy price.
- A **sell** order matches against the highest-priced resting buy orders, as long as the best bid
  price is **greater than or equal to** the sell price.
- Each match executes at the **resting order's price** (the price already on the book), and fills
  the smaller of the two remaining quantities.
- Orders at the same price are matched in the order they arrived (**price–time priority**).
- Any quantity that cannot be matched **rests on the book** and waits for a future counter-order.
- When an order's quantity reaches 0 it is fully filled and marked no longer live.

### Example

1. Add a **buy** for 6 @ $120 — nothing to match, so it rests on the book.
2. Add a **sell** for 5 @ $110 — the resting bid at $120 is ≥ $110, so they trade.

Result: a trade of **5 units @ $120** (the resting bid's price). The buy order has 1 unit left
resting on the book; the sell order is fully filled.

## Reading the `show` output

`show` prints four things. Here's what the numbers mean:

**Order Map** — every order ever submitted, keyed by order ID:

```python
{0: {'side': 'buy', 'price': 120.0, 'qty': 1, 'live': True}, ...}
```
- `qty` is the **remaining** (unfilled) quantity.
- `live` is `True` while the order still rests on the book; `False` once it is fully filled or cancelled.

**Trades** — a list of executed fills, each a tuple:

```python
(fill_quantity, execution_price, aggressor_order_id, resting_order_id)
```
- `aggressor_order_id` is the incoming order that triggered the match.
- `resting_order_id` is the order that was already on the book.

**Best Bid / Best Ask Price ($)** — the highest bid and lowest ask currently on the book, or `-`
if that side is empty.

**Book Snapshot** — live resting orders grouped per side:

```python
{'bids': [(price, qty), ...], 'asks': [(price, qty), ...]}
```
- Bids are sorted highest price first; asks lowest price first.
- Each resting order is listed as its own `(price, qty)` entry (entries are not aggregated by price).

## Using `OrderBook` as a library

The engine is usable directly without the CLI:

```python
from OrderBook import OrderBook

book = OrderBook()

buy_id  = book.add_order("buy", 120, 6)   # returns the new order's ID
sell_id = book.add_order("sell", 110, 5)

book.best_bid()        # -> [price, order_id, qty]  (or None if empty)
book.best_ask()        # -> [price, order_id, qty]  (or None if empty)
book.show_book()       # -> {"bids": [(price, qty), ...], "asks": [(price, qty), ...]}

book.cancel_order(buy_id)   # -> True if cancelled, False if unknown/filled/already cancelled
book.trades                 # list of executed (qty, price, aggressor_id, resting_id) tuples
```

### Implementation notes

- Bids are stored in a max-heap (prices negated) and asks in a min-heap, both as
  `(price, order_id, quantity)` tuples; `order_map` is the source of truth for each order's state.
- **Cancellation uses lazy deletion**: a cancelled order is marked `live = False` and is skipped
  wherever the book is read (`best_bid`, `best_ask`, `show_book`, and the matching loops). Its stale
  heap entry is discarded the next time it surfaces at the top of a heap, so a cancelled order can
  never be matched against.

## Limitations

- In-memory only — state is lost when the program exits.
- Limit orders only (no market, stop, or time-in-force order types).
- Single instrument; no fees, accounts, or balances.
- The book snapshot lists each resting order separately rather than aggregating volume by price level.
