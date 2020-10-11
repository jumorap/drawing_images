import numpy as np
import time
import imageio
import scipy.ndimage
import cv2
from PIL import Image


def dodge(front, back):
    final_sketch = front * 255 / (255 - back)
    final_sketch[final_sketch > 255] = 255
    final_sketch[back == 255] = 255

    return final_sketch.astype('uint8')


def image_selector():
    try:
        img = 'assets\\photo.png'
        save_img = Image.open(img)
    except:
        img = 'assets\\photo.jpg'
        save_img = Image.open(img)
        save_img.save('assets\\photo.png')
    finally:
        while True:
            try:
                my_sigma = int(input("Please add the sigma number to reformat the image: "))
                break
            except:
                print("Please add an integer number.\n")

    return variables_process('assets/photo.png', my_sigma)


def variables_process(image, my_sigma_format):
    rgb = imageio.imread(image)
    rgb_gray = np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])
    img_residual = 255 - rgb_gray

    blur = scipy.ndimage.filters.gaussian_filter(img_residual, sigma=my_sigma_format)

    return [dodge(blur, rgb_gray), my_sigma_format]


if __name__ == "__main__":
    image_result = image_selector()
    timer = str(time.strftime("%d%m%y%H%M%S")) + str(image_result[1])
    str_result = 'results/result%d.png' % int(timer)

    cv2.imwrite(str_result, image_result[0])
