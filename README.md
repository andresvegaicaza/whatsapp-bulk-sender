# WhatsApp Bulk Sender (Python + Excel + PyWhatKit)

## 🛠 Environment Setup

This project runs on Python 3 and automates WhatsApp Web.  
Below are the setup instructions for **macOS**, **Linux**, and **Windows**.

---

### 1️⃣ Common Requirements (All Platforms)

- Python **3.8+** (recommended: 3.10+)
- pip (Python package manager)
- Git
- Google Chrome (recommended browser)
- Active WhatsApp Web session:
  - https://web.whatsapp.com
  - Stay logged in during execution

---

### 2️⃣ macOS Setup

#### Install Homebrew (if not installed)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Install Python and Git
```
brew install python git
```

#### Install CopyQ (REQUIRED)
PyWhatKit uses the clipboard to paste messages.  
macOS requires **CopyQ**:
```
brew install --cask copyq
open -a CopyQ
```

#### Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 3️⃣ Linux Setup (Debian/Ubuntu)

#### Install Python, pip, Git
```
sudo apt update
sudo apt install -y python3 python3-pip git
```

#### Install CopyQ (REQUIRED)
```
sudo apt install -y copyq
copyq --version
copyq &
```

#### Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 4️⃣ Windows Setup

#### Install Python and Git
Download:
- Python: https://www.python.org/downloads/
- Git for Windows: https://git-scm.com/download/win

Verify:
```
python --version
git --version
```

#### CopyQ (OPTIONAL)
Windows has native clipboard support → CopyQ not required.

#### Create virtual environment
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### 5️⃣ Final Checklist Before Running

- Virtual environment activated  
- Dependencies installed  
- `customers.xlsx` and `promo.jpg` present  
- WhatsApp Web open and logged in  
- On macOS/Linux: **CopyQ running**  
- Do **not** use keyboard/mouse during message sending  
