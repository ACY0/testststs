import streamlit as st
import pandas as pd

# Sayfa Ayarları
st.set_page_config(
    page_title="Survey Status Dashboard",
    page_icon="📊",
    layout="centered"
)

# Minimal CSS
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .sub-title {
            text-align: center;
            color: #6b7280;
            margin-bottom: 30px;
        }
        .card {
            padding: 24px;
            border-radius: 14px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        }
        .sent {
            background: linear-gradient(145deg, #e8f1ff, #ffffff);
        }
        .completed {
            background: linear-gradient(145deg, #e9f9f0, #ffffff);
        }
        .count {
            font-size: 42px;
            font-weight: 800;
            margin-top: 10px;
        }
        .label {
            font-size: 15px;
            letter-spacing: 1px;
            color: #6b7280;
        }
    </style>
""", unsafe_allow_html=True)

# Başlık
st.markdown('<div class="main-title">Survey Status Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload your Excel file – We analyze column D automatically</div>', unsafe_allow_html=True)

# Dosya Yükleme
uploaded_file = st.file_uploader("Upload Excel File (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        if df.shape[1] < 4:
            st.error("The uploaded Excel file must contain at least 4 columns.")
        else:
            status_col = df.iloc[:, 3]
            status_clean = status_col.astype(str).str.strip().str.lower()

            sent_count = (status_clean == "sent").sum()
            completed_count = (status_clean == "completed").sum()
            total = len(status_clean)

            st.write("")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                    <div class="card sent">
                        <div class="label">SENT</div>
                        <div class="count" style="color:#2563eb;">{sent_count}</div>
                        <div style="font-size:28px;">📤</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                    <div class="card completed">
                        <div class="label">COMPLETED</div>
                        <div class="count" style="color:#15803d;">{completed_count}</div>
                        <div style="font-size:28px;">✅</div>
                    </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.caption(f"Total rows analyzed: {total}")

            # Alt özet bar
            progress = int((completed_count / total) * 100) if total > 0 else 0
            st.progress(progress)

            st.caption(f"Completion Rate: {progress}%")

    except Exception as e:
        st.error(f"Processing error: {e}")
else:
    st.info("Please upload an Excel file to start analysis.")
