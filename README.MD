# 🐱 LazyCat Cracker // Purr-fessional Edition

**LazyCat** is a modern, dark-themed GUI wrapper for **Hashcat**, designed specifically for cracking WPA/WPA2 Wi-Fi Handshakes (`.hc22000`). It turns complex command-line attacks into a simple "Point & Click" experience.

## ✨ Features

* **Stealth UI:** Deep black/gray theme with integrated read-only terminal logs.
* **Auto-Detection:** Automatically identifies your GPU IDs and Hashcat engine location.
* **Smart Wordlists:** Auto-scans the `/wordlists` directory for compatible text files.
* **Safe Execution:** Runs commands in a dedicated thread to prevent UI freezing.

---

## 📦 Downloads & Installation

### 1. The App (Required)

Download **`LZC-Stand-alone.7z`**.

* Includes `LazyCat.exe` and the core Hashcat binaries.

### 2. The Wordlists (Optional)

Download **`LZC-Wordlists.7z`**.

* Contains `rockyou.txt` and other top-tier dictionaries.

### 📂 Folder Structure

Ensure your directory looks exactly like this for the app to function:

```text
/LazyCat_Folder/
  ├── LazyCat.exe        <-- Main Application
  └── wordlists/         <-- Folder containing .txt files

```

---

## 🛠️ Troubleshooting & Manual Setup

If you receive an error stating that the **Hashcat Engine was not found**, or if `hashcat.exe` is missing from your folder:

1. **Download the Engine:** Visit the official [Hashcat Website](https://hashcat.net/hashcat/) and download the latest Windows binaries.
2. **Extract:** Open the downloaded `.7z` file.
3. **Placement:** Move the extracted folder into your LazyCat directory and rename it to simply `hashcat`.
4. **Verify:** Your `LazyCat.exe` should now see the `hashcat/hashcat.exe` path clearly.

---

## 📜 Credits

This tool is a GUI wrapper. The heavy lifting is done by the world's fastest cracker:

* **Engine:** [Hashcat](https://hashcat.net/) by Jens "atom" Steube and the Hashcat team.

---

## ⚠️ Disclaimer

> This tool is for **educational purposes** and **authorized security testing** only. The usage of this tool for attacking targets without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

---
