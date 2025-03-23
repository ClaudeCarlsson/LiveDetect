import cv2

# Try different indices if 0 doesn't work
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera. Please check your camera connection or try a different index.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('Live Camera Feed', frame)
    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
