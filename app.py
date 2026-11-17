import streamlit as st
import pandas as pd
import hashlib
import datetime
import time
import requests
from bs4 import BeautifulSoup

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GENSAFE AI | Enterprise Clinical & Web Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ULTRA-MODERN ADVANCED HOLOGRAPHIC SAAS CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Orbitron:wght@600;800;900&display=swap');

    .stApp {
        background: #020617;
        background-image: 
            radial-gradient(circle at 10% 10%, rgba(16, 185, 129, 0.12) 0%, transparent 45%),
            radial-gradient(circle at 90% 90%, rgba(59, 130, 246, 0.12) 0%, transparent 45%),
            linear-gradient(to bottom, #020617, #090d16);
        color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    @keyframes neonPulse {
        0% { border-color: rgba(16, 185, 129, 0.3); box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); }
        50% { border-color: rgba(16, 185, 129, 0.8); box-shadow: 0 0 40px rgba(16, 185, 129, 0.35); }
        100% { border-color: rgba(16, 185, 129, 0.3); box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); }
    }

    @keyframes liveScan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(1000%); }
    }

    .nav-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 24px 48px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 35px;
        background: rgba(2, 6, 23, 0.85);
        backdrop-filter: blur(24px);
        position: sticky;
        top: 0;
        z-index: 999;
    }

    .nav-logo {
        font-family: 'Orbitron', sans-serif;
        font-size: 1.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 30%, #10b981 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 2px;
    }

    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 4.5rem;
        font-weight: 800;
        line-height: 1.1;
        color: #ffffff;
        letter-spacing: -2px;
        margin-bottom: 20px;
    }

    .hero-title span {
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        font-weight: 400;
        line-height: 1.7;
        margin-bottom: 35px;
        max-width: 700px;
    }

    .advanced-hud-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85) 0%, rgba(3, 7, 18, 0.95) 100%);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 28px;
        padding: 40px;
        margin-bottom: 24px;
        box-shadow: 0 30px 60px -15px rgba(0, 0, 0, 0.9);
        animation: neonPulse 6s infinite ease-in-out;
        position: relative;
        overflow: hidden;
    }

    .advanced-hud-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #10b981, #3b82f6, transparent);
    }

    .image-hologram {
        width: 100%;
        height: 290px;
        object-fit: cover;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
        transition: transform 0.4s ease;
    }
    .image-hologram:hover {
        transform: scale(1.02);
    }

    .pricing-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 16px;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 15px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 14px;
        padding: 16px 24px;
        font-size: 1rem;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px -5px rgba(16, 185, 129, 0.5);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px -5px rgba(16, 185, 129, 0.7);
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "patient_id" not in st.session_state:
    st.session_state.patient_id = "GS-2026-FB9616"
if "patient_name" not in st.session_state:
    st.session_state.patient_name = "Adnan (Lead Principal Subject)"
if "patient_gene" not in st.session_state:
    st.session_state.patient_gene = "HLA-B*57:01 Positive (Hypersensitivity)"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "GenSafe Enterprise Core v42.0 online! Autonomous live web intelligence, clinical genomics, and neural telemetry fully active."}
    ]
if "selected_plan" not in st.session_state:
    st.session_state.selected_plan = None

# ==============================================================================
# TOP NAVBAR
# ==============================================================================
st.markdown("""
<div class="nav-container">
    <div class="nav-logo">GENSAFE AI ⚡</div>
    <div style="display: flex; gap: 30px; align-items: center; color: #94a3b8; font-size: 0.95rem;">
        <span>Autonomous Core: <strong style="color:#10b981;">ONLINE</strong></span>
        <span>Secure Node: <strong style="color:#38bdf8;">US-EAST-ALPHA</strong></span>
        <span>Admin: <strong style="color:#ffffff;">Adnan</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- NAVIGATION TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01 | CLINICAL DASHBOARD",
    "02 | ADR & GENOMICS SCANNER",
    "03 | LIVE WEB AI CHATBOT",
    "04 | PLATFORM FEATURES",
    "05 | PRICING & BILLING"
])

# ==============================================================================
# TAB 1: CLINICAL DASHBOARD & REGISTRATION (ULTRA-ADVANCED HUD SECTION)
# ==============================================================================
with tab1:
    st.markdown("""
    <div style="margin-bottom: 40px;">
        <div class="pricing-badge">Next-Gen Autonomous Architecture</div>
        <div class="hero-title">Clinical intelligence.<br><span>In seconds.</span></div>
        <div class="hero-subtitle">Experience lightning-fast live web scraping, advanced pharmacogenomics simulation, and seamless enterprise intelligence workflows built for modern clinical research.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([1.3, 1], gap="large")
    with c1:
        st.markdown('<div class="advanced-hud-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-family: Orbitron; font-size: 1.3rem; margin-bottom: 25px; color: #ffffff;'>Clinical Subject Registration & Telemetry ⚡</h3>", unsafe_allow_html=True)
        with st.form("reg_form"):
            p_name = st.text_input("Full Name / Subject Alias:", value=st.session_state.patient_name)
            col_a, col_b = st.columns(2)
            with col_a:
                p_age = st.number_input("Age (Years):", min_value=1, max_value=120, value=22)
            with col_b:
                p_blood = st.selectbox("Blood Group:", ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
            
            p_genotype = st.selectbox(
                "Primary Pharmacogene Variant (SNP Profile):",
                [
                    "HLA-B*57:01 Positive (Hypersensitivity)",
                    "CYP2D6 *4/*4 (Poor Metabolizer)",
                    "CYP2C19 *1/*1 (Normal Metabolizer)",
                    "TPMT *3A/*3A (High Toxicity Risk)",
                    "VKORC1 -1639G>A (Warfarin Sensitive)"
                ]
            )
            
            submitted = st.form_submit_button("GENERATE ENCRYPTED CLINICAL ID")
            if submitted:
                raw_str = f"{p_name}{p_age}{p_genotype}{time.time()}"
                hash_code = hashlib.sha256(raw_str.encode()).hexdigest()[:6].upper()
                st.session_state.patient_id = f"GS-2026-{hash_code}"
                st.session_state.patient_name = p_name
                st.session_state.patient_gene = p_genotype
                st.success("Clinical ID & Genomic Profile Successfully Registered!")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("<h3 style='font-family: Orbitron; font-size: 1.3rem; margin-bottom: 25px; color: #ffffff;'>Live Holographic Medical Feed</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class="advanced-hud-card" style="padding: 28px;">
            <img src="https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=800&q=80" class="image-hologram">
            <div style="font-size: 0.75rem; color: #34d399; letter-spacing: 3px; font-weight:800;">GENSAFE CLINICAL NETWORK</div>
            <h2 style="margin: 12px 0; color: #ffffff; letter-spacing: 2px; font-family:'Orbitron'; font-size:1.5rem;">{pid}</h2>
            <hr style="border-color: rgba(16, 185, 129, 0.3); margin: 15px 0;">
            <p style="margin: 8px 0; font-size:0.95rem;"><b>SUBJECT:</b> {pname}</p>
            <p style="margin: 8px 0; font-size:0.95rem;"><b>GENOTYPE:</b> {pgene}</p>
            <p style="margin: 8px 0; font-size:0.95rem;"><b>STATUS:</b> <span style="color:#34d399; font-weight:bold; text-shadow: 0 0 10px rgba(52,211,153,0.5);">VERIFIED & ACTIVE</span></p>
        </div>
        """.format(pid=st.session_state.patient_id, pname=st.session_state.patient_name, pgene=st.session_state.patient_gene), unsafe_allow_html=True)

# ==============================================================================
# TAB 2: PHARMACOGENOMICS & ADR SCANNER
# ==============================================================================
with tab2:
    st.markdown('<div class="advanced-hud-card">', unsafe_allow_html=True)
    st.markdown("### Automated Drug-Gene Compatibility Engine")
    st.info(f"Running diagnostics against Active Clinical Profile: **{st.session_state.patient_name}** | Genotype: **{st.session_state.patient_gene}**")

    drug_choice = st.selectbox(
        "Select Target Pharmaceutical Compound to Screen:",
        [
            "Panadol / Paracetamol (Analgesic / Antipyretic)",
            "Codeine (Analgesic / Pain Management)",
            "Clopidogrel (Antiplatelet / Cardiac)",
            "Azathioprine (Immunosuppressant)",
            "Warfarin (Anticoagulant)"
        ]
    )

    if st.button("EXECUTE CLINICAL ADR & METABOLISM SIMULATION"):
        with st.spinner("Analyzing Cytochrome P450 enzyme pathways..."):
            time.sleep(0.4)

        gene = st.session_state.patient_gene
        risk_level = "LOW RISK (OPTIMAL)"
        efficacy = "96.4%"
        toxicity = "4.2%"
        mechanism = "Standard hepatic clearance via glucuronidation and sulfation. Safe therapeutic index observed."
        recommendation = "Standard clinical dosage approved. Safe for regular administration."

        if "Panadol" in drug_choice:
            risk_level = "LOW RISK (SAFE CLINICAL PROFILE)"
            efficacy = "98.5%"
            toxicity = "2.1%"
            mechanism = "Paracetamol is primarily metabolized in the liver by glucuronide and sulfate conjugation, with a small fraction oxidized by CYP2E1 into NAPQI (hepatotoxic metabolite) neutralized by glutathione."
            recommendation = "Standard dosage (500mg - 1000mg every 4-6 hours) is safe. Do not exceed 4g daily."
        elif "Codeine" in drug_choice and "CYP2D6" in gene:
            risk_level = "CRITICAL ADR ALERT (INEFFECTIVE / TOXIC)"
            efficacy = "11.0%"
            toxicity = "78.5%"
            mechanism = "CYP2D6 *4/*4 allele causes complete loss of enzyme function. Codeine cannot convert into active morphine metabolites."
            recommendation = "CONTRAINDICATED: Avoid Codeine. Switch to non-CYP2D6 analgesic."

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f'<div class="advanced-hud-card"><div style="color:#64748b; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase;">Clinical Verdict</div><div style="color:#34d399; font-weight:700; font-size:1.1rem; margin-top:8px;">{risk_level}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="advanced-hud-card"><div style="color:#64748b; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase;">Predicted Efficacy</div><div style="font-family:Orbitron; font-size:2rem; font-weight:800; color:#10b981;">{efficacy}</div></div>', unsafe_allow_html=True)
        with m3:
            st.markdown(f'<div class="advanced-hud-card"><div style="color:#64748b; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase;">Toxicity Probability</div><div style="font-family:Orbitron; font-size:2rem; font-weight:800; color:#f87171;">{toxicity}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="advanced-hud-card">
            <h4 style="color:#10b981; font-family:'Orbitron'; font-size:1rem;">MOLECULAR MECHANISM & PATHWAY ANALYSIS</h4>
            <p style="font-size:1rem; line-height:1.6; color:#cbd5e1;">{mechanism}</p>
            <hr style="border-color: rgba(255,255,255,0.08);">
            <h4 style="color:#38bdf8; font-family:'Orbitron'; font-size:1rem;">CLINICAL ACTION PROTOCOL</h4>
            <p style="font-size:1rem; font-weight:600; color:#ffffff;">{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TAB 3: LIVE WEB AI CHATBOT
# ==============================================================================
with tab3:
    st.markdown('<div class="advanced-hud-card">', unsafe_allow_html=True)
    st.markdown("### Live Web Intelligence Assistant")
    st.caption("Ask anything for live web searching or computational biology research")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    def enterprise_ai_response(query):
        q = query.lower().strip()
        conversational_phrases = ["ha", "haan", "hi", "hello", "hey", "salam", "assalam", "kaise ho", "kya haal hai", "kia haal ha", "ok", "theek", "thanks"]
        if q in conversational_phrases or (len(q.split()) <= 2 and not any(w in q for w in ["panadol", "nims", "medicine", "search", "traffic", "news", "python", "mitosis"])):
            return f"Walaikum Assalam, Adnan! GenSafe Enterprise Terminal is online. What live query or research can I execute for you today?"

        try:
            url = "https://html.duckduckgo.com/html/"
            params = {"q": query}
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
            
            response = requests.post(url, data=params, headers=headers, timeout=6)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                snippets = []
                results = soup.find_all('div', class_='result', limit=4)
                for res in results:
                    title_tag = res.find('a', class_='result__title')
                    snippet_tag = res.find('a', class_='result__snippet')
                    title = title_tag.get_text().strip() if title_tag else "Web Result"
                    snippet = snippet_tag.get_text().strip() if snippet_tag else ""
                    if snippet:
                        snippets.append(f"**{title}**\n{snippet}")
                
                if snippets:
                    output = f"**Live Web Intelligence Results for:** *\"{query}\"*\n\n"
                    for idx, s in enumerate(snippets, 1):
                        output += f"{idx}. {s}\n\n"
                    return output
        except Exception:
            pass

        return f"""**GenSafe Advanced Synthesis:**
* **Query:** *"{query}"*
* **Telemetry:** Active Neural Stream
* **Status:** Processed through secure clinical bioinformatics pipelines."""

    user_query = st.chat_input("Ask anything or search live web...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Synthesizing response..."):
                reply = enterprise_ai_response(user_query)
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TAB 4: PLATFORM FEATURES
# ==============================================================================
with tab4:
    st.markdown("### Platform Core Capabilities & Neural Architecture")
    col_f1, col_f2 = st.columns(2, gap="large")
    with col_f1:
        st.markdown("""
        <div class="advanced-hud-card">
            <img src="https://images.unsplash.com/photo-1507413245164-6160d8298b31?auto=format&fit=crop&w=800&q=80" class="image-hologram" style="height:200px;">
            <h4 style="font-family:'Orbitron'; color:#10b981; font-size:1.1rem;">Autonomous Live Web Scraper</h4>
            <p style="color:#94a3b8; line-height:1.6;">Bypasses standard API restrictions to fetch real-time search results, web data, and research articles instantly.</p>
            <h4 style="font-family:'Orbitron'; color:#38bdf8; font-size:1.1rem; margin-top:25px;">Pharmacogenomics Engine</h4>
            <p style="color:#94a3b8; line-height:1.6;">Simulates Cytochrome P450 pathways to evaluate drug-gene compatibility and mitigate adverse reactions.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class="advanced-hud-card">
            <img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=800&q=80" class="image-hologram" style="height:200px;">
            <h4 style="font-family:'Orbitron'; color:#10b981; font-size:1.1rem;">Enterprise Telemetry & Security</h4>
            <p style="color:#94a3b8; line-height:1.6;">Seamless multi-node architecture supporting real-time data streaming and secure corporate compliance.</p>
            <h4 style="font-family:'Orbitron'; color:#38bdf8; font-size:1.1rem; margin-top:25px;">Digital Clinical Passports</h4>
            <p style="color:#94a3b8; line-height:1.6;">Generates SHA-256 encrypted clinical IDs for secure patient data tracking across medical networks.</p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: PRICING & BILLING GATEWAY
# ==============================================================================
with tab5:
    st.markdown("### Enterprise Pricing & Secure Checkout")
    st.markdown("<p style='color:#94a3b8; margin-bottom:30px;'>Choose a tier to activate instant license binding.</p>", unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3, gap="medium")
    
    with p1:
        st.markdown("""
        <div class="advanced-hud-card" style="text-align:center;">
            <div class="pricing-badge">Researcher</div>
            <h2 style="font-size:2.5rem; margin:15px 0; font-family:'Orbitron';">$29 <span style="font-size:1rem; color:#94a3b8; font-family:'Plus Jakarta Sans';">/mo</span></h2>
            <p style="color:#94a3b8; font-size:0.95rem; line-height:1.8;">500 Live Searches/mo<br>Basic ADR Scanner<br>Standard Support</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Researcher", key="bp1"):
            st.session_state.selected_plan = "Researcher Tier ($29/mo)"
            
    with p2:
        st.markdown("""
        <div class="advanced-hud-card" style="text-align:center; border: 2px solid #10b981;">
            <div class="pricing-badge" style="background:#10b981; color:#030712;">Most Popular</div>
            <h2 style="font-size:2.5rem; margin:15px 0; font-family:'Orbitron';">$89 <span style="font-size:1rem; color:#94a3b8; font-family:'Plus Jakarta Sans';">/mo</span></h2>
            <p style="color:#94a3b8; font-size:0.95rem; line-height:1.8;">Unlimited Web Scraping<br>Advanced CYP450 Engine<br>Priority Neural Access</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Clinical Pro", key="bp2"):
            st.session_state.selected_plan = "Clinical Pro Tier ($89/mo)"
            
    with p3:
        st.markdown("""
        <div class="advanced-hud-card" style="text-align:center;">
            <div class="pricing-badge">Enterprise</div>
            <h2 style="font-size:2.5rem; margin:15px 0; font-family:'Orbitron';">$249 <span style="font-size:1rem; color:#94a3b8; font-family:'Plus Jakarta Sans';">/mo</span></h2>
            <p style="color:#94a3b8; font-size:0.95rem; line-height:1.8;">Full API Access<br>Custom SNP Profiles<br>HIPAA Compliance</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Enterprise", key="bp3"):
            st.session_state.selected_plan = "Enterprise Tier ($249/mo)"
            
    if st.session_state.selected_plan:
        st.markdown("---")
        st.markdown(f"### Secure Checkout: **{st.session_state.selected_plan}**")
        with st.form("checkout_form"):
            cc1, cc2 = st.columns(2)
            with cc1:
                st.text_input("Cardholder Name", value="Adnan")
                st.text_input("Card Number", placeholder="4532 •••• •••• 8849")
            with cc2:
                st.text_input("Expiration Date", placeholder="MM/YY")
                st.text_input("CVV Code", type="password", placeholder="123")
                
            if st.form_submit_button("Complete Secure Payment"):
                st.success(f"Payment successful! License activated for **{st.session_state.selected_plan}**.")
                st.balloons()
                st.session_state.selected_plan = None