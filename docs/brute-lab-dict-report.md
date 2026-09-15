# brute-lab 字典固化报告（2026-09-15）

服务对象：anchorscan 口令爆破专用靶场（brute-lab-20260915）。
spec：anchorscan 仓 `docs/plans/brute-lab-20260915/spec.md`。

## 改动（全部只追加不删减）

- username：ssh/smb/ftp 追加 `lab`/`ftpuser`；**补建 redis.txt（redis）、vnc.txt（admin/root/user）**——此前 vnc 缺 username 侧会静默回退 top100（ADR-0027 缺侧回退），本次消掉该隐性回退。
- password：ssh+lab、redis+redis123、vnc 幂等、mssql+P@ssw0rd123、ftp+ftp123、smb+lab；每模块追加 3-5 个干扰项（靶标不持有、hard 强口令零撞车）。
- 红线：三个 hard 强口令（Kp7!vR2m#xQ9 / Tz4#bN8!wK2m / Yh6@Dj3^pW9f）全仓 grep 零出现——负样本「同字典零命中」依赖这一点。

## 实弹验证结论（anchorscan e2e TestBruteLab127Matrix，13 轮）

- 命中实证：ssh lab/lab、mysql root/root、redis redis123（requirepass 认证爆破可用）、vnc admin、rdp administrator/123456、mssql sa/P@ssw0rd123、ftp ftpuser/ftp123、telnet admin/admin、afrog dameng SYSDBA/dameng123。
- 能力边界（fscan 侧非字典问题）：smb@非445端口插件拒绝执行、smtp@aiosmtpd 不投递凭据。
- 干扰项全程零误报（负样本组同字典零命中）。

改动留工作区未提交，待所有者审。
