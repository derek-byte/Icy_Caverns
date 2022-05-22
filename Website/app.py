from flask import Flask, render_template, Response, request
from camera import VideoCamera
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        top_score = 107
        email = request.form['emailInput']

        message = Mail(from_email='derek55003@gmail.com',
                        to_emails=email,
                        subject='Icy Caverns',
                        plain_text_content='Someone has challenged you to a game of Icy Caverns! Click the link below to play! The score to beat is 107.',
                        html_content='<strong>Someone has challenged you to a game of Icy Caverns! Click the link below to play! The score to beat it 107</strong>')
        try:
            sg = SendGridAPIClient(os.environ('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return render_template('index.html')
    else:
        return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)