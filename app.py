import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
import time
from bs4 import BeautifulSoup
import pandas as pd

# -------------------------------------------------------------------------
# 1. STRUCTURING THE DATA TO HANDLE MULTIPLE PRODUCTS
# -------------------------------------------------------------------------
class ProductItem(BaseModel):
    title: str = Field(description="The full title or name of the specific product.")
    price: float = Field(description="The extracted current price as a float. Do not include currency symbols. If missing, default to 0.0.")
    rating: str = Field(description="The star rating or numerical rating score (e.g., '4.5 out of 5 stars', '4.2'). If missing, default to 'N/A'.")

class ScrapedCatalog(BaseModel):
    total_items_found: int = Field(description="The total number of separate products identified in the page context text.")
    products: List[ProductItem] = Field(description="An array containing every distinct product item extracted from the text context.")

# -------------------------------------------------------------------------
# 2. OPTIMIZED DOM CLEANING ENGINE
# -------------------------------------------------------------------------
def clean_and_package_html(raw_html_or_text: str):
    """
    Cleans raw HTML or source text by stripping heavy code tags to maximize 
    token efficiency and prevent context window clipping.
    """
    soup = BeautifulSoup(raw_html_or_text, 'html.parser')
    
    # Strip heavy codes that contain no catalog text data
    for script in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        script.extract()
        
    main_content = soup.find("main") or soup.find("div", {"id": "maincontent"}) or soup
    body_text = main_content.get_text(separator=" | ", strip=True)
    
    return {
        "title": soup.find("title").get_text(strip=True) if soup.find("title") else "Rendered DOM Analysis",
        "body_snippet": body_text[:250000] # Supports massive DOM structures from infinite scroll feeds
    }

def analyze_catalog_with_gemini(scraped_data: dict, api_key: str) -> ScrapedCatalog:
    """
    Leverages Gemini structuring engine to compile an exhaustive list of all items.
    """
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an advanced retail data extractor. Scan the entire text context provided below:
    Context Title: {scraped_data['title']}
    Page Content Blob: {scraped_data['body_snippet']}
    
    Identify EVERY single distinct commercial product or gift listing visible in the text frame from beginning to end. 
    For each item, capture its title, its exact price, and its star/user rating.
    """
    
    models_to_try = ['gemini-2.5-flash', 'gemini-1.5-flash']
    
    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ScrapedCatalog,
                        system_instruction=(
                            "You are a meticulous data loop analyzer. Do not summarize, do not truncate, and do not stop early. "
                            "Exhaustively parse every single product card mentioned in the text blob. "
                            "If multiple prices exist for an item, pick the main list price or active sale price."
                        ),
                        temperature=0.1
                    ),
                )
                return ScrapedCatalog.model_validate_json(response.text)
            except Exception as e:
                if "503" in str(e) and attempt == 0:
                    time.sleep(2)
                    continue
                break
                
    raise RuntimeError("The AI data extraction processing nodes are currently busy. Please retry.")

# -------------------------------------------------------------------------
# 3. HELPER FUNCTIONS FOR EXPORT FORMATTING
# -------------------------------------------------------------------------
def convert_to_text_report(products: List[ProductItem], title: str) -> str:
    """Generates a clean, human-readable text ledger report."""
    report = f"==================================================\n"
    report += f"AI CATALOG REPORT: {title.upper()}\n"
    report += f"Total Items Tracked: {len(products)}\n"
    report += f"==================================================\n\n"
    
    for idx, item in enumerate(products, start=1):
        report += f"📦 ITEM #{idx}\n"
        report += f"Title:  {item.title}\n"
        report += f"Price:  ${item.price:.2f}\n"
        report += f"Rating: {item.rating}\n"
        report += f"--------------------------------------------------\n"
    return report

def convert_to_markdown_table(products: List[ProductItem]) -> str:
    """Generates a markdown table block easily copied to clipboard notes."""
    markdown = "| # | Product Title | Price | Customer Rating |\n"
    markdown += "|---|---|---|---|\n"
    for idx, item in enumerate(products, start=1):
        clean_title = item.title.replace("|", "-") # Prevent breaking columns
        markdown += f"| {idx} | {clean_title} | ${item.price:.2f} | {item.rating} |\n"
    return markdown

# -------------------------------------------------------------------------
# 4. HIGH-END STREAMLIT INTERFACE WITH PREMIUM VISUAL LAYOUT
# -------------------------------------------------------------------------
st.set_page_config(page_title="AI Catalog Monitor", page_icon="⚡", layout="wide")

# Injection of custom CSS styling to modernize visual components (Fixed Typo Here)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Apply smooth typography adjustments */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        /* Modern Glassmorphic Container Blocks */
        .product-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .product-card:hover {
            transform: translateY(-4px);
            border-color: #FF4B4B;
        }
        
        /* Clean Title Badge Styles */
        .badge-index {
            background-color: #FF4B4B;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 12px;
        }
        
        /* Visual adjustments for data display values */
        .value-accent {
            font-size: 1.6rem;
            font-weight: 700;
            color: #10B981;
            margin-top: 4px;
        }
        .rating-accent {
            font-size: 1.1rem;
            font-weight: 600;
            color: #FBBF24;
            margin-top: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# App branding and contextual headings
st.title("⚡ Universal Multi-Product AI Catalog Monitor")
st.caption("Instantly decode dynamic browser DOM trees into pristine structured catalog visualizations.")

with st.sidebar:
    st.header("🔑 Authentication")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Input your secret Google AI Studio token key here.")
    st.markdown("---")
    st.info("💡 **Pro-Tip:** Open your target marketplace layout screen, inspect the core page element, copy the outerHTML node structure, and drop it straight into the input terminal frame.")

st.markdown("### 📋 Live DOM Payload Input")
pasted_source = st.text_area(
    "Paste Webpage Source Code Context", 
    height=250,
    placeholder="🎯 Right-click page element -> Click 'Inspect' -> Right-click the <html> block -> Select 'Copy' -> Click 'Copy outerHTML' -> Paste here..."
)

if st.button("🚀 Run AI Structure Engine", type="primary"):
    if not gemini_key:
        st.error("Authentication Missing: Please check and supply your Gemini API key inside the sidebar terminal.")
    elif not pasted_source:
        st.error("Context Missing: Please copy and paste valid structural page source text data to proceed.")
    else:
        with st.spinner("Processing DOM map layers and running deep AI validation sweeps..."):
            try:
                # Clean up the pasted HTML structure
                scraped_payload = clean_and_package_html(pasted_source)
                
                # Send the clean snippet to Gemini
                catalog_result = analyze_catalog_with_gemini(scraped_payload, gemini_key)
                
                st.balloons()
                st.success(f"Parsing Sequence Complete: Successfully structured {catalog_result.total_items_found} target items.")
                st.markdown("---")
                
                if catalog_result.products:
                    # -----------------------------------------------------
                    # THE EXPORT & DOWNLOAD HUB
                    # -----------------------------------------------------
                    st.markdown("### 📥 Data Export Controls")
                    
                    # Process data structures for download objects
                    text_report_data = convert_to_text_report(catalog_result.products, scraped_payload["title"])
                    markdown_table_str = convert_to_markdown_table(catalog_result.products)
                    
                    # Convert to Pandas DataFrame for a clean spreadsheet download
                    df_items = pd.DataFrame([{
                        "Item Number": i+1,
                        "Product Title": p.title,
                        "Price ($)": p.price,
                        "Rating": p.rating
                    } for i, p in enumerate(catalog_result.products)])
                    csv_bytes = df_items.to_csv(index=False).encode('utf-8')
                    
                    exp_col1, exp_col2, exp_col3 = st.columns(3)
                    with exp_col1:
                        st.download_button(
                            label="📄 Download Text Ledger (.txt)",
                            data=text_report_data,
                            file_name="scraped_catalog_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with exp_col2:
                        st.download_button(
                            label="📊 Export Spreadsheet Ledger (.csv)",
                            data=csv_bytes,
                            file_name="scraped_catalog_spreadsheet.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    with exp_col3:
                        with st.popover("📋 Capture Markdown Table String", use_container_width=True):
                            st.text_area("Copy markdown syntax snapshot below:", markdown_table_str, height=200)
                    
                    st.markdown("---")
                    
                    # -----------------------------------------------------
                    # PRODUCT VISUALIZATION GRID
                    # -----------------------------------------------------
                    st.markdown("### 📦 Extracted Catalog View")
                    cols = st.columns(3)
                    for index, item in enumerate(catalog_result.products):
                        current_col = cols[index % 3]
                        with current_col:
                            # Render custom stylized HTML card inside column container
                            display_title = f"{item.title[:65]}..." if len(item.title) > 65 else item.title
                            price_display = f"${item.price:.2f}" if item.price > 0 else "N/A"
                            
                            st.markdown(f"""
                                <div class="product-card">
                                    <div class="badge-index">ITEM #{index + 1}</div>
                                    <div style="font-weight: 600; font-size: 1rem; margin-bottom: 12px; min-height: 48px;">{display_title}</div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px;">
                                        <div>
                                            <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.7;">Target Price</div>
                                            <div class="value-accent">{price_display}</div>
                                        </div>
                                        <div style="text-align: right;">
                                            <div style="font-size: 0.75rem; text-transform: uppercase; opacity: 0.7;">Rating</div>
                                            <div class="rating-accent">⭐ {item.rating}</div>
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("Structure Resolution Empty: No items could be resolved from this configuration context window.")
            except Exception as ai_err:
                st.error(f"Processing Matrix Exception: {ai_err}")
