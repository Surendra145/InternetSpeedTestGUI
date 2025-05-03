import tkinter as tk
from tkinter import ttk
import speedtest
import threading

def run_speed_test():
    test_button.config(state="disabled")
    label_status.config(text="Testing... Please wait.")
    download_var.set("0 Mbps")
    upload_var.set("0 Mbps")
    ping_var.set("0 ms")
    isp_var.set("...")
    server_var.set("...")

    def test():
        try:
            st = speedtest.Speedtest()
            best_server = st.get_best_server()

            download = st.download()
            upload = st.upload()
            ping = st.results.ping
            isp = st.config['client']['isp']
            server_info = f"{best_server['sponsor']} ({best_server['name']}, {best_server['country']})"

            download_var.set(f"{download / 1_000_000:.2f} Mbps")
            upload_var.set(f"{upload / 1_000_000:.2f} Mbps")
            ping_var.set(f"{ping:.0f} ms")
            isp_var.set(isp)
            server_var.set(server_info)

            label_status.config(text="Test Complete")
        except Exception as e:
            label_status.config(text=f"Error: {e}")
        finally:
            test_button.config(state="normal")

    threading.Thread(target=test).start()

# === GUI Setup ===
app = tk.Tk()
app.title("Internet Speed Test")
app.geometry("500x380")
app.resizable(False, False)
app.configure(bg="#1e1e1e")  # dark background

# Styling
style = ttk.Style(app)
style.theme_use("clam")

# Dark theme for ttk widgets
style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.map("TButton",
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '#444'), ('active', '#333')])

# Variables
download_var = tk.StringVar()
upload_var = tk.StringVar()
ping_var = tk.StringVar()
isp_var = tk.StringVar()
server_var = tk.StringVar()

# Widgets
tk.Label(app, text="Internet Speed Test", font=("Segoe UI", 18, "bold"), bg="#1e1e1e", fg="#ffffff").pack(pady=15)

frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(pady=5)

# Label pairs
labels = [
    ("Download:", download_var),
    ("Upload:", upload_var),
    ("Ping:", ping_var),
    ("Your ISP:", isp_var),
    ("Test Server:", server_var)
]

for i, (label, var) in enumerate(labels):
    ttk.Label(frame, text=label).grid(row=i, column=0, sticky="e", padx=10, pady=5)
    ttk.Label(frame, textvariable=var).grid(row=i, column=1, sticky="w", padx=10, pady=5)

label_status = tk.Label(app, text="", font=("Segoe UI", 10), bg="#1e1e1e", fg="#cccccc")
label_status.pack(pady=10)

test_button = ttk.Button(app, text="Run Speed Test", command=run_speed_test)
test_button.pack(pady=10)

app.mainloop()

