# backtest_engine.py
import backtrader as bt
from strategy import FactorBasedStrategy

def run_backtest(data, factor="PERatio", ascending=True):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(FactorBasedStrategy, factor=factor, ascending=ascending)

    datafeed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(datafeed)

    cerebro.broker.set_cash(100000.0)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(bt.analyzers.Returns, _name="returns")
    results = cerebro.run()
    sharpe = results[0].analyzers.sharpe.get_analysis()
    returns = results[0].analyzers.returns.get_analysis()

    return cerebro, sharpe, returns
