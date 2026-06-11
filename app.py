import streamlit as st
import os
import tempfile
from pathlib import Path
from datetime import datetime

from utils.text_extractor import extract_text_from_file
from utils.analyzer import ArticleAnalyzer
from utils.report_generator import ReportGenerator

# Page configuration must be the first Streamlit command
st.set_page_config(
    page_title="Article Critique Platform | Research Quality Assessment",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    css_file = Path("static/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Fixed header and footer (matching Radar app style with red accent)
st.markdown("""
<div class="fixed-header">
    <h1>📋 JOURNAL <span style="color: #dc3545; font-weight: bold;">CRITIQUE</span> PLATFORM</h1>
    <h2><span style="color: #dc3545; font-weight: bold;">S</span>ystematic <span style="color: #dc3545; font-weight: bold;">A</span>rticle <span style="color: #dc3545; font-weight: bold;">C</span>ritique for <span style="color: #dc3545; font-weight: bold;">A</span>cademic <span style="color: #dc3545; font-weight: bold;">R</span>esearch</h2>
</div>
<div class="fixed-footer">
    <span style="color: white;">Scholarly Academic Resource by </span>
    <a href="https://wawerujm.github.io" target="_blank" style="color: #dc3545; text-decoration: underline; font-weight: bold;">
        James Waweru
    </a>
    <span style="color: white;"> | Evidence-Based Research Platform</span>
</div>
""", unsafe_allow_html=True)

# Content wrapper - content starts immediately below header
st.markdown("<div class='content'>", unsafe_allow_html=True)

# Initialize session state
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "report_html" not in st.session_state:
    st.session_state.report_html = None

# Main title section - reduced top margin
st.markdown("""
<div style="text-align: center; padding: 10px 0 20px 0;">
    <h2 style="color: #2c3e50; margin-bottom: 10px;">📊 13-Point Systematic Article Critique</h2>
    <p style="color: #7f8c8d; font-size: 16px;">Follows CASP, STROBE, CONSORT, PRISMA, and SMART reporting guidelines</p>
</div>
""", unsafe_allow_html=True)

# Two column layout for upload and settings
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; border: 1px solid #e0e0e0;">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">📄 Upload Journal Article</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file (PDF or DOCX)",
        type=['pdf', 'docx'],
        help="Upload a research article for systematic critique",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        st.success(f"✅ File loaded: {uploaded_file.name}")

with col_right:
    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; border: 1px solid #e0e0e0;">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">⚙️ Analysis Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    depth = st.select_slider(
        "Analysis Depth",
        options=["Quick Scan", "Standard Review", "In-depth Critique", "Comprehensive Audit"],
        value="Standard Review",
        help="Deeper analysis checks more criteria points"
    )
    
    guideline_ref = st.multiselect(
        "Apply Reporting Guidelines",
        ["CONSORT (RCT)", "STROBE (Observational)", "PRISMA (Systematic Review)", "CASP (Qualitative)"],
        default=["CONSORT (RCT)", "STROBE (Observational)"],
        help="Select guidelines applicable to your article type"
    )

# Analysis button and progress
if uploaded_file is not None:
    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        analyze_button = st.button(
            "🔬 START SYSTEMATIC ANALYSIS", 
            use_container_width=True,
            type="primary"
        )
    
    if analyze_button:
        with st.spinner("🔍 Analyzing article with scientific rigor..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Extract text
                article_text = extract_text_from_file(tmp_path)
                
                if article_text and len(article_text.strip()) > 500:
                    # Analyze
                    analyzer = ArticleAnalyzer(article_text, depth, guideline_ref)
                    analysis_results = analyzer.analyze_all_criteria()
                    
                    # Generate report
                    report_gen = ReportGenerator(analysis_results, uploaded_file.name)
                    
                    # Store in session state
                    st.session_state.analysis_complete = True
                    st.session_state.analysis_results = analysis_results
                    st.session_state.uploaded_filename = uploaded_file.name
                    st.session_state.report_html = report_gen.generate_streamlit_html()
                    
                    st.success("✅ Analysis complete!")
                    st.rerun()
                    
                else:
                    st.error("❌ Could not extract sufficient text. Ensure file contains readable text (not scanned images).")
                    
            except Exception as e:
                st.error(f"⚠️ Analysis error: {str(e)}")
            finally:
                try:
                    os.unlink(tmp_path)
                except:
                    pass

# Display results if analysis is complete
if st.session_state.analysis_complete and st.session_state.report_html:
    st.markdown("<hr style='margin: 30px 0 20px 0;'>", unsafe_allow_html=True)
    
    # Results header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h2 style="color: #2c3e50;">📊 CRITIQUE RESULTS</h2>
        <p style="color: #7f8c8d;">Comprehensive assessment based on 13 scientific quality criteria</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the rendered HTML report
    from streamlit.components.v1 import html
    html(st.session_state.report_html, height=900, scrolling=True)
    
    # Download section
    st.markdown("""
    <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; margin-top: 20px;">
        <h3 style="color: #2c3e50; margin-bottom: 15px;">📥 Export Report</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    
    with col_dl1:
        report_gen = ReportGenerator(st.session_state.analysis_results, st.session_state.uploaded_filename)
        full_html = report_gen.generate_full_report()
        st.download_button(
            label="📄 Download HTML",
            data=full_html.encode('utf-8'),
            file_name=f"critique_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_dl2:
        md_report = report_gen.generate_markdown_report()
        st.download_button(
            label="📝 Download Markdown",
            data=md_report,
            file_name=f"critique_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col_dl3:
        import json
        json_report = json.dumps(st.session_state.analysis_results, indent=2)
        st.download_button(
            label="📊 Download JSON",
            data=json_report,
            file_name=f"critique_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    # Reset button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start New Analysis", use_container_width=True):
        st.session_state.analysis_complete = False
        st.session_state.analysis_results = None
        st.session_state.uploaded_filename = None
        st.session_state.report_html = None
        st.rerun()

# Guidelines section at bottom (when no analysis)
else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f4f8 0%, #d1e9f0 100%); border-radius: 12px; padding: 25px; margin-top: 10px;">
        <h3 style="color: #2c3e50; margin-bottom: 15px; text-align: center;">📚 Assessment Criteria Overview</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px;">
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>1. Topic Relevance</strong><br>
                <small>Current scientific interest & knowledge gap</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>2. Source Strength</strong><br>
                <small>Journal impact factor & publisher credibility</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>3. PICO Clarity</strong><br>
                <small>Population, Intervention, Comparison, Outcome</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>4. Authorship</strong><br>
                <small>Expertise & conflict of interest declaration</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>5. Abstract Quality</strong><br>
                <small>IMRAD structure & authentic summary</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>6. Introduction</strong><br>
                <small>Literature knowledge & SMART objectives</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>7. Methodology</strong><br>
                <small>Study design & ethical considerations</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>8. Results Validity</strong><br>
                <small>Outcome variables & precision measures</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>9. Data Analysis</strong><br>
                <small>Statistical tools & inferential calculations</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>10. Discussion</strong><br>
                <small>Balanced corroboration & limitations</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>11. Conclusions</strong><br>
                <small>Justification & external validity</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>12. Research Impact</strong><br>
                <small>Evidence level & practice change</small>
            </div>
            <div style="background: white; border-radius: 8px; padding: 12px;">
                <strong>13. References</strong><br>
                <small>Currency & bias assessment</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)