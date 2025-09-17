# MCP Demo 服务与客户端

这是一个 **UV MCP Demo 服务**，演示 MCP 服务与客户端的完整交互流程，包含查询天气生成小故事的示例。

## 环境要求

* Python >= 3.12
* `uv` CLI 工具
* 虚拟环境管理工具（推荐 `venv` 或 `poetry`）

---

## 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/chenghuang7/DOC_RAG.git
cd mcp_serve
```

2. 创建并激活虚拟环境：

```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

3. 安装依赖：

使用 `pyproject.toml`：

```bash
pip install .
```

---

## 启动 MCP Client

客户端用于测试与 MCP 服务的交互：

```bash
python clients/mcp_client.py
```

运行后示例输出：

```
# python clients/mcp_client.py 

Query: 帮我生成一个契合今天北京天气的故事
[助手调用工具完成任务'帮我生成一个契合今天北京天气的故事'中...]
INFO:mcp.server.lowlevel.server:Processing request of type ListToolsRequest
INFO:mcp.server.lowlevel.server:Processing request of type CallToolRequest
INFO:root:web_search called. query='今天北京天气'
INFO:httpx:HTTP Request: POST https://open.bigmodel.cn/api/paas/v4/tools "HTTP/1.1 200 OK"
INFO:mcp.server.lowlevel.server:Processing request of type CallToolRequest
INFO:mcp.server.lowlevel.server:Processing request of type CallToolRequest
INFO:httpx:HTTP Request: POST https://open.bigmodel.cn/api/paas/v4/chat/completions "HTTP/1.1 200 OK"
INFO:mcp.server.lowlevel.server:Processing request of type CallToolRequest
INFO:httpx:HTTP Request: POST https://open.bigmodel.cn/api/paas/v4/images/generations "HTTP/1.1 200 OK"
INFO:tools.story_tool:image generate res: https://maas-watermark-prod.cn-wlcb.ufileos.com/1758083981914_watermark.png?UCloudPublicKey=TOKEN_75a9ae85-4f15-4045-940f-e94c0f82ae90&Signature=89DYQyEaX7WLOa9x5FVKiKWzcR8%3D&Expires=1758170381
INFO:httpx:HTTP Request: POST https://open.bigmodel.cn/api/paas/v4/images/generations "HTTP/1.1 200 OK"
INFO:tools.story_tool:image generate res: https://maas-watermark-prod.cn-wlcb.ufileos.com/1758083989681_watermark.png?UCloudPublicKey=TOKEN_75a9ae85-4f15-4045-940f-e94c0f82ae90&Signature=94xtC3syVzYfPFiaVhjS%2BRl11e8%3D&Expires=1758170389
INFO:httpx:HTTP Request: POST https://open.bigmodel.cn/api/paas/v4/images/generations "HTTP/1.1 200 OK"
INFO:tools.story_tool:image generate res: https://maas-watermark-prod.cn-wlcb.ufileos.com/1758084003401_watermark.png?UCloudPublicKey=TOKEN_75a9ae85-4f15-4045-940f-e94c0f82ae90&Signature=KOBn9Xgyfxtl%2BjbwwWTTz3MzamE%3D&Expires=1758170403

=== 对话历史 ===
[用户 1] 帮我生成一个契合今天北京天气的故事
[助手调用工具 2] web_search 参数: {"query": "\u4eca\u5929\u5317\u4eac\u5929\u6c14"}
[助手调用工具 4] get_story_prompt 参数: {"story_theme": "\u5317\u4eac ..."}
[助手调用工具 6] generate_story 参数: {"story_prompt": ...}
[助手调用工具 8] generate_image 参数: {"images_prompts": ["An ..."]}
[助手 10] 根据今天北京的天气情况（晴朗，温度适中，天高云淡），我为您生成了一个温暖的秋天故事，并配上了相应的图片。

## 《秋日重逢》

**第一幕：晨光中的等待**
北京秋日的晨光中，天空漆蓝如洗，温和的阳光洒落在四合院的青砖灰瓦上。老人张爷爷坐在门前的石椅上，温暖的风帆轻折着他铸铸的白发。街巷里传来远处的鸽子啼啼声，一切都那么安祥而温柔。

**第二幕：正午的重逢**  
中午时分，一个年轻女子手持一束正胜花走进四合院。她是张爷爷多年未见的孙女，从海外回来。阳光下，两代人相见的眼睛里湃满了温情，那束粉红的花朵在秋风中轻轻摇晃，如同时光的温暖与希望。

**第三幕：黄昏的漫步**
黄昏时分，孙女握着爷爷的手，一起步行在北京的胡同里。秋风轻吹，街道两旁的老树叶子已经染上金黄。阳光从西边斜照下来，把他们的影子拉得长长的。这一刻，北京的秋天温暖而深情，如同两代人之间那份永恒的爱。

![第一幕图片](https://maas-watermark-prod.cn-wlcb.ufileos.com/1758084280410_watermark.png?UCloudPublicKey=TOKEN_75a9ae85-4f15-4045-940f-e94c0f82ae90&Signature=0%2Fl7ghQkfDO3OjpKIQq5dhZqaTY%3D&Expires=1758170680)

![第二幕图片](https://maas-watermark-prod.cn-wlcb.ufileos.com/1758084288327_watermark.png?UCloudPublicKey=TOKEN_75a9ae85-4f15-4045-940f-e94c0f82ae90&Signature=vTWi2qzuHRJvXhinAdGQLv8vces%3D&Expires=1758170688)

![第三幕图片](https://maas-watermark-prod.cn-wlcb.ufileos.com/1758084296252_watermark.png?UCloudPublicKey=TOKEN_75a9ae85-4f15-4045-940f-e94c0f82ae90&Signature=c1TzJVvQl%2FPydvbn%2BuB9qHYTLz0%3D&Expires=1758170696)

这个故事完美契合了今天北京晴朗温暖的秋日天气，展现了家人团聚的温馨时刻。
================
```