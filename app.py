import streamlit as st
import pandas as pd

st.image("logo.jpg")

st.set_page_config(
    page_title="Tính Lãi Gửi Tiết Kiệm",
    page_icon="💰",
    layout="wide"
)

st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .box {
        background: #f5f9ff;
        border-left: 5px solid #1f77b4;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 0.8rem;
    }
    .big-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #d9534f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>💰 ỨNG DỤNG TÍNH LÃI GỬI TIẾT KIỆM</div>", unsafe_allow_html=True)

# Input
st.sidebar.header("📥 Nhập thông tin")
so_tien_gui = st.sidebar.number_input("Số tiền gửi (VNĐ)", min_value=0, value=100000000, step=1000000)
lai_suat = st.sidebar.number_input("Lãi suất (%/năm)", min_value=0.0, value=7.5, step=0.1)
ky_han = st.sidebar.selectbox("Kỳ hạn", [1, 3, 6, 12, 18, 24, 36], format_func=lambda x: f"{x} tháng")
hinh_thuc_nhan_lai = st.sidebar.selectbox("Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"])
loai_lai = st.sidebar.selectbox("Loại lãi", ["Lãi đơn", "Lãi kép"])

# Chuyển đổi hình thức nhận lãi thành số kỳ
def lay_so_ky_tinh_lai(ky_han_thang, hinh_thuc):
    if hinh_thuc == "Cuối kỳ":
        return 1
    elif hinh_thuc == "Hàng tháng":
        return ky_han_thang
    elif hinh_thuc == "Hàng quý":
        return max(1, ky_han_thang // 3)
    return 1

so_ky = lay_so_ky_tinh_lai(ky_han, hinh_thuc_nhan_lai)

# Tính toán
if so_tien_gui > 0 and lai_suat > 0:
    so_nam = ky_han / 12

    if loai_lai == "Lãi đơn":
        tong_tien_lai = so_tien_gui * (lai_suat / 100) * so_nam
        lai_dinh_ky = tong_tien_lai / so_ky
        tong_tien = so_tien_gui + tong_tien_lai
    else:
        # Lãi kép theo hình thức nhận lãi
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

    # Hiển thị 4 thẻ thông tin
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class='box'>
                <div>Tiền lãi định kỳ</div>
                <div class='big-number'>{lai_dinh_ky:,.0f} VNĐ</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class='box'>
                <div>Tổng tiền lãi</div>
                <div class='big-number'>{tong_tien_lai:,.0f} VNĐ</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class='box'>
                <div>Gốc</div>
                <div class='big-number'>{so_tien_gui:,.0f} VNĐ</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class='box'>
                <div>Gốc + Lãi</div>
                <div class='big-number'>{tong_tien:,.0f} VNĐ</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Bảng chi tiết
    st.subheader("📊 Kết quả chi tiết")

    info = {
        "Số tiền gửi": f"{so_tien_gui:,.0f} VNĐ",
        "Kỳ hạn": f"{ky_han} tháng",
        "Lãi suất": f"{lai_suat:.2f}%/năm",
        "Hình thức nhận lãi": hinh_thuc_nhan_lai,
        "Loại lãi": loai_lai,
        "Tiền lãi định kỳ": f"{lai_dinh_ky:,.0f} VNĐ",
        "Tổng tiền lãi": f"{tong_tien_lai:,.0f} VNĐ",
        "Tổng số tiền gốc + lãi": f"{tong_tien:,.0f} VNĐ",
    }

    st.json(info)

    # Dữ liệu lịch
    st.subheader("📅 Lịch tính lãi")

    rows = []

    if loai_lai == "Lãi đơn":
        if hinh_thuc_nhan_lai == "Cuối kỳ":
            for i in range(1, so_ky + 1):
                rows.append({
                    "Kỳ": i,
                    "Gốc đầu kỳ": so_tien_gui,
                    "Lãi kỳ": lai_dinh_ky,
                    "Tổng": so_tien_gui + i * lai_dinh_ky
                })
        elif hinh_thuc_nhan_lai == "Hàng tháng":
            for i in range(1, so_ky + 1):
                rows.append({
                    "Kỳ": i,
                    "Gốc đầu kỳ": so_tien_gui,
                    "Lãi kỳ": lai_dinh_ky,
                    "Tổng": so_tien_gui + i * lai_dinh_ky
                })
        else:
            for i in range(1, so_ky + 1):
                rows.append({
                    "Kỳ": i,
                    "Gốc đầu kỳ": so_tien_gui,
                    "Lãi kỳ": lai_dinh_ky,
                    "Tổng": so_tien_gui + i * lai_dinh_ky
                })
    else:
        if hinh_thuc_nhan_lai == "Cuối kỳ":
            rows.append({
                "Kỳ": 1,
                "Gốc đầu kỳ": so_tien_gui,
                "Lãi kỳ": tong_tien_lai,
                "Tổng": tong_tien
            })
        elif hinh_thuc_nhan_lai == "Hàng tháng":
            for i in range(1, so_ky + 1):
                tien_tai_kỳ = so_tien_gui * (1 + (lai_suat / 100) / 12) ** i
                lai_ky = tien_tai_kỳ - so_tien_gui
                rows.append({
                    "Kỳ": i,
                    "Gốc đầu kỳ": so_tien_gui,
                    "Lãi kỳ": lai_ky,
                    "Tổng": tien_tai_kỳ
                })
        else:
            for i in range(1, so_ky + 1):
                tien_tai_kỳ = so_tien_gui * (1 + (lai_suat / 100) / 4) ** i
                lai_ky = tien_tai_kỳ - so_tien_gui
                rows.append({
                    "Kỳ": i,
                    "Gốc đầu kỳ": so_tien_gui,
                    "Lãi kỳ": lai_ky,
                    "Tổng": tien_tai_kỳ
                })

    df = pd.DataFrame(rows)
    df["Gốc đầu kỳ"] = df["Gốc đầu kỳ"].map(lambda x: f"{x:,.0f} VNĐ")
    df["Lãi kỳ"] = df["Lãi kỳ"].map(lambda x: f"{x:,.0f} VNĐ")
    df["Tổng"] = df["Tổng"].map(lambda x: f"{x:,.0f} VNĐ")

    st.dataframe(df, use_container_width=True, hide_index=True)

else:
    st.warning("⚠️ Vui lòng nhập số tiền gửi và lãi suất hợp lệ.")

st.markdown("---")
st.caption("📌 Ứng dụng này chỉ mang tính tham khảo, không phải lời khuyên tài chính.")\
