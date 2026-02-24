# app.py
import os
import time
import streamlit as st

from proposal_engine import build_payload, generate_proposal_offline
from roi import ROIInput, compute_roi
from export_pptx import export_to_pptx
from export_docx import export_to_docx

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="AI Sales Proposal Automation", layout="wide")
st.title("AI Sales Proposal Automation – Enterprise Edition")

with st.sidebar:
    st.header("Client Inputs")
    industry = st.selectbox("Client Industry", ["Finance", "Logistics", "Retail"])
    company_size = st.selectbox("Company Size", ["SME", "Enterprise"])
    pain_points = st.multiselect(
        "Key Pain Points",
        ["manual process", "high cost", "slow approval", "inconsistent quality", "slow response to client", "lack of standard template"],
        default=["manual process", "inconsistent quality"],
    )
    workflow = st.text_area(
        "Current Workflow Description",
        "Sales writes proposals manually using Word/PowerPoint; revisions via email; no standard ROI model."
    )
    budget = st.selectbox("Budget Range", ["<HKD 50k", "HKD 50k–100k", "HKD 100k–300k", "HKD 300k+"])
    objective = st.text_input("Project Objective", "Reduce proposal preparation time and standardize deliverables.")
    timeline = st.selectbox("Timeline", ["2–4 weeks", "1–2 months", "2–3 months"])

st.subheader("ROI Calculator (for the proposal)")
c1, c2, c3, c4 = st.columns(4)
with c1:
    proposals_per_week = st.number_input("Proposals / week", min_value=1, value=10)
with c2:
    hours_before = st.number_input("Hours before", min_value=0.5, value=3.0, step=0.5)
with c3:
    hours_after = st.number_input("Hours after", min_value=0.1, value=1.0, step=0.1)
with c4:
    cost_per_hour = st.number_input("Cost per hour (HKD)", min_value=50, value=300, step=50)

roi_result = compute_roi(ROIInput(
    proposals_per_week=int(proposals_per_week),
    hours_before=float(hours_before),
    hours_after=float(hours_after),
    cost_per_hour_hkd=float(cost_per_hour),
    tool_monthly_cost_hkd=0.0
))
st.write(roi_result)

st.divider()

if st.button("Generate Proposal"):
    payload = build_payload(
        industry=industry,
        company_size=company_size,
        pain_points=pain_points,
        workflow=workflow,
        budget=budget,
        objective=objective,
        timeline=timeline,
    )

    data = generate_proposal_offline(payload)

    data["roi_estimation_notes"] = (
        f"Based on inputs: {roi_result['weekly_hours_saved']} hours saved/week, "
        f"~HKD {roi_result['monthly_cost_saved_hkd']} saved/month, "
        f"~HKD {roi_result['annual_net_saving_hkd']} saved/year (assumptions adjustable)."
    )

    ts = time.strftime("%Y%m%d-%H%M%S")
    pptx_path = os.path.join(OUTPUT_DIR, f"proposal_{industry}_{ts}.pptx")
    docx_path = os.path.join(OUTPUT_DIR, f"proposal_{industry}_{ts}.docx")

    export_to_pptx(data, pptx_path)
    export_to_docx(data, docx_path)

    st.success("Generated!")
    st.subheader("Preview (JSON)")
    st.json(data)

    with open(pptx_path, "rb") as f:
        st.download_button("Download PPTX", f, file_name=os.path.basename(pptx_path))
    with open(docx_path, "rb") as f:
        st.download_button("Download DOCX", f, file_name=os.path.basename(docx_path))
