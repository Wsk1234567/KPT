# HERO v3 — 「Road Dispatch」救护车行驶场景

目标：首屏一眼高级。中央一辆**持续向右行驶**的救护车（轮子转 + 背景左移视差），上方机构名，下方 Transfer/Standby + 电话。

---

## 1. 视觉方向

**锚点：** 夜间出动公路电影海报 × 精密仪表 UI。  
不是卡通贴纸，而是**扁平高精度 SVG 场景** + 克制光效（电压青 `#3DF5C8`）。

| 层 | 内容 | 动效 |
|----|------|------|
| L0 天空 | 近黑渐变 `#0A0C0B → #0E1A18` + 微星点 | 星点极慢闪烁 |
| L1 远山 | 彭亨丘陵剪影（低对比） | 向左慢速平移 |
| L2 城市/树线 | 抽象剪影 + 稀疏窗光/路灯 | 向左中速平移 |
| L3 路面 | 公路 + 标线 | 向左快速平移（虚线流动） |
| L4 救护车 | 侧视、**车头朝右**，白车身 + 青十字 + 警灯 | 轮子 360° 转；车身极轻微起伏 |
| L5 光 | 车头灯锥、车底反射、速度线 | 向左划过 |
| L6 文案 | 车上 / 车下文字 | 进场 fade-up；电话可点 `tel:` |

**速度感公式：** 车在画面水平中心略偏右；背景 `translateX` 循环无缝；轮子 `rotate` 与位移节奏一致。

---

## 2. 文案结构（车上下）

```
        [ KAWASAN PAHANG TENGAH ]          ← 小标
   St. John Ambulans Malaysia              ← 主标题（Fraunces）
        ≡ 救护车行驶（居中） ≡
   Transfer · Standby · Event Cover        ← 服务一句
   +60 9-000 0000   [ Call Now ]           ← 电话 + CTA
```

四角保留：`EST. SERVICE · PAHANG` / `01 / DISPATCH` / `CENTRAL PAHANG AREA` / 滚动指示。

---

## 3. 救护车设计（SVG 细节）

- 比例：宽约 `min(72vw, 640px)`，侧视 3/4 侧影不必，**正侧视最稳、最酷**。
- 车身：纸白/浅灰，底部石墨阴影，窗玻璃偏青灰。
- 标识：侧门电压青十字（抽象八角十字可简化为医疗十字）+ 细字条 `AMBULANCE` / `ST. JOHN`。
- 轮胎：深灰胎 + 青灰轮毂，**两轮独立 `animation: spin`**。
- 警灯：车顶灯条，青/琥珀交替呼吸（`opacity` + `box-shadow` 模拟）。
- 车头朝右 → 行驶方向明确。

---

## 4. 动画规格（性能友好）

| 元素 | 属性 | 时长 | 备注 |
|------|------|------|------|
| 远山层 | `translateX` -10% 循环 | 40s linear infinite | 两段无缝拼贴 |
| 树/城层 | `translateX` | 22s | |
| 路面标线 | `translateX` | 8s | 虚线错位拼贴 |
| 轮子 | `rotate(360deg)` | 1.2s linear infinite | 与车速匹配 |
| 车身起伏 | `translateY(±2px)` | 1.4s ease-in-out | 极轻微 |
| 速度线 | `translateX` + opacity | 1.8s | 2–3 条 |
| 警灯 | opacity/scale | 1.2s alternate | |

- 只用 `transform` / `opacity`（不跑 layout）。
- `prefers-reduced-motion: reduce`：全部停，保留静态海报构图。
- 手机：缩小车宽、减星点与速度线数量。

---

## 5. 布局（仍满屏 Hero）

```
header (sticky)
┌──────────────────────────────────────┐
│  ·四角标签                             │
│         St. John Ambulans Malaysia    │
│         KAWASAN PAHANG TENGAH         │
│                                      │
│      🚑  ← 轮转 + 背景左移 →         │
│                                      │
│   Transfer · Standby · Event Cover   │
│   +60 9-000 0000    [ Call Now ]      │
│                              Scroll  │
└──────────────────────────────────────┘
home-impact / summary / news / footer  ← 不动
```

文案与车**不重叠**；车下有细线分隔服务行。

---

## 6. 技术

- 纯 `index.html` + `styles.css` + `main.js`（无构建、无 CDN 依赖），适合 GitHub Pages。
- 救护车：内联 SVG（可调色、可动轮子）；不用位图，放大不糊。
- `main.js` 仅在需要时加强（reduced-motion、可选视差滚动）；核心动画纯 CSS。
- 改完自动可 `git push` 到 `Wsk1234567/KPT`。

## 7. 明确不做

- 不用 Three.js/WebGL（杀鸡用牛刀，Pages 也更稳）。
- 不用真实 3D 车模 / 外链图片。
- 不改内页结构（只改 `index.html` Hero + 相应 CSS）。

## 8. 交付检查

1. 桌面 1280：车居中、轮转、背景左移、文案上下清晰  
2. 手机 390：车不裁切、电话可点、动画不卡  
3. reduced-motion：静态完整构图  
4. push → Pages 刷新验收  
