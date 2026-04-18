# 真实运行数据流：三域 O&M 主链路（2026-04-18）

**更新日期**: 2026-04-18  
**范围**: 当前 `battery / cnc / nev` 三域运维表单真实链路

## 1. 使用的数据

当前真实输入文件为：

- `data/battery/BATOM_001.md`
- `data/cnc/CNCOM_001.md`
- `data/nev/EVMAN_001.md`

三份数据统一按以下类型处理：

- `source_type = "om_manual"`

## 2. 运行命令

预处理：

```bash
python -m crossextend_kg.cli preprocess --config D:\crossextend_kg\config\persistent\preprocessing.deepseek.json
```

主流程：

```bash
python -m crossextend_kg.cli run --config D:\crossextend_kg\config\persistent\pipeline.deepseek.json
```

## 3. 本轮适配后的关键改动

当前链路已经完成这些针对 O&M 的适配：

- 支持 `BATOM_* / CNCOM_* / EVMAN_*` 文件名自动识别为 `om_manual`
- 读取 markdown 时自动去 BOM
- 预处理 prompt 改成 O&M 专用版本
- 过滤阶段强制保住 `T1/T2/...` 步骤任务
- 观测类候选可以在证据充分时被重锚为 `Signal` / `State`
- MemoryBank 检索前按 `memory_id` 去重
- 关系约束重新整理为适合 O&M 诊断语义的版本

## 4. 当前质量最强的一次运行

运行目录：

- `artifacts/deepseek-20260418T095937Z`

这次运行最适合作为“当前架构已经适配成功”的展示样本。

### 4.1 验证结果

- relation validation: `114 / 117` 有效
- 剩余无效关系族：
  - `communication = 2`

### 4.2 各域结果

- `battery`
  - `37` 个接纳节点
  - `44` 条接纳三元组
- `cnc`
  - `33` 个接纳节点
  - `31` 条接纳三元组
- `nev`
  - `38` 个接纳节点
  - `39` 条接纳三元组

### 4.3 这次运行说明了什么

- `T<number>` 步骤节点已经能稳定保留为 `Task`
- 含有 `report/document` 的步骤标题不再被误判成文档标题
- `pressure result`、`fresh wetting`、`wet after shutdown` 这类运维观测量已经能进入图
- `historical_context.json` 中的重复记忆命中已经消失
- `CNCOM_001` 的 BOM 污染已经被清掉

### 4.4 还剩下的误差

这次剩余的 2 条无效边主要来自少见关系动词没有完全归一：

- `T6 Inspect Components -> separates -> connector leakage`
- `T6 Inspect Components -> separates -> plate-side crack`

这属于局部关系词归一问题，不是架构失效。

## 5. 最新确认运行

运行目录：

- `artifacts/deepseek-20260418T101615Z`

这次运行是在补充 `separates` 归一后再次执行的确认跑。

### 5.1 验证结果

- relation validation: `106 / 108` 有效
- 剩余无效关系族：
  - `lifecycle = 1`

### 5.2 结论

它说明：

- 最后的归一补丁没有把主链路搞坏
- 当前系统已经能稳定跑通三域 O&M 数据

但它也暴露出一个更核心的现实：

- LLM 预处理本身仍然存在一定运行间方差

所以当前真正要解决的重点已经不是“能不能适配 O&M”，而是“如何让评测更稳、更可信”。

## 6. 当前阶段性判断

### 已经基本解决的问题

1. 运维表单已经可以贯通到最终图谱。
2. 预处理对 O&M 文件类型和 BOM 的适配已经完成。
3. 过滤规则已经显著贴近运维步骤与观测量语义。
4. 记忆检索不会再因为重复条目放大历史提示。

### 仍然需要继续优化的问题

1. 预处理 LLM 抽取存在随机性。
2. 低频关系词仍需继续补充归一规则。
3. 某些非常细碎但无关系支撑的部件候选仍会被过抽取，不过目前大多能被干净拒绝。

## 7. 论文写法建议

当前最稳妥的论文写法应该是：

- 把 2026-04-18 的三域 O&M 主链路作为当前系统
- 用质量最强的运行展示真实产物
- 诚实说明重复运行仍有方差
- 主指标使用人工标注 gold 子集
- 自动生成参考只作为 silver
