import cv2
import numpy as np


def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
  # Grab image isze and intitialize dimensions
  dim = None
  (h, w) = image.shape[:2]
  # Return original image if no need to resize
  if width is None and height is None:
    return image
  # We are resizing height if width is None
  if width is None:
    r = height / float(h)
    dim = (int(w * r), height)
  # We are resizing width if height is None
  else:
    r = width / float(w)
    dim = (width, int(h * r))

  return cv2.resize(image, dim, interpolation=inter)

  # Laad template, convert to grayscale, perform canny edge detection
  template = cv2.imread('template.pn')  # Add another image here
  template = cv2.cv2Color(template, cv2.COLOR_BGR2GRAY)
  template = cv2.canny(template, 50, 200)
  (tH, tW) = template.shape[:2]
  cv2.imshow("template", template)

  # Load original image, convert to grayscale
  original_image = cv2.imread('test.png')
  final = original_image.copy()
  gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
  found = None

  # Dynamically rescale image for better template matching
  for scale in np.linspace(0.2, 1.0, 20)[::-1]:
    resized = maintain_aspect_ratio_resize(gray, width=int(gray.shape[1] * scale))
    r = gray.shape[1] / float(resized.shape[1])

    if resized.shape[0] < tH or resized.shape[1] < tW:
      break

    canny = cv2.Canny(resized, 50, 200)
    detected = cv2.matchTemplate(canny, template, cv2.TM_CCOEFF)
    (_, max_val, _, max_loc) = cv2.minMaxLoc(detected)
    if found is None or max_val > found[0]:
      found = (max_val, max_loc, r)
    (_, max_loc, r) = found
    (start_x, start_y) = (int(max_loc[0] * r), int(max_loc[1] * r))
    (end_x, end_y) = (int((max_loc[0] + tW) * r), int((max_loc[1] + tH) * r))

    # Draw bounding box on ROI to remove
    cv2.rectangle(original_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    imshow('detected', original_image)

    # Erase unwanted ROI (Fill ROI with white)
    cv2.rectangle(final, (start_x, start_y), (end_x, end_y), (255, 255, 255), -1)
    cv2.imwrite('final.png', final)
    cv2.waitKey(0)


def print_hi(name):
  print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
  print_hi('PyCharm')
  image = '/home/shetu/Desktop/org.png'
  maintain_aspect_ratio_resize(image)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
