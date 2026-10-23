# 第1–6章交叉审稿

审稿日期：2026-10-23。审稿人：practice；仅提交本报告，不改其他组章节。核对对象为六章Markdown、scripts/draw_figures.py，并实际查看fig03/fig05。fig02b仍由图解代理制作，应在最终构建前再核对。

## 结论

章节逻辑与非专业读者定位吻合，没有发现需要重写的色科学错误。对典型色觉、颜料非理想性、HSL非感知均匀、灰度检查局限、WCAG适用范围均有必要限定。实际练习可操作，不把喜欢与任务表现混同。

## 必须修正

1. **第5章图注与实际图不符。**图注写「连线表示选色方向」，draw_figures.py和实际fig05只有色环与下方三组色块，没有连线。最小修正建议：改为「下方色组表示几种选色方向，不是颜料配方；色块的明暗与鲜艳程度还需要单独调整」。也可以真正补连线，但不必为图注增复杂度。

## 建议增强（不阻塞正文）

2. **第4章适应/颜色恒常性的就近引用较宽。**CSS Color 4确实涉及观看条件与色适应，但链接的Color Terminology段不是颜色恒常性的直接教学来源。建议对这一小段补视觉科学教材的恒常性/适应章节，或明确CSS引用仅支撑颜色表示与条件的区别，而不让它承担整段生理解释。
3. **第3章图题替代文本仍可更严谨。**图片本体与图注明确使用HSL；alt写「色相、明度与彩度分别变化」可改为「HSL色相、L与S分别变化的三组样本」，以免忽略图注的读者误认严格恒定感知量。现正文已解释限制，故不是实质事实错误。
4. **图02b最终检查。**应看RGB相交区是否为C/M/Y/白、理想CMY相交是否为B/G/R/黑；必须标理想滤色模型，避免暗示任意颜料会给出相同结果。正文已有相应限制。

## 独立复核

- UW–Madison Additive Color Mixing 页面可正常读取，明确叠加灯光及屏幕应用；Subtractive Color Mixing明确CMY与滤色片、材料吸收模型。两处链接与第2章用途一致。
- NCBI Cones and Color Vision 检索结果支持S/M/L及重叠光谱敏感性；正文没有把它们写成只响应红绿蓝的独立探测器。
- CSS Color 4当前为2026-10-22 Candidate Recommendation Draft，正文称持续修订标准草案恰当；HSL零饱和度色相无作用的说明成立。
- 独立复算暖纸#F6F1E7对比度：#B9B8A8=1.7792568、#24544B=7.6304906、#202824=13.4166400、#C86345=3.5021949、#A6AEA3=2.0266401，与第6章表格/图注一致。
- 第1章图注已称多色分区，与修正版图相符。
- 第4章中心块值及并排验证条均为#808080；图未声称像素相同等于跨设备发光相同。

## 本次复核一手来源

- https://www.physics.wisc.edu/ingersollmuseum/exhibits/opticscolor/color-mixing/
- https://www.physics.wisc.edu/ingersollmuseum/exhibits/opticscolor/subcolormix/
- https://www.ncbi.nlm.nih.gov/books/NBK11059/
- https://www.w3.org/TR/css-color-4/
