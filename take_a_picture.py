# 依靠CV2来进行摄像头的拍照，将照片保存本地
from cv2.cv2 import VideoCapture, imwrite, imshow, waitKey

# 获取本地摄像头
# folder_path 截取图片的存储目录
from cv2.cv2 import destroyAllWindows


def get_img_from_camera_local(folder_path):
    cap = VideoCapture(0)
    ret, frame = cap.read()
    # cv2.imshow("capture", frame)
    imwrite(folder_path, frame)  # 存储为图像
    cap.release()
    destroyAllWindows()


# 获取网络摄像头，格式：rtsp://username:pwd@ip/
# folder_path 截取图片的存储目录
def get_img_from_camera_net(folder_path):
    cap = VideoCapture('rtsp://username:pwd@ip/')
    i = 1
    while True:
        ret, frame = cap.read()
        imshow("capture", frame)
        print(str(i))
        imwrite(folder_path + str(i) + '.jpg', frame)  # 存储为图像
        if waitKey(1) & 0xFF == ord('q'):
            break
        i += 1
    cap.release()
    destroyAllWindows()
