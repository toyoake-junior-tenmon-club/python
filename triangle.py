import sys
import cv2
import numpy as np

import math



if __name__ == '__main__':
    # 8ビット1チャンネルのグレースケールとして画像を読み込む
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

    level = 250
    if len(sys.argv) > 2:
        level = int(sys.argv[2])

    min = 30.0
    if len(sys.argv) > 3:
        min = float(sys.argv[3])
    max = 90.0
    if len(sys.argv) > 4:
        max = float(sys.argv[4])

    _, img_bin = cv2.threshold(img, level, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # 画像表示用に入力画像をカラーデータに変換する
    img_disp = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # 全ての輪郭を描画
    # cv2.drawContours(img_disp, contours, -1, (0, 0, 255), 2)

    p_lst = []
    p_pre = [0., 0.]

    # 輪郭の点の描画
    for contour in contours:
        for point in contour:
            # 輪郭
            p_cur = point[0]
            if len(p_lst) == 0:
                print('(', p_cur[1], ',', p_cur[0], ')')
                p_lst.append(p_cur)
            else:
                p_diff = p_cur - p_pre
                if abs(p_diff[0]) + abs(p_diff[1]) > 100:
                    p_lst.append(p_cur)
                    print('(', p_cur[1], ',', p_cur[0], ')')
            p_pre = p_cur

    # 角度計算
    for o in p_lst:
        for p in p_lst:
            op = p - o
            op_abs = np.linalg.norm(op)
            if op_abs > 1:
                for q in p_lst:
                    oq = q - o
                    arg = 180.0

                    oq_abs = np.linalg.norm(oq)
                    if oq_abs > 1:
                        cos_arg = np.dot(op, oq) / (op_abs * oq_abs)
                        if -1 < cos_arg < 1:
                            arg = math.acos(cos_arg) * 180.0 / math.pi

                    if 20.0 < arg < 90.0:
                        print('o = (', o[1], ',', o[0], ')')
                        print('p = (', p[1], ',', p[0], ')')
                        print('q = (', q[1], ',', q[0], ')')
                        print('angle = ', arg, ' deg')
                        cv2.circle(img_disp, o, 10, (0, 255, 0), -1)




    cv2.imwrite('ret.png', img_disp)

