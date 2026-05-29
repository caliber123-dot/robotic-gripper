import os
import time
import numpy as np

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from matplotlib.patches import (
    Ellipse,
    Circle,
    Rectangle,
    Arc
)

# =========================================================
# COMMON STYLE
# =========================================================

def engineering_text(ax, x, y, txt, size=24):

    t = ax.text(
        x,
        y,
        txt,

        fontsize=size,
        fontweight='bold',
        family='serif',

        # KEEP TEXT ABOVE ALL OBJECTS
        zorder=20,

        # WHITE BACKGROUND
        bbox=dict(
            facecolor='white',
            edgecolor='none',
            pad=0.15,
            alpha=1.0
        )
    )

    return t


# =========================================================
# SPRING
# =========================================================

def draw_spring(ax, x1, y1, x2, y2, coils=6, width=0.06):

    # MAIN DIRECTION
    dx = x2 - x1
    dy = y2 - y1

    length = np.sqrt(dx**2 + dy**2)

    ux = dx / length
    uy = dy / length

    # PERPENDICULAR VECTOR
    px = -uy
    py = ux

    # START + END OFFSET
    start_offset = 0.12 * length
    end_offset = 0.12 * length

    sx = x1 + ux * start_offset
    sy = y1 + uy * start_offset

    ex = x2 - ux * end_offset
    ey = y2 - uy * end_offset

    # CREATE SPRING POINTS
    xs = [x1, sx]
    ys = [y1, sy]

    step = (length - start_offset - end_offset) / (coils * 2)

    for i in range(coils * 2):

        direction = 1 if i % 2 == 0 else -1

        cx = sx + ux * step * (i + 1)
        cy = sy + uy * step * (i + 1)

        cx += px * width * direction
        cy += py * width * direction

        xs.append(cx)
        ys.append(cy)

    xs.extend([ex, x2])
    ys.extend([ey, y2])

    # DRAW SPRING
    ax.plot(
        xs,
        ys,
        color='black',
        linewidth=2.5,
        solid_joinstyle='miter',
        solid_capstyle='round'
    )
# =========================================================
# DIMENSION ARROW
# =========================================================

def dimension_arrow(ax, x1, y1, x2, y2, txt, txtx, txty):

    ax.annotate(
        '',
        xy=(x1, y1),
        xytext=(x2, y2),
        arrowprops=dict(
            arrowstyle='<->',

            # LINE WIDTH
            lw=2.8,

            color='black',

            # LARGE ARROW HEADS
            mutation_scale=28,

            # CLEAN ENGINEERING STYLE
            shrinkA=0,
            shrinkB=0
        )
    )

    engineering_text(
        ax,
        txtx,
        txty,
        txt,
        16
    )

# =========================================================
# SPHERE shape
# =========================================================

def generate_sphere(R):

    # fig, ax = plt.subplots(figsize=(8,8))
    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # OBJECT
    circle = Circle(
        (0,0),
        R,
        facecolor='#dddddd',
        edgecolor='black',
        linewidth=2
    )

    ax.add_patch(circle)

    # AXIS
    ax.plot([-1.2*R,1.2*R],[0,0],'--',color='black')
    ax.plot([0,0],[-1.2*R,1.2*R],'--',color='black')

    # CENTER
    ax.plot(0,0,'ko',markersize=10)

    engineering_text(ax,0.08*R,-0.1*R,'C',32)

    # CONTACT POINTS
    th = np.radians(130)

    x = R*np.cos(th)
    y = R*np.sin(th)

    ax.plot(x,y,'ko',markersize=10)

    # engineering_text(ax,x-0.5*R,y+0.1*R,r'$A_i$',28)
    # CONTACT LABEL A_i
    engineering_text(
        ax,
        x-0.15*R,
        y-0.18*R,
        r'$A_i$',
        24
    )

    # FOOTER TITLE
    engineering_text(
        ax,
        -1.6*R,
        -1.75*R,
        "Fig. 2: Typical Grasp Postures for Objects of Shapes: SPHERICAL",
        14
    )

    # RADIUS
    ax.plot([0,x],[0,y],'--',color='black')

    engineering_text(ax,x*0.4,y*0.4,'r',28)

    # THETA
    arc = Arc(
        (0,0),
        0.5*R,
        0.5*R,
        theta1=130,
        theta2=180,
        linewidth=2
    )

    ax.add_patch(arc)

    engineering_text(ax,-0.25*R,0.1*R,r'$\theta$',28)

    # SPRING
    draw_spring(
        ax,
        x-1.05*R,
        y+0.45*R,
        x,
        y,
        coils=7,
        width=0.07*R
    )

    # FORCE
    ax.annotate(
        '',
        xy=(x,y),
        xytext=(x-0.5*R,y+0.2*R),
        arrowprops=dict(
            arrowstyle='simple',
            color='black'
        )
    )

    engineering_text(
        ax,
        x-0.7*R,
        y+0.35*R,
        r'$\Delta S$',
        28
    )

    # DIMENSION SPHERE
   # =========================================
    # RADIUS DIMENSION (HALF ONLY)
    # =========================================

    radius_txt = f"Radius = {R:.2f} mm"

    dimension_arrow(
        ax,
        0,          # start from center
        -1.2*R,
        R,          # end at circle edge
        -1.2*R,
        radius_txt,
        0.15*R,
        -1.38*R
    )

    # ax.set_xlim(-1.7*R,1.7*R)
    # ax.set_ylim(-1.5*R,1.5*R)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    os.makedirs("static/generated",exist_ok=True)

    # fname = f"sphere_{time.time()}.png"
    fname = "sphere.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,
        dpi=128,
        bbox_inches=None
    )

    plt.close()

    return path


# =========================================================
# RECTANGLE shape
# =========================================================

def generate_rectangle(L,B):

    # fig, ax = plt.subplots(figsize=(10,6))
    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    rect = Rectangle(
        (0,0),
        L,
        B,
        facecolor='#dddddd',
        edgecolor='black',
        linewidth=2
    )

    ax.add_patch(rect)

    # CENTER
    cx = L/2
    cy = B/2

    ax.plot(cx,cy,'ko',markersize=10)

    # AXIS
    ax.plot([cx,cx],[-0.2*B,1.2*B],'--',color='black')
    ax.plot([-0.2*L,1.2*L],[cy,cy],'--',color='black')

    engineering_text(ax,cx+0.05*L,cy-0.1*B,'C',30)

    # CONTACT
    x = 0
    y = 0.7*B

    ax.plot(x,y,'ko',markersize=10)

    # engineering_text(ax,-0.2*L,y+0.05*B,r'$A_i$',28)
    # CONTACT LABEL A_i
    engineering_text(
        ax,
        x-0.09*L,      # move near contact point
        y+0.12*B,      # move ABOVE line
        r'$A_i$',
        24
    )
    # FOOTER TITLE
    engineering_text(
        ax,
        -0.60*L,
        -0.75*B,
        "Fig. 2: Typical Grasp Postures for Objects of Shapes: RECTANGULAR",
        14
    )

    # RADIUS
    ax.plot([cx,x],[cy,y],'--',color='black')

    engineering_text(ax,0.25*L,0.65*B,'r',28)

    # THETA
    arc = Arc(
        (cx,cy),
        0.25*L,
        0.25*L,
        theta1=130,
        theta2=180,
        linewidth=2
    )

    ax.add_patch(arc)

    engineering_text(ax,0.38*L,0.52*B,r'$\theta$',18)

    # SPRING
    # draw_spring(
    #     ax,
    #     -0.7*L,
    #     y+0.25*B,
    #     x,
    #     y
    # )
    # SPRING RECTANGLE
    draw_spring(
        ax,
        -0.85*L,
        y+0.30*B,
        x,
        y,
        coils=7,
        width=0.05*L
    )

    # FORCE
    ax.annotate(
        '',
        xy=(x,y),
        xytext=(-0.25*L,y+0.08*B),
        arrowprops=dict(
            arrowstyle='simple',
            color='black'
        )
    )

    engineering_text(
        ax,
        -0.45*L,
        y+0.18*B,
        r'$\Delta S$',
        28
    )

    # DIMENSION RECTANGLE
    # DIMENSION TEXT
    length_txt = f"Length = {L:.2f} mm"
    breadth_txt = f"Breadth = {B:.2f} mm"

    # LENGTH
    dimension_arrow(
        ax,
        0,
        -0.2*B,
        L,
        -0.2*B,
        length_txt,
        0.20*L,
        -0.38*B
    )

    # BREADTH
    dimension_arrow(
        ax,
        -0.15*L,
        0,
        -0.15*L,
        B,
        breadth_txt,
        -0.75*L,
        0.45*B
    )

    ax.set_xlim(-0.9*L,1.2*L)
    ax.set_ylim(-0.4*B,1.2*B)

    os.makedirs("static/generated",exist_ok=True)

    # fname = f"rect_{time.time()}.png"
    fname = "rectangle.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,
        dpi=128,
        bbox_inches=None
    )

    plt.close()

    return path


# =========================================================
# 3D RECTANGLE (ENGINEERING STYLE)
# =========================================================

def generate_rectangle_3d(L, B, H=40):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # 3D DEPTH OFFSET
    # =====================================================

    dx = 0.18 * L
    dy = 0.12 * B

    # =====================================================
    # FRONT FACE
    # =====================================================

    front = Rectangle(
        (0, 0),
        L,
        B,
        facecolor='#dddddd',
        edgecolor='black',
        linewidth=2.5,
        zorder=2
    )

    ax.add_patch(front)

    # =====================================================
    # BACK FACE
    # =====================================================

    back = Rectangle(
        (dx, dy),
        L,
        B,
        facecolor='#efefef',
        edgecolor='black',
        linewidth=2.5,
        zorder=1
    )

    ax.add_patch(back)

    # =====================================================
    # CONNECT EDGES
    # =====================================================

    front_pts = [
        (0,0),
        (L,0),
        (L,B),
        (0,B)
    ]

    back_pts = [
        (dx,dy),
        (L+dx,dy),
        (L+dx,B+dy),
        (dx,B+dy)
    ]

    for (x1,y1),(x2,y2) in zip(
        front_pts,
        back_pts
    ):

        ax.plot(
            [x1,x2],
            [y1,y2],
            color='black',
            linewidth=2
        )

    # =====================================================
    # CENTER
    # =====================================================

    cx = L/2
    cy = B/2

    ax.plot(
        cx,
        cy,
        'ko',
        markersize=10
    )

    engineering_text(
        ax,
        cx + 0.05*L,
        cy - 0.1*B,
        'C',
        30
    )

    # =====================================================
    # AXIS
    # =====================================================

    ax.plot(
        [cx,cx],
        [-0.2*B,1.2*B],
        '--',
        color='black'
    )

    ax.plot(
        [-0.2*L,1.3*L],
        [cy,cy],
        '--',
        color='black'
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    x = 0
    y = 0.7 * B

    ax.plot(
        x,
        y,
        'ko',
        markersize=10
    )

    engineering_text(
        ax,
        x - 0.09*L,
        y + 0.12*B,
        r'$A_i$',
        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [cx,x],
        [cy,y],
        '--',
        color='black'
    )

    engineering_text(
        ax,
        0.25*L,
        0.65*B,
        'r',
        28
    )

    # =====================================================
    # THETA
    # =====================================================

    arc = Arc(
        (cx,cy),
        0.25*L,
        0.25*L,
        theta1=130,
        theta2=180,
        linewidth=2.5
    )

    ax.add_patch(arc)

    engineering_text(
        ax,
        0.38*L,
        0.52*B,
        r'$\theta$',
        18
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,
        -0.85*L,
        y + 0.30*B,
        x,
        y,
        coils=7,
        width=0.05*L
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',
        xy=(x,y),
        xytext=(-0.25*L,y+0.08*B),

        arrowprops=dict(
            arrowstyle='simple',
            color='black'
        )
    )

    engineering_text(
        ax,
        -0.45*L,
        y + 0.18*B,
        r'$\Delta S$',
        28
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    length_txt = f"Length = {L:.2f} mm"

    breadth_txt = f"Breadth = {B:.2f} mm"

    # LENGTH
    dimension_arrow(
        ax,
        0,
        -0.22*B,
        L,
        -0.22*B,
        length_txt,
        0.20*L,
        -0.40*B
    )

    # BREADTH
    dimension_arrow(
        ax,
        -0.15*L,
        0,
        -0.15*L,
        B,
        breadth_txt,
        -0.75*L,
        0.45*B
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,
        -0.60*L,
        -0.82*B,
        "Fig. 2: Typical Grasp Postures for Objects of Shapes: RECTANGULAR",
        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -0.9*L,
        1.45*L
    )

    ax.set_ylim(
        -0.5*B,
        1.35*B
    )

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "rectangle3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,
        dpi=128,
        bbox_inches=None
    )

    plt.close()

    return path


# =========================================================
# ELLIPSOID shape
# =========================================================

def generate_ellipsoid(a,b):

    # fig, ax = plt.subplots(figsize=(10,8))
    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    ellipse = Ellipse(
        (0,0),
        width=2*a,
        height=2*b,
        facecolor='#dddddd',
        edgecolor='black',
        linewidth=2
    )

    ax.add_patch(ellipse)

    # AXIS
    ax.plot([-1.3*a,1.3*a],[0,0],'--',color='black')
    ax.plot([0,0],[-1.3*b,1.3*b],'--',color='black')

    # CENTER
    ax.plot(0,0,'ko',markersize=10)

    engineering_text(ax,0.08*a,-0.1*b,'C',32)

    # CONTACT
    th = np.radians(145)

    x = a*np.cos(th)
    y = b*np.sin(th)

    ax.plot(x,y,'ko',markersize=10)

    engineering_text(ax,x-0.3*a,y-0.15*b,r'$A_i$',28)

    # FOOTER TITLE
    engineering_text(
        ax,
        -1.40*a,
        -1.75*b,
        "Fig. 2: Typical Grasp Postures for Objects of Shapes: ELLIPSOIDAL",
        14
    )

    # RADIUS
    ax.plot([0,x],[0,y],'--',color='black')

    engineering_text(ax,x*0.45,y*0.45,'r',28)

    # THETA
    arc = Arc(
        (0,0),
        0.4*a,
        0.4*a,
        theta1=145,
        theta2=180,
        linewidth=2
    )

    ax.add_patch(arc)

    engineering_text(ax,-0.18*a,0.1*b,r'$\theta$',18)

    # SPRING ELLIPSOID
    # draw_spring(
    #     ax,
    #     x-1.1*a,
    #     y+0.5*b,
    #     x,
    #     y
    # )
    # SPRING ELLIPSOID
    draw_spring(
        ax,
        x-1.00*a,
        y+0.45*b,
        x,
        y,
        coils=7,
        width=0.06*a
    )

    # FORCE
    ax.annotate(
        '',
        xy=(x,y),
        xytext=(x-0.35*a,y+0.18*b),
        arrowprops=dict(
            arrowstyle='simple',
            color='black'
        )
    )

    engineering_text(
        ax,
        x-0.55*a,
        y+0.35*b,
        r'$\Delta S$',
        28
    )

    # ELLIPSOID
    # DIMENSIONS
    major_txt = f"Rmajor = {a:.2f} mm"
    minor_txt = f"Rminor = {b:.2f} mm"

    # MAJOR
    dimension_arrow(
        ax,
        -a,
        -1.2*b,
        a,
        -1.2*b,
        major_txt,
        -0.45*a,
        -1.38*b
    )

    # MINOR
    dimension_arrow(
        ax,
        -1.15*a,
        -b,
        -1.15*a,
        b,
        minor_txt,
        -2.0*a,
        0
    )

    ax.set_xlim(-1.8*a,1.6*a)
    ax.set_ylim(-1.5*b,1.6*b)

    os.makedirs("static/generated",exist_ok=True)

    # fname = f"ellipse_{time.time()}.png"
    fname = "ellipse.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    # plt.savefig(
    #     path,
    #     bbox_inches='tight',
    #     dpi=300
    # )
    plt.savefig(
        path,
        dpi=128,
        bbox_inches=None
    )

    plt.close()

    return path

# =========================================================
# 3D ELLIPSOID (ENGINEERING STYLE)
# =========================================================

def generate_ellipsoid_3d(a, b):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # DEPTH OFFSET
    # =====================================================

    dx = 0.35 * a
    dy = 0.22 * b

    # =====================================================
    # BACK ELLIPSOID
    # =====================================================

    back = Ellipse(
        (dx,dy),

        width=2*a,
        height=2*b,

        facecolor='#efefef',
        edgecolor='black',

        linewidth=2.5,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT ELLIPSOID
    # =====================================================

    front = Ellipse(
        (0,0),

        width=2*a,
        height=2*b,

        facecolor='#dddddd',
        edgecolor='black',

        linewidth=2.5,

        zorder=1
    )

    ax.add_patch(front)

    # =====================================================
    # CONNECT EDGE LINES
    # =====================================================

    angles = [45, 135, 225, 315]

    for ang in angles:

        t = np.radians(ang)

        x1 = a * np.cos(t)
        y1 = b * np.sin(t)

        x2 = x1 + dx
        y2 = y1 + dy

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=2
        )

    # =====================================================
    # ENGINEERING CENTER AXIS
    # =====================================================

    # centerline = (0, (10, 3, 2, 3))
    centerline = '--'

    # HORIZONTAL AXIS
    ax.plot(
        [-1.5*a, 1.9*a],
        [0, 0],

        linestyle=centerline,

        color='black',

        linewidth=1.8,

        zorder=20
    )

    # VERTICAL AXIS
    ax.plot(
        [0, 0],
        [-1.4*b, 1.6*b],

        linestyle=centerline,

        color='black',

        linewidth=1.8,

        zorder=20
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        0,
        0,
        'ko',

        markersize=10,

        zorder=30
    )

    engineering_text(
        ax,
        0.08*a,
        -0.1*b,
        'C',
        32
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    th = np.radians(145)

    x = a * np.cos(th)
    y = b * np.sin(th)

    ax.plot(
        x,
        y,
        'ko',

        markersize=10,

        zorder=30
    )

    engineering_text(
        ax,
        x - 0.28*a,
        y - 0.12*b,
        r'$A_i$',
        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [0,x],
        [0,y],

        '--',

        color='black',

        linewidth=2,

        zorder=25
    )

    engineering_text(
        ax,
        x * 0.45,
        y * 0.45,
        'r',
        28
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (0,0),

        0.45*a,
        0.45*a,

        theta1=145,
        theta2=180,

        linewidth=2.5,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,
        -0.16*a,
        0.08*b,
        r'$\theta$',
        18
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        x - 1.0*a,
        y + 0.45*b,

        x,
        y,

        coils=7,
        width=0.06*a
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            x - 0.35*a,
            y + 0.18*b
        ),

        arrowprops=dict(
            arrowstyle='simple',
            color='black'
        )
    )

    engineering_text(
        ax,
        x - 0.55*a,
        y + 0.35*b,
        r'$\Delta S$',
        28
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    major_txt = f"Rmajor = {a:.2f} mm"

    minor_txt = f"Rminor = {b:.2f} mm"

    # MAJOR AXIS
    dimension_arrow(
        ax,

        -a,
        -1.2*b,

        a,
        -1.2*b,

        major_txt,

        -0.45*a,
        -1.38*b
    )

    # MINOR AXIS
    dimension_arrow(
        ax,

        -1.15*a,
        -b,

        -1.15*a,
        b,

        minor_txt,

        -2.0*a,
        0
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,

        -1.45*a,
        -1.75*b,

        "Fig. 2: Typical Grasp Postures for Objects of Shapes: ELLIPSOIDAL",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -2.1*a,
        2.2*a
    )

    ax.set_ylim(
        -1.7*b,
        1.9*b
    )

    # =====================================================
    # SAVE IMAGE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "ellipse3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# =========================================================
# 3D SPHERE (ENGINEERING STYLE)
# =========================================================

def generate_sphere_3d(R):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # DEPTH OFFSET
    # =====================================================

    dx = 0.28 * R
    dy = 0.20 * R

    # =====================================================
    # BACK SPHERE
    # =====================================================

    back = Circle(
        (dx,dy),

        R,

        facecolor='#efefef',
        edgecolor='black',

        linewidth=2.5,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT SPHERE
    # =====================================================

    front = Circle(
        (0,0),

        R,

        facecolor='#dddddd',
        edgecolor='black',

        linewidth=2.5,

        zorder=1
    )

    ax.add_patch(front)

    # =====================================================
    # CONNECT EDGES
    # =====================================================

    angles = [45, 135, 225, 315]

    for ang in angles:

        t = np.radians(ang)

        x1 = R * np.cos(t)
        y1 = R * np.sin(t)

        x2 = x1 + dx
        y2 = y1 + dy

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=2
        )

    # =====================================================
    # AXIS
    # =====================================================

    ax.plot(
        [-1.25*R, 1.55*R],
        [0,0],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    ax.plot(
        [0,0],
        [-1.25*R, 1.45*R],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        0,
        0,

        'ko',

        markersize=10,

        zorder=30
    )

    engineering_text(
        ax,
        0.08*R,
        -0.1*R,

        'C',

        32
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    th = np.radians(130)

    x = R * np.cos(th)
    y = R * np.sin(th)

    ax.plot(
        x,
        y,

        'ko',

        markersize=10,

        zorder=30
    )

    engineering_text(
        ax,
        x - 0.16*R,
        y - 0.18*R,

        r'$A_i$',

        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [0,x],
        [0,y],

        '--',

        color='black',

        linewidth=2,

        zorder=25
    )

    engineering_text(
        ax,
        x * 0.42,
        y * 0.42,

        'r',

        28
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (0,0),

        0.5*R,
        0.5*R,

        theta1=130,
        theta2=180,

        linewidth=2.5,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,
        -0.22*R,
        0.10*R,

        r'$\theta$',

        28
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        x - 1.05*R,
        y + 0.45*R,

        x,
        y,

        coils=7,
        width=0.07*R
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            x - 0.5*R,
            y + 0.2*R
        ),

        arrowprops=dict(
            arrowstyle='simple',
            color='black'
        )
    )

    engineering_text(
        ax,
        x - 0.7*R,
        y + 0.35*R,

        r'$\Delta S$',

        28
    )

    # =====================================================
    # DIMENSION
    # =====================================================

    radius_txt = f"Radius = {R:.2f} mm"

    dimension_arrow(
        ax,

        0,
        -1.22*R,

        R,
        -1.22*R,

        radius_txt,

        0.20*R,
        -1.42*R
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,

        -1.65*R,
        -1.85*R,

        "Fig. 2: Typical Grasp Postures for Objects of Shapes: SPHERICAL",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -1.8*R,
        2.0*R
    )

    ax.set_ylim(
        -1.6*R,
        1.8*R
    )

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "sphere3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# =========================================================
# 3D SPHERE (SOLIDWORKS STYLE)
# =========================================================

def generate_sphere_3d_2(R):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # DEPTH OFFSET
    # =====================================================

    dx = 0.30 * R
    dy = 0.22 * R

    # =====================================================
    # BACK SPHERE
    # =====================================================

    back = Circle(
        (dx,dy),

        R,

        facecolor='#f0f0f0',

        edgecolor='black',

        linewidth=2.5,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT SPHERE
    # =====================================================

    front = Circle(
        (0,0),

        R,

        facecolor='#d9d9d9',

        edgecolor='black',

        linewidth=3,

        zorder=2
    )

    ax.add_patch(front)

    # =====================================================
    # SHADOW
    # =====================================================

    shadow = Circle(
        (0.18*R,-0.18*R),

        0.92*R,

        facecolor='black',

        edgecolor='none',

        alpha=0.08,

        zorder=3
    )

    ax.add_patch(shadow)

    # =====================================================
    # HIGHLIGHT
    # =====================================================

    highlight = Circle(
        (-0.30*R,0.32*R),

        0.45*R,

        facecolor='white',

        edgecolor='none',

        alpha=0.35,

        zorder=4
    )

    ax.add_patch(highlight)

    # =====================================================
    # CONNECT EDGE LINES
    # =====================================================

    angles = [45, 135, 225, 315]

    for ang in angles:

        t = np.radians(ang)

        x1 = R * np.cos(t)
        y1 = R * np.sin(t)

        x2 = x1 + dx
        y2 = y1 + dy

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=1
        )

    # =====================================================
    # WIREFRAME ELLIPSE
    # =====================================================

    theta = np.linspace(0, 2*np.pi, 400)

    wx = R*np.cos(theta)
    wy = 0.38*R*np.sin(theta)

    ax.plot(
        wx,
        wy,

        '--',

        color='black',

        linewidth=1.5,

        alpha=0.5,

        zorder=5
    )

    # =====================================================
    # ENGINEERING AXIS
    # =====================================================

    ax.plot(
        [-1.3*R,1.6*R],
        [0,0],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    ax.plot(
        [0,0],
        [-1.3*R,1.5*R],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        0,
        0,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        0.08*R,
        -0.1*R,

        'C',

        34
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    th = np.radians(130)

    x = R*np.cos(th)
    y = R*np.sin(th)

    ax.plot(
        x,
        y,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        x-0.18*R,
        y-0.20*R,

        r'$A_i$',

        26
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [0,x],
        [0,y],

        '--',

        color='black',

        linewidth=2.2,

        zorder=25
    )

    engineering_text(
        ax,

        x*0.42,
        y*0.42,

        'r',

        30
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (0,0),

        0.52*R,
        0.52*R,

        theta1=130,
        theta2=180,

        linewidth=2.8,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        -0.24*R,
        0.10*R,

        r'$\theta$',

        30
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        x-1.10*R,
        y+0.45*R,

        x,
        y,

        coils=8,

        width=0.08*R
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            x-0.55*R,
            y+0.22*R
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        x-0.75*R,
        y+0.38*R,

        r'$\Delta S$',

        32
    )

    # =====================================================
    # DIMENSION
    # =====================================================

    radius_txt = f"Radius = {R:.2f} mm"

    dimension_arrow(
        ax,

        0,
        -1.22*R,

        R,
        -1.22*R,

        radius_txt,

        0.18*R,
        -1.42*R
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,

        -1.70*R,
        -1.90*R,

        "Fig. 2: Typical Grasp Postures for Objects of Shapes: SPHERICAL",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    # ax.set_xlim(
    #     -1.9*R,
    #     2.1*R
    # )

    # ax.set_ylim(
    #     -1.7*R,
    #     1.9*R
    # )

    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "sphere3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# =========================================================
# 3D ELLIPSOID (SOLIDWORKS STYLE)
# =========================================================

def generate_ellipsoid_3d_2(a, b):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # DEPTH OFFSET
    # =====================================================

    dx = 0.38 * a
    dy = 0.24 * b

    # =====================================================
    # BACK ELLIPSOID
    # =====================================================

    back = Ellipse(
        (dx,dy),

        width=2*a,
        height=2*b,

        facecolor='#f0f0f0',

        edgecolor='black',

        linewidth=2.5,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT ELLIPSOID
    # =====================================================

    front = Ellipse(
        (0,0),

        width=2*a,
        height=2*b,

        facecolor='#d9d9d9',

        edgecolor='black',

        linewidth=3,

        zorder=2
    )

    ax.add_patch(front)

    # =====================================================
    # SHADOW
    # =====================================================

    shadow = Ellipse(
        (0.15*a,-0.15*b),

        width=1.75*a,
        height=1.75*b,

        facecolor='black',

        edgecolor='none',

        alpha=0.08,

        zorder=3
    )

    ax.add_patch(shadow)

    # =====================================================
    # HIGHLIGHT
    # =====================================================

    highlight = Ellipse(
        (-0.32*a,0.32*b),

        width=0.60*a,
        height=0.45*b,

        facecolor='white',

        edgecolor='none',

        alpha=0.35,

        zorder=4
    )

    ax.add_patch(highlight)

    # =====================================================
    # CONNECT EDGE LINES
    # =====================================================

    angles = [45, 135, 225, 315]

    for ang in angles:

        t = np.radians(ang)

        x1 = a*np.cos(t)
        y1 = b*np.sin(t)

        x2 = x1 + dx
        y2 = y1 + dy

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=1
        )

    # =====================================================
    # WIREFRAME ELLIPSE
    # =====================================================

    theta = np.linspace(0, 2*np.pi, 500)

    wx = a*np.cos(theta)
    wy = 0.38*b*np.sin(theta)

    ax.plot(
        wx,
        wy,

        '--',

        color='black',

        linewidth=1.5,

        alpha=0.45,

        zorder=5
    )

    # =====================================================
    # ENGINEERING AXIS
    # =====================================================

    ax.plot(
        [-1.45*a,1.85*a],
        [0,0],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    ax.plot(
        [0,0],
        [-1.4*b,1.55*b],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        0,
        0,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        0.08*a,
        -0.1*b,

        'C',

        34
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    th = np.radians(145)

    x = a*np.cos(th)
    y = b*np.sin(th)

    ax.plot(
        x,
        y,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        x-0.28*a,
        y-0.14*b,

        r'$A_i$',

        26
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [0,x],
        [0,y],

        '--',

        color='black',

        linewidth=2.2,

        zorder=25
    )

    engineering_text(
        ax,

        x*0.45,
        y*0.45,

        'r',

        30
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (0,0),

        0.45*a,
        0.45*a,

        theta1=145,
        theta2=180,

        linewidth=2.8,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        -0.18*a,
        0.08*b,

        r'$\theta$',

        24
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        x-1.05*a,
        y+0.45*b,

        x,
        y,

        coils=8,

        width=0.07*a
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            x-0.38*a,
            y+0.18*b
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        x-0.68*a,
        y+0.35*b,

        r'$\Delta S$',

        30
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    major_txt = f"Rmajor = {a:.2f} mm"

    minor_txt = f"Rminor = {b:.2f} mm"

    # MAJOR
    dimension_arrow(
        ax,

        -a,
        -1.22*b,

        a,
        -1.22*b,

        major_txt,

        -0.45*a,
        -1.40*b
    )

    # MINOR
    dimension_arrow(
        ax,

        -1.15*a,
        -b,

        -1.15*a,
        b,

        minor_txt,

        -2.0*a,
        0
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,

        -1.50*a,
        -1.78*b,

        "Fig. 2: Typical Grasp Postures for Objects of 3D Shapes: ELLIPSOIDAL",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -2.0*a,
        2.3*a
    )

    ax.set_ylim(
        -1.7*b,
        1.9*b
    )

    # =====================================================
    # SAVE IMAGE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "ellipse3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# =========================================================
# 3D RECTANGLE (SOLIDWORKS STYLE)
# =========================================================

def generate_rectangle_3d_2(L, B, H=40):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # DEPTH OFFSET
    # =====================================================

    dx = 0.22 * L
    dy = 0.15 * B

    # =====================================================
    # BACK FACE
    # =====================================================

    back = Rectangle(
        (dx,dy),

        L,
        B,

        facecolor='#f0f0f0',

        edgecolor='black',

        linewidth=2.5,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT FACE
    # =====================================================

    front = Rectangle(
        (0,0),

        L,
        B,

        facecolor='#d9d9d9',

        edgecolor='black',

        linewidth=3,

        zorder=2
    )

    ax.add_patch(front)

    # =====================================================
    # SHADOW
    # =====================================================

    shadow = Rectangle(
        (0.08*L,-0.08*B),

        0.95*L,
        0.95*B,

        facecolor='black',

        edgecolor='none',

        alpha=0.08,

        zorder=3
    )

    ax.add_patch(shadow)

    # =====================================================
    # HIGHLIGHT
    # =====================================================

    highlight = Rectangle(
        (0.10*L,0.60*B),

        0.42*L,
        0.16*B,

        facecolor='white',

        edgecolor='none',

        alpha=0.30,

        zorder=4
    )

    ax.add_patch(highlight)

    # =====================================================
    # CONNECT EDGE LINES
    # =====================================================

    front_pts = [
        (0,0),
        (L,0),
        (L,B),
        (0,B)
    ]

    back_pts = [
        (dx,dy),
        (L+dx,dy),
        (L+dx,B+dy),
        (dx,B+dy)
    ]

    for (x1,y1),(x2,y2) in zip(
        front_pts,
        back_pts
    ):

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=1
        )

    # =====================================================
    # WIREFRAME
    # =====================================================

    ax.plot(
        [0,L],
        [B/2,B/2],

        '--',

        color='black',

        linewidth=1.5,

        alpha=0.45,

        zorder=5
    )

    ax.plot(
        [L/2,L/2],
        [0,B],

        '--',

        color='black',

        linewidth=1.5,

        alpha=0.45,

        zorder=5
    )

    # =====================================================
    # ENGINEERING AXIS
    # =====================================================

    cx = L/2
    cy = B/2

    ax.plot(
        [cx,cx],
        [-0.25*B,1.30*B],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    ax.plot(
        [-0.25*L,1.35*L],
        [cy,cy],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        cx,
        cy,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        cx+0.05*L,
        cy-0.1*B,

        'C',

        34
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    x = 0
    y = 0.70 * B

    ax.plot(
        x,
        y,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        x-0.11*L,
        y+0.10*B,

        r'$A_i$',

        26
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [cx,x],
        [cy,y],

        '--',

        color='black',

        linewidth=2.2,

        zorder=25
    )

    engineering_text(
        ax,

        0.25*L,
        0.65*B,

        'r',

        30
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (cx,cy),

        0.28*L,
        0.28*L,

        theta1=130,
        theta2=180,

        linewidth=2.8,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        0.38*L,
        0.52*B,

        r'$\theta$',

        28
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        -0.90*L,
        y+0.32*B,

        x,
        y,

        coils=8,

        width=0.06*L
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            -0.28*L,
            y+0.10*B
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        -0.48*L,
        y+0.20*B,

        r'$\Delta S$',

        32
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    length_txt = f"Length = {L:.2f} mm"

    breadth_txt = f"Breadth = {B:.2f} mm"

    # LENGTH
    dimension_arrow(
        ax,

        0,
        -0.22*B,

        L,
        -0.22*B,

        length_txt,

        0.20*L,
        -0.42*B
    )

    # BREADTH
    dimension_arrow(
        ax,

        -0.15*L,
        0,

        -0.15*L,
        B,

        breadth_txt,

        -0.78*L,
        0.45*B
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,

        -0.70*L,
        -0.85*B,

        "Fig. 2: Typical Grasp Postures for Objects of Shapes: RECTANGULAR",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -1.0*L,
        1.55*L
    )

    ax.set_ylim(
        -0.55*B,
        1.45*B
    )

    # =====================================================
    # SAVE IMAGE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "rectangle3d_2.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# ========================= VERTICAL ================================
# VERTICAL RECTANGLE (2D ENGINEERING STYLE) VERTICAL
# =========================================================

def generate_rectangle_vertical(L, B):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # RECTANGLE
    # =====================================================

    rect = Rectangle(
        (0,0),

        B,     # horizontal breadth
        L,     # vertical length

        facecolor='#dddddd',

        edgecolor='black',

        linewidth=2.5
    )

    ax.add_patch(rect)

    # =====================================================
    # CENTER
    # =====================================================

    cx = B / 2
    cy = L / 2

    ax.plot(
        cx,
        cy,

        'ko',

        markersize=10
    )

    engineering_text(
        ax,
        cx + 0.06*B,
        cy - 0.08*L,

        'C',

        32
    )

    # =====================================================
    # AXIS
    # =====================================================

    ax.plot(
        [cx,cx],
        [-0.15*L,1.15*L],

        '--',

        color='black',

        linewidth=2
    )

    ax.plot(
        [-0.6*B,1.3*B],
        [cy,cy],

        '--',

        color='black',

        linewidth=2
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    x = 0
    y = 0.82 * L

    ax.plot(
        x,
        y,

        'ko',

        markersize=10
    )

    engineering_text(
        ax,

        x - 0.16*B,
        y + 0.05*L,

        r'$A_i$',

        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [cx,x],
        [cy,y],

        '--',

        color='black',

        linewidth=2
    )

    engineering_text(
        ax,

        0.30*B,
        0.70*L,

        'r',

        28
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (cx,cy),

        0.40*B,
        0.40*B,

        theta1=125,
        theta2=180,

        linewidth=2.5
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        0.33*B,
        0.56*L,

        r'$\theta$',

        20
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        -1.2*B,
        y + 0.18*L,

        x,
        y,

        coils=7,

        width=0.07*B
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            -0.35*B,
            y + 0.05*L
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        -0.65*B,
        y + 0.12*L,

        r'$\Delta S$',

        30
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    length_txt = f"Length = {L:.2f} mm"

    breadth_txt = f"Breadth = {B:.2f} mm"

    # LENGTH
    dimension_arrow(
        ax,

        -0.18*B,
        0,

        -0.18*B,
        L,

        length_txt,

        -0.95*B,
        0.50*L
    )

    # BREADTH
    dimension_arrow(
        ax,

        0,
        -0.10*L,

        B,
        -0.10*L,

        breadth_txt,

        0.18*B,
        -0.22*L
    )

    # =====================================================
    # FOOTER TITLE
    # =====================================================

    engineering_text(
        ax,

        -1.20*B,
        -0.32*L,

        "Fig. 2: Typical Grasp Postures for Objects of Shapes: RECTANGULAR",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -1.4*B,
        1.4*B
    )

    ax.set_ylim(
        -0.25*L,
        1.12*L
    )

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "rectangle_vertical.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# =========================================================
# 3D VERTICAL RECTANGLE (ENGINEERING STYLE)
# =========================================================

def generate_rectangle_vertical_3d(L, B, H=40):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # DEPTH OFFSET
    # =====================================================

    dx = 0.25 * B
    dy = 0.12 * L

    # =====================================================
    # BACK FACE
    # =====================================================

    back = Rectangle(
        (dx,dy),

        B,
        L,

        facecolor='#f0f0f0',

        edgecolor='black',

        linewidth=2.5,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT FACE
    # =====================================================

    front = Rectangle(
        (0,0),

        B,
        L,

        facecolor='#d9d9d9',

        edgecolor='black',

        linewidth=3,

        zorder=2
    )

    ax.add_patch(front)

    # =====================================================
    # SHADOW
    # =====================================================

    shadow = Rectangle(
        (0.05*B,-0.04*L),

        0.96*B,
        0.96*L,

        facecolor='black',

        edgecolor='none',

        alpha=0.08,

        zorder=3
    )

    ax.add_patch(shadow)

    # =====================================================
    # HIGHLIGHT
    # =====================================================

    highlight = Rectangle(
        (0.12*B,0.68*L),

        0.32*B,
        0.14*L,

        facecolor='white',

        edgecolor='none',

        alpha=0.30,

        zorder=4
    )

    ax.add_patch(highlight)

    # =====================================================
    # CONNECT EDGES
    # =====================================================

    front_pts = [
        (0,0),
        (B,0),
        (B,L),
        (0,L)
    ]

    back_pts = [
        (dx,dy),
        (B+dx,dy),
        (B+dx,L+dy),
        (dx,L+dy)
    ]

    for (x1,y1),(x2,y2) in zip(
        front_pts,
        back_pts
    ):

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=1
        )

    # =====================================================
    # CENTER
    # =====================================================

    cx = B / 2
    cy = L / 2

    ax.plot(
        cx,
        cy,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        cx + 0.08*B,
        cy - 0.06*L,

        'C',

        34
    )

    # =====================================================
    # AXIS
    # =====================================================

    ax.plot(
        [cx,cx],
        [-0.12*L,1.18*L],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    ax.plot(
        [-0.65*B,1.40*B],
        [cy,cy],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    x = 0
    y = 0.82 * L

    ax.plot(
        x,
        y,

        'ko',

        markersize=11,

        zorder=30
    )

    engineering_text(
        ax,

        x - 0.16*B,
        y + 0.05*L,

        r'$A_i$',

        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [cx,x],
        [cy,y],

        '--',

        color='black',

        linewidth=2.2,

        zorder=25
    )

    engineering_text(
        ax,

        0.28*B,
        0.72*L,

        'r',

        30
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (cx,cy),

        0.42*B,
        0.42*B,

        theta1=125,
        theta2=180,

        linewidth=2.8,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        0.33*B,
        0.57*L,

        r'$\theta$',

        24
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        -1.25*B,
        y + 0.20*L,

        x,
        y,

        coils=8,

        width=0.08*B
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            -0.35*B,
            y + 0.05*L
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        -0.70*B,
        y + 0.13*L,

        r'$\Delta S$',

        32
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    length_txt = f"Length = {L:.2f} mm"

    breadth_txt = f"Breadth = {B:.2f} mm"

    # LENGTH
    dimension_arrow(
        ax,

        -0.18*B,
        0,

        -0.18*B,
        L,

        length_txt,

        -1.0*B,
        0.50*L
    )

    # BREADTH
    dimension_arrow(
        ax,

        0,
        -0.10*L,

        B,
        -0.10*L,

        breadth_txt,

        0.18*B,
        -0.22*L
    )

    # =====================================================
    # FOOTER
    # =====================================================

    engineering_text(
        ax,

        -1.20*B,
        -0.32*L,

        "Fig. 2: Typical Grasp Postures for Objects of 3D Shapes: RECTANGULAR",

        14
    )

    # =====================================================
    # LIMITS
    # =====================================================

    ax.set_xlim(
        -1.5*B,
        1.7*B
    )

    ax.set_ylim(
        -0.25*L,
        1.25*L
    )

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "rectangle_vertical_3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path


# =========================================================
# FIXED 3D VERTICAL ELLIPSOID (SOLIDWORKS STYLE)
# 1536 x 1024 OUTPUT
# HORIZONTAL CENTERED
# =========================================================

def generate_ellipsoid_vertical_3d(a, b):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # VERTICAL ELLIPSOID
    # =====================================================

    major_y = a
    minor_x = b

    # =====================================================
    # SMALLER DEPTH
    # =====================================================

    dx = 0.10 * minor_x
    dy = 0.08 * major_y

    # =====================================================
    # BACK ELLIPSOID
    # =====================================================

    back = Ellipse(
        (dx,dy),

        width=2*minor_x,
        height=2*major_y,

        facecolor='#f0f0f0',

        edgecolor='black',

        linewidth=2.2,

        zorder=0
    )

    ax.add_patch(back)

    # =====================================================
    # FRONT ELLIPSOID
    # =====================================================

    front = Ellipse(
        (0,0),

        width=2*minor_x,
        height=2*major_y,

        facecolor='#d9d9d9',

        edgecolor='black',

        linewidth=3,

        zorder=2
    )

    ax.add_patch(front)

    # =====================================================
    # SOFT SHADOW
    # =====================================================

    shadow = Ellipse(
        (0.05*minor_x,-0.05*major_y),

        width=1.85*minor_x,
        height=1.85*major_y,

        facecolor='black',

        edgecolor='none',

        alpha=0.06,

        zorder=3
    )

    ax.add_patch(shadow)

    # =====================================================
    # HIGHLIGHT
    # =====================================================

    highlight = Ellipse(
        (-0.18*minor_x,0.35*major_y),

        width=0.35*minor_x,
        height=0.45*major_y,

        facecolor='white',

        edgecolor='none',

        alpha=0.28,

        zorder=4
    )

    ax.add_patch(highlight)

    # =====================================================
    # CONNECT EDGES
    # =====================================================

    angles = [45,135,225,315]

    for ang in angles:

        t = np.radians(ang)

        x1 = minor_x*np.cos(t)
        y1 = major_y*np.sin(t)

        x2 = x1 + dx
        y2 = y1 + dy

        ax.plot(
            [x1,x2],
            [y1,y2],

            color='black',

            linewidth=2,

            zorder=1
        )

    # =====================================================
    # HORIZONTAL WIREFRAME
    # =====================================================

    theta = np.linspace(0,2*np.pi,400)

    wx = minor_x*np.cos(theta)
    wy = 0.28*major_y*np.sin(theta)

    ax.plot(
        wx,
        wy,

        '--',

        color='black',

        linewidth=1.2,

        alpha=0.35,

        zorder=5
    )

    # =====================================================
    # AXIS
    # =====================================================

    ax.plot(
        [0,0],
        [-1.15*major_y,1.18*major_y],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    ax.plot(
        [-1.45*minor_x,1.45*minor_x],
        [0,0],

        '--',

        color='black',

        linewidth=2,

        zorder=20
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        0,
        0,

        'ko',

        markersize=10,

        zorder=30
    )

    engineering_text(
        ax,

        0.08*minor_x,
        -0.06*major_y,

        'C',

        30
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    th = np.radians(145)

    x = minor_x*np.cos(th)
    y = major_y*np.sin(th)

    ax.plot(
        x,
        y,

        'ko',

        markersize=10,

        zorder=30
    )

    engineering_text(
        ax,

        x - 0.22*minor_x,
        y + 0.11*major_y,

        r'$A_i$',

        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [0,x],
        [0,y],

        '--',

        color='black',

        linewidth=2,

        zorder=25
    )

    engineering_text(
        ax,

        x*0.42,
        y*0.42,

        'r',

        28
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (0,0),

        0.50*minor_x,
        0.50*minor_x,

        theta1=145,
        theta2=180,

        linewidth=2.5,

        zorder=25
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        -0.12*minor_x,
        0.10*major_y,

        r'$\theta$',

        20
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        x - 0.95*minor_x,
        y + 0.35*major_y,

        x,
        y,

        coils=7,

        width=0.05*minor_x
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            x - 0.28*minor_x,
            y + 0.08*major_y
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        x - 0.72*minor_x,
        y + 0.28*major_y,

        r'$\Delta S$',

        24
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    major_txt = f"Rmajor = {major_y:.2f} mm"

    minor_txt = f"Rminor = {minor_x:.2f} mm"

    # VERTICAL
    dimension_arrow(
        ax,

        -1.05*minor_x,
        -major_y,

        -1.05*minor_x,
        major_y,

        major_txt,

        -2.45*minor_x,
        0
    )

    # HORIZONTAL
    dimension_arrow(
        ax,

        -minor_x,
        -1.08*major_y,

        minor_x,
        -1.08*major_y,

        minor_txt,

        -0.30*minor_x,
        -1.22*major_y
    )

    # =====================================================
    # FOOTER
    # =====================================================

    engineering_text(
        ax,

        -2.90*minor_x,
        -1.52*major_y,

        "Fig. 2: Typical Grasp Postures for Objects of 3D Shapes: ELLIPSOIDAL",

        14
    )

    # =====================================================
    # PERFECT CENTERING
    # =====================================================

    x_margin = 2.8 * minor_x

    ax.set_xlim(
        -x_margin,
        x_margin
    )

    ax.set_ylim(
        -1.5*major_y,
        1.55*major_y
    )

    ax.set_anchor('C')

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "ellipsoid_vertical_3d.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path


# =========================================================
# 2D VERTICAL ELLIPSOID (ENGINEERING STYLE)
# 1536 x 1024 OUTPUT
# HORIZONTAL CENTERED
# =========================================================

def generate_ellipsoid_vertical(a, b):

    fig, ax = plt.subplots(figsize=(12,8))

    ax.set_aspect('equal')
    ax.axis('off')

    # =====================================================
    # ELLIPSOID PARAMETERS
    # =====================================================

    major_y = a
    minor_x = b

    # =====================================================
    # MAIN ELLIPSOID
    # =====================================================

    ellipsoid = Ellipse(
        (0,0),

        width=2*minor_x,
        height=2*major_y,

        facecolor='#dddddd',

        edgecolor='black',

        linewidth=3,

        zorder=2
    )

    ax.add_patch(ellipsoid)

    # =====================================================
    # CENTER WIREFRAME
    # =====================================================

    # theta = np.linspace(0,2*np.pi,400)

    # wx = minor_x*np.cos(theta)
    # wy = 0.28*major_y*np.sin(theta)

    # ax.plot(
    #     wx,
    #     wy,

    #     '--',

    #     color='black',

    #     linewidth=1.2,

    #     alpha=0.45,

    #     zorder=5
    # )

    # =====================================================
    # AXIS LINES
    # =====================================================

    ax.plot(
        [0,0],
        [-1.15*major_y,1.15*major_y],

        '--',

        color='black',

        linewidth=2
    )

    ax.plot(
        [-1.4*minor_x,1.4*minor_x],
        [0,0],

        '--',

        color='black',

        linewidth=2
    )

    # =====================================================
    # CENTER POINT
    # =====================================================

    ax.plot(
        0,
        0,

        'ko',

        markersize=10
    )

    engineering_text(
        ax,

        0.08*minor_x,
        -0.06*major_y,

        'C',

        30
    )

    # =====================================================
    # CONTACT POINT
    # =====================================================

    th = np.radians(145)

    x = minor_x*np.cos(th)
    y = major_y*np.sin(th)

    ax.plot(
        x,
        y,

        'ko',

        markersize=10
    )

    engineering_text(
        ax,

        x - 0.20*minor_x,
        y + 0.11*major_y,

        r'$A_i$',

        24
    )

    # =====================================================
    # RADIUS LINE
    # =====================================================

    ax.plot(
        [0,x],
        [0,y],

        '--',

        color='black',

        linewidth=2
    )

    engineering_text(
        ax,

        x*0.45,
        y*0.45,

        'r',

        28
    )

    # =====================================================
    # THETA ARC
    # =====================================================

    arc = Arc(
        (0,0),

        0.48*minor_x,
        0.48*minor_x,

        theta1=145,
        theta2=180,

        linewidth=2.5
    )

    ax.add_patch(arc)

    engineering_text(
        ax,

        -0.12*minor_x,
        0.10*major_y,

        r'$\theta$',

        20
    )

    # =====================================================
    # SPRING
    # =====================================================

    draw_spring(
        ax,

        x - 0.95*minor_x,
        y + 0.35*major_y,

        x,
        y,

        coils=7,

        width=0.05*minor_x
    )

    # =====================================================
    # FORCE ARROW
    # =====================================================

    ax.annotate(
        '',

        xy=(x,y),

        xytext=(
            x - 0.28*minor_x,
            y + 0.08*major_y
        ),

        arrowprops=dict(
            arrowstyle='simple',

            color='black'
        )
    )

    engineering_text(
        ax,

        x - 0.72*minor_x,
        y + 0.30*major_y,

        r'$\Delta S$',

        22
    )

    # =====================================================
    # DIMENSIONS
    # =====================================================

    major_txt = f"Rmajor = {major_y:.2f} mm"

    minor_txt = f"Rminor = {minor_x:.2f} mm"

    # VERTICAL
    dimension_arrow(
        ax,

        -1.05*minor_x,
        -major_y,

        -1.05*minor_x,
        major_y,

        major_txt,

        -2.45*minor_x,
        0
    )

    # HORIZONTAL
    dimension_arrow(
        ax,

        -minor_x,
        -1.08*major_y,

        minor_x,
        -1.08*major_y,

        minor_txt,

        -0.30*minor_x,
        -1.22*major_y
    )

    # =====================================================
    # FOOTER
    # =====================================================

    engineering_text(
        ax,

        -2.95*minor_x,
        -1.52*major_y,

        "Fig. 2: Typical Grasp Postures for Objects of Shapes: ELLIPSOIDAL",

        14
    )

    # =====================================================
    # CENTERING
    # =====================================================

    x_margin = 2.8 * minor_x

    ax.set_xlim(
        -x_margin,
        x_margin
    )

    ax.set_ylim(
        -1.5*major_y,
        1.55*major_y
    )

    ax.set_anchor('C')

    # =====================================================
    # SAVE
    # =====================================================

    os.makedirs(
        "static/generated",
        exist_ok=True
    )

    fname = "ellipsoid_vertical.png"

    path = os.path.join(
        "static/generated",
        fname
    )

    plt.savefig(
        path,

        dpi=128,

        bbox_inches=None
    )

    plt.close()

    return path

# ===================================================

# generate_rectangle(100,60)

# generate_rectangle_vertical(100, 60)
# generate_rectangle_vertical_3d(100, 60)

# generate_ellipsoid_vertical_3d(50, 30)
# generate_ellipsoid_vertical(50, 30)

# generate_rectangle_3d(100, 60)

# generate_ellipsoid(80, 50)
# generate_ellipsoid_3d_2(80, 50)

# generate_sphere(50)
# generate_sphere_3d_2(50)

# generate_rectangle_3d_2(100, 60, 40)
# print("Generated rectangle.png")
# print("Generated rectangle3d.png")
# generate_sphere(50)