import markdown
from weasyprint import HTML, CSS
from langchain_core.tools import tool
from typing import Annotated
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")
# import markdown2
# from reportlab.platypus import SimpleDocTemplate, Paragraph
# from reportlab.lib.styles import getSampleStyleSheet

# import pypandoc

WORKING_DIRECTORY = Path(__file__).parent.parent.parent / "summaries"
WORKING_DIRECTORY.mkdir(parents=True, exist_ok=True)
FILE_NAME = "report.pdf"

@tool
def create_pdf_tool(
    content: Annotated[str, "Markdown Content that should be written into the document"]
) -> Annotated[str, "Path of the saved document file"]:
    """
    PDF creation tool from markdown content
    """
    # Markdown content
    md_text = content

    # ✅ Convert Markdown to HTML
    html_body = markdown.markdown(md_text, extensions=["extra", "sane_lists"])

    # ✅ Wrap inside a full HTML page with CSS
    html_full = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 10px;
        }}
        h3 {{
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 10px;
        }}
        ul {{
        margin-bottom: 15px;
        }}
        li {{
        margin-bottom: 6px;
        }}
        strong {{
        color: #000;
        }}
    </style>
    </head>
    <body>
    {html_body}
    </body>
    </html>
    """

    # ✅ Generate proper PDF
    HTML(string=html_full).write_pdf("report.pdf")

    return "PDF saved as report.pdf"

# @tool
# def pdf_maker(query:str):
#     """_summary_
#     """
#     # Convert Markdown to HTML
#     markdown_text = query
#     output = pypandoc.convert_text(
#     markdown_text, 
#     to="pdf", 
#     format="md", 
#     outputfile="output.pdf", 
#     extra_args=['--standalone']
#     )

#     print("PDF saved as output.pdf")


if __name__ == "__main__":
    query = """
### Market Snapshot:
bhau
- **GDP Growth Rate**: India's GDP growth rate for the fiscal year 2025 is reported at 6.5%, driven by strong private consumption and investments. (Source: Deloitte)
- **Sector Contribution**: The services sector dominates the economy, contributing 54.7%, followed by industry at 27.6% and agriculture at 17.7%. (Source: Wikipedia)
- **Recent Quarter Growth**: The Indian GDP expanded by 5.4% in the September quarter of 2024, down from 6.7% in the previous quarter. (Source: Trading Economics)

### Key Financial Events:
- **GDP Growth Projection**: The Reserve Bank of India (RBI) projects a growth rate of 6.5% for FY26, indicating continued economic expansion. (Source: IBEF)
- **Inflation Rate**: The average consumer price inflation rate is 4.2%, reflecting controlled price levels. (Source: IMF)

### Data & Sources (with timestamps):
1. **Deloitte**: India's GDP growth for FY25 is 6.5%, supported by domestic demand and easing inflation. (Recent)
2. **World Bank Data**: Confirms India's GDP growth rate of 6.5%. (Recent)
3. **Trading Economics**: Reports a 5.4% GDP growth in Q3 2024. (Recent)
4. **IMF DataMapper**: Provides detailed metrics including real GDP growth and per capita growth. (Recent)
5. **Wikipedia**: Sector-wise contribution to GDP. (Recent)
6. **IBEF**: Projects 6.5% growth for FY26. (Recent)
7. **World Bank**: GDP and per capita growth figures. (Recent)
8. **IMF**: Real GDP growth and inflation rates. (Recent)

### Investment/Business Implications:
- **Positive Outlook**: The consistent GDP growth rate and controlled inflation suggest a stable economic environment, making India an attractive destination for investments.
- **Sector Opportunities**: The dominance of the services sector, coupled with contributions from industry and agriculture, presents diverse investment opportunities across sectors.
- **Consumer Demand**: Strong private consumption and investments indicate resilient domestic demand, favorable for businesses and investors.

Overall, the Indian economy is showing signs of steady growth, supported by strong domestic demand and a stable inflation environment, making it an attractive market for investors and businesses.
"""

    
    create_pdf_tool.invoke(query)
    # pdf_maker.invoke(query)
    
    
    