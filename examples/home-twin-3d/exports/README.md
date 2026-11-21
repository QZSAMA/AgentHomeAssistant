# NeonPlan 3D 导入成果

推荐使用 **wuhan-neonplan-backup.json**：在真实 NeonPlan 的 **Editor → Backup → Import** 中导入，或先打开本项目的本地预览：

`/vendor/neonplan/preview/wuhan.html?lang=zh&style=cozy&nopro`

本地预览使用官方模拟 Home Assistant 环境，自动装载上述备份；它不控制真实设备。客厅主灯、餐厅吊灯、电竞房主灯、电竞房桌面灯这四个示意点位仅在本页内存中绑定 `light.demo_wuhan_*`，可点灯具或右下按钮切换。重载恢复导入文件和关灯状态，不保存模拟修改。原版演示入口是 `/vendor/neonplan/preview/index.html`。

## 已实际执行的验证

- 固定上游：Mastershort/neonplan3d **v4.0.0**，commit **8a0fecd90c4eb565c8af8e2fcac01346125f069f**，MIT；官方必要源码、bundle、字体和许可证保存在 `vendor/neonplan`，没有下载大批演示图片。
- 用未经修改的官方 TypeScript `readSimple → buildPlan` 读取简化 JSON。
- 用官方 `exportFile → parseExport` 验证完整备份，运行官方 `generateWalls / openingHost / locateOpening` 检查实际墙体生成与开口附着。
- 用官方 Home Assistant 后端 `schema.py` 的 `BUILDING_SCHEMA`（本地 voluptuous 0.15.2）实际验证完整 Building。
- 六项回归测试覆盖房间数、单位/尺度、弧度转角度、窗宽、相邻区域、“开放客餐厅不生成虚构隔墙”、“备份灯模型不绑定虚构实体”、有效材质枚举，以及材质更新不移动/旋转原家具、不改变墙开口、重复导出不叠加装饰。具体结果见 `neonplan-validation.json`。
- 已在本机 Chromium 实际加载官方3D组件并点击模拟灯；截图 `neonplan-preview-off.png` / `neonplan-preview-on.png`。这是官方前端的本地 mockHA 测试，不能替代真实 HA 接入联调。

## 为什么同时交付两份 JSON

`wuhan-neonplan-import.json` 是官方公开的 `neonplan-import` 简化输入格式，供复现转换过程使用，**不建议将它直接作为最终户型导入**。本项目的九个 polygon 是地面语义分区，包含开放客餐厅；它们不是闭合墙中心线。官方简化导入器会默认沿所有房间边界生墙，且当前图会在自动吸附时丢弃两处开口。

`wuhan-neonplan-backup.json` 是先跑官方导入器，再应用本地适配得到的完整原生格式：设置所有区域边的 `wall_heights=0`（官方支持的“无墙”值），保留 CAD 审核后的 32 段实体墙；为 10 个门窗另建原生开口承载墙，再用原生 opening 切出开口。因此全部十处开口都有真实渲染墙锚点，开放分区不会凭空生墙。承载墙两端各延伸 20 mm，避免端部脱缝。家具坐标和尺寸保留；源旋转弧度转换为官方顺时针角度；吧台用内置 island、通用柜用 sideboard 表示。

房间边全部关闭使 NeonPlan 将部分相邻区域视作开放空间；复杂的按房间隔光与墙面内外材质分配仍应在正式接入时按实墙进一步调整。源图的墙高、门窗高度、家具高度、主卫局部形状等仍沿用小样假设，不能作为施工尺寸。

## 真实设备接入

完整备份有 23 件基础示意家具、4 件未绑定的控制点位灯具模型，以及设计参考中可原生表达的装饰（数量见校验报告），`entity` 均为 `null`，不含捏造的 HA entity ID，也没有令牌。导入实际 HA 后，需把房间关联到 HA Area，并绑定灯具、窗帘等实体。灯位来自 `data/devices.json` 的小样假设，不代表电气图实测位置。本次验证的是文件格式、坐标、几何与本地官方加载，不是你家 HA 的在线控制测试。

## 设计师 VR 外观映射

导出器读取与 `house.json` 同目录的 `design-style.json`，在官方导入完成后映射原生有效的地材、墙色和家具 finish。`neonplan-material-mapping.json` 逐项记录实际生效字段、装饰清单和近似项；`neonplan-material-capabilities.md` 给出对应上游源码能力证据。官方预览使用同一完整备份，刷新即同步。

当前参考的公共区是浅暖人字木地板、奶油墙、蓝色织物与木色/深色家具；原生以 oak 木地板近似人字纹。透明圆茶几近似为不透明圆桌，彩块地毯近似单色，落地灯保留模型及位置但不能携带红色壳体。柜门双色只对确实使用对应颜色角色的模型有效。木框玻璃半墙保留原始 CAD 墙线与高度，不在原生备份中新增猜测开口；其具体外观由独立预览表达。所有近似都不改变原始沙发朝向。

主卧原生 bed 的 fabric 对应床品，已按 `linenColor` 映射浅蓝，床架按木色；橙黄床头软包没有独立原生角色，未伪称复刻。厨房原生 wood 对应台面，已按浅色 `counterColor` 映射；木下柜与白上柜的分材质表达仍受内置模型限制。玄关 sideboard 没有独立 front 角色，橄榄绿柜门在原生中未生效。次卧全景加载不完整，目前只核实可见白色柜门；其床品继续明确作为示意，床位按用户要求靠东窗与北墙。

## 重建

在项目目录运行（Node 25+，Python 3.14；官方源码使用可由 Node 直接执行的 TypeScript）：

```powershell
python scripts/export_neonplan.py
python scripts/make_neonplan_preview.py
python -m unittest discover -s tests -p test_neonplan_export.py
```

使用现有本地 HTTP 服务打开预览，不能直接双击 HTML 通过 file:// 运行。所有户型处理与验证均在本机执行；原始 DWG/DXF 未纳入仓库，派生户型 JSON 与备份随本次代码交付。
