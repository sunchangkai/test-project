import random
import numpy as np

# from seed_selection.utils import scan_imgs
from seed_selection.utils import seedsQueue, scan_imgs


class seedSelection(object):
    def __init__(self, img_dir, p_min, r, project):
        self.img_dir = img_dir
        self.seed_paths = scan_imgs(self.img_dir)
        self.p_min = p_min
        self.r = r
        self.seed_q = seedsQueue(
            seed_paths=self.seed_paths, p_min=self.p_min, r=self.r, project=project
        )
        self.current_indx = -1
        self.current_seed = None

    def get_seed(self, num: int):
        # img, indx, state = self.seed_q.get_seed()
        # self.current_indx = indx
        # return img, state
        temp_indx, temp_seed = self.seed_q.get_seed(num=num)
        self.current_indx = temp_indx
        self.current_seed = temp_seed
        return temp_seed

    def update_seed(self, m_times):
        for seed_indx in self.current_indx:
            self.seed_q.update_seed(index=seed_indx, m_time=m_times)

    def add_seed(self, path, state, init_seed, ref_path, label):
        self.seed_q.add_seed(
            path=path, state=state, init_seed=init_seed, ref_path=ref_path, label=label
        )
