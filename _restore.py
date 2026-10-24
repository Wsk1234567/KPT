from pathlib import Path
import subprocess

root = Path(r"C:\Users\wskan\XiaomiMiMoProjects\KPT Website")
index = root / "index.html"


def git_show(rev, path="index.html"):
    return subprocess.check_output(
        ["git", "show", f"{rev}:{path}"],
        cwd=str(root),
        encoding="utf-8",
        errors="replace",
    )


def extract_section(html, start_markers, end_tag="</section>"):
    for mark in start_markers:
        i = html.find(mark)
        if i == -1:
            continue
        sec = html.rfind("<section", 0, i + 40)
        if sec == -1:
            continue
        depth = 0
        j = sec
        while j < len(html):
            if html.startswith("<section", j):
                depth += 1
                j += 8
            elif html.startswith("</section>", j):
                depth -= 1
                j += 10
                if depth == 0:
                    return html[sec:j]
            else:
                j += 1
    return None


current = index.read_text(encoding="utf-8", errors="replace")

# --- Help cards from commit with photos + correct names (5140bad) ---
help_src = git_show("5140bad")
help_sec = extract_section(help_src, ['id="help"', 'help-band', "What do you need"])
print("help sec", "ok" if help_sec else "FAIL", len(help_sec or ""))

# --- Intro from before removal (aea87db still has intro? check 5140bad) ---
intro_sec = extract_section(help_src, ['id="intro"', "intro-band", "intro-slogan"])
if not intro_sec:
    intro_sec = extract_section(git_show("409a8cf"), ['id="intro"', "intro-band", "intro-slogan"])
if not intro_sec:
    intro_sec = extract_section(git_show("22e0a92"), ['id="intro"', "intro-band", "intro-slogan"])
print("intro sec", "ok" if intro_sec else "FAIL", len(intro_sec or ""))

# --- Activity from current ---
act_sec = extract_section(current, ['id="activity"', "latest-activity"])
print("activity", "ok" if act_sec else "FAIL", len(act_sec or ""))

# Hero ... end of hero section: split current at end of hero
hero_end = extract_section(current, ["hero-road", "aria-label=\"Introduction\""])
print("hero", "ok" if hero_end else "FAIL")

# Build from current: keep from start through hero, then inject sections, keep rest after latest-activity
# Simpler: take current, replace from latest-activity start to home-summary start with ordered blocks

ms = current.find("<section class=\"home-summary\"")
if ms == -1:
    ms = current.find("home-summary")
print("home-summary at", ms)

hero_marker = "hero-road"
hi = current.find(hero_marker)
# find end of hero section
hero_block = extract_section(current, ["hero-road"])
assert hero_block and act_sec

# everything before hero
before = current[: current.find(hero_block)]
# everything after activity (from home-summary)
after = current[ms:] if ms != -1 else "</main>" + current.split("</main>")[-1]

# Ensure help includes correct names if 5140bad already has them
if help_sec and "Ambulance Service" not in help_sec:
    print("warn: help missing Ambulance Service names")

parts = [before.rstrip() + "\n\n"]
if help_sec:
    parts.append(help_sec + "\n\n")
else:
    print("NO HELP")
if intro_sec:
    parts.append(intro_sec + "\n\n")
else:
    print("NO INTRO")
parts.append(act_sec + "\n\n")
parts.append(after if after.startswith("<section") or after.startswith("\n") else after)

new = "".join(parts)
index.write_text(new, encoding="utf-8")

# verify order
for key in ["hero-road", "help-band", "What do you need", "intro-slogan", "latest-activity", "home-summary"]:
    print(key, new.find(key))
