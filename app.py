import os
import sys

# 傻瓜式环境安装：如果缺插件，代码会自动帮你在云端装好
try:
    import streamlit as st
    from stl import mesh
    import numpy as np
except ImportError:
    os.system(f"{sys.executable} -m pip install streamlit numpy-stl")
    # 安装完需要刷新一下环境，直接提示用户或自动重试
    st.warning("系统正在初始化环境，请稍等10秒后刷新页面...")
    st.stop()

# --- 这里是你的报价逻辑，你可以随时改这里的数字 ---
STARTUP_FEE = 20.0  # 起步费
PRICE_PER_GRAM = 0.6  # 每克材料费
DENSITY = 1.25  # PLA材料密度
PROFIT_MARGIN = 2.5  # 利润倍数

st.set_page_config(page_title="我的3D打印报价单")
st.title("🚀 3D打印在线自动报价")

uploaded_file = st.file_uploader("第一步：请上传您的 STL 模型文件", type=["stl"])

if uploaded_file:
    # 临时保存文件
    with open("temp.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # 解析模型体积
        your_mesh = mesh.Mesh.from_file("temp.stl")
        volume, _, _ = your_mesh.get_mass_properties()
        vol_cm3 = volume / 1000  # 换算成立方厘米
        
        # 计算价格
        weight = vol_cm3 * DENSITY
        total_price = max(STARTUP_FEE, weight * PRICE_PER_GRAM * PROFIT_MARGIN)
        
        # 华丽地显示结果
        st.balloons()
        st.success(f"### 💰 预估报价：￥{total_price:.2f}")
        st.info(f"模型信息：预估重量约 {weight:.2f} 克")
    except Exception as e:
        st.error(f"模型读取失败，请确保是标准的STL格式。错误原因: {e}")
