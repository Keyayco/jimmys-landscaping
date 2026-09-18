"""Generates layered landscape illustrations used as PLACEHOLDER imagery for the
Jimmy's Landscaping site. These are illustrations, not photographs of real work.
Replace the files in assets/img/ with Jimmy's own project photographs.

Run:  python3 gen_images.py
"""
import random, math, os
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img")
os.makedirs(OUT, exist_ok=True)
SS = 2  # supersample factor

SKY = [((216, 228, 220), (246, 241, 230)), ((206, 221, 214), (243, 237, 225)),
       ((199, 215, 209), (238, 232, 219))]
FAR = [(43, 70, 52), (50, 80, 58), (39, 64, 47)]
MID = [(60, 100, 70), (69, 114, 82), (53, 96, 65)]
LAWN = [(93, 143, 82), (106, 154, 91), (83, 133, 74)]
LAWND = [(79, 125, 71), (92, 138, 79), (71, 113, 64)]
SHRUB = [(47, 90, 60), (61, 107, 69), (73, 122, 79), (38, 80, 58), (90, 134, 82)]
STONE = [(222, 215, 199), (213, 205, 187), (230, 223, 208)]
BARK = (74, 58, 44)
FLOWER = [(238, 226, 199), (226, 200, 150), (214, 179, 186), (240, 235, 220), (206, 168, 120)]


def mix(c, d, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c, d))


def canopy(d, rng, cx, cy, r, col, blobs=9):
    for i in range(blobs):
        a = rng.uniform(0, math.tau)
        dist = rng.uniform(0, r * 0.55)
        x, y = cx + math.cos(a) * dist, cy + math.sin(a) * dist * 0.7
        rr = r * rng.uniform(0.45, 0.72)
        shade = mix(col, (255, 255, 255), 0.10) if i % 3 == 0 else col
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=shade)


def tree(d, rng, x, ground, h, col):
    tw = max(6, h * 0.045)
    top = ground - h
    d.rounded_rectangle([x - tw / 2, top + h * 0.30, x + tw / 2, ground], radius=tw / 2, fill=BARK)
    canopy(d, rng, x, top + h * 0.26, h * 0.40, col, 11)


def scene(seed, variant, w, h):
    rng = random.Random(seed)
    W, H = w * SS, h * SS
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img, "RGBA")
    sky_a, sky_b = rng.choice(SKY)
    far, mid = rng.choice(FAR), rng.choice(MID)
    lawn, lawnd, stone = rng.choice(LAWN), rng.choice(LAWND), rng.choice(STONE)
    horizon = H * rng.uniform(0.34, 0.43)

    for y in range(int(horizon) + 1):
        d.line([(0, y), (W, y)], fill=mix(sky_a, sky_b, y / max(1, horizon)))
    x = -40
    while x < W + 80:
        r = rng.uniform(H * 0.05, H * 0.12)
        d.ellipse([x - r, horizon - r * 1.3, x + r, horizon + r * 0.3], fill=far + (235,))
        x += r * rng.uniform(0.7, 1.15)
    for y in range(int(horizon), H):
        t = max(0.0, (y - horizon) / max(1, H - horizon))
        d.line([(0, y), (W, y)], fill=mix(lawnd, lawn, t ** 0.7))

    if variant in ("hedge", "garden", "seating"):
        hy, hh = horizon - H * 0.055, H * 0.13
        d.rounded_rectangle([-20, hy, W + 20, hy + hh], radius=hh * 0.3, fill=mid)
        cx = 0
        while cx < W + 60:
            r = hh * 0.42
            d.ellipse([cx - r, hy + hh * 0.12 - r, cx + r, hy + hh * 0.12 + r], fill=mid)
            cx += hh * 0.5

    if variant in ("lawn", "garden", "seating", "tree"):
        n = 9
        y0 = horizon + H * 0.03
        for i in range(0, n, 2):
            tl = W * (i / n) * 0.55 + W * 0.22
            tr = W * ((i + 1) / n) * 0.55 + W * 0.22
            bl = W * (i / n) * 1.9 - W * 0.45
            br = W * ((i + 1) / n) * 1.9 - W * 0.45
            d.polygon([(tl, y0), (tr, y0), (br, H), (bl, H)], fill=lawnd + (165,))

    if variant in ("paving", "seating", "garden"):
        y0 = horizon + H * 0.09
        d.polygon([(W * 0.40, y0), (W * 0.56, y0), (W * 0.88, H), (W * 0.08, H)], fill=stone)
        rows = 8
        for i in range(1, rows):
            t = (i / rows) ** 1.6
            yy = y0 + (H - y0) * t
            lx = W * 0.40 - (W * 0.32) * t
            rx = W * 0.56 + (W * 0.32) * t
            d.line([(lx, yy), (rx, yy)], fill=(255, 255, 255, 120), width=int(3 * SS))
        edge = mix(stone, (110, 100, 80), 0.35) + (160,)
        d.line([(W * 0.40, y0), (W * 0.08, H)], fill=edge, width=int(3 * SS))
        d.line([(W * 0.56, y0), (W * 0.88, H)], fill=edge, width=int(3 * SS))

    if variant == "seating":
        bx, by = W * 0.63, horizon + H * 0.20
        bw, bh = W * 0.22, H * 0.05
        d.ellipse([bx - 10, by + bh * 2.4, bx + bw + 10, by + bh * 3.1], fill=(0, 0, 0, 40))
        d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10 * SS, fill=(138, 111, 82))
        d.rectangle([bx + 18 * SS, by + bh, bx + 30 * SS, by + bh * 2.6], fill=(111, 88, 63))
        d.rectangle([bx + bw - 30 * SS, by + bh, bx + bw - 18 * SS, by + bh * 2.6], fill=(111, 88, 63))

    beds = 5 if variant in ("garden", "planting") else 3
    for _ in range(beds):
        cx = rng.uniform(W * 0.04, W * 0.96)
        cy = rng.uniform(horizon + H * 0.10, H * 0.93)
        r = rng.uniform(H * 0.05, H * 0.11)
        d.ellipse([cx - r * 1.3, cy + r * 0.35, cx + r * 1.3, cy + r * 0.95], fill=(0, 0, 0, 30))
        canopy(d, rng, cx, cy, r, rng.choice(SHRUB), 7)
        for _ in range(rng.randint(4, 9)):
            a, dd = rng.uniform(0, math.tau), rng.uniform(0, r * 0.6)
            fx, fy = cx + math.cos(a) * dd, cy + math.sin(a) * dd * 0.7
            fr = r * rng.uniform(0.045, 0.075)
            d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=rng.choice(FLOWER))

    count = {"tree": 3, "garden": 2, "hedge": 2, "lawn": 1, "paving": 1, "seating": 2, "planting": 2}[variant]
    for _ in range(count):
        tx = rng.uniform(W * 0.08, W * 0.92)
        th = rng.uniform(H * 0.36, H * 0.58)
        g = horizon + H * 0.20
        d.ellipse([tx - th * 0.30, g - th * 0.05, tx + th * 0.30, g + th * 0.07], fill=(0, 0, 0, 35))
        tree(d, rng, tx, g, th, rng.choice(SHRUB))

    # out-of-focus foliage framing the top corners adds depth
    fg = rng.choice([(32, 62, 44), (38, 72, 50)])
    frame = Image.new("RGB", (W, H), (0, 0, 0))
    fmask = Image.new("L", (W, H), 0)
    fd = ImageDraw.Draw(frame)
    fmd = ImageDraw.Draw(fmask)
    for side in (0, 1):
        ox = 0 if side == 0 else W
        for _ in range(0):
            bx = ox + rng.uniform(-W * 0.06, W * 0.14) * (1 if side == 0 else -1)
            by = rng.uniform(-H * 0.08, H * 0.16)
            br = rng.uniform(H * 0.05, H * 0.11)
            fd.ellipse([bx - br, by - br, bx + br, by + br], fill=fg)
            fmd.ellipse([bx - br, by - br, bx + br, by + br], fill=150)
    frame = frame.filter(ImageFilter.GaussianBlur(13 * SS))
    fmask = fmask.filter(ImageFilter.GaussianBlur(13 * SS))
    img = Image.composite(frame, img, fmask)

    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, H], fill=(255, 240, 210, 14))

    # vignette
    vig = Image.new("L", (W, H), 0)
    ImageDraw.Draw(vig).ellipse([-W * 0.25, -H * 0.3, W * 1.25, H * 1.3], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(H * 0.12))
    img = Image.composite(img, Image.new("RGB", (W, H), (26, 42, 30)), vig.point(lambda v: min(255, int(v * 1.12 + 40))))

    # fine grain so the surfaces are not perfectly flat
    noise = Image.effect_noise((W, H), 14).convert("L")
    img = Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.045)

    img = img.filter(ImageFilter.GaussianBlur(0.35 * SS))
    return img.resize((w, h), Image.LANCZOS)


FILES = {
    "hero-garden": ("garden", 11, 1800, 1150),
    "about-garden": ("tree", 42, 1100, 1300),
    "project-lawn": ("lawn", 3, 1100, 850),
    "project-garden": ("garden", 17, 1100, 850),
    "project-paving": ("paving", 5, 1100, 850),
    "project-hedge": ("hedge", 23, 1100, 850),
    "project-seating": ("seating", 8, 1100, 850),
    "project-planting": ("planting", 31, 1100, 850),
}

if __name__ == "__main__":
    for name, (variant, seed, w, h) in FILES.items():
        p = os.path.join(OUT, name + ".jpg")
        scene(seed, variant, w, h).save(p, "JPEG", quality=80, optimize=True, progressive=True)
        print(name, os.path.getsize(p) // 1024, "KB")
