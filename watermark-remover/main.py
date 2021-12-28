# import cv2
import glob
import os
import time
from datetime import datetime

import numpy as np
from PIL import Image


# def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
#     # Grab image isze and intitialize dimensions
#     dim = None
#     (h, w) = image.shape[:2]
#     # Return original image if no need to resize
#     if width is None and height is None:
#         return image
#     # We are resizing height if width is None
#     if width is None:
#         r = height / float(h)
#         dim = (int(w * r), height)
#     # We are resizing width if height is None
#     else:
#         r = width / float(w)
#         dim = (width, int(h * r))
#
#     return cv2.resize(image, dim, interpolation=inter)
#
#     # Laad template, convert to grayscale, perform canny edge detection
#     template = cv2.imread('template.pn')  # Add another image here
#     template = cv2.cv2Color(template, cv2.COLOR_BGR2GRAY)
#     template = cv2.canny(template, 50, 200)
#     (tH, tW) = template.shape[:2]
#     cv2.imshow("template", template)
#
#     # Load original image, convert to grayscale
#     original_image = cv2.imread('test.png')
#     final = original_image.copy()
#     gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
#     found = None
#
#     # Dynamically rescale image for better template matching
#     for scale in np.linspace(0.2, 1.0, 20)[::-1]:
#         resized = maintain_aspect_ratio_resize(gray, width=int(gray.shape[1] * scale))
#         r = gray.shape[1] / float(resized.shape[1])
#
#         if resized.shape[0] < tH or resized.shape[1] < tW:
#             break
#
#         canny = cv2.Canny(resized, 50, 200)
#         detected = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF)
#         (_, max_val, _, max_loc) = cv2.minMaxLoc(detected)
#         if found is None or max_val > found[0]:
#             found = (max_val, max_loc, r)
#         (_, max_loc, r) = found
#         (start_x, start_y) = (int(max_loc[0] * r), int(max_loc[1] * r))
#         (end_x, end_y) = (int((max_loc[0] + tW) * r), int((max_loc[1] + tH) * r))
#
#         # Draw bounding box on ROI to remove
#         cv2.rectangle(original_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
#         imshow('detected', original_image)
#
#         # Erase unwanted ROI (Fill ROI with white)
#         cv2.rectangle(final, (start_x, start_y), (end_x, end_y), (255, 255, 255), -1)
#         cv2.imwrite('final.png', final)
#         cv2.waitKey(0)


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def collect_folders(target_dir):
    folders = [f.path for f in os.scandir(target_dir) if f.is_dir()]
    return folders


def collect_images(image_dir):
    images = []
    for image in glob.glob(image_dir + "/*.jpeg"):
        images.append(image)
    return images


def remove_watermark(src_dir, replacing_img, save_dir):
    count = 0
    print("Start Time =", datetime.now())
    sub_folders = collect_folders(src_dir)
    for sub_folder in sub_folders:
        images = collect_images(sub_folder)
        for image in images:
            image_name = image.split("/")
            new_path = save_dir + "/" + image_name[-2]
            if os.path.exists(new_path) is False:
                os.mkdir(new_path)
            image_save_dir = new_path + "/" + image_name[-1]
            image_replace(image, replacing_img, image_save_dir)
            count = count + 1
            print("Total saved:{}, currently saved:{}".format(count, image_save_dir))
    print("End Time =", datetime.now())


def image_replace(target, replace, relative_location):
    try:
        # Relative Path
        # Image on which we want to paste
        img = Image.open(target)
        img_size = img.size
        img_y_axis = img_size[1]

        # Relative Path
        # Image which we want to paste
        img2 = Image.open(replace)
        img.paste(img2, (0, img_y_axis - 107))

        # Saved in the same relative location
        img.save(relative_location)
    except IOError:
        pass


if __name__ == '__main__':
    # print_hi('PyCharm')
    # image = '/home/shetu/Desktop/org.png'
    # maintain_aspect_ratio_resize(image)
    # main_dir = '/home/shetu/Documents'
    # target = main_dir + '/target.jpeg'
    replace_img = '/home/shetu/Documents/white_bg.png'
    saving_dir = '/media/shetu/Entertainment/islamic-book-water-mark-removed-images'
    # new_image = saving_dir + '/new_image.jpeg'
    # image_replace(target, replace, new_image)
    target_dir = '/home/shetu/islamic-book-images'
    # images_dir = '/home/shetu/islamic-book-images/7155'
    # collect_folders(islami_book_dir)
    # image_list = collect_images(images_dir)
    remove_watermark(target_dir, replace_img, saving_dir)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
