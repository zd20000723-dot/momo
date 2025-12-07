# momo

用于背单词。

## 功能
- 调用墨墨背单词（MoMo）API 自动获取每日单词列表。
- 根据单词生成包含目标词汇的英文阅读材料。
- 使用 LibreTranslate 兼容接口在中英之间互译生成的阅读内容。

## 快速开始
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 设置环境变量：
   - `MOMO_API_TOKEN`：墨墨背单词接口的 Token。
   - `MOMO_API_BASE`（可选）：API 基址，默认 `https://api.maimemo.com`。
   - `MOMO_DAILY_ENDPOINT`（可选）：每日单词接口路径，默认 `/v2/review/today-words`。
   - `LIBRE_TRANSLATE_URL`（可选）：LibreTranslate 兼容的翻译接口 URL，默认 `https://translate.argosopentech.com/translate`。
3. 运行脚本生成阅读并翻译：
   ```bash
   python momo_cli.py --sentences 6 --direction en2zh
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
