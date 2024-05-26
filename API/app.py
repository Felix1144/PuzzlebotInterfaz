from flask import Flask, render_template, Response, jsonify
import rospy
from std_msgs.msg import Float32
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Vector3, Twist, Point, Pose, Quaternion
from nav_msgs.msg import Odometry
import tf.transformations as tf
import threading

app = Flask(__name__)

# Variable global para almacenar la última imagen recibida
last_image = None
robot_data = {
    'vel_v' : 0.0,
    'vel_w' : 0.0,
    'wl' : 0.0,
    'wr' : 0.0,
    'theta' : 0.0,
    'x' : 0.0,
    'y' : 0.0
}


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

@app.route('/data')
def get_data():
    global robot_data
    return jsonify(robot_data)

def callback_image(data):
    global last_image
    #app.logger.info("Received image with timestamp: %s",data.header.stamp)
    last_image = data.data
    #app.logger.info("Received  image data size %d bytes",len(last_image))

def callback_velocity(data):
    global robot_data
    robot_data['vel_v'] = data.linear.x
    robot_data['vel_w'] = data.angular.z

def callback_position(data):
    global robot_data
    robot_data['x'] = data.pose.pose.position.x
    robot_data['y'] = data.pose.pose.position.y
    robot_data['theta'] = orientation_as_euler(data.pose.pose.orientation)

def callback_wl(data):
    global robot_data
    robot_data['wl'] = data.data

def callback_wr(data):
    global robot_data
    robot_data['wr'] = data.data

def orientation_as_euler(quat):
    euler = tf.euler_from_quaternion((quat.x, quat.y, quat.z, quat.w))
    yaw = euler[2]
    return yaw


def listener():
    rospy.init_node('web_image_listener', anonymous=True)
    rospy.Subscriber("/image_topic/compressed", CompressedImage, callback_image)
    rospy.Subscriber("/cmd_vel", Twist, callback_velocity)
    rospy.Subscriber("/puzzlebot/odom", Odometry, callback_position)
    rospy.Subscriber("/wl",Float32, callback_wl)
    rospy.Subscriber("/wr", Float32, callback_wr)
    rospy.loginfo("ROS node initialized and subscriber created")
    rospy.spin()

if __name__ == '__main__':
    app.logger.info("Starting Flask Server")
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0',port=5000))
    flask_thread.start()
    listener()
    #threading.Thread(target=listener).start()
    #app.run(host='0.0.0.0', port=5000)
