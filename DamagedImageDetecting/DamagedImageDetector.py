import os

from DamagedImageDetecting.CheckImage import CheckImage
from PIL import Image


class CheckBrockImage(object):
    def __init__(self, train_dir):
        self.train_dir = train_dir
        self.completeFile = 0
        self.incompleteFile = 0

    def get_imgs(self):
        """搜尋底下圖片"""
        for file in os.listdir(self.train_dir):
            if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == ".jpeg":

                try:

                    ret = self.check_img(file)
                    if ret:
                        self.completeFile += 1

                    else:
                        self.incompleteFile = self.incompleteFile + 1
                        self.img_remove(file)  # 删除不完整图片

                    self.resize_image(file)
                except FileNotFoundError as e:
                    print(f"FileNotFoundError {e}")

    # resize image 並且 刪除太小的圖片
    def resize_image(self, file):
        image = Image.open(self.train_dir + file)
        if (180, 180) > image.size:
            self.img_remove(file)
        elif (400, 400) < image.size:
            image.thumbnail((400, 400))
            image.save(self.train_dir + file)
            print("image resized: " + file + str(image.size))

    def img_remove(self, file):
        """刪除圖片"""
        print("image removed")
        os.remove(self.train_dir + file)

    def check_img(self, img_file):
        """檢測圖片"""
        boo = False
        try:
            boo = CheckImage(self.train_dir + img_file).check_jpg_jpeg()
        except OSError as e:
            print(e)
        return boo

    def run(self):
        """執行程式"""
        self.get_imgs()

        print('毀損圖片 : %d個' % self.incompleteFile)
        print('正常圖片 : %d個' % self.completeFile)


if __name__ == '__main__':
    # landmark 的資料夾路徑
    dir = '../train/白馬塔'

    print('正在檢測' + dir + ':')
    imgs = CheckBrockImage(dir + "/")
    imgs.run()
