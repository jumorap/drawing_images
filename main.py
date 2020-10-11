import numpy as np
import time
import imageio
import scipy.ndimage
import cv2
from PIL import Image


def dodge(front, back):
    # We force the blur to return us the value 255 if is > than 255
    final_sketch = front * 255 / (255 - back)
    final_sketch[final_sketch > 255] = 255
    final_sketch[back == 255] = 255

    return final_sketch.astype('uint8')


def image_selector():
    # Using exceptions (can be better optimized), we select the file called
    # 'photo' in png format. Additional to it, we require to our users that
    # introduce a sigma value [my_sigma], this value is the intensity of blurness
    try:
        img = 'assets\\proof.png'
        save_img = Image.open(img)
    except:
        img = 'assets\\proof.jpg'
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
    # Read the image and is processed like a image in gray scale
    # After it we load the sigma value in [my_sigma_format], that
    # is a value that ingress or user
    rgb = imageio.imread(image)
    rgb_gray = np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])
    img_residual = 255 - rgb_gray

    blur = scipy.ndimage.filters.gaussian_filter(img_residual, sigma=my_sigma_format)

    return [dodge(blur, rgb_gray), my_sigma_format]


if __name__ == "__main__":
    '''While better quality (inclusive size) have the image, is possible build image with more details'''
    # After call [image_selector()], that return a vector of 2 components
    # we use 2 indicators to give name to image result, the first is actual
    # date using 'time' library, and sigma value [image_result[1]]
    image_result = image_selector()
    timer = str(time.strftime("%d%m%y%H%M%S")) + str(image_result[1])
    my_time = int(timer)
    str_result = 'results/result%d.png' % my_time
    file = r'results/result%d.png' % my_time

    # Image result is saved and after showed to our users in another window
    cv2.imwrite(str_result, image_result[0])
    reader = cv2.imread(file)
    cv2.imshow('Result', reader)
    cv2.waitKey()
