# 🤖 Robotic Gripper Simulation (Spring Structural Model)

An **interactive web application** to simulate and visualize a **robotic gripper** using a spring-based mathematical model.

---

## 📌 Overview

This project models different configurations of a robotic gripper using **spring mechanics and differential equations**.

It supports:

- 🖐️ **3-Finger + 1 Thumb Gripper**
- ✋ **4-Finger Gripper**

The system also considers different **object shapes** and **material properties** to simulate realistic gripping behavior.

---

## 🧮 Mathematical Model

The system is governed by the following equation:

```
(mg)_i - r_i sin(θ_i) (dθ_i/dt)
+ r cos(θ_i) (d²θ_i/dt²)
+ K_i [ r_i ( θ_i - (θ_i³/3!) + (θ_i⁵/5!) ) ]
= F_i(t)
```

### 📘 Where:
- \( m \) = Mass  
- \( g \) = Gravity  
- \( r_i \) = Radius of finger  
- \( \theta_i \) = Angular displacement  
- \( K_i \) = Spring constant  
- \( F_i(t) \) = Applied force  
---

## 🚀 Live Demo

Your application is live here:

👉 https://robotic-gripper.onrender.com

---

## ⚙️ Features

### 🖐️ Gripper Configurations
- 3 Fingers + 1 Thumb  
- 4 Fingers  

### 📦 Object Shapes
- Rectangular  
- Spherical  
- Ellipsoidal  

### 🧱 Material Types
- Rubber  
- ABS (Acrylonitrile Butadiene Styrene)  
- Teflon  

### 🔧 Functional Features
- Multiple modes (Spring Constant Mode, Gripper Mode)  
- Real-time calculations (Force, Volume, etc.)  
- Dynamic parameter input  
- Interactive web interface  

---

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask / FastAPI)  
- **Deployment:** Render  

---

## 📂 Project Structure

```
robotic-gripper/
│── app.py
│── static/
│   └── js/
│       └── function.js
│── templates/
│── README.md
```

---

## ▶️ Run Locally

```bash
git clone https://github.com/your-username/robotic-gripper.git
cd robotic-gripper

pip install -r requirements.txt
python app.py
```

Then open:

👉 http://127.0.0.1:5000

---

## 📈 Future Improvements

- 3D visualization of gripper  
- Real-time graph plotting (θ vs time)  
- AI-based grip optimization  
- Mobile app integration  

---

## 👨‍💻 Author

Developed by **Niyaz Pathan**