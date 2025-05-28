from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

# הגדרות בסיס
app = Flask(__name__)
DOCUMENT_ID = '1zTVBxrfzztv3irl6QCYZjbpgd3AYoTVKQrMB3FzW1yw'
import os
import json

SCOPES = ['https://www.googleapis.com/auth/documents']

service_account_info = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))

creds = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)

# בניית שירות ה־Docs
docs_service = build('docs', 'v1', credentials=creds)

@app.route('/add_note', methods=['POST'])
def add_note():
    data = request.get_json()
    note = data.get("text")
    
    if not note:
        return jsonify({"error": "Missing 'text'"}), 400

    # הכנסת התובנה למסמך
    requests = [{
        'insertText': {
            'location': {'index': 1},
            'text': f'\n🟢 {note}\n'
        }
    }]

    try:
        docs_service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': requests}
        ).execute()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# הפעלת השרת
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
