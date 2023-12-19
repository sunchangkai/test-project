import time
import cv2
import numpy as np
import tensorflow.keras as keras
import os
from seed_selection.seedSelection import seedSelection
from mutation.mutationStrategy import mutationStrategy
from copy import deepcopy
from utils.utils import decode_res, create_folder, decode_yaml, store_label_json
from criteria.criterial_strategy import CriteriaStrategy
from lib.logger import Logger
from scipy.special import softmax


np.set_printoptions(precision=10, suppress=True)

agewegweg=1

class DeepHuner(object):
    def __init__(
        self,
        img_dir,
        output_dir,
        model_path,
        criteria,
        criteria_params,
        p_min,
        r,
        k_times,
        try_num,
        max_iter,
        alpha,
        beta,
        meta_params,
        project,
        batch_size=1,
    ):
        # hyperparams init
        self.img_dir = img_dir
        self.output_dir = output_dir
        self.model_path = model_path
        self.p_min = p_min
        self.r = r
        self.k_times = k_times
        self.try_num = try_num
        self.max_iter = max_iter
        self.criteria = criteria
        self.alpha = alpha
        self.beta = beta
        self.meta_params = meta_params
        self.criteria_params = criteria_params
        self.batch_size = batch_size
        self.attack_total = 0
        self.attack_success = 0
        # init the project folder
        if not os.path.exists(project):
            self.project = project
            create_folder(project)
        else:
            project = project + str(time.time())
            self.project = project
            create_folder(project)
        # init seed strategy
        self.seed_selection = seedSelection(
            img_dir=self.img_dir, p_min=self.p_min, r=self.r, project=project
        )
        # init model
        self.model = keras.models.load_model(model_path)
        # init mutation strategy
        self.fuzzer = mutationStrategy(
            k=self.k_times,
            try_time=self.try_num,
            alpha=self.alpha,
            beta=self.beta,
            params=self.meta_params,
            project=self.project,
            model=self.model,
        )
        # init criteria strategy
        self.criteria_calculator = CriteriaStrategy(
            criteria=self.criteria, model=self.model, params=self.criteria_params
        )
        # fail_set is a dict: {sample1: {'label': x, path: ''}}
        self.fail_set = {}
        self.logger = Logger(log_name=project, log_path=f"{project}/Mylog.log")

    def isCoverageGain(self, o_img, m_lst):
        if self.criteria[0] in ["NC", "KMNC", "TopK"]:
            o_img = deepcopy(o_img)
            m_lst = deepcopy(m_lst)
            m_imgs = []
            for diction in m_lst:
                for key in diction:
                    m_imgs.append(diction[key]["img"])
            o_img, m_imgs = np.array(o_img), np.array(m_imgs)
            o_img, m_imgs = o_img[:, :, :, ::-1] / 255, m_imgs[:, :, :, ::-1] / 255
            o_res = self.criteria_calculator.calculate(
                model_name=self.project, img=[o_img]
            )
            m_res = self.criteria_calculator.calculate(
                model_name=self.project, img=[m_imgs]
            )
            # ttt = 1
            gained_indx = []
            for i in range(self.batch_size):
                split_m_res = m_res[self.criteria[0]][
                    i * self.k_times : (i + 1) * self.k_times
                ]
                split_o_res = o_res[self.criteria[0]][i]
                compare_res = split_m_res > split_o_res
                t_indx = np.where(compare_res is True)[0] + (self.k_times * i)
                gained_indx += t_indx.tolist()
            return gained_indx
        elif self.criteria[0] in ["NeuronSensitivity"]:
            e = self.criteria_params["NeuronSensitivity"]["e"]
            o_img = deepcopy(o_img)
            m_lst = deepcopy(m_lst)
            m_imgs = []
            o_imgs = []
            gained_indx = []
            for j in range(len(m_lst)):
                diction = m_lst[j]
                for key in diction:
                    m_imgs.append(diction[key]["img"])
                    o_imgs.append(o_img[j])
            o_imgs, m_imgs = np.array(o_imgs), np.array(m_imgs)
            o_imgs, m_imgs = o_imgs[:, :, :, ::-1] / 255, m_imgs[:, :, :, ::-1] / 255
            m_res = self.criteria_calculator.calculate(
                model_name=self.project, img=[o_imgs, m_imgs]
            )
            bool_res = m_res[self.criteria[0]] > e
            for p in range(len(bool_res)):
                if bool_res[p]:
                    gained_indx.append(p)
            return gained_indx

    def run(self):
        ccc = 1
        for i in range(self.max_iter):
            with open(f"{self.project}/iteration.txt", "w") as f:
                f.write(f"iteration: {i}")
            f.close()
            self.attack_total += self.k_times * self.batch_size
            print("=" * 10, f"iteration-{i}", "=" * 10)
            # sample a seed
            temp_seed_classes = self.seed_selection.get_seed(num=self.batch_size)
            temp_seeds = []
            for item in temp_seed_classes:
                temp_seeds.append(cv2.imread(item.path))
            # temp_seed = cv2.imread(temp_seed_class.path)
            # mutation
            mutated_lst = []
            for i in range(len(temp_seed_classes)):
                temp_seed = temp_seeds[i]
                temp_seed_class = temp_seed_classes[i]
                temp_mutated_dict = self.fuzzer.mutate_one(
                    cur_seed=temp_seed_class, img=temp_seed
                )
                mutated_lst.append(temp_mutated_dict)
            # mutated_dict = self.fuzzer.mutate_one(cur_seed=temp_seed_class, img=temp_seed)
            # update the probability of current seed
            # regard multiple times mutation as once: m_times -> 1
            self.seed_selection.update_seed(m_times=1)
            # use real mutation time: m_times -> len(mutated_dict)
            # self.seed_selection.update_seed(m_times=len(mutated_dict))
            # test result
            for i in range(len(mutated_lst)):
                mutated_dict = mutated_lst[i]
                temp_seed_class = temp_seed_classes[i]
                temp_mutated_imgs = np.array(
                    [mutated_dict[j]["img"] / 255 for j in mutated_dict]
                )
                res = self.model.predict(temp_mutated_imgs[:, :, :, ::-1], verbose=0)
                pred_label = decode_res(res)
                temp_label = temp_seed_class.label
                need_to_save = pred_label == temp_label
                for k in range(len(need_to_save)):
                    if not need_to_save[k]:
                        self.attack_success += 1
                        if not os.path.exists(f"{self.project}/fail_test/{temp_label}"):
                            os.makedirs(f"{self.project}/fail_test/{temp_label}")
                        temp_path = f"{self.project}/fail_test/{temp_label}/{ccc}.png"
                        temp_pre_res = np.round(softmax(res[k]), 4)
                        cv2.imwrite(temp_path, mutated_dict[k]["img"])
                        # store the diff, it could be deleted at anytime!
                        ori_img = temp_seeds[i]
                        ttt_m_img = mutated_dict[k]["img"]
                        diff_img = ttt_m_img - ori_img
                        if not os.path.exists(
                            f"{self.project}/fail_test_diff/{temp_label}"
                        ):
                            os.makedirs(f"{self.project}/fail_test_diff/{temp_label}")
                        temp_diff_path = (
                            f"{self.project}/fail_test_diff/{temp_label}/{ccc}_diff.png"
                        )
                        cv2.imwrite(temp_diff_path, diff_img)
                        # =========================
                        self.logger.add_log(
                            s=f"for {temp_path}: its label should be {temp_label}, "
                            f"but got {pred_label[k]}, it would be stored in {temp_path}"
                        )
                        with open(f"{self.project}/fail_test_info.txt", "a") as f:
                            sss = (
                                f"ref_path:{mutated_dict[k]['ref_path']},init_path:{mutated_dict[k]['init_path']},saved_path:{temp_path},"
                                f"pred_label:{pred_label[k]},true_label:{temp_label},"
                                f"from_seed_path:{mutated_dict[k]['from_seed_path']},mutated_method:{mutated_dict[k]['mutated_method']},"
                                f"pred_res:{temp_pre_res},diff_path:{temp_diff_path}\n"
                            )
                            f.write(sss)
                        f.close()
                        ccc += 1
            # write a txt to store ASR
            with open(f"{self.project}/attack_success_rate.txt", "w") as f:
                asr = self.attack_success / self.attack_total
                f.write(
                    f"attack_total:{self.attack_total},attack_success:{self.attack_success},ASR:{asr}"
                )
            f.close()
            gain_indx = self.isCoverageGain(o_img=temp_seeds, m_lst=mutated_lst)
            for indx in gain_indx:
                try:
                    bat_indx, k_indx = divmod(indx, self.k_times)
                    ttt_m_img_info = mutated_lst[bat_indx][k_indx]
                    new_path = f"{self.project}/saved/{ccc}.png"
                    cv2.imwrite(new_path, ttt_m_img_info["img"])
                    self.logger.add_log(s=f"the new seed would be stored as {new_path}")
                    new_state = ttt_m_img_info["state"]
                    new_ref_path = ttt_m_img_info["ref_path"]
                    new_init_path = ttt_m_img_info["init_path"]
                    new_label = ttt_m_img_info["label"]
                    from_seed = ttt_m_img_info["from_seed_path"]
                    new_m_method = ttt_m_img_info["mutated_method"]
                    self.seed_selection.add_seed(
                        init_seed=new_init_path,
                        ref_path=new_ref_path,
                        state=new_state,
                        label=new_label,
                        path=new_path,
                    )
                    with open(f"{self.project}/new_seed_info.txt", "a") as f:
                        s = (
                            f"init_seed:{new_init_path},ref_path:{new_ref_path},"
                            f"label:{new_label},path:{new_path},from_seed_path:{from_seed},"
                            f"mutated_method:{new_m_method}\n"
                        )
                        f.write(s)
                    f.close()
                    ccc += 1
                except Exception:
                    print(bat_indx, k_indx, gain_indx)
        #


if __name__ == "__main__":
    yaml_path = "hyps/hyps_v16_ifgsm-ns.yaml"
    meta_params, criteria_params = decode_yaml(yaml_path)
    deephunter = DeepHuner(
        img_dir="./data/train_part",
        output_dir="./useless",
        model_path="./models/v16/tsr_classifier_model.h5",
        # criteria=['NC'],
        criteria=["NeuronSensitivity"],
        criteria_params=criteria_params,
        p_min=0.7,
        r=20,
        k_times=5,
        try_num=30,
        max_iter=500,
        alpha=0.8,
        beta=0.8,
        batch_size=16,
        meta_params=meta_params,
        project="test-demo-fixed-all-cate-ifgsm-NS",
    )
    deephunter.run()
