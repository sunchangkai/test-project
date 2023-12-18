import random
import cv2
import numpy as np
from mutation.utils import mutators
from copy import deepcopy
from seed_selection.utils import seed
from lib.logger import Logger
import time


class mutationStrategy(object):
    """
    the params is a dict like : {
                                'aug_method_1':{'param_1': (x, y), ......,'param_n'(i, j)},
                                ......
                                'aug_method_n':{'param_1': (x, y), ......,'param_n'(i, j)},
                                }
    the value of params is a tuple means the range!
    """

    def __init__(
        self,
        k: int,
        try_time: int,
        params: dict,
        alpha: float,
        beta: float,
        project: str,
        model,
    ):
        """

        :param k: Total number of tests to be generated
        :param try_time: The maximum number of trials
        :param params: the dict store the range for each parameter for mutators
        :param alpha: the radio of the number of pixels could be changed
        :param beta: the radio of the range of a pixel's value could be changed
        """
        self.k = k
        self.try_time = try_time
        self.current_params = {}
        self.meta_params = params
        self.alpha = alpha
        self.beta = beta
        self.project = project
        self.logger = Logger(log_name=project, log_path=f"{project}/Mylog.log")
        self.model = model
        self.change_params()
        # mutator = mutators(params=self.current_params)
        self.mutator = mutators(params=self.current_params, model=self.model)

    def change_params(self):
        for key in self.meta_params:
            self.current_params[key] = {}
            for sub_key in self.meta_params[key]:
                if sub_key != "dtype":
                    if self.meta_params[key]["dtype"] == "int":
                        if isinstance(self.meta_params[key][sub_key], list):
                            self.current_params[key][sub_key] = random.randint(
                                self.meta_params[key][sub_key][0],
                                self.meta_params[key][sub_key][1],
                            )
                        else:
                            self.current_params[key][sub_key] = self.meta_params[key][
                                sub_key
                            ]
                    elif self.meta_params[key]["dtype"] == "float":
                        if isinstance(self.meta_params[key][sub_key], list):
                            self.current_params[key][sub_key] = random.uniform(
                                self.meta_params[key][sub_key][0],
                                self.meta_params[key][sub_key][1],
                            )
                        else:
                            self.current_params[key][sub_key] = self.meta_params[key][
                                sub_key
                            ]

    def mutate_one(self, cur_seed: seed, img: np.ndarray):
        """
        :param seed: a seed class
        :param state: whether ref_img == init_img; stat=0: ref_img==init_img; state=1:ref_img!=init_img
        :return: a dict like:{sample1:{ref_img: np.ndarray, init_img: path, img: np.ndarray}}
        """
        # ref_img = cv2.imread(cur_seed.ref_path)
        init_img = cv2.imread(cur_seed.init_path)
        state = cur_seed.state
        label = cur_seed.label
        # self.change_params()
        # # mutator = mutators(params=self.current_params)
        # self.mutator = mutators(params=self.current_params, model=self.model)
        cc = 0
        res = {}
        for k in range(self.k):
            flag = False
            for t in range(self.try_time):
                new_img = deepcopy(img)
                # if s′ is the same with s0 then
                # if (ref_img == init_img).all():
                if state == 0:
                    # t ← randomPick(G U P)
                    mutator_dict = self.mutator.sample_mutators_p_g()
                else:
                    # t ← randomPick(P);
                    mutator_dict = self.mutator.sample_mutators_p()
                mutated_method = list(mutator_dict.keys())[0]
                self.logger.add_log(s=f"{mutator_dict.keys()} has been chosen")
                # print(f"{mutator_dict.keys()} has been chosen")
                # p ← pickRandomParam(t);
                self.change_params()
                # s′ ← t(s,p);
                for fn_name in mutator_dict.keys():
                    if fn_name in self.current_params:
                        temp_fn = mutator_dict[fn_name]
                        new_img = temp_fn(
                            img=new_img, params=self.current_params, seed=cur_seed
                        )
                # if isSatisf ied f (s0, s′) then
                if self.is_satisfy(img=init_img, img_bar=new_img):
                    # if t ∈ G then :if 'p_or_g' == 'g': renew the ref_img
                    # define the info of new mutated image
                    new_state = state
                    new_ref_path = cur_seed.ref_path
                    new_init_path = cur_seed.init_path
                    if mutator_dict["p_or_g"] == "g":
                        # s 0′ ← t ( s 0 , p ) ;
                        new_ref_img = deepcopy(init_img)
                        for fn_name in mutator_dict.keys():
                            if fn_name == "p_or_g":
                                continue
                            temp_fn = mutator_dict[fn_name]
                            new_ref_img = temp_fn(
                                img=new_ref_img,
                                params=self.current_params,
                                seed=cur_seed,
                            )
                        # i n f o ( s ′ ) ← ( s 0 , s 0′ ) ;
                        # -> store the new ref-img
                        # -> renew the ref_path
                        new_state = 1
                        new_ref_path = (
                            f"./{self.project}/saved/ref-{cc}-{str(time.time())}.png"
                        )
                        cv2.imwrite(
                            f"./{self.project}/saved/ref-{cc}-{str(time.time())}.png",
                            new_ref_img,
                        )
                        new_init_path = cur_seed.init_path
                    # Success ← True;
                    flag = True
                    # T ← U {s′};
                    res[cc] = {
                        "ref_path": new_ref_path,
                        "init_path": new_init_path,
                        "img": new_img,
                        "state": new_state,
                        "label": label,
                        "mutated_method": mutated_method,
                        "from_seed_path": cur_seed.path,
                    }
                    self.logger.add_log(
                        s=f'new image has been created: ref_path: {res[cc]["ref_path"]}, '
                        f'init_path: {res[cc]["init_path"]}, '
                        f'state: {res[cc]["state"]}'
                    )
                    # print(f'new image has been created: ref_path: {res[cc]["ref_path"]}, '
                    #       f'init_path: {res[cc]["init_path"]}, '
                    #       f'state: {res[cc]["state"]}')
                    cc += 1
                    break
            # if not Success then
            if not flag:
                res[cc] = {
                    "ref_path": cur_seed.ref_path,
                    "init_path": cur_seed.init_path,
                    "img": img,
                    "state": cur_seed.state,
                    "label": label,
                    "mutated_method": None,
                    "from_seed_path": cur_seed.path,
                }
                self.logger.add_log(
                    f'add original image: ref_path: {res[cc]["ref_path"]}, '
                    f'init_path: {res[cc]["init_path"]}, '
                    f'state: {res[cc]["state"]}'
                )
                # print(f'add original image: ref_path: {res[cc]["ref_path"]}, '
                #       f'init_path: {res[cc]["init_path"]}, '
                #       f'state: {res[cc]["state"]}')
        return res

    def is_satisfy(self, img, img_bar):
        h, w, c = img.shape
        pixel_num = h * w * c
        # calculate the number of pixel img == img_bar
        l_0 = np.sum(img == img_bar)
        # calculate the divation between img and img_bar
        l_alpha = abs(img - img_bar)
        if l_0 < self.alpha * pixel_num:
            if (l_alpha <= 255).all():
                return True
            else:
                return False
        else:
            if (l_alpha <= 255 * self.beta).all():
                return True
            else:
                return False


if __name__ == "__main__":
    print(abs(np.array([[-1], [1], [-3]])))
