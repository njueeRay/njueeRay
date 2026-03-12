#!/usr/bin/env python3
"""
Generate assets/team-knowledge-graph.svg — 7-agent radial layout.
All 7 agents rendered with brand colors; Profile-Designer included.
Run: python scripts/gen-knowledge-graph.py
"""

import math
import os

# ── Layout constants ──────────────────────────────────────────────────────────
CANVAS_W, CANVAS_H = 900, 500
CX, CY = 450, 250          # center of the graph
CENTER_R = 44              # njueeRay core node radius
AGENT_R  = 26              # agent circle radius
ORBIT_R  = 130             # distance from center to agent nodes
CONCEPT_ORBIT = 210        # distance from center to concept nodes

# ── Agent data ────────────────────────────────────────────────────────────────
# (name, brand-color, concept-label)
# Order = clockwise from top; evenly spaced 360/7 ≈ 51.43°
AGENTS = [
    ("Brain",            "#3B5BDB", "AI-native"),
    ("PM",               "#2F9E44", "Sprint-Board"),
    ("Dev",              "#7048E8", "njueeray.io"),
    ("Researcher",       "#E8590C", "Knowledge"),
    ("Code-Reviewer",    "#C92A2A", "Blog"),
    ("Brand",            "#0C8599", "Build-Public"),
    ("Prof.Designer",    "#F08C00", "Pixel-Avatar"),
]

# ── Geometry helpers ──────────────────────────────────────────────────────────
def polar(r: float, deg: float):
    """Convert polar (r, angle°) relative to canvas center → absolute (x, y)."""
    rad = math.radians(deg)
    return CX + r * math.cos(rad), CY + r * math.sin(rad)

def edge(ax, ay, bx, by, ra, rb):
    """Return (sx, sy, ex, ey): segment from edge of circle-A to edge of circle-B."""
    dx, dy = bx - ax, by - ay
    dist   = math.hypot(dx, dy) or 1
    sx = ax + ra * dx / dist
    sy = ay + ra * dy / dist
    ex = bx - rb * dx / dist
    ey = by - rb * dy / dist
    return sx, sy, ex, ey

def rgb_lighten(hex_color: str, amount: float = 0.45) -> str:
    """Lighten a #rrggbb hex colour towards white by `amount` (0–1)."""
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return f"#{r:02x}{g:02x}{b:02x}"

# ── Position computation ──────────────────────────────────────────────────────
n = len(AGENTS)
step = 360.0 / n

agent_data = []   # (name, color, concept, x, y, concept_x, concept_y)
for i, (name, color, concept) in enumerate(AGENTS):
    angle = -90.0 + i * step
    ax, ay = polar(ORBIT_R, angle)
    cx2, cy2 = polar(CONCEPT_ORBIT, angle)
    agent_data.append((name, color, concept, ax, ay, cx2, cy2))

# ── SVG build ─────────────────────────────────────────────────────────────────
lines = []
w = lambda s: lines.append(s)

w(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
  f'viewBox="0 0 {CANVAS_W} {CANVAS_H}">')

# Filters
w('  <defs>')
w('    <filter id="glow-gold" x="-60%" y="-60%" width="220%" height="220%">')
w('      <feGaussianBlur stdDeviation="5" result="blur"/>')
w('      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')
w('    </filter>')
for i, (name, color, *_) in enumerate(AGENTS):
    fid = f"glow{i}"
    w(f'    <filter id="{fid}" x="-60%" y="-60%" width="220%" height="220%">')
    w(f'      <feGaussianBlur stdDeviation="4" result="blur"/>')
    w(f'      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')
    w(f'    </filter>')
w('    <pattern id="dots" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">')
w('      <circle cx="20" cy="20" r="0.8" fill="#21262d" opacity="0.8"/>')
w('    </pattern>')
w('  </defs>')

# Background
w(f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#0d1117" rx="12"/>')
w(f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="url(#dots)" rx="12"/>')

# Title
w('  <text x="450" y="24" text-anchor="middle"')
w('        fill="#58a6ff" font-family="\'Segoe UI\',Arial,sans-serif"')
w('        font-size="13" font-weight="bold" letter-spacing="0.5">')
w('    Team Knowledge Graph \u2014 AI-native \u56e2\u968f\u8ba4\u77e5\u56fe\u8c31')
w('  </text>')

# ── LAYER 1: Center → Agent edges ─────────────────────────────────────────────
w('  <!-- center → agent edges -->')
w('  <g stroke="#1f6feb" stroke-width="1.8" opacity="0.55" fill="none">')
for name, color, concept, ax, ay, cx2, cy2 in agent_data:
    sx, sy, ex, ey = edge(CX, CY, ax, ay, CENTER_R, AGENT_R)
    w(f'    <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}"/>')
w('  </g>')

# ── LAYER 2: Agent → Concept edges ────────────────────────────────────────────
w('  <!-- agent → concept edges -->')
w('  <g stroke="#30363d" stroke-width="1.5" opacity="0.9" fill="none" stroke-dasharray="4,3">')
for name, color, concept, ax, ay, cx2, cy2 in agent_data:
    sx, sy, ex, ey = edge(ax, ay, cx2, cy2, AGENT_R, 0)
    w(f'    <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{cx2:.1f}" y2="{cy2:.1f}"/>')
w('  </g>')

# ── LAYER 3: Concept nodes ────────────────────────────────────────────────────
BOX_W, BOX_H = 100, 26
w('  <!-- concept nodes -->')
for name, color, concept, ax, ay, cx2, cy2 in agent_data:
    bx = cx2 - BOX_W / 2
    by = cy2 - BOX_H / 2
    w(f'  <rect x="{bx:.1f}" y="{by:.1f}" width="{BOX_W}" height="{BOX_H}" rx="6"')
    w(f'        fill="#161b22" stroke="#58a6ff" stroke-width="1.2" opacity="0.85"/>')
    w(f'  <text x="{cx2:.1f}" y="{cy2 + 4.5:.1f}" text-anchor="middle"')
    w(f'        fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11.5">{concept}</text>')

# ── LAYER 4: Agent circles ────────────────────────────────────────────────────
w('  <!-- agent nodes -->')
for i, (name, color, concept, ax, ay, cx2, cy2) in enumerate(agent_data):
    light = rgb_lighten(color, 0.5)
    w(f'  <!-- {name} -->')
    w(f'  <circle cx="{ax:.1f}" cy="{ay:.1f}" r="{AGENT_R}"')
    w(f'          fill="#0d1117" stroke="{color}" stroke-width="2.2"')
    w(f'          filter="url(#glow{i})"/>')
    # Two-line label for long names
    label_parts = name.split(".")  # "Prof.Designer" → ["Prof", "Designer"]
    if len(label_parts) == 2:
        w(f'  <text x="{ax:.1f}" y="{ay - 3:.1f}" text-anchor="middle"')
        w(f'        fill="{color}" font-family="\'Segoe UI\',Arial,sans-serif" font-size="9.5" font-weight="bold">{label_parts[0]}.</text>')
        w(f'  <text x="{ax:.1f}" y="{ay + 9:.1f}" text-anchor="middle"')
        w(f'        fill="{color}" font-family="\'Segoe UI\',Arial,sans-serif" font-size="9.5" font-weight="bold">{label_parts[1]}</text>')
    else:
        fs = "11" if len(name) <= 4 else "9.5"
        w(f'  <text x="{ax:.1f}" y="{ay + 4.5:.1f}" text-anchor="middle"')
        w(f'        fill="{color}" font-family="\'Segoe UI\',Arial,sans-serif" font-size="{fs}" font-weight="bold">{name}</text>')

# ── LAYER 5: Center node ──────────────────────────────────────────────────────
w('  <!-- center: njueeRay -->')
w(f'  <circle cx="{CX}" cy="{CY}" r="{CENTER_R}"')
w(f'          fill="#161b22" stroke="#f0e68c" stroke-width="2.5"')
w(f'          filter="url(#glow-gold)"/>')
w(f'  <text x="{CX}" y="{CY - 3}" text-anchor="middle"')
w(f'        fill="#f0e68c" font-family="\'Segoe UI\',Arial,sans-serif" font-size="13" font-weight="bold">njueeRay</text>')
w(f'  <text x="{CX}" y="{CY + 13}" text-anchor="middle"')
w(f'        fill="#f0e68c" font-family="\'Segoe UI\',Arial,sans-serif" font-size="8.5" opacity="0.75" letter-spacing="1">CORE</text>')

# ── Legend ────────────────────────────────────────────────────────────────────
w('  <!-- legend -->')
w(f'  <g transform="translate(748, 400)">')
w(f'    <rect x="-4" y="-4" width="140" height="88" rx="6"')
w(f'          fill="#161b22" stroke="#21262d" stroke-width="1"/>')
w(f'    <circle cx="12" cy="12" r="8" fill="#161b22" stroke="#f0e68c" stroke-width="1.8"/>')
w(f'    <text x="26" y="16" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11">Core (Ray)</text>')
w(f'    <circle cx="12" cy="38" r="8" fill="#0d1117" stroke="#58a6ff" stroke-width="1.8"/>')
w(f'    <text x="26" y="42" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11">AI Agent</text>')
w(f'    <rect x="4" y="56" width="16" height="10" rx="3" fill="#161b22" stroke="#58a6ff" stroke-width="1"/>')
w(f'    <text x="26" y="65" fill="#8b949e" font-family="\'Segoe UI\',Arial,sans-serif" font-size="11">Concept</text>')
w(f'  </g>')

w('</svg>')

# ── Output ────────────────────────────────────────────────────────────────────
out_path = os.path.join(os.path.dirname(__file__), "..", "assets", "team-knowledge-graph.svg")
out_path = os.path.normpath(out_path)
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"✅ Written: {out_path}")
print(f"   Canvas: {CANVAS_W}×{CANVAS_H}px, {n} agents")
for name, color, concept, ax, ay, *_ in agent_data:
    print(f"   {name:16s} {color}  pos=({ax:.0f},{ay:.0f})")
