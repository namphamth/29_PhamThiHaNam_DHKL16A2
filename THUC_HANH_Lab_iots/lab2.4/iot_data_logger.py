import csv
import json
import time
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

# Định nghĩa tệp CSV
CSV_FILE = "sensor_data.csv"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/khdl/esp32"

# Tạo file CSV nếu chưa có
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "temperature", "humidity"])

temps, hums, times = [], [], []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Đã kết nối MQTT broker.")
        client.subscribe(MQTT_TOPIC)
    else:
        print("❌ Kết nối thất bại, mã lỗi:", rc)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        timestamp = data.get("timestamp", time.time())
        temp = data.get("temperature", 0)
        hum = data.get("humidity", 0)

        print(f"📥 Dữ liệu nhận được: {timestamp}, {temp}, {hum}")

        # Lưu dữ liệu vào CSV
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, temp, hum])

        temps.append(temp)
        hums.append(hum)
        times.append(timestamp)

        # Hiển thị thông báo đã gửi dữ liệu
        print(f"✅ Đã gửi dữ liệu: {timestamp}, {temp}, {hum}")

        # Vẽ biểu đồ sau mỗi 10 bản ghi
        if len(temps) % 10 == 0:
            plt.clf()  # Clear figure

            plt.subplot(2, 1, 1)
            plt.plot(times, temps, 'r-', label='Nhiệt độ (°C)')
            plt.legend()

            plt.subplot(2, 1, 2)
            plt.plot(times, hums, 'b-', label='Độ ẩm (%)')
            plt.legend()

            plt.pause(0.1)  # Cập nhật đồ thị

    except Exception as e:
        print("⚠️ Lỗi xử lý dữ liệu:", e)

# Khởi tạo client MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Kết nối với broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Chế độ vẽ biểu đồ tương tác
plt.ion()

# Bắt đầu vòng lặp MQTT
client.loop_forever()
