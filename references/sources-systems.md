# 第19–24章来源核实记录

核实日期：2026-10-23。正文使用可访问的原始来源链接，每章末保留本章资料；间色方案、练习步骤与颜色分工为原创教学方法，不把它们归因于引用文献。

| 来源 | 使用章节 | 支持内容与核实方式 |
| --- | --- | --- |
| [Pantone Graphics and 294 New Colors—Uses and Best Practices](https://www.pantone.com/uk/en-gb/articles/uses-and-best-practices/pantone-graphics-and-294-new-colors) | 19 | 官方检索结果明确说明图形印刷与纺织体系/材料匹配差异；直接打开403，未声称通读全部网页 |
| [X-Rite: What Is Metamerism?](https://www.xrite.com/blog/what-is-metamerism) | 19 | 官方检索明确给出一种光源下匹配、换光源不匹配的定义，汽车跨材料例子；直接打开403 |
| [Benjamin Moore: Lighting and Paint Colors](https://www.benjaminmoore.com/-/media/sites/benjaminmoore/images/color-card-pdf-landing-page/color-handbook_use.pdf) | 20 | 官方PDF检索可得自然/人工照明差异与同空间对照；全文打开超过工具大小限制，未声称全本通读 |
| [Houser, Mossman, Smet & Whitehead: Tutorial: Color Rendering and Its Applications in Lighting](https://doi.org/10.1080/15502724.2014.989802) | 20 | 论文原站检索返回作者、摘要及第3节原文，支持相同色温/色度但不同光谱可能使物体显色不同；期刊卷12(1–2),7–26，2016，网络先行2015；正文不误署为Royer |
| [GOV.UK Design System: Colour](https://design-system.service.gov.uk/styles/colour/) | 21 | 已打开全文；功能颜色与网页色板区分、按语境使用变量、避免拷贝HEX；不将官方当前色值复制为间色品牌值 |
| [Material Components Android: Color Theming](https://github.com/material-components/material-components-android/blob/master/docs/theming/Color.md) | 21、22 | 已打开官方仓库文件；浅深主题不同角色映射及on-前景角色，品牌角色与error/surface区分 |
| [W3C: Understanding Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) | 21、24 | 已打开全文；颜色之外的可见线索，不夸称只加文字就符合整套WCAG |
| [W3C: Understanding Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) | 24 | 已打开全文；普通字4.5∶1、大字3∶1及字号/阈值；文字中的表格为本书计算 |
| [W3C: Understanding Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html) | 22 | 已打开全文；必要控件/状态线索相邻对比3∶1；不要求默认和悬停两状态彼此达到3∶1 |
| [W3C: CSS Color Module Level 4](https://www.w3.org/TR/css-color-4/) | 22、23 | 已打开工作草案全文；sRGB、P3、OKLCH、插值与色域边界；明确工作草案身份，无最终标准误述 |
| [ICC: Frequently Asked Questions](https://www.color.org/faqs/) | 23 | 已打开术语与主题目录；配置文件与颜色管理入口；具体流程另引白皮书 |
| [ICC White Paper 23: RGB Color Managed Workflow Example](https://www.color.org/ICC_white_paper_23_RGB_Workflow.pdf) | 23、24 | 已打开6页PDF文本；保留带配置主文件、多目标输出、转换、软打样与实物匹配边界 |
| [Pantone: Normal Printing Process Color Variances—Explained](https://support.pantone.com/en/normal-printing-process-color-variances-explained) | 23 | 已打开全文；纸张、油墨、颜料与过程差异，不把专色写成绝对不变 |

## 本书对比度计算

采用WCAG sRGB线性化：c≤0.04045时c/12.92，否则((c+0.055)/1.055)^2.4；相对亮度L=0.2126R+0.7152G+0.0722B；对比度=(L较亮+0.05)/(L较暗+0.05)。所有输入均为不透明sRGB实色。表格显示两位小数，但阈值按全精度判断。

- #24544B / #F6F1E7：7.6304906488
- #202824 / #F6F1E7：13.4166399588
- #FFFFFF / #24544B：8.5898596935
- #C86345 / #F6F1E7：3.5021948544，不达普通字4.5
- #9B3A2C / #F6F1E7：6.1458703223
- #202824 / #B9D9CE：9.9821463764

## 事实与解释的边界

- 没有把屏幕AI材料图当成真实材料测量。
- 没有把文化空间图当真实品牌、工程效果或现场照片。
- 不承诺浅/深主题一定对某类人更舒适。
- 不承诺RGB/CMYK、专色、ICC转换让所有媒介外观绝对一致。
- 菜单纸张/墙面选材观察法属于教学建议，不代替工程规范或专业验收。
