import torch
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import open3d as o3d
from transformers import DPTImageProcessor, DPTForDepthEstimation
import time

start_time = time.time()
IMAGE_PATH = "../OUTDOOR IMAGES/LOCATION1/FOR MONOCULAR DEPTH ESTIMATION/location1HQ.jpeg"
image = Image.open(IMAGE_PATH)

# DPT feature extractor
processor = DPTImageProcessor.from_pretrained("Intel/dpt-large")
model = DPTForDepthEstimation.from_pretrained("Intel/dpt-large")

# LOADING AND RESAIZING THE IMAGE
image = Image.open(IMAGE_PATH)
new_height = 480 if image.height > 480 else image.height
new_height -= (new_height % 32)
new_width = int(new_height * image.width / image.height)
diff = new_width % 32

new_width = new_width - diff if diff < 16 else new_width + 32 - diff
new_size = (new_width, new_height)
image = image.resize(new_size)

# prepare image for the model
inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    predicted_depth = outputs.predicted_depth

# interpolate to original size
prediction = torch.nn.functional.interpolate(
    predicted_depth.unsqueeze(1),
    size=image.size[::-1],
    mode="bicubic",
    align_corners=False,
)

# visualize the prediction
output = prediction.squeeze().cpu().numpy()
formatted = (output * 255 / np.max(output)).astype("uint8")
depth = Image.fromarray(formatted)


# VISUALIZE THE PREDICTION
# fig, ax = plt.subplots(1,2)
# ax[0].imshow(image)
# ax[0].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
# ax[0].set_title("Original Image")

# ax[1].imshow(output, cmap='plasma')
# ax[1].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
# ax[1].set_title("Processed Output - DPT")
# plt.tight_layout()
# plt.pause(5)

# DEPTH IMAGE FOR OPEN3D
width, height = image.size

depth_image = (output * 255 / np.max(output)).astype('uint8')
image = np.array(image)

# CREATE RGBD IMAGE

depth_o3d = o3d.geometry.Image(depth_image)
image_o3d = o3d.geometry.Image(image)
rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
    image_o3d,
    depth_o3d,
    convert_rgb_to_intensity=False
)


camera_intrinsic = o3d.camera.PinholeCameraIntrinsic()
# https://chatgpt.com/share/6c7a562b-abe1-47fd-8577-da949d0feaa0
# width (int) – Width of the image.
# height (int) – Height of the image.
# fx (float) – X-axis focal length
# fy (float) – Y-axis focal length.
# cx (float) – X-axis principle point.
# cy (float) – Y-axis principle point.
camera_intrinsic.set_intrinsics(width, height,  418.56, 310.04, width/2, height/2)


# POINT CLOUD
pcd_raw = o3d.geometry.PointCloud.create_from_rgbd_image(
    rgbd_image,
    camera_intrinsic
)

# Rotate 180 degrees around the x-axis
rotation_matrix = np.array([[1, 0, 0, 0],
                            [0, -1, 0, 0],
                            [0, 0, -1, 0],
                            [0, 0, 0, 1]])

pcd_corrected = pcd_raw.transform(rotation_matrix)

'''
# Step 2: Extract color data
colors = np.asarray(pcd_raw.colors)  # Extract the colors

# Step 3: Create a mask for points that belong to the sky (blue color)
# Assume that sky points have a high blue component compared to red and green components.
# Adjust the threshold values as needed based on your specific data.

blue_min = np.array([65, 100, 70]) / 255.0  # Lower bound of light blue in RGB
blue_max = np.array([195, 220, 255]) / 255.0  # Upper bound of light blue in RGB

mask = np.all((colors >= blue_min) & (colors <= blue_max), axis=1)

# Step 4: Apply the mask to filter out sky points
filtered_points = np.asarray(pcd_raw.points)[~mask]
filtered_colors = colors[~mask]

# Step 5: Create a new point cloud with the filtered points and colors
filtered_pcd = o3d.geometry.PointCloud()
filtered_pcd.points = o3d.utility.Vector3dVector(filtered_points)
filtered_pcd.colors = o3d.utility.Vector3dVector(filtered_colors)

# 1. outlier removal
cl, ind = filtered_pcd.remove_statistical_outlier(nb_neighbors = 20, std_ratio=6.0)
pcd = filtered_pcd.select_by_index(ind)


# o3d.visualization.draw_geometries([pcd])
# o3d.io.write_point_cloud("../POINT CLOUD/MDE/location1.ply", pcd)
'''

# End timing
end_time = time.time()
print(f"Processing time DPT: {end_time - start_time:.2f} seconds")
