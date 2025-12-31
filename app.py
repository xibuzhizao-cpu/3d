import streamlit as st
from stl import mesh
from streamlit_stl import stl_from_file # 导入预览插件
import os

# --- 材料参数配置 ---
MATERIALS = {
    "PLA (普通塑料)": {"density": 1.25, "price_factor": 1.0},
    "光敏树脂 (高精度)": {"density": 1.15, "price_factor": 2.0},
    "316L 不锈钢": {"density": 7.98, "price_factor": 8.0},
    "铝合金 (AlSi10Mg)": {"density": 2.68, "price_factor": 10.0}
}

STARTUP_FEE = 20.0
BASE_PRICE_PER_GRAM = 0.6
PROFIT_MARGIN = 2.5

st.set_page_config(page_title="西部制造-3D预览报价", layout="wide") # 改为宽屏模式
st.title("📦 3D模型在线预览与报价")

# 侧边栏配置
st.sidebar.header("配置选项")
material_name = st.sidebar.selectbox("选择材料：", list(MATERIALS.keys()))
selected_mat = MATERIALS[material_name]

uploaded_file = st.file_uploader("请上传您的 STL 模型文件", type=["stl"])

if uploaded_file:
    # 临时保存
    with open("temp.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # 左右分栏：左边看图，右边看报价
    col_view, col_price = st.columns([3, 2])
    
    with col_view:
        st.subheader("🔍 模型预览")
        # 核心功能：在线渲染 3D 模型
        # color 可以改颜色，例如 #FF9900 是橙色，#777777 是金属色
        stl_from_file(file_path="temp.stl", color="#0099FF", material="flat")
    
    with col_price:
        try:
            # 计算逻辑
            your_mesh = mesh.Mesh.from_file("temp.stl")
            volume, _, _ = your_mesh.get_mass_properties()
            vol_cm3 = volume / 1000 
            
            weight = vol_cm3 * selected_mat['density']
            cost = weight * BASE_PRICE_PER_GRAM * selected_mat['price_factor']
            total_price = max(STARTUP_FEE, cost * PROFIT_MARGIN)
            
            st.subheader("💰 报价清单")
            st.metric("预估总价", f"￥{total_price:.2f}")
            st.write(f"**所选材料：** {material_name}")
            st.write(f"**模型重量：** {weight:.2f} 克")
            st.write(f"**模型体积：** {vol_cm3:.2f} cm³")
            
            st.divider()
            st.info("💡 鼠标左键旋转，右键平移，滚轮缩放")
            
        except Exception as e:
            st.error("模型解析失败。")

st.sidebar.markdown("---")
st.sidebar.write("📱 微信：xibuzhizao-cpu")
