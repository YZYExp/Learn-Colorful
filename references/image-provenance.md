# 图片来源与制作记录（编辑资料，不进入正文）

## 精确教学图

`fig-01.png`至`fig-24.png`及`fig-02b.png`、`fig-08b.png`、`fig-22b.png`由本工程 `scripts/draw_figures.py` 原创绘制。sRGB色值、HSL示意样本和WCAG相对亮度在脚本中可复算。每张图的教学边界写在图内/图注；数字图不证明真实材料的色差、照明或颜色情绪效应。图18为虚构数据，发散两端近似平衡感知明暗，不宣称整条色阶感知均匀。

`palette-01.png`至`palette-08.png`及封面由 `scripts/draw_palette_studies.py` 原创绘制；八组色彩应用不是年度趋势或真实品牌配色。数值记录于 `palette-studies.json`。

## AI情景示意

两张图使用内置 image_gen 生成（非CLI），生成日期2026-10-23，均已打开检查并实际嵌入正文。生成图不可用作校准、材料鉴定、建筑施工或实拍事实证明。色号在提示词中仅为外观方向，不意味着生成像素严格遵循。

### jianse-space.png

用途：第20章，绿色柜体、暖墙与陶橘座椅如何形成空间中的面积分配与局部呼应。

完整生成提示：

> Use case: product-mockup. Asset type: Chinese illustrated color education book, original fictional small culture space named Jianse (no visible lettering). Create one exquisite realistic architectural editorial photograph: a compact welcoming contemporary bookstore cafe gallery, cream warm paper walls, muted deep forest-green joinery, one terracotta orange upholstered bench as a restrained accent, dark charcoal slim furniture, natural light from side window, books, one simple ceramic cup, small original abstract exhibition framed print, believable architectural proportions, polished but lived-in, no people. Entire space visible in a composed three-quarter eye-level view, vertical 4:5 portrait composition, sophisticated contemporary art-book photography, realistic materials and soft shadows. This is an illustrative original design rather than an existing venue, no logo no watermarks no text, avoid decorative clutter. Colors should be visually inspired by dark green #24544B, cream #F6F1E7, terracotta #C86345, charcoal #202824 but do not include hex codes; image is for contextual appearance not color calibration.

检查结果：实际生成双层空间，正文按实际图说明，未称严格小尺度或施工方案；室内颜色受阴影与反射影响，未标示像素等于基础色号。

### material-board.png

用途：第19章，帮助观察纹理、透明感与高光如何改变绿色外观。

完整生成提示：

> Use case: product-mockup. Asset type: teaching image in illustrated color design book. A beautiful photorealistic flat-lay material board for a fictional bookstore cafe: six generous green material samples in a calm neatly spaced two-column three-row arrangement on a warm off-white paper background. Samples are matte painted wood, lustrous glazed ceramic, folded woven cotton, translucent tinted glass with soft cast shadow, lightly textured paper, brushed green coated metal. All inspired by the same muted dark forest green family; visible difference in reflection and texture, realistic physical materials, gentle side daylight, refined contemporary design magazine macro photography, clean clearly separated samples, no labels, no visible lettering, no logos, no watermarks. Portrait 4:5 composition. Not a scientific calibrated comparison: aim visual explanation of material differences, not exact equal reflectance.

检查结果：六格分明，木纹、织物、透明感和反光可观察。左下纹理可能被看成石材，不用于判定材料种类；正文明确「材质外观教学示意」并给出材料鉴定限制。

## 使用与引用

本书没有把AI图冒充真实品牌、真实建筑或历史作品。真实机构与品牌案例以正文就近的一手资料链接为依据。本记录不授予第三方品牌素材额外使用许可。
