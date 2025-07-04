# Questionnaire_AI_Agent

這是一個簡單的問卷 demo，透過 Google Gemini 模型與使用者互動提問，收集以下資訊：

- 姓名  
- 用餐時間（格式：`yyyy/mm/dd hh:mm`）  
- 用餐內容（可為多項）

資料將自動寫入指定的 Google Sheet。

---

## 檔案與目錄結構

請將以下兩個檔案放在與 `main.py` 相同的目錄下：

- `Gemini_API_key.txt`：存放你的 Gemini API 金鑰  
- `credentials.json`：Google Sheets 的服務帳號憑證檔

> ⚠️ 這兩個檔案不會包含在 GitHub 中，請自行建立並避免上傳。

---

## 注意事項

- 所有收集到的資料將寫入以下 Google Sheet：  
  **[https://docs.google.com/spreadsheets/d/1iFnmo2VQkHuYrIsXRbxv-zOZzuUONwI-nQDk5ZdOLXU/edit?usp=sharing](#)**

- 請勿輸入任何敏感或個人隱私資訊。

---

## 安裝相依套件

```bash
pip install -r requirements.txt
```