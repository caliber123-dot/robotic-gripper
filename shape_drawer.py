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

    ax.set_xlim(-1.7*R,1.7*R)
    ax.set_ylim(-1.5*R,1.5*R)

    os.makedirs("static/generated",exist_ok=True)

    fname = f"sphere_{time.time()}.png"

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

    fname = f"rect_{time.time()}.png"

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

    fname = f"ellipse_{time.time()}.png"

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