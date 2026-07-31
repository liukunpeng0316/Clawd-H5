# Clawd 表情工坊 Web 版

## 本地启动

1. 复制 `.env.example` 为 `.env`，填写 DeepSeek API Key；同时保留 StepFun Key 作为备用。
2. 运行 `docker compose up -d --build`。
3. 打开 `http://localhost:8088`。

公开版本默认限制为全站并发 3、队列最多 100、每个 IP 同时一个任务。作品文件累计达到 5 GiB 后，按创建时间删除最早作品。

模型请求默认使用 DeepSeek V4 Flash 非思考模式；连接失败或返回 HTTP 错误时，依次切换到 Step Plan 和 StepFun 按量接口。

不要把 `.env`、API Key 或 Docker 数据卷提交到仓库。
