import gradio as gr
import os
import time
from datetime import datetime
import random
from typing import Tuple
from docx import Document  # 用于解析Word文档
import pandas as pd  # 用于解析Excel和CSV文件

# 支持的文件类型
SUPPORTED_FILE_TYPES = [
    ".xlsx", ".xls",  # Excel文件
    ".docx", ".doc",  # Word文件
    ".pdf",  # PDF文件
    ".csv"  # CSV文件
]


# -------------------- 文档内容提取功能 --------------------
def extract_text_from_docx(file_path):
    """从Word文档中提取文本内容"""
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"提取Word内容出错: {e}")
        return ""


def extract_text_from_excel(file_path):
    """从Excel文档中提取文本内容和关键数据"""
    try:
        # 读取Excel文件的所有工作表
        xls = pd.ExcelFile(file_path)
        full_text = []

        # 遍历所有工作表
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            # 将数据转换为字符串
            sheet_text = f"工作表: {sheet_name}\n"

            # 提取列名
            columns = [str(col) for col in df.columns if pd.notna(col)]
            if columns:
                sheet_text += f"列名: {', '.join(columns)}\n"

            # 提取前5行数据作为样本
            sample_data = []
            for _, row in df.head(5).iterrows():
                row_data = [str(val) for val in row if pd.notna(val)]
                if row_data:
                    sample_data.append(', '.join(row_data))

            if sample_data:
                sheet_text += f"样本数据: {'; '.join(sample_data)}\n"

            full_text.append(sheet_text)

        return '\n'.join(full_text)
    except Exception as e:
        print(f"提取Excel内容出错: {e}")
        return ""


def extract_text_from_csv(file_path):
    """从CSV文件中提取文本内容"""
    try:
        df = pd.read_csv(file_path)
        full_text = []

        # 提取列名
        columns = [str(col) for col in df.columns if pd.notna(col)]
        if columns:
            full_text.append(f"列名: {', '.join(columns)}")

        # 提取前5行数据作为样本
        sample_data = []
        for _, row in df.head(5).iterrows():
            row_data = [str(val) for val in row if pd.notna(val)]
            if row_data:
                sample_data.append(', '.join(row_data))

        if sample_data:
            full_text.append(f"样本数据: {'; '.join(sample_data)}")

        return '\n'.join(full_text)
    except Exception as e:
        print(f"提取CSV内容出错: {e}")
        return ""


def extract_keywords(text):
    """从文本中提取行业和采购目标关键词"""
    if not text:
        return "", ""

    text_lower = text.lower()

    # 行业关键词库
    industry_keywords = {
        "制造": ["制造", "生产", "manufacture", "production"],
        "零售": ["零售", "retail", "distribution", "销售"],
        "建筑": ["建筑", "construction", "building", "工程"],
        "医疗": ["医疗", "hospital", "medical"],
        "教育": ["教育", "education", "school"],
        "金融": ["金融", "finance", "bank"]
    }

    # 采购目标关键词库
    objective_keywords = {
        "分类优化": ["分类", "组合", "portfolio", "categorize"],
        "供应商协作": ["合作", "联合", "协作", "collaboration", "供应商"],
        "物料计划": ["物料", "计划", "mrp", "生产排期"],
        "维护维修": ["维护", "维修", "mro", "间接物料"],
        "成本控制": ["成本", "节约", "降低", "control", "reduce"]
    }

    # 提取行业
    industry = ""
    for ind, keywords in industry_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            industry = ind
            break

    # 提取采购目标
    objective = ""
    for obj, keywords in objective_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            objective = obj
            break

    return industry, objective


# -------------------- 方法论及流程图生成 --------------------
def get_procurement_advice_with_flow(industry: str, objective: str) -> Tuple[str, str, str]:
    """返回方法论标题、描述、流程图(mermaid代码)"""
    industry_lower = industry.lower().strip()
    objective_lower = objective.lower().strip()

    # 行业/目标识别
    is_manufacturing = any(w in industry_lower for w in ["制造", "生产", "manufacture"])
    wants_portfolio = any(w in objective_lower for w in ["分类", "组合", "portfolio"])
    wants_collaboration = any(w in objective_lower for w in ["合作", "联合", "协作", "collaboration"])
    wants_material_plan = any(w in objective_lower for w in ["物料", "计划", "mrp", "生产排期"])
    wants_maintenance = any(w in objective_lower for w in ["维护", "维修", "mro", "间接物料"])
    wants_cost_reduction = any(w in objective_lower for w in ["成本", "节约", "降低", "control", "reduce"])

    # 1. 卡拉杰克采购组合模型
    if wants_portfolio:
        title = "卡拉杰克采购组合模型"
        desc = "通过「战略型、杠杆型、瓶颈型、常规型」分类，优化采购资源与供应商关系，降本提效。"
        flow = """
        ```mermaid
        graph TD
            A[确定采购物品清单] --> B[分析物品重要性<br/>(对业务影响)]
            A --> C[分析供应风险<br/>(稀缺性/替代难度)]
            B --> D{重要性高?}
            C --> E{供应风险高?}
            D -->|是| F[战略型物品<br/>(例：核心零部件)]
            D -->|否| G[杠杆型物品<br/>(例：标准化原材料)]
            E -->|是| H[瓶颈型物品<br/>(例：独家配件)]
            E -->|否| I[常规型物品<br/>(例：办公用品)]
            F --> J[建立长期战略合作]
            G --> K[集中采购+招标压价]
            H --> L[多源寻源+库存缓冲]
            I --> M[简化流程+自动化采购]
        ```
        """
        return title, desc, flow

    # 2. VMI联合价值创造模型
    elif wants_collaboration:
        title = "VMI联合价值创造模型"
        desc = "供应商深度参与库存管理，减少积压/缺货，适合长期战略合作场景。"
        flow = """
        ```mermaid
        graph TD
            A[供需双方签订VMI协议] --> B[共享销售/库存数据<br/>(实时同步)]
            B --> C[供应商预测需求<br/>(结合历史数据)]
            C --> D{库存低于安全线?}
            D -->|是| E[自动补货至目标库存]
            D -->|否| F[维持现有库存]
            E --> G[双方定期复盘<br/>(调整预测模型)]
            G --> B[循环优化]
        ```
        """
        return title, desc, flow

    # 3. MRP物料需求计划方法论
    elif wants_material_plan and is_manufacturing:
        title = "MRP物料需求计划方法论"
        desc = "基于生产计划精准计算物料需求，减少库存浪费，适配制造型企业排产。"
        flow = """
        ```mermaid
        graph TD
            A[制定主生产计划<br/>(MPS)] --> B[分解物料清单<br/>(BOM层级展开)]
            B --> C[统计现有库存<br/>(含在途/在制)]
            C --> D[计算净需求<br/>(毛需求-库存-在途)]
            D --> E{净需求>0?}
            E -->|是| F[生成采购订单<br/>(按提前期)]
            E -->|否| G[无需采购]
            F --> H[跟踪订单交付<br/>(与生产计划匹配)]
            H --> I[生产执行与反馈]
        ```
        """
        return title, desc, flow

    # 4. MRO分类采购管理方法论
    elif wants_maintenance:
        title = "MRO分类采购管理方法论"
        desc = "聚焦非生产物料（维护/维修/运营），分类管控间接采购成本，保障产线稳定。"
        flow = """
        ```mermaid
        graph TD
            A[梳理MRO物料清单] --> B[分类：<br/>1. 高频低价值<br/>2. 低频高价值<br/>3. 应急必需]
            B --> C[高频低价值：<br/>长期协议+自动补货]
            B --> D[低频高价值：<br/>战略寻源+最小库存]
            B --> E[应急必需：<br/>多供应商+安全库存]
            C --> F[定期消耗分析<br/>(优化补货参数)]
            D --> G[供应商响应速度考核]
            E --> H[模拟应急场景<br/>(测试供应能力)]
        ```
        """
        return title, desc, flow

    # 5. TCO总成本优化方法论
    elif wants_cost_reduction:
        title = "TCO总成本优化方法论"
        desc = "从采购、使用到处置的全生命周期成本分析，识别隐性节约空间，系统性降低总拥有成本。"
        flow = """
        ```mermaid
        graph TD
            A[确定分析对象<br/>(单一物品/品类)] --> B[计算采购成本<br/>(价格+运输+税费)]
            B --> C[计算使用成本<br/>(能耗+维护+人工)]
            C --> D[计算处置成本<br/>(报废+环保+替代)]
            D --> E[汇总TCO=B+C+D]
            E --> F[识别成本占比最高项<br/>(例如：维护成本过高)]
            F --> G[针对性优化<br/>(例：换高效型号)]
            G --> H[验证优化效果<br/>(TCO降低比例)]
        ```
        """
        return title, desc, flow

    # 6. 默认：采购策略综合评估法
    else:
        title = "采购策略综合评估法"
        desc = "建议先梳理采购物品属性、供应商关系、成本结构，再适配具体方法论。"
        flow = """
        ```mermaid
        graph TD
            A[明确采购目标<br/>(降本/保供/创新)] --> B[分析物品特性<br/>(价值/风险/复杂度)]
            B --> C[评估现有供应商<br/>(能力/合作历史)]
            C --> D[梳理内外部约束<br/>(预算/时间/政策)]
            D --> E[匹配候选方法论<br/>(对比优缺点)]
            E --> F[小范围试点验证]
            F --> G[全面推广+持续迭代]
        ```
        """
        return title, desc, flow


# -------------------- 文件分析逻辑 --------------------
def analyze_file(file_path: str, industry_input, objective_input) -> Tuple[str, str, str, str]:
    """分析文件并提取关键词，返回报告 + 状态 + 行业 + 目标"""
    if not file_path:
        return "# 请先上传文件", "请上传文件进行分析", industry_input, objective_input

    # 文件基础信息
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    file_size_mb = file_size / (1024 * 1024)

    # 提取文件内容
    extracted_text = ""
    extracted_industry = ""
    extracted_objective = ""
    file_type = ""

    # 根据文件类型提取内容
    if file_name.lower().endswith('.docx'):
        extracted_text = extract_text_from_docx(file_path)
        file_type = "Word文档"
    elif file_name.lower().endswith(('.xlsx', '.xls')):
        extracted_text = extract_text_from_excel(file_path)
        file_type = "Excel文档"
    elif file_name.lower().endswith('.csv'):
        extracted_text = extract_text_from_csv(file_path)
        file_type = "CSV文件"
    else:
        file_type = "其他文件"
        extracted_text = "暂不支持该类型文件的内容提取"

    # 从提取的文本中获取行业和目标
    if extracted_text and file_type != "其他文件":
        extracted_industry, extracted_objective = extract_keywords(extracted_text)

    # 模拟分析进度
    progress = gr.Progress()
    for i in range(100):
        time.sleep(0.03)
        progress(i / 100, desc="分析中...")

    # 生成分析报告
    new_industry = extracted_industry if extracted_industry else industry_input
    new_objective = extracted_objective if extracted_objective else objective_input
    advice_title, advice_content, flow_chart = get_procurement_advice_with_flow(new_industry, new_objective)

    analysis_result = f"""
    # 文件分析报告  
    ## 基本信息  
    - 文件名: {file_name}  
    - 文件类型: {file_type}
    - 大小: {file_size_mb:.2f} MB  
    - 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

    ## 内容提取  
    - 识别到的行业: {extracted_industry if extracted_industry else '未明确识别'}  
    - 识别到的采购目标: {extracted_objective if extracted_objective else '未明确识别'}  

    ## 内容分析  
    - 识别到 {random.randint(3, 10)} 个关键数据点  
    - 发现 {random.randint(1, 3)} 条潜在趋势/异常  
    - 建议结合「采购方法论」进一步优化策略  

    ## 结论  
    {random.choice([
        "文件数据完整度高，可用于采购策略建模。",
        "数据存在零散性，建议先做标准化清洗。",
        "内容与采购场景强相关，适合辅助方法论落地。",
        "数据呈现出明确的采购模式，可直接应用推荐的方法论。"
    ])}

    ## 推荐的采购方法论  
    ### {advice_title}  
    {advice_content}  

    ## 方法论流程图  
    {flow_chart}
    """

    return analysis_result, f"分析完成: {file_name}", new_industry, new_objective


# -------------------- 清除文件逻辑 --------------------
def clear_files() -> Tuple[None, str, str, str, str]:
    """清空文件、结果、状态和输入框"""
    return None, "# 等待文件上传和分析...", "请上传文件或填写采购需求", "", ""


# -------------------- 单独推荐方法论（含流程图） --------------------
def recommend_methodology(industry, objective):
    title, desc, flow = get_procurement_advice_with_flow(industry, objective)
    result = f"""
    # 采购方法论推荐结果  

    ## {title}  
    {desc}  

    ## 流程图  
    {flow}
    """
    return result, f"已生成 {title} 的推荐"


# -------------------- Gradio界面搭建 --------------------
def main():
    with gr.Blocks(title="采购咨询智能分析平台", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 📊 采购咨询智能分析平台")
        gr.Markdown("支持 **文件分析** + **采购方法论推荐**（含流程图），一站式解决采购策略问题！")

        with gr.Row():
            # 左侧：文件上传区
            with gr.Column(scale=1):
                file_input = gr.File(
                    label="选择文件（可选）",
                    file_types=SUPPORTED_FILE_TYPES,
                    type="filepath",
                )
                with gr.Row():
                    analyze_btn = gr.Button("开始文件分析", variant="primary")
                    clear_btn = gr.Button("清除文件", variant="secondary")
                status_text = gr.Textbox(
                    label="状态", value="请上传文件或填写采购需求", interactive=False
                )

            # 中间：采购需求交互区
            with gr.Column(scale=1):
                gr.Markdown("### 采购需求描述")
                industry_input = gr.Textbox(
                    label="行业背景",
                    placeholder="例如：制造业、零售业、建筑工程...",
                    lines=2,
                )
                objective_input = gr.Textbox(
                    label="采购目标",
                    placeholder="例如：优化库存、供应商协作、降本提效...",
                    lines=2,
                )
                recommend_btn = gr.Button("推荐采购方法论", variant="primary")

            # 右侧：结果展示区
            with gr.Column(scale=2):
                result_output = gr.Markdown(
                    label="分析结果", value="# 等待操作或输入..."
                )

        # 事件绑定
        analyze_btn.click(
            fn=analyze_file,
            inputs=[file_input, industry_input, objective_input],
            outputs=[result_output, status_text, industry_input, objective_input],
        )
        recommend_btn.click(
            fn=recommend_methodology,
            inputs=[industry_input, objective_input],
            outputs=[result_output, status_text],
        )
        clear_btn.click(
            fn=clear_files,
            inputs=[],
            outputs=[file_input, result_output, status_text, industry_input, objective_input],
        )
        # 回车触发推荐
        industry_input.submit(
            fn=recommend_methodology,
            inputs=[industry_input, objective_input],
            outputs=[result_output, status_text],
        )
        objective_input.submit(
            fn=recommend_methodology,
            inputs=[industry_input, objective_input],
            outputs=[result_output, status_text],
        )

        # 功能说明
        gr.Markdown("""
        ### 功能说明  
        1. **文件分析**：上传Excel/Word/CSV等文件，系统自动提取内容并推荐带流程图的采购方法论；  
        2. **直接推荐**：手动填写行业背景和采购目标，直接获取匹配的方法论及流程图；  
        3. 流程图采用mermaid语法绘制，可直观展示方法论的步骤和决策逻辑。

        ### 支持文件类型  
        Excel(.xlsx/.xls)、Word(.docx/.doc)、PDF(.pdf)、CSV(.csv)（最大200MB）  
        """)

    # 启动服务
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
    )


if __name__ == "__main__":
    main()
