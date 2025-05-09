from google import genai
from pydantic import BaseModel
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

class Answer(BaseModel):
    name: str
    time: str
    order: list[str]

class Response(BaseModel):
    end: bool
    note: str 
    answer: Answer
    response: str

def get_API_key():
    with open('./Gemini_API_key.txt', 'r') as key:
        return key.read()

def chat_with_gemini(user_input):
    global prompt
    
    content = prompt+f'{state}\n目前時間{datetime.now()}\nUser:{user_input}'
    # print(content)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=content,
        config={
            "response_schema": Response,
            "response_mime_type": "application/json",
        }
    )
    return response
    
prompt = '''<zh>你要與使用者進行多輪問答，依序問出使用者的姓名、用餐日期時間(使用者可能會用相對時間，你要自己轉成yyyy/mm/dd hh:mm)、餐點。當你收集完答案時，必須要做一次最後確認，必須等使用者回覆確認後再表達對使用者的感謝，然後才能結束對話。
目前狀態
'''
state = ''
history = []

SHEET_URL = 'https://docs.google.com/spreadsheets/d/1iFnmo2VQkHuYrIsXRbxv-zOZzuUONwI-nQDk5ZdOLXU/edit?usp=sharing'
def write_to_sheet(data):
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SHEET_URL).sheet1
    history_QA = [f'Agent: {QA["Agent"]}'+ (('\n'+f'{"User: "+QA.get("User", "")}'+'\n')if "User" in QA else "") for QA in history]
    row = [data.name, data.time, ", ".join(data.order), "\n".join(history_QA)]
    sheet.append_row(row)

def main():
    global state, history
    user_input = ''
    while True:
        reply = chat_with_gemini(user_input)
        parsed: Response = reply.parsed # type: ignore
        state = parsed
        # print(reply.text)
        history.append({'Agent':parsed.response})
        if parsed.end:
            print(parsed.response)
            break
        # print(parsed.note)
        user_input = input(parsed.response+'\n')
        history[-1]['User'] = user_input
        print()

    print('對話結束')
    write_to_sheet(parsed.answer)

# 設計⼀個問卷，透過問答，搜集問卷答案，並將結果寫⼊ Google Sheet 中
if __name__ == '__main__':
    API_key = get_API_key()
    client = genai.Client(api_key=API_key)
    main()


