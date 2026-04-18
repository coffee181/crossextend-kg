# CrossExtend-KG 中文说明

[English](README.md) | 中文

## 当前项目定位

`CrossExtend-KG` 当前只保留面向论文主线的 O&M 表单知识图谱构建链路，核心约束如下：

- 输入类型只支持 `om_manual`
- 当前数据域只包含 `battery`、`cnc`、`nev`
- 运行时 backbone 固定，不做动态扩张
- 主方法变体为 `full_llm`
- 评测以人工标注 gold 子集为主
- 最高原则是 `no fallback`：不支持的文档、缺失的必要配置、失败的关键阶段都必须显式报错

## 文档入口

- `docs/SYSTEM_DESIGN.md`
  当前系统设计、阶段划分和强约束
- `docs/PIPELINE_INTEGRATION.md`
  端到端命令、检查点和验证方式
- `docs/PROJECT_ARCHITECTURE.md`
  仓库结构与模块职责
- `docs/EXECUTION_MEMORY.md`
  最近修复、有效运行和后续优先级
- `docs/MANUAL_ANNOTATION_PROTOCOL.md`
  论文用人工 gold 标注规范
- `docs/REAL_RUN_DATA_FLOW_OM_3DOMAIN_20260418.md`
  当前三域 O&M 真实运行链路说明

## 当前链路

```text
O&M markdown -> EvidenceRecord -> 固定 backbone -> retrieval -> attachment -> filtering -> graph assembly -> validation -> snapshot -> export
```

## 推荐命令

预处理：

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

主流程：

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```

可选多变体实验：

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek_full.json
```

## 当前状态

已验证的当前事实：

- 三个域的 O&M 文档都能进入同一条预处理链路
- UTF-8 BOM 清理有效
- MemoryBank 检索已按 `memory_id` 去重
- O&M 步骤节点能稳定保留在 `Task`
- 旧 `product_intro` / `fault_case` 路径已从活动代码和配置中移除

## 评测原则

- 自动生成参考只能视为 silver
- 论文主指标应基于人工标注并裁决后的 gold 子集

详见：

- `docs/MANUAL_ANNOTATION_PROTOCOL.md`
