# 全屋规则分流与 J3455 旁路由实施计划

> **同日修订：全屋推广暂停，先读[故障隔离与 Fusion 规则核验](../specs/2026-11-05-home-rule-routing-availability.md)。** 用户现要求 J3455故障不影响普通上网；本文原单VM/唯一DHCP方案不能满足。任务1–5仅可在核清实际参数后用于隔离或单设备试验；任务6–8的全屋地址服务迁移不可照旧执行。优先核验 Fusion仅将指定网站交给J3455的功能，普通流量和地址/解析服务保持独立，再据验证结果重写推广步骤。

> **For agentic workers:** 使用 `executing-plans` 技能按任务执行并在各阶段核验证据。本文交付的是计划，不代表已连接或改动家庭设备。各步骤用复选框记录，只有实机完成后才能勾选。

**Goal:** 全屋终端在原有物理布线下按网站规则自动选择出口，同时具备断网时可用的管理和人工恢复路径。

**Architecture:** Fusion 保留宽带与控制器；现有 J3455/Proxmox 新增 OpenWrt 完整 VM，单臂接入同一家庭 LAN，负责全屋默认网关、DNS和唯一 DHCP。先保持 Fusion 地址服务，单设备试点通过后再全屋切换。

**Tech Stack:** 现有 Proxmox；候选 OpenWrt 25.12.6 x86-64、OpenClash v0.48.002、Mihomo v1.19.33 amd64 v1；fw4/nftables；VirtIO。

## Global Constraints

- 用户已确认所有联网设备都要覆盖；基础设施启动与应急管理按设计保留上游例外。
- 保留现有存储 VM，不重装宿主、不重建宿主网络桥，不在本轮安装网卡或迁移 HA。
- 四条中央主干、三个 AP、现有 J3455 端口和物理线保持；J3455 箱外通风摆放。
- 同一家庭 LAN 任意时刻只允许一台 DHCP 服务器提供租约。
- 首期使用标准 fw4 SNAT，关闭插件重复的旁路兼容转换；不能停止防火墙。
- 首期外网 IPv4 是设计建议；公网 IPv6已有依赖时，停止全屋切换，另做双栈设计；保留本地 IPv6/Thread。
- 所有地址均为示例，先建立实际参数表；真实凭据不入 Git。
- 版本是候选组合，未经试点不得写成兼容通过；全部实机项目初始为 `not_run`。

设计依据：[详细设计](../specs/2026-11-05-home-rule-routing-design.md)。现场记录位置：[验收与应急单](../../validation/home-rule-routing.md)。

## 文档、配置和接口边界

| 位置 | 责任 | 写入时机 |
|---|---|---|
| 本计划 | 操作顺序、参数示例、各阶段进入/退出条件 | 设计交付；执行差异另记 |
| `docs/validation/home-rule-routing.md` | 脱敏参数、逐设备状态、实际版本、故障恢复用时 | 现场操作时追加证据 |
| OpenWrt `/etc/config/network` | 固定 LAN 地址、上游默认路由、系统启动解析 | 单设备试点前 |
| OpenWrt `/etc/config/dhcp` | 唯一 DHCP、租约、本地名称、普通/规则 DNS 接入 | 先关闭 DHCP，正式切换才开启 |
| OpenWrt `/etc/config/firewall` | 单臂转发、标准 SNAT、关闭加速 | 单设备普通转发验证前 |
| OpenWrt `/etc/sysctl.d/90-home-routing.conf` | redirect 关闭设置 | 单臂转发配置时 |
| OpenClash 私有配置 | 节点、规则、解析模式及运行状态 | 普通转发和 DNS通过后 |
| Fusion 管理界面 | DHCP唯一性、独立上游 DNS、外网 IPv6发布、控制器 | 盘点核验，切换时变更必要项 |
| PVE 的该新 VM 设置 | 磁盘、VirtIO、固定 MAC、启动顺序及备份 | 新建 VM 与最终验收 |

执行人员需要能在本地进入 Fusion 管理页、PVE控制台和新 VM 控制台。设备尚未到货时，先完成文档与离线文件准备；不要将候选设备的计划界面当成已经验证的现场功能。

## 任务 1：盘点资源、地址、基线和恢复通道（约 45–90 分钟）

**输入：** 现网和 J3455。**输出：** 实际参数表、现有服务清单、可恢复备份、普通网络基线。**退出条件：** 新 VM 有独立资源；管理员不依赖规则服务就能访问宿主与上游。

- [ ] 确认已到货的 Fusion、交换机、AP 型号与固件；未到货项记为尚未安装，不做虚构实测。
- [ ] 在 PVE 本地控制台或已授权的管理连接执行以下只读命令，保存脱敏结果。不能把命令示例作为连接真实主机的替代。

```sh
pveversion -v
qm list
pct list
pvesm status
ip -br address
ip route
bridge link
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
lscpu
```

- [ ] 记录实际 PVE 管理 IP、网关、DNS、家庭桥名、桥下物理网卡；只读查看当前来宾配置和启动顺序。识别旧规则容器有无接管、端口占用、自动修改宿主路由的行为。
- [ ] 逐台登记家庭终端的 IP、MAC、接入区、地址来源、网关、DNS、应用内独立网络设置。包括交换机、AP、存储 VM、未来 HAOS预留、M200/M1S/E1/S100、中枢、电视及手机；没有独立 IP 的 Zigbee 终端按所属网关登记。
- [ ] 通过现用终端和 Fusion 租约表核对真实网段，排除 `.2/.3/.10` 已被占用的情况；建立设计中的参数名到现场值的完整映射。保留原网段和已有固定地址，避免全屋重新编号。
- [ ] 核查 Fusion 是该 LAN 当前唯一地址服务、现有租期、普通 DNS上游、是否能导出配置、IPv6 默认路由从哪里发布。公网 IPv6已有依赖则保留现网，后续只试点，不进行全屋切换。
- [ ] 为管理笔记本保存一份**已查重**的静态地址配置，网关/DNS直接指向 Fusion；实际访问 Fusion、PVE及存储管理地址。再接回原网络。IP管理可用才继续。
- [ ] 导出 Fusion配置、PVE来宾配置、原地址保留及现有来宾可恢复备份；复制一份到 J3455之外。确认备份可列出文件且记录恢复入口。
- [ ] 选宿主本地可靠数据存储，确认它不依赖存储 VM先启动；为新 VM 留 2vCPU/2GiB/8GiB，并留出备份空间和宿主、存储、未来 HAOS预算。记录 `free`/磁盘状态，不按机器总内存推定有余量。
- [ ] 在同一有线电脑记录普通外网三次吞吐、延迟、丢包，连续传输 30分钟；记录 J3455 CPU/温度/内存/磁盘等待。没有开通目标宽带时，只写当前接入基线。

**失败处理：** 资源不够、管理链路不独立、备份不可读或地址冲突未消除时，不创建承担全屋职责的 VM；保持现网。

## 任务 2：准备可离线恢复的安装资料（约 30–60 分钟）

**输入：** 参数表与候选版本。**输出：** 校验过的镜像、插件/引擎文件、普通 DNS恢复记录。**退出条件：** 关键安装文件在断网时可取得；软件版本兼容性仍待任务 4/5验证。

- [ ] 从设计第13节的发行来源获取镜像 `openwrt-25.12.6-x86-64-generic-ext4-combined.img.gz`、该目录 `sha256sums`、插件 APK及 amd64 v1引擎。不要下载来源不明的整合系统或把动态远程脚本直接送进 shell。
- [ ] 在保存安装文件的 Windows管理电脑核对压缩镜像；以下命令只适用于该精确文件，在文件所在目录执行：

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath '.\openwrt-25.12.6-x86-64-generic-ext4-combined.img.gz'
```

预期 SHA256 为 `f8538784d0288b4133a99ac2a68443e4922ffde6343e80df56a5882364b9d499`，并应与官网下载清单一致。下载其他版本不能沿用此校验值。插件和引擎保留发行来源、文件哈希；来源提供签名/校验材料时一并核验。

- [ ] 准备官方 GParted Live ISO，记录来源和官方校验结果；它只用于新的虚拟盘，不挂任何宿主/存储数据盘给这台 VM。
- [ ] 将镜像解压成 `.img`，记录传入 PVE的绝对路径、文件哈希；用 `qemu-img info`读取镜像属性。实际执行路径来自刚传入的文件，不对任何 `/dev/sd*` 使用导入或覆盖操作。
- [ ] 保存 Fusion 管理入口、PVE入口、本计划、应急单和实际参数表在管理电脑及手机；凭据存个人密码管理器。先演示关闭互联网后仍能打开这些本地文件。
- [ ] 记录普通模式的 DNS上游：本案为 Fusion的 LAN IP，Fusion本身解析独立。节点域名必须能通过该路径解析，避免启动依赖回环。

## 任务 3：隔离创建 OpenWrt 完整虚拟机（约 45–75 分钟）

**输入：** 已核验的 VMID、存储和桥名；本地镜像。**输出：** 单网卡、固定地址、文件系统扩容后的独立 VM。**退出条件：** 连接家庭 LAN前默认地址和 DHCP/RA已关闭。

- [ ] 在 PVE网页创建新 VM，名称 `home-rule-router`；选空闲 VMID、SeaBIOS、2vCPU、CPU `host`、固定 2048MiB内存、VirtIO SCSI控制器。暂不勾选开机自启，确保不挂现有数据盘。
- [ ] 添加一张 VirtIO网卡，桥接任务1记录的家庭桥，不设 VLAN tag；固定 MAC并记录。**首启前勾选 Disconnect/链路断开**。不改宿主桥，不做物理网卡直通。
- [ ] 导入已解压镜像为这个新 VM的磁盘。按现场 PVE帮助使用 `qm disk import`或相应版本的 `qm importdisk`；把返回的 unused disk挂到该 VM，再设置磁盘启动。以下交互示例要求人工输入已核验参数，不含默认 VMID/存储猜测：

```sh
read -r -p '新 VMID: ' RULE_VMID
read -r -p '镜像绝对路径: ' RULE_IMAGE
read -r -p '目标本地存储 ID: ' RULE_STORAGE
qm config "$RULE_VMID"
qemu-img info "$RULE_IMAGE"
```

确认输出是新建空 VM和正确 `.img`后，再按当前 PVE支持的形式执行导入：

```sh
qm disk import "$RULE_VMID" "$RULE_IMAGE" "$RULE_STORAGE"
```

如果本机只支持 `qm importdisk`，使用 `qm help importdisk`核对相同参数后执行；**不要两种命令都运行**。GUI 挂载导入返回的磁盘卷，再将该虚拟盘扩到总计 8GiB。

- [ ] 用 GParted ISO离线启动新 VM；看清仅有新虚拟盘及 ISO，确认根分区后扩展根分区和 ext4文件系统至可用空间。操作前保留原始导入文件；如果分区结构无法确认，关机回到原始镜像，不操作其他盘。
- [ ] 卸载 ISO，设置新磁盘为首启动；保持网卡链路断开，进入 PVE串口/图形控制台。使用 `ip -br link`确认 guest实际网口名，`lsblk`/`df -h`确认根文件系统已扩展。不能只看 PVE虚拟盘显示 8GiB。
- [ ] 在 guest console先读取默认 UCI：

```sh
uci show network
uci show dhcp
ip -br link
```

若默认配置确有 `network.lan` 与 `dhcp.lan`，在链路断开时将示例整体映射为真实值后应用：

```sh
uci set network.lan.proto='static'
uci set network.lan.ipaddr='192.168.50.2'
uci set network.lan.netmask='255.255.255.0'
uci set network.lan.gateway='192.168.50.1'
uci set network.lan.peerdns='0'
uci -q delete network.lan.dns
uci add_list network.lan.dns='192.168.50.1'
uci set dhcp.lan.ignore='1'
uci set dhcp.lan.ra='disabled'
uci set dhcp.lan.dhcpv6='disabled'
uci commit network
uci commit dhcp
```

上述 UCI ID并不存在时先用默认文件中实际 LAN段名替换；不要新增第二个名字相似的 LAN接口。若 guest 旧配置把不匹配的 WAN/WAN6接口绑定到网口，先核清其默认路由、防火墙 zone和 DHCPv6服务，再移除对应绑定。首期只保留 LAN上游路径。设置管理员口令，管理界面仅家庭 LAN可达，关闭不需要的外网管理入口。提交前用 `uci show network`、`uci show dhcp`和 `uci changes`核对完整状态。
- [ ] 保存 guest配置并在仍隔离时重启，从控制台再次确认固定地址、DHCP/RA关闭。随后连接 VirtIO链路，验证没有地址冲突、没有第二个租约来源。
- [ ] 从管理电脑访问 OpenWrt固定 IP，从 guest测试 Fusion和普通域名解析；PVE网关/DNS继续直接指向 Fusion。此时全屋其他终端仍由 Fusion分配地址。

**失败处理：** 仅断开并停止新 VM；现网 DHCP不变。任何宿主地址/桥接变更均超出本任务。

## 任务 4：先验证无规则服务的普通网关（约 30–60 分钟）

**输入：** 可管理的新 VM；家庭仍由 Fusion分地址。**输出：** 单设备通过 OpenWrt普通转发、DNS与本地访问。**退出条件：** 独立于插件的直接转发基线成立。

- [ ] 备份新 VM的 `/etc/config/network`、`dhcp`、`firewall`，并通过 PVE console保留登录。防火墙的 LAN区域启用必要的 input/output及同区 forward；只绑定实际 LAN，不开放不存在的外网接口。
- [ ] 配置标准 fw4 SNAT。下列 UCI模板采用示例子网；执行前必须统一替换为任务1的实际参数。先查询，确认 `lan`区域唯一：

```sh
uci show firewall
fw4 check
```

在 guest执行模板，若无法找到 LAN区域立即停止而不是新建重复区域：

```sh
LAN_ZONE="$(uci show firewall | sed -n "s/^\(firewall\.[^.]*\)\.name='lan'$/\1/p")"
[ -n "$LAN_ZONE" ] || exit 1
uci set "$LAN_ZONE.forward=ACCEPT"
uci set "$LAN_ZONE.masq=1"
uci -q delete "$LAN_ZONE.masq_src"
uci -q delete "$LAN_ZONE.masq_dest"
uci add_list "$LAN_ZONE.masq_src=192.168.50.0/24"
uci set 'firewall.@defaults[0].flow_offloading=0'
uci set 'firewall.@defaults[0].flow_offloading_hw=0'
uci commit firewall
fw4 check
```

`fw4 check`应无语法错误后才 `/etc/init.d/firewall restart`。如果区域名、输出或网络不符，先回控制台恢复备份，不把命令连续强行执行。主案暂不运行 OpenClash，后续保持其 `bypass_gateway_compatible=0`。

- [ ] 写入 `/etc/sysctl.d/90-home-routing.conf`关闭 IPv4 redirect。以下接口名为 guest的 `br-lan`示例；实际不叫此名时替换最后两行。持久化后应用并读取实际值：

```conf
net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.send_redirects=0
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv4.conf.br-lan.send_redirects=0
net.ipv4.conf.br-lan.accept_redirects=0
```

```sh
sysctl -p /etc/sysctl.d/90-home-routing.conf
sysctl net.ipv4.ip_forward
sysctl net.ipv4.conf.all.send_redirects
sysctl net.ipv4.conf.all.accept_redirects
ip route
nft list ruleset
```

预期 IPv4转发为 `1`，关闭项为 `0`，默认路由经 Fusion，LAN出口有单套预期 masquerade；重启 guest后复查实际 LAN关闭项。若此版本未默认启转发，先查配置并明确持久化 `net.ipv4.ip_forward=1`，再重验。

- [ ] 让一台试点有线电脑暂用池外已查重的静态地址，网关/DNS均 `.2`；它不通过 DHCP取得此试点设置，其他终端仍指向 Fusion。
- [ ] 从试点电脑访问 Fusion/PVE/HA或存储的真实 IP，再测试普通域名和外网。查看 `nft`计数器；抓取 guest LAN上的对应外网会话，确认去往 Fusion的源是 `.2`、回包确实经过 `.2`。
- [ ] 试点电脑访问同网段 NAS；确认交换机内本地传输未绕 `.2`。用原电脑、原测点重复三次普通吞吐并对比基线。
- [ ] 记录并演示试点电脑把网关/DNS恢复 `.1`即回到原普通路径；结束后再设 `.2`继续试点。此阶段仍不开 OpenWrt DHCP。

**失败处理：** 试点电脑恢复原自动地址或 `.1`，修复新 VM再试；不得全屋切换。

## 任务 5：安装并验证规则服务（约 60–120 分钟）

**输入：** 已通过普通转发试点的 VM。**输出：** 单设备规则、DNS、UDP和本地发现验证；“普通模式”恢复步骤。**退出条件：** 配置可校验，普通和指定流量各走预期路径。

- [ ] 对尚未提供 DHCP的 VM做一次关机备份。维护窗口内通过 PVE控制台操作依赖包；不要在失去 DNS就无法连接的远程单通道下更换解析组件。
- [ ] 核对版本和包管理。此候选使用 `apk`，按对应发行版仓库安装；**不混入其他版本内核模块和旧式包**。先只读检查：

```sh
cat /etc/openwrt_release
apk --version
apk info dnsmasq
apk info dnsmasq-full
```

- [ ] 保存当前 `/etc/config/dhcp`。若装有普通 `dnsmasq`，先确认当前版本 `dnsmasq-full`可下载及依赖可满足，下载所需包到本地缓存；用 `apk del --simulate dnsmasq`查看移除影响。只在替代包齐备、控制台可恢复且 OpenWrt DHCP仍关闭时，按该版本 APK冲突处理方式停旧解析、移除冲突包、安装 `dnsmasq-full`，保留/恢复已备份配置。不要使用全局强制覆盖绕过文件归属冲突。如果替换失败，恢复任务4备份，不继续切换。
- [ ] 按插件发行页安装 fw4所需依赖；本候选清单如下，执行前对照所用发行版仓库可用性：

```sh
apk update
apk add bash dnsmasq-full curl ca-bundle ip-full ruby ruby-yaml kmod-tun kmod-inet-diag unzip kmod-nft-tproxy luci-compat luci luci-base
```

安装本地 APK使用该版本支持的本地文件参数。第三方包如无 OpenWrt官方仓库信任签名，仅对已核来源和哈希的**该本地文件**使用安装器要求的显式信任选项，不修改系统全局信任策略。先看 `apk add --help`，记录实际命令和结果，不给一个动态网络安装脚本永久执行权限。

- [ ] 在 LuCI找到新插件；通过它的本地上传/引擎管理入口安装已核验的 amd64 v1引擎，不启用自动软件更新。记录它实际存放的可执行文件和生成配置路径；用实际文件执行 `-v`与 `-t -f`，后者必须返回配置有效。错误即保持服务停用并修复，不让它带错启动。
- [ ] 选择候选 `fake-ip-mix`和 `system`协议栈；启用 IPv4规则接管与插件 DNS接入，关闭插件的 `bypass_gateway_compatible`，保持任务4唯一标准 SNAT。核对 `uci show openclash`和生成配置；不要只根据 UI翻译猜测已保存的值。首期不另开手工 TUN自动路由、额外重定向脚本和第二套 DNS插件。
- [ ] 在私有配置区录入实际节点及必要域名解析上游，创建 `RULE-OUT`组，不含 DIRECT后备；先用两个实际可测试站点分别验证普通和指定规则。公开验收记录只记脱敏名称 `site-direct-01`、`site-rule-01`，不贴节点资料。
- [ ] 规则次序按设计第7.3节；排除本地域名和需要真实地址的服务，不把 mDNS送进引擎。修改后重新执行引擎配置校验，再从单设备试点开启规则。
- [ ] 使用试点电脑检查 DNS来自 `.2`；本地域名返回真实家庭地址，指定站点命中指定组，普通站点命中 DIRECT。使用插件会话/命中记录以及选定站点的可观测结果共同验证；“网页能开”本身不能证明出口正确。
- [ ] 检查启动解析：重启规则服务、再重启 VM，各做一次；验证节点域名和公共域名不会依赖自身尚未建立的规则出口。Fusion和 PVE仍能独立解析和管理。
- [ ] 测试 UDP、语音/游戏、QUIC及一段视频；记录节点 UDP支持和实际规则，出现问题只修改相关服务规则。游戏 NAT类型和自动端口映射另记结果；不默认 UPnP跨单臂 SNAT仍有效，不同时全局开放两层映射。
- [ ] 在现有普通 DHCP仍运行时，让试点电脑有线/无线分别试一次，确认 AP桥接不另加路由；本地 NAS、AirPlay、家庭发现和已有智能控制仍正常。
- [ ] 在插件支持的接管范围内验证普通 TCP/UDP 53处理，检查写死 DNS、应用加密解析、私有中继和客户端独立规则设置。逐设备记需配合修改的项；有未核验的绕行路径就不能标注全屋覆盖完成。

### 在此阶段制作并实测“普通模式”

此模式用于规则服务坏了但 OpenWrt还活着，地址仍由 `.2`提供：

1. 保存当前有效私有配置；用插件自身停用入口移除它的接管/路由/DNS重定向，而不是只杀引擎进程。
2. 确认任务4的标准 fw4 SNAT与转发还在；`fw4 check`及规则计数正常。检查 `nft list ruleset`与策略路由没有失效的 TUN残留。
3. 把 dnsmasq恢复成可直接解析普通域名的上游；示例把普通上游固定为 Fusion，**执行前将 `.1`替换为实际值并核对 `@dnsmasq[0]`是本实例**：

```sh
uci set dhcp.@dnsmasq[0].noresolv='1'
uci -q delete dhcp.@dnsmasq[0].server
uci add_list dhcp.@dnsmasq[0].server='192.168.50.1'
uci commit dhcp
/etc/init.d/dnsmasq restart
```

4. 清除试点电脑/浏览器的合成解析缓存，重连网络；必要时重启该终端。真实地址访问和新解析的普通站点都应可用，指定站点规则此时明确暂停。
5. 验证 `.2`仍可分地址的配置保留，但**此时不要提前启用 DHCP**；记录各配置差异。恢复规则服务后重验 DNS接管和网站命中，再保存“规则模式”和“普通模式”两份可读配置/恢复记录。

如果插件的停用不能可靠清理接管，或普通模式复测失败，先解决后再切全屋。不得把未验证的“服务停了就自动直接访问”写进应急承诺。

## 任务 6：准备全屋地址服务迁移并演练故障（约 45–90 分钟，另加租约等待）

**输入：** 单设备规则试点通过。**输出：** 可迁移的地址映射、短租期、静态设备清单和恢复实测。**退出条件：** 没有未处理的旧租约冲突，管理员不依赖 `.2`恢复。

- [ ] 在 Fusion当前地址服务将迁移期租约改为 `10min`；**原来已取得长租约的设备不会立刻变成短租约**。等原最大租期过去，或逐台主动续租并读取新租期；离线后可能带旧地址醒来的设备列为迁移对象。
- [ ] 导出 Fusion所有活动租约和固定保留；在仍关闭 DHCP的 OpenWrt内建立对应 MAC→IP保留及本地名称。为仍可能持有旧租约的地址建立临时保留/占用排除，避免新服务把它分给另一台设备。只看新服务“池为空”不能说明旧地址已释放。
- [ ] 若某固件不能安全导入原保留，逐台建映射并核对；无法确定旧租约有效范围时，保持 Fusion服务，等待完整最大租期和设备确认后再切。不要两个服务同时开着“慢慢迁移”。
- [ ] OpenWrt预设池 `.100–.199`、掩码 `/24`、租期 `10m`，下发网关和 DNS均 `.2`。排除实际管理 IP、静态地址和已保留租约；保留 `home.arpa`映射。先保存配置，LAN的 `ignore=1`仍保持。

在新建的 `dhcp.lan` 段可用且实际地址已整体替换的前提下，示例参数可通过下列 UCI 预先保存；DHCP继续关闭，直到正式切换：

```sh
uci set dhcp.lan.start='100'
uci set dhcp.lan.limit='100'
uci set dhcp.lan.leasetime='10m'
uci set dhcp.lan.ignore='1'
uci commit dhcp
```

另用 `uci add dhcp domain` 建立固定 IP 的 `home.arpa` 主机映射，按已核对的 MAC/address/name 录入；若既有主机名采用保留租约，则通过对应 `dhcp.host` 段记录。正式切换前在 LuCI 或 `uci show dhcp` 读回每条映射，确认它们落在动态池外或已正确保留。切换时单独将 `dhcp.lan.ignore='0'` 保存并重启地址服务，随后立即验证唯一应答者；如果本机所用 UCI 不支持某选项，不猜测替代键。

- [ ] 在尚未正式切换的单设备试点环境检查公网 IPv6默认路由。经确认首期不需要公网 IPv6时，安排在维护窗口使 Fusion不向家庭 LAN发布公网默认路由；不要删除本地 IPv6/Thread路由或全局禁 RA。终端重新获取路由后查验，保证本地协议仍工作。若现网需要公网 IPv6，留在试点并另外设计双栈。
- [ ] 核对 PVE网关/DNS直达 Fusion，OpenWrt自身上游直达 Fusion；PVE本地磁盘/管理不依赖 OpenWrt、存储 VM或规则域名解析。
- [ ] 实测规则服务停用 → 普通模式 → 规则模式；计时并记录，不能只按纸面推断。
- [ ] 停止新 OpenWrt VM，试点设备应失去经 `.2`的外网；应急笔记本改为直达 Fusion，实际访问 `.1`及 `.3`、从 PVE重新启动该 VM。此时 Fusion DHCP仍在，其他家人设备不受这个试点停机影响。
- [ ] 记录全屋回退界面入口、Fusion普通 DHCP参数、OpenWrt停止/禁止重启方式、终端续租方法。**完整全屋 DHCP回退实测安排在任务7**，本阶段不把试点恢复记成全屋恢复通过。
- [ ] 安排维护窗口，准备逐设备清单和管理电脑；需要把静态设备的网关、DNS逐个改为 `.2`，不能只改动态租约。

## 任务 7：全屋切换与完整回退演练（约 60–120 分钟）

**输入：** 前六任务通过；唯一地址服务、IPv6及旧租约已处理。**输出：** 全屋覆盖、完整回退实测。**退出条件：** 每台终端通过网关/DNS核对与使用验证。

- [ ] 切换前再次导出 Fusion配置及租约，确认 OpenWrt DHCP仍关闭；管理笔记本使用直达 `.1`的应急静态方案，保持 PVE控制台可用。
- [ ] **先关闭 Fusion该 LAN的 DHCP**，确认已保存；此时 OpenWrt仍关闭，允许短暂没有 DHCP。再开启 OpenWrt该 LAN的 DHCP。不要把顺序反过来。
- [ ] 以新连接的测试电脑抓取 DHCP交互或查看租约详细信息，确认只有 OpenWrt答复，网关/DNS均 `.2`、租期10分钟、无地址冲突。OpenWrt租约表应出现该电脑。
- [ ] 电脑主动续租/手机重新连接家庭 SSID；电视、中枢、网关等逐台重连或通过其支持的方法更新租约。Windows电脑可在本地用 `ipconfig /release`、`ipconfig /renew`、`ipconfig /all`，不要在唯一远程管理连接中使用 release；其他系统按各自网络设置操作。
- [ ] 修改所有手工静态终端及来宾的网关/DNS为 `.2`；保留 Fusion/PVE/OpenWrt上游例外。静态映射与随机 MAC重新核对，逐台在验收清单记录，而不是只看活动连接总数。
- [ ] 每个房间分别检查有线、AP下联及 Wi-Fi设备；实际启用的不同频段均获得同一规则策略。次卧没有 AP时验证大厅覆盖；旧临时 AP如启用，必须桥接且 DHCP关闭。
- [ ] 每类设备验证普通网站/服务，支持浏览的设备再验证指定网站；网关/摄像机等无法浏览的设备，使用对应云功能、规则会话记录及解析结果验证其经过 `.2`。本地 Zigbee通过所属网关验收，不编造传感器独立上网测试。
- [ ] 同时检查 DNS权威/本地域名、家庭发现、AirPlay、影音、HA/Apple Home、M200/M1S；Matter/Thread若现场已有，则测本地控制与相关 IPv6路由。尚未购入设备一律 `not_run`，不能作为已实现全屋覆盖的证据。
- [ ] 清理旧默认路由和解析缓存后，查验终端没有绕行的公网 IPv6默认路由；写死 DNS/加密解析/独立客户端按任务5结论逐台处理。
- [ ] **执行一次完整人工回退演练**：按应急单先关 OpenWrt DHCP或停 VM并阻止自动拉起，再启 Fusion唯一 DHCP；逐台续租、静态设备改 `.1`、清缓存；记录从故障到各类设备恢复的实际时间。回退期间明确暂停网站规则。
- [ ] 回退通过后，再按本任务相同顺序切回：Fusion DHCP关 → OpenWrt DHCP开 → 续租/静态设备恢复 `.2` → 规则与本地控制复验。不能把恢复 Fusion的状态误记成全屋规则已启用。

**失败处理：** 任一普遍通信故障、地址冲突、失去管理通道、IPv6绕行或不可接受的性能下降，按应急单恢复 Fusion普通网络；保留日志和证据，不通过批量关防火墙推进。

## 任务 8：72小时观察、备份和交付（观察之外约 45–60 分钟）

**输入：** 全屋切换及回退通过。**输出：** 稳定版本、外部备份、最终参数及实测状态。**退出条件：** 验收记录完整，故障恢复有人能按单操作。

- [ ] 在原电脑和测点对比普通路径：三次下载中位数至少为基线85%，空闲外网延迟中位数增加不超过5ms；连续30分钟无持续丢包、内存耗尽或热降频。节点路径按实际站点表现另记，不给千兆承诺。
- [ ] 同时进行一段 J3455存储访问，观察外网、CPU、网卡、温度和磁盘等待；测试同交换机 Mac↔独立 NAS的本地路径（NAS未购则保持 `not_run`）。瓶颈与是否换网卡分开判定。
- [ ] 在72小时内覆盖睡眠唤醒、手机漫游、电视播放、语音/游戏、订阅节点刷新、规则服务重启和 VM重启；时间从实际切全屋起算。没有完成72小时就不能提前勾选。
- [ ] 在可接受的维护窗口验证宿主正常重启时 OpenWrt先启动、其他依赖来宾后起，正常关机顺序相反；不要拔电制造存储损坏。确认启动盘不依赖存储 VM、规则节点域名能独立解析。
- [ ] 通过后把唯一 OpenWrt DHCP租期由10分钟调为12小时；记住此后紧急恢复需要客户端主动续租，不能期待下一次自动续租立即发生。
- [ ] 对 OpenWrt VM做可恢复备份，保存两种模式、DHCP保留、本地 DNS、fw4/sysctl及版本清单，复制到 J3455之外；读回核对。快照仅是辅助，不代替这份备份。
- [ ] 备份旧规则容器后停止重叠的规则/接管功能、取消对应自启动；检查没有同时运行的 DNS/规则接管。保留存储 VM，不删除原备份以冒充迁移成功。
- [ ] 在验收表填实际版本、时间、证据和未通过项；仅在真实完成后把 `not_run`改为 `passed`或 `failed`。将最终普通模式步骤和完整回退方法保存离线，并实际由另一位家人按单找到管理入口。
- [ ] 更新基础设施台账与当前拓扑的实施状态；只提交脱敏记录，不提交下载二进制、节点资料或设备配置原件。版本变更记录中区分“方案已写”和“设备已部署”。

## 实施自检对照

| 设计要求 | 负责任务 | 必须取得的证据 |
|---|---|---|
| 资源/数据保留、单臂接线 | 1、3 | 宿主盘点、仅新 VM磁盘、原存储可用 |
| 版本和完整 VM选择 | 2、3、5 | 校验值、实际版本、文件系统大小、引擎配置校验 |
| 转发/SNAT/redirect/offload | 4、5 | nft规则、回包路径、重启后 sysctl |
| DNS和规则顺序、UDP | 5 | 普通与指定命中、本地域名、UDP测试、服务重启 |
| 全设备及唯一地址服务 | 6、7 | 租约冲突处理、唯一服务端、静态设备逐台核对 |
| 公网与本地 IPv6区分 | 1、6、7 | 终端路由、本地发现/Thread测试；未购项保持未运行 |
| 两种故障恢复 | 5、6、7 | 普通模式及完整 DHCP回退的实际用时 |
| 性能、稳定和备份 | 8 | 同条件测量、72h记录、外部备份读回 |

本轮文档交付只做 Markdown/链接/用语/一致性静态核对，不运行软件单元测试，也不把静态检查替代任何一项现场验收。
