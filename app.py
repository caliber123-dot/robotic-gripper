# from turtle import mode
import math
# import os
from flask import Flask, render_template, request, jsonify, send_file
from waitress import serve as waitress_serve
import datetime
import time
# from openpyxl import Workbook
# from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
from sympy import symbols, diff, sympify, N
from sympy.core.expr import Expr
from shape_drawer import (
    generate_sphere,
    generate_rectangle,
    generate_ellipsoid
)

import base64
from io import BytesIO
from openpyxl.drawing.image import Image

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World'

@app.route('/')
def index():
    # print("############# Rendering index.html")
    return render_template('index.html')

@app.route('/graph')
def graph():
    # print("############# Rendering Bar Chart graph.html")
    return render_template('graph.html')

# Material density
materials = {
    "rubber": 1100,
    "abs": 1040,
    "teflon": 2200
}

# Volume calculation
def calculate_volume(shape):
    if shape == 1:  # Rectangular
        return 0.1 * 0.04 * 0.02
    elif shape == 2:  # Sphere
        return (4/3) * 3.14 * (0.05 ** 3)
    elif shape == 3:  # Ellipsoid
        return (4/3) * 3.14 * 0.05 * 0.03 * 0.03
    else:
        return 0   # 🔥 VERY IMPORTANT

def parse_theta_function(func_str, t_value):

    # normalize input
    func_str = (
        func_str
        .replace("^", "**")
        .replace(" ", "")
    )

    t = symbols('t')

    # symbolic expression
    expr: Expr = sympify(func_str)

    # derivatives
    d1: Expr = diff(expr, t)
    d2: Expr = diff(d1, t)

    # numerical evaluation
    th = float(N(expr.subs(t, t_value)))
    dth = float(N(d1.subs(t, t_value)))
    d2th = float(N(d2.subs(t, t_value)))

    return th, dth, d2th


# θ(t) and c = func
def theta(c, t):
    if c == 1:
        return t/2 + (t*t)/3
    elif c == 2:
        return t/2 + (t*t)/3 + (t*t*t)/4
    elif c == 3:
        return t/3 + (t*t)/4 + (t*t*t)/5

# θ'(t)
def dtheta(c, t):
    if c == 1:
        return 1/2 + (2*t)/3
    elif c == 2:
        return 1/2 + (2*t)/3 + (3*t*t)/4
    elif c == 3:
        return 1/3 + (2*t)/4 + (3*t*t)/5

# θ''(t)
def d2theta(c, t):
    if c == 1:
        return 2/3
    elif c == 2:
        return 2/3 + (3*t)/2
    elif c == 3:
        return 1/2 + (6*t)/5

# ===================== EQ 14 =====================
g = 9.8    # constant from your notes in Part A
r = 0.05   # constant from your notes in Part A and B
def compute_A(M, th, dth, d2th):  
    # mgr2 = d2th  - th * d2th- (th**2 / 2) * dth + (th**3 / 6) * dth + (th**4 / 24) * d2th - (th**5 / 120) * dth
    # print("mgr2:", mgr2)
    return (M * g * r) * (
        d2th
        - th * dth
        - (th**2 / 2) * d2th
        + (th**3 / 6) * dth
        + (th**4 / 24) * d2th
        - (th**5 / 120) * dth
    )

def compute_B(th):
    return r * (th - (th**3)/6 + (th**5)/120)

# F = A + K * B
def cal_force_eq14(M, K, func, t):  
    # CALL DYNAMIC FUNCTION PARSER
    # θ(t), θ′(t), θ″(t)
    th, dth, d2th = parse_theta_function(func, t)
    
    A = compute_A(M, th, dth, d2th)    
    B = compute_B(th)    
    
    return A, B, K   # ✅ RETURN SEPARATE VALUES


@app.route("/calculate", methods=["POST"])
def calculate():    
    start_time = time.time()  # ⏱ start
    # print(request.json)
    data = request.json
    # shape = int(data["shape"])
    shape = int(data.get("shape", 0))
    event = data["event"]  # 🔥 GET EVENT TYPE string value

    length = float(data.get("length", 0)) * 0.001
    breadth = float(data.get("breadth", 0)) * 0.001
    width = float(data.get("width", 0)) * 0.001

    radius = float(data.get("radius", 0)) * 0.001

    Rmajor = float(data.get("Rmajor", 0)) * 0.001
    Rminor = float(data.get("Rminor", 0)) * 0.001

    material = data["material"]
    t = float(data["time"])
    func = data["func"]
    print("Function:", func)  
    
    # print("Selected Function ID:", func)
    
    gripper = int(data["gripper"]) # 1 or 2

    if shape == 1:  # Rectangular
        if event == "length":
            # L, B, H = 0.1, 0.04, 0.02
            L, B, H = length, breadth, width
        elif event == "breadth":
            # L, B, H = 0.04, 0.1, 0.02
            L, B, H = breadth, length, width
        else:
            L, B, H = 0.1, 0.04, 0.02  # default ✅
        volume = L * B * H
        print("Volume:", volume)

    elif shape == 2:  # Spherical
        # r = 0.05
        r = radius
        volume = (4/3) * math.pi * (r ** 3)

    elif shape == 3:  # Ellipsoid
        if event == "major":
            # a, b, c = 0.05, 0.03, 0.03
            a, b, c = Rmajor, Rminor, Rminor
        elif event == "minor":
            # a, b, c = 0.03, 0.03, 0.05
            a, b, c = Rminor, Rminor, Rmajor
        else:
            a, b, c = 0.05, 0.03, 0.03  # default ✅
        volume = (4/3) * math.pi * a * b * c

    else:
        volume = 0
    density = materials.get(material, 0)
    M = density * volume
    # print("Density:", density)
    # print("Volume:", volume)
    # print("Mass:", M)
        
    forces = []
    forcesA = []
    forcesB = []
    kf_total = []    
    thumb = 0
    ktt = 0
    tA = 0
    tB = 0
    finger_count = 4 if gripper == 1 else 3
    mode = data["mode"] # get string constant values eg 1, 2, 3

    # print("\n===== CALCULATION MODE =====")    
    # ================= MODE 1 All equal =================
    if mode == "1":  # All equal
        k = float(data.get("k_common", 0))
        kf = (k * k)/(k + k)
         
        # Fingers
        for i in range(finger_count):
            #🔥 forces.append(round(calculate_force(M, k_finger_total, func, t), 3))
            kf_total.append(kf)
            A, B, K = cal_force_eq14(M, kf, func, t)
            # F = A + K * B
            F = abs(A) + K * abs(B)  # ✅ Use absolute values to avoid negative forces
            forcesA.append(round(abs(A), 4))
            forcesB.append(round(abs(B), 4))
            forces.append(round(F, 4))

        # Thumb (only if exists)
        if gripper == 2:
            # thumb = round(calculate_force(M, k_thumb_total, func, t), 3)            
            ktt = 1/((1/k) + (1/k) + (1/k))  # Parallel spring formula
            A, B, K = cal_force_eq14(M, ktt, func, t)
            F = abs(A) + K * abs(B)
            tA = round(abs(A), 4)
            tB = round(abs(B), 4)
            # print("Thumb A:", tA)
            # print("Thumb B:", tB)
            # print("Thumb K:", ktt)
            thumb = round(F, 4)

    # ================= MODE 2 Fingers same, Thumb different=================
    elif mode == "2":
        kf = float(data.get("k_finger", 0))
        # 🔥 FIX: Finger has 2 springs → multiply by 2
        # kf_total = kf * 2
        kf = (kf * kf)/(kf + kf)
          # ✅ Store total finger stiffness for debugging
        # print("kf_total:", kf_total)
        for i in range(finger_count):
            # forces.append(round(calculate_force(M, kf_total, func, t), 2))
            # cal_force_eq14(M, K, func, t)
            kf_total.append(kf)
            A, B, K = cal_force_eq14(M, kf, func, t)
            F = abs(A) + K * abs(B)
            forcesA.append(round(abs(A), 4))
            forcesB.append(round(abs(B), 4))
            forces.append(round(F, 4))
            
            # forces.append(round(cal_force_eq14(M, kf_total, func, t), 4))
        if gripper == 2:
            # kt = sum(data.get("thumb", []))  # already correct (108+112+100=320)            
            kt = data.get("thumb", [])
            if len(kt) >= 3:
                ktt = 1/((1/kt[0]) + (1/kt[1]) + (1/kt[2]))  # Parallel spring formula
                # print("ktt:", ktt)
            A, B, K = cal_force_eq14(M, ktt, func, t)
            F = abs(A) + K * abs(B)
            tA = round(abs(A), 4)
            tB = round(abs(B), 4)
            # print("Thumb A:", tA)
            # print("Thumb B:", tB)
            # print("Thumb K:", ktt)
            thumb = round(F, 4)
            # thumb = round(cal_force_eq14(M, ktt, func, t), 4)
            
    # ================= MODE 3 All unequal=================
    elif mode == "3":
        # kfinger = []
        for i in range(finger_count):
            # k = data["fingers"][i]["k1"] + data["fingers"][i]["k2"]
            k1 = data["fingers"][i]["k1"]
            k2 = data["fingers"][i]["k2"]        
            kf = (k1 * k2)/(k1 + k2)    
            kf_total.append(kf)
            # forces.append(round(calculate_force(M, k, func, t), 2))
            A, B, K = cal_force_eq14(M, kf, func, t)
            F = abs(A) + K * abs(B)
            forcesA.append(round(abs(A), 4))
            forcesB.append(round(abs(B), 4))
            forces.append(round(F, 4))

        if gripper == 2:
            # kt = sum(data.get("thumb", [])) 
            kt = data.get("thumb", [])
            if len(kt) >= 3:
                ktt = 1/((1/kt[0]) + (1/kt[1]) + (1/kt[2]))  # Parallel spring formula
            A, B, K = cal_force_eq14(M, ktt, func, t)
            F = abs(A) + K * abs(B)
            tA = round(abs(A), 4)
            tB = round(abs(B), 4)
            # print("Thumb A:", tA)
            # print("Thumb B:", tB)
            # print("Thumb K:", ktt)
            thumb = round(F, 4)
            # thumb = round(calculate_force(M, kt, func, t), 2)

    # TOTAL
    total = round(sum(forces) + thumb, 4)    
   
    # total = round(sum(forces) + thumb, 2)
    fig1, fig2 = "", ""    # 🔥 IMPORTANT: Initialize variables to avoid reference errors
    fig3 = ""
    gripper_name = ""
    shape_name = ""
    if gripper == 1:
        # print("gripper type: 4-Finger Gripper") 
        fig1= "static/img/model_4Fingers.png"
        fig3 = "static/img/Industrial_For4inger.jpg"
        gripper_name = "4-Finger Gripper"
    elif gripper == 2:
        # print("gripper type: 3-Finger Gripper with Thumb")
        fig1= "static/img/model_3Fingers_Thumb.png"
        fig3 = "static/img/basic.avif"
        gripper_name = "3-Finger Gripper with Thumb"
    
    # =====================================
    # DYNAMIC ENGINEERING FIGURES
    # =====================================

    if shape == 1:

        shape_name = "Rectangular"

        fig2 = generate_rectangle(
            length * 1000,
            breadth * 1000
        )

    elif shape == 2:

        shape_name = "Spherical"

        fig2 = generate_sphere(
            radius * 1000
        )

    elif shape == 3:

        shape_name = "Ellipsoidal"

        fig2 = generate_ellipsoid(
            Rmajor * 1000,
            Rminor * 1000
        )
    
    end_time = time.time()  # ⏱ end
    # execution_time = (end_time - start_time) * 1000  # convert to ms
    execution_time = (end_time - start_time) * 1000000  # microseconds (µs)
    return jsonify({
        "volume": volume,
        "mass": M,
        "forces": forces,
        "thumb": thumb,
        "total": total,
        "execution_time": round(execution_time, 2),
        "fig1": fig1,
        "fig2": fig2,
        "gripper_name": gripper_name,
        "shape_name": shape_name,
        "forcesA": forcesA,
        "forcesB": forcesB,
        "thumbA": tA,
        "thumbB": tB,
        "kf_total": kf_total,
        "ktt": ktt,
        "fig3": fig3
    })

@app.route("/download_excel", methods=["POST"])
def download_excel():

    data = request.json

    wb = Workbook()

    ws = wb.active

    if ws is None:
        raise Exception("Worksheet not created")

    ws.title = "Gripper Results"

    # =========================
    # HEADER DETAILS
    # =========================

    header_font = Font(bold=True)
    Grippertype= data.get("gripper_name", "")

    ws["A1"] = "Gripper type:"
    ws["B1"] = Grippertype

    ws["A2"] = "Object Shape"
    ws["B2"] = data.get("shape_name", "")

    ws["A3"] = "Material"
    ws["B3"] = data.get("material", "")

    ws["A4"] = "Time"
    ws["B4"] = str(data.get("time", "")) + " sec"

    ws["A5"] = "θ(t) Function"
    ws["B5"] = data.get("func", "")

    ws["A6"] = "Spring Constant"
    ws["B6"] = data.get("mode_name", "")

    # Bold left labels
    for row in range(1, 7):

        ws[f"A{row}"].font = header_font

    # =========================
    # TABLE HEADER
    # =========================

    ws["A8"] = "Gripper"
    ws["B8"] = "A"
    ws["C8"] = "K"
    ws["D8"] = "B"
    ws["E8"] = "F(t) (N)"

    for cell in ["A8", "B8", "C8", "D8", "E8"]:

        ws[cell].font = header_font
        ws[cell].alignment = Alignment(horizontal="center")

    # =========================
    # DATA ROWS
    # =========================

    rows = [

        ["Finger 1",
            data.get("a1"),
            data.get("k1"),
            data.get("b1"),
            data.get("f1")],

        ["Finger 2",
            data.get("a2"),
            data.get("k2"),
            data.get("b2"),
            data.get("f2")],

        ["Finger 3",
            data.get("a3"),
            data.get("k3"),
            data.get("b3"),
            data.get("f3")]
    ]

    # =========================
    # 4 Finger Gripper
    # =========================

    if "4" in str(data.get("gripper_name", "")):

        rows.append([
            "Finger 4",
            data.get("a4"),
            data.get("k4"),
            data.get("b4"),
            data.get("f4")
        ])

    # =========================
    # 3 Finger + Thumb
    # =========================

    if "Thumb" in str(data.get("gripper_name", "")):

        rows.append([
            "Thumb",
            data.get("ta"),
            data.get("tk"),
            data.get("tb"),
            data.get("ft")
        ])

    start_row = 9

    for row_data in rows:

        ws.append(row_data)

    # =========================
    # TOTAL
    # =========================

    ws["A15"] = "TOTAL"
    ws["E15"] = data.get("total")

    ws["A15"].font = Font(bold=True)
    ws["E15"].font = Font(bold=True)

    # =========================
    # COLUMN WIDTH
    # =========================

    for col_num, column_cells in enumerate(ws.columns, 1):

        length = max(
            len(str(cell.value or ""))
            for cell in column_cells
        )

        column_letter = get_column_letter(col_num)

        ws.column_dimensions[column_letter].width = length + 5

    # =========================
    # SAVE FILE
    # =========================

    file_name = "gripper_results.xlsx"

    wb.save(file_name)

    return send_file(
        file_name,
        as_attachment=True
    )

# CALL NEW API FROM graph.js
# CREATE COMMON FUNCTION
def perform_calculation(data, t):

    shape = int(data.get("shape", 0))
    event = data["event"]

    length = float(data.get("length", 0)) * 0.001
    breadth = float(data.get("breadth", 0)) * 0.001
    width = float(data.get("width", 0)) * 0.001

    radius = float(data.get("radius", 0)) * 0.001

    Rmajor = float(data.get("Rmajor", 0)) * 0.001
    Rminor = float(data.get("Rminor", 0)) * 0.001

    material = data["material"]

    func = data["func"]

    gripper = int(data["gripper"])

    # =====================================
    # VOLUME
    # =====================================

    if shape == 1:

        if event == "length":
            L, B, H = length, breadth, width

        elif event == "breadth":
            L, B, H = breadth, length, width

        else:
            L, B, H = 0.1, 0.04, 0.02

        volume = L * B * H

    elif shape == 2:

        volume = (4/3) * math.pi * (radius ** 3)

    elif shape == 3:

        if event == "major":
            a, b, c = Rmajor, Rminor, Rminor

        elif event == "minor":
            a, b, c = Rminor, Rminor, Rmajor

        else:
            a, b, c = 0.05, 0.03, 0.03

        volume = (4/3) * math.pi * a * b * c

    else:
        volume = 0

    density = materials.get(material, 0)

    M = density * volume

    forces = []

    thumb = 0

    finger_count = 4 if gripper == 1 else 3

    mode = data["mode"]

    # =====================================
    # MODE 1
    # =====================================

    if mode == "1":

        k = float(data.get("k_common", 0))

        kf = (k * k)/(k + k)

        for i in range(finger_count):

            A, B, K = cal_force_eq14(M, kf, func, t)

            F = abs(A) + K * abs(B)

            forces.append(round(F, 4))

        if gripper == 2:

            ktt = 1/((1/k) + (1/k) + (1/k))

            A, B, K = cal_force_eq14(M, ktt, func, t)

            thumb = round(abs(A) + K * abs(B), 4)

    # =====================================
    # MODE 2
    # =====================================

    elif mode == "2":

        kf = float(data.get("k_finger", 0))

        kf = (kf * kf)/(kf + kf)

        for i in range(finger_count):

            A, B, K = cal_force_eq14(M, kf, func, t)

            F = abs(A) + K * abs(B)

            forces.append(round(F, 4))

        if gripper == 2:

            kt = data.get("thumb", [])

            if len(kt) >= 3:

                ktt = 1/(
                    (1/kt[0]) +
                    (1/kt[1]) +
                    (1/kt[2])
                )

                A, B, K = cal_force_eq14(
                    M,
                    ktt,
                    func,
                    t
                )

                thumb = round(
                    abs(A) + K * abs(B),
                    4
                )

    # =====================================
    # MODE 3
    # =====================================

    elif mode == "3":

        for i in range(finger_count):

            k1 = data["fingers"][i]["k1"]

            k2 = data["fingers"][i]["k2"]

            kf = (k1 * k2)/(k1 + k2)

            A, B, K = cal_force_eq14(M, kf, func, t)

            F = abs(A) + K * abs(B)

            forces.append(round(F, 4))

        if gripper == 2:

            kt = data.get("thumb", [])

            if len(kt) >= 3:

                ktt = 1/(
                    (1/kt[0]) +
                    (1/kt[1]) +
                    (1/kt[2])
                )

                A, B, K = cal_force_eq14(
                    M,
                    ktt,
                    func,
                    t
                )

                thumb = round(
                    abs(A) + K * abs(B),
                    4
                )

    total = round(sum(forces) + thumb, 4)

    return total

@app.route("/calculate_graph", methods=["POST"])
def calculate_graph():
    start_time = time.perf_counter()
    data = request.json
    time_data = []
    force_data = []

    for t in range(1, 6):
        total_force = perform_calculation(data, t)
        time_data.append(f"{t} sec")
        force_data.append(total_force)

    
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1_000_000
    
    return jsonify({

        "time": time_data,
        "force": force_data,
        "execution_time": round(execution_time, 2)

    })

@app.route("/download_graph_excel", methods=["POST"])
def download_graph_excel():

    data = request.json

    wb = Workbook()

    ws = wb.active

    if ws is None:
        raise Exception("Worksheet not created")

    ws.title = "Graph Report"

    # =========================================
    # MAIN HEADING
    # =========================================

    ws.merge_cells("A1:H1")

    shape_name = data.get("shape_name", "")
    ws["A1"] = (
        "Bar Chart Representation of "
        f"Spring Structure Model ({shape_name})"
    )
    ws["A1"].font = Font(
        bold=True,
        size=18
    )

    ws["A1"].alignment = Alignment(
        horizontal="center"
    )

    # =========================================
    # OBJECT DETAILS
    # =========================================

    object_shape = data.get(
        "object_shape",
        "-"
    )

    material = data.get(
        "material",
        "-"
    )

    ws["A2"] = (
        f"Object Shape : {object_shape}"
    )

    ws["A3"] = (
        f"Material : {material}"
    )

    ws["A2"].font = Font(
        bold=True,
        size=12
    )

    ws["A3"].font = Font(
        bold=True,
        size=12
    )
    # =========================================
    # TABLE HEADER
    # =========================================

    ws["A5"] = "Time t (sec)"
    ws["B5"] = "Force (N)"

    # from openpyxl.styles import Alignment
    ws["B5"].alignment = Alignment(
        horizontal="right"
    )

    header_font = Font(bold=True)

    ws["A5"].font = header_font
    ws["B5"].font = header_font

    # =========================================
    # TABLE DATA
    # =========================================

    row = 6
    for item in data["tableData"]:

        ws[f"A{row}"] = item["time"]

        ws[f"B{row}"] = float(item["force"])

        row += 1

    # =========================================
    # COLUMN WIDTH
    # =========================================

    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 20

    # =========================================
    # GRAPH IMAGE
    # =========================================

    graph_data = data["graphImage"]

    graph_data = graph_data.split(",")[1]

    image_data = base64.b64decode(graph_data)

    with open("temp_chart.png", "wb") as f:

        f.write(image_data)

    img = Image("temp_chart.png")

    img.width = 900
    img.height = 450

    # place graph below table
    ws.add_image(img, "A13")

    # =========================================
    # SAVE FILE
    # =========================================
    shape_name = (
        shape_name
        .replace(" ", "")
        .replace("+", "")
    )
    # filename = "Graph_Report_AAAA.xlsx"
    filename = (
        f"Graph_"
        f"{shape_name}_"
        f"{object_shape}_"
        f"{material}.xlsx"
    )
    print("Saving file:", filename)
    wb.save(filename)

    return send_file(
        filename,
        as_attachment=True
    )

if __name__ == '__main__':
    # app.run()
    # print("# Start App on", "http://localhost:8000")
    # app.run(host="0.0.0.0", port=8000, debug=True) 
    waitress_serve(app, host="0.0.0.0", port=8000, threads=8)

# Version Control Commands (Git)
# git status
# git add .
# git commit -m "describe your changes"
# git commit -m "Updated index and app"
# # Pull latest (SAFE PRACTICE)
# git pull origin main --rebase
# git push
# git push -f origin main

# Faster Version (Important) Start Command::
# gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 8

# Add the command in Render Dashboard → Service → Settings → Build Command:

# pip install --prefer-binary -r requirements.txt && python -c "import matplotlib.pyplot as plt"

# And Start Command:

# gunicorn --bind 0.0.0.0:$PORT app:app --workers 1 --threads 8

# This is the correct Render setup.