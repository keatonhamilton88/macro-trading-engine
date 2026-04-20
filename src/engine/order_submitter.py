from ib_insync import MarketOrder, LimitOrder, StopOrder

class OrderSubmitter:
    def __init__(self, ib_instance):
        self.ib = ib_instance

    def submit_bracket_order(self, contract, action, quantity, entry_price, stop_loss_price, take_profit_price):
        """
        Submits a bracket order: Entry + Stop Loss + Take Profit.
        Uses Market for entry if desired, or Limit for precision.
        """
        # 1. Qualify the contract to fill in missing IDs (conId, etc.)
        self.ib.qualifyContracts(contract)

        # 2. Define the Parent Order (The Entry)
        # Using a LimitOrder here for price control, set transmit=False
        parent = LimitOrder(action, quantity, entry_price)
        parent.orderId = self.ib.client.getReqId()
        parent.transmit = False

        # 3. Define the Stop Loss (The Protection)
        reverse_action = 'SELL' if action == 'BUY' else 'BUY'
        stop_loss = StopOrder(reverse_action, quantity, stop_loss_price)
        stop_loss.parentId = parent.orderId
        stop_loss.transmit = False

        # 4. Define the Take Profit (The Exit)
        take_profit = LimitOrder(reverse_action, quantity, take_profit_price)
        take_profit.parentId = parent.orderId
        take_profit.transmit = True  # Set to True to send the whole bracket

        # 5. Place the orders
        bracket = [parent, stop_loss, take_profit]
        trades = [self.ib.placeOrder(contract, o) for o in bracket]
        
        print(f"✅ Bracket Order Submitted for {contract.localSymbol}: {action} {quantity}")
        return trades
