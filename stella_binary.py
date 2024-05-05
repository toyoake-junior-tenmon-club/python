
import numpy as np
import sys
import cv2

levels = [150, 170]

def main(img_in, img_out):
    im = cv2.imread(img_in, cv2.IMREAD_GRAYSCALE)

    # マスクパターン作成
    (height, width) = im.shape
    mask = np.zeros((height, width,3), np.uint8)
    mask_0 = cv2.rectangle(mask, (1,1), (width,int(2*height/3)-110), (255,255,255), -1)
    mask_0 = cv2.cvtColor(mask_0, cv2.COLOR_BGR2GRAY)

    mask_1 = cv2.rectangle(mask, (1,int(2*height/3)-115), (width,height), (255,255,255), -1)
    mask_1 = cv2.cvtColor(mask_1, cv2.COLOR_BGR2GRAY)

    im_mask0 = cv2.bitwise_and(im, mask_0)
    _, im_filter0 = cv2.threshold(im_mask0, levels[0], 255, cv2.THRESH_BINARY)

    im_mask1 = cv2.bitwise_and(im, mask_1)
    _, im_filter1 = cv2.threshold(im_mask1, levels[1], 255, cv2.THRESH_BINARY)

    im_out = im_filter0
    im_out[mask_0 == 0] = im_filter1[mask_0 == 0]

    cv2.imwrite(img_out, im_filter0)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])