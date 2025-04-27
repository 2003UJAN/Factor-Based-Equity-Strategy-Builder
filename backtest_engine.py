# backtest_engine.py
import backtrader as bt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

class FactorBasedStrategy(bt.Strategy):
    params = dict(factor='PERatio', ascending=True)

    def __init__(self):
        pass

    def next(self):
        if not self.position:
            self.buy()
        elif self.data.close[0] < self.data.close[-1]:
            self.sell()

def run_backtest(data, factor="PERatio", ascending=True, benchmark_data=None):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(FactorBasedStrategy, factor=factor, ascending=ascending)

    datafeed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(datafeed)

    if benchmark_data is not None:
        benchmark_feed = bt.feeds.PandasData(dataname=benchmark_data)
        cerebro.adddata(benchmark_feed)

    cerebro.broker.set_cash(100000.0)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")

    results = cerebro.run()
    sharpe = results[0].analyzers.sharpe.get_analysis()
    returns = results[0].analyzers.returns.get_analysis()

    buf = io.BytesIO()
    cerebro.plot(style='candlestick')[0][0].savefig(buf, format='png')
    buf.seek(0)

    return buf, sharpe, returns
