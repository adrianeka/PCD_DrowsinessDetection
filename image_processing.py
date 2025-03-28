import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import math
from collections import Counter
from pylab import savefig
import cv2
import json
import torch
import logging

def grayscale():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]
    new_arr = r.astype(int) + g.astype(int) + b.astype(int)
    new_arr = (new_arr/3).astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w, h = im.size
    for i in range(w):
        for j in range(h):
            r, g, b = im.getpixel((i, j))
            if r != g != b:
                return False
    return True


def zoomin():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    img_arr = np.asarray(img)
    new_size = ((img_arr.shape[0] * 2),
                (img_arr.shape[1] * 2), img_arr.shape[2])
    new_arr = np.full(new_size, 255)
    new_arr.setflags(write=1)

    r = img_arr[:, :, 0]
    g = img_arr[:, :, 1]
    b = img_arr[:, :, 2]

    new_r = []
    new_g = []
    new_b = []

    for row in range(len(r)):
        temp_r = []
        temp_g = []
        temp_b = []
        for i in r[row]:
            temp_r.extend([i, i])
        for j in g[row]:
            temp_g.extend([j, j])
        for k in b[row]:
            temp_b.extend([k, k])
        for _ in (0, 1):
            new_r.append(temp_r)
            new_g.append(temp_g)
            new_b.append(temp_b)

    for i in range(len(new_arr)):
        for j in range(len(new_arr[i])):
            new_arr[i, j, 0] = new_r[i][j]
            new_arr[i, j, 1] = new_g[i][j]
            new_arr[i, j, 2] = new_b[i][j]

    new_arr = new_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def zoomout():
    img = Image.open("static/img/img_now.jpg")
    img = img.convert("RGB")
    x, y = img.size
    new_arr = Image.new("RGB", (int(x / 2), int(y / 2)))
    r = [0, 0, 0, 0]
    g = [0, 0, 0, 0]
    b = [0, 0, 0, 0]

    for i in range(0, int(x/2)):
        for j in range(0, int(y/2)):
            r[0], g[0], b[0] = img.getpixel((2 * i, 2 * j))
            r[1], g[1], b[1] = img.getpixel((2 * i + 1, 2 * j))
            r[2], g[2], b[2] = img.getpixel((2 * i, 2 * j + 1))
            r[3], g[3], b[3] = img.getpixel((2 * i + 1, 2 * j + 1))
            new_arr.putpixel((int(i), int(j)), (int((r[0] + r[1] + r[2] + r[3]) / 4), int(
                (g[0] + g[1] + g[2] + g[3]) / 4), int((b[0] + b[1] + b[2] + b[3]) / 4)))
    new_arr = np.uint8(new_arr)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_left():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (0, 50)), 'constant')[:, 50:]
    g = np.pad(g, ((0, 0), (0, 50)), 'constant')[:, 50:]
    b = np.pad(b, ((0, 0), (0, 50)), 'constant')[:, 50:]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_right():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 0), (50, 0)), 'constant')[:, :-50]
    g = np.pad(g, ((0, 0), (50, 0)), 'constant')[:, :-50]
    b = np.pad(b, ((0, 0), (50, 0)), 'constant')[:, :-50]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_up():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((0, 50), (0, 0)), 'constant')[50:, :]
    g = np.pad(g, ((0, 50), (0, 0)), 'constant')[50:, :]
    b = np.pad(b, ((0, 50), (0, 0)), 'constant')[50:, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def move_down():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    r, g, b = img_arr[:, :, 0], img_arr[:, :, 1], img_arr[:, :, 2]
    r = np.pad(r, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    g = np.pad(g, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    b = np.pad(b, ((50, 0), (0, 0)), 'constant')[0:-50, :]
    new_arr = np.dstack((r, g, b))
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_addition():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('uint16')
    img_arr = img_arr+100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_substraction():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img).astype('int16')
    img_arr = img_arr-100
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_multiplication():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr*1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def brightness_division():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img)
    img_arr = img_arr/1.25
    img_arr = np.clip(img_arr, 0, 255)
    new_arr = img_arr.astype('uint8')
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def convolution(img, kernel):
    h_img, w_img, _ = img.shape
    out = np.zeros((h_img-2, w_img-2), dtype=float)
    new_img = np.zeros((h_img-2, w_img-2, 3))
    if np.array_equal((img[:, :, 1], img[:, :, 0]), img[:, :, 2]) == True:
        array = img[:, :, 0]
        for h in range(h_img-2):
            for w in range(w_img-2):
                S = np.multiply(array[h:h+3, w:w+3], kernel)
                out[h, w] = np.sum(S)
        out_ = np.clip(out, 0, 255)
        for channel in range(3):
            new_img[:, :, channel] = out_
    else:
        for channel in range(3):
            array = img[:, :, channel]
            for h in range(h_img-2):
                for w in range(w_img-2):
                    S = np.multiply(array[h:h+3, w:w+3], kernel)
                    out[h, w] = np.sum(S)
            out_ = np.clip(out, 0, 255)
            new_img[:, :, channel] = out_
    new_img = np.uint8(new_img)
    return new_img


def edge_detection():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float)
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def blur():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def sharpening():
    img = Image.open("static/img/img_now.jpg")
    img_arr = np.asarray(img, dtype=int)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    new_arr = convolution(img_arr, kernel)
    new_img = Image.fromarray(new_arr)
    new_img.save("static/img/img_now.jpg")


def histogram_rgb():
    img_path = "static/img/img_now.jpg"
    img = Image.open(img_path)
    img_arr = np.asarray(img)
    if is_grey_scale(img_path):
        g = img_arr[:, :, 0].flatten()
        data_g = Counter(g)
        plt.bar(list(data_g.keys()), data_g.values(), color='black')
        plt.savefig(f'static/img/grey_histogram.jpg', dpi=300)
        plt.clf()
    else:
        r = img_arr[:, :, 0].flatten()
        g = img_arr[:, :, 1].flatten()
        b = img_arr[:, :, 2].flatten()
        data_r = Counter(r)
        data_g = Counter(g)
        data_b = Counter(b)
        data_rgb = [data_r, data_g, data_b]
        warna = ['red', 'green', 'blue']
        data_hist = list(zip(warna, data_rgb))
        for data in data_hist:
            plt.bar(list(data[1].keys()), data[1].values(), color=f'{data[0]}')
            plt.savefig(f'static/img/{data[0]}_histogram.jpg', dpi=300)
            plt.clf()


def df(img):  # to make a histogram (count distribution frequency)
    values = [0]*256
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            values[img[i, j]] += 1
    return values


def cdf(hist):  # cumulative distribution frequency
    cdf = [0] * len(hist)  # len(hist) is 256
    cdf[0] = hist[0]
    for i in range(1, len(hist)):
        cdf[i] = cdf[i-1]+hist[i]
    # Now we normalize the histogram
    # What your function h was doing before
    cdf = [ele*255/cdf[-1] for ele in cdf]
    return cdf


def histogram_equalizer():
    img = cv2.imread('static\img\img_now.jpg', 0)
    my_cdf = cdf(df(img))
    # use linear interpolation of cdf to find new pixel values. Scipy alternative exists
    image_equalized = np.interp(img, range(0, 256), my_cdf)
    cv2.imwrite('static/img/img_now.jpg', image_equalized)


def threshold(lower_thres, upper_thres):
    img = cv2.imread("static/img/img_now.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, lower_thres, upper_thres, cv2.THRESH_BINARY)
    cv2.imwrite("static/img/img_now.jpg", thresholded)


def threshold(lower_thres, upper_thres):
    img_path = "static/img/img_now.jpg"
    if not is_grey_scale(img_path):
        grayscale()  # Mengubah citra menjadi grayscale terlebih dahulu
        
    img = cv2.imread(img_path, 0)
    _, thresholded = cv2.threshold(img, lower_thres, upper_thres, cv2.THRESH_BINARY)
    cv2.imwrite(img_path, thresholded)


def is_binary(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    unique_values = np.unique(img)
    return len(unique_values) == 2 and 0 in unique_values and 255 in unique_values


def binary():
    img_path = "static/img/img_now.jpg"

    if not is_grey_scale(img_path):
        grayscale()  # Mengubah citra menjadi grayscale terlebih dahulu

    img = cv2.imread("static/img/img_now.jpg", 0)
    _, binary_img = cv2.threshold(img, 128, 255, cv2.THRESH_OTSU)
    cv2.imwrite("static/img/img_now.jpg", binary_img)


def dilation():
    binary()
    img = cv2.imread("static/img/img_now.jpg", 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite("static/img/img_now.jpg", dilated)


def erosion():
    binary()
    img = cv2.imread("static/img/img_now.jpg", 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    eroded = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("static/img/img_now.jpg", eroded)


def opening():
    binary()
    img = cv2.imread("static/img/img_now.jpg", 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    cv2.imwrite("static/img/img_now.jpg", opened)


def closing():
    binary()
    img = cv2.imread("static/img/img_now.jpg", 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite("static/img/img_now.jpg", closed)


def counting_object():
    crack =  cv2.imread("static/img/img_now.jpg")

    binary()
    crack_binary = cv2.imread("static/img/img_now.jpg", 0)

    full_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    crack_final = cv2.morphologyEx(crack_binary, cv2.MORPH_OPEN, full_kernel)
    crack_final = cv2.erode(crack_final, full_kernel, iterations=3)
    crack_final = cv2.dilate(crack_final, full_kernel, iterations=1)

    contours, _ = cv2.findContours(crack_final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    crack_with_contours = crack.copy()
    cv2.drawContours(crack_with_contours, contours, -1, (0, 255, 0), 2)
    cv2.imwrite("static/img/img_now.jpg", crack_with_contours)

    num_blobs = len(contours)
    
    return num_blobs

def freeman_chain_code2(contour):
    chain_code = []
    prev_point = contour[0][0]
    
    for point in contour[1:]:
        x, y = point[0]
        dx = x - prev_point[0]
        dy = y - prev_point[1]
        
        # Calculate the angle in degrees
        angle = np.degrees(np.arctan2(dy, dx))
        
        # Convert the angle to Freeman Chain Code (numerical values)
        code = round((angle % 360) / 45) % 8
        chain_code.append(code)
        
        prev_point = point[0]
    
    return chain_code

def read_binary(input_image_path):
    # Load the image
    image = cv2.imread(input_image_path)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    if image is None:
        print("Error: Unable to read the image.")
        return

    # Apply Otsu's thresholding
    _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


    return binary_image

def get_contour(binary_image):
    
    contours, _ = cv2.findContours(
        binary_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return contours

def FCC(binary_image):
    contours = get_contour(binary_image)
    for contour in contours:
        result = freeman_chain_code2(contour)
        print(f'result {result}')
        return result
        
def invert_binary_image(binary_image):
    # Invert the binary image using the NOT operation
    inverted_image = cv2.bitwise_not(binary_image)
    return inverted_image

def thinning_image(image):
    # Apply thinning operation (Zhang-Suen algorithm)
    thinning_image = cv2.ximgproc.thinning(image, thinningType=cv2.ximgproc.THINNING_ZHANGSUEN)
    return thinning_image

def calculate_similarity(chain_code1, chain_code2):
    # Calculate the similarity between two FCCs
    length1 = len(chain_code1)
    length2 = len(chain_code2)

    # Pad the shorter chain code with zeros to match the length of the longer chain code
    if length1 < length2:
        chain_code1 = chain_code1 + [0] * (length2 - length1)
    elif length1 > length2:
        chain_code2 = chain_code2 + [0] * (length1 - length2)

    return np.sum(np.array(chain_code1) == np.array(chain_code2))

def recognize_digit(input_chain_code, knowledge_base):
    best_match = None
    best_similarity = 0

    for digit, data in knowledge_base.items():
        for stored_chain_code in data["FCC_8_Directions"]:
            for input_code in input_chain_code:
                similarity = calculate_similarity(input_code, stored_chain_code)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = digit

    return best_match

def number_recognition():
    img_path = "static/img/img_now.jpg"

    with open("knowledge_base.json", "r") as file:
        knowledge_base = json.load(file)

    # Read and process the image
    binary_image = invert_binary_image(read_binary(img_path))
    contours = get_contour(binary_image)

    recognized_digits = []

    # Create a dictionary to map the position of contours to their FCC
    contour_position_mapping = {}
    for contour in contours:
        # Calculate FCC in 8 directions for each contour
        fcc_8_directions = freeman_chain_code2(contour)

        # Determine the position (e.g., x-coordinate) of the contour
        position = contour[0][0][0]  # Assuming x-coordinate is at index 0
            
        contour_position_mapping[position] = fcc_8_directions

        # Sort the contours based on their positions
    sorted_contours = sorted(contour_position_mapping.items())

    for _, fcc_8_directions in sorted_contours:
        recognized_digit = recognize_digit([fcc_8_directions], knowledge_base)

        if recognized_digit is not None:
            recognized_digits.append(recognized_digit)

    if recognized_digits:
        recognized_result = ''.join(map(str, recognized_digits))
        return recognized_result
    else:
        return "Digit recognition failed for {img_path}. No matching digits found in the knowledge base."
    
def face_recognition(frame):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/last.pt', force_reload=True)
    results = model(frame)
    frame = np.squeeze(results.render())
    return frame

def generate_frames():    
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/last.pt', force_reload=True)
    logging.basicConfig(level=logging.INFO)
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        logging.error("Cannot open camera")
        return

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        logging.error("Failed to load cascade classifier")
        return

    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame)
            # Render results on the frame
            frame = np.squeeze(results.render())

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

