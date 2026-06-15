# 家庭双路由网络方案可行性分析

## 摘要

本报告针对"主路由器 + 副路由器"双路由网络架构进行技术可行性评估。该方案的核心需求为：主路由器承载家庭日常网络，副路由器通过 WireGuard 隧道 24 小时连接公司网络，用户通过切换 WiFi 即可在家庭网络与工作网络之间切换，同时工作网络需保持对 NAS 文件访问及 AirPlay/HomeKit 设备发现的能力。经分析，该方案在技术层面整体可行，但 mDNS 跨子网中继在 HomeKit 场景下存在已知可靠性问题，需通过配置优化和备选策略缓解。

## 1. 方案概述与需求分析

### 1.1 核心需求

| 需求维度 | 具体要求 | 优先级 |
|----------|---------|--------|
| 网络隔离 | 工作流量与家庭流量完全隔离，VPN 故障不影响家庭网络 | P0 |
| 切换便捷 | 切换 WiFi 即可切换网络出口，无需额外操作 | P0 |
| NAS 访问 | 工作网络下可访问家庭 NAS 的 SMB/NFS 文件服务 | P0 |
| 设备发现 | 工作网络下可使用 AirPlay 投屏、HomeKit 控制智能家居 | P1 |
| 主路由不动 | 主路由器保持原厂固件，不做任何改动 | P1 |
| VPN 隧道 | 副路由器 24 小时维持 WireGuard 隧道连接公司网络 | P0 |

### 1.2 约束条件

- 主路由器使用原厂固件，不刷 OpenWrt
- 用户有 OpenWrt 刷机经验，可购买新硬件
- 公司网络通过 WireGuard/OpenVPN 虚拟组网接入
- 预算范围：副路由器 150-350 元

## 2. 方案架构设计

### 2.1 网络拓扑

```
互联网
  │
  ▼
┌──────────────────┐
│   光猫 (桥接模式)  │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────┐
│   主路由器 (原厂固件)          │
│   192.168.1.1                │
│   DHCP: 192.168.1.100-200    │
│   WiFi: "Home"               │
└────────┬─────────────────────┘
         │
    ┌────┴──────────────────────┐
    │  主网络 192.168.1.0/24     │
    │  NAS / Mac / 智能家居设备   │
    │                            │
    │  ┌────────────────────────┐│
    │  │ 副路由器 (OpenWrt)      ││
    │  │ WAN: DHCP → 192.168.1.x││  ← 从主路由器获取 IP
    │  │ LAN: 192.168.2.1       ││  ← 创建工作子网
    │  │ WiFi: "Work"           ││
    │  │ + WireGuard 隧道        ││  ← 24h 连接公司
    │  │ + avahi-daemon 中继     ││  ← 跨子网 mDNS
    │  │ + NAT (MASQUERADE)      ││  ← 透明访问主网络
    │  └────────┬───────────────┘│
    │           │                │
    │  工作子网 192.168.2.0/24    │
    │  你的工作设备               │
    └────────────────────────────┘
```

### 2.2 数据流路径

| 场景 | 流量路径 |
|------|---------|
| 工作设备 → 公司网络 | 设备 → 副路由器 LAN → WireGuard 隧道 (wg0) → 公司网络 |
| 工作设备 → 互联网 | 设备 → 副路由器 LAN → WireGuard 隧道 → 公司网络 → 互联网 |
| 工作设备 → NAS | 设备 → 副路由器 LAN → NAT 转换 → 副路由器 WAN → 主网络 → NAS |
| 工作设备 → AirPlay | 设备 mDNS 查询 → avahi-daemon 中继 → 主网络 AirPlay 设备响应 → 副路由器 NAT → 设备 |

## 3. 关键技术可行性评估

### 3.1 WireGuard 隧道性能

副路由器需同时处理 WireGuard 加密和 WiFi 转发，CPU 是关键瓶颈。基于社区基准测试数据：

| SoC | CPU 规格 | WireGuard 吞吐量 | CPU 占用 | 数据来源 |
|-----|---------|------------------|---------|---------|
| MT7981B | 2× A53 @ 1.3 GHz | **355-470 Mbps** | ~95% (满载) | GL.iNet 官方 / LeMaker 基准 |
| MT7986AV | 4× A53 @ 2.0 GHz | **735-936 Mbps** | ~60-70% | OpenWrt 论坛 wg-bench |
| MT7988A | 4× A73 @ 1.8 GHz | **~1 Gbps** | ~55-65% | LeMaker 基准 |

**评估结论**：MT7981B 平台路由器（150-350 元价位）的 WireGuard 吞吐量为 **355-470 Mbps**，对于办公场景（远程桌面、文件传输、视频会议）完全足够。典型办公带宽需求为 20-50 Mbps，即使 4K 视频会议也仅需 15-25 Mbps。CPU 满载仅出现在极端吞吐场景，日常使用 CPU 占用预计低于 30%。

> 在 150-350 元价位段，MT7981B 是唯一可选 SoC，WireGuard 性能充裕，不构成瓶颈。

### 3.2 mDNS 跨子网中继可行性

这是本方案最关键的技术风险点。mDNS（Bonjour）基于组播，天然不跨越路由器边界，需要中继器转发。

#### 可用方案对比

| 方案 | 优势 | 劣势 | 推荐度 |
|------|------|------|--------|
| **avahi-daemon (reflector 模式)** | OpenWrt 官方源可用；支持服务类型过滤；有 init 脚本 | 需禁用 umdns 避免冲突；~1-2MB 存储占用 | ★★★★★ |
| mdns-repeater | 极轻量 (~20KB) | 不在官方源；需自行编译；无服务过滤；无 IPv6 | ★★★ |
| umdns | OpenWrt 默认 | **不支持 reflector 模式**，无法跨子网 | ★ |

**推荐方案**：avahi-daemon，配置 reflector 模式 + 服务类型过滤。

#### 各协议跨子网可靠性评估

| 协议/服务 | 跨子网可靠性 | 说明 |
|-----------|-------------|------|
| **SMB/NFS 文件访问** | ✅ 完全可靠 | 基于 TCP 单播，NAT 转换后正常工作，不依赖 mDNS |
| **AirPrint** | ✅ 可靠 | avahi reflector 最成熟的用例 |
| **AirPlay 发现** | ⚠️ 基本可用 | 发现可工作，但偶有设备列表延迟 5-15 秒出现 |
| **AirPlay 投屏** | ⚠️ 基本可用 | 连接建立后稳定，初始发现稍慢 |
| **HomeKit 控制** | ⚠️ 有风险 | 已知问题：设备偶发显示"无响应"，因 mDNS 公告超时 |
| **HomeKit 配对** | ❌ 需同网段 | 首次配对必须在同一子网完成 |

**核心风险**：Apple 设备的 mDNS 公告刷新间隔为 60-120 秒，avahi-daemon 在转发过程中可能出现公告超时，导致 HomeKit 设备间歇性显示"无响应"。此为已知的架构性限制，非配置问题。

#### 缓解策略

1. **HomeKit 设备配对**：首次配对在主网络完成后再使用，跨子网控制已配对设备的可靠性优于首次配对
2. **avahi 服务过滤**：仅转发必要的服务类型，减少 mDNS 噪声
3. **reflector-quick-join**：启用快速加入模式，缩短发现延迟
4. **防火墙放行**：确保 UDP 5353 端口在两个子网间畅通

### 3.3 NAT 穿透与 NAS 访问

副路由器 WAN 口开启 MASQUERADE 后，工作子网设备访问 NAS 的流量路径：

```
工作设备 (192.168.2.100)
  → 请求 192.168.1.50:445 (NAS SMB)
  → 副路由器 NAT: 源地址 192.168.2.100 → 192.168.1.x (副路由器 WAN IP)
  → NAS 收到来自 192.168.1.x 的请求，正常响应
  → 副路由器 NAT 还原，转发响应给工作设备
```

**评估结论**：✅ 完全可行。副路由器 NAT 使 NAS 看到请求来自同网段设备，无需在主路由器上添加静态路由。这是 OpenWrt 默认行为，无需额外配置。

**注意事项**：
- 需开启 `mtu_fix`（MSS Clamping），避免双 NAT 场景下的 MTU 分片问题
- 主网络设备无法主动访问工作子网设备（单向可访问），但这对当前需求无影响

### 3.4 主路由器零改动可行性

| 操作 | 是否需要主路由器配合 |
|------|-------------------|
| 副路由器 WAN 获取 IP | ❌ 主路由器 DHCP 自动分配 |
| 工作子网访问 NAS | ❌ 副路由器 NAT 处理 |
| mDNS 中继 | ❌ 副路由器 avahi-daemon 处理 |
| WireGuard 隧道 | ❌ 副路由器独立建立 |
| 工作子网访问互联网 | ✅ 通过 WireGuard 隧道，不经主路由器 WAN |

**评估结论**：✅ 主路由器完全零配置。副路由器对主路由器而言只是一个普通的有线客户端。

## 4. 硬件选型分析

### 4.1 候选副路由器

| 型号 | SoC | RAM/Flash | WiFi | 网口 | OpenWrt 支持 | 参考价格 |
|------|-----|-----------|------|------|-------------|---------|
| **小米 AX3000T (RD03)** | MT7981B | 512MB/128MB | WiFi 6 AX3000 | 4× 千兆 | 23.05 起官方支持 | ¥90-160 |
| **GL.iNet MT3000** | MT7981B | 512MB/256MB | WiFi 6 AX3000 | 1× 2.5G + 1× 千兆 | 原生 OpenWrt | ¥300-430 |
| **GL.iNet MT2500A** | MT7981B | 1GB/8GB eMMC | 无 WiFi | 1× 2.5G + 1× 千兆 | 原生 OpenWrt | ¥349-369 |
| **CMCC RAX3000M** | MT7981B | 512MB/128MB | WiFi 6 AX3000 | 4× 千兆 | 官方支持 | ¥150-250 (二手) |

### 4.2 选型建议

| 使用场景 | 推荐型号 | 理由 |
|---------|---------|------|
| **性价比首选** | 小米 AX3000T (RD03) | 价格最低 (~¥130)，WiFi 6 完整，4 个千兆口。**必须确认是 RD03 版本**，RD01/RD02 为高通芯片，OpenWrt 支持差 |
| **开箱即用** | GL.iNet MT3000 | 原生 OpenWrt，无需刷机，2.5G WAN 口。但仅 1 个 LAN 口，扩展性有限 |
| **纯旁路由 (无 WiFi)** | GL.iNet MT2500A | 1GB RAM + 8GB eMMC，性能余量大。需搭配独立 AP 或主路由器 WiFi |
| **均衡之选** | CMCC RAX3000M | 4 千兆口 + USB 3.0，但需二手渠道购买 |

> **核心提醒**：所有 150-350 元价位路由器均使用 MT7981B SoC，WireGuard 吞吐上限约 470 Mbps。若需更高 VPN 性能，需升级至 MT7986 平台（¥400+）。

## 5. 风险评估与缓解

### 5.1 风险矩阵

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| HomeKit 设备间歇性"无响应" | 高 | 中 | 首次配对在主网完成；使用 avahi 服务过滤减少噪声；接受偶发延迟 |
| WireGuard 隧道断线 | 低 | 高 | 配置 `persistent_keepalive 25`；OpenWrt 自带 Watchdog 自动重连 |
| 副路由器硬件故障 | 低 | 中 | 工作网络中断不影响家庭网络；更换成本低 (~¥130) |
| avahi-daemon 与 umdns 冲突 | 中 | 低 | 安装后立即禁用 umdns，写入启动脚本 |
| 双 NAT 导致 MTU 问题 | 低 | 中 | 开启 `mtu_fix` (MSS Clamping) |
| 小米 AX3000T 买错版本 | 中 | 高 | **购买前确认 RD03 版本**，RD01/RD02 不可用 |

### 5.2 已知限制

1. **HomeKit 跨子网非完美体验**：这是 mDNS 中继的架构性限制，无法通过配置完全消除。若 HomeKit 可靠性是硬性要求，需考虑替代方案（见第 6 章）
2. **主网络无法主动访问工作子网**：NAT 导致单向可访问。若需双向访问（如从 Mac SSH 到工作设备），需在副路由器上配置端口转发
3. **副路由器 WiFi 性能**：MT7981B 的 WiFi 6 在 2×2 MIMO 下理论最高 1.2 Gbps，实际约 500-700 Mbps。若工作设备密集使用，可能成为瓶颈

## 6. 替代方案对比

### 6.1 方案对比矩阵

| 维度 | A: 双子网 + mDNS 中继 | B: 主路由 VPN + PBR | C: 副路由透明网桥 | D: 副路由 Dumb AP + 设备端 VPN |
|------|----------------------|---------------------|------------------|------------------------------|
| 同网段 | 否（功能等效） | 是 | 是 | 是 |
| AirPlay/HomeKit | 通过 mDNS 中继（有风险） | 原生支持 | 原生支持 | 原生支持 |
| 主路由是否需改动 | ❌ 不需要 | ✅ 需刷 OpenWrt | ❌ 不需要 | ❌ 不需要 |
| 配置难度 | 低 | 中 | 高 | 低 |
| VPN 位置 | 副路由器 | 主路由器 | 副路由器 | 各设备 |
| 切换方式 | 切换 WiFi | 切换 WiFi | 切换 WiFi | 手动开关 VPN |
| 稳定性 | 高 | 中 | 低 | 高 |
| 硬件成本 | ~¥130 | 可能需升级主路由 | ~¥130 | ~¥0 (软件VPN) |

### 6.2 方案 D 补充说明：Dumb AP + 设备端 VPN

此方案将副路由器配置为 Dumb AP（不创建子网，仅扩展 WiFi 覆盖），VPN 由各工作设备自行连接：

- 副路由器关闭 DHCP，桥接到主网络
- 工作设备连接 "Work" WiFi，仍在 192.168.1.0/24 网段
- 工作设备上运行 WireGuard 客户端连接公司
- AirPlay/HomeKit 原生工作，无任何兼容问题

**优势**：完美解决 mDNS 兼容性问题，配置最简单
**劣势**：每台工作设备需单独配置 VPN 客户端；iOS/macOS 的 WireGuard 客户端需手动开关

## 7. 结论与建议

### 7.1 总体可行性判定

**方案 A（双子网 + mDNS 中继）技术可行，但存在 HomeKit 可靠性风险。** 核心评估如下：

- WireGuard 隧道性能：✅ 充裕（355-470 Mbps，远超办公需求）
- NAS 文件访问：✅ 完全可靠（NAT 穿透无障碍）
- AirPlay 投屏：⚠️ 基本可用（发现延迟 5-15 秒，连接后稳定）
- HomeKit 控制：⚠️ 有风险（偶发"无响应"，架构性限制）
- 主路由零改动：✅ 完全可行

### 7.2 推荐实施路径

**推荐采用方案 A 作为主方案，方案 D 作为 HomeKit 场景的备选。**

1. 首先部署方案 A（双子网 + mDNS 中继），满足 90% 的使用场景
2. 若 HomeKit 体验不可接受，可将副路由器切换为 Dumb AP 模式，工作设备自行运行 VPN 客户端
3. 两种模式可在副路由器上保存为不同配置，快速切换

### 7.3 硬件采购建议

**首选：小米 AX3000T (RD03)**，约 ¥130。购买时务必确认 RD03 版本。若追求开箱即用和稳定性，可选 GL.iNet MT3000（约 ¥300-430）。

## 参考资料

[1] OpenWrt Forum. A WireGuard Comparison DB[EB/OL]. https://forum.openwrt.org/t/a-wireguard-comparison-db/187586
[2] LeMaker. WireGuard Throughput Benchmarks: Filogic Routers[EB/OL]. https://blog.lemaker.org/wireguard-throughput-benchmarks-filogic-routers-bpi-r4-vs-openwrt-one/
[3] OpenWrt Wiki. Zero Configuration Networking[EB/OL]. https://openwrt.org/docs/guide-user/network/zeroconfig/zeroconf
[4] OpenWrt Forum. mDNS Repeater Using mdnsd[EB/OL]. https://forum.openwrt.org/t/mdns-repeater-using-mdnsd-mdnsresponder/53112
[5] OpenWrt Forum. Apple Home/HomeKit on Isolated Network[EB/OL]. https://forum.openwrt.org/t/apple-home-homekit-on-a-isolated-network-results-in-very-slow-iot-devices/148802
[6] OpenWrt Forum. How to Access Second OpenWrt Router[EB/OL]. https://forum.openwrt.org/t/how-to-access-second-openwrt-router/193624
[7] Habr. What OpenWrt Router to Buy in 2025[EB/OL]. https://habr.com/en/articles/990172/
[8] TheTestedHub. GL-MT3000 Review[EB/OL]. https://thetestedhub.com/reviews/gl-inet-beryl-ax/
