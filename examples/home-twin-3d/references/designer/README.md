# 设计师 VR 参考记录

仓库仅收录已核实的参考截图与本说明，用于现有弹窗和外观证据。下文列出的网页源码、网络诊断、XML、重复截图及未成功加载的场景记录保留在原本地工作目录，不随代码交付；它们不是运行依赖。`data/design-style.json` 中的截图文件名是证据标记，不会自动请求缺失的诊断文件。

来源页面：[https://vr.justeasy.cn/view/179416y8s9w6pc82-1794271703.html](https://vr.justeasy.cn/view/179416y8s9w6pc82-1794271703.html)

检查日期：2026-11-21（Asia/Shanghai）。页面标题为“方林集团毛锐”。页面由建E的 krpano 播放器渲染；它是六面体全景图漫游，不是可导入本地 Three.js 的可编辑建筑网格。公开数据给出场景名称、sceneId、预览图和 `pano/..._six_..._kjl.tiles/` 路径。没有发现公开的 GLB、GLTF、OBJ 或 FBX 下载入口。页面公开 XML URL 已记录，但返回内容是加密 CDATA，本次不做解密或绕过访问控制。

## 场景

完整清单见 [`scenes.json`](./scenes.json)，共 10 个场景：客厅 2 个角度、厨房、入户、电竞房、主卧 2 个角度、次卧、卫生间、主卧卫生间。播放器可用公开的 `krpanoSWFObject` 调用 `loadscene(scene_<sceneId>, null, MERGE, BLEND(...))` 切换。

## 可核实的视觉参考

| 场景 | 文件 | 画面中实际可见的内容 |
| --- | --- | --- |
| 客厅 | `runtime-current.png` | 奶油白墙顶、浅暖人字木地板、木框玻璃隔断、蓝色织物长沙发和单椅、绿色抱枕、白底彩色块地毯、透明圆茶几、红色落地灯、黑色低电视柜、黑色线性嵌灯和暖色灯槽 |
| 电竞房 | `studio-01.png` | 暖木双人长桌、深蓝色下柜、黄色及墨绿色台灯、白粉三角 RGB 墙灯、木搁板、双显示器和木色墙面 |
| 电竞房朝客厅 | `studio-02.png` | 木框大玻璃与半墙，能看到客厅电视墙、沙发背面和暖木地面 |
| 主卧 | `master-bedroom-01.png` | 暖木床头护墙、橙黄色织物软靠背、浅蓝床品、米色织物帘、奶油墙、白柜门与木边框 |
| 厨房 | `kitchen-01.png` | 暖木下柜、白色上柜、白色细纹台面、浅米白大块墙砖、黑色灶具、暖色柜底灯 |
| 入户 | `entry-01.png` | 奶油墙、深橄榄绿矮柜、蓝色吊顶/包裹块、暖木桌面、暖色吊灯和花束 |

这些是给本地模型使用的外观参考，不改变 DWG 的墙体、门洞和用户已确认的家具方向。沙发方向继续按用户最新要求保持；次卧床位另按用户决定处理。图片是浏览器页面截图，仅作为设计参考，没有把远程全景媒体复制进本地工程。

## 原始检查记录

- `page-source.html`：页面 HTML（含公开 Next 数据）。
- `public-page-data.txt`：从公开页面脚本提取的场景数据文本。
- `tour-public.xml`：公开 XML URL 的响应；内容为加密 CDATA，未解密。
- `initial-dom.json`、`initial-network.json`、`runtime-diagnostic.json`：DOM、网络和播放器公开 API 诊断。
- `scene-load-check.json`：10 个 sceneId 的切换和进度检查。

不把页面里的摄影全景当作 3D 模型，也不以其中的透视关系反推 CAD 尺寸。

## 未完整加载的画面

`second-bedroom-01.png` / `second-bedroom-02.png` 在切换卡住时仍为前一个场景画面，不应当作次卧设计依据。后续已确认 `xml.scene=scene_447151233`，但进度长期为 5/6；`second-bedroom-verified.png` 只显示暖白柜门。次卧床位依据用户明确要求修正，床品与地板目前保留示意，不根据场景缩略图或未加载画面声称精确还原。

`master-bedroom-02.png` / `kitchen-02.png` / `entry-02.png` 主要为局部空墙视角，不用于进一步判断家具形式。实际采用的证据是上表可核实截图。
