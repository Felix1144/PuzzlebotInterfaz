from flask import Flask, render_template, Response
import rospy
from sensor_msgs.msg import CompressedImage
import threading

app = Flask(__name__)

# Variable global para almacenar la última imagen recibida
last_image = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/image')
def get_image():
    global last_image
    if last_image is not None:
        return Response(last_image, mimetype='image/jpeg')
    else:
        return jsonify({"error": "No image received"}), 404

def callback(data):
    global last_image
    last_image = data.data

def listener():
    rospy.init_node('web_image_listener', anonymous=True)
    rospy.Subscriber('/camera/image/compressed', CompressedImage, callback)
    rospy.spin()

if __name__ == '__main__':
    threading.Thread(target=listener).start()
    app.run(host='0.0.0.0', port=5000)
