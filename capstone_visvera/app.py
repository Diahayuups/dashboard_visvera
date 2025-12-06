import streamlit as st
import json
import os
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Visvera | Interview Evaluation", layout="wide", page_icon="🧠")

# --- TITLE ---
st.markdown("""
<div style="
    background-color: rgba(255, 255, 255, 0.04);
    padding: 16px 20px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 15px;
    text-align: center;
    line-height: 1.6;
">
    <h3 style="color:#FFFFFF; font-weight:600; margin-bottom:10px;">📊 Visvera – Interview Evaluation Dashboard</h3>

    <p style="color:#DDDDDD;">
        This dashboard visualizes the final results of the <b>Visvera AI Interview Evaluation</b> pipeline executed locally.<br>
        It displays data from three main sources — <b>Verbal</b>, <b>Nonverbal</b>, and <b>Final Assessment</b> — 
        all generated directly from our custom-built models.<br><br>

        The dashboard serves as the main visualization interface to present candidate evaluation scores, reasoning details, 
        and overall system decisions in a clear and structured format.
    </p>

    <hr style="border: 0.5px solid rgba(255,255,255,0.1); margin: 10px 0;">

    <p style="color:#CCCCCC; font-size:14px;">
        <b>Informasi (Bahasa Indonesia):</b><br>
        Dashboard ini menampilkan hasil akhir dari seluruh pipeline sistem <b>Visvera AI Interview Evaluation</b> 
        yang telah dijalankan secara lokal. Data berasal dari tiga sumber utama — <b>verbal</b>, <b>nonverbal</b>, dan <b>final assessment</b> — 
        yang seluruhnya dihasilkan oleh model buatan tim.<br><br>
        Dashboard ini berfungsi sebagai media visualisasi utama untuk memperlihatkan hasil penilaian kandidat, alasan penilaian, 
        serta ringkasan keputusan akhir dari sistem secara terstruktur.
    </p>
</div>
""", unsafe_allow_html=True)


# --- PATH SETUP (biar file /data selalu bisa diakses di cloud) ---
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

def load_json(filename):
    """Load JSON file safely from the /data folder"""
    path = os.path.join(DATA_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

# --- LOAD FILES ---
verbal_data = load_json("hasil_final_evaluasi_assesment_verbal.json")
nonverbal_data = load_json("hasil_final_evaluasi_assesment_noVerbal.json")
final_data = load_json("hasil_final_evaluasi_assesment.json")

# --- SIDEBAR ---
st.sidebar.header("📂 Data Sources")
st.sidebar.write("- Verbal: hasil_final_evaluasi_assesment_verbal.json")
st.sidebar.write("- Nonverbal: hasil_final_evaluasi_assesment_noVerbal.json")
st.sidebar.write("- Final: hasil_final_evaluasi_assesment.json")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🗣️ Verbal Assessment", "👁️ Nonverbal Assessment", "📊 Final Result"])

# --- TAB 1: VERBAL ---
with tab1:
    st.header("Verbal Assessment Result")

    if verbal_data:
        for idx, s in enumerate(verbal_data, start=1):
            with st.expander(f"Question {idx} - Score: {s['score']}"):
                st.write(f"**Formula Score:** {s['verbal_formula_score']}")
                st.write(f"**Reason:** {s['reason']}")
    else:
        st.warning("⚠️ Data verbal belum tersedia. Pastikan file `hasil_final_evaluasi_assesment_verbal.json` ada di folder `/data`.")

# --- TAB 2: NONVERBAL ---
with tab2:
    st.header("Nonverbal Assessment Result")

    if nonverbal_data:
        nv = nonverbal_data["assessment_nonVerbal"]
        st.subheader("📉 Nonverbal Metrics")
        st.json(nv["metrics"])
        
        st.subheader("🎯 Scores")
        st.write(f"**Face Focus:** {nv['scores']['FaceFocus']}")
        st.write(f"**Gaze Movement:** {nv['scores']['GazeMovement']}")
        st.write(f"**Nonverbal Formula Score:** {nv['nonVerbal_formula_score']}")
        st.write(f"**Final Score:** {nv['final_score']}")
        st.write("📋 **Summary:**")
        st.info(nv["summary"])
    else:
        st.warning("⚠️ Data nonverbal belum tersedia. Pastikan file `hasil_final_evaluasi_assesment_noVerbal.json` ada di folder `/data`.")

# --- TAB 3: FINAL RESULT ---
with tab3:
    st.header("📊 Combined Final Evaluation")

    if final_data:
        overview = final_data["scoresOverview"]
        st.metric("🧠 Decision", final_data["decision"])
        st.metric("📅 Reviewed At", final_data["reviewedAt"])
        
        st.subheader("Scores Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Project", overview["project"])
        col2.metric("Interview", overview["interview"])
        col3.metric("Total", overview["total"])
        
        st.subheader("Interview Scores Detail")
        for idx, s in enumerate(final_data["reviewChecklistResult"]["interviews"]["scores"], start=1):
            with st.expander(f"Question {idx} - Score: {s['score']}"):
                st.write(s.get("reason", "No reason provided"))

        st.subheader("📝 Overall Notes")
        st.success(final_data["overallNotes"])
    else:
        st.warning("⚠️ Data final belum tersedia. Pastikan file `hasil_final_evaluasi_assesment.json` ada di folder `/data`.")

