import cv2
import csv

# Initialize a list to store the points and lines
points = []
rois = []

# Mouse callback function to draw lines
def draw_line(event, x, y, flags, param):
    global drawing, frame, img_copy, points

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) > 1:
            cv2.line(img_copy, points[-2], points[-1], (0, 255, 0), 2)
            cv2.imshow('image', img_copy)
        if len(points) == 4:
            points.append(points[0])  # Close the rectangle
            for i in range(4):
                cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 2)
            rois.append(points[:4])
            save_coordinates()
            points = []  # Reset points
            img_copy = frame.copy()  # Update img_copy with the new rectangle

# Function to save coordinates to CSV
def save_coordinates():
    with open(r'C:\Users\ASUS\PycharmProjects\Spot Finder\data\rois3.csv', 'a', newline='') as outf:
        csv_writer = csv.writer(outf)
        for i, roi in enumerate(rois[-1:]):  # Save only the last rectangle
            csv_writer.writerow([f'Box {len(rois)}', roi[0][0], roi[0][1], roi[1][0], roi[1][1], roi[2][0], roi[2][1], roi[3][0], roi[3][1]])
    print(f"Coordinates for rectangle {len(rois)} saved to 'data/rois3.csv'")

# Load the image
image_path = r'C:\Users\ASUS\PycharmProjects\Spot Finder\image\output_image3.png'
frame = cv2.imread(image_path)
img_copy = frame.copy()

# Create a window and bind the function to window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_line)

# Initialize drawing state
drawing = False

# Write the header to the CSV file
with open(r'C:\Users\ASUS\PycharmProjects\Spot Finder\data\rois3.csv', 'w', newline='') as outf:
    csv_writer = csv.writer(outf)
    csv_writer.writerow(['Parking Slot', 'Point1_X', 'Point1_Y', 'Point2_X', 'Point2_Y', 'Point3_X', 'Point3_Y', 'Point4_X', 'Point4_Y'])

while True:
    cv2.imshow('image', img_copy)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):
        points = []  # Reset points for new rectangle
    elif key == ord('r') and len(points) > 0:
        points.pop()  # Remove the last point
        img_copy = frame.copy()  # Reset the image to the original frame
        for i in range(len(points) - 1):
            cv2.line(img_copy, points[i], points[i + 1], (0, 255, 0), 2)  # Redraw the remaining lines

cv2.destroyAllWindows()
print("Task completed. Coordinates saved to 'data/rois3.csv'.")
