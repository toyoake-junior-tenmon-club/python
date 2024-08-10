#ライブラリのインポート
import cv2
import argparse
import numpy as np

def main(args):
    img_in_file = args.input
    img_out_file = args.output
    alpha = args.alpha
    beta = args.beta
    #γ変換のγ値
    gamma = args.gamma
    #画像を読み込む
    img = cv2.imread(img_in_file)

    # 明るさ・コントラスト操作
    img = cv2.convertScaleAbs(img,alpha = alpha,beta = beta)

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)


    
    gamma_cvt = np.array([[255 * (float(i) / 255) ** (1.0 / gamma)] for i in range(256)])

    #γ変換を行う
    img_yuv[:,:,0] = cv2.LUT(img_yuv[:,:,0], gamma_cvt)
    img_gamma = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    cv2.imwrite(img_out_file, img_gamma)

    #変換後の画像を表示する。
    cv2.imshow("gamma", img_gamma)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Image Converter')
    parser.add_argument('input', help='input file')
    parser.add_argument('output', help='output file')

    parser.add_argument('--alpha', type=float, default=1.0)
    parser.add_argument('--beta', type=float, default=0)
    parser.add_argument('--gamma', type=float, default=1.0)

    args = parser.parse_args()
    main(args)
