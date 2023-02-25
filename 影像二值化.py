from osgeo import gdal
from tqdm import tqdm
import numpy as np
import os

def binarize_tif(tif_path, threshold, output):
    # 打开tif影像
    tif = gdal.Open(tif_path)
    # 读取影像数据
    tif_array = tif.GetRasterBand(1).ReadAsArray()
    # 获取影像数据的行列数
    rows, cols = tif_array.shape
    # 创建一个和影像数据大小相同的全0数组
    bin_array = np.zeros_like(tif_array)
    # 将大于阈值的像素值设为1
    bin_array[tif_array > threshold] = 1
    # 将二值化后的数组写入新的tif文件中
    driver = gdal.GetDriverByName('GTiff')
    out_tif = driver.Create(output, cols, rows, 1, gdal.GDT_Byte)
    out_tif.GetRasterBand(1).WriteArray(bin_array)
    out_tif.FlushCache()
    out_tif = None

if __name__ == '__main__':
    # # 单幅转换
    # input_image = 'E:/WeiFangimage/weifang_8552.JPG'   # 原始影像
    # output_image = 'E:/weifang_8552_123.JPG'   # 二值化后的影像
    # threshold = 0    # 阈值
    # binarize_tif(input_image, threshold, output_image)

    # 多幅转换
    input_file = 'E:/WeiFangimage' # 输入影像文件夹
    output_file = 'E:/test/123'    # 输出影像文件夹
    threshold = 0    # 阈值
    if not os.path.exists(output_file):
        os.makedirs(output_file)
    for filename in tqdm(os.listdir(input_file)):
        if filename.endswith(".JPG"):
            input_image = os.path.join(input_file, filename)
            output_image = os.path.join(output_file, filename)
            binarize_tif(input_image, threshold, output_image)
    
    print('Transfer Success')