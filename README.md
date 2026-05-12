# Dict

渗透测试与安全评估常用字典集合，针对中国互联网环境优化。

## 适用场景

- Web 目录扫描 (dirsearch / ffuf / gobuster)
- 账号密码爆破 (hydra / medusa / burp)
- API 端点探测
- 配置文件与备份文件发现
- 国产 CMS / OA / 云服务的安全评估

## 目录结构

```
dict/
├── username/           # 用户名字典
│   ├── common.txt      # 通用账号 (admin, root, test...)
│   ├── database.txt    # 数据库相关账号
│   ├── security-tools.txt  # 安全工具默认账号
│   ├── devops.txt      # 运维/部署相关账号
│   ├── network-device.txt  # 网络设备默认账号
│   └── china-systems.txt   # 国产系统默认账号
│
├── password/           # 密码字典
│   ├── common.txt      # 通用弱密码
│   ├── keyboard-pattern.txt  # 键盘序列密码
│   └── china-default.txt     # 国产系统默认密码
│
├── path/               # 目录/路径字典
│   ├── common.txt      # 通用路径
│   ├── admin-panel.txt # 后台面板路径
│   ├── database-tool.txt     # 数据库管理工具路径
│   ├── cms.txt         # CMS 特征路径
│   ├── config-leak.txt # 配置文件泄露路径
│   ├── vcs.txt         # 版本控制泄露路径
│   ├── springboot.txt  # SpringBoot 特征路径
│   └── china-systems.txt     # 国产系统特征路径
│
├── api/                # API 端点字典
│   ├── common.txt      # 通用 API 端点
│   └── china-cloud.txt # 国内云服务商 API
│
└── backup/             # 备份文件字典
    └── patterns.txt    # 备份文件命名模式
```

## 使用示例

### 目录扫描

```bash
# 使用 dirsearch 扫描后台
python dirsearch.py -u http://target.com -w path/admin-panel.txt

# 使用 ffuf 扫描国产 CMS
ffuf -u http://target.com/FUZZ -w path/china-systems.txt

# 组合多个字典
cat path/*.txt > all-paths.txt
ffuf -u http://target.com/FUZZ -w all-paths.txt
```

### 账号爆破

```bash
# Hydra 爆破 SSH
hydra -L username/common.txt -P password/common.txt ssh://target.com

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

## 更新日志

| 日期 | 内容 |
|------|------|
| 2026-05-12 | 重组目录结构，补充国产系统字典，优化分类 |

## 贡献指南

欢迎提交 PR 补充字典内容。新增条目请遵循以下原则：

1. 按场景分类放到对应目录
2. 去重（同一文件内不重复）
3. 补充国产系统时请注明来源（厂商文档/实际渗透测试经验）
4. 密码条目优先补充实际出现过的高频弱密码

## 免责声明

本字典仅供授权的安全测试和渗透测试使用。使用本工具进行未经授权的访问属于违法行为，由使用者自行承担法律责任。
