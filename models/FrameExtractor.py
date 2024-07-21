
import cv2
import pafy
import time
import os

# YouTube video URL
video_url = 'https://www.youtube.com/watch?v=HBDD3j5so0g'

# Set up video streaming
video = pafy.new(video_url)
best_stream = video.getbest(preftype="mp4")
cap = cv2.VideoCapture(best_stream.url)

# Create the output directory for frames
output_dir = "C://Users//rooyv//Documents//Loyalist//TERM 2//STEP 2//Extracted Frames"

os.makedirs(output_dir, exist_ok=True)

# Function to save frame with timestamp
def save_frame(frame, output_dir):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    frame_path = os.path.join(output_dir, f"frame_{timestamp}.jpg")
    cv2.imwrite(frame_path, frame)
    print(f"Saved frame at {frame_path}")

# Loop through the video frames
start_time = time.time()
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Save frame every 30 seconds
    if time.time() - start_time >= 30:
        save_frame(frame, output_dir)
        start_time = time.time()

    # Display the frame (optional, you can remove this if you don't need to see the video)
    cv2.imshow('Live Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
cap.release()
cv2.destroyAllWindows()
