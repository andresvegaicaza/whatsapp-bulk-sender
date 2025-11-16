# WhatsApp Bulk Sender  
**Automated personalized WhatsApp message sender using Python, Excel, and PyWhatKit**

This project allows you to send **personalized WhatsApp messages with optional images** to large lists of customers stored in an Excel file, while safely tracking which messages were already sent.  
It automates **WhatsApp Web** using PyWhatKit and requires **CopyQ** for reliable clipboard operations on macOS and Linux.

---

## 🚀 Features

- Reads customer data from an Excel file (`customers.xlsx`)
- Builds fully personalized messages based on attributes in the database
- Sends WhatsApp messages **with an image attachment** via WhatsApp Web
- Automatically updates the Excel file (`SentFlag = 1`) so you don’t resend messages
- Safe to re-run multiple times
- Works for:
  - Marketing campaigns  
  - Promotions  
  - Reminders  
  - Event invites  
  - Save-the-dates  
  - General notifications  
- Fully configurable and extensible

---

## 📁 Project Structure


---

## 🧪 Example Excel Input (`customers.xlsx`)

Your Excel file must contain:

| Column         | Description                                  |
|----------------|----------------------------------------------|
| `Phone`        | Customer phone number                        |
| `Name`         | Customer name                                |
| `City`         | Customer city (optional)                     |
| `Segment`      | Customer segment (optional)                  |
| `MessageLabel` | Personalized label (optional)                |
| `SendFlag`     | `1` = send, `0` = skip                       |
| `SentFlag`     | `1` = already sent, `0` = not sent yet       |

### ✔ Example row:

| Phone         | Name   | City | Segment | MessageLabel      | SendFlag | SentFlag |
|---------------|--------|------|---------|--------------------|----------|----------|
| 5215555555555 | Laura  | CDMX | Premium | Laura y familia    | 1        | 0        |

Only customers where:


will receive messages.

---

## 🧠 How the message is personalized

The script uses:

- `MessageLabel` → If present, used as greeting  
- otherwise falls back to `Name`  
- inserts `City` and `Segment` when available  
- includes **TEST MODE** label if enabled  

### ✔ Example generated message:

