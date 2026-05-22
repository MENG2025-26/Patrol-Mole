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