# 家庭基础设施登记与实施台账

> **用途**：记录户型、设备计划、网络架构、Apple Home/Home Assistant 关系和本地模型部署计划。
> **登记日期**：2026-10-12
> **维护规则**：本文件是当前事实源。`已确认`只表示用户明确提出或已有证据；`候选`表示尚未购买的选项；`待验证`表示需要现场、官方资料或 PoC 验证；`已部署`必须有实际设备或验收记录支持。

## 1. 当前决策摘要

| 主题 | 当前记录 | 状态 |
|------|----------|------|
| 户型 | 一层长方形住宅，布局见第 2 节 | 已确认，尺寸待补 |
| 家庭中枢 | 计划使用未来 Apple Home Hub，具体型号和上市信息待官方确认 | 用户意向 |
| 房间音频 | 主要房间放 HomePod mini；大厅不再预置 HomePod | 计划 |
| 智能家居品牌 | 绿米（Aqara）为主；欧瑞博只保留空调候选 | 已确认方向 |
| 家庭服务节点 | Mac Studio M5 Ultra；用户所说“512GB”含义待确认；承担模型、视频剪辑、软件开发和家庭服务 | 计划购买 |
| 网络 | 光猫桥接 → AC 主路由/网关 → 中央管理型多千兆 PoE 交换机 → 4 个墙面/入墙有线 AP（吸顶仅在满足额外 2.5G 口时考虑）；房间内按需接小交换机 | 设计可行，待选型 |
| 自动化平台 | Home Assistant 与 Apple Home 并行；HA 通过 HomeKit Bridge/Matter 等方式接入 Apple Home | 集成方案待 PoC |
| 本地模型 | Flash planner 常驻，其余模型按需或队列运行 | 设计基线，待实机验证 |

## 2. 户型与点位假设

用户给出的相对布局如下。当前没有房屋长宽、墙体材质、门窗和家具尺寸，因此图示不用于施工放线。

```text
北 / 上
┌──────────────────────────┬──────────────────────────┐
│ 主卧（左上）              │ 次卧（右上）              │
│                          │                          │
├──────────────────────────┼──────────────────────────┤
│ 卫生间 A（中部）          │ 公共区域/大厅（具体边界待补）│
│ 门朝主卧                 │                          │
├──────────────────────────┼──────────────────────────┤
│ 工作室 + 电竞房（左下）    │ 公共卫生间（右侧，门朝上）  │
│                          │ 入户门位于右下角附近       │
└──────────────────────────┴──────────────────────────┘
南 / 下
```

建议预埋四个 AP 网线点，但不在未测量前承诺四台都长期启用。初始命名如下：

| 点位 | 建议位置 | 计划用途 | 状态 |
|------|----------|----------|------|
| `AP-MASTER` | 主卧高位或墙面中上部 | 主卧 Wi‑Fi 7 覆盖；AP 第二个 2.5G 口接电脑 | 预埋点计划 |
| `AP-SECOND` | 次卧高位或墙面中上部 | 次卧 Wi‑Fi 7 覆盖；AP 第二个 2.5G 口接电脑 | 预埋点计划 |
| `AP-STUDIO` | 工作室/电竞房高位或墙面中上部 | 高带宽工作设备、低延迟漫游；需要多设备时再接房间小交换机 | 预埋点计划 |
| `AP-HALL` | 大厅靠中心位置 | 公共区域、入户附近、HomePod/Apple Home 覆盖；大厅 Hub 位置待确认 | 预埋点计划 |

卫生间通常不单独放 AP。6GHz 穿墙衰减明显，最终启用 3 台还是 4 台应以现场热力图、漫游和 HomePod/Matter 稳定性测试决定。大厅的准确位置、房屋尺寸、承重墙/玻璃/金属隔断和 AP 吸顶或墙装方式仍需补充。

### 2.1 房间侧网络形态（已确认偏好）

每个房间不默认建设独立的“设备箱 + 交换机”。推荐采用集中式设备柜：中央 PoE 交换机分别回接四个房间的 Cat6A 墙面 AP。每台 AP 的验收条件是 **Wi‑Fi 7、≥2.5GbE 有线回程、PoE+（或明确兼容的供电方式），并且至少有一个额外的 ≥2.5GbE 客户端口**；电脑直接插 AP 的额外端口。

当工作室/电竞房、电视墙等位置需要多台有线设备时，可将 AP 的额外 2.5G 口接到桌边的风扇less 2.5G 小交换机，再连接电脑、游戏主机、NAS 等。小交换机应放在可维护、可散热的位置并配普通电源，不建议封在墙内；施工时可在工作室预留第二条 Cat6A 到桌面，作为绕过 AP 的扩展或故障旁路。只有在确有设备密度、距离或美观要求时，才另设可通风的弱电箱。

## 3. 设备登记

### 3.1 已确认的购买方向

| 类别 | 设备 | 数量/位置 | 角色 | 状态 |
|------|------|-----------|------|------|
| 房间音频与家庭中枢辅助 | HomePod mini | 各主要房间至少 1 台；当前按主卧、次卧、工作室/电竞房预留 | Siri/音频/Thread 与家庭中枢冗余 | 计划购买，数量待确认 |
| 家庭中枢 | Apple Home Hub（用户所说的后续 Apple 产品） | 大厅或公共区域 | Apple Home 的主家庭中枢候选 | 型号、上市时间、连接方式待官方确认 |
| 计算与服务 | Mac Studio M5 Ultra；“512GB”统一内存/存储含义待确认 | 1 台，建议放在通风设备柜或工作室设备位 | 本地模型、视频剪辑、软件开发服务器、HA 相关服务 | 计划购买 |
| 智能家居主品牌 | Aqara/绿米 | 待按房间和装修点位选型 | 开关、传感器、窗帘、网关等 | 计划，型号待确认 |
| 空调候选 | ORVIBO/欧瑞博空调 | 待确定 | 仅考虑空调接入 | 兼容性待验证 |

大厅不再记录为固定采购 HomePod。Apple Home Hub 仍按“计划项”记录，不能把未发布或未确认的型号写成已购买设备；在确认前应为大厅保留可靠 Wi‑Fi、电源和可维护的位置。

### 3.2 当前不能作为事实的旧记录

仓库旧版 README、Code Wiki 和设备清单曾把绿米、欧瑞博、Mac Studio、NAS 等混合写成“已接入”或“待购”。当前没有采购凭证、安装记录或 HA 实例验收记录，因此本台账将它们统一视为“未核验”，以本文件和后续现场记录为准。

## 4. 网络架构

### 4.1 推荐物理拓扑

```text
入户光纤
   │
   ▼
ISP 光猫（优先桥接）
   │  PPPoE / ISP VLAN / IPv6 参数由运营商确认
   ▼
AC：主路由器/网关
   │  NAT、防火墙、DHCP、VLAN、IPv6、远程访问策略
   ▼
管理型 2.5G/10G PoE+ 交换机（弱电柜或通风设备柜）
   ├── Cat6A → AP-MASTER（额外 2.5G 口 → 主卧电脑）
   ├── Cat6A → AP-SECOND（额外 2.5G 口 → 次卧电脑）
   ├── Cat6A → AP-STUDIO（额外 2.5G 口 → 电脑或房间小交换机）
   ├── Cat6A → AP-HALL（额外 2.5G 口 → 大厅有线设备，按需）
   ├── Mac Studio / HA 主机（建议有线）
   └── 控制器（Omada OC200 或 UniFi 网关内置控制器）
```

这里的 AC 已按用户说明解释为主路由器/网关。无线控制器若单独存在，只负责 AP、SSID、漫游和 VLAN 的管理，应作为 LAN 终端接入交换机，不能串在光猫和交换机之间。光猫无法桥接时，需要记录双 NAT 或 DMZ 方案，并重新验证 IPv6、入站访问、Home Assistant 远程访问和端口转发。

### 4.2 设计约束与布线要求

- 四个 AP 全部使用有线回程，关闭对无线 Mesh 的依赖；预埋点采用星型回线。
- 每个 AP 点至少 1 条 Cat6A 实芯铜线，推荐 2 条并预留穿线管和维修余量；不使用 CCA 线。墙面 AP 位置应预留标准底盒/面板空间和附近电源（若型号不采用 PoE）。
- AP 采购验收必须逐项核对：Wi‑Fi 7、≥2.5GbE 上联、PoE+ 或明确供电标准，以及额外客户端口也为 ≥2.5GbE；只有一个 2.5G 上联口的吸顶 AP（如 EAP772/U7 Pro Max 类）不满足本项目最终硬条件。
- 默认不在每个房间做密闭设备箱。多设备房间可在桌边增设风扇less 2.5G 小交换机；如确需隐蔽安装，应使用可通风、可断电维护的箱体并单独核算散热和电源。
- 交换机至少需要 8 个 2.5G PoE+ 口，较稳妥的容量是 16 口，并提供 10G 上联或端口给 Mac Studio/NAS 使用。
- PoE 预算按“**四台最终 AP 铭牌最大功耗之和 × 1.3 + 其他 PoE 设备最大功耗**”核算；EAP725‑Wall 或替代型号的实际功耗、PoE+ / PoE++ 要求和北美硬件版本必须在下单前从官方数据表核对。
- 现有布线文档中的 `400×300×100mm` 弱电箱尺寸不足以直接容纳大型 1U 多千兆 PoE 交换机、光猫、网关、电源和弯曲半径。应改为可通风的通信柜/壁挂机柜，或把交换机移到通风设备柜，弱电箱只放光猫和上联设备。
- 弱电设备接入 UPS，设备柜要有独立电源、散热和可维护空间。Mac Studio 不建议放进密闭弱电箱。
- HomePod mini 主要依赖 Wi‑Fi、家庭中枢和 mDNS/组播稳定性，AP 的 2.5G/10G 速率不会直接变成 HomePod 的有线速率；未来 Apple Home Hub 的连接方式仍待官方确认，不能据此提前假定无线或有线接口。

### 4.3 候选产品组合

以下都是候选，不代表已购买。应选定一个生态，避免 Omada 和 UniFi 的控制器、漫游、VLAN 与诊断界面分裂。

| 生态 | 主路由/网关 | PoE 交换机 | AP | 控制器/备注 |
|------|-------------|------------|----|-------------|
| TP‑Link Omada（紧凑、性价比优先） | ER707‑M2：适合不超过 2.5G 宽带；若明确需要 10G WAN，升级到 10G 网关 | SG2210XMP‑M2：8×2.5G PoE+、2×10G SFP+、160W，尺寸和风扇less 形态更适合有限空间；采购前核对北美版本 | **EAP725‑Wall：Wi‑Fi 7，2×2.5G 口（1×PoE 输入）+ 3×千兆口；第二个 2.5G 口可接电脑**；最终以北美硬件版本数据表为准 | OC200 或软件控制器；控制器接 LAN |
| UniFi（统一管理和界面优先） | Cloud Gateway Max：2.5G；Cloud Gateway Fiber：10G 网关和控制器 | USW Pro Max 16 PoE | U7 Pro Max/U7 Pro Wall 虽有 2.5G 上联，但当前公开规格未提供额外 ≥2.5G 客户端口；不满足本项目硬条件，需另加房间 2.5G 小交换机或等待符合规格的墙面型号 | 网关可内置控制器；交换机仍需给 AP 提供 PoE |

当前推荐先按 Omada 墙面 AP 方案做预算：`光猫桥接 → ER707‑M2 → SG2210XMP‑M2 → 4×EAP725‑Wall`。如果运营商明确提供 10G、Mac Studio/NAS 需要大文件高速互拷，改用 10G 网关、10G 上联和相应 10G AP；若 EAP725‑Wall 在购买时无北美库存，则保留墙面点位并选择经规格验收合格的同类多千兆墙面 AP，不得退回单口吸顶 AP。

### 4.4 逻辑网络与 Apple Home/HA

第一阶段把 HomePod、Apple Home/Matter、Aqara 网关、Home Assistant 和主要智能设备放在同一个可信网络，先完成配网和端到端控制。第二阶段再考虑管理、主网、IoT、访客 VLAN；一旦分 VLAN，必须配置并验收双向 mDNS/Bonjour、IGMP snooping、控制器到 HA/设备的 ACL 和 HomePod/Matter 配网流程。智能家居 2.4GHz 设备需保留兼容 SSID，不能只启用 6GHz 或 WPA3-only。

Home Assistant 是设备编排和自动化核心，Apple Home 是家庭交互与生态入口。优先使用 HA 的 HomeKit Bridge 把已验证设备暴露到 Apple Home，并根据 Aqara/空调型号选择 Matter、HomeKit、Zigbee 或厂商集成；不能仅凭品牌名称保证兼容。

## 5. Mac Studio 与模型部署计划

### 5.1 硬件约束

用户只说“512GB 版本”，尚未确认 512GB 指统一内存还是存储；本台账暂按“可能指 512GB 统一内存”记录，不视为已确认 SKU。项目保存的 Apple 技术规格证据显示 M5 Ultra 基础 SSD 为 1TB，可配置 2/4/8/16TB；因此不要再写成“存储从 2TB 起”，实际购买须以具体地区 SKU、上市状态和报价为准。模型权重按当前页面容量粗算约 397GB，还不包括运行时、缓存、KV cache、视频中间文件和备份，项目建议 SSD 至少 2TB、长期 4TB 或外接 Thunderbolt 5 NVMe。

Mac Studio 建议有线接入交换机，原生运行 MLX/MLX‑VLM/llama.cpp 等 Apple Silicon 服务；Home Assistant 可在同机容器或独立主机运行，但不能假设 Linux 容器直接获得 Metal/MLX GPU。所有服务先限制为局域网受控 API，工具调用采用白名单并记录审计日志。

### 5.2 模型登记

| 模型 | 任务 | 格式/运行时 | 页面容量或内存参考 | Apple 路径 | HA 角色 | 状态与风险 |
|------|------|-------------|--------------------|------------|---------|-------------|
| [Qwen3.8‑Flash‑Next‑4bit](https://huggingface.co/rapid-mlx/Qwen3.8-Flash-Next-4bit) | 文本规划、工具调用 | MLX/Safetensors，Rapid‑MLX | 下载约 105GB；active 约 103–105GB；页面建议 128GB 准入、192GB 推荐 | Rapid‑MLX，页面有 Apple 基准但不是 M5 实测 | 首选 planner，先单并发 | experimental、text-only；参考性能来自 M3 Ultra，不作为 SLA；Qwen Community License 需复核服务条款 |
| [Qwen3‑Omni‑30B‑A3B‑Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct) | 音频/图像/视频/文本 | Transformers/Safetensors，BF16 | 页面按视频时长给出约 78.85–144.81GB 理论显存区间 | 官方示例偏 CUDA/vLLM/FlashAttention2，Apple/MPS 未验证 | 实验 profile，暂不作为 HA 常驻语音链路 | Apple 兼容性和音频输出需 PoC；不能把激活参数量当作完整运行内存 |
| [Qwen3.8‑27B‑bf16](https://huggingface.co/mlx-community/Qwen3.8-27B-bf16) | 图像理解、视觉问答 | MLX‑VLM/Safetensors，BF16 | 约 54.7GB | MLX‑VLM | 视觉按需任务 | Apple 路径清晰，M5 性能和并发待测；页面容量不是 4/8-bit 量化 |
| [DeepSeek‑V4‑Flash‑0731‑GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF) | 编程、复杂异步任务 | GGUF，llama.cpp/Metal | 完整模型 Q4 约 155GB、Q8 约 162GB；页面中的 10.9/11.3GB DSPARK 文件不是完整模型 | macOS/llama.cpp 路径明确 | 独占编码队列 | 不适合低延迟 HA 常驻；需要支持该模型的新版 llama.cpp 和本机实测 |
| [LTX‑2.5‑MLX](https://huggingface.co/PocketAiHub/LTX-2.5-MLX) | 文生视频/音视频 | MLX/Safetensors，第三方转换 | BF16 主快照约 71GB；页面有 Q8/Q4 运行参考 | Apple Silicon MLX；需固定仓库 revision | 独占创作队列 | gated access、第三方转换和许可需确认；不要与大模型同时常驻 |
| [SDXL‑Turbo‑GGUF](https://huggingface.co/OlegSkutte/sdxl-turbo-GGUF) | 文生图 | GGUF，stable-diffusion.cpp/Metal | Q8 页面约 4.1GB | 预计可走 Metal，需本机验证 | 图片按需任务 | 体积小；`sai-nc-community` 许可需在对外服务前复核 |
| [Unlimited‑OCR‑bf16](https://huggingface.co/mlx-community/Unlimited-OCR-bf16) | OCR、扫描件识别 | MLX‑VLM/Safetensors | BF16 约 6.67GB；4bit 约 2.29GB | MLX‑VLM ≥ 0.6.8 | OCR 按需或轻量常驻 | Apple 路径清晰；建议先用 4/8bit 版本做家居文档索引 |
| [Qwen3‑Embedding‑0.6B‑8bit](https://huggingface.co/mlx-community/Qwen3-Embedding-0.6B-8bit) | 向量检索、设备/场景知识库 | MLX embedding | 约 633MB | `mlx-embeddings` | RAG/检索常驻 | 只能生成向量，不能生成回答；Apache‑2.0 |

部署编排基线是：`Flash planner + Embedding` 常驻；OCR 轻量常驻或按需；Qwen 27B 和 SDXL 按需；DeepSeek 与 LTX 独占队列；Omni 先做实验。所有模型初始 `max_concurrency=1`、上下文从 32K 起，并记录 load/unload、healthcheck、温度、统一内存峰值和实际 tok/s。

### 5.3 语音和 Apple Home 链路

HomePod/Siri 的 Apple Home 请求不会自动把本地模型当作 Siri 后端。第一版建议使用 Home Assistant Assist + 本地 STT/TTS + Flash planner，再通过受控 HA 服务调用设备并将结果播报到 HomePod/AirPlay。Omni 的音频能力列为后续 PoC，不能作为当前家庭控制链路的前置依赖。

## 6. 采购、部署与验收清单

| 优先级 | 事项 | 验收证据 | 状态 |
|--------|------|----------|------|
| P0 | 确认运营商带宽、光猫桥接、PPPoE/VLAN/IPv6/CGNAT | ISP 参数截图或工单记录 | 待确认 |
| P0 | 确认 Mac Studio 512GB 是统一内存，SSD 选 2TB 起/4TB 优先 | 具体 SKU 和报价 | 待确认 |
| P0 | 确认大厅 Home Hub 的官方型号、上市和连接方式 | Apple 官方页面/购买凭证 | 待确认 |
| P0 | 选定 Omada 或 UniFi 生态，并验收墙面 AP 的端口硬条件 | 网关、交换机、AP、控制器完整 BOM；AP 上联和额外电脑口均 ≥2.5GbE、PoE 预算达标 | 待确认 |
| P0 | 复核通信柜尺寸、散热、UPS 与 PoE 预算 | 柜体图、温度记录、供电清单 | 待确认 |
| P0 | 预埋四个 AP 点和至少一条 Cat6A 备用线 | 线缆测试报告、点位照片 | 待施工 |
| P1 | 获取户型长宽、墙体材质和门窗家具图 | 标注平面图 | 待补充 |
| P1 | 绿米设备逐型号确认 HomeKit/Matter/HA 接入 | 型号、固件、集成测试记录 | 待采购 |
| P1 | 欧瑞博只验证空调型号，不采购面板/照明作为默认方案 | HA/Apple Home PoC 结果 | 待选型 |
| P1 | HA HomeKit Bridge、Matter、mDNS 和 HomePod 配网验收 | 端到端测试记录 | 待部署 |
| P1 | Mac Studio 模型 PoC | 每模型运行日志、峰值内存、许可证记录 | 待购买 |
| P2 | 建立备份、更新、重启和服务审计策略 | 运维记录和恢复演练 | 待设计 |

## 7. 参考资料与证据边界

- [Apple Mac Studio](https://www.apple.com/mac-studio/) 和 [技术规格](https://www.apple.com/mac-studio/specs/)：M5 Ultra 统一内存、10GbE、Thunderbolt 5 和存储规格；购买前以具体 SKU 页面为准。
- [TP‑Link EAP725‑Wall](https://www.omadanetworks.com/us/business-networking/omada-wifi-wall-plate/eap725-wall/)、[EAP772](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap772/)、[EAP773](https://www.omadanetworks.com/us/business-networking/omada-wifi-ceiling-mount/eap773/)、[SG2210XMP‑M2](https://www.omadanetworks.com/us/business-networking/omada-switch-access-pro/sg2210xmp-m2/)、[ER707‑M2](https://www.omadanetworks.com/us/business-networking/omada-router-wired-router/er707-m2/)：候选网络设备的官方规格，硬件版本、供电要求和地区库存仍需核对；EAP772/EAP773 仅作为规格对照，不能替代本项目“额外 ≥2.5GbE 电脑口”硬条件。
- [UniFi U7 Pro Max](https://store.ui.com/us/en/products/u7-pro-max)、[U7 Pro XG](https://store.ui.com/us/en/products/u7-pro-xg)、[USW Pro Max 16 PoE](https://store.ui.com/us/en/products/usw-pro-max-16-poe)、[Cloud Gateway Fiber](https://store.ui.com/us/en/products/ucg-fiber)：UniFi 候选组合。
- 模型链接见第 5.2 节。模型卡中的容量、性能和兼容性是页面声明；M5 Ultra 的实际速度、并发、温度、Metal 分配和长时间稳定性必须在购买后实测。

## 8. 变更记录

| 日期 | 变更 |
|------|------|
| 2026-10-12 | 首次建立；记录用户户型、HomePod mini、未来 Apple Home Hub、Mac Studio M5 Ultra、Aqara 优先/ORVIBO 仅空调、四 AP 多千兆有线拓扑和模型部署基线。 |
| 2026-10-12 | 根据用户确认补充：不要求每个房间建设设备箱；默认中央 PoE 交换机回接墙面 AP，AP 额外 ≥2.5GbE 端口直接接电脑，房间多设备时再接可维护的 2.5G 小交换机；修正 Mac Studio 512GB 含义和 SSD 规格记录。 |
