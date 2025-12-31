import streamlit as st
from stl import mesh
import os

# --- 价格参数（你可以根据需要修改这些数字） ---
STARTUP_FEE = 20.0     # 起步费（元）
PRICE_PER_GRAM = 0.6   # 每克材料成本（元）
DENSITY = 1.25         # 材料密度 (g/cm³)
PROFIT_MARGIN = 2.5    # 利润倍数

st.set_page_config(page_title="3D打印在线报价", layout="centered")
st.title("💰 3D打印在线自动报价系统")

uploaded_file = st.file_uploader("第一步：请上传您的 STL 模型文件", type=["stl"])

if uploaded_file:
    # 临时保存上传的文件
    with open("temp.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # 使用插件解析体积
        your_mesh = mesh.Mesh.from_file("temp.stl")
        volume, _, _ = your_mesh.get_mass_properties()
        vol_cm3 = volume / 1000  # 换算为立方厘米
        
        # 计算重量和价格
        weight = vol_cm3 * DENSITY
        total_price = max(STARTUP_FEE, weight * PRICE_PER_GRAM * PROFIT_MARGIN)
        
        # 显示报价结果
        st.balloons()
        st.success(f"### 预估报价：￥{total_price:.2f}")
        st.write(f"模型预估重量：约 {weight:.2f} 克")
        st.info("💡 提示：此报价为自动计算，最终价格请联系客服确认。")
        
    except Exception as e:
        st.error(f"解析失败，请确保上传的是标准的 STL 格式文件。")
