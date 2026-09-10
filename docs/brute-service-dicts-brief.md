# Brief：dict 仓新增 rdp/smb/mysql/mssql/oracle/redis/smtp 按服务字典（brute-service-dicts）

你是编码 agent，只做本 brief 写明的事。**动机**：AnchorScan init-setup（其仓 ADR-0027 §3）把 `brute.dicts.<module>` 映射到本仓 `username/<module>.txt + password/<module>.txt`；七服务文件此前缺失，AnchorScan 侧暂时回退全局 top100（其 doctor 已点名提示）。本票补齐文件；落盘并发布后由 AnchorScan 仓自行摘回退提示（跨仓，非本票）。

已有先例：`username/ssh.txt` + `password/ssh.txt`（P1）、telnet/ftp/vnc（P2b-1），读它们学格式。

## 必读

1. `README.md`（能力 ID `<dir>-<basename>`、本地门禁）
2. `scripts/validate_dict.py`、`scripts/secret_scan.py`、`scripts/generate_catalog.py`（catalog 只收 provenance accepted；本票无 provenance 操作，预期 catalog 无变化）
3. `username/ssh.txt`、`password/vnc.txt`（格式样例）

## 范围：新建 13 文件，内容逐字如下（顺序即文件顺序；行数多一行即失败）

1. `username/rdp.txt`：`administrator`、`admin`、`root`（3 行）
2. `password/rdp.txt`：`123456`、`P@ssw0rd`、`admin`（3 行；笛卡尔 3×3=9）
3. `username/smb.txt`：`administrator`、`admin`、`root`（3 行）
4. `password/smb.txt`：`123456`、`admin`、`password`（3 行；笛卡尔 3×3=9）
5. `username/mysql.txt`：`root`、`mysql`、`admin`（3 行）
6. `password/mysql.txt`：`root`、`123456`、`mysql`（3 行；笛卡尔 3×3=9）
7. `username/mssql.txt`：`sa`、`admin`（2 行）
8. `password/mssql.txt`：`sa`、`123456`、`P@ssw0rd`（3 行；笛卡尔 2×3=6）
9. `username/oracle.txt`：`system`、`sys`、`scott`（3 行）
10. `password/oracle.txt`：`oracle`、`tiger`、`123456`（3 行；笛卡尔 3×3=9）
11. `password/redis.txt`：`123456`、`redis`、`password`、`foobared`、`root`（5 行，单维无笛卡尔）
12. `username/smtp.txt`：`admin`、`test`（2 行）
13. `password/smtp.txt`：`123456`、`password`、`admin`（3 行；笛卡尔 2×3=6）

来源口径：全部为通用出厂/安装默认凭据（Windows 管理员组、`sa`、MySQL `root`、Oracle `system|sys|scott/tiger`、redis `requirepass` 示例值 `foobared`），无第三方词表引入，NOTICE 不变。

## 明确不做

- **不建 `username/redis.txt`**：Redis 认证无用户名概念，与 VNC 同口径（P2b-1 裁决「用户名文件一律不建」）。AnchorScan 侧 `brute.dicts.redis.user_dict` 届时指向 top100 或回退全局，属其仓工作，不是本票。
- 不改任何已有文件；不做 provenance 审批（新资产保持 `held`，catalog 预期无变化）；不动 `releases/`；不碰其他四仓。

## 铁律

- UTF-8 无 BOM、LF、无行尾空格、末尾换行、无重复行；每文件行数恰好等于上表。
- 笛卡尔天花板 9：rdp 9、smb 9、mysql 9、mssql 6、oracle 9、redis 单维 5、smtp 6——报告中用乘法写清七组计数。

## 验收

```bash
python scripts/validate_dict.py        # exit 0
python scripts/secret_scan.py --tree . # exit 0
python scripts/test_dict.py            # exit 0
python scripts/generate_catalog.py --write  # exit 0 且 catalog 无修改（git status 仅 13 新文件 + 本 brief/report）
```

报告写 `docs/brute-service-dicts-report.md`：改动清单、三门禁完整输出、七组笛卡尔计数、redis 用户名不建的裁决引用。
