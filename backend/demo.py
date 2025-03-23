import json
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from djitellopy import Tello

# Initialize drone
drone = Tello()
drone.connect()
drone.streamon()

# Load or create paths file
try:
    with open("paths.json", "r") as f:
        paths = json.load(f)
except FileNotFoundError:
    paths = {}

# GUI Setup
root = tk.Tk()
root.title("Drone Path Recorder")
root.geometry("400x500")
root.configure(bg="#87CEEB")  # Light blue background

commands = []

def start_recording():
    global path_name, commands
    path_name = simpledialog.askstring("Path Name", "Enter a name for this path:")
    
    if not path_name or path_name in paths:
        messagebox.showerror("Error", "Invalid or duplicate path name!")
        return
    
    commands = []
    drone.takeoff()
    messagebox.showinfo("Recording", "Recording Started!")

def record_command(cmd):
    speed = 30  # cm/s
    duration = 1  # Fixed duration per move (can be changed dynamically)
    distance = int(speed * duration)
    commands.append((cmd, distance))
    
    if cmd == "w":
        drone.move_forward(distance)
    elif cmd == "s":
        drone.move_back(distance)
    elif cmd == "a":
        drone.move_left(distance)
    elif cmd == "d":
        drone.move_right(distance)
    elif cmd == "u":
        drone.move_up(distance)
    elif cmd == "j":
        drone.move_down(distance)
    elif cmd == "q":
        drone.rotate_counter_clockwise(30)
    elif cmd == "e":
        drone.rotate_clockwise(30)

def stop_recording():
    global paths
    drone.land()
    paths[path_name] = commands
    with open("paths.json", "w") as f:
        json.dump(paths, f, indent=4)
    messagebox.showinfo("Success", f"Path '{path_name}' saved successfully!")

# UI Elements
tk.Label(root, text="Drone Path Recorder", font=("Arial", 16, "bold"), bg="#87CEEB").pack(pady=10)
tk.Button(root, text="Start Recording", command=start_recording, bg="#FFA500", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=10)

tk.Button(root, text="Forward (W)", command=lambda: record_command("w"), width=15).pack(pady=5)
tk.Button(root, text="Backward (S)", command=lambda: record_command("s"), width=15).pack(pady=5)
tk.Button(root, text="Left (A)", command=lambda: record_command("a"), width=15).pack(pady=5)
tk.Button(root, text="Right (D)", command=lambda: record_command("d"), width=15).pack(pady=5)
tk.Button(root, text="Up (U)", command=lambda: record_command("u"), width=15).pack(pady=5)
tk.Button(root, text="Down (J)", command=lambda: record_command("j"), width=15).pack(pady=5)
tk.Button(root, text="Rotate Left (Q)", command=lambda: record_command("q"), width=15).pack(pady=5)
tk.Button(root, text="Rotate Right (E)", command=lambda: record_command("e"), width=15).pack(pady=5)

tk.Button(root, text="Stop & Save", command=stop_recording, bg="#FF4500", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=20)

root.mainloop()
