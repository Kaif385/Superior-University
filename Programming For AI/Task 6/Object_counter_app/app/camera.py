import os
from ultralytics import YOLO
model_path = os.path.join(os.getcwd(), "models", "yolov8n.pt")
model = YOLO(model_path)
import cv2


def detect_animals(image_path):
    img = cv2.imread(image_path)
    results = model(img)

    detected_animals = []

    for result in results:
        for box in result.boxes:
            cls_index = int(box.cls[0])
            label = result.names[cls_index]
            detected_animals.append(label)

            # Draw bounding box on image
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.9, (0, 255, 0), 2)

    detected_animals = list(set(detected_animals))

    # Save the image with boxes
    output_image_path = os.path.join(os.getcwd(), "app", "static", "uploads", "marked_" + os.path.basename(image_path))
    cv2.imwrite(output_image_path, img)

    result_text = f"Detected animals in {os.path.basename(image_path)}: {', '.join(detected_animals)}"
    return result_text, output_image_path
