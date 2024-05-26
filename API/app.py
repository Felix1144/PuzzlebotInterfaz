from flask import Flask, render_template, Response, jsonify
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
        app.logger.info("Serving image")
        return Response(last_image, mimetype='image/jpeg')
    else:
        app.logger.warning("No image received yet")
        return jsonify({"error": "No image received"}), 404

def callback(data):
    global last_image
    app.logger.info("Received image with timestamp: %s",data.header.stamp)
    last_image = data.data
    app.logger.info("Received  image data size %d bytes",len(last_image))

def listener():
    rospy.init_node('web_image_listener', anonymous=True)
    rospy.Subscriber("/image_topic/compressed", CompressedImage, callback)
    rospy.loginfo("ROS node initialized and subscriber created")
    rospy.spin()

if __name__ == '__main__':
    app.logger.info("Starting Flask Server")
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0',port=5000))
    flask_thread.start()
    listener()
    #threading.Thread(target=listener).start()
    #app.run(host='0.0.0.0', port=5000)
