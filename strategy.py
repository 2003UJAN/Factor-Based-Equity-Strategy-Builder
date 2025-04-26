# strategy.py
import backtrader as bt

class FactorBasedStrategy(bt.Strategy):
    params = (
        ("factor", "PERatio"),
        ("ascending", True),  # True: lower factor is better
    )

    def __init__(self):
        pass

    def next(self):
        if not self.position:
            if self.params.ascending:
                if self.data0.close[0] < self.data0.close[-1]:  # dummy factor, refine based on real factor
                    self.buy()
            else:
                if self.data0.close[0] > self.data0.close[-1]:
                    self.buy()
        else:
            if self.data0.close[0] > self.data0.close[-1]:  # dummy exit
                self.sell()
