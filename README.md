# 色彩的语言

从看懂颜色到建立配色系统。面向兴趣学习的非专业读者，以「看见—关系—表达—实践—应用—系统」组织六篇24章，与《设计系统》相互参照，可独立阅读。

## 阅读顺序

从 [导读](appendices/00-how-to-read.md) 开始，分章目录由 `book.json` 维护，详见 [目录](CONTENTS.md)。书中「间色」为原创虚构文化空间，真实案例在正文展示官方图像并链接资料；照片感情景图标注为AI教学示意。精确色块不以生成图作证。

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

## 本轮视觉修订

新增8个真实案例分析（12张官方参考图），覆盖Spotify、Penguin、Duolingo、iMac、LEGO House、Carbon与Firefox；新增6组AI完整应用示意，覆盖品牌物料、刊物、包装、空间、材料与穿搭。全部嵌入对应正文，真实参考与AI示意分别标注。

[视觉案例索引](appendices/04-visual-cases.md)提供集中浏览入口，首页精选8项。八组配色海报改用完整刊物摄影和精确编辑排印，保留同版式、同摄影、指定色号与可复算对比度。

- `references/real-cases.json`：真实图片原始地址、权利归属与所属章节。
- `references/visual-cases.json`：首页精选与案例导航清单。
- `editorial/generated-case-prompts.json`：生图提示词、方法与输出路径。

## 逐章应用补充（2026-10-23）

针对仍只有抽象示意的13章，新增19张图像：6组生图场景、2张馆藏实图、10张精确应用面板与1张可复算取色图；第8章用已有服装图补充专门的冷暖解读。24章均有具体对象或完整设计案例，见视觉案例索引的逐章入口。图像覆盖不是完备性的替代，后续按概念需要继续扩展。

- `editorial/chapter-visual-coverage.json`记录各章应用图实际引用。
- `editorial/generated-chapter-v2-prompts.json`记录本轮6组生图。
- `references/real-cases-v2.json`记录本轮馆藏图片来源。
- `scripts/sample_chapter_photo.py`可复算第13章的采样色号。

## 基础图解视觉修订

旧的27张自创示意已重新审查：19张保留教学任务并重绘，8张重复的简笔图由所在章节的完整案例接替。颜色数值、面积比例、对比度与图表数据仍用程序控制；摄影、材料和完整应用承担具体场景。封面同步更新为精确排印结合原创场景。

`python scripts/draw_figures.py`复现现行图解，`--only 04 02b`可只生成选定图。旧版已撤下图号不再生成，避免之后构建又覆盖成旧图。三个分组脚本与共享样式共同维护，数值验证记录见`editorial/redraw-*.json`。
