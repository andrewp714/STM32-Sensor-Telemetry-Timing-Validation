# STM32 Sensor Telemetry Timing Validation
Implemented a timer-based data acquisition system on STM32F401RE with interrupt-driven sampling, UART telemetry, and validation of timing accuracy and jitter using oscilloscope measurements and Python analysis.

## 📌 Overview

This project implements a timer-driven data acquisition system on an STM32F401RE.
It samples analog data at fixed intervals, transmits telemetry over UART, and validates system timing using both an oscilloscope and Python-based analysis.

---

## ⚙️ System Architecture

```
Analog Signal → ADC → UART → Python → Analysis & Visualization
                ↑
             Timer (1 kHz)
```

---

## 🔧 Features

* Timer-driven deterministic sampling (TIM2 interrupt)
* 12-bit ADC acquisition (0–4095 range)
* UART telemetry streaming (timestamp + ADC value)
* Oscilloscope-based timing validation
* Python-based analysis:

  * Sampling interval verification
  * Jitter measurement
  * Anomaly detection
  * Data visualization

---

## 📊 Results

### ⏱ Timing Validation

* Expected sampling rate: **1 kHz**
* Measured sampling rate: **~1000 Hz**
* Mean dt: **1.0 ms**
* Jitter: **0.0 ms**
* Missing samples: **0**

### 🔌 Voltage Measurement

ADC readings converted to voltage:

[
V = \frac{ADC}{4095} \times 3.3
]

Observed range:

* ~0.75 V to ~0.96 V (floating input noise)

---

## 📸 Oscilloscope Validation

* Before optimization: ~470 Hz
* After optimization: ~505 Hz
* Verified improved timing after removing blocking operations from ISR

---

## 🧠 Key Insight

Blocking operations (ADC polling + UART transmission) inside interrupts degrade timing accuracy.
Refactoring to a flag-based design ensures deterministic behavior.

---

## 🐍 Python Analysis

The Python script:

* Parses UART telemetry
* Computes sampling interval and jitter
* Detects missing samples
* Logs data to CSV
* Plots ADC/voltage vs time

---

## 🚀 How to Run

### Firmware

1. Flash STM32 using STM32CubeIDE
2. Connect UART (115200 baud)

### Python

```bash
pip install pyserial matplotlib numpy
python analysis.py
```

---

## 📈 Example Output

```
Mean dt: 1.0
Jitter: 0.0
Estimated sample rate: 1000 Hz
Missing samples: 0
Out of range values: 0
```

---

## 🎯 Conclusion

This project demonstrates a complete embedded telemetry pipeline with validated timing accuracy and real-time data analysis.

---
