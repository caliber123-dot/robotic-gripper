# 🤖 Robotic Gripper Simulation (Spring Structural Model)

An **interactive web application** to simulate and visualize a **robotic gripper** using a spring-based mathematical model.

---

## 📌 Overview

This project models a **3-finger + 1 thumb robotic gripper** using spring mechanics and differential equations.

It allows users to:

- Input physical parameters (spring constant, mode, geometry, etc.)
- Compute grip force, displacement, and volume
- Visualize system behavior dynamically

---

## 🧮 Mathematical Model

The system is governed by the following equation:

\[
(mg)_i - r_i \sin\theta_i \frac{d\theta_i}{dt}
+ r \cos\theta_i \frac{d^2\theta_i}{dt^2}
+ K_i \left[r_i \left(\theta_i - \frac{\theta_i^3}{3!} + \frac{\theta_i^5}{5!} \right)\right]
= F_i(t)
\]

---

## 🚀 Live Demo

Your application is live here:

👉 https://robotic-gripper.onrender.com

---

## ⚙️ Features

- 🖐️ 3 Fingers + 1 Thumb spring model  
- 🔧 Multiple modes (Spring Constant Mode, Gripper Mode)  
- 📊 Real-time calculations (Force, Volume, etc.)  
- 🌐 Web-based interactive UI  
- 🧠 Based on physics + mathematical modeling  

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