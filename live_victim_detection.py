# import cv2
# import os
# from ultralytics import YOLO
#
# # ================= CONFIGURATION =================
# # 1. Path to your trained model (use best.pt for highest accuracy)
# MODEL_PATH = r'C:\Users\troll\PycharmProjects\PythonProject5\runs\detect\train58\weights\best.pt'
#
# # 2. Camera index (0 = default webcam, 1/2 = external cameras)
# CAMERA_INDEX = 0
#
# # 3. Confidence threshold for detections (0.0 to 1.0)
# CONF_THRESHOLD = 0.5
# # =================================================
#
# # Verify model exists
# if not os.path.exists(MODEL_PATH):
#     raise FileNotFoundError(f"Model not found at: {MODEL_PATH}\nCheck your training runs folder.")
#
# # Load trained model
# print(f"🔹 Loading model from: {MODEL_PATH}")
# model = YOLO(MODEL_PATH)
#
# # Print available classes to verify your dataset labels
# print(f"🔹 Available classes in model: {model.names}")
# if 'victim' not in model.names.values():
#     print("Warning: 'victim' class not found in model names. Check your dataset labels.")
#
# # Initialize camera
# cap = cv2.VideoCapture(CAMERA_INDEX)
# if not cap.isOpened():
#     print("Error: Could not open camera.")
#     exit()
#
# print(f"Camera initialized. Capturing a single frame...")
# ret, frame = cap.read()
# cap.release()  # Release camera immediately since we only need one frame
#
# if not ret:
#     print("Error: Failed to capture frame.")
#     exit()
#
# # Run inference on the captured frame
# print("Running victim detection...")
# results = model(frame, conf=CONF_THRESHOLD)
# result = results[0]  # YOLO returns a list; we take the first (and only) frame
#
# # Process detections
# victim_found = False
# if result.boxes is not None and len(result.boxes) > 0:
#     for box in result.boxes:
#         # Extract coordinates, confidence, and class
#         x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().tolist())
#         conf = float(box.conf[0].item())
#         cls_id = int(box.cls[0].item())
#         class_name = model.names[cls_id]
#
#         # Draw bounding box & label
#         color = (0, 255, 0) if class_name == 'victim' else (0, 0, 255)  # Green=victim, Red=other
#         cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
#         label_text = f"{class_name} {conf:.2f}"
#         cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#
#         if class_name == 'victim':
#             victim_found = True
#
# # Print final status
# print("\n" + "="*30)
# print("DETECTION RESULT")
# print("="*30)
# if victim_found:
#     print("STATUS: VICTIM DETECTED!")
# else:
#     print("STATUS: No victim detected in the frame.")
# print("="*30 + "\n")
#
# # Save and display the annotated frame
# output_path = 'victim_detection_result.jpg'
# cv2.imwrite(output_path, frame)
# print(f"Annotated frame saved to: {os.path.abspath(output_path)}")
#
# print("Press any key to close the image window...")
# cv2.imshow('Victim Detection Result', frame)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import os
import cv2
from ultralytics import YOLO

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Path to your trained best model
MODEL_PATH = 'C:/Users/troll/PycharmProjects/PythonProject5/runs/detect/train58/weights/best.pt'

# Load the trained model
model = YOLO(MODEL_PATH)

# Initialize camera (0 = default webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("Camera initialized. Press any key to capture and detect, or 'q' to quit.")

while True:
    # Show live preview
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    cv2.imshow('Live Preview - Press SPACE to detect, Q to quit', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        print("Exiting...")
        break
    elif key == ord(' '):
        print("Capturing frame for detection...")

        # Run detection on the captured frame
        results = model(frame, imgsz=640, conf=0.28)

        # Plot results on the frame
        annotated_frame = results[0].plot()

        # Display the result
        cv2.imshow('Detection Result', annotated_frame)
        print(f"Detection complete. Found {len(results[0].boxes)} object(s).")

        # Wait for user to view result, then return to preview
        print("Press any key to return to live preview...")
        cv2.waitKey(0)
        cv2.destroyWindow('Detection Result')

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Camera released. Program ended.")