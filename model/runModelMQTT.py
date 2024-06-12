import paho.mqtt.client as mqtt
from ultralytics import YOLO
import json

# Initialize the YOLO model
model = YOLO('yolov8n-seg.pt')
# classes for model yolov8n-seg.pt:{0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}


# Run inference without showing or saving the results
results = model(stream = True, show = True,source=0, conf=0.6, save=False,imgsz = 480)
#Setup Mqtt communication
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed")

def on_publish(client, userdata, mid):
    print("Message published")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect("localhost", 1883, 60)

# Publish a message to a topic
topic = "test"
message = "Hello, this the data stream from the camera"
client.publish(topic, message)

# Define a function to get the position of a person in the frame
def get_person_position(frame_shape, person_box):
    # Extract frame dimensions
    frame_width, frame_height = frame_shape[:2]

    print('shape',  person_box.shape)
    x1, y1, x2, y2 = person_box

    # Calculate center of the bounding box
    box_center_x = (x1 + x2) / 2
    box_center_y = (y1 + y2) / 2

    # Calculate center of the frame
    frame_center_x = frame_width / 2
    frame_center_y = frame_height / 2
    # calculate size of the bounding box
    box_size = (x2 - x1) * (y2 - y1)
    print('box_size', box_size)

    # Determine position based on bounding box center relative to the frame center
    if box_center_y < frame_center_y - frame_height / 8:
        vertical_position = "Up"
    elif box_center_y > frame_center_y + frame_height / 8:
        vertical_position = "Down"
    else:
        vertical_position = "Center"

    if box_center_x < frame_center_x - frame_width / 8:
        horizontal_position = "Left"
    elif box_center_x > frame_center_x + frame_width / 8:
        horizontal_position = "Right"
    else:
        horizontal_position = "Center"
    
    #now determinate wheter the person is close or far
    print('box size:',box_size)
    if int(box_size) > 200000:
        distance = "Close"
    elif int(box_size) < 200000 and int(box_size) > 100000:
        distance = "Neutral"
    else:
        distance = "Far"

    # Concatenate vertical and horizontal positions
    
    position = {
        "horizontal_position": horizontal_position, 
        "distance": distance,
    }

    return position

for result in results:
    detection_boxes = result.boxes.cpu().numpy()  # Extract bounding boxes
    detection_classes = result.boxes.cls.cpu().numpy()  # Extract class labels

    # Iterate through detections
    for cls, box in zip(detection_classes, detection_boxes):
        # Check if the detected class is "person"
        if cls == 0:  # Assuming "person" is the class label for people
            # Get bounding box coordinates
            frame_shape = (640, 550)  # Example frame dimensions
            person_box = detection_boxes.xyxy[0]  # Example bounding box coordinates
            positions = get_person_position(frame_shape, person_box)
            positions = str(positions)
            print("Person positions:", positions)
            client.publish(topic, positions, qos=0)


client.disconnect()


