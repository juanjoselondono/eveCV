from ultralytics import YOLO

# Initialize the YOLO model
model = YOLO('yolov8n-seg.pt')
# classes for model yolov8n-seg.pt:{0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}


# Run inference without showing or saving the results
results = model(stream = True, show = True,source=1, conf=0.5, save=False)

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

    # Concatenate vertical and horizontal positions
    position = f"{horizontal_position}"

    return position
    #return positions


for result in results:
    detection_class = result.boxes.cls
    if detection_class.numel() > 0 and detection_class.numel() == 1:
        # Get the value as a scalar
        detected_class = detection_class.item()
        #check if object is a person
        if(detection_class == 0):
            person_box = result.boxes.cpu().numpy().xyxy[0]
            frame_shape = (640, 480)  # Example frame dimensions
            positions = get_person_position(frame_shape, person_box)
            print("Person positions:", positions)
            

