# Brief：dict 仓新增 telnet/ftp/vnc 迷你字典（P2b-1）

你是编码 agent，只做本 brief 写明的事。本票是人工验证命令的字典沉淀——**不与 fathom 逐对一致，只求小**（用户裁决，见 Playbook ADR-0005 待写）。已有先例：`username/ssh.txt` + `password/ssh.txt`（P1，2×2，读它们学格式）。

## 必读

1. `README.md`（能力 ID `<dir>-<basename>`、门禁命令）
2. `scripts/validate_dict.py`、`scripts/secret_scan.py`、`scripts/generate_catalog.py`（catalog 只收录 provenance accepted，本票无 provenance 操作，预期 catalog 无变化）
3. `username/ssh.txt`（格式样例）

## 范围：新建 5 文件，内容逐字如下（顺序即文件顺序）

1. `username/telnet.txt`：`admin`、`root`（2 行）
2. `password/telnet.txt`：`admin`、`root`、`123456`（3 行；笛卡尔 2×3=6）
3. `username/ftp.txt`：`anonymous`、`admin`、`root`（3 行）
4. `password/ftp.txt`：`anonymous`、`admin`、`123456`（3 行；笛卡尔 3×3=9）
5. `password/vnc.txt`：`123456`、`password`、`vnc`、`admin`、`1234`、`vnc123`、`12345678`、`root`（8 行，单维无笛卡尔；VNC 无用户名是协议如此，用户名文件一律不建）

附带：`python scripts/generate_catalog.py --write`（如实报告输出；不自创 provenance 条目）；报告 `docs/p2b-dict-report.md`（改动清单、三门禁完整输出、三个笛卡尔计数 6/9/8）。

## 明确不做

- rlogin/web-form 字典（已裁决转人工复核，不建）；`123456` 之外的增补；已有文件修改；`releases/`；其他四仓。

## 铁律

- UTF-8 无 BOM、LF、无行尾空格、末尾换行、无重复行；每文件行数恰好等于上表，多一行即失败。
- 笛卡尔天花板 9：telnet 6、ftp 9、vnc 单维 8——报告中用乘法写清三组计数。

## 验收

```bash
python scripts/validate_dict.py        # exit 0
python scripts/secret_scan.py --tree . # exit 0
python scripts/test_dict.py            # exit 0
python scripts/generate_catalog.py --write  # exit 0 且 catalog 无修改（git status 仅 5 新文件 + 本 brief/report）
```
