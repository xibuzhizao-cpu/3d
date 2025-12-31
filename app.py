import streamlit as st
import trimesh # 强大的多格式处理库
from streamlit_stl import stl_from_file
import os

# ... 前面的材料参数保持不变 ...

# 修改上传组件，增加 obj 和 3mf
uploaded_file = st.file_uploader("请上传模型文件", type=["stl", "obj", "3mf", "step", "stp"])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    # 保存文件
    with open(f"temp.{file_ext}", "wb") as f:
        f.write(uploaded_file.getbuffer())

    if file_ext in ['step', 'stp']:
        st.warning("⚠️ 检测到 STEP 工业格式。由于该格式包含复杂参数，系统无法自动算价，请联系客服人工报价。")
        # 依然可以显示文件名
        st.info(f"文件名: {uploaded_file.name}")
    else:
        try:
            # 使用 trimesh 加载多种格式
            mesh_data = trimesh.load(f"temp.{file_ext}")
            
            # 如果是场景文件（包含多个零件），取其合集
            if isinstance(mesh_data, trimesh.Scene):
                volume = mesh_data.volume
            else:
                volume = mesh_data.volume
                
            vol_cm3 = volume / 1000 
            
            # ... 接下来的价格计算逻辑和显示代码 ...
            # 注意：只有 STL 格式支持 stl_from_file 预览
            if file_ext == 'stl':
                stl_from_file(file_path="temp.stl")
            else:
                st.info("该格式暂不支持 3D 实时预览，但体积计算已完成。")

        except Exception as e:
            st.error("解析失败，建议导出为 STL 格式再上传。")
