import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Survey Status – Minimal Dashboard",
    page_icon="🍏",
    layout="wide"
)

# --- CUSTOM CSS (Apple vibes) ---
st.markdown(
    """
    <style>
        /* Arka plan ve genel yapı */
        .stApp {
            background: #f5f5f7;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
        }

        /* Header */
        .apple-header {
            text-align: center;
            padding-top: 40px;
            padding-bottom: 10px;
        }
        .apple-title {
            font-size: 40px;
            font-weight: 700;
            letter-spacing: -0.03em;
            color: #111827;
        }
        .apple-subtitle {
            font-size: 16px;
            color: #6b7280;
            margin-top: 8px;
        }

        /* Ana container */
        .apple-shell {
            max-width: 900px;
            margin: 30px auto 50px auto;
        }

        /* Glass / Card */
        .glass-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 24px;
            padding: 28px 26px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.18);
        }

        /* Upload kartı */
        .upload-title {
            font-size: 18px;
            font-weight: 600;
            color: #111827;
            margin-bottom: 8px;
        }
        .upload-desc {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 16px;
        }

        /* Stat kartları */
        .stats-row {
            display: flex;
            gap: 18px;
            margin-top: 20px;
        }
        .stat-card {
            flex: 1;
            border-radius: 20px;
            padding: 18px 18px;
            background: #f9fafb;
            border: 1px solid rgba(148, 163, 184, 0.25);
            display: flex;
            flex-direction: column;
            gap: 4px;
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        }
        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            border-color: rgba(59, 130, 246, 0.4);
        }
        .stat-label {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #6b7280;
        }
        .stat-value {
            font-size: 32px;
            font-weight: 700;
        }
        .stat-icon {
            font-size: 20px;
            margin-top: 4px;
        }

        .sent-color {
            color: #2563eb;
        }
        .completed-color {
            color: #16a34a;
        }

        /* Completion bar */
        .completion-wrapper {
            margin-top: 24px;
        }
        .completion-label-row {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 6px;
        }
        .completion-bar {
            width: 100%;
            height: 10px;
            border-radius: 999px;
            background: #e5e7eb;
            overflow: hidden;
        }
        .completion-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, #22c55e, #16a34a, #15803d);
            transition: width 0.4s ease;
        }

        /* Küçük text */
        .tiny-note {
            margin-top: 10px;
            font-size: 11px;
            color: #9ca3af;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- HEADER ---
st.markdown(
    """
    <div class="apple-header">
        <div class="apple-title">Survey Status</div>
        <div class="apple-subtitle">
            Upload your Excel file and instantly see how many <b>Sent</b> and <b>Completed</b> surveys you have.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Dış çerçeve
st.markdown('<div class="apple-shell">', unsafe_allow_html=True)

# İç kart başlangıcı
st.markdown('<div class="glass-card">', unsafe_allow_html=True)

# --- UPLOAD ALANI ---
st.markdown(
    """
    <div class="upload-title">Upload .xlsx file</div>
    <div class="upload-desc">
        We automatically read <b>Column D</b> and count how many rows are marked as <code>sent</code> and <code>completed</code>.
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    label=" ",
    type=["xlsx"],
    label_visibility="collapsed"
)

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        if df.shape[1] < 4:
            st.error("The uploaded file must contain at least 4 columns (we expect survey status in column D).")
        else:
            # D sütunu
            status_col = df.iloc[:, 3]
            status_clean = status_col.astype(str).str.strip().str.lower()

            sent_count = (status_clean == "sent").sum()
            completed_count = (status_clean == "completed").sum()
            total = len(status_clean)

            # Stat kartları
            st.markdown(
                f"""
                <div class="stats-row">
                    <div class="stat-card">
                        <div class="stat-label">Sent</div>
                        <div class="stat-value sent-color">{sent_count}</div>
                        <div class="stat-icon">📤</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Completed</div>
                        <div class="stat-value completed-color">{completed_count}</div>
                        <div class="stat-icon">✅</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Completion rate bar
            if total > 0:
                completion_rate = round((completed_count / total) * 100, 1)
            else:
                completion_rate = 0.0

            st.markdown(
                f"""
                <div class="completion-wrapper">
                    <div class="completion-label-row">
                        <div>Completion rate</div>
                        <div>{completion_rate}%</div>
                    </div>
                    <div class="completion-bar">
                        <div class="completion-fill" style="width: {completion_rate}%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="tiny-note">
                    Total rows analyzed in column D: <b>{total}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"Processing error: {e}")

else:
    # Henüz dosya yokken küçük not
    st.info("Drag & drop an Excel file here to get started.")

# Kart kapanışı + shell kapanışı
st.markdown("</div>", unsafe_allow_html=True)  # glass-card
st.markdown("</div>", unsafe_allow_html=True)  # apple-shell
