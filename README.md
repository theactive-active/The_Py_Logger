Local Keylogger (Educational Use Only)

⚠️ Important Notice
This keylogger is provided strictly for ethical, legal, and educational purposes only.
Use it only on machines you personally own or have explicit written consent to test on.
Never deploy it on someone else’s device without permission — doing so is illegal.

⸻

Overview

This project demonstrates how to capture keyboard input locally and save it to a hidden file. Unlike malicious keyloggers, this one does not transmit data over the network — everything stays on your own computer.

The script:
	•	Runs locally on your PC.
	•	Captures keystrokes using the pynput library.
	•	Writes logs to a hidden file in your home directory (e.g., ~/.hidden_keystrokes.log on Linux/macOS, hidden file attribute on Windows).
	•	Prints the full path to the log file on startup so you can find it.
	•	Handles log rotation if the file grows larger than 10 MB.

⸻

Requirements
	•	Python 3.8+
	•	pip installed
	•	Dependencies listed in requirements.txt

Install dependencies:

pip install -r requirements.txt


⸻

Running the Keylogger
	1.	Open a terminal/command prompt.
	2.	Navigate to the folder containing the script:

cd path/to/project


	3.	Run the script:

python keylogger.py


	4.	On startup, the program prints where the log file is stored, for example:

Log file saved at: /home/username/.hidden_keystrokes.log


	5.	Stop the program anytime with Ctrl+C (or by killing the process).

⸻

Viewing the Logs
	•	Navigate to your home directory and look for .hidden_keystrokes.log.
	•	Open it with a text editor:

cat ~/.hidden_keystrokes.log

or on Windows, open the file with Notepad once you’ve made hidden files visible.

Each log line contains:

YYYY-MM-DD HH:MM:SS - PRESSED/RELEASED - KEY


⸻

Example Log Output

2025-10-02 12:00:01 - PRESSED  - h
2025-10-02 12:00:01 - PRESSED  - e
2025-10-02 12:00:02 - PRESSED  - l
2025-10-02 12:00:02 - PRESSED  - l
2025-10-02 12:00:03 - PRESSED  - o
2025-10-02 12:00:03 - PRESSED  - [SPACE]
2025-10-02 12:00:04 - PRESSED  - w
2025-10-02 12:00:04 - PRESSED  - o
2025-10-02 12:00:04 - PRESSED  - r
2025-10-02 12:00:05 - PRESSED  - l
2025-10-02 12:00:05 - PRESSED  - d


⸻

Ethical Use Cases
	•	Demonstrating logging concepts in a cybersecurity course.
	•	Researching how malware captures input.
	•	Teaching students how to detect keyloggers.
	•	Experimenting on your own machine for defensive learning.

⚠️ Never use this for malicious purposes. Unauthorized use is illegal and punishable by law.

Clear-Content -Path "$env:USERPROFILE\.hidden_keystrokes.log" -Force

Get-Item "$env:USERPROFILE\.hidden_keystrokes.log" | Select-Object FullName,Length