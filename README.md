# 色彩的语言

从看懂颜色到建立配色系统。面向兴趣学习的非专业读者，以「看见—关系—表达—实践—应用—系统」组织六篇24章，与《设计系统》相互参照，可独立阅读。

## 阅读顺序

从 [导读](appendices/00-how-to-read.md) 开始，分章目录由 `book.json` 维护，详见 [目录](CONTENTS.md)。书中「间色」为原创虚构文化空间，品牌真实案例在正文链接官方资料；照片感情景图标注为AI教学示意。精确色块不以生成图作证。

## 构建

需要Python 3.10或更高版本。重绘图片还需要已安装的Noto CJK、思源或苹方字体；可用 `COLOR_BOOK_FONT` 指定字体文件绝对路径。已有图片随工程提供，仅构建EPUB无需重绘。

```bash
python -m pip install -r requirements.txt
python scripts/draw_figures.py
python scripts/draw_palette_studies.py
python scripts/build.py --check
python scripts/build.py
```

输出位于 `build/色彩的语言.epub`。EPUB采用重排阅读，文字可放大，教学图逐张展开；读者设备和阅读器可能改变显示效果。`build/validation.json`记录本地内容、图片、EPUB XML和内部资源检查结果，不代表专业色彩校准或已通过所有阅读器认证。

## 工程结构

- `chapters/`：24章中文Markdown主稿。
- `appendices/`：导读、练习手册和术语。
- `assets/images/`：实际教学图和情景示意。
- `references/`：资料与图片来源记录。
- `editorial/`：写作约定、图解规范、审校记录，不进入书籍正文。
- `scripts/`：精确配图、校验与EPUB构建。
- `book.json`：章节稳定ID、顺序、资源路径与未来阅读站URL slug。

## 网页阅读与自动发布

`site/` 保存样式和交互，`scripts/build_site.py` 直接读取现有主稿与 `book.json` 生成主页、分章阅读、全书搜索和配色对照。图片保持原比例，手机端目录可折叠；提供字号、深浅主题及继续阅读。

```bash
python -m pip install -r requirements-site.txt
python scripts/build_site.py --base-path /Learn-Colorful/
python scripts/check_site.py --base-path /Learn-Colorful/
```

网页输出为 `build/site/`，已忽略入Git。用于根路径预览时传入 `--base-path /`。若显式附带经过验证的电子书，可使用 `--epub build/色彩的语言.epub`；默认构建不会读取旧导出文件。

`.github/workflows/pages.yml` 在main相关内容更新时独立构建和部署，PR只校验；仓库Pages的Source应为GitHub Actions。网站流程仅安装Markdown，不安装字体或重跑配图。

`.github/workflows/ebook.yml` 独立导出并完整解码验证EPUB图片，产物为 `color-language-epub`，保留90天。网页中的离线阅读入口指向该流程，下载Actions附件需要登录GitHub。
Git首次提交只含零字节README，后续按书稿与图解进展叠加。
