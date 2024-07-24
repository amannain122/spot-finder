import os
import aws
import data_loader as dlu

spot_finder_dir = dlu.find_spot_finder_dir()
file_to_upload = "parking_fares_calculated.csv"
upload_file = os.path.join(spot_finder_dir, 'experimental', 'pipeline', 'data', file_to_upload)
aws.upload_to_s3(upload_file)