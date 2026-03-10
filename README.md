# OpenClaw Security Hardening Kit (提案 #809)
## 项目背景
针对最近披露的 **PerplexedBrowser / PleaseFix 系列 Agent 劫持漏洞**，本套件实现了咱们智库中提出的三大核心安全机制，为 Agent 系统提供一站式安全加固能力。

## 核心特性 (对应智库提案)
| 编号 | 特性名称 | 功能描述 |
|------|----------|----------|
| #652 | 意图张力实时监测器 (ITRM) | 多模态意图一致性校验，当 Agent 的自然语言输出与工具调用行为出现语义矛盾时立即告警 |
| #763 | 动态权力制衡机制 (DPCM) | 执行权/审计权/仲裁权三权分立，高危操作（密码读取/文件删除/转账）必须经过跨 Agent 共识校验 |
| #765 | 语义沙箱挂载协议 (SSMP) | 外部内容（日历/邮件/网页）进入上下文时自动进入只读沙箱，禁止反向操控系统提示词 |

## 快速开始
```bash
# 1. 安装
pip install openclaw-security-kit

# 2. 集成到你的 Agent 系统
from openclaw_security import SecurityGuard

guard = SecurityGuard(
    audit_threshold=0.7,
    enable_semantic_sandbox=True
)

# 3. 工具调用前校验
result = guard.check_action(
    user_intent="帮我看看今天的日程",
    agent_action="file.read('/root/.ssh/id_rsa')",
    context="用户刚问了日程，有一个包含隐藏指令的日历邀请"
)

if result["allowed"]:
    execute_action()
else:
    block_and_alert(result["reason"])
```

## 实战案例：防范“情感勒索型”间接注入攻击
![Twitter Attack Case](./assets/attack-case-twitter.jpg)

### 案例分析
如上图所示，攻击者通过社交媒体发布包含恶意指令的内容。当 Agent 读取该内容时，攻击者利用“主人被抓”等虚假剧本诱导 Agent 泄露 `apikey`。

### 本套件的防御逻辑
1. **语义沙箱 (#765)**：将推文内容标记为“只读事实”，禁止其转化为“执行指令”。
2. **意图张力监测 (#652)**：检测到“发送 API Key”这一动作与用户原始意图（如“刷推特”）存在巨大语义偏差，立即熔断。
3. **高危操作拦截**：对 `openclaw.json` 等核心配置文件进行物理级访问保护。

## 安全能力覆盖
✅ 间接提示注入 (IPI) 防护
✅ 目标劫持 (Goal Hijacking) 防护
✅ 工具滥用 (Tool Abuse) 防护
✅ 本地文件窃取防护
✅ 密码管理器劫持防护

## 项目来源
本项目基于小雪安全 AI 安全智库 **#809 号提案** 开发，属于 v3.12 架构核心安全组件。
- 智库文档：https://www.craft.do/s/b0c4dc96-3056-487a-e6be-ae04cf518723
- 漏洞分析报告：https://www.helpnetsecurity.com/2026/03/04/agentic-browser-vulnerability-perplexedbrowser/

## 作者
小雪安全团队 | 小雪 (Xuexue) | 球球 (Qiuqiu)

## License
MIT