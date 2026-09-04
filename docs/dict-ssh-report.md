# dict SSH 专用迷你字典 — 执行报告（P1）

## 1. 改动清单（仅新增，不修改已有文件）

| 文件 | 内容 | 行数 | 能力 ID |
|------|------|------|---------|
| `username/ssh.txt` | `root`、`admin`（此顺序） | 恰好 2 行 | `username-ssh` |
| `password/ssh.txt` | `root`、`admin`（此顺序） | 恰好 2 行 | `password-ssh` |
| `docs/dict-ssh-report.md` | 本报告 | — | — |

- 对齐依据（唯一真相源，只读未改）：`../RBKD-templates/javascript/default-logins/ssh-mini-brute.yaml` 的 `payloads` 段：
  ```yaml
  payloads:
    usernames:
      - root
      - admin
    passwords:
      - root
      - admin
  ```
- 新文件内容逐行等于上述 payloads，顺序 root 在前、admin 在后，未添加 `123456` 等任何额外条目。
- 格式：UTF-8 无 BOM、LF 换行、无行尾空格、无重复行、末尾换行（`xxd` 确认 `726f6f74 0a61646d696e 0a`，即 `root\nadmin\n`，11 字节）。
- 未动项：`releases/` staging、provenance 审批、任何已有文件均未修改；Playbook / fathom / RBKD-templates / new-Anchor 四仓未碰（RBKD 模板仅只读一次）；未执行任何 git 操作；未安装/升级依赖。

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
✓ wrote /var/folders/py/r19j2zh13m75xrmhvprxq86h0000gn/T/tmp06v041g0/capabilities/catalog-v1.json (0 capabilities)
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
  ?? docs/
  ?? password/ssh.txt
  ?? username/ssh.txt
  ```
  （`docs/` 未跟踪系因本 brief 与本报告均在其中；除 2 个新字典文件 + docs 报告外无其他变更。）
- `git diff --stat`（实际输出）：空（ tracked 文件零修改；`capabilities/` 无 diff）。
- 原因：`capabilities/rights/provenance.json` 共 33 条资产、`accepted` 0 条、无 `ssh` 条目；`dictlib.load_provenance` 只收录 `decision == accepted` 资产，故新资产不进 catalog，catalog 保持 0 capabilities。未自创任何 provenance 条目。

## 3. 笛卡尔计数证明（hydra `-L/-P` 为乘积语义）

- `username/ssh.txt` 行数：2（root、admin）
- `password/ssh.txt` 行数：2（root、admin）
- 笛卡尔积：2 × 2 = **4 次尝试**，枚举如下：
  ```
  root / root
  root / admin
  admin / root
  admin / admin
  ```
- 验证命令：`count = $(wc -l < username/ssh.txt) * $(wc -l < password/ssh.txt)` = 4。
- 对应 RBKD 模板约束：`max-request: 4` / `MAX 4 ATTEMPTS`，一致，未超预算。

## 4. 结论

- 四条验收命令全部 exit 0，完整输出已如上粘贴，无"基本通过"代替退出码。
- catalog diff 为空是**正确且预期的**（新资产无 provenance 条目）。
- 无未完成项；无偏离 brief 的行为。
