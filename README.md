# Travel Journal 2026 · v3 高清拼贴手帐版

一本可以翻页的 3D 精装旅行手帐。阅读器用的是开源项目
[HaichaoLihc/create-photo-flipbook-ui](https://github.com/HaichaoLihc/create-photo-flipbook-ui)
自带的 3D 精装书。

顺序：日本 → 仙本那 → 巴厘岛 → 大理 → 深圳湾 → 济州岛（共 15 个跨页：封面、目录、每个地方 2 个跨页、结尾）。

- **照片 = 你的原图**：只做了裁切、白边、撕纸边、轻微调色和颗粒，没有用 AI 改。
- **装饰插画**（水彩风景、邮票、吉祥物贴纸、花枝、地标小画）是单独生成的图片，放在 `source/art/`，可以随便换。
- 车票、邮戳、红色毛笔线、回形针、和纸胶带、竖排地名标签都是代码画的，文字都能改。

---

本版把每一页渲染成 **2400×3200**（前一版的两倍），全屏看和录屏都会更清楚。
3D 翻页程序已打开各向异性过滤、mipmap，并按 `min(设备像素比, 2)` 输出。

## 怎么打开

**方法 A（推荐，直接双击）：** 用 Chrome 或 Edge 打开 `album_standalone.html`（单文件版，不用开黑窗口）。第一次加载要等几秒。

**方法 B（文件夹版）：不要直接双击 `index.html`。** 3D 书需要本地网页服务。

1. 双击 `start.bat`（或在本文件夹打开命令行，运行 `py -m http.server 4173`）
2. 用 Chrome 或 Edge 打开 http://127.0.0.1:4173/

拖页角、点击书页或按左右方向键翻页。需要 WebGL（新版 Chrome / Edge 都可以）。

---

## 文件在哪

```
album_standalone.html  ← 单文件版，双击即可翻页（图片已打包进文件）
assets/pages/          ← 渲染好的每一页（JPG，2400×3200），3D 书直接读取它们
source/
  config.json          ← 所有文字 + 照片文件名（最常改的地方）
  photos/              ← 你的原图
  art/                 ← 装饰插画（透明 WebP）
  art_raw/             ← 装饰插画原图（白底 JPG）
  layouts/collage.py   ← 每一页的拼贴图层：位置、大小、角度、裁切
  layouts/kit.py       ← 图层工具：拍立得、撕纸照片、邮票、邮戳、车票、胶带……
  layouts/shared.css   ← 字体和样式
  tools/photofx.py     ← 照片处理（撕边、白边、调色）
  tools/prep_art.py    ← 把 art_raw/ 的插画抠成透明 PNG
  render.py            ← 运行它重新生成所有页面
  cache/               ← 自动生成的照片碎片，可以随时删，会自动重建
```

---

## 第一次在自己电脑上重新渲染（只需要装一次）

```bat
py -m pip install pillow numpy opencv-python-headless playwright
py -m playwright install chromium
```

之后每次修改完，在 `source` 文件夹里运行：

```bat
py render.py            :: 渲染全部页面
py render.py s02 s03    :: 只渲染日本的两个跨页（快很多）
```

跨页编号：`cover` 封面，`s01` 目录，`s02 s03` 日本，`s04 s05` 仙本那，`s06 s07` 巴厘岛，
`s08 s09` 大理，`s10 s11` 深圳湾，`s12 s13` 济州岛，`s14` 结尾。

---

## 怎么换照片

**方法 1（最简单）**：用同名文件替换 `source/photos/` 里的照片，例如把新照片命名为 `01_japan_3.jpg` 覆盖原来的，再运行 `py render.py`。（先备份旧照片。）

**方法 2**：把新照片放进 `source/photos/`，然后打开 `config.json`，改 `"photos"` 里对应的文件名：

```json
"japan_me": "01_japan_3.jpg",     ← 改成你的新文件名
```

左边的 `japan_me` 是照片的“代号”，`collage.py` 里用的就是这个代号，所以不用改别的地方。

如果新照片的构图不一样，可能要调整裁切：在 `collage.py` 里找到用这个代号的那一行，改 `box`：

```python
K.polaroid("japan_me", [0.0, 0.04, 1.0, 0.86], 300, 250, 600, 800, 3.5, ...)
#                      [左,  上,   右,  下 ]   x    y    宽   高  角度
```

`box` 用 0~1 的比例表示裁哪一块：`[0,0,1,1]` 是整张，`[0,0,1,0.5]` 是上半张。

---

## 每一层拼贴在哪里定义

打开 `source/layouts/collage.py`，每个跨页是一个函数：

| 跨页 | 函数 |
|---|---|
| 封面 | `cover()` |
| 目录 | `contents()` |
| 日本 | `japan_a()`、`japan_b()` |
| 仙本那 | `semporna_a()`、`semporna_b()` |
| 巴厘岛 | `bali_a()`、`bali_b()` |
| 大理 | `dali_a()`、`dali_b()` |
| 深圳湾 | `sz_a()`、`sz_b()` |
| 济州岛 | `jeju_a()`、`jeju_b()` |
| 结尾 | `closing()` |

每个地方第一个跨页的左页（大标题、邮票、邮戳、水彩风景）用的是同一个函数 `opener_left()`，
可以在调用它的地方改标题大小、邮票位置等参数。

函数里**每一行 `L.append(...)`（左页）或 `R.append(...)`（右页）就是一个图层**，从上到下依次叠放，
`z=` 数字越大越在上面。单页大小 1200 × 1600，坐标 (0,0) 在页面左上角。

| 写法 | 是什么 |
|---|---|
| `K.polaroid("代号", box, x, y, 宽, 高, 角度, caption="手写说明")` | 白边拍立得 |
| `K.torn("代号", box, x, y, 宽, 高, 角度, seed=数字)` | 撕纸边照片碎片（换 seed 就换一种撕法；`fx="faded"` 变复古褪色） |
| `K.mini("代号", box, x, y, 宽, 高, 角度)` | 小相片 |
| `K.scrap("kraft", x, y, 宽, 高, 角度)` | 纸片：kraft 牛皮纸 / grid 方格 / lined 横线 / cream / blue / pink / sage / sand / ink |
| `K.art("japan_landscape", x, y, 宽, 角度)` | 插画（`source/art/` 里的文件名） |
| `K.sticker("japan_mascot", x, y, 宽, 角度)` | 带阴影的贴纸 |
| `K.stamp("japan", x, y, 宽, 角度)` | 邮票（文字在 config.json → stamp） |
| `K.postmark("japan", x, y, 大小, 角度, color=...)` | 圆形邮戳（config.json → postmark） |
| `K.ticket("japan", x, y, 宽, 高, 角度)` | 车票（config.json → ticket） |
| `K.vlabel("japan", x, y, 字号, 角度, color=...)` | 竖排地名标签（config.json → label） |
| `K.washi(x, y, 宽, 高, 角度, "颜色", "dots")` | 和纸胶带（dots / stripe / grid / plain） |
| `K.paperclip(x, y, 高, 角度)` | 回形针 |
| `K.brush(x, y, 宽, 高, "颜色")` | 毛笔下划线 |
| `K.text("文字", x, y, 宽, cls="hand", size=34)` | 文字：`hand` 手写、`note` 笔记、`type` 打字机、`title` 大标题 |

想删掉某个元素：在那一行前面加 `#`。想复制一个：复制那一行，改 x、y。

---

## 改文字

全部在 `source/config.json`：每个地方的标题、手写短句（`hand`）、坐标、笔记（`notes`）、
照片说明（`cap_a` `cap_b` `cap_c`）、日记（`journal`）、邮票面值、邮戳文字、车票起点终点。
改完运行 `py render.py`。

## 换装饰插画

把新的白底图片放进 `source/art_raw/`，文件名照旧（例如 `bali_mascot.jpg`），运行
`py tools/prep_art.py` 抠成透明图，再运行 `py render.py`。
命名规则：`地方_landscape`（水彩风景）、`_stamp`（邮票）、`_mascot`（贴纸）、`_branch`（花枝）、`_landmark`（地标小画）。

## 字体

都在 `source/fonts/`，SIL OFL / Apache 开源授权：Bodoni Moda（大标题）、Special Elite（打字机字）、
Homemade Apple / Caveat（手写）、Cormorant Garamond、Playfair Display 等。
中文标签用电脑自带的宋体（Noto Serif / 思源宋体 / SimSun）。
