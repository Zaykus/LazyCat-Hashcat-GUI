# 🐱 LazyCat Cracker // Purr-fessional Edition

**LazyCat** is a modern, dark-themed GUI wrapper for **Hashcat**, designed specifically for cracking WPA/WPA2 Wi-Fi Handshakes (`.hc22000`). It turns complex command-line attacks into a simple "Point & Click" experience.

## ✨ Features

* **Stealth UI:** Deep black/gray theme with integrated read-only terminal logs.
* **Auto-Detection:** Automatically identifies your GPU IDs and Hashcat engine location.
* **Crash Handler:** Built-in "Safe Mode" that generates debug logs if an error occurs.
* **Smart Wordlists:** Auto-scans the `/wordlists` directory for compatible text files.
* **Target Helper:** Integrated link to convert `.cap` files to Hashcat-ready formats.
* **Safe Execution:** Runs commands in a dedicated thread to prevent UI freezing.

---

## 📦 Downloads & Installation

We provide two separate packages to keep download sizes optimized.

### 1. The App (Required)

Download **`LZC-Stand-alone.7z`**.

* Includes `LazyCat.exe` and the full **Hashcat Engine**.
* **How to use:** Extract the contents to a folder and run the executable.

### 2. The Wordlists (Optional)

Download **`LZC-Wordlists.7z`**.

* Includes `rockyou.txt` and `piotrcki-top10m.txt`.
* **How to use:** Extract the `wordlists` folder and place it in the **same directory** as `LazyCat.exe`.

### 📂 Folder Structure

To ensure everything runs smoothly, your folder should look like this:

```text
/LazyCat_Folder/
  ├── LazyCat.exe        <-- Main Application
  ├── hashcat/           <-- (Included in Stand-alone)
  └── wordlists/         <-- (Place your .txt files here)
       ├── rockyou.txt
       └── top-passwords.txt

```

---

## 🛠️ Usage Guide

1. **Target:** Click **"OPEN CONVERTER"** to turn your Wireshark `.cap` file into a `.hc22000` file. Load the resulting file into the app.
2. **Hardware:** Click **"TEST GPU"**. Note the Device ID (usually 1 or 2) and enter it in the GPU ID box.
3. **Attack Selection:**
* **Wordlist:** Select a dictionary file from the dropdown.
* **Brute-Force:** Enter a mask (e.g., `?d?d?d?d?d?d?d?d` for 8-digit numeric passwords).


4. **Execute:** Click **"START ATTACK"**. You can monitor progress via the terminal log.
5. **Result:** If a match is found, a success notification will appear. Click **"DECRYPT RESULT"** to view the password.

---

## ⚠️ Disclaimer

> This tool is for **educational purposes** and **authorized security testing** only. The usage of this tool for attacking targets without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---
