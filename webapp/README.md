# Clawd 表情工坊 Web 版

## 本地启动

1. 复制 `.env.example` 为 `.env`，填写 DeepSeek API Key；同时保留 StepFun Key 作为备用。
2. 运行 `docker compose up -d --build`。
3. 打开 `http://localhost:8088`。

公开版本默认限制为模型生成并发 10、GIF 导出并发 2、队列最多 100；同一 IP 可以提交多个任务。作品文件累计达到 5 GiB 后，按创建时间删除最早作品。

制作页会显示排队、模型生成、等待导出和 GIF 导出阶段及累计用时。公开作品页在手机上使用双列布局，支持直接下载 GIF、基于公开 SVG“做同款”，并在滚动到底时继续加载。

模型请求默认使用 DeepSeek V4 Flash 非思考模式；连接失败或返回 HTTP 错误时，依次切换到 Step Plan 和 StepFun 按量接口。

不要把 `.env`、API Key 或 Docker 数据卷提交到仓库。
