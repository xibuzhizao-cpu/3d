import os
import sys
import subprocess

# --- 强力初始化：如果缺零件，强制在后台静默安装 ---
def install_requirements():
    try:
        import stl
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy-stl"])
        st.rerun()

import streamlit as st

# 启动时先检查安装
install_requirements()
from stl import mesh

# --- 你的报价逻辑 ---
STARTUP_FEE = 20.0  # 起步费
PRICE_PER_GRAM = 0.6  # 每克材料费
DENSITY = 1.25  # PLA材料密度
PROFIT_MARGIN = 2.5  # 利润倍数

st.set_page_config(page_title="我的3D打印报价单")
st.title("🚀 3D打印在线自动报价")

uploaded_file = st.file_uploader("第一步：请上传您的 STL 模型文件", type=["stl"])

if uploaded_file:
    with open("temp.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        your_mesh = mesh.Mesh.from_file("temp.stl")
        volume, _, _ = your_mesh.get_mass_properties()
        vol_cm3 = volume / 1000 
        weight = vol_cm3 * DENSITY
        total_price = max(STARTUP_FEE, weight * PRICE_PER_GRAM * PROFIT_MARGIN)
        
        st.balloons()
        st.success(f"### 💰 预估报价：￥{total_price:.2f}")
        st.info(f"模型信息：预估重量约 {weight:.2f} 克")
    except Exception as e:
        st.error(f"解析失败: {e}")
