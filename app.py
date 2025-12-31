import streamlit as st
from stl import mesh
import os

# --- 报价参数设置（可根据需要修改数字） ---
STARTUP_FEE = 20.0     # 起步费（元）
PRICE_PER_GRAM = 0.6   # 每克材料费（元）
DENSITY = 1.25         # 材料密度（PLA通常为1.25g/cm³）
PROFIT_MARGIN = 2.5    # 利润倍数

st.set_page_config(page_title="3D打印在线报价", layout="centered")
st.title("💰 3D打印在线自动报价")

uploaded_file = st.file_uploader("请上传您的 STL 模型文件", type=["stl"])

if uploaded_file:
    # 临时保存模型
    with open("temp.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # 使用 numpy-stl 解析体积
        your_mesh = mesh.Mesh.from_file("temp.stl")
        volume, _, _ = your_mesh.get_mass_properties()
        vol_cm3 = volume / 1000  # 换算为立方厘米
        
        # 计算重量和价格
        weight = vol_cm3 * DENSITY
        total_price = max(STARTUP_FEE, weight * PRICE_PER_GRAM * PROFIT_MARGIN)
        
        # 华丽地显示结果
        st.balloons()
        st.success(f"### 预估报价：￥{total_price:.2f}")
        st.write(f"模型预估重量：{weight:.2f} 克")
        st.info("💡 提示：此报价为系统预估，最终价格以客服确认为准。")
        
    except Exception as e:
        st.error("模型解析失败，请确保文件是标准的 STL 格式。")
