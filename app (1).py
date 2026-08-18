import streamlit as st
import pandas as pd
import numpy as np
import re
import ast
from urllib.parse import quote

# ============================================================
# MYNTRA AI ASSISTANT - STREAMLIT APP
# ============================================================

st.set_page_config(
    page_title="Myntra AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = "Fashion Dataset.csv"

# -----------------------------
# Session state
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "wishlist" not in st.session_state:
    st.session_state.wishlist = []
if "bag" not in st.session_state:
    st.session_state.bag = []
if "cart" not in st.session_state:
    st.session_state.cart = []
if "search_text" not in st.session_state:
    st.session_state.search_text = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = None

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
@import url('<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 12% 8%, rgba(228,0,115,.12), transparent 40%),
      radial-gradient(circle at 88% 15%, rgba(138,0,95,.10), transparent 42%),
      radial-gradient(circle at 50% 90%, rgba(230,0,120,.08), transparent 45%),
      linear-gradient(180deg, #fdf3fa 0%, #fff 45%, #fdf3fa 100%);
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #65005f 0%, #9b087f 52%, #e5006d 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
    font-family: 'Outfit', sans-serif;
}

.brand-box {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(18px) saturate(160%);
    -webkit-backdrop-filter: blur(18px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.55);
    border: 1px solid #f2c5e5;
    border-radius: 24px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 8px 25px rgba(116, 0, 92, .08);
}

.brand-title {
    font-size: 34px;
    font-weight: 800;
    background: linear-gradient(90deg,#8a005f,#e40073);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-sub {
    color: #6f5269;
    font-size: 14px;
    margin-top: 3px;
}

.hero {
    border-radius: 28px;
    padding: 42px 48px;
    background:
      radial-gradient(circle at 10% 20%, rgba(255,255,255,.25), transparent 25%),
      linear-gradient(115deg, rgba(104,0,95,.85), rgba(166,0,131,.85) 48%, rgba(224,0,118,.85));
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.25);
    color: white;
    box-shadow: 0 15px 40px rgba(105,0,91,.20);
    margin-bottom: 22px;
}

.hero h1 {
    font-size: 44px;
    margin: 0;
    font-weight: 800;
}

.hero p {
    font-size: 17px;
    margin-top: 8px;
    color: #ffeaf8;
}

.search-wrap {
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.55);
    padding: 14px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,.10);
    margin-top: 24px;
}

.section-title {
    font-size: 27px;
    font-weight: 800;
    color: #3e1837;
    margin: 26px 0 12px;
}

.metric-card {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.55);
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 8px 24px rgba(70,0,60,.10);
}

.metric-number {
    font-size: 29px;
    font-weight: 800;
    color: #9a006d;
}

.metric-label {
    color: #806579;
    font-size: 13px;
}

.cat-card {
    background: rgba(255, 255, 255, 0.4);
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.55);
    border-radius: 20px;
    padding: 10px 8px 14px;
    text-align: center;
    box-shadow: 0 8px 22px rgba(60,0,50,.08);
}

.cat-icon {
    width: 82px;
    height: 82px;
    border-radius: 50%;
    margin: 0 auto 8px;
    background: linear-gradient(145deg, rgba(255,255,255,.55), rgba(244,217,237,.55));
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 39px;
}

.cat-name {
    font-size: 13px;
    font-weight: 600;
    color: #4b3046;
}

.product-card {
    background: rgba(255, 255, 255, 0.42);
    backdrop-filter: blur(18px) saturate(160%);
    -webkit-backdrop-filter: blur(18px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.55);
    border-radius: 18px;
    padding: 10px;
    margin-bottom: 16px;
    box-shadow: 0 10px 28px rgba(63,0,50,.10);
    transition: transform .15s ease, box-shadow .15s ease;
}

.product-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 34px rgba(63,0,50,.16);
}

.product-name {
    font-weight: 600;
    font-size: 14px;
    line-height: 1.35;
    min-height: 39px;
    color: #321d2e;
}

.product-brand {
    color: #8c6980;
    font-size: 12px;
    margin: 3px 0;
}

.price {
    color: #8d005f;
    font-size: 18px;
    font-weight: 800;
}

.rating {
    color: #ef9d00;
    font-size: 13px;
}

.small-note {
    color: #816a79;
    font-size: 12px;
}

.empty-box {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    border: 1px dashed rgba(217, 184, 207, 0.8);
    border-radius: 20px;
    padding: 35px;
    text-align: center;
    color: #6e5668;
}

.stButton > button, .stLinkButton > a {
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-family: 'Outfit', sans-serif !important;
}

div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.45);
    backdrop-filter: blur(16px) saturate(160%);
    -webkit-backdrop-filter: blur(16px) saturate(160%);
    border: 1px solid rgba(255, 255, 255, 0.55);
    padding: 12px;
    border-radius: 16px;
    box-shadow: 0 8px 22px rgba(70,0,60,.08);
}

.top-nav-wrap {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Load dataset
# -----------------------------
@st.cache_data
def load_data(path):
    # The supplied "Fashion Dataset.xls" is actually CSV text.
    try:
        data = pd.read_csv(path)
    except Exception:
        data = pd.read_excel(path)

    data = data.copy()

    # Remove unwanted index column if present
    if "Unnamed: 0" in data.columns:
        data = data.drop(columns=["Unnamed: 0"])

    required = ["p_id", "name", "price", "brand", "img", "ratingCount", "avg_rating"]
    for col in required:
        if col not in data.columns:
            data[col] = ""

    for col in ["name", "brand", "img", "description", "p_attributes", "colour"]:
        if col in data.columns:
            data[col] = data[col].fillna("").astype(str)

    data["price"] = pd.to_numeric(data["price"], errors="coerce").fillna(0)
    data["avg_rating"] = pd.to_numeric(data["avg_rating"], errors="coerce").fillna(0)
    data["ratingCount"] = pd.to_numeric(data["ratingCount"], errors="coerce").fillna(0)

    return data

try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Dataset could not be loaded: {e}")
    st.stop()

# -----------------------------
# Category definitions
# -----------------------------
CATEGORY_RULES = {
    "Kurtis": [
        "kurta", "kurti", "kurta set", "kurta with"
    ],
    "Sarees": [
        "saree", "sari"
    ],
    "Footwear": [
        "shoe", "shoes", "sneaker", "sneakers", "sandal", "sandals",
        "heels", "flats", "loafers", "boots", "footwear"
    ],
    "Beauty Care": [
        "beauty", "makeup", "cosmetic", "lipstick", "foundation",
        "mascara", "skincare", "skin care", "perfume", "fragrance"
    ],
    "Menswear": [
        "men ", "men's", "mens ", "man ", "male "
    ],
    "T-Shirts": [
        "t-shirt", "tshirt", "tee "
    ],
    "Casuals": [
        "casual"
    ],
    "Accessories": [
        "bag", "wallet", "belt", "watch", "sunglasses", "jewellery",
        "jewelry", "earrings", "necklace", "bracelet", "accessory"
    ],
}

CATEGORY_UI = {
    "Kurtis": ("👗", "Kurtis"),
    "Sarees": ("🥻", "Sarees"),
    "Footwear": ("👟", "Shoes"),
    "Beauty Care": ("💄", "Beauty Care"),
    "Menswear": ("👔", "Menswear"),
    "T-Shirts": ("👕", "T-Shirts"),
    "Casuals": ("🧥", "Casuals"),
    "Accessories": ("👜", "Accessories"),
}

def category_mask(data, category):
    terms = CATEGORY_RULES[category]
    text = (
        data["name"].fillna("").astype(str) + " " +
        data.get("p_attributes", pd.Series("", index=data.index)).fillna("").astype(str)
    ).str.lower()

    pattern = "|".join(re.escape(x) for x in terms)
    return text.str.contains(pattern, regex=True, na=False)

def get_category_data(category):
    return df[category_mask(df, category)].copy()

def search_products(query):
    query = query.strip().lower()

    if not query:
        return df.head(24).copy()

    # First: exact category intent
    for category in CATEGORY_RULES:
        if query in category.lower() or any(
            query == term.lower().strip() for term in CATEGORY_RULES[category]
        ):
            return get_category_data(category)

    # Category aliases
    aliases = {
        "shoe": "Footwear",
        "shoes": "Footwear",
        "footwear": "Footwear",
        "sari": "Sarees",
        "saree": "Sarees",
        "sarees": "Sarees",
        "kurti": "Kurtis",
        "kurtis": "Kurtis",
        "kurta": "Kurtis",
        "kurtas": "Kurtis",
        "men": "Menswear",
        "menswear": "Menswear",
        "tshirt": "T-Shirts",
        "tshirts": "T-Shirts",
        "t-shirt": "T-Shirts",
        "beauty": "Beauty Care",
        "beautycare": "Beauty Care",
        "accessories": "Accessories",
        "casual": "Casuals",
        "casuals": "Casuals",
    }

    if query in aliases:
        return get_category_data(aliases[query])

    # General product search across useful fields
    searchable = (
        df["name"].fillna("").astype(str) + " " +
        df["brand"].fillna("").astype(str) + " " +
        df["colour"].fillna("").astype(str) + " " +
        df["description"].fillna("").astype(str) + " " +
        df["p_attributes"].fillna("").astype(str)
    ).str.lower()

    result = df[searchable.str.contains(re.escape(query), na=False)].copy()

    # Rank exact name matches first
    if not result.empty:
        result["_rank"] = result["name"].str.lower().str.contains(
            re.escape(query), na=False
        ).astype(int)
        result = result.sort_values(
            ["_rank", "avg_rating"], ascending=[False, False]
        ).drop(columns="_rank")

    return result

# -----------------------------
# Helpers
# -----------------------------
def product_key(row):
    return str(row["p_id"])

def myntra_search_url(name):
    return "https://www.myntra.com/search/" + quote(str(name).replace("/", " "))

def add_to_list(state_key, row):
    pid = product_key(row)
    if pid not in st.session_state[state_key]:
        st.session_state[state_key].append(pid)

def remove_from_list(state_key, pid):
    if pid in st.session_state[state_key]:
        st.session_state[state_key].remove(pid)

def get_products_by_ids(ids):
    if not ids:
        return df.iloc[0:0].copy()
    return df[df["p_id"].astype(str).isin([str(x) for x in ids])].copy()

def render_products(products, title="Products", max_items=24):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    if products.empty:
        st.markdown("""
        <div class="empty-box">
            <h3>No matching products found</h3>
            <p>This dataset does not currently contain products for this search/category.</p>
            <p>Try <b>kurti</b>, <b>kurtis</b>, <b>saree</b>, <b>tshirt</b>, or another term available in the dataset.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    products = products.head(max_items)

    # Build a key-safe, unique prefix per section so identical p_ids in
    # different (or the same) lists never collide on widget keys.
    section_key = re.sub(r"[^a-zA-Z0-9]+", "_", title).strip("_").lower()

    cols = st.columns(4)
    for i, (_, row) in enumerate(products.iterrows()):
        with cols[i % 4]:
            st.markdown('<div class="product-card">', unsafe_allow_html=True)

            img = str(row.get("img", "")).strip()
            if img:
                try:
                    st.image(img, use_container_width=True)
                except Exception:
                    st.markdown("🛍️")

            name = str(row["name"])
            brand = str(row["brand"])
            price = float(row["price"])
            rating = float(row["avg_rating"])
            rating_count = int(float(row["ratingCount"])) if str(row["ratingCount"]) not in ("", "nan") else 0

            st.markdown(
                f'<div class="product-name">{name[:75]}{"..." if len(name)>75 else ""}</div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div class="product-brand">{brand}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<span class="price">₹{price:,.0f}</span> '
                f'<span class="rating">★ {rating:.1f}</span>',
                unsafe_allow_html=True
            )
            st.caption(f"{rating_count:,} ratings")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("♡ Wishlist", key=f"wish_{section_key}_{i}_{product_key(row)}", use_container_width=True):
                    add_to_list("wishlist", row)
                    st.toast("Added to Wishlist ❤️")
            with c2:
                if st.button("🛍 Bag", key=f"bag_{section_key}_{i}_{product_key(row)}", use_container_width=True):
                    add_to_list("bag", row)
                    add_to_list("cart", row)
                    st.toast("Added to Bag 🛍️")

            st.link_button(
                "Buy Now",
                myntra_search_url(name),
                key=f"buy_{section_key}_{i}_{product_key(row)}",
                use_container_width=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Sidebar navigation
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 20px;">
        <div style="font-size:42px;">✨</div>
        <div style="font-size:23px;font-weight:800;">MYNTRA AI</div>
        <div style="font-size:11px;">Fashion Intelligence Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    nav_items = {
        "🏠 Home": "Home",
        "✨ AI Stylist": "AI Stylist",
        "🛍️ Bag": "Bag",
        "❤️ Wishlist": "Wishlist",
        "🛒 Cart": "Cart",
    }

    for label, page in nav_items.items():
        if st.button(label, key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

# ============================================================
# MAIN PAGE TOP-RIGHT NAVIGATION BAR
# ============================================================
top_spacer, top_nav_col = st.columns([5, 3])
with top_nav_col:
    t1, t2, t3 = st.columns(3)
    with t1:
        if st.button("🏠 Home", key="top_nav_home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
    with t2:
        if st.button("❤️ Wishlist", key="top_nav_wishlist", use_container_width=True):
            st.session_state.page = "Wishlist"
            st.rerun()
    with t3:
        if st.button("🛍️ Bag", key="top_nav_bag", use_container_width=True):
            st.session_state.page = "Bag"
            st.rerun()

# ============================================================
# HOME
# ============================================================
if st.session_state.page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>MYNTRA AI ASSISTANT ✨</h1>
        <p>Your Personal AI Fashion & Smart Shopping Assistant</p>
        <p>Search a product, discover the right style, save favourites and add products to your bag.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search
    c1, c2 = st.columns([5, 1])
    with c1:
        query = st.text_input(
            "Search",
            value=st.session_state.search_text,
            placeholder="Try: Kurti, Sarees, Shoes, T-Shirts, Menswear...",
            label_visibility="collapsed"
        )
    with c2:
        search_clicked = st.button("🔍 Search", use_container_width=True)

    if search_clicked:
        st.session_state.search_text = query
        st.session_state.search_results = search_products(query)
        st.rerun()

    # Categories
    st.markdown('<div class="section-title">Shop by Categories</div>', unsafe_allow_html=True)

    category_cols = st.columns(8)
    for i, (category, (icon, label)) in enumerate(CATEGORY_UI.items()):
        with category_cols[i]:
            count = len(get_category_data(category))
            st.markdown(
                f"""
                <div class="cat-card">
                    <div class="cat-icon">{icon}</div>
                    <div class="cat-name">{label}</div>
                    <div class="small-note">{count:,} products</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Explore", key=f"cat_{category}", use_container_width=True):
                st.session_state.search_text = label
                st.session_state.search_results = get_category_data(category)
                st.rerun()

    # Search result
    if st.session_state.search_results is not None:
        st.markdown("---")
        render_products(
            st.session_state.search_results,
            f"Search Results for “{st.session_state.search_text}”"
        )


    # Dashboard
    st.markdown('<div class="section-title">Customer Dashboard</div>', unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("Total Products", f"{len(df):,}"),
        ("Total Brands", f"{df['brand'].replace('', np.nan).nunique():,}"),
        ("Wishlist Items", str(len(st.session_state.wishlist))),
        ("Bag / Cart Items", str(len(st.session_state.cart))),
    ]

    for col, (label, value) in zip([m1,m2,m3,m4], metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown('<div class="section-title">Recommended for You</div>', unsafe_allow_html=True)

    # High-rated products
    recommended = df[df["avg_rating"] > 4].sort_values(
        ["avg_rating", "ratingCount"], ascending=False
    )
    render_products(recommended, "Top Rated Fashion Picks", max_items=8)

# ============================================================
# AI STYLIST
# ============================================================
elif st.session_state.page == "AI Stylist":

    st.markdown("""
    <div class="brand-box">
        <div class="brand-title">✨ AI Stylist</div>
        <div class="brand-sub">Tell me what you want to wear and I will find matching products from your dataset.</div>
    </div>
    """, unsafe_allow_html=True)

    occasion = st.selectbox(
        "What are you shopping for?",
        ["Daily Wear", "College / Casual", "Office", "Festive", "Party", "Wedding"]
    )

    style = st.text_input(
        "Describe your style",
        placeholder="Example: black kurti, floral saree, men's t-shirt..."
    )

    budget = st.slider("Maximum Budget (₹)", 500, 10000, 3000, 100)

    if st.button("✨ Generate My Style", use_container_width=True):
        result = search_products(style) if style.strip() else df.copy()
        result = result[result["price"] <= budget]

        if result.empty:
            st.warning("No exact matching products found within your budget. Try increasing the budget or changing the search.")
        else:
            # Simple recommendation score
            result = result.copy()
            result["style_score"] = (
                result["avg_rating"].fillna(0) * 20
                + np.log1p(result["ratingCount"].fillna(0))
            )
            result = result.sort_values("style_score", ascending=False)

            st.success(f"AI Stylist found {len(result):,} matching products for {occasion}.")
            render_products(result, "Your AI Style Picks", max_items=12)

# ============================================================
# BAG
# ============================================================
elif st.session_state.page == "Bag":

    st.markdown("""
    <div class="brand-box">
        <div class="brand-title">🛍️ My Bag</div>
        <div class="brand-sub">Products you selected for shopping.</div>
    </div>
    """, unsafe_allow_html=True)

    items = get_products_by_ids(st.session_state.bag)

    if items.empty:
        st.markdown('<div class="empty-box"><h3>Your Bag is Empty 🛍️</h3><p>Search for a product and click “Bag”.</p></div>', unsafe_allow_html=True)
    else:
        for _, row in items.iterrows():
            c1, c2, c3 = st.columns([1, 4, 1])
            with c1:
                if row["img"]:
                    st.image(row["img"], width=100)
            with c2:
                st.write(f"**{row['name']}**")
                st.write(f"{row['brand']} • ₹{row['price']:,.0f} • ⭐ {row['avg_rating']:.1f}")
            with c3:
                if st.button("Remove", key=f"remove_bag_{product_key(row)}"):
                    remove_from_list("bag", product_key(row))
                    remove_from_list("cart", product_key(row))
                    st.rerun()

        st.divider()
        total = items["price"].sum()
        st.subheader(f"Bag Total: ₹{total:,.0f}")
        if st.button("🛒 Move Bag to Cart", use_container_width=True):
            st.session_state.cart = list(dict.fromkeys(st.session_state.cart + st.session_state.bag))
            st.success("All bag items are now in Cart.")

# ============================================================
# WISHLIST
# ============================================================
elif st.session_state.page == "Wishlist":

    st.markdown("""
    <div class="brand-box">
        <div class="brand-title">❤️ Wishlist</div>
        <div class="brand-sub">Your favourite products are saved here.</div>
    </div>
    """, unsafe_allow_html=True)

    items = get_products_by_ids(st.session_state.wishlist)

    if items.empty:
        st.markdown('<div class="empty-box"><h3>No Wishlist Items ❤️</h3><p>Click “♡ Wishlist” on any product to save it.</p></div>', unsafe_allow_html=True)
    else:
        render_products(items, "Saved Products", max_items=24)

# ============================================================
# CART
# ============================================================
elif st.session_state.page == "Cart":

    st.markdown("""
    <div class="brand-box">
        <div class="brand-title">🛒 Cart</div>
        <div class="brand-sub">Review your selected products before shopping.</div>
    </div>
    """, unsafe_allow_html=True)

    items = get_products_by_ids(st.session_state.cart)

    if items.empty:
        st.markdown('<div class="empty-box"><h3>Your Cart is Empty 🛒</h3><p>Add products using the “🛍 Bag” button.</p></div>', unsafe_allow_html=True)
    else:
        for _, row in items.iterrows():
            c1, c2, c3 = st.columns([1, 5, 1])
            with c1:
                if row["img"]:
                    st.image(row["img"], width=90)
            with c2:
                st.write(f"**{row['name']}**")
                st.write(f"{row['brand']} • ₹{row['price']:,.0f} • ⭐ {row['avg_rating']:.1f}")
            with c3:
                if st.button("Remove", key=f"remove_cart_{product_key(row)}"):
                    remove_from_list("cart", product_key(row))
                    st.rerun()

        total = items["price"].sum()
        st.divider()

        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader("Order Summary")
            st.write(f"Items: {len(items)}")
            st.write(f"Total: ₹{total:,.0f}")
        with c2:
            if st.button("💳 Checkout", use_container_width=True):
                st.success("Checkout ready! Use the Buy Now links to continue to Myntra.")
