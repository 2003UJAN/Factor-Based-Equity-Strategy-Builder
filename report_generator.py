# report_generator.py
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Factor-Based Strategy Backtest Report', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, text):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, text)
        self.ln()

def generate_report(symbol, sharpe_ratio, total_return):
    pdf = PDFReport()
    pdf.add_page()
    pdf.chapter_title(f"Stock Symbol: {symbol}")
    pdf.chapter_body(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    pdf.chapter_body(f"Total Return: {total_return:.2f}%")

    file_path = "backtest_report.pdf"
    pdf.output(file_path)
    return file_path
