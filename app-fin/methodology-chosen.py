def get_procurement_advice(industry, objective):
    """
    根据行业背景和采购目标提供专业的采购管理方法论及选择原因

    参数:
    industry (str): 行业背景描述
    objective (str): 用户在采购方面想要达成的目标或解决的问题

    返回:
    tuple: 包含方法论和选择原因的元组
    """
    # 转换为小写便于关键词匹配
    industry_lower = industry.lower()
    objective_lower = objective.lower()

    # 分析行业关键词
    is_manufacturing = any(word in industry_lower for word in ["制造", "生产", "manufacture", "production"])
    is_retail = any(word in industry_lower for word in ["零售", "零售", "retail", "distribution"])
    is_construction = any(word in industry_lower for word in ["建筑", "construction", "building"])
    is_service = any(word in industry_lower for word in ["服务", "service"])

    # 分析采购目标关键词
    wants_portfolio = any(word in objective_lower for word in ["分类", "组合", "portfolio", "categorize"])
    wants_collaboration = any(word in objective_lower for word in ["合作", "联合", "协作", "collaboration", "joint"])
    wants_inventory = any(word in objective_lower for word in ["库存", "库存管理", "inventory", "stock"])
    wants_material = any(word in objective_lower for word in ["物料", "材料", "material"])
    wants_maintenance = any(word in objective_lower for word in ["维护", "维修", "maintenance", "repair"])

    # 根据分析结果推荐采购方法论
    if wants_portfolio or (wants_material and wants_inventory):
        methodology = "卡拉杰克采购组合模型 (Kraljic Portfolio Matrix)"
        reason = "卡拉杰克采购组合模型通过将采购物品按利润影响和供应风险两个维度进行分类，" \
                 "将采购项目分为战略型、杠杆型、瓶颈型和常规型四类，针对不同类型制定差异化采购策略。" \
                 "这一方法论特别适合帮助企业优化采购资源分配，建立高效的供应商关系管理体系，" \
                 "降低整体采购成本和风险。"

    elif wants_collaboration or any(word in objective_lower for word in ["供应商管理", "联合库存", "vmi"]):
        methodology = "VMI联合价值创造模型 (Vendor Managed Inventory)"
        reason = "VMI联合价值创造模型通过供应商参与买方的库存管理决策，实现供需双方的信息共享与协同合作。" \
                 "该方法论能够减少库存积压和缺货风险，降低整体供应链成本，提高响应速度。" \
                 "尤其适合需要与核心供应商建立长期战略合作关系的企业，通过信息共享和协同计划创造双赢局面。"

    elif wants_material and wants_inventory and is_manufacturing:
        methodology = "MRP物料需求计划方法论 (Material Requirements Planning)"
        reason = "MRP物料需求计划方法论基于生产计划和物料清单，精确计算生产所需的原材料和零部件数量及时间。" \
                 "该方法通过计算机系统实现物料需求的精准预测和计划，确保生产所需物料按时按量供应，" \
                 "同时最小化库存成本。特别适合制造型企业的生产物料采购管理，提高生产效率和物料周转率。"

    elif wants_maintenance or any(word in objective_lower for word in ["间接物料", "维护用品", "mro"]):
        methodology = "MRO分类采购管理方法论 (Maintenance, Repair, and Operations)"
        reason = "MRO分类采购管理方法论专注于非生产性物料的采购与管理，通过对维护、维修和运营所需物品进行分类，" \
                 "制定针对性的采购策略和库存管理方案。该方法能够提高间接物料的采购效率，降低库存成本，" \
                 "确保企业运营的连续性，特别适合需要大量维护和运营物料的行业。"

    else:
        # 当无法明确匹配时，推荐综合评估方法
        methodology = "采购方法论综合评估法"
        reason = "基于您提供的信息，我们建议先对采购需求进行全面评估，包括：\n" \
                 "1. 分析采购物品的特性和重要性\n" \
                 "2. 评估与供应商的合作模式需求\n" \
                 "3. 明确库存管理目标\n" \
                 "根据评估结果，可选择卡拉杰克采购组合模型进行分类管理，VMI模型优化供应商协作，\n" \
                 "MRP方法进行生产物料计划，或MRO分类管理间接物料，也可组合使用多种方法。"

    return methodology, reason


def main():
    print("=== 采购管理咨询方法论推荐系统 ===")
    print("请输入以下信息，我们将为您推荐合适的采购管理方法论")
    print("----------------------------------------")

    # 获取用户输入
    industry = input("1. 请描述您所在的行业背景：")
    objective = input("2. 请说明您在采购管理方面想要达成的目标或解决的问题：")

    # 获取咨询建议
    methodology, reason = get_procurement_advice(industry, objective)

    # 输出结果
    print("\n----------------------------------------")
    print("【推荐的采购管理方法论】")
    print(methodology)
    print("\n【选择该方法论的原因】")
    print(reason)
    print("\n----------------------------------------")
    print("希望以上建议对您有所帮助！如有其他问题，欢迎再次咨询。")


if __name__ == "__main__":
    main()
