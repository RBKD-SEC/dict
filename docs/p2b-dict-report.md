# dict telnet/ftp/vnc 迷你字典 — 执行报告（P2b-1）

## 1. 改动清单（仅新增 5 文件，不修改已有文件）

| 文件 | 内容（此顺序） | 行数 | 能力 ID |
|------|---------------|------|---------|
| `username/telnet.txt` | `admin`、`root` | 恰好 2 行 | `username-telnet` |
| `password/telnet.txt` | `admin`、`root`、`123456` | 恰好 3 行 | `password-telnet` |
| `username/ftp.txt` | `anonymous`、`admin`、`root` | 恰好 3 行 | `username-ftp` |
| `password/ftp.txt` | `anonymous`、`admin`、`123456` | 恰好 3 行 | `password-ftp` |
| `password/vnc.txt` | `123456`、`password`、`vnc`、`admin`、`1234`、`vnc123`、`12345678`、`root`（此顺序） | 恰好 8 行 | `password-vnc` |
| `docs/p2b-dict-report.md` | 本报告 | — | — |

- 本票是人工验证命令的字典沉淀——**不与 fathom 逐对一致，只求小**（用户裁决，Playbook ADR-0005 待写）。
- VNC 无用户名文件是协议如此（VNC 认证只有密码，无用户名维度），用户名文件一律不建。
- 格式：UTF-8 无 BOM、LF 换行、无行尾空格、无重复行、末尾换行（`validate_dict.py` 全绿 + `wc -l` == `grep -c ''` 五文件一致）。
- 未动项：已有文件零修改；`releases/` staging 未碰；未自创任何 provenance 条目；rlogin/web-form 字典未建（已裁决转人工复核）；`123456` 之外无增补；其他四仓未碰；未执行任何 git 操作。

## 2. 门禁完整输出（逐项命令与退出码）

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
✓ wrote /var/folders/py/r19j2zh13m75xrmhvprxq86h0000gn/T/tmpt43mvd39/capabilities/catalog-v1.json (0 capabilities)
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

- `git status --short`（实际输出）：
  ```
  ?? docs/p2b-dict-brief.md
  ?? password/ftp.txt
  ?? password/telnet.txt
  ?? password/vnc.txt
  ?? username/ftp.txt
  ?? username/telnet.txt
  ```
  （`docs/p2b-dict-brief.md` 为本票 brief；本报告 `docs/p2b-dict-report.md` 写于 status 之后，同属 docs 新增。除 5 个新字典文件 + docs 外无其他变更。）
- `git diff --stat`（实际输出）：空（tracked 文件零修改；`capabilities/` 无 diff）。
- 原因：catalog 只收录 provenance `accepted` 资产，本票无 provenance 操作，新资产不进 catalog，catalog 保持 0 capabilities。未自创任何 provenance 条目。

## 3. 笛卡尔计数证明（hydra `-L/-P` 为乘积语义，天花板 9）

- telnet：2（`username/telnet.txt`） × 3（`password/telnet.txt`）= **6 次尝试**：
  ```
  admin / admin
  admin / root
  admin / 123456
  root / admin
  root / root
  root / 123456
  ```
- ftp：3（`username/ftp.txt`） × 3（`password/ftp.txt`）= **9 次尝试**（恰达天花板，未超）：
  ```
  anonymous / anonymous
  anonymous / admin
  anonymous / 123456
  admin / anonymous
  admin / admin
  admin / 123456
  root / anonymous
  root / admin
  root / 123456
  ```
- vnc：单维 8（`password/vnc.txt`），无用户名维度、无乘法——**8 次尝试**：
  ```
  123456
  password
  vnc
  admin
  1234
  vnc123
  12345678
  root
  ```
- 验证：`wc -l` 输出 `username/telnet.txt:2 password/telnet.txt:3 username/ftp.txt:3 password/ftp.txt:3 password/vnc.txt:8`，且 `wc -l` == `grep -c ''` 五文件一致（末尾换行齐全，无多行）。

## 4. 结论

- 四条验收命令全部 exit 0，完整输出已如上粘贴，无"基本通过"代替退出码。
- catalog diff 为空是**正确且预期的**（新资产无 provenance 条目）。
- 三组计数 6 / 9 / 8，天花板 9 未超；vnc 单维 8 无笛卡尔。
- 无未完成项；无偏离 brief 的行为。
