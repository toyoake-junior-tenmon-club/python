import sys
import numpy as np #数値計算用
import matplotlib.pyplot as plt #描画用
from astroquery.skyview import SkyView #天文写真取得用
from astropy import units as u #取得範囲設定用
from astropy.wcs import WCS #天球座標変換用
from astropy.visualization import ZScaleInterval,ImageNormalize

survey_2mass = ['2MASS-K','2MASS-H','2MASS-J'] #近赤外線波長域での天文観測プロジェクト
survey_dss = ['DSS2R', 'DSS', 'DSS1B']

get_survey = lambda key: survey_2mass if key == '2MASS' else survey_dss


def plotimage(survey_key, target_key):
    survey = get_survey(survey_key)
    radius = 30*u.arcmin #取得する写真の範囲
    pixels = 600 #取得する写真の大きさ
    figsize = [6,6] #画像表示エリアのサイズ

    hdu = SkyView.get_images(target_key,survey=survey,radius=radius,pixels=pixels) #天文写真を取得
    wcs = WCS(hdu[0][0].header) #WCS座標を取得
    plt.figure(figsize=figsize).add_subplot(projection=wcs,title=target_key) #取得した座標をプロットする
    np_frame = np.stack([ImageNormalize(hdu[i][0].data,interval=ZScaleInterval())(hdu[i][0].data) for i in range(3)], axis=2)
    plt.imshow(np_frame,origin='lower') #強調化・合成して画像を表示
    plt.savefig(target_key + '.jpg') #画像保存
    plt.close() #クローズ


if __name__ == '__main__':
    plotimage(sys.argv[1], sys.argv[2])
    