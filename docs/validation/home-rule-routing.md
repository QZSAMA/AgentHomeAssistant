# 全屋规则分流验收与应急操作单

> **需求已修订：以[最新故障隔离设计](../superpowers/specs/2026-11-05-home-rule-routing-availability.md)为准。** 本文C表和D节是原单网关试验/人工回退记录，不能证明“J3455故障时普通上网仍可用”。原全屋DHCP迁移暂停。优先试验定向 DNS + 合成地址段静态路由；见[官方功能调研](../fusion-domain-routing-capability-research.md)。以下所有设备检查均未实测。

文档核验已完成：Fusion 专用手册确认域名策略、目的网段静态下一跳及 Local DNS FORWARD；策略界面没有任意 LAN 下一跳字段。此状态仅表示资料已核验，**不将任何现场项目标为 `passed`**。

| 新ID | 优先架构必须验证的内容 | 状态 |
|---|---|---|
| A1 | Fusion具体硬件版、Omada OS及Network Application版本 | `not_run` |
| A2 | 实机具有 Local DNS FORWARD 与静态 Next Hop；专用合成地址段可经 LAN 交给 VM，不能只证实 WAN 选线 | `not_run` |
| A3 | 普通网站一直直接走Fusion；转回Fusion的规则流量不循环 | `not_run` |
| A4 | DHCP与普通DNS不依赖J3455；缓存不使普通网站间接依赖规则服务 | `not_run` |
| A5 | 停规则服务、停VM、正常停宿主、拔J3455网线时普通上网仍可用 | `not_run` |
| A6 | IPv6、CDN共用地址、应用独立解析不导致错误分流 | `not_run` |
| A7 | 指定网站在J3455故障时可失败，符合用户已确认范围 | `not_run` |
| A8 | FORWARD 的完整域名、子域、别名、CNAME 与作用 LAN 范围已核验；试验不误影响全屋 | `not_run` |
| A9 | Fusion 正常转交合成地址响应；普通域名不进入合成地址段；与现有地址用途不冲突 | `not_run` |
| A10 | Fusion 定向清单与引擎清单一致；DNS 不递归，节点启动解析不依赖自身，服务端口可达 | `not_run` |
| A11 | 重启后 Fusion/终端/引擎缓存与映射正确；同 LAN 转发、回包及 ICMP redirect 行为已记录 | `not_run` |
| A12 | 指定 DNS 上游停机或超时不拖累普通解析；同时测普通 DNS 缓存命中、未命中及新连接 | `not_run` |
| A13 | AAAA、HTTPS/SVCB、应用自身 DNS 与硬编码 IP 的覆盖差异逐类记录；本地 IPv6/Thread 正常 | `not_run` |
| A14 | 规则数量、更新、容量和撤销方式可维护；未将手工小样本通过等同全屋完整覆盖 | `not_run` |

状态基线：`not_run`。日期：2026-11-05。本文是脱敏记录模板；不要填写真实节点、订阅地址、口令或完整访问历史。先看[设计](../superpowers/specs/2026-11-05-home-rule-routing-design.md)与[实施计划](../superpowers/plans/2026-11-05-home-rule-routing.md)。

## A. 实际参数表（部署前填写）

| 参数 | 示例 | 实际值 | 证据/时间 |
|---|---|---|---|
| 家庭 LAN/CIDR | `192.168.50.0/24` | `not_run` |  |
| Fusion LAN IP | `.1` | `not_run` |  |
| OpenWrt 管理 IP | `.2` | `not_run` |  |
| PVE 管理 IP | `.3` | `not_run` |  |
| 应急笔记本 | `.10/24` | `not_run` |  |
| 家庭桥名 | `vmbr0`（示例） | `not_run` |  |
| 新 VMID / 名称 | `待分配 / home-rule-router` | `not_run` |  |
| 固定 MAC | `待记录` | `not_run` |  |
| OpenWrt 实际 LAN 接口 | `br-lan`（示例） | `not_run` |  |
| Fusion 普通 DHCP 状态 | `enabled`（原网） | `not_run` |  |
| OpenWrt DHCP 状态 | `disabled`（建 VM） | `not_run` |  |
| 公网 IPv6 默认路由 | `未核验` | `not_run` |  |
| 宿主本地备份存储 | `待核` | `not_run` |  |

示例地址不是事实。若实际子网不同，实施计划中的所有 `.1/.2/.3/.10`、池和私有网段规则必须整体映射。

## B. 设备覆盖清单

每台有家庭 IP 的设备逐行登记：设备/区域、地址来源（动态/保留/静态）、MAC 是否随机、网关、DNS、普通访问、指定网站、局域网发现、最后续租时间。没有独立 IP 的 Zigbee 设备填写“经所属网关”，不要伪造终端地址。

| 设备类别 | 数量/范围 | 状态 | 备注 |
|---|---:|---|---|
| 手机/平板/电脑 | 待盘点 | `not_run` | 有线与三个 AP实际启用频段分别抽测 |
| 电视/投影/影音 | 待盘点 | `not_run` | 播放、发现、睡眠唤醒 |
| Apple 家庭中枢/音箱 | 待盘点 | `not_run` | 本地发现与云功能分开记 |
| Aqara 网关及设备 | 网关待到货 | `not_run` | M200/M1S 的家庭 IP；传感器经网关 |
| 摄像机/其他 IoT | 待盘点 | `not_run` | 不能浏览的设备用服务会话验收 |
| J3455 宿主/来宾 | 宿主+现有 VM+规则 VM | `not_run` | 管理网关/DNS走 Fusion |
| 交换机/AP/Fusion | 按当前拓扑 | `not_run` | 管理地址保持可达 |

## C. 现场验收记录

| ID | 检查 | 状态 | 证据/时间 |
|---|---|---|---|
| P1 | PVE/J3455资源、温度、磁盘健康及存储 VM不受影响 | `not_run` |  |
| P2 | 镜像/插件/引擎哈希及实际版本 | `not_run` |  |
| P3 | OpenWrt根文件系统实际扩容；只操作新虚拟盘 | `not_run` |  |
| P4 | OpenWrt固定地址、上游 `.1`、DHCP/RA关闭阶段无冲突 | `not_run` |  |
| P5 | 标准 fw4 SNAT、IPv4转发、无 ICMP redirect、flow offload关闭 | `not_run` |  |
| P6 | 试点设备普通外网、DNS、本地 IP访问及回包路径 | `not_run` |  |
| P7 | 规则模式：指定网站命中 `RULE-OUT`，普通网站为 `DIRECT` | `not_run` |  |
| P8 | 规则服务重启、VM重启后 DNS与路由不回环 | `not_run` |  |
| P9 | UDP/QUIC/语音/游戏/影音与本地 mDNS/AirPlay/HA/Matter（若有） | `not_run` |  |
| P10 | 写死 DNS、应用内加密解析、私有中继等设备已识别 | `not_run` |  |
| P11 | Fusion DHCP关闭、OpenWrt唯一 DHCP开启；动态/静态设备逐台续租 | `not_run` |  |
| P12 | IPv6无公网绕行；本地 IPv6/Thread能力仍可用 | `not_run` |  |
| P13 | 全屋普通/指定访问和各区域接入覆盖 | `not_run` |  |
| P14 | 全屋人工回退到 Fusion，并实测恢复时间 | `not_run` |  |
| P15 | 72h稳定性、性能、启动顺序和外部备份读回 | `not_run` |  |

## D. 最小应急操作

### D1. 管理入口

1. 用有线笔记本接入任一**未故障**的家庭交换机端口；若电竞房链路故障，改接中央或大厅可用端口。
2. 暂时设置已查重的静态地址 `ADMIN_IP/24`，网关/DNS填 `FUSION_IP`。通过实际 IP 打开 Fusion、OpenWrt和 PVE 管理页；不要依赖域名解析。
3. 记下变更前时间和当前 DHCP 服务端。没有确认 OpenWrt DHCP已停前，不能开启 Fusion DHCP。

### D2. 规则服务坏了，但 OpenWrt VM仍在线

1. 从 OpenWrt 管理页或 PVE控制台停用规则接管；不要只杀 Mihomo进程。
2. 确认标准 fw4转发/SNAT仍在，删除失效 TUN/策略路由残留；运行 `fw4 check`，再查看 `nft list ruleset`。
3. 将 dnsmasq普通上游恢复为 Fusion实际 LAN IP；重启 dnsmasq。清除试点/受影响终端的合成解析缓存并重新连接。
4. 测试普通域名、真实 IP、本地 NAS/家庭控制；在记录中写“规则暂停”，不要把此状态写成规则仍生效。

### D3. OpenWrt VM/J3455 停机，全屋回到 Fusion

1. 使用应急笔记本按 D1 进入管理；确认 OpenWrt VM 已停止，且 PVE不会自动把它拉起。若宿主彻底断电，确认其网卡没有继续提供 DHCP。
2. **先确认 OpenWrt DHCP停止/不可运行，再在 Fusion LAN上开启唯一 DHCP。** 记录 Fusion原来的池、网关 `.1`、DNS和租期。不要先开 Fusion再去关 OpenWrt。
3. 对手机/电脑/电视/网关逐类断开重连或主动续租；手工静态设备把网关/DNS改回 `.1`。清除合成解析缓存，确认普通网站和本地服务。
4. 记录每类设备恢复时间；同网段真实 IP的部分本地访问可能仍可用，依赖 DNS、新租约、云服务或 J3455 上 HA 的功能可能不可用。
5. 若需要继续使用规则系统，先恢复 Fusion普通网络，再在 PVE控制台修 OpenWrt；修复后按计划的切换顺序重新启用，不要在故障现场同时打开两台 DHCP。

### D4. 完整恢复后的切回规则模式

1. 导出 Fusion配置/租约，确认 OpenWrt配置和备份可读。
2. Fusion DHCP关闭并确认保存；OpenWrt DHCP开启并确认只有它回应。
3. 动态终端续租，静态终端改回 `.2`；核对网关、DNS、IPv6和本地发现。
4. 先测普通访问，再测 `RULE-OUT`站点；更新 C 表，不把“VM已启动”当成全屋完成。

## E. 状态规则

- `not_run`：未执行或只有文档/静态检查证据。
- `passed`：现场有时间、命令/页面或脱敏截图证据，且限制条件已记录。
- `failed`：现场复现失败，记录影响、回退动作和下一步；不得用“未发现问题”替换。
- 任何真实凭据、节点地址、订阅链接、完整终端访问日志只放加密运维资料，不进入本文件或 Git。
