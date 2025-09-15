import streamlit as st
import json
import pandas as pd
from collections import defaultdict

try:
    import boto3
    from botocore.exceptions import ClientError
except Exception:
    boto3 = None
    ClientError = Exception

st.set_page_config(page_title="Resource Optimizer Agent", layout="wide")
st.title("Resource Optimizer Agent — Demo (v0.1)")

st.markdown(
    "Upload a billing JSON or fetch it from S3 (optional). "
    "The app aggregates costs by the field you choose (supports dot notation like `tags.env`)."
)

source = st.radio("Load data from:", ("Local file (recommended)", "S3 (bucket/key)"))

records = []
if source == "Local file (recommended)":
    uploaded = st.file_uploader("Upload billing JSON (array of records)", type=["json"])
    if uploaded:
        try:
            text = uploaded.read().decode("utf-8")
            records = json.loads(text)
            st.success(f"Loaded {len(records):,} records from uploaded file")
        except Exception as e:
            st.error(f"Failed to parse JSON: {e}")
    else:
        st.info("Or use the sample data below to try the app.")
        if st.button("Load sample_data/sample_billing.json"):
            try:
                with open("../sample_data/sample_billing.json") as f:
                    records = json.load(f)
                st.success(f"Loaded {len(records):,} sample records")
            except Exception as e:
                st.error(f"Unable to load sample file: {e}")

else:
    bucket = st.text_input("S3 bucket")
    key = st.text_input("S3 key (path/to/file.json)")
    if st.button("Fetch from S3"):
        if not boto3:
            st.error("boto3 is not available in this environment. Install boto3 and configure credentials.")
        elif not bucket or not key:
            st.error("Provide both bucket and key.")
        else:
            try:
                s3 = boto3.client("s3")
                obj = s3.get_object(Bucket=bucket, Key=key)
                body = obj["Body"].read().decode("utf-8")
                records = json.loads(body)
                st.success(f"Loaded {len(records):,} records from s3://{bucket}/{key}")
            except ClientError as e:
                st.error(f"S3 access error: {e}")
            except Exception as e:
                st.error(f"Failed to load or parse object: {e}")

if records:
    st.sidebar.header("Options")
    key_field = st.sidebar.text_input("Aggregate by field (dot notation)", value="service")
    top_n = int(st.sidebar.number_input("Top N", min_value=1, max_value=100, value=5, step=1))
    show_raw = st.sidebar.checkbox("Show raw records", value=False)

    def get_field_value(record, key):
        if not key:
            return None
        parts = key.split(".")
        current = record
        for p in parts:
            if isinstance(current, dict) and p in current:
                current = current[p]
            else:
                return None
        return current

    totals = defaultdict(float)
    for r in records:
        k = get_field_value(r, key_field) or r.get(key_field) or r.get("service") or "unknown"
        try:
            cost = float(r.get("cost", 0) or 0)
        except Exception:
            cost = 0.0
        totals[k] += cost

    df = pd.DataFrame([{"key": k, "cost": v} for k, v in sorted(totals.items(), key=lambda x: x[1], reverse=True)])
    df_top = df.head(top_n).reset_index(drop=True)

    st.subheader("Top cost drivers")
    st.table(df_top)

    st.subheader("Cost distribution (bar chart)")
    st.bar_chart(df_top.set_index("key")["cost"])

    out_json = df_top.to_json(orient="records", indent=2)
    st.download_button("Download top results (JSON)", data=out_json, file_name="resource_optimizer_top.json", mime="application/json")

    if show_raw:
        st.subheader("Raw records (first 200 rows shown as table)")
        try:
            df_raw = pd.json_normalize(records)[:200]
            st.dataframe(df_raw)
        except Exception:
            st.write(records[:50])
