# from turtle import mode
import math
import os
from flask import Flask, render_template, request, jsonify
from waitress import serve as waitress_serve
import datetime
import time

app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello World'

@app.route('/')
def index():
    return render_template('index.html')

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

# θ(t)
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
# Force
# def calculate_force(M, K, c, t):
#     return M * d2theta(c, t) + K * theta(c, t)
# def calculate_force(M, K, c, t):
#     return (M * d2theta(c, t)) + (K * theta(c, t))

# F = A + K * B
def cal_force_eq14(M, K, func, t):
    th = theta(func, t)
    dth = dtheta(func, t)
    d2th = d2theta(func, t)    
    # print("th:", th)
    # print("dth:", dth)
    # print("d2th:", d2th)
    # print("M:", M)
    # print("mgr:", M * g * r)
    A = compute_A(M, th, dth, d2th)    
    B = compute_B(th)    
    # print("A:", A)
    # print("B:", B)
    # print("K:", K)
    # return A + K * B
    return A, B, K   # ✅ RETURN SEPARATE VALUES

@app.route("/calculate", methods=["POST"])
def calculate():    
    start_time = time.time()  # ⏱ start
    data = request.json
    # shape = int(data["shape"])
    shape = int(data.get("shape", 0))
    event = data["event"]  # 🔥 GET EVENT TYPE string value

    # length = float(data.get("length", 0))
    # breadth = float(data.get("breadth", 0))
    # width = float(data.get("width", 0))
    # radius = float(data.get("radius", 0))
    # Rmajor = float(data.get("Rmajor", 0))
    # Rminor = float(data.get("Rminor", 0))
    length = float(data.get("length", 0)) * 0.001
    breadth = float(data.get("breadth", 0)) * 0.001
    width = float(data.get("width", 0)) * 0.001

    radius = float(data.get("radius", 0)) * 0.001

    Rmajor = float(data.get("Rmajor", 0)) * 0.001
    Rminor = float(data.get("Rminor", 0)) * 0.001

    material = data["material"]
    t = float(data["time"])
    func = int(data["func"])
    gripper = int(data["gripper"])

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
    mode = data["mode"]

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
            F = A + K * B
            forcesA.append(round(A, 4))
            forcesB.append(round(B, 4))
            forces.append(round(F, 4))

        # Thumb (only if exists)
        if gripper == 2:
            # thumb = round(calculate_force(M, k_thumb_total, func, t), 3)            
            ktt = 1/((1/k) + (1/k) + (1/k))  # Parallel spring formula
            A, B, K = cal_force_eq14(M, ktt, func, t)
            F = A + K * B
            tA = round(A, 4)
            tB = round(B, 4)
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
            F = A + K * B
            forcesA.append(round(A, 4))
            forcesB.append(round(B, 4))
            forces.append(round(F, 4))
            
            # forces.append(round(cal_force_eq14(M, kf_total, func, t), 4))
        if gripper == 2:
            # kt = sum(data.get("thumb", []))  # already correct (108+112+100=320)            
            kt = data.get("thumb", [])
            if len(kt) >= 3:
                ktt = 1/((1/kt[0]) + (1/kt[1]) + (1/kt[2]))  # Parallel spring formula
                # print("ktt:", ktt)
            A, B, K = cal_force_eq14(M, ktt, func, t)
            F = A + K * B
            tA = round(A, 4)
            tB = round(B, 4)
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
            F = A + K * B            
            forcesA.append(round(A, 4))
            forcesB.append(round(B, 4))
            forces.append(round(F, 4))

        if gripper == 2:
            # kt = sum(data.get("thumb", [])) 
            kt = data.get("thumb", [])
            if len(kt) >= 3:
                ktt = 1/((1/kt[0]) + (1/kt[1]) + (1/kt[2]))  # Parallel spring formula
            A, B, K = cal_force_eq14(M, ktt, func, t)
            F = A + K * B
            tA = round(A, 4)
            tB = round(B, 4)
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
    if shape == 1:
        shape_name = "Rectangular"
        if event == "length":
            fig2 = "static/img/shape_rectangle.png"
        elif event == "breadth":
            fig2 = "static/img/shape_rectangle_breadth.png"        
    elif shape == 2:
        shape_name = "Spherical"
        fig2 = "static/img/shape_sphere.png"
    elif shape == 3:
        shape_name = "Ellipsoidal"
        if event == "major":
            fig2 = "static/img/shape_ellipsoid.png"
        elif event == "minor":
            fig2 = "static/img/shape_ellips_minor.png"
    

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

if __name__ == '__main__':
    # app.run()
    # print("# Start App on", "http://localhost:8000")
    # app.run(host="0.0.0.0", port=8000, debug=True) 
    waitress_serve(app, host="0.0.0.0", port=8000)

# Version Control Commands (Git)
# git status
# git add .
# git commit -m "describe your changes"
# git commit -m "Updated index and app"
# # Pull latest (SAFE PRACTICE)
# git pull origin main --rebase
# git push
# Faster Version (Important) Start Command::
# gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 8