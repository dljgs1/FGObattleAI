import numpy as np
import cv2

def Harris(img):
    # find Harris corners
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)

    res = dst > 0.05 * dst.max()
    # img[dst > 0.05 * dst.max()] = [0, 0, 255]
    # return img
    print(res)
    input()
    return res
def Sift(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(gray, None)
    img = cv2.drawKeypoints(gray, kp, img)
    return img
def corner(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 25, 0.01, 10)
    corners = np.int0(corners)
    ans = []
    x_sum = 0
    y_sum = 0
    ct = 0
    for i in corners:
        x, y = i.ravel()
        x_sum += x
        y_sum += y
        ct += 1
    x_sum /= ct
    y_sum /= ct
    for i in corners:
        x, y = i.ravel()
        print(x, y)
        ans.append(float(x - x_sum) / 50)
        ans.append(float(y - y_sum) / 50)
    print(type(ans))
    return ans
