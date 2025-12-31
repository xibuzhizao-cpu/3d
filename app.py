import streamlit as st
from stl import mesh
from streamlit_stl import stl_from_file
import os

# --- 1. 材料与单价配置 ---
MATERIALS = {
    "PLA (工程塑料)": {"density": 1.25, "price_factor": 1.0, "note": "适合常规手办、结构件"},
    "光敏树脂 (高精度)": {"density": 1.15, "price_factor": 2.2, "note": "表面光滑，适合精细模型"},
    "--- 金属打印专区 ---": {"density": 0, "price_factor": 0, "note": ""},
    "316L 不锈钢": {"density": 7.98, "price_factor": 8.5, "note": "硬度高，耐磨损"},
    "铝合金 (AlSi10Mg)": {"density": 2.68, "price_factor": 10.0, "note": "轻量化，散热出色"},
    "钛合金 (TC4)": {"density": 4.43, "price_factor": 22.0, "note": "极高强度，航天级品质"}
}

STARTUP_FEE = 20.0        # 起步费
BASE_PRICE_PER_GRAM = 0.6 # 基础单价
PROFIT_MARGIN = 2.5       # 综合利润倍数

# --- 2. 页面配置 ---
st.set_page_config(page_title="西部制造 | 3D打印在线报价", layout="wide")

# 侧边栏
with st.sidebar:
    st.header("🛠️ 西部制造服务中心")
    st.write("---")
    mat_name = st.selectbox("第一步：选择打印材料", list(MATERIALS.keys()))
    selected_mat = MATERIALS[mat_name]
    
    if selected_mat['density'] > 0:
        st.info(f"💡 **材料特性：** {selected_mat['note']}")
    
    st.write("---")
    st.subheader("📞 联系下单")
    st.success("✅ 全球发货 | 顺丰包邮")
    st.code("微信：xibuzhizao-cpu", language=None)
    st.caption("提示：STEP文件建议添加微信人工核价")

# --- 3. 主界面 ---
st.title("💰 3D打印在线自动报价系统")
st.write("支持 STL 自动算价；STEP 格式支持手动输入体积报价。")

uploaded_file = st.file_uploader("点击或拖拽上传模型文件", type=["stl", "step", "stp", "obj"])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    col_left, col_right = st.columns([3, 2])

    # 情况 A：STEP 格式
    if file_ext in ['step', 'stp']:
        with col_left:
            st.warning(f"⚠️ 检测到工业格式：{uploaded_file.name}")
            st.info("系统无法直接解析此格式体积，请在右侧输入体积手动报价。")
        with col_right:
            st.subheader("📝 手动辅助报价")
            manual_vol = st.number_input("请输入模型体积 (cm³)：", min_value=0.0, step=0.1)
            if manual_vol > 0 and selected_mat['density'] > 0:
                weight = manual_vol * selected_mat['density']
                price = max(STARTUP_FEE, weight * BASE_PRICE_PER_GRAM * selected_mat['price_factor'] * PROFIT_MARGIN)
                st.metric(label="预估总价 (元)", value=f"￥{price:.2f}")
                st.write(f"**预估重量：** {weight:.2f} 克")

    # 情况 B：STL 格式
    else:
        with open("temp.stl", "wb") as f:
            f.write(uploaded_file.getbuffer())
        with col_left:
            st.subheader("🔍 3D 模型预览")
            try:
                stl_from_file(file_path="temp.stl", color="#007bff")
            except:
                st.write("预览载入中...")
        with col_right:
            st.subheader("💰 自动报价单")
            try:
                your_mesh = mesh.Mesh.from_file("temp.stl")
                volume, _, _ = your_mesh.get_mass_properties()
                vol_cm3 = volume / 1000 
                if selected_mat['density'] > 0:
                    weight = vol_cm3 * selected_mat['density']
                    price = max(STARTUP_FEE, weight * BASE_PRICE_PER_GRAM * selected_mat['price_factor'] * PROFIT_MARGIN)
                    st.metric(label="预估总价 (元)", value=f"￥{price:.2f}")
                    st.write(f"**模型体积：** {vol_cm3:.2f} cm³")
                    st.balloons()
            except:
                st.error("解析失败，请检查文件。")

else:
    st.info("👋 欢迎！请上传模型文件开始报价。")

# --- 4. 页脚 (已修复报错的赋值问题) ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 西部制造 | 工业级3D打印专家</p>", unsafe_allow_index=True)
