# from turtle import mode

from flask import Flask, render_template, request, jsonify
from waitress import serve
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

# θ''(t)
def d2theta(c, t):
    if c == 1:
        return 2/3
    elif c == 2:
        return 2/3 + (3*t)/2
    elif c == 3:
        return 1/2 + (6*t)/5

# Force
# def calculate_force(M, K, c, t):
#     return M * d2theta(c, t) + K * theta(c, t)
def calculate_force(M, K, c, t):
    return (M * d2theta(c, t)) + (K * theta(c, t))

@app.route("/calculate", methods=["POST"])
def calculate():    
    start_time = time.time()  # ⏱ start
    data = request.json
    # shape = int(data["shape"])
    shape = int(data.get("shape", 0))
    event = data["event"]  # 🔥 GET EVENT TYPE string value
    material = data["material"]
    t = float(data["time"])
    func = int(data["func"])
    gripper = int(data["gripper"])

   
    if shape == 1:  # Rectangular
        if event == "length":
            L, B, H = 0.1, 0.04, 0.02
        elif event == "breadth":
            L, B, H = 0.04, 0.1, 0.02
        else:
            L, B, H = 0.1, 0.04, 0.02  # default ✅
        volume = L * B * H

    elif shape == 2:  # Sphere
        r = 0.05
        volume = (4/3) * 3.14 * (r ** 3)

    elif shape == 3:  # Ellipsoid
        if event == "major":
            a, b, c = 0.05, 0.03, 0.03
        elif event == "minor":
            a, b, c = 0.03, 0.03, 0.05
        else:
            a, b, c = 0.05, 0.03, 0.03  # default ✅
        volume = (4/3) * 3.14 * a * b * c

    else:
        volume = 0
    density = materials.get(material, 0)
    M = density * volume
    # M = materials[material] * volume
    
    forces = []
    thumb = 0
    finger_count = 4 if gripper == 1 else 3
    mode = data["mode"]

    # print("\n===== CALCULATION MODE =====")
    # print("mode:", mode)  # 🔥 PRINT MODE
    # print("func:", func)  # 🔥 PRINT FUNCTION 
    
    # ================= MODE 1 All equal =================
    if mode == "1":  # All equal
        k = float(data.get("k_common", 0))
         # 🔥 Finger has 2 springs
        k_finger_total = k * 2

        # 🔥 Thumb has 3 springs
        k_thumb_total = k * 3
        # Fingers
        for i in range(finger_count):
            forces.append(round(calculate_force(M, k_finger_total, func, t), 3))

        # Thumb (only if exists)
        if gripper == 2:
            thumb = round(calculate_force(M, k_thumb_total, func, t), 3)

    # ================= MODE 2 Fingers same, Thumb different=================
    elif mode == "2":
        kf = float(data.get("k_finger", 0))
        # 🔥 FIX: Finger has 2 springs → multiply by 2
        kf_total = kf * 2
        for i in range(finger_count):
            forces.append(round(calculate_force(M, kf_total, func, t), 2))
        if gripper == 2:
            kt = sum(data.get("thumb", []))  # already correct (108+112+100=320)
            thumb = round(calculate_force(M, kt, func, t), 2)

    # ================= MODE 3 All unequal=================
    elif mode == "3":
        for i in range(finger_count):
            k = data["fingers"][i]["k1"] + data["fingers"][i]["k2"]
            forces.append(round(calculate_force(M, k, func, t), 2))

        if gripper == 2:
            kt = sum(data.get("thumb", []))
            thumb = round(calculate_force(M, kt, func, t), 2)

    # TOTAL
    total = round(sum(forces) + thumb, 2)    
   
    # total = round(sum(forces) + thumb, 2)
    fig1, fig2 = "", ""    # 🔥 IMPORTANT: Initialize variables to avoid reference errors
    gripper_name = ""
    shape_name = ""
    if gripper == 1:
        # print("gripper type: 4-Finger Gripper") 
        fig1= "static/img/model_4Fingers.png"
        gripper_name = "4-Finger Gripper"
    elif gripper == 2:
        # print("gripper type: 3-Finger Gripper with Thumb")
        fig1= "static/img/model_3Fingers_Thumb.png"
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
    execution_time = (end_time - start_time) * 1000  # convert to ms
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
        "shape_name": shape_name
    })

if __name__ == '__main__':
    # app.run()
    # app.run(host="0.0.0.0", port=8000, debug=True)  
    serve(app, host="0.0.0.0", port=8000, threads=8)

# Version Control Commands (Git)
# git status
# git add .
# git commit -m "describe your changes"
# git commit -m "Updated index and app"
# # Pull latest (SAFE PRACTICE)
# git pull origin main --rebase
# git push