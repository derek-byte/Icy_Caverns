from flask import Flask, render_template, Response, request
from camera import VideoCamera
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        email = request.form['emailInput']

        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("derek55003@gmail.com")
        to_email = To(email)
        subject = "Someone Has Reached The Icy Caverns"
        content = Content("text/plain", "Someone has challenged you to a game of Icy Caverns! Click the link below to play!")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

        return render_template('index.html', confirmation="Email Sent to: "+email)
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