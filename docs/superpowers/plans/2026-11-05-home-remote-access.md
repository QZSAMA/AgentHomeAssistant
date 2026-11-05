# 家庭私有网络远程接入实施计划

> **For agentic workers:** 后续实施使用 `executing-plans` 技能按阶段执行并核验证据。本次交付仅为详细方案和远程仓库文档；下方真实设备步骤尚未执行，不能将提交成功当作部署成功。

**Goal:** 在家庭无公网入站 IPv4/IPv6 的前提下，统一访问群晖、VS Code Remote-SSH、Jupyter 和其他私有服务，并验证可用于日常开发的连接质量。

**Architecture:** 开发机直接加入 Tailscale；J3455 的独立 Linux VM 为其他设备提供按需子网路由。业务优先直连，必要时使用国内 Peer Relay，DERP 仅在其后提供连接协商/应急路径。Fusion 保留家庭基础网络，原美国出口独立使用。

**Tech Stack:** Proxmox 上的独立 Debian Linux VM；Tailscale 官方稳定客户端（资料核验候选 1.104.5，Peer Relay 参与端最低 1.86）；OpenSSH、VS Code Remote-SSH、JupyterLab；可选国内 Linux 公网节点。

设计：[详细架构与取舍](../specs/2026-11-05-home-remote-access-design.md)。现场证据：[验收单](../../validation/home-remote-access.md)。

## Global Constraints

- 家庭保持同一 LAN；Fusion 继续承担主路由、唯一 DHCP、普通 DNS。不得按此计划迁移全屋网关、DHCP、DNS或添加 VLAN。
- 不重装 J3455，不修改现有 NAS/HA/代理 VM 的配置，不将远程接入部署到规则代理 VM 内。
- 家庭接入 VM 不开启 exit node，不接受/发布默认路由；保留子网 SNAT，首期只发布 NAS 的 `/32`。
- 不以美国节点转发中国家庭业务；公共 DERP 应急回退若发生，单独标记路径和体验，不能算作国内中继验收通过。
- 示例 IP、域名、账户必须映射为实值。它们是有说明的配置参数，不表示已分配、已注册或已验证。
- 账号凭据、auth key、SSH 私钥、Jupyter token、真实节点状态不入 Git。文档中不设置任何真实密码。
- 本次不部署真实设备、不购买服务器、不修改云防火墙。后续实际执行须已有对应环境与操作授权。

## 文件与接口

| 位置 | 责任 |
|---|---|
| `docs/superpowers/specs/2026-11-05-home-remote-access-design.md` | 架构、设备职责、访问路径、限制、官方来源 |
| 本计划 | 操作顺序、配置示例、预期结果、停止和回退条件 |
| `docs/validation/home-remote-access.md` | 私有参数的脱敏登记、逐项实机结果、性能与恢复证据 |
| Tailnet 管理控制台 | 身份、设备、标签、grants、路由批准、可选 DERP map |
| 接入 VM `/etc/sysctl.d/90-home-access.conf` | 仅该 VM 的 IP forwarding |
| 外部电脑 `~/.ssh/config` | 开发机 SSH 别名和本地转发；Windows 对应用户 `.ssh/config` |
| 可选服务器 `/etc/systemd/system/derper.service` | 可选 DERP PoC 的自启和恢复，不属于初期必建项 |

## 任务 1：盘点与参数冻结

**输入：** 家庭设备、一个外部笔记本、实际可用的外部网络。**输出：** 可回退基线和真实参数。**退出条件：** 确认现网路径、J3455 资源和控制台恢复方式。

- [ ] 记录现有主路由型号、固件、LAN、DHCP/DNS 提供者、NAS 地址/HTTPS 端口、开发机系统/SSH 用户。Fusion 未到货时记录实际主路由，不虚构安装状态。
- [ ] 在 J3455 本地或已授权管理连接只读检查：`pveversion -v`、`qm list`、`pct list`、`free -h`、`pvesm status`、`ip -br address`、`ip route`。确认给新 VM 的资源不会挤占现有 NAS/HA/代理。
- [ ] 记录现有家庭服务、普通上网和 LAN 访问基线，确认可通过本地 PVE 控制台恢复新 VM。保存现有主路由配置备份。
- [ ] 在外部终端检查当前 VPN、代理/TUN、路由表；确认工作网络允许安装/使用所需客户端。遇到不允许使用的网络，只记录该网络不支持，不绕过其访问管理。
- [ ] 核对以下规划示例，并在私有运行记录中填入实际值；仓库仅保留脱敏结果。

| 参数 | 规划示例 | 用途 |
|---|---|---|
| `LAN_CIDR` | `192.168.50.0/24` | 当前家庭网段；无须为示例迁移现网 |
| `FUSION_IP` | `192.168.50.1` | 实际家庭网关和普通 DNS |
| `ACCESS_IP` | `192.168.50.4` | 新 VM 经 DHCP 保留的地址，先查重 |
| `NAS_IP` | `192.168.50.30` | 首期唯一广告 `/32` |
| `DEV_NAME` | `home-dev` | 开发机在 tailnet 的唯一名称 |
| `DEV_USER` | `dev` | 开发机上真实存在的普通 SSH 用户 |
| `OWNER_LOGIN` | `owner@example.com` | 替换为真实 tailnet 登录身份；示例邮箱不可直接提交 |
| `RELAY_PUBLIC_IP` | `203.0.113.10` | 文档保留地址，必须替换为所购国内节点公网地址 |
| `DERP_FQDN` | `derp-cn.example.com` | 仅可选 DERP 使用；必须替换为自有域名 |

没有 VM 资源时，先完成开发机直接接入，不停掉现有 NAS 腾资源。尚无云节点时，可以完成任务 2–4；任务 5、6 保持未运行。

## 任务 2：建立最小 tailnet 与访问策略

**输入：** 真实个人身份和开发机。**输出：** 一台外部设备可通过组网地址 SSH 到开发机。**退出条件：** 控制登录可用，权限按预期，实际 SSH 成功。

- [ ] 由用户自己的身份创建/选用 tailnet，启用账户多因素认证。若已有 tailnet，先导出原策略和现用标签；不得覆盖无关规则。
- [ ] 从 [Tailscale 官方下载](https://tailscale.com/download)安装适合平台的稳定客户端，记录 `tailscale version`。Linux 可下载官方安装脚本后审阅并执行；不要混用不明套件源。

```sh
curl -fsSL https://tailscale.com/install.sh -o /tmp/tailscale-install.sh
less /tmp/tailscale-install.sh
sudo sh /tmp/tailscale-install.sh
tailscale version
```

- [ ] 在控制台设置下面的最小策略。先替换账户和 NAS 地址；已有策略按项合并。去除或收窄覆盖这些目标的默认全通配 allow 规则，grants 是累加允许，不存在“后面的窄规则覆盖前面的宽规则”。

```json
{
  "groups": {
    "group:home-admins": ["owner@example.com"]
  },
  "tagOwners": {
    "tag:home-dev": ["group:home-admins"],
    "tag:home-access": ["group:home-admins"],
    "tag:home-nas": ["group:home-admins"],
    "tag:cn-relay": ["group:home-admins"]
  },
  "hosts": {
    "nas-lan": "192.168.50.30"
  },
  "grants": [
    {
      "src": ["group:home-admins"],
      "dst": ["tag:home-dev", "tag:home-access", "tag:cn-relay"],
      "ip": ["tcp:22"]
    },
    {
      "src": ["group:home-admins"],
      "dst": ["nas-lan", "tag:home-nas"],
      "ip": ["tcp:5001", "tcp:445"]
    },
    {
      "src": ["group:home-admins"],
      "dst": ["tag:home-dev", "tag:home-access", "nas-lan"],
      "ip": ["icmp:*"]
    },
    {
      "src": ["tag:home-dev", "tag:home-access", "tag:home-nas"],
      "dst": ["tag:cn-relay"],
      "app": {"tailscale.com/cap/relay": []}
    }
  ],
  "tests": [
    {
      "src": "group:home-admins",
      "proto": "tcp",
      "accept": ["tag:home-dev:22", "nas-lan:5001", "nas-lan:445"],
      "deny": ["tag:home-dev:8888", "nas-lan:22", "192.168.50.1:443", "192.168.50.3:8006"]
    },
    {
      "src": "tag:cn-relay",
      "proto": "tcp",
      "deny": ["tag:home-dev:22", "nas-lan:5001", "nas-lan:445"]
    }
  ]
}
```

示例默认 DSM HTTPS 是 5001；若现网不同，允许规则与 tests 同步修改。relay capability 的 `src` 是允许借助该中继被访问的家庭节点，不是给所有移动设备配置全局出口。使用此 capability 不需要再对中继新增全端口网络 grant。[设计 S1、S5]

- [ ] 保存前让控制台完成策略语法及 tests 校验。未建立节点时可先验证语法，节点注册后再重跑策略和实际拒绝测试。离线 JSON 解析不能替代控制台校验。
- [ ] 开发机登录并标记，外部笔记本使用自己的个人身份登录、**不打服务器 tag**。Linux 示例如下；macOS/Windows 使用其官方客户端的等价设置。

```sh
sudo tailscale up --hostname=home-dev --advertise-tags=tag:home-dev
tailscale ip -4
tailscale status
tailscale netcheck
```

- [ ] 在开发机启用系统 OpenSSH，安装个人公钥并验证主机指纹。Linux 检查 SSH 服务和防火墙；macOS 使用“远程登录”；Windows 按 OpenSSH Server 配置。首期不使用 `tailscale up --ssh`。
- [ ] 外部笔记本开启 MagicDNS，执行 `tailscale ping home-dev`，然后 `ssh dev@home-dev`。短名称冲突时使用控制台显示的完整 MagicDNS 名称或实际 Tailscale IP。
- [ ] 检查 `tailscale status` 的实际 `direct`/`relay` 状态。第一次探测经 DERP 再升级直连属可能情况，等待稳定后记录；不要凭一次 ping 宣布线路质量。

停止条件：无法完成控制登录、节点地址冲突、SSH 主机身份不符或授权 tests 不通过。保留现网，定位问题后再继续。

## 任务 3：创建家庭接入 VM，只接入一台 NAS

**输入：** 任务 1 参数和任务 2 的 tailnet。**输出：** 外部通过 NAS `/32` 私有路由访问 HTTPS/SMB。**退出条件：** NAS 可达，普通家庭网络和开发机直接接入不受 VM 停机影响。

- [ ] 在 Proxmox 新建独立 Debian stable VM，建议 1 vCPU、1GiB RAM、8GiB 系统盘、VirtIO 单网卡接现有 LAN 桥；镜像从官方获取并校验。不要桥接 WAN、不修改物理桥、不在 VM 安装 DHCP/RA 服务。
- [ ] 在家庭主路由为该 VM 固定 MAC 设置 DHCP 保留地址，例如 `.4`；网关/DNS 指向实际 Fusion。VM 内用 `ip route` 和 `resolvectl status` 或系统解析配置确认不依赖美国代理/规则 VM。
- [ ] 在新 VM 安装 Tailscale，按服务器角色注册，然后只开启 IPv4 子网转发；本阶段只广告 IPv4 `/32`，无需改动家庭 IPv6。

```sh
sudo tailscale up --hostname=home-access --advertise-tags=tag:home-access
printf '%s\n' 'net.ipv4.ip_forward = 1' | sudo tee /etc/sysctl.d/90-home-access.conf
sudo sysctl -p /etc/sysctl.d/90-home-access.conf
sudo tailscale set --advertise-routes=192.168.50.30/32
sysctl net.ipv4.ip_forward
tailscale status
```

- [ ] 保持 Tailscale 默认子网 SNAT 和 netfilter 管理。若使用发行版防火墙，保留默认拒绝转发，仅允许 `tailscale0` 到指定 NAS 和已建立连接的返回；确认规则顺序与 Tailscale 管理规则兼容。不要整体停用防火墙来“解决连通”。
- [ ] 在控制台批准 `home-access` 广告的 NAS `/32`。该阶段不配自动批准、不广告整个 `/24`，也不发布 `0.0.0.0/0`。
- [ ] 外部 Linux 客户端执行下列命令接受子网路由；Windows/macOS/iOS/Android 通常自动接受，仍需在实际版本检查。**不要在接入 VM 上为了此步骤开启 `--accept-routes`。**

```sh
sudo tailscale set --accept-routes=true
```

- [ ] NAS 防火墙允许接入 VM 的实际 LAN 地址访问所需 HTTPS/SMB 端口，并保留现有本地访问规则。通过 SNAT 后 NAS 看到 VM 来源，不能只放行 `100.64.0.0/10` 就认为足够。
- [ ] 外部打开 `https://192.168.50.30:5001`，核对证书及实际端口；用 SMB 客户端访问指定共享，验证登录、读取和允许的写入。未正确配置证书名称时先解决信任/名称问题，不把关闭证书校验当成正式方案。
- [ ] 停止该 VM 的 Tailscale 服务：NAS 子网访问应中断，独立开发机和其他家庭设备普通上网应继续；恢复服务后复测。此项只测试新 VM，不关闭 J3455 宿主。

需要更多服务时，追加明确的主机路由和 grants；修改 `--advertise-routes` 时传入**完整保留列表**，避免意外删掉原路由。

## 任务 4：配置开发工作流

**输入：** 可用的 `home-dev` SSH。**输出：** VS Code、Jupyter、一个本地 Web 服务均可远程使用。**退出条件：** 持续工作 30 分钟并完成断线恢复测试。

- [ ] 外部电脑安装 VS Code Remote-SSH，在用户 SSH 配置中增加别名；把 `dev` 换成实际系统账户，保留首次主机指纹校验。

```sshconfig
Host home-dev
    HostName home-dev
    User dev
    ServerAliveInterval 30
    ServerAliveCountMax 3
```

- [ ] 用 VS Code 的 “Remote-SSH: Connect to Host” 选择 `home-dev`，打开远端项目。确认终端进程、依赖安装与构建发生在开发机；记录 VS Code Server/扩展首次安装的下载条件。
- [ ] 在开发机现有项目环境运行 JupyterLab，保留默认 token 或已经配置的密码。以下命令不安装/升级项目依赖，只启动已安装的 JupyterLab。

```sh
jupyter lab --no-browser --ip=127.0.0.1 --port=8888
```

- [ ] 在外部电脑另开终端建立本地转发；本地端口被占用时把左侧 `8888` 改为 `18888`，浏览器同步使用新端口。

```sh
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:8888:127.0.0.1:8888 home-dev
```

- [ ] 浏览器访问 `http://127.0.0.1:8888`，用 Jupyter 提供的 token/密码登录，执行 cell、保存 notebook、重连内核。等价地可用 VS Code “Ports” 面板转发 8888。不要将 token URL 粘贴到公共仓库。
- [ ] 选一个现有开发 Web 服务，以 3000 为例进行转发；服务实际端口不同则两端同时修改。容器服务先确保容器端口已映射到开发机本机。

```sh
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:3000:127.0.0.1:3000 home-dev
```

- [ ] 验证页面和 WebSocket/HMR；本地浏览器请求 `localhost` API 时，该 API 端口也需转发，不能认为转发前端端口会自动转发全部后端。
- [ ] 验证睡眠、电源、重启和用户登录前的 Tailscale/SSH 可用性；长任务采用现有会话管理器或服务管理方式。macOS 磁盘加密解锁等条件按实际设备记录，不能承诺重启后无人值守必然恢复。

## 任务 5：按实测增加国内 Peer Relay

**进入条件：** 用户准备启用国内云节点，已获得购买/操作权限，或提供已有节点。**输出：** 不能直连的常用网络有经过验证的国内中继路径。

- [ ] 先按[验收单](../../validation/home-remote-access.md)测家宽、手机热点、常用办公网络。若直连已经满足需求，可保持本任务未运行；正式需要备用能力时再做短期节点试测。
- [ ] 选择候选国内节点，记录地域、运营商线路、公网带宽、流量计费和实际公网地址。通过云控制台保留恢复通道；初次管理使用云控制台或限定来源的 SSH。
- [ ] 在节点安装官方 Tailscale 并注册为 `cn-relay-1`、`tag:cn-relay`。检查参与连接的客户端版本 ≥1.86。
- [ ] 云安全组和主机防火墙放行 UDP 40000 的入站及返回流量；外部和家庭节点能访问这个公网 UDP 端口。Peer Relay 为移动网络提供服务时不按某个固定家庭公网 IP 限制来源，使用 tailnet capability 控制谁能分配 relay 连接。

```sh
sudo tailscale up --hostname=cn-relay-1 --advertise-tags=tag:cn-relay
sudo tailscale set --relay-server-port=40000 --relay-server-static-endpoints=203.0.113.10:40000
tailscale status
```

`203.0.113.10` 是不可直接使用的文档示例，必须换为实际地址；云侧存在端口映射时填写**外部可达**地址/端口。仅在服务器本地监听成功不足以证明公网可达。此节点不需要开启 Linux 三层转发来转发 Tailscale 的 peer-relay 封装，也不需要开启 exit node。

- [ ] 确认任务 2 的 relay grant 对家庭节点生效；它只授予中继分配能力，不授予中继主机读取 NAS 或登录开发机的网络权限。
- [ ] 在自然无法直连的测试网络产生 SSH/文件流量，检查两端 `tailscale status` 出现 `peer-relay`，并记录对应实际公网节点。若所有网络都直连，另在隔离测试终端针对已观察到的家庭直连公网端点临时阻断 UDP，保留到中继 UDP 40000 和控制/DERP 的连接；恢复规则后复测。
- [ ] 不全局封禁 UDP 来强测 Peer Relay，否则其自身也会被封禁。不要在唯一远程管理通道或家庭生产路由器上做阻断试验；记录并恢复测试规则。
- [ ] 测单向/并发吞吐、RTT、开发体验和中继重启。节点不达门槛时更换线路再测，不先买长期套餐。

Peer Relay 关闭命令：

```sh
sudo tailscale set --relay-server-port=""
```

## 任务 6：可选国内 DERP PoC

**进入条件：** 常用外部网络 UDP 受限，或公共 DERP 回退体验不可接受；接受当前官方 alpha 的维护和兼容性边界。**退出条件：** 冷启动、TCP 备用、证书续期及故障恢复均实测通过，否则保持试验状态。

- [ ] 按官方 [Custom DERP](https://tailscale.com/kb/1118/custom-derp-servers) 核验公网直接接入和端口要求。不要把普通 HTTP CDN、反向代理或不支持所需协议的负载均衡器放在前面；云公网/NAT 形态不满足官方要求时换节点或停止此项。
- [ ] 准备实际自有域名的 A 记录指向节点公网 IPv4；没有可用 IPv6 时不创建 AAAA。Peer Relay 本身不要求此域名。服务器允许 TCP 80/443、UDP 3478 和 ICMP；原 Peer Relay UDP 40000 可并存。
- [ ] 节点保持同一 tailnet 的 `tailscaled` 运行，用 `--verify-clients` 限定本 tailnet 客户端。使用匹配的稳定源版本编译 derper，记录源码 tag 与二进制散列；下面固定值是本轮核验候选，未来实施先复核稳定版本。

```sh
go install tailscale.com/cmd/derper@v1.104.5
sudo install -m 0755 "$(go env GOPATH)/bin/derper" /usr/local/bin/derper
sudo install -d -m 0700 /var/lib/derper
/usr/local/bin/derper --help
```

- [ ] 使用满足该版本 `go.mod` 要求的 Go 工具链。创建下面的 systemd 单元，将域名换为真实值；按官方默认 Let's Encrypt 流程申请证书，确认服务器可完成签发和续期。若 DNS/证书流程不满足，不用关闭 TLS 校验的方式推进。

```ini
[Unit]
Description=Home access DERP proof of concept
Wants=network-online.target
After=network-online.target tailscaled.service
Requires=tailscaled.service

[Service]
Type=simple
ExecStart=/usr/local/bin/derper --hostname=derp-cn.example.com --certdir=/var/lib/derper --verify-clients
Restart=on-failure
RestartSec=5
UMask=0077

[Install]
WantedBy=multi-user.target
```

- [ ] 保存为 `/etc/systemd/system/derper.service` 后启动并检查，不把“网页能打开”当作 DERP 转发已通过。

```sh
sudo systemctl daemon-reload
sudo systemctl enable --now derper
sudo systemctl status derper --no-pager
sudo journalctl -u derper -n 50 --no-pager
```

- [ ] 在**现有** tailnet policy 中合并以下 `derpMap` 对象，替换公网 IP 和域名。保留任务 2 的 grants/tests 等其他字段，不用此片段覆盖整个策略。

```json
{
  "derpMap": {
    "OmitDefaultRegions": false,
    "Regions": {
      "901": {
        "RegionID": 901,
        "RegionCode": "cn-home",
        "RegionName": "China home access PoC",
        "Nodes": [
          {
            "Name": "cn-home-1",
            "RegionID": 901,
            "HostName": "derp-cn.example.com",
            "IPv4": "203.0.113.10"
          }
        ]
      }
    }
  }
}
```

- [ ] 用 `tailscale netcheck` 确认新 region 可见；在可控的单个测试客户端暂时限制 UDP，保留 TCP 443/80、DNS 和控制登录通道，观察业务是否经 `cn-home` DERP。恢复网络后验证重新直连/Peer Relay。
- [ ] **加入 map 不保证节点一定选择它。** 记录实际 region 和延迟；默认公共 DERP 仍可能被选择。如果要排除所有公共 DERP，先验证至少一条自建恢复路径并保留控制台回退，再评估 `OmitDefaultRegions: true`；需要高可用时增加另一独立 region/节点。
- [ ] 验证证书续期、服务重启、`tailscaled` 停机后的客户端验证行为、跨网络冷启动和控制服务依赖。结果写入验收单，未通过不称为正式备用。

回退：先恢复上一个可用 DERP map，再停止可选 derper 服务；不得先删除唯一可用的连接协商路径。

## 任务 7：分流、体验、权限与故障验收

**输出：** [验收单](../../validation/home-remote-access.md)各项真实结果和证据。**退出条件：** 所有适用必测项通过；不适用项写原因，不能把未做的测试标成通过。

- [ ] 按服务逐项验收：SSH、VS Code、Jupyter、WebSocket/开发页面、NAS HTTPS、SMB、已选远程桌面工具。
- [ ] 每个常用外部网络测试实际路径、100 次 RTT、吞吐、30 分钟开发会话和并发上传。连通性与办公体验分别判定。
- [ ] 同时开启原美国代理/VPN，检查家庭服务的实际路由仍不绕美国；手机平台不支持双 VPN 时记录明确切换流程。
- [ ] 验证未授权身份/设备不能访问 NAS/开发机；个人管理员也不能访问未批准端口。tag 中继只能转发加密流量，不能直接登录家庭服务。
- [ ] 分别停止新接入 VM、国内 Peer Relay、可选 DERP，并从可控终端测试换网/重新登录/重启。故障恢复按验收表记录；不为了本轮验收擅自关闭整个家庭生产宿主。
- [ ] 确认普通上网、家庭设备相互访问、现有 DNS/DHCP 和本地 IPv6/Thread 行为与基线一致。
- [ ] 保存脱敏版本、策略、路由和恢复文档。客户端状态文件/私钥只做受控私有备份；不要克隆同一节点状态到两台同时在线设备。

## 任务 8：上线、回退与备选切换

- [ ] 验收通过后，记录适用网络和支持范围，配置新 VM 开机启动、Tailscale 自启和监控。监控至少覆盖节点在线、当前业务路径、证书到期（若使用 DERP）与实际交互可达。
- [ ] 客户端/服务器分批升级：先外部测试端和一个非关键节点，再家庭接入与中继；更新后复跑路径、SSH、Jupyter、NAS 和拒绝访问测试。
- [ ] 退役设备时从控制台撤销授权，删除其应用密钥；仅卸载客户端不代替服务端撤权。

整个方案回退按以下顺序进行：

1. 保存实际配置和故障记录，确保本地或云控制台仍可使用。
2. 在控制台取消新 NAS 子网路由批准，在 `home-access` 清空本方案的广告路由：`sudo tailscale set --advertise-routes=`。
3. 撤销本次新增节点和授权；已有 tailnet 只恢复本次涉及字段，不覆盖其他服务。
4. 删除或禁用新 VM 内的 forwarding 配置，按该 VM 是否还有其他合法用途恢复先前值；不修改全屋 Fusion/DHCP/AP。
5. 关闭已不使用的 Peer Relay/DERP 和对应云端口；云资源是否释放按实际资源管理决定，不误删已有共享服务器。
6. 验证家庭普通上网与现有服务仍正常；原美国出口保持原有用途。

若改用国内 WireGuard，单独生成实际密钥、服务器/家庭/client peer 配置与防火墙规则，再停用冲突的 Tailscale 路由。规划地址可用 `10.203.0.0/24`（先查重）：VPS `.1`、家庭 `.2`、外部 `.10`；VPS 的家庭 peer `AllowedIPs` 包含 `.2/32` 与 NAS `/32`，外部 peer 为 `.10/32`；家庭 peer 只将该 VPN 网段送 VPS，外部 peer 只将 VPN 网段和 NAS `/32` 送 VPS，NAT 后端启用 `PersistentKeepalive=25`。VPS 仅放行必要的 peer 间转发，家庭 VM 对获准 NAS 访问做限定 SNAT。

WireGuard 备选尚未生成真实配置或验收；不与主案同时广告相同目标，不配置全局默认出口，也不声称其能够解决完全禁止 UDP 的外部网络。
