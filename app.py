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
def calculate_force(M, K, c, t):
    return M * d2theta(c, t) + K * theta(c, t)

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

    volume = calculate_volume(shape)
    density = materials.get(material, 0)
    M = density * volume
    # M = materials[material] * volume
    
    # print("\n===== INPUT DATA =====")
    # print("current date and time:", datetime.datetime.now())
    # print("shape:", shape)
    # if shape == 1:
    #     print("shape type: Rectangular Prism")
    # elif shape == 2:
    #     print("shape type: Sphere")
    # elif shape == 3:        
    #     print("shape type: Ellipsoid")
    # print("material:", material)
    # print("volume:", volume)
    # print("density:", density)
    # print("mass:", M)
    # print("time:", t)
    # print("event type:", event)  # 🔥 PRINT EVENT TYPE

    forces = []
    thumb = 0

    if data["mode"] == "unequal":
        finger_count = 4 if gripper == 1 else 3

        for i in range(finger_count):
            k = data["fingers"][i]["k1"] + data["fingers"][i]["k2"]
            f = calculate_force(M, k, func, t)
            forces.append(round(f, 2))

        if gripper == 2:
            kt = sum(data["thumb"])
            thumb = round(calculate_force(M, kt, func, t), 2)

    total = round(sum(forces) + thumb, 2)
    fig1, fig2 = "", ""    # 🔥 IMPORTANT: Initialize variables to avoid reference errors
    if gripper == 1:
        # print("gripper type: 4-Finger Gripper") 
        fig1= "static/img/model_4Fingers.png"
    elif gripper == 2:
        # print("gripper type: 3-Finger Gripper with Thumb")
        fig1= "static/img/model_3Fingers_Thumb.png"
    if shape == 1:
        if event == "length":
            fig2 = "static/img/shape_rectangle.png"
        elif event == "breadth":
            fig2 = "static/img/shape_rectangle_breadth.png"        
    elif shape == 2:
        fig2 = "static/img/shape_sphere.png"
    elif shape == 3:
        if event == "major":
            fig2 = "static/img/shape_ellipsoid.png"
        elif event == "minor":
            fig2 = "static/img/shape_ellips_minor.png"
    # 🔥 PRINT IN CONSOLE
    # print("\n===== FORCE OUTPUT =====")
    # for i, f in enumerate(forces):
    #     print(f"Finger {i+1}: {f} N")

    # if gripper == 2:
    #     print(f"Thumb: {thumb} N")

    # print(f"Total Force: {total} N")
    # print("========================\n")

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
        "fig2": fig2
    })

if __name__ == '__main__':
    # app.run()
    # app.run(host="0.0.0.0", port=8000, debug=True)  
    serve(app, host="0.0.0.0", port=8000, threads=8)