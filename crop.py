from scipy.ndimage import binary_fill_holes
import numpy as np
import SimpleITK as sitk
import os

'''
第一步根据四维图像数据data(C,X,Y,Z)生成三维的非零模板nonzero_mask，标示图像中哪些区域是非零的 。不同的模态都有对应的三维数据，产生不同的三维nonzero_mask，
而整个四维图像的非零模板为各个模态非零模板的并集。最后调用scipy库的binary_fill_holes函数对生成的nonzero_mask进行填充。
'''
data_dir= r'E:\python\monai\data_padding\naomo\niidata'

out_path = r'E:\python\monai\crop_end\naomo\niidata'


class_names = sorted(x for x in os.listdir(data_dir)
                     if os.path.isdir(os.path.join(data_dir, x)))
num_class = len(class_names)

img_path = [[os.path.join(data_dir,class_label,x)
             for x in os.listdir(os.path.join(data_dir,class_label))]
            for class_label in os.listdir(data_dir)]


# 得到每类当中数据的数量
num_each = [len(img_path[i]) for i in range(num_class)]
# 两个列表分别来 存放所有图片路径和对应标签
image_files_list = []
image_class = []
for i in range(num_class):
    image_files_list.extend(img_path[i])
    image_class.extend([i] * num_each[i])
num_total = len(image_class)


'''
查看三个维度上面 最大的图像尺寸
max_z = -1
max_y = -1
max_x = -1
for image_3d in range(num_total):
    itk_img = sitk.ReadImage(image_files_list[image_3d])
    data = sitk.GetArrayFromImage(itk_img)
    origin = itk_img.GetOrigin()
    direction = itk_img.GetDirection()
    space = itk_img.GetSpacing()
    z,y,x = data.shape

    if z>max_z:
        max_z = z
    if y>max_y:
        max_y = y
    if x>max_x:
        max_x = x
print(max_z,max_y,max_x)
print(max_z,max_y,max_x)
'''

nonzero_mask = np.zeros((24,512,512), dtype=bool)
# for c in range(data.shape[0]):
#     this_mask = data[c] != 0
#     nonzero_mask = nonzero_mask | this_mask
# nonzero_mask = binary_fill_holes(nonzero_mask)


# 此时为单模态，仅三个维度，若4维，需要对每个模态处理
# 数据shape为（Z,Y,X）
# itk_img = sitk.ReadImage(image_files_list[0])
# data = sitk.GetArrayFromImage(itk_img)
# origin = itk_img.GetOrigin()
# direction = itk_img.GetDirection()
# space = itk_img.GetSpacing()
# nonzero_mask = np.zeros(data.shape[:], dtype=bool)
for image_3d in range(num_total):
    itk_img = sitk.ReadImage(image_files_list[image_3d])
    data = sitk.GetArrayFromImage(itk_img)
    # origin = itk_img.GetOrigin()
    # direction = itk_img.GetDirection()
    # space = itk_img.GetSpacing()
    # x = np.zeros(data.shape[:], dtype=bool)
    # if x.shape[0]>nonzero_mask.shape[0] or  x.shape[1]>nonzero_mask.shape[1] or x.shape[2]>nonzero_mask.shape[2]:
    #     nonzero_mask = x

    this_mask = data != 0 # 不等于0的都认为是背景
    nonzero_mask = nonzero_mask | this_mask
nonzero_mask = binary_fill_holes(nonzero_mask)



'''
第二步根据生成的非零模板，确定用于裁剪的bounding_box大小和位置，在代码中就是要找到nonzero_mask在x，y，z三个坐标轴上值为1的最小坐标值以及最大坐标值。
'''
def  get_bbox_from_mask(nonzero_mask, outside_value=0):
    mask_voxel_coords = np.where(nonzero_mask != outside_value)
    minzidx = int(np.min(mask_voxel_coords[0]))
    maxzidx = int(np.max(mask_voxel_coords[0])) + 1
    minxidx = int(np.min(mask_voxel_coords[1]))
    maxxidx = int(np.max(mask_voxel_coords[1])) + 1
    minyidx = int(np.min(mask_voxel_coords[2]))
    maxyidx = int(np.max(mask_voxel_coords[2])) + 1
    bbox = [[minzidx, maxzidx], [minxidx, maxxidx], [minyidx, maxyidx]]
    return bbox
'''
第三步就根据bounding_box对该张图像的每个模态依次进行裁剪，然后重新组合在一起。
'''
bbox = get_bbox_from_mask(nonzero_mask)
resizer = (slice(bbox[0][0], bbox[0][1]), slice(bbox[1][0], bbox[1][1]), slice(bbox[2][0], bbox[2][1]))
cropped_data = []


for i in range(num_class):
    for j in range(len(img_path[i])):
        itk_img = sitk.ReadImage(img_path[i][j])
        data = sitk.GetArrayFromImage(itk_img)
        origin = itk_img.GetOrigin()
        direction = itk_img.GetDirection()
        space = itk_img.GetSpacing()
        cropped = data[resizer]
        cropped_data.append(cropped[None])
        print(data.shape)
        ## save

        out = sitk.GetImageFromArray(cropped)
        out.SetOrigin(origin)
        out.SetDirection(direction)
        out.SetSpacing(space)
        out_dir = os.path.join(out_path, str(i + 1), img_path[i][j].split('\\')[-1])
        sitk.WriteImage(out, out_dir)

        print(out_dir)
# for c in range(data.shape[0]):
#     cropped = data[c][resizer]
#     cropped_data.append(cropped[None])
# data = np.vstack(cropped_data)
