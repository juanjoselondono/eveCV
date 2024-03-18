from yolov5.models.experimental import attempt_load
from yolov5.utils.general import non_max_suppression, scale_coords
from torch.backends import cudnn
import torch

# Load YOLOv5 model
model = attempt_load('yolov5s.pt', map_location=torch.device('cpu'))  # Load YOLOv5s model

# Set YOLOv5 to inference mode
model.eval()

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Run inference on live stream
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert image to torch tensor
    img = torch.from_numpy(frame).to(device)

    # Inference
    pred = model(img, augment=False)[0]

    # Apply non-maximum suppression
    pred = non_max_suppression(pred, conf_thres=0.65, iou_thres=0.45)

    # Process detections
    for det in pred:
        if det is not None and len(det):
            # Rescale boxes from img_size to frame size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()

            # Iterate over detections and draw bounding boxes
            for *xyxy, conf, cls in det:
                if int(cls) == 0:  # Check if class is 'person'
                    person_boxes = xyxy  # Extract bounding box coordinates
                    print('person: ', person_boxes)

    # Show frame
    cv2.imshow('YOLOv5', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
