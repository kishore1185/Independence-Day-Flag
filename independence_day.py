import tkinter as tk
import math, random

root = tk.Tk()
root.title("Independence Day 🇮🇳")

W, H = 600, 400
canvas = tk.Canvas(root, width=W, height=H, bg="white", highlightthickness=0)
canvas.pack()

stageH = 40
stepH = 18
stepW = 180
step_on = False

poleX, poleW, poleH = 200, 6, 250
curHeight = 0

flagH, flagW = 90, 150
waveAngle = 0
flag_on = False
flagScale = 0.1

fireworks = []
fadeVal = 0

def draw_stage():
    canvas.create_rectangle(0, H-stageH, W, H, fill="sienna4", outline="")
    if step_on:
        l = poleX - stepW//2
        r = poleX + poleW + stepW//2
        t = H - stageH - stepH
        canvas.create_rectangle(l, t, r, H-stageH, fill="peru", outline="")
        canvas.create_rectangle(l+10, t-10, r-10, t, fill="burlywood3", outline="")

def draw_pole():
    topY = H - stageH - (stepH if step_on else 0) - curHeight
    botY = H - stageH - (step_on and stepH or 0)
    canvas.create_rectangle(poleX, topY, poleX+poleW, botY, fill="gray20", outline="")
    if curHeight > 0:
        etop = topY - 10
        cx = poleX + poleW//2
        canvas.create_polygon(cx-8, etop+10, cx, etop, cx+8, etop+10, cx+5, etop+16, cx-5, etop+16,
                              fill="#FFD54D", outline="#B8860B", width=1)

def draw_flag(scale=1.0):
    global waveAngle
    waveAngle += 0.12
    stripeH = int((flagH*scale) // 3)
    stripeW = int(flagW*scale)
    cols = ["#FF9933", "white", "#138808"]
    y0 = H - stageH - (stepH if step_on else 0) - poleH
    x0 = poleX + poleW
    for i, c in enumerate(cols):
        y1 = y0 + i*stripeH
        y2 = y1 + stripeH
        pts = []
        for x in range(stripeW+1):
            off = math.sin((x/14)+waveAngle+i*0.4)*5*scale + math.sin((x/45)+waveAngle*0.6)*2*scale
            pts.append((x0+x, y1+off))
        for x in range(stripeW, -1, -1):
            off = math.sin((x/14)+waveAngle+i*0.4)*5*scale + math.sin((x/45)+waveAngle*0.6)*2*scale
            pts.append((x0+x, y2+off))
        canvas.create_polygon(pts, fill=c, outline="black")
    r = stripeH//2
    cx = x0 + stripeW//2
    cy = y0 + stripeH + r
    ring = []
    for ang in range(0, 360, 6):
        rad = math.radians(ang)
        xx = cx + r*math.cos(rad)
        wob = math.sin((ang/57.0)+waveAngle*0.9)*0.8*scale
        yy = cy + r*math.sin(rad) + wob
        ring.append((xx, yy))
    for i in range(len(ring)):
        x1, y1 = ring[i]
        x2, y2 = ring[(i+1)%len(ring)]
        canvas.create_line(x1, y1, x2, y2, fill="#000080", width=2)
    for ang in range(0, 360, 15):
        rad = math.radians(ang)
        sx = cx
        sy = cy + math.sin(waveAngle*0.9)*0.8*scale
        ex = cx + (r-1)*math.cos(rad)
        ey = cy + (r-1)*math.sin(rad) + math.sin((ang/57.0)+waveAngle*0.9)*0.8*scale
        canvas.create_line(sx, sy, ex, ey, fill="#000080", width=1)

def draw_fw():
    for fw in fireworks:
        x, y, rad, col, life = fw
        for a in range(0, 360, 30):
            ang = math.radians(a)
            x2, y2 = x + rad*math.cos(ang), y + rad*math.sin(ang)
            canvas.create_line(x, y, x2, y2, fill=col, width=2)
        fw[2] += 2
        fw[4] -= 1
    fireworks[:] = [fw for fw in fireworks if fw[4] > 0]
    while len(fireworks) < 8:
        fireworks.append([
            random.randint(30, W-30),
            random.randint(30, H-60),
            0,
            random.choice(["red","yellow","orange","white","cyan","magenta","deeppink","lime"]),
            18
        ])
    if random.random() < 0.25:
        fireworks.append([
            random.randint(30, W-30),
            random.randint(30, H-60),
            0,
            random.choice(["red","yellow","orange","white","cyan","magenta","deeppink","lime"]),
            18
        ])

def lerp(a, b, t): return int(a + (b-a)*t)

def blend(c1, c2, t):
    r = lerp(c1[0], c2[0], t)
    g = lerp(c1[1], c2[1], t)
    b = lerp(c1[2], c2[2], t)
    return f"#{r:02x}{g:02x}{b:02x}"

def draw_text():
    global fadeVal
    fadeVal += 0.08
    fade = 0.35 + 0.65*(0.5 + 0.5*math.sin(fadeVal))
    saffron = (255,153,51)
    white = (230,230,230)
    green = (19,136,8)
    txt = "Happy Independence Day"
    baseY = H - stageH + stageH//2
    totalW = len(txt)*10
    startX = W//2 - totalW//2
    for i, ch in enumerate(txt):
        t = i / max(1, len(txt)-1)
        if t < 0.5:
            col = blend(tuple(int(v*fade) for v in saffron),
                        tuple(int(v*fade) for v in white),
                        t/0.5)
        else:
            col = blend(tuple(int(v*fade) for v in white),
                        tuple(int(v*fade) for v in green),
                        (t-0.5)/0.5)
        jitter = random.choice([0,0,0,1,-1])
        canvas.create_text(startX + i*10, baseY + jitter, text=ch,
                           fill=col, font=("Helvetica", 16, "bold"))

def draw_scene(scale=1.0):
    canvas.delete("all")
    draw_stage()
    draw_pole()
    if flag_on:
        draw_flag(scale)
        draw_fw()
        draw_text()

def show_step():
    global step_on
    step_on = True
    draw_scene()
    root.after(450, grow_pole)

def grow_pole():
    global curHeight, flag_on
    if curHeight < poleH:
        curHeight += 3
        draw_scene()
        root.after(18, grow_pole)
    else:
        flag_on = True
        bounce_flag()

def bounce_flag():
    global flagScale
    if flagScale < 1.06:
        flagScale += 0.05
        draw_scene(scale=flagScale)
        root.after(28, bounce_flag)
    else:
        flagScale = 1.0
        animate_flag()

def animate_flag():
    draw_scene()
    root.after(45, animate_flag)

show_step()
root.mainloop()
