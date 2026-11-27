# 规则分流：公开案例、故障与浏览器兼容证据

调研日期：2026-11-05。当时调查对象为Fusion与J3455上的规则服务，未连接或修改家庭设备。本文保留原始来源和证据边界，本次整理不刷新检索日期。

现行采用[同一LAN按设备手动选用OpenWrt](superpowers/specs/2026-11-05-home-device-rule-routing-design.md)，普通设备继续走Fusion，规则终端故障时手动切回。执行见[现行计划](superpowers/plans/2026-11-05-home-device-rule-routing.md)和[验收单](validation/home-device-rule-routing.md)。下列案例是研究证据，不是待采用的替代采购或部署方案。

## 1. 证据结论

**定向DNS与合成地址路由存在公开使用记录；原检索没有找到可核验的Fusion专用完整部署和宿主停机验收案例。** 其他网关的成功或故障自述不能替代本户验证，也不改变已批准的按设备方案。Fusion原厂功能边界见[官方核验](fusion-domain-routing-capability-research.md)。

## 2. 实际找到的案例

| 来源及日期 | 实际报告的内容 | 能证明什么 | 不能证明什么 |
|---|---|---|---|
| [Mihomo #916](https://github.com/MetaCubeX/mihomo/issues/916)，2023-12-14 发起 | 发帖者说明自己在主路由运行 mosdns，分别返回真实地址与合成地址，再用静态路由交给规则设备 | DNS 与数据路径分离有实际使用者 | 帖首的部分配置是功能提案，不能整段当作现行配置；没有 Fusion 实测 |
| [同帖使用反馈](https://github.com/MetaCubeX/mihomo/issues/916#issuecomment-1869186304)，2023-12-26 | 一位参与者自述“用了2个月了，非常稳定” | 同类方案有持续使用自述 | 没有公开完整的断电、DNS 冷缓存或所有应用验收，不能量化故障率 |
| [RouterOS + J4125/PVE 案例](https://github.com/kkkgo/PaoPaoGateWay/discussions/48)，2023-12-23 至 12-30 | 独立 MikroTik 主路由，J4125/PVE 承载 DNS 与规则网关，主路由配置合成地址段静态路由；作者报告能访问但页面慢，之后反馈调整防火墙后问题解决 | 与本项目接近的“小主机 + PVE + 独立主路由”实际部署；转发/回包需要适配 | 普通 DNS 也在该 PVE 上，原文没有证明宿主停机后普通解析独立可用；不是 Fusion |
| [爱快 + PaoPao 网关案例](https://github.com/kkkgo/PaoPaoGateWay/discussions/26)，2023-10-08 起 | 作者报告已能访问，来源地址被转换成爱快地址，后反馈调整 NAT 规则后恢复来源识别；其他参与者报告不同路由方式下有故障 | 爱快主路由配合独立规则网关有实际案例，配置细节影响结果 | 不能由“爱快支持下一跳”推出自动故障切换已就绪；评论中的故障归因没有独立复测 |
| [梅林 + Hyper-V 教程](https://github.com/lesnolie/Marverick/issues/37)，2024-03-16 | 作者给出 DNS、规则 VM、主路由及静态路由的安装记录 | 另一平台上的实际部署记录 | 文章提出备用 DNS，但没有证明备用服务与主服务位于独立宿主，也没有完整的停机演练 |

另外，[PaoPaoGateWay 项目](https://github.com/kkkgo/PaoPaoGateWay)与[作者的原理说明](https://blog.03k.org/post/paopaogateway.html)明确描述了合成地址映射、主路由静态路由与 DNS 分流。[PaoPaoDNS 文档](https://github.com/kkkgo/PaoPaoDNS)的 `CUSTOM_FORWARD` 支持按名单向指定 DNS 转交查询。这证明已有实现思路和组件，不意味着应该把现有 OpenWrt 计划直接换成该项目。

不能照搬教程中的旧版本参数、地址池和防火墙放宽规则。此处引用的是部署事实与故障现象；具体设置应依据当前软件文档及本地验证。

## 3. 为什么“普通流量直连”仍可能在旁路停机时断网

普通访问依赖两个过程：先解析域名，再建立连接。

```text
数据直连，但解析依赖 J3455：
终端 → Fusion → 宽带                 数据路径独立
终端 → DNS 服务（J3455 上）           解析仍有共同故障点

现行按设备方案：
普通设备的解析与连接 → Fusion → 宽带
选用OpenWrt的终端 → J3455规则VM → Fusion → 宽带
规则VM/宿主故障时，该终端手动切回Fusion普通路径
```

因此，下列情况都不能证明本项目的要求已满足：

- 关闭规则服务后，已经打开的视频继续播放：这可能只说明已有连接尚可用。
- 两个 DNS 容器或两台 VM 都放在 J3455：宿主停机后会一起不可用。
- 终端填写两个 DNS 地址：终端或应用可能选择任意一个，不保证严格主备，也可能使指定规则失效。
- 只改变 DHCP 下发网关：旧租约和静态配置不会立即更新。
- 只 ping J3455：宿主在线并不代表 VM 内解析和规则服务正常。
- 只停用插件测试一次：不能替代 VM、宿主和数据线故障测试。

上述社区讨论有人只依赖 DNS 缓存撑过短时间故障。缓存不覆盖未访问域名与过期记录，不能作为长期普通上网的保障。

## 4. 合成地址的浏览器兼容证据

原调研读取的[PaoPaoGateWay文档](https://github.com/kkkgo/PaoPaoGateWay)提醒合成地址池可能触发浏览器本地网络访问检查。[Chrome官方公告](https://developer.chrome.com/blog/local-network-access)说明相关权限从Chrome 142推出；[地址空间规范](https://wicg.github.io/local-network-access/)将`198.18.0.0/15`列为loopback地址空间。

这不等于所有合成地址连接都会被禁止；行为与浏览器版本、页面来源和资源请求类型有关。若现行OpenWrt规则VM使用合成地址，试点应覆盖普通页面请求该类资源，不能仅凭主站打开就认定地址池可用。不得把文档示例`198.18.0.0/16`未经验证直接设为家庭参数，也不照搬随意占用真实公网地址的旧教程。这里只保留规则终端的兼容性检查，不在Fusion新增全屋静态路由。

## 5. 现行验收与研究边界

普通设备的网关、地址服务与普通DNS继续由Fusion提供；停止规则服务、VM、宿主及断开J3455数据线时，要验证普通新域名与新连接。选用OpenWrt的终端另验手动切回、局域网发现、应用解析及IPv6行为，记录在[现行验收单](validation/home-device-rule-routing.md)。全部现场项目仍为`not_run`，没有因本研究新增硬件或部署。

原调查读取上述项目讨论、作者文档及[RouterOS Netwatch](https://help.mikrotik.com/docs/spaces/ROS/pages/8323208/Netwatch)、[RouterOS DNS](https://help.mikrotik.com/docs/spaces/ROS/pages/37748767/DNS)与[Omada控制器离线说明](https://support.omadanetworks.com/us/document/12964/)等官方资料。它们提供健康检测、解析和控制器故障的背景知识，不证明Fusion具备相同功能，也不构成更换主网关/迁移控制器的决定。

针对Fusion组合的公开检索曾遇到验证码及结果相关性限制；“没有找到完整成功与宿主故障验收案例”仅限原已核验资料，不等于全网不存在。
