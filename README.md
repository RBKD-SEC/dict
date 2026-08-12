# Dict
渗透测试与安全评估常用字典集合，针对中国互联网环境优化。
## 适用场景
- Web 目录扫描 (dirsearch / ffuf / gobuster)
- 账号密码爆破 (hydra / medusa / burp)
- API 端点探测
- 配置文件与备份文件发现
- 国产 CMS / OA / 云服务的安全评估
## 快速开始（实战首选）
每个分类目录下的 `top*.txt` 是按实战高频度排序的综合性字典，**直接拿来用**：
```bash
# 目录扫描 — 最常用100个路径
ffuf -u http://target.com/FUZZ -w path/top100.txt
# 目录扫描 — 最常用1000个路径（更全面）
ffuf -u http://target.com/FUZZ -w path/top1000.txt
# 账号爆破 — 最常用100个用户名 + 100个密码
hydra -L username/top100.txt -P password/top100.txt ssh://target.com
# 账号爆破 — 常用500个（更全但慢）
hydra -L username/top500.txt -P password/top500.txt ssh://target.com
```
## 目录结构
```
dict/
|-- username/               # 用户名字典
|-- password/               # 密码字典
|-- path/                   # 目录/路径字典
|-- api/                    # API 端点字典
|-- backup/                 # 备份文件字典
|-- capabilities/           # v1 规范化能力目录（ Ticket 04 新增）
|-- scripts/                # 生成器与门禁脚本
|-- tests/fixtures/         # 测试夹具
|-- LICENSE / NOTICE        # Apache-2.0 与来源声明
└── README.md
```

## Capability catalog & release

本仓库是 repository-orchestration-v2 的 `dictionary` 能力仓。发布门禁：

- 每个 `.txt` 文件对应一个稳定能力 ID，格式为 `<dir>-<basename>`（如 `username-top100`）。
- `capabilities/catalog-v1.json` 仅包含 provenance 审批为 `accepted` 的资产；当前全部资产处于 `held` 待审状态，因此 catalog 为空。
- 发布候选通过 `scripts/stage_release.py --calver YYYY.MM.DD.N` 生成，包含 catalog、schema、LICENSE、NOTICE、provenance 与按 ID 获取的字典。
- 消费者用 `scripts/fetch_dict.py --release releases/YYYY.MM.DD.N --id username-top100 --output /tmp/out.txt` 按能力 ID 获取字典。

本地门禁：

```bash
python scripts/validate_dict.py
python scripts/secret_scan.py --tree .
python scripts/test_dict.py
python scripts/generate_catalog.py --write
python scripts/stage_release.py --calver 2026.08.10.1
shasum -a 256 -c releases/2026.08.10.1/SHA256SUMS
```
## 使用建议
| 场景 | 推荐字典 | 说明 |
|------|----------|------|
| 快速侦察 | `path/top100.txt` | 最快的路径发现 |
| 标准扫描 | `path/top500.txt` | 平衡速度与覆盖 |
| 深度扫描 | `path/top1000.txt` | 最全面的路径覆盖 |
| 通用爆破 | `username/top100.txt` + `password/top100.txt` | 最快爆破 |
| 深度爆破 | `username/top500.txt` + `password/top500.txt` | 更全面 |
| 定向测试 | `username/china-systems.txt` + `password/china-default.txt` | 针对国产系统 |
| SpringBoot | `path/springboot.txt` | actuator 等端点 |
| 国产OA | `path/china-systems.txt` | 泛微/致远/通达等 |
## 使用示例
### 目录扫描
```bash
# 最常用 — 直接扫 top100
ffuf -u http://target.com/FUZZ -w path/top100.txt
# 更全面 — 扫 top1000
ffuf -u http://target.com/FUZZ -w path/top1000.txt
# 针对国产 CMS
ffuf -u http://target.com/FUZZ -w path/china-systems.txt
# 使用 dirsearch 扫描后台
python dirsearch.py -u http://target.com -w path/admin-panel.txt
# 组合多个分类字典
cat path/admin-panel.txt path/china-systems.txt > admin-paths.txt
ffuf -u http://target.com/FUZZ -w admin-paths.txt
```
### 账号爆破
```bash
# 最快 — top100
hydra -L username/top100.txt -P password/top100.txt ssh://target.com
# 深度 — top500
hydra -L username/top500.txt -P password/top500.txt ssh://target.com
# 针对国产系统
hydra -L username/china-systems.txt -P password/china-default.txt ssh://target.com
```
### 备份文件扫描
```bash
# 使用 gobuster 扫描备份文件
gobuster dir -u http://target.com -w backup/patterns.txt -x php,zip,sql
```
## 中国特色覆盖
- **CMS/框架**: ThinkPHP, DedeCMS(织梦), Discuz!, 帝国CMS, PHPCMS, ECShop, FastAdmin, JeecgBoot
- **OA 系统**: 泛微 e-cology, 致远 OA, 蓝凌 OA, 通达 OA, 帆软报表
- **云服务**: 阿里云, 腾讯云, 华为云, 百度云, 七牛云, 又拍云
- **网络设备**: 华为, H3C, 锐捷, 深信服, TP-Link, 海康威视, 大华
- **安全厂商**: 奇安信, 启明星辰, 天融信, 绿盟, 安恒, 360
- **企业应用**: 用友 NC/U8, 金蝶 K3/EAS, 钉钉, 企业微信, 飞书
- **运营商/金融**: 中国移动, 中国联通, 中国电信, 各大银行, 支付宝, 微信支付
## top 字典的排序逻辑
综合性 `top*` 字典的排序基于以下优先级：
1. **实战出现频率** — 渗透测试中实际遇到的比例
2. **通用性** — 覆盖系统/框架的数量
3. **中国特色** — 国内互联网环境中更常见的条目靠前
4. **危害性** — 命中后信息泄露/权限获取的潜在价值
## 更新日志
| 日期 | 内容 |
|------|------|
| 2026-05-12 | 重组目录结构，新增 top100/top500/top1000 综合性字典，补充国产系统字典 |
## 贡献指南
欢迎提交 PR 补充字典内容。新增条目请遵循以下原则：
1. **top 字典** — 只添加高频/高实战价值的条目，会定期根据反馈调整排序
2. **分类字典** — 按场景放到对应目录，同一文件内不重复
3. 补充国产系统时请注明来源（厂商文档/实际渗透测试经验）
4. 密码条目优先补充实际出现过的高频弱密码
## 免责声明
本字典仅供授权的安全测试和渗透测试使用。使用本工具进行未经授权的访问属于违法行为，由使用者自行承担法律责任。
