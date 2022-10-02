from base64 import b64decode
import cv2
import numpy as np
from pyzbar.pyzbar import decode

# function to convert the JavaScript object into an OpenCV image
def js_to_image(js_reply):
  """
  Params:
          js_reply: JavaScript object containing image from webcam
  Returns:
          img: OpenCV BGR image
  """
  # decode base64 image
  image_bytes = b64decode(js_reply.split(',')[1])
  # convert bytes to numpy array
  jpg_as_np = np.frombuffer(image_bytes, dtype=np.uint8)
  # decode numpy array into OpenCV BGR image
  img = cv2.imdecode(jpg_as_np, flags=1)

  return img



def take_photo(data, show=0):
    # get OpenCV format image
    img = js_to_image(data) 
    
    if show:
        # Get bounding box
        decoder = cv2.QRCodeDetector()
        data, points, _ = decoder.detectAndDecode(img)

        if points is not None:
            points = points[0]
            for i in range(len(points)):
                pt1 = [int(val) for val in points[i]]
                pt2 = [int(val) for val in points[(i + 1) % 4]]
                cv2.line(img, pt1, pt2, color=(255, 0, 0), thickness=3)

            cv2.imshow(img)

    # Get website/info
    data = decode(img)[0].data
    data_str = data.decode("utf-8")
    print('Decoded data: ', data_str)
    
    return data_str



