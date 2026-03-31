# Original Work by Andrew Pham

import serial
import numpy as np
import matplotlib.pyplot as plt
import csv

# ---------- Step 1: Read Serial Data ----------
# Open serial port (must match STM32 UART settings)
ser = serial.Serial('COM4', 115200)

data = []

# Collect a fixed number of samples from UART (10k+)
for _ in range(10002):
    line = ser.readline().decode().strip()

    try:
        # Parse formatted string: "t=123 ms, adc=2048"
        parts = line.split(',')

        t = int(parts[0].split('=')[1].replace(' ms', ''))
        val = int(parts[1].split('=')[1])

        data.append((t, val))

    except:
        # Skip malformed or incomplete lines
        continue

ser.close()

print("Collected samples:", len(data))


# ---------- Step 2: Timing Validation ----------
# Extract timestamps and compute time differences between samples
timestamps = np.array([d[0] for d in data])
dt = np.diff(timestamps)

# Check sampling consistency
print("Mean dt:", np.mean(dt))          # expected ~1 ms
print("Jitter (std):", np.std(dt))      # variation in sampling interval

# Estimate effective sampling rate
sample_rate = 1000 / np.mean(dt)        # convert ms to Hz
print("Estimated sample rate (Hz):", sample_rate)


# ---------- Step 3: Anomaly Detection ----------
# Extract ADC values
values = np.array([d[1] for d in data])

# Detect missing samples (non-1 ms intervals)
missing_samples = np.sum(dt != 1)

# Detect invalid ADC readings (outside 12-bit range)
out_of_range = np.sum((values < 0) | (values > 4095))

print("Missing samples:", missing_samples)
print("Out of range values:", out_of_range)


# ---------- Step 4: Logging ----------
# Save collected data to CSV for offline analysis
with open("log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "value"])
    writer.writerows(data)

print("Data saved to log.csv")


# ---------- Step 5: Plot ----------
# Visualize ADC data over time
plt.figure(figsize=(10,5))
plt.plot(timestamps, values)
plt.title("ADC vs Time")
plt.xlabel("Time (ms)")
plt.ylabel("ADC Value")
plt.grid()
plt.show()

# Visualize Voltage over time
voltages = values * 3.3 / 4095  # Convert ADC counts to voltage

plt.figure(figsize=(10,5))
plt.plot(timestamps, voltages)
plt.title("Voltage vs Time")
plt.xlabel("Time (ms)")
plt.ylabel("Voltage (V)")
plt.grid()
plt.show()
