"""
gen-pixel-badge.py
生成 Agent 像素头像横幅 SVG（深色 + 浅色各一份）
数据来源与 njueeray.github.io/src/data/pixel-avatars.ts 保持一致
"""
import os

agents = [
    {'id': 'brain',            'name': 'Brain',    'color': '#3B5BDB'},
    {'id': 'pm',               'name': 'PM',       'color': '#2F9E44'},
    {'id': 'dev',              'name': 'Dev',      'color': '#7048E8'},
    {'id': 'researcher',       'name': 'Research', 'color': '#E8590C'},
    {'id': 'code-reviewer',    'name': 'Reviewer', 'color': '#C92A2A'},
    {'id': 'profile-designer', 'name': 'Designer', 'color': '#F08C00'},
    {'id': 'brand',            'name': 'Brand',    'color': '#0C8599'},
]

PIXEL_AVATARS = {
    'brain': [
        [0,0,1,1,1,1,0,0],
        [0,1,0,0,0,0,1,0],
        [1,0,0,2,2,0,0,1],
        [1,0,2,0,0,2,0,1],
        [1,0,2,0,0,2,0,1],
        [1,0,0,2,2,0,0,1],
        [0,1,0,0,0,0,1,0],
        [0,0,1,1,1,1,0,0],
    ],
    'pm': [
        [0,2,0,0,0,2,0,0],
        [0,2,0,0,0,2,0,0],
        [0,1,0,0,0,1,0,0],
        [1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1],
        [0,1,0,0,0,1,0,0],
        [0,2,0,0,0,2,0,0],
        [0,2,0,0,0,2,0,0],
    ],
    'dev': [
        [0,0,1,2,2,1,0,0],
        [0,0,1,2,2,1,0,0],
        [1,1,1,1,1,1,1,1],
        [2,2,1,0,0,1,2,2],
        [2,2,1,0,0,1,2,2],
        [1,1,1,1,1,1,1,1],
        [0,0,1,2,2,1,0,0],
        [0,0,1,2,2,1,0,0],
    ],
    'researcher': [
        [2,0,0,1,1,0,0,2],
        [0,0,0,1,1,0,0,0],
        [0,0,1,1,1,1,0,0],
        [1,1,1,2,2,1,1,1],
        [1,1,1,2,2,1,1,1],
        [0,0,1,1,1,1,0,0],
        [0,0,0,1,1,0,0,0],
        [2,0,0,1,1,0,0,2],
    ],
    'code-reviewer': [
        [0,0,0,1,1,0,0,0],
        [0,0,1,0,0,1,0,0],
        [0,1,0,2,2,0,1,0],
        [1,0,2,0,0,2,0,1],
        [1,0,2,0,0,2,0,1],
        [0,1,0,2,2,0,1,0],
        [0,0,1,0,0,1,0,0],
        [0,0,0,1,1,0,0,0],
    ],
    'profile-designer': [
        [1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,1],
        [1,0,2,2,2,2,1,0],
        [1,0,2,0,0,2,1,0],
        [1,0,2,0,1,0,1,0],
        [1,0,2,2,1,0,1,0],
        [1,0,0,0,1,0,1,0],
        [1,1,1,1,1,0,0,0],
    ],
    'brand': [
        [0,0,0,0,0,0,0,0],
        [1,0,0,0,0,0,1,0],
        [1,1,0,0,0,1,1,0],
        [0,1,1,0,1,1,0,0],
        [2,0,1,2,1,0,2,0],
        [2,2,0,2,0,2,2,0],
        [0,2,2,2,2,2,0,0],
        [0,0,0,0,0,0,0,0],
    ],
}


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f'#{r:02X}{g:02X}{b:02X}'


def lighten(color_hex, amount=0.5):
    r, g, b = hex_to_rgb(color_hex)
    r = int(r + (255 - r) * amount)
    g = int(g + (255 - g) * amount)
    b = int(b + (255 - b) * amount)
    return rgb_to_hex(r, g, b)


def build_svg(bg, label_color, border_color):
    block = 5          # px per pixel
    avatar_size = 8 * block  # 40px
    gap_x = 14
    pad_x = 16
    pad_y = 12
    label_size = 11
    label_gap = 6

    total_w = pad_x * 2 + 7 * avatar_size + 6 * gap_x
    total_h = pad_y + avatar_size + label_gap + label_size + pad_y

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">',
        f'  <rect width="{total_w}" height="{total_h}" rx="8" fill="{bg}" stroke="{border_color}" stroke-width="1"/>',
    ]

    for i, agent in enumerate(agents):
        main_color = agent['color']
        accent_color = lighten(main_color, 0.5)
        grid = PIXEL_AVATARS[agent['id']]

        ax = pad_x + i * (avatar_size + gap_x)
        ay = pad_y

        for row_idx, row in enumerate(grid):
            for col_idx, val in enumerate(row):
                if val == 0:
                    continue
                fill = main_color if val == 1 else accent_color
                x = ax + col_idx * block
                y = ay + row_idx * block
                lines.append(f'  <rect x="{x}" y="{y}" width="{block}" height="{block}" fill="{fill}"/>')

        label_x = ax + avatar_size // 2
        label_y = ay + avatar_size + label_gap + label_size
        lines.append(
            f'  <text x="{label_x}" y="{label_y}" text-anchor="middle" '
            f'font-family="monospace,Consolas,ui-monospace" font-size="{label_size}" '
            f'fill="{label_color}">{agent["name"]}</text>'
        )

    lines.append('</svg>')
    return '\n'.join(lines), total_w, total_h


assets_dir = r'f:\Project\GitHub\njueeRay\njueeRay-profile\assets'
os.makedirs(assets_dir, exist_ok=True)

# Dark mode
svg_dark, w, h = build_svg(bg='#0d1117', label_color='#8b949e', border_color='#30363d')
dark_path = os.path.join(assets_dir, 'agent-pixel-badge-dark.svg')
with open(dark_path, 'w', encoding='utf-8') as f:
    f.write(svg_dark)

# Light mode
svg_light, _, _ = build_svg(bg='#f6f8fa', label_color='#57606a', border_color='#d0d7de')
light_path = os.path.join(assets_dir, 'agent-pixel-badge-light.svg')
with open(light_path, 'w', encoding='utf-8') as f:
    f.write(svg_light)

print(f'Generated dark:  {dark_path}')
print(f'Generated light: {light_path}')
print(f'Dimensions: {w}x{h}px')
