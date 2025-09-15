# ui/streamlit_app.py
import streamlit as st
import json
import pandas as pd
from collections import defaultdict
import boto3
from io import StringIO

st.set_page_config(page_title="Resource Optimizer", layout="wide")

st.title("Resource Optimizer Agent — Demo (v0.1)")

source = st.radio("Load data from:", ("Local file", "S3 (bucket/key)"))

records = []
if source == "Local file":
    uploaded = st.file_uploader("Upload billing JSON (array of records)", type=["json"])
    if uploaded:
        text = uploaded.read().decode("utf-8")
        records = json.loads(text)
else:
    bucket = st.text_input("S3 bucket")
    key = st.text_input("S3 key (path/to/file.json)")
    if st.button("Fetch from S3"):
        if not bucket or not key:
            st.error("Provide both bucket and key")
        else:
            try:
                s3 = boto3.client("s3")
                obj = s3.get_object(Bucket=bucket, Key=key)
                records = json.loads(obj["Body"].read().decode("utf-8"))
                st.success("Loaded from S3")
            except Exception as e:
                st.error(f"Failed to fetch S3 object: {e}")

if records:
    st.sidebar.header("Options")
    key_field = st.sidebar.text_input("Aggregate by field (dot notation)", value="service")
    top_n = st.sidebar.number_input("Top N", min_value=1, max_value=50, value=5, step=1)

    def get_field_value(record, key):
        if not key:
            return None
        parts = key.split(".")
        curr = record
        for p in parts:
            if isinstance(curr, dict) and p in curr:
                curr = curr[p]
            else:
                return None
        return curr

    totals = defaultdict(float)
    for r in records:
        k = get_field_value(r, key_field) or r.get(key_field) or r.get("service") or "unknown"
        try:
            cost = float(r.get("cost", 0) or 0)
        except Exception:
            cost = 0.0
        totals[k] += cost

    df = pd.DataFrame([
        {"key": k, "cost": v} for k, v in sorted(totals.items(), key=lambda x: x[1], reverse=True)
    ])
    df_top = df.head(top_n)
    st.subheader("Top cost drivers")
    st.table(df_top.reset_index(drop=True))

    st.subheader("Cost distribution")
    st.bar_chart(df_top.set_index("key")["cost"])
