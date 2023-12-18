import cv2
import numpy as np
import os
import random
from copy import deepcopy
import tensorflow as tf
from keras import losses


random_seed = 2022


# random.seed(random_seed)
def onehot(label, cls_num):
    res = np.array([0 for i in range(cls_num)])
    res[label] = 1
    res = np.expand_dims(res, axis=0)
    return res


class mutators(object):
    def __init__(self, params, model):
        """
        this is a controller for both affine transformation and pixel-level transformation
        """
        self.params = params
        self.model = model
        self.pixel_modification = pixelModification(
            params=self.params, model=self.model
        )
        self.affine_modification = affineModification(params=self.params)

    def sample_mutators_p_g(self, num=1, replace=False):
        p_dict = self.pixel_modification.sample()
        p_name_lst = list(p_dict.keys())
        g_dict = self.affine_modification.sample()
        g_name_lst = list(g_dict.keys())
        p_g_name_lst = p_name_lst + g_name_lst
        rand_indx = random.randint(0, len(p_g_name_lst) - 1)
        random.shuffle(p_g_name_lst)
        res = {}
        if p_g_name_lst[rand_indx] in p_name_lst:
            res[p_g_name_lst[rand_indx]] = p_dict[p_g_name_lst[rand_indx]]
            res["p_or_g"] = "p"
            return res
        elif p_g_name_lst[rand_indx] in g_name_lst:
            res[p_g_name_lst[rand_indx]] = g_dict[p_g_name_lst[rand_indx]]
            res["p_or_g"] = "g"
            return res

    def sample_mutators_p(self, num=1, replace=False):
        res = self.pixel_modification.sample(num, replace)
        res["p_or_g"] = "p"
        return res


class pixelModification(object):
    """
    currently, we have brightness, contrast, papper_noise, uniform_noise, exponent_noise
    mean_blur, gaussian_blur, vertical_flip, mirror
    """

    def __init__(self, params, model):
        """
        init pixel modification function, params should be a dict like
        {'aug_method': {param_1:x, param_2:y}}
        all the key in params dict should be in the self.function_dict
        aug method could be modified by your own
        :param params:
        """
        self.model = model
        self.al_function_dict = {
            "brightness": self.brightness,
            "contrast": self.contrast,
            "papper_noise": self.papper_noise,
            "uniform_noise": self.uniform_noise,
            "exponent_noise": self.exponent_noise,
            "mean_blur": self.mean_blur,
            "gaussian_blur": self.gaussian_blur,
            "vertical_flip": self.vertical_flip,
            "mirror": self.mirror,
            "single_pixel": self.single_pixel,
            "poisson_noise": self.poisson_noise,
            "gaussian_noise": self.gaussian_noise,
            "FGSM": self.FGSM,
            "IFGSM": self.IFGSM,
        }
        self.ap_function_dict = {}
        self.info_name = []
        for key in params:
            if key in self.al_function_dict:
                self.info_name.append(key)
                self.ap_function_dict[key] = self.al_function_dict[key]
        print(f"for pixel modification, {self.info_name} would be applied!")

    def sample(self, num: int = 1, repeat: bool = False):
        """
        sampling modification method
        :param num: how many functions would be sampled
        :param repeat: could sample one function more than 1 time
        :return: a dict like {'aug_method': aug_method, .........}
        """
        res = {}
        if num >= len(self.ap_function_dict) or num == -1:
            dict_key = list(self.ap_function_dict.keys())
            random.shuffle(dict_key)
            for key in dict_key:
                res[key] = self.ap_function_dict[key]
            return res
        else:
            dict_key = list(self.ap_function_dict.keys())
            ch_keys = np.random.choice(dict_key, size=num)
            for key in ch_keys:
                res[key] = self.ap_function_dict[key]
            return res

    def brightness(self, img, params, seed):
        beta = params["brightness"]["beta"]
        new_img = cv2.add(img, beta)
        new_img = np.clip(new_img, 0, 255)
        return new_img

    def contrast(self, img, params, seed):
        """
        alpha*x + beta; default: alpha (0,2), beta (0,5)
        :param img: img
        :param params: a dict
        :return:
        """
        alpha = params["contrast"]["alpha"]
        beta = params["contrast"]["beta"]
        # new_img=cv2.normalize(img,dst=None,alpha=alpha,beta=beta,norm_type=cv2.NORM_MINMAX)
        new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return new_img

    def papper_noise(self, img, params, seed):
        """
        Ps=0.05，Pp=0.02，则噪声密度 P=0.07，表示图像中约 5% 的像素被盐粒噪声污染，
        约 2% 的像素被胡椒粒噪声污染，噪声密度为 7%，即图像中 7% 的像素被椒盐噪声污染。
        :param img: image
        :param params: a dictionary
        :return: new image
        """
        ps = params["papper_noise"]["ps"]
        pp = params["papper_noise"]["pp"]
        mask = np.random.choice(
            (0, 0.5, 1), size=img.shape[:2], p=[pp, (1 - ps - pp), ps]
        )
        imgChoiceNoise = img.copy()
        imgChoiceNoise[mask == 1] = 255
        imgChoiceNoise[mask == 0] = 0
        return imgChoiceNoise

    def uniform_noise(self, img, params, seed):
        """
        均匀噪声 mean, sigma = (5, 20), (50, 150)
        :param img: image
        :param params: dictionary
        :return: new image
        """
        mean = params["uniform_noise"]["mean"]
        sigma = params["uniform_noise"]["sigma"]
        a = 2 * mean - np.sqrt(12 * sigma)  # a = -14.64
        b = 2 * mean + np.sqrt(12 * sigma)  # b = 54.64
        noiseUniform = np.random.uniform(a, b, img.shape)
        imgUniformNoise = img + noiseUniform
        imgUniformNoise = np.uint8(
            cv2.normalize(imgUniformNoise, None, 0, 255, cv2.NORM_MINMAX)
        )
        return imgUniformNoise

    def exponent_noise(self, img, params, seed):
        """
        指数噪声
        :param img: image
        :param params: dictionary
        :return: new image
        """
        a = params["exponent_noise"]["a"]
        noiseExponent = np.random.exponential(scale=a, size=img.shape)
        imgExponentNoise = img + noiseExponent
        imgExponentNoise = np.uint8(
            cv2.normalize(imgExponentNoise, None, 0, 255, cv2.NORM_MINMAX)
        )
        return imgExponentNoise

    def mean_blur(self, img, params, seed):
        """
        均值滤波
        :param img:
        :param params:
        :return:
        """
        kernel_size = params["mean_blur"]["kernel_size"]
        if kernel_size % 2 != 1:
            kernel_size = kernel_size - 1
        img2 = cv2.blur(img, (kernel_size, kernel_size))
        return img2

    def gaussian_blur(self, img, params, seed):
        """
        高斯滤波
        :param img:
        :param params:
        :return:
        """
        kernel_size = params["gaussian_blur"]["kernel_size"]
        if kernel_size % 2 != 1:
            kernel_size = kernel_size - 1
        img2 = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0, 0)
        return img2

    def vertical_flip(self, img, params, seed):
        """
        水平翻转，不需要参数
        :param img:
        :param params:
        :return:
        """
        new_img = cv2.flip(img, 0)
        return new_img

    def mirror(self, img, params, seed):
        """
        镜像，不需要参数
        :param img:
        :param params:
        :return:
        """
        new_img = cv2.flip(img, 1)
        return new_img

    def single_pixel(self, img, params, seed):
        """
        change 1-10 pixels' value
        """
        num_pixel = params["single_pixel"]["num_pixel"]
        color = params["single_pixel"]["color"]
        row_lst = [random.randint(0, len(img) - 1) for _ in range(num_pixel)]
        col_lst = [random.randint(0, len(img[0]) - 1) for _ in range(num_pixel)]
        for i in range(len(row_lst)):
            img[row_lst[i]][col_lst[i]] = color
        return img

    def poisson_noise(self, img, params, seed):
        """
        add poison noise to images, no params needs
        """
        vals = len(np.unique(img))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy_img = np.random.poisson(img * vals) / float(vals)
        noisy_img = np.uint8(noisy_img)
        return noisy_img

    def gaussian_noise(self, img, params, seed):
        """
        add gaussian noise to img
        """
        mean = params["gaussian_noise"]["mean"]
        sigma = params["gaussian_noise"]["sigma"]
        # ratio = params["gaussian_noise"]["ratio"]
        img = img / 255
        noise = np.random.normal(mean, sigma, img.shape)
        gaussian_out = img + noise
        gaussian_out = np.clip(gaussian_out, 0, 1)
        gaussian_out = gaussian_out * 255
        gaussian_out = np.uint8(gaussian_out)
        return gaussian_out

    def FGSM(self, img, params, seed):
        model = self.model
        eps = params["FGSM"]["eps"]
        clas_num = params["FGSM"]["class_num"]
        print(eps)
        label = seed.label
        img = np.expand_dims(img[:, :, ::-1] / 255, axis=0)
        loss_fn = losses.CategoricalCrossentropy(from_logits=True)
        y_true = onehot(label=label, cls_num=clas_num)
        images = tf.cast(img, tf.float32)
        with tf.GradientTape() as tape:
            tape.watch(images)
            preds = model(images)
            # top_class = preds[:, y]
            loss_val = loss_fn(y_true, preds)
        grads = tape.gradient(loss_val, images)
        grads = grads.numpy()[0]
        p_grads = np.sign(grads)
        n_image = (img[0] + (eps * p_grads)) * 255
        # n_image = n_image + (eps*p_grads)
        n_image = np.clip(n_image, a_min=0, a_max=255)
        n_image = n_image.astype(np.uint8)
        # n_image = np.clip((img[0]*255 + (p_grads * eps)).astype(np.uint8), a_min=0, a_max=255)
        return n_image[:, :, ::-1]

    def IFGSM(self, img, params, seed):
        model = self.model
        eps = params["IFGSM"]["eps"]
        clas_num = params["IFGSM"]["class_num"]
        num_iter = params["IFGSM"]["iteration_num"]
        label = seed.label
        img = np.expand_dims(img[:, :, ::-1] / 255, axis=0)  # RGB
        loss_fn = losses.CategoricalCrossentropy(from_logits=True)
        y_true = onehot(label=label, cls_num=clas_num)
        for i in range(num_iter):
            images = tf.cast(img, tf.float32)
            with tf.GradientTape() as tape:
                tape.watch(images)
                preds = model(images)
                # top_class = preds[:, y]
                loss_val = loss_fn(y_true, preds)
            grads = tape.gradient(loss_val, images)
            grads = grads.numpy()
            p_grads = np.sign(grads)
            img = img + (eps * p_grads)
        img = img * 255
        n_image = np.clip(img[0].astype(np.uint8), a_min=0, a_max=255)
        return n_image[:, :, ::-1]  # BGR


class affineModification(object):
    def __init__(self, params):
        self.al_function_dict = {
            "rotate_zero": self.rotate_zero,
            "rotate_center": self.rotate_center,
            "affine": self.affine,
            "perspective": self.perspective,
        }
        self.ap_function_dict = {}
        self.info_name = []
        for key in params:
            if key in self.al_function_dict:
                self.info_name.append(key)
                self.ap_function_dict[key] = self.al_function_dict[key]
        print(f"for affine modification, {self.info_name} would be applied!")

    def sample(self):
        rand_indx = random.randint(0, len(self.ap_function_dict) - 1)
        i = 0
        res = {}
        for key in self.ap_function_dict:
            if i == rand_indx:
                res[key] = self.ap_function_dict[key]
                break
            i += 1
        return res

    def rotate_zero(self, img, params, seed):
        """
        旋转，绕（0，,0）旋转theta个角度，-45 < theta < 45
        :param img:
        :param params:
        :return:
        """
        theta = params["rotate_zero"]["theta"]
        rows, cols, ch = img.shape
        theta = np.pi / theta  # 顺时针旋转角度
        cosTheta = np.cos(theta)
        sinTheta = np.sin(theta)
        MAT = np.float32([[cosTheta, -sinTheta, 0], [sinTheta, cosTheta, 0]])
        dst = cv2.warpAffine(img, MAT, (cols, rows), borderValue=(0, 0, 0))
        return dst

    def rotate_center(self, img, params, seed):
        """
        绕图片中心做旋转，theta可为任意整数
        :param img:
        :param params:
        :return:
        """
        theta = params["rotate_center"]["theta"]
        height, width, ch = img.shape
        x0, y0 = width // 2, height // 2
        MAR1 = cv2.getRotationMatrix2D((x0, y0), theta, 1.0)
        imgR1 = cv2.warpAffine(img, MAR1, (width, height))
        return imgR1

    def affine(self, img, params, seed=1):
        """
        「pos_1」-----------「pos_3」
            \                   \
            \                   \
            \                   \
            \                   \
            \                   \
        「pos_2」-----------「ignore」
        仿射变换, 建议每个点的x和y值的变化在0-10之间
        :param img:
        :param params:
        :return:
        """
        pos_1_x = params["affine"]["pos_1_x"]
        pos_1_y = params["affine"]["pos_1_y"]
        pos_2_x = params["affine"]["pos_2_x"]
        pos_2_y = params["affine"]["pos_2_y"]
        pos_3_x = params["affine"]["pos_3_x"]
        pos_3_y = params["affine"]["pos_3_y"]
        height, width = img.shape[:2]
        # 在原图像和目标图像上各选择三个点
        mat_src = np.float32([[0, 0], [height, 0], [0, width]])
        # 变换后三个点的位置
        mat_dst = np.float32(
            [
                [pos_1_y, pos_1_x],
                [height - pos_2_y, pos_2_x],
                [pos_3_y, width - pos_3_x],
            ]
        )
        mat_trans = cv2.getAffineTransform(mat_src, mat_dst)
        dst = cv2.warpAffine(img, mat_trans, (height, width))
        dst = dst[
            max(pos_1_x, pos_3_x) : height - pos_2_x,
            max(pos_1_y, pos_2_y) : width - pos_3_y,
            :,
        ]
        dst = cv2.resize(dst, (height, width))
        return dst

    def perspective(self, img, params, seed=1):
        """
        「pos_1」-----------「pos_3」
            \                   \
            \                   \
            \                   \
            \                   \
            \                   \
        「pos_2」-----------「pos_4」
        仿射变换, 建议每个点的x和y值的变化在0-10之间
        :param img:
        :param params:
        :return:
        """
        pos_1_x = params["perspective"]["pos_1_x"]
        pos_1_y = params["perspective"]["pos_1_y"]
        pos_2_x = params["perspective"]["pos_2_x"]
        pos_2_y = params["perspective"]["pos_2_y"]
        pos_3_x = params["perspective"]["pos_3_x"]
        pos_3_y = params["perspective"]["pos_3_y"]
        pos_4_x = params["perspective"]["pos_4_x"]
        pos_4_y = params["perspective"]["pos_4_y"]
        height, width = img.shape[:2]
        former = np.float32([[0, 0], [height, 0], [0, width], [height, width]])
        pts = np.float32(
            [
                [pos_1_y, pos_1_x],
                [height - pos_2_y, pos_2_x],
                [pos_3_y, width - pos_3_x],
                [height - pos_4_y, width - pos_4_x],
            ]
        )
        M = cv2.getPerspectiveTransform(former, pts)
        out_img = cv2.warpPerspective(img, M, (height, width))
        out_img = out_img[
            min(pos_1_x, pos_3_x) : max(height - pos_2_x, height - pos_4_x),
            min(pos_1_y, pos_2_y) : max(width - pos_3_y, width - pos_4_y),
            :,
        ]
        out_img = cv2.resize(out_img, (height, width))
        return out_img


if __name__ == "__main__":
    img = cv2.imread("../data/clsed_images_train/1/016_1_0001_1_j.png")
    params = {
        # 'brightness': {'beta': 50},
        # 'mean_blur': {'kernel_size': 5},
        # 'gaussian_blur': {'kernel_size': 5},
        # 'exponent_noise': {'a': 5},
        # 'contrast':{'alpha': 1.5, 'beta': 5},
        # 'papper_noise':{'ps': 0.005, 'pp':0.005},
        # 'uniform_noise': {'mean': 57.9, 'sigma':59.6},
        # 'vertical_flip': {'a': 13},
        # 'mirror': {'b': 15},
        # 'rotate_zero': {'theta':38},
        # 'rotate_center': {'theta': 90},
        "affine": {
            "pos_1_x": 25,
            "pos_1_y": 5,
            "pos_2_x": 18,
            "pos_2_y": 13,
            "pos_3_x": 18,
            "pos_3_y": 15,
        },
        # 'perspective': {'pos_1_x': 11, 'pos_1_y': 6,
        #                 'pos_2_x': 4, 'pos_2_y': 5,
        #                 'pos_3_x': 8, 'pos_3_y': 4,
        #                 'pos_4_x': 9, 'pos_4_y': 12},
        # 'single_pixel': {'num_pixel': 6, 'color': 66},
        # 'poisson_noise': {'a': 0},
        # 'gaussian_noise': {'sigma': 0.01, 'mean': 0.01, 'ratio':0.1}
    }
    # pixel_aug = pixelModification(params)
    # fns = pixel_aug.sample()
    affine_aug = affineModification(params)
    fns = affine_aug.sample()
    print(fns.keys())
    for fn_name in fns:
        temp_fn = fns[fn_name]
        img = temp_fn(img, params)
    cv2.imshow("tt", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
