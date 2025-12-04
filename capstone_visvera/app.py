import streamlit as st
import json
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Visvera | Interview Evaluation", layout="wide", page_icon="🧠")

# --- TITLE ---
st.title("🎯 Visvera - Interview Evaluation Dashboard")

# --- LOAD DATA FUNCTION ---
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# --- LOAD FILES ---
verbal_data = load_json("data/hasil_final_evaluasi_assesment_verbal.json")
nonverbal_data = load_json("data/hasil_final_evaluasi_assesment_noVerbal.json")
final_data = load_json("data/hasil_final_evaluasi_assesment.json")

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
        st.warning("Data verbal belum tersedia. Pastikan file hasil_final_evaluasi_assesment_verbal.json ada di folder /data")

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
        st.warning("Data nonverbal belum tersedia. Pastikan file hasil_final_evaluasi_assesment_noVerbal.json ada di folder /data")

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
        st.warning("Data final belum tersedia. Pastikan file hasil_final_evaluasi_assesment.json ada di folder /data")
