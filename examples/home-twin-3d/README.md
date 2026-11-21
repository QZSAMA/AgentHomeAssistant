# 武汉印 · CAD 户型与灯光交互小样

本项目将用户的《武汉印130最新版.dwg》重建为可操作的三维户型，并提供已通过官方解析器与 HA 后端 schema 验证的 NeonPlan 3D 原生备份。

仓库交付目录为 `examples/home-twin-3d`，可独立复制运行。原始 DWG、转换后的 DXF、大型 CAD 中间文件、运行日志及网页诊断抓取未纳入仓库；运行所需的派生户型 JSON、平面预览、核实过的设计参考截图、第三方组件及许可证均随代码提供。完成范围和复验结果见 [交付核验](docs/delivery-check.md)。

## V0.2：设计师效果参考

按用户提供的[建E全景](https://vr.justeasy.cn/view/179416y8s9w6pc82-1794271703.html)补充外观。它提供的是六面体全景渲染，不是可直接导入的三维模型；没有取得设计师的原始精模或材质工程。

- **沙发朝向、位置和尺寸保持原样**，遵循用户随后更正的“沙发好像没问题”。
- **次卧床贴北墙和东侧窗边**：中心 `[10.82,1.33] m`，床体 `1.5×2.0 m`；床头板也限制在床体平面范围内，避免贴墙后穿墙。
- 客厅加入蓝色织物沙发/单椅、橄榄绿靠垫、暖木人字拼纹理、奶油墙、透明圆茶几、浅底彩块地毯、红色折臂落地灯、深色电视地台。
- 电竞房加入木桌/蓝下柜、双屏示意与白粉色三角灯板。玻璃隔断沿原 `studio-north` 墙线显示为半墙＋木框玻璃；线的位置和原始墙数据不变，高度仍为假设。
- 主卧按可见画面加入暖木床头、橙黄软包、浅蓝床品；厨房加入暖木下柜和白色上柜/浅台面；玄关矮柜为橄榄绿。
- 次卧全景未完整加载，白色柜门可见；床品仍为示意，未声称复原未看清细节。卫生间当前仅做浅色砖材近似。
- 新增 **“设计师配色”** 对比开关和 **“次卧”** 视角。关闭剖切可查看玻璃隔断、上柜和高位三角灯板；它们在剖切时隐藏以便看清平面。

材质配置与每项证据在 `data/design-style.json`，参考页截图和核查记录在 `references/designer/`。电脑屏幕、地板织物和地毯图案为本地程序绘制；不是从全景抠取带烘焙阴影的贴图。灯光仍为四个原有模拟设备，新增摆件不是已接入的真实设备。

独立预览对外观表达更完整。NeonPlan 原生备份已同步其支持的颜色/材质与三件装饰，保留全部10处门窗；原生不直接支持此人字铺法、透明桌面、彩块毯图案、半墙木框玻璃及部分柜门分色，采用近似或保留基础形态。逐项见 `exports/neonplan-material-mapping.json`，不能将原生预览称为同等精度复刻。

## 打开

双击 `start.cmd`，然后访问 **http://127.0.0.1:8776/**。也可运行：

```powershell
python serve.py --port 8776
```

端口被占用时改用 `--port 8777` 并访问对应地址。服务只监听本机，只提供本目录文件；无需 npm 安装，不依赖 CDN。页面需支持 WebGL。不要直接通过 file:// 打开 HTML。

- **独立交互预览**：`/`。中文控制界面，旋转、俯视、客餐厅/电竞房视角、四盏灯的开关与亮度、回家/观影/离家场景、日间/夜景、剖切和 CAD 线稿。
- **NeonPlan 官方运行时**：`/vendor/neonplan/preview/wuhan.html?lang=zh&style=cozy&nopro`。使用固定版本 v4.0.0 的官方组件和本地模拟 HA，装载同一份户型。与独立预览的模拟状态互不共享。
- **正式导入文件**：`exports/wuhan-neonplan-backup.json`，用于 NeonPlan 的 Editor → Backup → Import。不要把简化输入 `wuhan-neonplan-import.json` 当最终备份；区别见 `exports/README.md`。

## 当前完成范围

当前 CAD 作为候选布局基准，重建 9 个空间区域、32 段墙体、10 处门窗开口，并放置 23 件基础简化家具。四个交互样例为客厅主灯、餐厅吊灯、电竞房主灯和桌面灯。V0.2另加设计参考装饰，官方备份中包含23家具＋4灯＋3件支持的装饰，共30个家具/灯具对象。

独立预览中，直接点灯标记或三维灯具即切换开关；右侧名字按钮用于选择灯，亮度滑块用于调光。拖动旋转不会误触开关。聚焦画布后，方向键旋转，加减键缩放。触屏单指旋转、双指缩放。

剖切状态将墙体显示为低墙，并缩短高柜方便查看内部；关掉剖切恢复完整示意高度。此效果不修改 CAD 数据，也不表示拆墙或缩短柜体。

## 尺寸和来源

- 数据来源是本地 DWG 转出的 DXF。原始 DWG/DXF 留在本地；仓库包含运行所需的派生户型 JSON 与平面预览。
- 米制坐标：x 向图右、z 向图下、y 向上；家具旋转为弧度。图纸方向不自动等于南北。
- 图中 **11.33 m 是内部横向尺寸链**；模型外轮廓最大包围尺寸为 **11.83 × 10.17 m**。它们不是同一尺寸基准，不能相互替代，也不据此外推建筑面积。
- 电竞房内宽由 CAD 核对为 3.21 m。当前内部按这份 CAD 的吧台/柜体布置显示，未将旧 `studio-room-3d` 连体桌方案当成本次 CAD 事实。
- 墙高暂按 2.65 m；门窗高度、窗台高度、家具高度/材质以及灯位均为示意，需现场或设计图确认。
- 房间多边形是地面和交互分区，开放的客餐厅不能因此自动生成隔墙。实际墙段经过 CAD 线条与开口交叉核对。
- 旧文本编码和字体存在转换限制；房间语义、主卫局部与部分家具做了简化。本产物用于布局与交互核对，不是施工图。

详见 `data/geometry-notes.md` 与 CAD 叠图 `data/geometry-audit.png`。几何提取脚本保留来源实体和假设记录。

## 设备状态与后续接入

这是**模拟体验**，没有连接真实 Home Assistant、没有令牌，不会开关家里的设备。独立预览只把亮度、选择和场景存入浏览器 `wuhan-twin-demo-v1`；损坏或不可信存储会被校验。可用“重置体验”恢复。

下载的设备映射全部 `entityId:null`。NeonPlan 原生备份也不含虚构的已绑定实体。官方本地预览仅在运行时使用 `light.demo_wuhan_*` 模拟状态，它们不是用户家中的设备。

HA 部署好后，可将原生备份导入 NeonPlan，再逐个绑定真实实体，验证开关/调光/状态回报。独立预览当前并不是 HA 集成；直接填写下载映射不会自动让它连接设备。真实接入与离线/失败反馈需在后续适配时完成。

## 文件

| 文件 | 用途 |
|---|---|
| `data/house.json` | 米制几何、语义分区、尺寸校核与来源 |
| `data/devices.json` | 四个模拟灯位，实际实体为空 |
| `scripts/extract_cad.py` | 从原 DXF 可复现生成几何 |
| `state.mjs` | 纯模拟控制、持久化和映射导出 |
| `scene.mjs` | Three.js 模型、相机、光照与拾取 |
| `app.mjs` | 中文界面和交互绑定 |
| `scripts/export_neonplan.py` | 官方导入链与原生模型适配 |
| `exports/neonplan-validation.json` | 官方解析/几何/后端校验结果 |
| `previews/` | 桌面、夜景、俯视、手机截图与浏览器验收报告 |

## 验证

以下命令在本目录运行。仅打开页面需要 Python 3 和支持 WebGL 的浏览器；完整测试/重新导出已在 Python 3.14、Node 25.8.2 上验证。浏览器测试需先安装 `playwright` 及其 Chromium（`python -m pip install playwright`、`python -m playwright install chromium`）。

日常运行、现有几何检查和 NeonPlan 重新导出使用随仓库提供的数据，不需要原始 CAD。只有重新提取几何时需要另行安装 `ezdxf`，并用 `python scripts/extract_cad.py --source "本机同版图纸的路径/floorplan.dxf"` 指定本地 DXF；脚本默认路径是最初工作区位置，换目录后不能直接沿用。

```powershell
node --test tests/state.test.mjs
node --test tests/design-appearance.test.mjs
python scripts/test_geometry.py
python -m unittest discover -s tests -p test_neonplan_export.py
# 以下命令需要本地预览服务运行，且安装了 Playwright/Chromium
python tests/browser.py --base-url http://127.0.0.1:8776
python tests/canvas_pick.py
```

V0.2 单元验证：14 项状态、6 项外观/床边界、6 项几何、6 项 NeonPlan 导出测试通过，原生后端 schema 通过。浏览器验收报告见 `previews/browser-report.json`，覆盖开关、调光、场景、视角、夜景、剖切、CAD 叠图、拖动防误触、键盘、保存恢复、映射下载、设计风格对比、参考弹窗和窄屏操作。另有不经过 DOM 按钮的真实画布射线拾取检查。

## 第三方组件

独立页面使用本地 Three.js 0.180.0 和 OrbitControls，MIT 许可证位于 `vendor/THREE-LICENSE.txt`。NeonPlan 固定为 v4.0.0，commit `8a0fecd90c4eb565c8af8e2fcac01346125f069f`；保留其许可证及来源说明。独立预览不是 NeonPlan 官方产品；原生预览使用官方 bundle 和本地演示适配器。

两款字体的 OFL 声明和 Lit 的 BSD 声明见 [第三方许可来源](vendor/licenses/SOURCES.md)；本地校验依赖 voluptuous 的 BSD 声明位于 `vendor/python-deps/voluptuous-0.15.2.dist-info/COPYING`。`vendor/neonplan/frontend/src` 是导出器所需源码及能力核查证据的子集，不是完整上游构建工程；要重建 NeonPlan 本身应取得上述固定版本的完整上游仓库。
