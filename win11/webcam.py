import cv2

# Open the capture device
cap = cv2.VideoCapture('/dev/video0')

# Check if the capture device is opened successfully
if not cap.isOpened():
    print("Error: Could not open capture device")
else:
    while True:
        # Read a frame from the capture device
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture device and close the window
    cap.release()
    cv2.destroyAllWindows()
