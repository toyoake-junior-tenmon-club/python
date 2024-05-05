
import numpy as np
import sys
import cv2

#
# 多段ノイズ除去 
#
def main(img_in, img_out):
    # 画像をグレースケールで読み取り
    im_gray = cv2.imread(img_in, cv2.IMREAD_GRAYSCALE)

    # マスクパターン作成
    (height, width) = im_gray.shape

    # 輝度レベル
    levels = [100, 155, 170]
    p_starts = [(1,1), (1,int(height/3)-51), (1, int(2*height/3))]
    p_ends = [(width,int(height/3)-50), (width, int(2*height/3)-1), (width,height)]

    im_out = cv2.cvtColor(np.zeros((height, width,3), np.uint8), cv2.COLOR_BGR2GRAY)
    for n in range(0,len(levels)):
        mask = np.zeros((height, width,3), np.uint8)
        im_mask = cv2.rectangle(mask, p_starts[n], p_ends[n], (255,255,255), -1)
        im_mask = cv2.cvtColor(im_mask, cv2.COLOR_BGR2GRAY)
        im_area = cv2.bitwise_and(im_gray, im_mask)
        
        _, im_filter = cv2.threshold(im_area, levels[n], 255, cv2.THRESH_BINARY)
        cv2.imwrite('debug' + str(n) + '.jpg', im_filter)

        # 画像合成
        im_out = cv2.bitwise_or(im_out, im_filter)

    cv2.imwrite(img_out, im_out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])