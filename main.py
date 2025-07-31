from flask import Flask, request, render_template_string
from instagrapi import Client
import time

app = Flask(__name__)

# 🔐 Hardcoded Instagram login credentials
INSTAGRAM_USERNAME = "rohan929wis"
INSTAGRAM_PASSWORD = "pandit@ak90"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Instagram DM Sender</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
<div class="container mt-5" style="max-width:500px">
    <h2 class="text-center">Instagram DM Sender</h2>
    <form method="post" enctype="multipart/form-data">
        <div class="mb-3">
            <label>Target Username</label>
            <input type="text" name="target" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Message File (.txt)</label>
            <input type="file" name="message_file" class="form-control" accept=".txt" required>
        </div>
        <div class="mb-3">
            <label>Delay (seconds)</label>
            <input type="number" name="delay" class="form-control" required>
        </div>
        <button class="btn btn-primary w-100">Send Messages</button>
    </form>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        try:
            target = request.form['target']
            delay = int(request.form['delay'])
            file = request.files['message_file']

            filepath = 'messages.txt'
            file.save(filepath)

            with open(filepath, 'r', encoding='utf-8') as f:
                messages = f.read().splitlines()

            cl = Client()
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            user_id = cl.user_id_from_username(target)

            for msg in messages:
                cl.direct_send(msg, [user_id])
                time.sleep(delay)

            return f"✅ Sent {len(messages)} messages to @{target}"

        except Exception as e:
            return f"❌ Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
