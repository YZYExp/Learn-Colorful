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

后续主页源码使用 `site/`，直接消费现有主稿与清单；本阶段未创建或部署网站。Git首次提交只含零字节README，后续按书稿与图解进展叠加。
