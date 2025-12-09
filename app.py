import streamlit as st
import pandas as pd

st.set_page_config(page_title="Survey Status Counter", page_icon="📊", layout="centered")

# Başlık
st.title("📊 Survey Status Counter")
st.write("Excel (.xlsx) dosyanı yükle, ben de D sütunundaki **Sent / Completed** sayılarını sayayım.")

# Dosya yükleme
uploaded_file = st.file_uploader("Excel dosyanızı (.xlsx) yükleyin", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Excel'i oku
        df = pd.read_excel(uploaded_file)

        # En az 4 sütun var mı kontrolü
        if df.shape[1] < 4:
            st.error("Bu dosyada 4 sütun yok. Lütfen D sütununda survey durumu olan bir dosya yükleyin.")
        else:
            # D sütununu (index 3) al
            status_col = df.iloc[:, 3]

            # Metin haline getir, sağ/sol boşlukları temizle, küçük harfe çevir
            status_normalized = status_col.astype(str).str.strip().str.lower()

            # Sayımlar
            sent_count = (status_normalized == "sent").sum()
            completed_count = (status_normalized == "completed").sum()

            total_rows = len(status_col)

            st.divider()

            st.subheader("🔎 Sonuçlar")

            # 2 sütunlu layout
            col1, col2 = st.columns(2)

            with col1:
                # Sent (mavi)
                st.markdown(
                    f"""
                    <div style="background-color:#e8f2ff; padding:15px; border-radius:10px; text-align:center;">
                        <div style="font-size:40px;">📤</div>
                        <div style="font-size:18px; font-weight:bold; color:#1f6feb;">Sent</div>
                        <div style="font-size:26px; font-weight:bold; color:#1f6feb;">{sent_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                # Completed (yeşil)
                st.markdown(
                    f"""
                    <div style="background-color:#e7f8ec; padding:15px; border-radius:10px; text-align:center;">
                        <div style="font-size:40px;">✅</div>
                        <div style="font-size:18px; font-weight:bold; color:#1a7f37;">Completed</div>
                        <div style="font-size:26px; font-weight:bold; color:#1a7f37;">{completed_count}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.write("")
            st.caption(f"Toplam satır: **{total_rows}** (D sütunundaki hücre sayısı)")

            # Küçük bir özet tablo
            st.write("📋 Özet tablo:")
            summary_df = pd.DataFrame(
                {
                    "Status": ["Sent", "Completed"],
                    "Count": [sent_count, completed_count],
                }
            )
            st.table(summary_df)

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Lütfen önce bir Excel dosyası yükleyin.")
