# NeonPlan 4.0 材质映射能力与边界

依据固定的上游 v4.0.0（commit `8a0fecd90c4eb565c8af8e2fcac01346125f069f`）实际 schema 与渲染源码。颜色与材质选择来自主线程核对设计师 VR 后保存的 `data/design-style.json`，不把内置默认值当成设计要求；实际导出结果见 `neonplan-material-mapping.json`。

| 设计内容 | 可用原生字段 | 已核实行为与边界 |
|---|---|---|
| 木地板、瓷砖、灰地面 | `Room.floor_material` | 渲染器识别 `wood`、`oak`、`tiles`、`carpet`、`stone`、`concrete`；不是 `tile`。不识别的字符串回退木地板。 |
| 浅灰大规格地砖 | `floor_material: concrete` 或 `tiles`，按最终参考选择近似 | 天然风格固定颜色：tiles `#dedbd5`，concrete `#babcbe`；tiles 内置 0.25m 网格、stone 0.5m 错缝、concrete 1m 网格。没有逐房自定义地色、砖尺寸或纹理 URL 字段，不能声称精确复刻。 |
| 米白/浅灰实体墙 | `FreeWall.color: '#rrggbb'` | 两侧同色；本项目使用显式 free wall，因此应设置此字段。另有 `Room.wall_color` / `wall_colors`，但它们不应导致重新生成区域边界墙。 |
| 外立面 | `Building.settings.facade_color` | 作用于天然风格外墙；不能替代所有 free wall 的独立色。 |
| 沙发布色与木脚 | `Furniture.finish.fabric` / `.wood` | 内置 sofa、sofa_l 等明确使用这两个颜色角色。保留 `x/z/w/d/h/rotation` 可只换材质、不改朝向和位置。 |
| 床品/床架 | `finish.fabric / wood / front` | 内置 bed 提供以上角色；是简化颜色表达，非照片级织物纹理。 |
| 桌面/木柜/岛台台面 | `finish.wood` | table、coffee_table、sideboard、kitchen、island 的有效颜色角色不同；kitchen / island 的 wood 对应台面，柜体仍为模型默认色。 |
| 柜门和柜体分别着色 | `finish.front / body` | 字段在 schema 中有效，但仅对实际使用 `front` / `white` 角色的模型生效。`body` 实际映射到 `white` 角色，不是渲染源码所有 `C.body`。内置 wardrobe 的柜体使用固定 `C.body`，没有可覆写 finish 角色；内置 sideboard 主要是 wood，不能凭增加 front/body 字段就声称门板双色已生效。 |

所有 `finish`、墙色和内置天然地材在 **cozy / evening / winter 等 natural 风格**下生效。neon / blueprint 等风格会使用自己的配色，适合控制状态可视化，不适合核对装修颜色。

当前独立预览可承担准确的大砖铺贴尺寸、分材质柜门与细部纹理；官方预览与原生备份应保留可表达的颜色/材质类别，并在导出说明中列出近似项。除非后续明确扩展官方 renderer 或增加可携带的自定义模型，不应修改 vendor 原始 bundle 来隐藏能力边界。

核查源码：

- `vendor/neonplan/frontend/src/model.ts`：Room、Furniture.finish、FreeWall.color、BuildingSettings。
- `vendor/neonplan/frontend/src/finishes.ts`：`BUILTIN`、`finishRolesOf`、`finishTargets`。
- `vendor/neonplan/frontend/src/viewer/build.ts`：`FLOOR_LOOK`、`wallColors`、显式墙颜色。
- `vendor/neonplan/frontend/src/viewer/viewer3d.ts`：`patternAtlas` 的地板网格尺寸。
- `vendor/neonplan/frontend/src/viewer/furniture.ts`：`finishColors` 和各具体家具几何的颜色角色。
- `vendor/neonplan/custom_components/neonplan3d/schema.py`：原生数据校验。

后续导出必须继续通过官方 Building schema、墙开口检查与房间/尺度测试，并校验沙发朝向未变。次卧位置修正由源几何负责，本导出不二次推断。

## 本次 VR 参考确认后的映射方向

主线程实际查看设计师 VR 后确认客餐厅为浅暖人字拼木地板，而非浅灰砖。以下记录映射方式，具体选择取 `data/design-style.json`：

- 木地板使用原生 `oak`（内置天然色 `#c9a47c`），近似参考木色；不能携带人字拼图案。
- 奶油墙可写显式墙颜色；蓝色沙发可写 `finish.fabric`，不改既有朝向。
- 透明圆茶几可近似为原生圆桌轮廓，但原生圆桌台面使用不透明 wood 角色，不能当作透明玻璃复刻。
- 白底彩块地毯可近似单色地毯；多色拼块由独立预览表达。
- 红落地灯的红色壳体不应通过改变灯光颜色伪装；原生可保留灯具类型，但壳体色映射有限。
- 黑色电视地台可通过有 wood 角色的 sideboard / 柜体改变整体颜色；原生分柜门材质能力仍受模型限制。
- 木框玻璃隔断属于装修构件，不能为其重新生成语义分区隔墙；需由明确的参考位置和结构约束决定是否另做装饰模型。
