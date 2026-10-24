from pathlib import Path

root = Path(r"C:\Users\wskan\XiaomiMiMoProjects\KPT Website")
html = root / "index.html"
t = html.read_text(encoding="utf-8", errors="replace")

# 1) Remove intro / Service for Mankind block
start = t.find("<!-- ===== Introduction")
if start == -1:
    start = t.find('class="intro-')
if start != -1:
    # find section start
    sec = t.rfind("<section", 0, start + 20)
    if sec != -1:
        start = sec
    depth = 0
    i = start
    end = None
    while i < len(t):
        if t.startswith("<section", i):
            depth += 1
            i += 8
        elif t.startswith("</section>", i):
            depth -= 1
            i += 10
            if depth == 0:
                end = i
                break
        else:
            i += 1
    if end:
        t = t[:start] + t[end:]
        print("intro removed", end - start, "chars")
    else:
        print("intro end not found")
else:
    print("intro not found")

# 2) If latest-activity missing, leave; else rewrite cards to timeline-friendly
if "latest-activity" not in t:
    print("NO activity section!")
else:
    print("activity present")

html.write_text(t, encoding="utf-8")

# 3) Timeline CSS — center line, alternate left/right
css = root / "styles.css"
c = css.read_text(encoding="utf-8", errors="replace")
c += '''

/* ===== Latest Activity as center timeline ===== */
.latest-activity {
  background: var(--paper) !important;
  padding: 80px 0 96px !important;
}
.act-grid {
  position: relative;
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 36px 56px !important;
  max-width: 1100px !important;
  margin: 0 auto !important;
  padding: 12px 0 8px;
}
.act-grid::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(
    180deg,
    transparent,
    var(--voltage) 8%,
    var(--voltage) 92%,
    transparent
  );
  transform: translateX(-50%);
  opacity: 0.55;
}

.act-card,
.act-card--hero,
.act-card--sm,
.act-card--wide {
  grid-column: auto !important;
  grid-row: auto !important;
  display: flex !important;
  flex-direction: column !important;
  background: #fff !important;
  color: var(--ink) !important;
  border: 1px solid var(--line-light) !important;
  border-radius: 14px !important;
  position: relative;
}

/* alternate: odd left, even right */
.act-card:nth-child(odd) {
  grid-column: 1 !important;
}
.act-card:nth-child(even) {
  grid-column: 2 !important;
}
/* slight offset so they feel staggered on the line */
.act-card:nth-child(odd) {
  transform: translateY(0);
}
.act-card:nth-child(even) {
  transform: translateY(28px);
}

/* connector dots on the line */
.act-card::after {
  content: "";
  position: absolute;
  top: 36px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--voltage);
  border: 2px solid var(--paper);
  box-shadow: 0 0 0 2px var(--voltage);
}
.act-card:nth-child(odd)::after {
  right: -35px;
}
.act-card:nth-child(even)::after {
  left: -35px;
}

.act-card--hero .act-card__meta {
  position: static !important;
  padding: 16px 18px 0 !important;
}
.act-card--hero .act-card__pill {
  background: var(--voltage) !important;
  color: var(--night) !important;
}
.act-card--hero .act-card__chip {
  background: var(--paper) !important;
  color: var(--quiet-light) !important;
  border-color: var(--line-light) !important;
}
.act-card--hero .act-card__body h3 {
  color: var(--ink) !important;
  font-size: 1.35rem !important;
}
.act-card--hero .act-card__body p {
  color: var(--quiet-light) !important;
}
.act-card--hero .act-card__media {
  aspect-ratio: 3 / 2 !important;
  min-height: 0 !important;
}
.act-card--wide .act-card__media {
  min-height: 0 !important;
}

@media (max-width: 800px) {
  .act-grid {
    grid-template-columns: 1fr !important;
    gap: 18px !important;
    padding-left: 22px;
  }
  .act-grid::before {
    left: 8px;
    transform: none;
  }
  .act-card:nth-child(odd),
  .act-card:nth-child(even) {
    grid-column: 1 !important;
    transform: none !important;
  }
  .act-card:nth-child(odd)::after,
  .act-card:nth-child(even)::after {
    left: -22px;
    right: auto;
    top: 28px;
  }
}
'''
css.write_text(c, encoding="utf-8")
print("timeline css ok")
