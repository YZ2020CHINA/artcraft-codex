# gridcraft 工作方法

## 版本与证据

本机实测：`gridcraft-cli 0.17.0`。上游指南固定到 artcraft-skills `042c5d4ddcd8`，其应用审计版本通常比本机旧，正文部分有历史段落与新版本段落不一致。数值、缺失功能、格式列表和认证方式须用当前 CLI 帮助、MCP schema 或实际小文件验证。不要把“上游有菜单”视为本机端到端可用。

## 操作要点

- inspect_workbook/read_range 确认表、范围和类型，list_functions/evaluate_formula 发现函数和实际计算结果，再 write_range/format_range。保留公式，不能以看起来一样的常量替代。
- XLSX 是主要输出；老 .xls/.xlsb/.ods 的导入可能只有部分值、缓存或格式。用副本往返检查实际工作簿；不要承诺 Excel 修复提示为零。
- 宏可保留不代表会执行；.xlsm 改成 .xlsx 可能丢 VBA。加密输入的另存结果可能未加密，交付前明确检查。
- CSV/TSV/PDF 是导出，可能不清 dirty flag；保存原生工作簿后再关闭。资源 workbook/functions/commands 可用于只读检查。

## 按需查阅

- [上游应用详细指南](upstream-guide.md)：格式、编辑/导出、功能边界及历史认证信息。
- [当前本机 CLI 帮助](connection.md)：Windows 路径、headless/GUI 参数与 roots。
- [本机工具 schema 快照](tools.json)：准确的参数对象；有差异时使用实时 artcraft_tools。

上游文件位于 [gridcraft](https://github.com/midasmatterhorn/artcraft-skills/tree/042c5d4ddcd8e54178d72db3bc686a18658eee8d/gridcraft)；版权与许可见插件根目录 `licenses/artcraft-skills-MIT.txt`。未运行上游安装器，没有安装本机不存在的四款应用。
