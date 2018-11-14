import numpy as np
import cv2
from PIL import Image
import imutils
from pytesseract import image_to_string


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    tl, tr, br, bl = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def get_photo(card):
    card_height, card_width, channels = card.shape
    photo_h1 = round(0.28 * card_height)
    photo_h2 = round(0.76 * card_height)
    photo_w1 = round(0.0036 * card_width)
    photo_w2 = round(0.233 * card_width)
    photo = card[photo_h1: photo_h2, photo_w1: photo_w2]
    cv2.imwrite('static/image_detect/Card.jpg', card)
    cv2.imwrite('static/image_detect/Photo.jpg', photo)


def get_id(card):
    card_height, card_width, channels = card.shape
    ID_h1 = round(0.9 * card_height)
    ID_h2 = round(0.9799 * card_height)
    ID_w1 = round(0.003 * card_width)
    ID_w2 = round(0.23 * card_width)
    ID = card[ID_h1: ID_h2, ID_w1: ID_w2]
    ID = cv2.cvtColor(ID, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('static/image_detect/ID.jpg', ID)
    return image_to_string(Image.open('static/image_detect/ID.jpg'), lang='vie')


def get_name(card):
    card_height, card_width, channels = card.shape
    name_h1 = round(0.356 * card_height)
    name_h2 = round(0.47 * card_height)
    name_w1 = round(0.238 * card_width)
    name_w2 = round(0.96 * card_width)
    name = card[name_h1: name_h2, name_w1: name_w2]
    name = cv2.cvtColor(name, cv2.COLOR_BGR2GRAY)
    retval2, name = cv2.threshold(name, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite('static/image_detect/Name.jpg', name)
    return image_to_string(Image.open('static/image_detect/Name.jpg'), lang='vie')


def get_birth_day(card):
    card_height, card_width, channels = card.shape
    dob_h1 = round(0.45 * card_height)
    dob_h2 = round(0.545 * card_height)
    dob_w1 = round(0.238 * card_width)
    dob_w2 = round(0.647 * card_width)
    dob = card[dob_h1: dob_h2, dob_w1: dob_w2]
    dob = cv2.cvtColor(dob, cv2.COLOR_BGR2GRAY)
    retval2, dob = cv2.threshold(dob, 125, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite('static/image_detect/Date_of_Birth.jpg', dob)
    return image_to_string(Image.open('static/image_detect/Date_of_Birth.jpg'), lang='vie')


def get_info(card):
    get_photo(card)
    ID = get_id(card)
    Name = get_name(card)[get_name(card).rfind(':') + 2:]
    Date_of_Birth = get_birth_day(card)[get_birth_day(card).rfind(':') + 2:]
    result = [Name, ID, Date_of_Birth]
    return result


def get_card(img, origin):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(gray, 100, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    cnts = cv2.findContours(closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx == 4):
            screenCnt = approx
            break
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 5)
    card = four_point_transform(origin, screenCnt.reshape(4, 2))
    card_height, card_width, channels = card.shape
    cv2.imwrite('static/image_detect/Card.jpg', card)
    cv2.imwrite('static/image_detect/Image_detected.jpg', img)
    card = cv2.imread('static/image_detect/Card.jpg')


def total(link_img):
    img = cv2.imread(link_img)
    h, w, c = img.shape
    while (h > 4000 or w > 4000):
        h = int(h / 2.5)
        w = int(w / 2.5)
        c = 1
    if c == 1:
        img = cv2.resize(img, (w, h))
    origin = img.copy()
    get_card(img, origin)
    card = cv2.imread('static/image_detect/Card.jpg')
    card_height, card_width, channels = card.shape
    return get_info(card)