from datetime import datetime, timedelta

class RollManager:
    def __init__(self, ib_instance):
        self.ib = ib_instance

    def scan_for_rolls(self):
        """Checks all active futures for approaching expiry."""
        positions = self.ib.positions()
        roll_report = []

        for pos in positions:
            if pos.contract.secType == 'FUT':
                # Fetch details to get the last trading day
                details = self.ib.reqContractDetails(pos.contract)[0]
                expiry_str = details.contract.lastTradeDateOrContractMonth
                expiry_date = datetime.strptime(expiry_str, '%Y%m%d')
                
                days_to_expiry = (expiry_date - datetime.now()).days
                
                # CRITICAL: Roll 10 days before expiry to avoid 'Close-Only' mode
                if days_to_expiry <= 10:
                    roll_report.append({
                        "symbol": pos.contract.symbol,
                        "days_left": days_to_expiry,
                        "action": "ROLL REQUIRED"
                    })
        
        return roll_report
