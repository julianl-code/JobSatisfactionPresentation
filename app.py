import streamlit as st
import pandas as pd
import altair as alt

# ============================================================================
# INITIALIZATION: Set up Session State for tracking responses
# ============================================================================

# Ensure 'responses' exists in session_state
if 'responses' not in st.session_state:
    st.session_state.responses = []

# ============================================================================
# PAGE CONFIGURATION & CUSTOM STYLING
# ============================================================================

st.set_page_config(
    page_title="Job Satisfaction in the Digital Age",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better mobile responsiveness and styling
st.markdown("""
<style>
    /* Root variables for responsive sizing */
    :root {
        --desktop-max-width: 1200px;
        --padding-desktop: 3rem 2rem;
        --padding-mobile: 1rem 1rem;
    }
    
    /* Main container - responsive */
    .main {
        padding: var(--padding-desktop);
        max-width: var(--desktop-max-width);
        margin: 0 auto;
    }
    
    /* Title styling - responsive font */
    h1 {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
        font-size: 3rem;
    }
    
    h2 {
        color: #2c3e50;
        font-size: 1.8rem;
        margin-top: 1.5rem;
    }
    
    /* Subtitle styling */
    h3 {
        color: #2c3e50;
        margin-top: 1.5rem;
        font-size: 1.3rem;
    }
    
    h4 {
        color: #333;
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
    
    /* Slider container styling */
    .stSlider {
        padding: 0.5rem 0;
    }
    
    /* Card-like containers for scenarios */
    .phase-card {
        background: linear-gradient(135deg, #FFE5E5 0%, #FFB3B3 100%);
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 5px solid #FF6B6B;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #FF9999;
    }
    
    .phase-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.2);
    }
    
    .phase-card.phase2 {
        background: linear-gradient(135deg, #D4F5F2 0%, #A8E6E1 100%);
        border-left-color: #4ECDC4;
        border-color: #7DD3CA;
    }
    
    .phase-card.phase3 {
        background: linear-gradient(135deg, #FFF8DC 0%, #FFE680 100%);
        border-left-color: #FFD93D;
        border-color: #FFE066;
    }
    
    .phase-card p {
        margin: 0.5rem 0;
        line-height: 1.6;
        font-size: 1rem;
        color: #333;
    }
    
    .phase-card h4 {
        color: #333;
    }
    
    /* Button styling */
    .stButton > button {
        font-size: 1.1rem;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
    }
    
    /* Success message styling */
    .stSuccess {
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #00cc96;
    }
    
    /* Metrics styling */
    .metric-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Desktop-specific styles (> 1024px) */
    @media (min-width: 1024px) {
        .main {
            padding: var(--padding-desktop);
        }
        
        h1 {
            font-size: 3rem;
        }
        
        h2 {
            font-size: 2rem;
        }
        
        .phase-card {
            padding: 2rem;
            margin: 1.5rem 0;
        }
        
        .metrics-row {
            display: flex;
            gap: 1.5rem;
            justify-content: space-around;
        }
        
        .metric-item {
            flex: 1;
        }
    }
    
    /* Tablet styles (768px - 1024px) */
    @media (min-width: 768px) and (max-width: 1023px) {
        .main {
            padding: 2rem 1.5rem;
        }
        
        h1 {
            font-size: 2.2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        .phase-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
    }
    
    /* Mobile styles (< 768px) */
    @media (max-width: 767px) {
        .main {
            padding: var(--padding-mobile);
            max-width: 100%;
        }
        
        h1 {
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        h2 {
            font-size: 1.3rem;
        }
        
        h3 {
            font-size: 1.1rem;
        }
        
        h4 {
            font-size: 1rem;
        }
        
        .phase-card {
            padding: 1rem;
            margin: 0.8rem 0;
            border-left-width: 4px;
        }
        
        .phase-card p {
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        .stButton > button {
            font-size: 1rem;
            padding: 0.7rem;
        }
        
        .metric-box {
            padding: 1rem;
            min-height: 100px;
        }
        
        .metric-item h3 {
            font-size: 0.9rem;
        }
    }
    
    /* Text introduction styling */
    .intro-text {
        text-align: center;
        font-size: 1.1rem;
        color: #555;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Responsive info box */
    .info-box {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    /* Insight box styling */
    .insight-box {
        background-color: #f0f7ff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    /* Presenter view styling */
    .presenter-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8C8C 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .presenter-header h1 {
        color: white;
        margin: 0;
    }
    
    .view-selector {
        background-color: #f9f9f9;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        border-left: 4px solid #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# VIEW SELECTOR (Respondent vs Presenter)
# ============================================================================

st.sidebar.markdown("## 📺 View Mode")
view_mode = st.sidebar.radio(
    "Select your view:",
    ["👥 Respondent View", "🎤 Presenter View"],
    help="Choose whether you are filling in the survey (Respondent) or presenting results (Presenter)"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"### 📊 Current Responses: **{len(st.session_state.responses)}**")

# ============================================================================
# RESPONDENT VIEW
# ============================================================================

if view_mode == "👥 Respondent View":
    
    # ============================================================================
    # TITLE AND INTRODUCTION TEXT
    # ============================================================================

    # Header section
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# Job Satisfaction in the Digital Age")

    st.markdown("""
    <div class="intro-text">
        <p><strong>Discover how AI adoption affects your job satisfaction</strong></p>
        <p>Rate your satisfaction (1 = low, 10 = high) for each AI adoption scenario in your work</p>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================================
    # INTERACTIVE SLIDERS WITH DETAILED SCENARIOS
    # ============================================================================

    st.markdown("---")
    st.markdown("## 📋 Rate Your Job Satisfaction Per Scenario")
    st.markdown("")

    # Scenario 1: Little AI
    st.markdown("""
    <div class="phase-card">
        <h4>🔧 Scenario 1: </h4>
        <p>You manually type data from Excel to PowerPoint three days a week and search online for contact details. 
        It feels like you're working far below your skill level, but it's necessary for weekly reports. 
        You spend significant time on repetitive tasks that don't add strategic value.</p>
    </div>
    """, unsafe_allow_html=True)

    werkgeluk_fase1 = st.slider(
        "How satisfied are you in Scenario 1?",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="fase1_slider",
        label_visibility="collapsed"
    )

    # Responsive metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔧 Scenario 1", werkgeluk_fase1, delta=None)

    st.markdown("")

    # Scenario 2: Medium AI
    st.markdown("""
    <div class="phase-card phase2">
        <h4>⚡ Scenario 2: </h4>
        <p>You install an AI tool that takes over all data entry and builds reports within seconds. 
        You now spend your time truly analyzing trends, presenting to management, and developing 
        new strategic ideas. AI amplifies your capabilities and creates meaningful work.</p>
    </div>
    """, unsafe_allow_html=True)

    werkgeluk_fase2 = st.slider(
        "How satisfied are you in Scenario 2?",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="fase2_slider",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns(3)
    with col2:
        st.metric("⚡ Scenario 2", werkgeluk_fase2, delta=None)

    st.markdown("")

    # Scenario 3: Lots of AI
    st.markdown("""
    <div class="phase-card phase3">
        <h4>🤖 Scenario 3: </h4>
        <p>The AI not only analyzes data but also develops strategy, writes reports, and executes them 
        automatically. You only receive alerts when budget errors occur. You feel like a "software babysitter" 
        and worry that your professional skills are gradually disappearing. Decision-making authority slips away.</p>
    </div>
    """, unsafe_allow_html=True)

    werkgeluk_fase3 = st.slider(
        "How satisfied are you in Scenario 3?",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
        key="fase3_slider",
        label_visibility="collapsed"
    )

    col1, col2, col3 = st.columns(3)
    with col3:
        st.metric("🤖 Scenario 3", werkgeluk_fase3, delta=None)

    st.markdown("")

    # ============================================================================
    # SUBMIT BUTTON
    # ============================================================================

    st.markdown("---")

    col_submit_1, col_submit_2, col_submit_3 = st.columns([1, 2, 1])
    with col_submit_2:
        if st.button("📤 Submit Your Response", use_container_width=True, type="primary"):
            # Add current scores to responses
            st.session_state.responses.append({
                "fase1": werkgeluk_fase1,
                "fase2": werkgeluk_fase2,
                "fase3": werkgeluk_fase3
            })
            
            st.success("✅ Your answers have been saved! Thank you for participating.")

    st.markdown("")
    
    # Footer for respondent view
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9rem; padding: 2rem 0;">
        <p>💡 <strong>Interactive Research App</strong> | Please wait for the presenter to show results</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PRESENTER VIEW
# ============================================================================

else:  # Presenter View
    
    st.markdown("## 🎤 Presenter Dashboard")
    st.markdown("### Live Results & Analysis")
    
    st.markdown("")
    
    # Number of submitted responses
    aantal_reacties = len(st.session_state.responses)

    # Display response count with nice styling
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown(f"""
        <div class="metric-box">
            <h3 style="color: #FF6B6B; margin: 0;">👥 {aantal_reacties}</h3>
            <p style="color: #666; margin: 0.5rem 0 0 0;">Response{'s' if aantal_reacties != 1 else ''} Submitted</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    # Check if there are responses
    if aantal_reacties > 0:
        # Calculate averages
        gemiddelde_fase1 = sum([r["fase1"] for r in st.session_state.responses]) / aantal_reacties
        gemiddelde_fase2 = sum([r["fase2"] for r in st.session_state.responses]) / aantal_reacties
        gemiddelde_fase3 = sum([r["fase3"] for r in st.session_state.responses]) / aantal_reacties
        
        # Create a DataFrame for visualization
        data = pd.DataFrame({
            "Scenario": ["Scenario 1:\nThe Craftsman", "Scenario 2:\nThe Strategist", "Scenario 3:\nThe Observer"],
            "Average Job Satisfaction": [gemiddelde_fase1, gemiddelde_fase2, gemiddelde_fase3]
        })
        
        # Create a beautiful line chart with Altair - optimized for mobile
        chart = alt.Chart(data).mark_line(point=True, color="#FF6B6B", size=3).encode(
            x=alt.X("Scenario:N", title="AI Adoption Scenarios", axis=alt.Axis(labelAngle=0, labelFontSize=12)),        y=alt.Y(
            "Average Job Satisfaction:Q",
            title="Average Job Satisfaction (1-10)",
            scale=alt.Scale(domain=[1, 10]),
            axis=alt.Axis(labelFontSize=12)
        ),
            tooltip=["Scenario:N", alt.Tooltip("Average Job Satisfaction:Q", format=".2f", title="Satisfaction")]
        ).properties(
            width="container",
            height=400,
            title="Job Satisfaction per AI Adoption Scenario (Group Average)"
        ).interactive()
        
        # Display the chart with responsive container
        st.altair_chart(chart, use_container_width=True)
        
        st.markdown("")
        
        # Show exact values in a nice format
        st.markdown("### 📈 Average Satisfaction Scores:")
        
        # Display as three columns with metrics
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric(
                "🔧 Scenario 1",
                f"{gemiddelde_fase1:.2f}",
                delta=None,
                help="Manual work phase"
            )
        
        with metric_col2:
            st.metric(
                "⚡ Scenario 2",
                f"{gemiddelde_fase2:.2f}",
                delta=None,
                help="Strategic work phase"
            )
        
        with metric_col3:
            st.metric(
                "🤖 Scenario 3",
                f"{gemiddelde_fase3:.2f}",
                delta=None,
                help="Automated phase"
            )
        
        st.markdown("")
        
        # Additional insights
        max_phase = max(
            ("Scenario 1 (The Craftsman)", gemiddelde_fase1),
            ("Scenario 2 (The Strategist)", gemiddelde_fase2),
            ("Scenario 3 (The Observer)", gemiddelde_fase3),
            key=lambda x: x[1]
        )
        
        st.markdown(f"""
        <div class="insight-box">
            <p><strong>💡 Key Insight:</strong> The highest average satisfaction is in <strong>{max_phase[0]}</strong> with a score of <strong>{max_phase[1]:.2f}/5</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.markdown("""
        <div class="info-box">
            <h3>📭 No responses yet</h3>
            <p>Participants are still filling in their responses. The results will appear here as soon as they start submitting!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Presenter Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.9rem; padding: 2rem 0;">
        <p>💡 <strong>Presenter Dashboard</strong> | Share your screen with the audience to show these results</p>
    </div>
    """, unsafe_allow_html=True)
