import cv2
import numpy as np
import random
import base64


def brightness(img, params):
    beta = params["beta"]
    new_img = cv2.add(img, beta)
    new_img = np.clip(new_img, 0, 255)
    return new_img


def contrast(img, params):
    """
    alpha*x + beta; default: alpha (0,2), beta (0,5)
    :param img: img
    :param params: a dict
    :return:
    """
    alpha = params["alpha"]
    beta = params["beta"]
    # new_img=cv2.normalize(img,dst=None,alpha=alpha,beta=beta,norm_type=cv2.NORM_MINMAX)
    new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    return new_img


def papper_noise(img, params):
    """
    Ps=0.05, Pp=0.02, then the noise density P=0.07, indicating that about 5% of the pixels in the image are contaminated by salt noise,
    About 2% of the pixels are contaminated by pepper noise, with a noise density of 7%, which means that 7% of the pixels
    in the image are contaminated by salt and pepper noise.
    :param img: image
    :param params: a dictionary
    :return: new image
    """
    ps = params["ps"]
    pp = params["pp"]
    mask = np.random.choice((0, 0.5, 1), size=img.shape[:2], p=[pp, (1 - ps - pp), ps])
    imgChoiceNoise = img.copy()
    imgChoiceNoise[mask == 1] = 255
    imgChoiceNoise[mask == 0] = 0
    return imgChoiceNoise


def uniform_noise(img, params):
    """
    uniform_noise mean, sigma = (5, 20), (50, 150)
    :param img: image
    :param params: dictionary
    :return: new image
    """
    mean = params["mean"]
    sigma = params["sigma"]
    a = 2 * mean - np.sqrt(12 * sigma)  # a = -14.64
    b = 2 * mean + np.sqrt(12 * sigma)  # b = 54.64
    noiseUniform = np.random.uniform(a, b, img.shape)
    imgUniformNoise = img + noiseUniform
    imgUniformNoise = np.uint8(
        cv2.normalize(imgUniformNoise, None, 0, 255, cv2.NORM_MINMAX)
    )
    return imgUniformNoise


def exponent_noise(img, params):
    """
    exponent_noise
    :param img: image
    :param params: dictionary
    :return: new image
    """
    a = params["a"]
    noiseExponent = np.random.exponential(scale=a, size=img.shape)
    imgExponentNoise = img + noiseExponent
    imgExponentNoise = np.uint8(
        cv2.normalize(imgExponentNoise, None, 0, 255, cv2.NORM_MINMAX)
    )
    return imgExponentNoise


def mean_blur(img, params):
    """
    mean_blur
    :param img:
    :param params:
    :return:
    """
    kernel_size = params["kernel_size"]
    # kernel size must smaller than the minimal edge length of the images, and it should be odd number
    if kernel_size % 2 != 1:
        kernel_size = kernel_size - 1
    img2 = cv2.blur(img, (kernel_size, kernel_size))
    return img2


def gaussian_blur(img, params):
    """
    gaussian_blur
    :param img:
    :param params:
    :return:
    """
    kernel_size = params["kernel_size"]
    # kernel size must smaller than the minimal edge length of the images, and it should be odd number
    if kernel_size % 2 != 1:
        kernel_size = kernel_size - 1
    img2 = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0, 0)
    return img2


def vertical_flip(img, params):
    """
    vertical_flip， no params
    :param img:
    :param params:
    :return:
    """
    new_img = cv2.flip(img, 0)
    return new_img


def mirror(img, params):
    """
    mirror，no params
    :param img:
    :param params:
    :return:
    """
    new_img = cv2.flip(img, 1)
    return new_img


def single_pixel(img, params):
    """
    change 1-10 pixels' value
    """
    num_pixel = params["num_pixel"]
    color = params["color"]
    row_lst = [random.randint(0, len(img) - 1) for _ in range(num_pixel)]
    col_lst = [random.randint(0, len(img[0]) - 1) for _ in range(num_pixel)]
    for i in range(len(row_lst)):
        img[row_lst[i]][col_lst[i]] = color
    return img


def poisson_noise(img, params):
    """
    add poison noise to images, no params needs
    """
    vals = len(np.unique(img))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy_img = np.random.poisson(img * vals) / float(vals)
    noisy_img = np.uint8(noisy_img)
    return noisy_img


def gaussian_noise(img, params):
    """
    add gaussian noise to img
    """
    mean = params["mean"]
    sigma = params["sigma"]
    # ratio = params["gaussian_noise"]["ratio"]
    img = img / 255
    noise = np.random.normal(mean, sigma, img.shape)
    gaussian_out = img + noise
    gaussian_out = np.clip(gaussian_out, 0, 1)
    gaussian_out = gaussian_out * 255
    gaussian_out = np.uint8(gaussian_out)
    return gaussian_out


def rotate_zero(img, params):
    """
    rotate theta angle around (0, 0)，-45 < theta < 45
    :param img:
    :param params:
    :return:
    """
    theta = params["theta"]
    rows, cols, ch = img.shape
    theta = np.pi / theta  # clockwise rotation angle
    cosTheta = np.cos(theta)
    sinTheta = np.sin(theta)
    MAT = np.float32([[cosTheta, -sinTheta, 0], [sinTheta, cosTheta, 0]])
    dst = cv2.warpAffine(img, MAT, (cols, rows), borderValue=(0, 0, 0))
    return dst


def rotate_center(img, params):
    """
    rotate around the center of the image, theta can be any integer
    :param img:
    :param params:
    :return:
    """
    theta = params["theta"]
    height, width, ch = img.shape
    x0, y0 = width // 2, height // 2
    MAR1 = cv2.getRotationMatrix2D((x0, y0), theta, 1.0)
    imgR1 = cv2.warpAffine(img, MAR1, (width, height))
    return imgR1


def affine(img, params):
    """
    「pos_1」-----------「pos_3」
        \                   \
        \                   \
        \                   \
        \                   \
        \                   \
    「pos_2」-----------「ignore」
    Affine transformation, it is recommended that the variation of x and y  between 0 and 10
    :param img:
    :param params:
    :return:
    """
    pos_1_x = params["pos_1_x"]
    pos_1_y = params["pos_1_y"]
    pos_2_x = params["pos_2_x"]
    pos_2_y = params["pos_2_y"]
    pos_3_x = params["pos_3_x"]
    pos_3_y = params["pos_3_y"]
    height, width = img.shape[:2]
    # elect three points on each of the original and target images
    mat_src = np.float32([[0, 0], [height, 0], [0, width]])
    # The positions of the three points after transformation
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


def perspective(img, params):
    """
    「pos_1」-----------「pos_3」
        \                   \
        \                   \
        \                   \
        \                   \
        \                   \
    「pos_2」-----------「pos_4」

    :param img:
    :param params:
    :return:
    """
    pos_1_x = params["pos_1_x"]
    pos_1_y = params["pos_1_y"]
    pos_2_x = params["pos_2_x"]
    pos_2_y = params["pos_2_y"]
    pos_3_x = params["pos_3_x"]
    pos_3_y = params["pos_3_y"]
    pos_4_x = params["pos_4_x"]
    pos_4_y = params["pos_4_y"]
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
    print("start")

    img = cv2.imread("../../../static/rest_framework/img/test_image.jpg")

    print(img)

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
        # "affine": {
        "pos_1_x": 25,
        "pos_1_y": 5,
        "pos_2_x": 18,
        "pos_2_y": 13,
        "pos_3_x": 18,
        "pos_3_y": 15,
        # },
        # 'perspective': {'pos_1_x': 11, 'pos_1_y': 6,
        #                 'pos_2_x': 4, 'pos_2_y': 5,
        #                 'pos_3_x': 8, 'pos_3_y': 4,
        #                 'pos_4_x': 9, 'pos_4_y': 12},
        # 'single_pixel': {'num_pixel': 6, 'color': 66},
        # 'poisson_noise': {'a': 0},
        # 'gaussian_noise': {'sigma': 0.01, 'mean': 0.01, 'ratio':0.1}
    }
    img_new = affine(img, params)
    # image = Image()
    # out = StringIO()
    # image.save(out, "PNG")
    # out.seek(0)
    # response.write(out.read())
    # cv2.imshow("tt", img_new)
    retval, img_buffer = cv2.imencode(".png", img_new)
    image_base = base64.b64encode(img_buffer)
    data = {
        "image": "data:image/png;base64," + image_base.decode("utf-8"),
    }

    print(data)
