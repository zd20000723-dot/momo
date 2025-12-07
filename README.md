# momo

用于背单词。

## 功能
- 按官方开放平台文档（https://open.maimemo.com）获取 `access_token` 后，调用墨墨背单词 API 自动获取每日单词列表。
- 根据单词生成包含目标词汇的英文阅读材料。
- 使用 LibreTranslate 兼容接口在中英之间互译生成的阅读内容。

## 快速开始
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
   > 若网络受限，可先下载 `requests` 包的离线 whl 再本地安装。
2. 在墨墨开放平台创建应用并记录 `client_id`、`client_secret`（参见官网文档）。
3. 设置环境变量：
   - `MOMO_CLIENT_ID` / `MOMO_CLIENT_SECRET`：用于换取 `access_token` 的凭据。
   - `MOMO_ACCESS_TOKEN`（可选）：如果已经在外部拿到 Token，可直接填入跳过换取流程。
   - `MOMO_API_BASE`（可选）：API 基址，默认 `https://open.maimemo.com`。
   - `MOMO_TODAY_ENDPOINT`（可选）：每日单词接口路径，默认 `/api/v1/memo-words/today-review`。
   - `MOMO_DATED_ENDPOINT`（可选）：按日期取词接口路径，默认 `/api/v1/memo-words/review-by-date`。
   - `MOMO_TOKEN_ENDPOINT`（可选）：换取 Token 的路径，默认 `/oauth2/token`。
   - `LIBRE_TRANSLATE_URL`（可选）：LibreTranslate 兼容的翻译接口 URL，默认 `https://translate.argosopentech.com/translate`。
4. 运行脚本生成阅读并翻译：
   ```bash
   python momo_cli.py --sentences 6 --direction en2zh
   ```

## 详细用法（中文教程）
下面给出常用场景的中文示例：

### 1）用 MoMo 官方 API 拉取当天单词并生成阅读 + 翻译
```bash
python momo_cli.py --sentences 6 --direction en2zh --client-id YOUR_ID --client-secret YOUR_SECRET
```
- 会自动按照开放平台的 client_credentials 流程换取 `access_token`，调用官方接口获取今日待复习单词。
- `--direction en2zh` 表示英文 → 中文翻译；改成 `zh2en` 即中文 → 英文。
- 生成的内容会依次输出：单词列表、英文阅读、对应翻译。

### 2）指定日期取词
```bash
python momo_cli.py --date 2024-06-01 --sentences 5
```
- `--date` 需使用 `YYYY-MM-DD` 格式。

### 3）不调用 API，直接指定单词
```bash
python momo_cli.py --words "abandon, implement, deliberate" --direction en2zh
```
- 适合没有可用 Token 或临时练习场景。

### 4）保存结果到文件
```bash
python momo_cli.py --words "abandon, implement" --output ./output.txt
```
- 终端会打印生成内容，同时写入指定文件。

### 5）自定义接口地址
- MoMo 接口域名或开放平台反代地址变动时：
  ```bash
  python momo_cli.py --base-url https://open-proxy.example.com --client-id YOUR_ID --client-secret YOUR_SECRET
  ```
- 翻译服务更换或自建时：
  ```bash
  python momo_cli.py --translate-url https://your-translate.example.com/translate
  ```

## 自定义用法
- 指定日期获取单词：
  ```bash
  python momo_cli.py --date 2024-06-01
  ```
- 手动传入单词列表（跳过 API）：
  ```bash
  python momo_cli.py --words "abandon, implement, deliberate" --direction en2zh
  ```
- 保存输出到文件：
  ```bash
  python momo_cli.py --words "abandon, implement" --output ./output.txt
  ```

生成内容包含：
1. 单词列表
2. 根据单词生成的英文阅读
3. 对应方向的翻译（默认为英译中）

> 说明：MoMo API 具体路径可能会变动，可通过环境变量或参数调整。若翻译接口需要自建服务，可将 `LIBRE_TRANSLATE_URL` 指向自部署地址。
