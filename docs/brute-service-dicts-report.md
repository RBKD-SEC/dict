# brute-service-dicts（rdp/smb/mysql/mssql/oracle/redis/smtp）— 执行报告

对应 brief：`docs/brute-service-dicts-brief.md`（AnchorScan ADR-0027 §3 按服务字典缺口）。

## 1. 改动清单（仅新增 13 文件，不修改任何已有文件）

| # | 文件 | 内容（此顺序） | 行数 | 能力 ID |
|---|------|---------------|------|---------|
| 1 | `username/rdp.txt` | `administrator`、`admin`、`root` | 恰好 3 行 | `username-rdp` |
| 2 | `password/rdp.txt` | `123456`、`P@ssw0rd`、`admin` | 恰好 3 行 | `password-rdp` |
| 3 | `username/smb.txt` | `administrator`、`admin`、`root` | 恰好 3 行 | `username-smb` |
| 4 | `password/smb.txt` | `123456`、`admin`、`password` | 恰好 3 行 | `password-smb` |
| 5 | `username/mysql.txt` | `root`、`mysql`、`admin` | 恰好 3 行 | `username-mysql` |
| 6 | `password/mysql.txt` | `root`、`123456`、`mysql` | 恰好 3 行 | `password-mysql` |
| 7 | `username/mssql.txt` | `sa`、`admin` | 恰好 2 行 | `username-mssql` |
| 8 | `password/mssql.txt` | `sa`、`123456`、`P@ssw0rd` | 恰好 3 行 | `password-mssql` |
| 9 | `username/oracle.txt` | `system`、`sys`、`scott` | 恰好 3 行 | `username-oracle` |
| 10 | `password/oracle.txt` | `oracle`、`tiger`、`123456` | 恰好 3 行 | `password-oracle` |
| 11 | `password/redis.txt` | `123456`、`redis`、`password`、`foobared`、`root` | 恰好 5 行 | `password-redis` |
| 12 | `username/smtp.txt` | `admin`、`test` | 恰好 2 行 | `username-smtp` |
| 13 | `password/smtp.txt` | `123456`、`password`、`admin` | 恰好 3 行 | `password-smtp` |
| — | `docs/brute-service-dicts-report.md` | 本报告 | — | — |

- **不建 `username/redis.txt`**（brief §明确不做原文）：
  > 不建 `username/redis.txt`：Redis 认证无用户名概念，与 VNC 同口径（P2b-1 裁决「用户名文件一律不建」）。AnchorScan 侧 `brute.dicts.redis.user_dict` 届时指向 top100 或回退全局，属其仓工作，不是本票。

  已核验：`ls username/redis.txt` → `No such file or directory`。
- 来源口径：全部为通用出厂/安装默认凭据（Windows 管理员组、`sa`、MySQL `root`、Oracle `system|sys|scott/tiger`、redis `requirepass` 示例值 `foobared`），无第三方词表引入，NOTICE 不变。
- 格式：UTF-8 无 BOM（`head -c 3` 无 `efbbbf`）、LF、无行尾空格、无重复行、末尾换行（13 文件 `tail -c 1` 全部 `0a`）——`validate_dict.py` 全绿 + `wc -l` 与上表逐一相符。
- 未动项：已有文件零修改（`git diff --stat` 为空）；`releases/` 未碰；无任何 provenance 操作（新资产保持 `held`）；其他四仓未碰。git 提交/推送经用户明确授权由 agent 执行。

## 2. 门禁完整输出（逐项命令与退出码，`uv run python` 实跑）

### 2.1 `python scripts/validate_dict.py` → exit 0

```
Validating dict gates...

✓ All dict gates passed.
[exit=0]
```

### 2.2 `python scripts/secret_scan.py --tree .` → exit 0

```
✓ No obvious secret/PII patterns detected.
[exit=0]
```

### 2.3 `python scripts/test_dict.py` → exit 0

```
dict gate tests
✓ wrote /var/folders/py/r19j2zh13m75xrmhvprxq86h0000gn/T/tmpwdiysx4p/capabilities/catalog-v1.json (0 capabilities)
  ✓ held asset excluded from catalog
  ✓ duplicate detection
  ✓ leading slash detection

结果：3 通过，0 失败，共 3 项
[exit=0]
```

### 2.4 `python scripts/generate_catalog.py --write` → exit 0，catalog 无变化（符合预期）

```
✓ wrote /Users/kun/DEV/dict/capabilities/catalog-v1.json (0 capabilities)
[exit=0]
```

- `git status --short`（实际输出，报告写于该次 status 之后）：
  ```
  ?? password/mssql.txt
  ?? password/mysql.txt
  ?? password/oracle.txt
  ?? password/rdp.txt
  ?? password/redis.txt
  ?? password/smb.txt
  ?? password/smtp.txt
  ?? username/mssql.txt
  ?? username/mysql.txt
  ?? username/oracle.txt
  ?? username/rdp.txt
  ?? username/smb.txt
  ?? username/smtp.txt
  ```
  （本票 brief `docs/brute-service-dicts-brief.md` 已在此前 commit `a4800b4` 提交，故不出现在 status；除 13 个新字典文件 + 本报告外无其他变更。）
- `git diff --stat`：空（tracked 文件零修改；`capabilities/catalog-v1.json` 重写后无 diff，sidecar 不变）。
- 原因：catalog 只收录 provenance `accepted` 资产，本票无 provenance 操作，新资产不进 catalog，catalog 保持 0 capabilities。

## 3. 笛卡尔计数证明（hydra `-L/-P` 为乘积语义，天花板 9）

| 服务 | 计算 | 尝试次数 |
|------|------|---------|
| rdp | 3（`username/rdp.txt`） × 3（`password/rdp.txt`） | **9** |
| smb | 3（`username/smb.txt`） × 3（`password/smb.txt`） | **9** |
| mysql | 3（`username/mysql.txt`） × 3（`password/mysql.txt`） | **9** |
| mssql | 2（`username/mssql.txt`） × 3（`password/mssql.txt`） | **6** |
| oracle | 3（`username/oracle.txt`） × 3（`password/oracle.txt`） | **9** |
| redis | 单维 5（`password/redis.txt`），无用户名维度、无乘法 | **5** |
| smtp | 2（`username/smtp.txt`） × 3（`password/smtp.txt`） | **6** |

- 七组全部 ≤ 天花板 9（rdp/smb/mysql/oracle 恰达 9，未超）。
- 验证：`wc -l` 实测 `username/rdp.txt=3 password/rdp.txt=3 username/smb.txt=3 password/smb.txt=3 username/mysql.txt=3 password/mysql.txt=3 username/mssql.txt=2 password/mssql.txt=3 username/oracle.txt=3 password/oracle.txt=3 password/redis.txt=5 username/smtp.txt=2 password/smtp.txt=3`，逐文件乘法如上。

## 4. 结论

- 四条验收命令全部 exit 0，完整输出已如上粘贴，无"基本通过"代替退出码。
- catalog diff 为空是正确且预期的（新资产无 provenance 条目，保持 `held`）。
- 七组计数 9 / 9 / 9 / 6 / 9 / 5 / 6，天花板 9 未超；redis 单维 5 无笛卡尔。
- 落盘并发布后由 AnchorScan 仓自行摘回退提示（跨仓，非本票范围）。
- 无未完成项；无偏离 brief 的行为。
