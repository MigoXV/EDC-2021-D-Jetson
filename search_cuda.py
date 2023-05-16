import cv2
import numpy as np

def search_black(self, image, tick_time):
    black_min = np.array([0, 0, 0], dtype=np.uint8)  # 根据原始代码的阈值范围进行调整
    black_max = np.array([180, 255, 50], dtype=np.uint8)  # 根据原始代码的阈值范围进行调整

    image_cuda = cv2.cuda_GpuMat()  # 创建CUDA设备上的图像对象
    image_cuda.upload(image)  # 将图像数据上传到CUDA设备

    hsv_cuda = cv2.cuda.cvtColor(image_cuda, cv2.COLOR_BGR2HSV)  # 在CUDA设备上进行颜色空间转换
    mask_cuda = cv2.cuda.inRange(hsv_cuda, black_min, black_max)  # 在CUDA设备上进行阈值处理

    cnts_cuda = cv2.cuda.findContours(mask_cuda, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 在CUDA设备上查找轮廓
    cnts = cnts_cuda.download()  # 将轮廓数据下载到主机

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    c = None
    for c_ in cnts:
        if 1500 > cv2.contourArea(c_) > 10:
            bounding_box = cv2.boundingRect(c_)
            if bounding_box[0] < 5 and bounding_box[1] < 5:
                continue
            if bounding_box[0] < 5 and bounding_box[1] + bounding_box[3] > 475:
                continue
            if bounding_box[0] + bounding_box[2] > 635 and bounding_box[1] < 5:
                continue
            if bounding_box[0] + bounding_box[2] > 635 and bounding_box[1] + bounding_box[3] > 475:
                continue
            if bounding_box[2] < bounding_box[3] * 1.1:
                c = c_
                break

    if c is None:
        return

    bounding_box = cv2.boundingRect(c)
    cv2.rectangle(image, (bounding_box[0], bounding_box[1]),
                  (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                  (0, 0, 255), 2)

    M = cv2.moments(c)
    if M["m00"] == 0 or M["m00"] == 0:
        return

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    message = "Center(" + str(cX) + "," + str(cY) + ")"
    cv2.putText(image, message, (bounding_box[0] - 20, bounding_box[1] - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    if self.start_flag:
        self.analysis((cX, cY), tick_time)
