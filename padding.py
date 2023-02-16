import glob

import nibabel as nib
import numpy as np
from scipy import ndimage
import os

bing = 'naomo'
source = 'label'
modal = 't1c'

def pad_nii(img_path,out_path, padded_shape):
    img = nib.load(img_path)
    data = img.get_fdata()

    current_shape = np.array(data.shape)

    pad_widths = [(max(0, padded_shape[i] - current_shape[i]) // 2, (padded_shape[i] - current_shape[i] + 1) // 2) for i in range(3)]
    pad_widths = tuple(pad_widths)

    padded_data = np.pad(data, pad_width=pad_widths, mode='constant')

    # zoom_factors = tuple(padded_shape[i] / current_shape[i] for i in range(3))
    #
    # # 使用高质量的三次插值进行插值
    # padded_data = ndimage.zoom(padded_data, zoom_factors, order=3)

    padded_image = nib.Nifti1Image(padded_data, img.affine)




    if source == 'label':
        # 构造输出文件名
        output_path = os.path.join(out_path, bing, source, img_path.split('\\')[-3])


    else:
        # 构造输出文件名
        output_path = os.path.join(out_path, bing, source, img_path.split('\\')[-2])

    if not os.path.exists(output_path):  # 如果不存在路径，则创建这个路径，关键函数就在这两行，其他可以改变
        os.makedirs(output_path)

    output_path = os.path.join(output_path, img_path.split('\\')[-1])

    # 保存填充后的 Nii 文件
    nib.save(padded_image, output_path)


if __name__ == '__main__':


    img_path = rf'E:\weihai_braintumor\weihai\{bing}\{source}'
    out_path = r'E:\python\monai\data_padding'
    shape = [640,640,24]

    for patient in os.listdir(img_path):

        patient_path = os.listdir(os.path.join(img_path, patient))
        for f in patient_path:
            if source == 'niidata':
                if f.split("_")[1].startswith(modal):
                    path = os.path.join(img_path,patient,f)
                    pad_nii(path,out_path,shape)
            else:
                if f.startswith(modal):
                    path = os.path.join(img_path,patient,f)

                    for e in os.listdir(os.path.join(img_path,patient,f,path)):
                        end_path = os.path.join(img_path,patient,f,path,e)
                        pad_nii(end_path,out_path,shape)

