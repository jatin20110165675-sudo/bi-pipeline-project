import pandas as pd

# ── Extract ───────────────────────────────────
superstore = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
financial  = pd.read_excel('Financial Sample.xlsx')

print("Superstore shape:", superstore.shape)
print("Financial shape:", financial.shape)

# ── Transform Superstore ──────────────────────
superstore = superstore[[
    'Order Date', 'Segment', 'Country',
    'Category', 'Sales', 'Profit', 'Quantity'
]]
superstore['Source']       = 'Superstore'
superstore['Profit_Margin'] = (superstore['Profit'] / superstore['Sales'] * 100).round(2)
superstore['COGS']          = superstore['Sales'] - superstore['Profit']
superstore                   = superstore.rename(columns={'Order Date': 'Date', 'Category': 'Product'})

# ── Transform Financial ───────────────────────
financial = financial[[
    'Date', 'Segment', 'Country',
    'Product', 'Sales', 'Profit', 'Units Sold'
]]
financial['Source']       = 'Financial'
financial['Profit_Margin'] = (financial['Profit'] / financial['Sales'] * 100).round(2)
financial['COGS']          = financial['Sales'] - financial['Profit']
financial                   = financial.rename(columns={'Units Sold': 'Quantity'})

# ── Load (Merge both datasets) ────────────────
combined = pd.concat([superstore, financial], ignore_index=True)
combined['Date'] = pd.to_datetime(combined['Date'], errors='coerce')
combined['Year'] = combined['Date'].dt.year
combined['Month'] = combined['Date'].dt.strftime('%b %Y')
combined = combined.dropna(subset=['Sales', 'Profit'])

print(f"Combined dataset: {len(combined)} rows")
print(f"Sources: {combined['Source'].value_counts().to_dict()}")
print(f"Countries: {combined['Country'].nunique()}")
print(f"Years: {sorted(combined['Year'].dropna().unique().astype(int).tolist())}")

# ── Export ────────────────────────────────────
combined.to_csv('combined_business_data.csv', index=False)
print("✓ Saved: combined_business_data.csv")
from sqlalchemy import create_engine

# ── Push to MySQL ─────────────────────────────
engine = create_engine(
    'mysql+pymysql://root:Jatin123@localhost/bi_pipeline'
)

combined.to_sql(
    'business_data',
    con=engine,
    if_exists='replace',
    index=False
)
print("✓ Loaded to MySQL: bi_pipeline.business_data")