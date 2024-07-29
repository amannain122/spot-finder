import os

# Function to find the "spot-finder" directory
def find_spot_finder_dir():
    current_dir = os.getcwd()
    while True:
        if 'spot-finder' in os.listdir(current_dir):
            return os.path.join(current_dir, 'spot-finder')
        new_dir = os.path.dirname(current_dir)
        if new_dir == current_dir:
            raise FileNotFoundError("spot-finder directory not found")
        current_dir = new_dir
