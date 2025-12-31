import streamlit as st
from stl import mesh
from streamlit_stl import stl_from_file
import os

# --- 1. 核心材料与报价参数配置 ---
MATERIALS = {
    "PLA (工程塑料)": {"density": 1.25, "price_factor": 1.0, "note": "适合常规手办、结构件"},
    "光敏树脂 (高精度)": {"density": 1.15, "price_factor": 2.2, "note": "表面光滑，适合精细模型"},
    "--- 金属打印专区 ---": {"density": 0, "price_factor": 0, "note": ""},
    "316L 不锈钢": {"density": 7.98, "price_factor": 8.5, "note": "硬度高，耐磨损"},
    "铝合金 (AlSi10Mg)": {"density": 2.68, "price_factor": 10.0, "note": "轻量化，散热出色"},
    "钛合金 (TC4)": {"density": 4.43, "price_factor": 22.0, "note": "极高强度，航天级品质"}
}

STARTUP_FEE = 20.0        # 起步费（元）
BASE_PRICE_PER_GRAM = 0.6 # 基础单价（元/克）
PROFIT_MARGIN = 2.5       # 利润倍数

# --- 2. 页面设置 ---
st.set_page_config(page_title="西部制造 | 3D打印在线报价", layout="wide")

# 侧边栏
with st.sidebar:
    st.header("🛠️ 西部制造服务中心")
    st.write("---")
    st.subheader("第一步：选择材料")
    mat_name = st.selectbox("请选择打印材料", list(MATERIALS.keys()))
    selected_mat = MATERIALS[mat_name]
    
    if selected_mat['density'] > 0:
        st.info(f"💡 **材料特性：** {selected_mat['note']}")
    
    st.write("---")
    st.subheader("📞 联系下单")
    st.success("✅ 全球发货 | 顺丰包邮")
    st.code("微信：xibuzhizao-cpu", language=None)
    st.caption("提示：STEP文件建议添加微信人工核价")

# --- 3. 主界面布局 ---
st.title("💰 3D打印在线自动报价系统")
st.write("支持 STL 自动算价；STEP/STP 格式支持手动输入体积报价。")

uploaded_file = st.file_uploader("点击或拖拽上传模型文件", type=["stl", "step", "stp", "obj"])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    # 左右分栏
    col_left, col_right = st.columns([3, 2])

    # --- 情况 A：STEP/STP 格式 (无法自动解析体积) ---
    if file_ext in ['step', 'stp']:
        with col_left:
            st.warning("⚠️ 检测到 STEP 工业格式。系统无法自动提取几何体积。")
            st.info(f"文件名: {uploaded_file.name}")
            st.image("https://via.placeholder.com/600x400.png?text=STEP+File+Detected", caption="STEP格式暂不支持在线预览")
            
        with col_right:
            st.subheader("📝 手动辅助报价")
            st.write("如果您知道模型的预估体积，请输入下方数值以获取报价：")
            # 引导用户输入体积
            manual_vol = st.number_input("请输入模型体积 (cm³)：", min_value=0.0, step=1.0, help="您可以在设计软件的'属性'或'测量'中查看体积")
            
            if manual_vol > 0:
                if selected_mat['density'] == 0:
                    st.error("请在左侧选择具体材料类型")
                else:
                    weight = manual_vol * selected_mat['density']
                    calc_price = weight * BASE_PRICE_PER_GRAM * selected_mat['price_factor'] * PROFIT_MARGIN
                    final_price = max(STARTUP_FEE, calc_price)
                    
                    st.metric(label="参考总价 (元)", value=f"￥{final_price:.2f}")
                    st.write(f"**预估重量：** {weight:.2f} 克")
                    st.success("报价已生成！请截图发给客服下单。")
            else:
                st.write("请在上方输入体积以激活报价计算。")

    # --- 情况 B：STL 格式 (支持自动解析与预览) ---
    else:
        with open("temp.stl", "wb") as f:
            f.write(uploaded_file.getbuffer())

        with col_left:
            st.subheader("🔍 3D 模型预览")
            try:
                stl_from_file(file_path="temp.stl", color="#007bff", material="flat")
                st.caption("🖱️ 鼠标左键旋转，右键平移，滚轮缩放")
            except:
                st.error("预览加载失败，但不影响报价计算。")

        with col_right:
            st.subheader("💰 自动报价单")
            try:
                your_mesh = mesh.Mesh.from_file("temp.stl")
                volume, _, _ = your_mesh.get_mass_properties()
                vol_cm3 = volume / 1000 
                
                if selected_mat['density'] == 0:
                    st.warning("⚠️ 请在左侧侧边栏选择具体的材料")
                else:
                    weight = vol_cm3 * selected_mat['density']
                    calc_price = weight * BASE_PRICE_PER_GRAM * selected_mat['price_factor'] * PROFIT_MARGIN
                    final_price = max(STARTUP_FEE, calc_price)

                    st.metric(label="预估总价 (元)", value=f"￥{final_price:.2f}")
                    st.write(f"**预估重量：** {weight:.2f} 克")
                    st.write(f"**模型体积：** {vol_cm3:.2f} cm³")
                    st.balloons()
            except Exception as e:
                st.error("模型读取失败，请检查文件是否损坏。")

else:
    st.info("👋 欢迎使用！请上传模型文件开始报价。")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 西部制造 | 工业级3D打印专家</p>", unsafe_allow_index=True)
