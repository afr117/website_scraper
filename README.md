GitHub: github.com (For secure, private version control)

Streamlit Community Cloud: share.streamlit.io (For free application hosting)

A Free GitHub Account: To safely store a private copy of the application code.

A Free Streamlit Cloud Account: Linked directly to their GitHub account to serve the user interface live to the web.##
# ⚡ Universal Multi-Product AI Catalog Monitor (Premium Edition)

A professional, zero-overhead web data analysis dashboard. This application allows users to bypass aggressive anti-bot, CAPTCHA, and cloud scraper-blocking frameworks seamlessly by processing the browser's raw rendered DOM structure on-demand via the Google Gemini API.

---

## 📥 Persistent Data Tracking & Download Formats

Once the AI structure engine processes the visual catalog, the data can be locally saved and archived permanently. The dashboard features a **Data Export Control Hub** supporting three distinct tracking formats:

1. **📄 Clean Text Ledger (.txt):** Downloads a structured, human-readable raw text report. Excellent for quick reference, emailing standalone copy logs, or maintaining simple date-stamped file backups.
2. **📊 Spreadsheet Ledger (.csv):** Exports a fully parsed comma-separated data matrix. This format imports seamlessly into **Microsoft Excel**, **Google Sheets**, or any database system for immediate sorting, filtering, and mathematical price tracking.
3. **📋 Markdown Table Snippet:** Formats the entire extracted catalog into an instant markdown code block. Perfect for selecting, copying, and pasting straight into clean note-taking apps like **Notion**, **Obsidian**, or development threads.

---

## 🧩 Project Dependencies

The application relies on the following core Python libraries. These must be declared exactly in your server environment:

* **streamlit**: Powers the responsive front-end dashboard interface.
* **google-genai**: The official SDK optimized for processing deep text blobs with Gemini models.
* **beautifulsoup4**: Handles heavy structural HTML preprocessing and DOM cleaning to maximize AI token efficiency.
* **pandas**: Compiles extracted datasets instantly into downloadable spreadsheet matrices.

---

## 🛠️ Step-by-Step Deployment Guide

### Option A: Deploying Live to the Cloud (Recommended)
1. Sign up for a free account at [GitHub](https://github.com/) and create a new **Private Repository**.
2. Upload the `app.py` and `requirements.txt` files from this ZIP folder directly into your repository.
3. Go to [Streamlit Community Cloud](https://share.streamlit.io/) and log in using your GitHub account.
4. Click **Create app** -> Select your private repository -> Verify the main file path is set to `app.py`.
5. Name your secret custom app URL slug and click **Deploy!** Your cloud monitor will be live in under 60 seconds.

### Option B: Running Locally on Your Laptop
If you prefer to run the application locally on your computer, open your terminal inside the project directory and execute:
```bash
# 1. Install all necessary structural packages
pip install -r requirements.txt

# 2. Boot up the local runtime engine
streamlit run app.py

Advanced Extraction Guide: Copying HTML via Developer Tools
Because modern e-commerce marketplaces employ active script-blockers, the standard "View Source" tab (Ctrl + U) will only copy incomplete skeleton layouts rather than your live results. To extract everything perfectly, you must pull from the active browser memory tree using your target page's Inspect tools.

Method 1: The Fast Element Right-Click (Best for Specific Result Grids)
Open up your target marketplace display screen (e.g., Walmart, Amazon, or eBay).

Right-click directly over one of the product elements or anywhere on the main product grid framework.

Click Inspect to toggle the browser Developer Tools split-screen panel.

Look at the highlighted code block in the elements panel. Scroll up slightly if necessary to find the container tag enclosing the catalog (e.g., <main>, <div id="results">, or the top-level <html> node).

Right-click that specific tag block, navigate to Copy in the context menu, and select Copy outerHTML.

Paste that entire code blob into the live dashboard input block and execute the AI parse sweep.

Method 2: The Element Tree Keyboard Shortcut (Best for Endless Infinite-Scroll Feeds)
Navigate to the marketplace page and scroll down completely to allow all lazy-loading item cards to load on your screen.

Press F12 (or Ctrl + Shift + I on Linux/Windows, Cmd + Option + I on Mac) to launch the Developer Tools console.

Look closely at the top row of the DevTools elements tray and scroll to the very top line where the initial <html> tag declaration resides.

Right-click that main <html> tag line, choose Copy, and select Copy outerHTML.

Drop this payload directly into the monitor text box to pull all compiled listings simultaneously.

🔒 Data Privacy & Architecture Note
Cost Optimization: This software operates on an on-demand engine. It does not run background cloud routines or listen persistently, meaning it uses $0/month in idle cloud operating maintenance fees.

Enterprise Privacy Safeguards: This application runs on Google’s standard free tier for rapid testing. If your business scales to analyze sensitive internal pricing matrices or proprietary supplier catalogs, you can toggle your configuration to a pay-as-you-go key. Doing so costs pennies per thousand searches and automatically locks down the pipeline, opting your data out of any external model training loops entirely.
