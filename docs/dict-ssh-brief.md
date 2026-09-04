# Brief：dict 仓新增 SSH 专用迷你字典（P1）

你是编码 agent，只做本 brief 写明的事。读不到的东西不要猜，停下写报告。

## 必读（先读，再动手）

1. `README.md`——字典分类、能力 ID 规则（`<dir>-<basename>`）、门禁命令
2. `scripts/validate_dict.py` 头注释——格式门禁（UTF-8/LF/无 BOM/无行尾空格/无重复行）
3. `scripts/dictlib.py` `load_provenance` 附近——catalog 只收录 `capabilities/rights/provenance.json` 中 `decision == accepted` 的资产
4. `username/common.txt`、`password/common.txt`——格式样例（一行一条，LF，末尾换行）
5. 对齐依据（内容唯一真相源）：`../RBKD-templates/javascript/default-logins/ssh-mini-brute.yaml` 的 `payloads` 段（usernames: root、admin；passwords: root、admin）。只读该仓这一个文件，不改它。

## 范围（只做这些）

1. 新建 `username/ssh.txt`：恰好 2 行，顺序 `root`、`admin`
2. 新建 `password/ssh.txt`：恰好 2 行，顺序 `root`、`admin`
3. 运行 `python scripts/generate_catalog.py --write`（预期：catalog 无变化，因新资产无 provenance 条目；如实报告实际输出，不要为"让 catalog 有内容"而自创 provenance 条目）
4. 写报告 `docs/dict-ssh-report.md`（改动清单、门禁完整输出、笛卡尔计数证明：2 用户 × 2 密码 = 4 次尝试）

## 明确不做

- `releases/` staging、provenance 审批、任何已有文件修改
- Playbook / fathom / RBKD-templates / new-Anchor 四个仓一律不碰（除上条只读 RBKD 模板文件）
- 不执行任何 git 操作（add/commit/push 全部禁止）；不安装/升级任何依赖

## 铁律（违反即失败）

- 每文件恰好 2 行，不许多加——`123456` 等一律不收，本票无例外（RBKD-templates 铁律第 4 条：弱口令最多 2×2=4 次尝试）
- 内容逐行等于对齐依据的 payloads；顺序 root 在前、admin 在后
- UTF-8 无 BOM、LF 换行、无行尾空格、无重复行
- hydra 笛卡尔语义：`-L/-P` 是乘积不是配对，行数即预算，永远不许"顺手补几个"

## 验收（逐项给出命令与退出码）

```bash
python scripts/validate_dict.py        # 须 exit 0
python scripts/secret_scan.py --tree . # 须 exit 0
python scripts/test_dict.py            # 须 exit 0（按 README 门禁）
python scripts/generate_catalog.py --write  # 报告实际输出；catalog diff 须为空（`git status --short` 仅显示 2 个新文件 + 本 brief/report，catalog 无修改才是对的）
```

报告中粘贴以上四条命令的完整输出。做不到的如实写做不到，不许用"基本通过"代替退出码。
