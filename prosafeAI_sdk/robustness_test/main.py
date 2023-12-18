# -*- coding: utf-8 -*-
"""
@Time ： 14/2/2023 2:46 pm
@Auth ： Jingrui Han
@File ：main.py
@IDE ：PyCharm
@Motto: ProsafeAI (AI Hub China)
"""
import os
import time

import cv2
import numpy as np
from prosafeAI_sdk.robustness_test.criteria.criteria_strategy import CriteriaStrategy
from prosafeAI_sdk.robustness_test.mutation.mutation_strategy import MutationStrategy
from prosafeAI_sdk.robustness_test.seed_selection.seeds import SeedSelection
from prosafeAI_sdk.robustness_test.lib.logger import Logger
from prosafeAI_sdk.robustness_test.model.model import MyModel
from prosafeAI_sdk.robustness_test.utils.others import (
    create_folder,
    compare_res,
    convert_dimension,
    decode_res,
    decode_yaml,
    torch_process,
    keras_process,
)

np.set_printoptions(precision=10, suppress=True)


class TestingFramework(object):
    def __init__(
        self,
        img_dir,  # the dir path of images
        dataset_format,  # the format of dataset, it could be one of [classification, yolo, or something else]
        model_path,  # the path of model
        device,  # which device would be used; cpu or 1 or 2 or 3 ....; only one!!!!!!!
        dl_frame,  # which deeplearning framework of the model: torch or keras
        task_type,  # classification of detection, currently support classification
        criteria,  # which criteria would be the guider
        criteria_params,  # the parameters of criteria
        p_min,  # the minimal probability of a seed been sampled, if applied probability based sampling method
        r,  # declare rate of probability
        k_times,  # the number of mutators of one seed
        try_num,  # the maximum number of time of mutating a seed
        max_iter,  # the number of time of iteration
        alpha,  # alpha
        beta,  # beta
        meta_params,  # the params of mutation strategy
        project,  # the project name, the output would be stored there
        batch_size=1,  # batch size
    ):
        # hyperparams init
        self.img_dir = img_dir
        self.dataset_format = dataset_format
        self.model_path = model_path
        self.device = device
        self.dl_frame = dl_frame
        self.task_type = task_type
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
        self.seed_selection = SeedSelection(
            img_dir=self.img_dir, p_min=self.p_min, r=self.r, project=project
        )

        # init model
        self.model = MyModel(
            model_path=self.model_path, device=self.device, dl_frame=self.dl_frame
        )
        # renew the device
        self.device = self.model.device

        # init mutation strategy
        self.fuzzer = MutationStrategy(
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
            criteria=self.criteria,
            model=self.model,
            params=self.criteria_params,
            dl_frame=self.dl_frame,
            batch_size=self.batch_size,
            device=self.device,
        )

        # init logger
        self.logger = Logger(log_name=project, log_path=f"{project}/Mylog.log")

        # init data preprocessor
        self.data_processor = self.create_data_preprocessor()[self.dl_frame]

    def cal_asr(self):
        pass

    def create_data_preprocessor(self):
        processor_dict = {"torch": torch_process, "keras": keras_process}
        return processor_dict

    def run(self):
        ccc = 0
        self.logger.add_log(f"start testing for {self.max_iter}")
        for iter in range(self.max_iter):
            # record ASR
            # self.attack_total += self.k_times * self.batch_size
            start_time = time.time()
            print("=" * 10, f"iteration-{iter}", "=" * 10)
            # extract seed, temp_Seed_classes is a list with multi-classes
            temp_seed_classes = self.seed_selection.get_seed(num=self.batch_size)
            # extract original images <-- temp_seeds
            temp_o_imgs = []
            temp_o_labels = []
            for item in temp_seed_classes:
                temp_o_imgs.append(cv2.imread(item.path))
                temp_o_labels.append(item.label)
            temp_o_imgs = np.array(temp_o_imgs)
            # start mutation
            print("start mutating images")
            mutated_lst = []
            for i in range(len(temp_seed_classes)):
                temp_seed = temp_o_imgs[i]
                temp_seed_class = temp_seed_classes[i]
                temp_mutated_dict = self.fuzzer.mutate_one(
                    cur_seed=temp_seed_class, img=temp_seed
                )
                mutated_lst.append(temp_mutated_dict)
            print("mutation over")
            # renew the parameter of seeds
            self.seed_selection.update_seed(m_times=1)
            # 抽取所有的mutated images并按照顺序排列，从上到下，从左到右
            # extract all the mutated images and sort them following the order: top -> bottom, left -> right
            temp_mutated_images = convert_dimension(
                input_data=mutated_lst,
                type="reduce",
                batch_size=self.batch_size,
                k=self.k_times,
            )
            # 初始化二维数组记录记录mutated images的预测结果 (暂时不用)
            # 一次预测出所有的mutated images的结果, 然后conver至三维
            # predict all the mutated images and increase the dimension to 3D
            mutation_preds_ori = self.model.inference(
                data=self.data_processor(temp_mutated_images[:, :, :, ::-1])
            )
            mutation_preds = decode_res(
                res=mutation_preds_ori, task_type=self.task_type
            )
            # 将原始seed的正确结果和mutated images的预测结果传入compare_res()
            # try:
            t_or_f = compare_res(
                seeds_labels=temp_o_labels,
                mutation_preds=mutation_preds,
                task_type=self.task_type,
                batch_size=self.batch_size,
                k=self.k_times,
            )
            # except:
            # continue
            # 使用criteria测试seeds和mutated seeds 并得到 大小比较矩阵
            # l_or_s = self.criteria_calculator.test_once(original_seeds=temp_o_imgs, mutators=temp_mutated_images)
            l_or_s = self.criteria_calculator.test_once(
                original_seeds=self.data_processor(temp_o_imgs[:, :, :, ::-1]),
                mutators=self.data_processor(temp_mutated_images[:, :, :, ::-1]),
            )
            # 对错矩阵和大小矩阵进行或运算
            temp_final_array = t_or_f * l_or_s
            # final矩阵中的T位置生成新seed
            # 预测矩阵中的F位置储存
            # save_seed, save_fail = post_process(comp_array=t_or_f,
            #                                     mutation_preds=mutation_preds,
            #                                     final_array=temp_final_array,
            #                                     mutation_lst=mutated_lst)
            # flatten t_or_f and l_or_s
            t_or_f, l_or_s, temp_final_array = (
                t_or_f.flatten(),
                l_or_s.flatten(),
                temp_final_array.flatten(),
            )
            # renew asr related parameters
            self.attack_total += self.k_times * self.batch_size
            self.attack_success += len([iii for iii in t_or_f if not iii])
            # process fail_test_set
            for j in range(len(t_or_f)):
                pred_label = mutation_preds[j]
                row, col = divmod(j, self.k_times)
                tmp_m_dict = mutated_lst[row][col]
                tmp_m_dict["pred_label"] = pred_label
                temp_path = "no_saved"
                if not t_or_f[j]:
                    if not os.path.exists(
                        f'{self.project}/fail_test/{tmp_m_dict["label"]}'
                    ):
                        os.makedirs(f'{self.project}/fail_test/{tmp_m_dict["label"]}')
                    cv2.imwrite(
                        f"{self.project}/fail_test/{tmp_m_dict['label']}/fail-sample_{ccc}.png",
                        tmp_m_dict["img"],
                    )
                    # ======logger========#
                    temp_path = f"{self.project}/fail_test_samples/{tmp_m_dict['label']}/fail-sample_{ccc}.png"
                    temp_label = tmp_m_dict["label"]
                    self.logger.add_log(
                        s=f"for {temp_path}: its label should be {temp_label}, "
                        f"but got {pred_label}, it would be stored in {temp_path}"
                    )
                    with open(f"{self.project}/fail_test_info.txt", "a") as f:
                        sss = (
                            ",".join(
                                [
                                    f"{key}:{val}"
                                    for (key, val) in tmp_m_dict.items()
                                    if key != "img"
                                ]
                            )
                            + ","
                            + f"saved_path:{temp_path}"
                            + "\n"
                        )
                        f.write(sss)
                    f.close()
                    ccc += 1
                elif temp_final_array[j]:
                    new_path = f"{self.project}/saved_seeds/{ccc}.png"
                    temp_path = new_path
                    if not os.path.exists(f"{self.project}/saved_seeds/"):
                        os.makedirs(f"{self.project}/saved_seeds/")
                    cv2.imwrite(new_path, tmp_m_dict["img"])
                    self.logger.add_log(s=f"the new seed would be stored as {new_path}")
                    new_state = tmp_m_dict["state"]
                    new_ref_path = tmp_m_dict["ref_path"]
                    new_init_path = tmp_m_dict["init_path"]
                    new_label = tmp_m_dict["label"]
                    # from_seed = tmp_m_dict["from_seed_path"]
                    # new_m_method = tmp_m_dict["mutated_method"]
                    self.seed_selection.add_seed(
                        init_seed=new_init_path,
                        ref_path=new_ref_path,
                        state=new_state,
                        label=new_label,
                        path=new_path,
                    )
                    with open(f"{self.project}/new_seed_info.txt", "a") as f:
                        s = (
                            ",".join(
                                [
                                    f"{key}:{val}"
                                    for (key, val) in tmp_m_dict.items()
                                    if key != "img"
                                ]
                            )
                            + ","
                            + f"saved_path:{temp_path}"
                            + "\n"
                        )
                        f.write(s)
                    f.close()
                    ccc += 1

                # 记录所有结果，用于生成不同odd的分析
                with open(f"{self.project}/all_records.txt", "a") as f:
                    s = (
                        ",".join(
                            [
                                f"{key}:{val}"
                                for (key, val) in tmp_m_dict.items()
                                if key != "img"
                            ]
                        )
                        + ","
                        + f"saved_path:{temp_path}"
                        + "\n"
                    )
                    f.write(s)
                f.close()
                ccc += 1
            # 输出asr相关记录
            with open(f"{self.project}/attack_success_rate.txt", "w") as f:
                s = (
                    f"attack_total:{self.attack_total},attack_success:{self.attack_success},"
                    f"ASR:{round(self.attack_success/self.attack_total, 5)}\n"
                )
                f.write(s)
                f.close()
            with open(f"{self.project}/attack_success_rate_sim.txt", "a") as f:
                s = (
                    f"iter:{iter},attack_total:{self.attack_total},attack_success:{self.attack_success},"
                    f"ASR:{round(self.attack_success/self.attack_total, 5)}\n"
                )
                f.write(s)
                f.close()
            yield {
                "criteria": self.criteria[0],
                "iteration": iter,
                "fail_test_num": self.attack_success,
                "total_mutator": self.attack_total,
                "ASR": round(self.attack_success / self.attack_total, 4),
                "process_rate": round(iter / self.max_iter, 4),
                "running_time": round(time.time() - start_time, 4),
                "ETA": round((time.time() - start_time) * (self.max_iter - iter), 4),
            }


if __name__ == "__main__":
    yaml_path = "../../hyps/hyps_all.yaml"
    meta_params, criteria_params, running_params = decode_yaml(yaml_path)
    # deephunter = TestingFramework(img_dir='./data/fewer',
    #                        model_path='./v14/tsr_classifier_model.h5',
    #                        # model_path='v14/unaug-v1_resnet50_model.pth',
    #                        criteria=['TopK'],
    #                        criteria_params=criteria_params,
    #                        p_min=0.7,
    #                        r=20,
    #                        k_times=5,
    #                        try_num=30,
    #                        max_iter=500,
    #                        alpha=0.8,
    #                        beta=0.8,
    #                        batch_size=2,
    #                        meta_params=meta_params,
    #                        project='test_all_cate_latest',
    #                        dataset_format='classification',
    #                        device='cpu',
    #                        dl_frame='keras',
    #                        # dl_frame='torch',
    #                        task_type='classification'
    #                        )
    deephunter = TestingFramework(**running_params)
    deephunter.run()
