import streamlit as st
import pandas as pd
st.image("logo.png", width=120)
st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="💰",
    layout="centered"
)

st.markdown(
    """
    <style>
    * {
        box-sizing: border-box;
    }

    .page-wrap {
        max-width: 1100px;
        margin: 0 auto;
    }

    .header-section {
        background: linear-gradient(135deg, #d9534f 0%, #c9302c 100%);
        padding: 28px 20px;
        border-radius: 20px 20px 0 0;
        text-align: center;
        color: white;
    }

    .header-section h1 {
        font-size: clamp(1.8rem, 2vw, 2.5rem);
        font-weight: 700;
        margin: 10px 0 0 0;
    }

    .logo-img {
        width: 110px;
        height: auto;
        border-radius: 14px;
    }

    .content-section {
        background: #ffffff;
        padding: 25px 20px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .input-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 12px;
    }

    .stNumberInput, .stSelectbox {
        margin-bottom: 12px;
    }

    .actions {
        display: flex;
        gap: 10px;
        margin-top: 20px;
        margin-bottom: 10px;
        flex-wrap: wrap;
    }

    .result-section {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 22px 18px;
        border: 1px solid #eee;
        margin-top: 14px;
    }

    .result-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 18px;
    }

    .result-box {
        background: linear-gradient(135deg, #f5f9ff 0%, #e8f4f8 100%);
        border-left: 5px solid #d9534f;
        border-radius: 10px;
        padding: 18px 16px;
        text-align: center;
        min-height: 130px;
    }

    .result-label {
        font-size: 0.88rem;
        color: #666;
        font-weight: 600;
    }

    .result-value {
        font-size: clamp(1.4rem, 2vw, 1.9rem);
        font-weight: 800;
        color: #d9534f;
        line-height: 1.3;
        margin-top: 8px;
        word-break: break-word;
    }

    .table-wrap {
        overflow-x: auto;
        margin-top: 18px;
    }

    .note-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 14px 16px;
        border-radius: 10px;
        margin-top: 18px;
        color: #856404;
    }

    @media (max-width: 768px) {
        .result-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# State
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# Header
st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="header-section">
        <img class="logo-img" src="https://raw.githubusercontent.com/tuyethane/streamlit-savings-calculator/main/logo.png" />
        <h1>💰 TÍNH LÃI GỬI TIẾT KIỆM</h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="content-section">', unsafe_allow_html=True)

st.markdown('<div class="input-title">📥 Nhập thông tin</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    so_tien_gui = st.number_input("Số tiền gửi (VNĐ)", min_value=0, value=100000000, step=1000000, format="%d")
with col2:
    lai_suat = st.number_input("Lãi suất (%/năm)", min_value=0.0, value=7.5, step=0.1, format="%.2f")

col3, col4 = st.columns(2)
with col3:
    ky_han = st.selectbox("Kỳ hạn", [1, 3, 6, 12, 18, 24, 36], format_func=lambda x: f"{x} tháng")
with col4:
    hinh_thuc_nhan_lai = st.selectbox("Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"])

col5, col6 = st.columns(2)
with col5:
    loai_lai = st.selectbox("Loại lãi", ["Lãi đơn", "Lãi kép"])
with col6:
    st.empty()

# Buttons
col_btn1, col_btn2 = st.columns([3, 1])
with col_btn1:
    if st.button("🧮 TÍNH LÃI", use_container_width=True):
        st.session_state.show_result = True
with col_btn2:
    if st.button("↻ Xóa", use_container_width=True):
        st.session_state.show_result = False
        st.rerun()

if st.session_state.show_result:
    if so_tien_gui > 0 and lai_suat > 0:
        def lay_so_ky_tinh_lai(ky_han_thang, hinh_thuc):
            if hinh_thuc == "Cuối kỳ":
                return 1
            elif hinh_thuc == "Hàng tháng":
                return ky_han_thang
            elif hinh_thuc == "Hàng quý":
                return max(1, ky_han_thang // 3)
            return 1

        so_ky = lay_so_ky_tinh_lai(ky_han, hinh_thuc_nhan_lai)
        so_nam = ky_han / 12

        if loai_lai == "Lãi đơn":
            tong_tien_lai = so_tien_gui * (lai_suat / 100) * so_nam
            lai_dinh_ky = tong_tien_lai / so_ky
            tong_tien = so_tien_gui + tong_tien_lai
        else:
            if hinh_thuc_nhan_lai == "Cuối kỳ":
                so_ky_lai_kep = 1
                lai_suat_ky = lai_suat / 100
            elif hinh_thuc_nhan_lai == "Hàng tháng":
                so_ky_lai_kep = ky_han
                lai_suat_ky = (lai_suat / 100) / 12
            else:
                so_ky_lai_kep = max(1, ky_han // 3)
                lai_suat_ky = (lai_suat / 100) / 4

            tong_tien = so_tien_gui * (1 + lai_suat_ky) ** so_ky_lai_kep
            tong_tien_lai = tong_tien - so_tien_gui
            lai_dinh_ky = tong_tien_lai / so_ky

        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown('<h3 style="color:#333; margin-bottom: 12px;">📊 Kết quả tính toán</h3>', unsafe_allow_html=True)

        st.markdown('<div class="result-grid">', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Tiền lãi định kỳ</div>
                <div class="result-value">{lai_dinh_ky:,.0f} VNĐ</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Tổng tiền lãi</div>
                <div class="result-value">{tong_tien_lai:,.0f} VNĐ</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Số tiền gốc</div>
                <div class="result-value">{so_tien_gui:,.0f} VNĐ</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Gốc + Lãi</div>
                <div class="result-value">{tong_tien:,.0f} VNĐ</div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<h3 style="color:#333; margin-top: 22px; margin-bottom: 10px;">📋 Thông tin chi tiết</h3>', unsafe_allow_html=True)
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.write(f"**Số tiền gửi:** {so_tien_gui:,.0f} VNĐ")
            st.write(f"**Kỳ hạn:** {ky_han} tháng")
            st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
            st.write(f"**Hình thức nhận lãi:** {hinh_thuc_nhan_lai}")
        with col_info2:
            st.write(f"**Loại lãi:** {loai_lai}")
            st.write(f"**Số kỳ tính lãi:** {so_ky}")
            ty_le = (tong_tien_lai / so_tien_gui) * 100 if so_tien_gui > 0 else 0
            st.write(f"**Tỷ lệ lợi nhuận:** {ty_le:.2f}%")

        st.markdown('<h3 style="color:#333; margin-top: 22px; margin-bottom: 10px;">📅 Lịch tính lãi</h3>', unsafe_allow_html=True)
        rows = []

        if loai_lai == "Lãi đơn":
            for i in range(1, so_ky + 1):
                rows.append({
                    "Kỳ": i,
                    "Gốc (VNĐ)": so_tien_gui,
                    "Lãi kỳ (VNĐ)": lai_dinh_ky,
                    "Tổng tiền (VNĐ)": so_tien_gui + i * lai_dinh_ky,
                })
        else:
            if hinh_thuc_nhan_lai == "Cuối kỳ":
                rows.append({
                    "Kỳ": 1,
                    "Gốc (VNĐ)": so_tien_gui,
                    "Lãi kỳ (VNĐ)": tong_tien_lai,
                    "Tổng tiền (VNĐ)": tong_tien,
                })
            elif hinh_thuc_nhan_lai == "Hàng tháng":
                for i in range(1, so_ky + 1):
                    tien_tai_kỳ = so_tien_gui * (1 + (lai_suat / 100) / 12) ** i
                    lai_ky = tien_tai_kỳ - so_tien_gui
                    rows.append({
                        "Kỳ": i,
                        "Gốc (VNĐ)": so_tien_gui,
                        "Lãi kỳ (VNĐ)": lai_ky,
                        "Tổng tiền (VNĐ)": tien_tai_kỳ,
                    })
            else:
                for i in range(1, so_ky + 1):
                    tien_tai_kỳ = so_tien_gui * (1 + (lai_suat / 100) / 4) ** i
                    lai_ky = tien_tai_kỳ - so_tien_gui
                    rows.append({
                        "Kỳ": i,
                        "Gốc (VNĐ)": so_tien_gui,
                        "Lãi kỳ (VNĐ)": lai_ky,
                        "Tổng tiền (VNĐ)": tien_tai_kỳ,
                    })

        df = pd.DataFrame(rows)
        df["Gốc (VNĐ)"] = df["Gốc (VNĐ)"].map(lambda x: f"{x:,.0f}")
        df["Lãi kỳ (VNĐ)"] = df["Lãi kỳ (VNĐ)"].map(lambda x: f"{x:,.0f}")
        df["Tổng tiền (VNĐ)"] = df["Tổng tiền (VNĐ)"].map(lambda x: f"{x:,.0f}")

        st.dataframe(df, hide_index=True, use_container_width=True)

        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Tải xuống CSV",
            data=csv,
            file_name="ket_qua_lai_tiet_kiem.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown('<div class="note-box">📌 Ứng dụng này chỉ mang tính tham khảo, không phải lời khuyên tài chính chính thức.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result-section"><div class="note-box" style="background:#f8d7da; border-left-color:#dc3545; color:#721c24;">⚠️ Vui lòng nhập số tiền gửi và lãi suất lớn hơn 0.</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
