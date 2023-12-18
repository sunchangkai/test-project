import torch
import keras
import numpy as np
import os
import tensorflow as tf
from keras import losses
import torch.nn.functional as F


class MyModel(object):
    def __init__(self, model_path, device, dl_frame="keras"):
        """
        :param model_path: model path
        :param dl_frame: torch of keras, it should be one of element in [torch, keras]
        """
        self.model_path = model_path
        self.dl_frame = dl_frame
        if device == "cpu":
            self.device = "cpu"
        else:
            self.device = device
        # load model based on the dl framework
        if dl_frame in ["keras", "Keras", "KERAS"]:
            self.device = device
            self.model = keras.models.load_model(self.model_path)
            try:
                os.environ["CUDA_VISIBLE_DEVICES"] = f"{self.device}"
            except Exception:
                raise Exception("wrong devices!!!!!")

        elif dl_frame in ["torch", "Torch", "Pytorch"]:
            if device != "cpu":
                self.device = torch.device(f"cuda:{device}")
            else:
                self.device = torch.device("cpu")
            self.model = torch.load(self.model_path, map_location="cpu").to(self.device)
            pass
        else:
            raise Exception(
                "the dl framework is not support currently, please choose one from [torch, keras]"
            )

    def inference(self, data):
        if self.dl_frame == "torch":
            self.model.eval()
            # data = torch.Tensor(data.copy().transpose(0, 3, 1, 2)).to(self.device)
            with torch.no_grad():
                tmp_res = self.model(data.to(self.device))
            tmp_res = tmp_res.cpu().detach().numpy()
            return tmp_res
        elif self.dl_frame == "keras":
            tmp_res = self.model.predict(data, verbose=False)
            # tmp_res = np.argmax(tmp_res)
            # print(tmp_res, len(tmp_res))
            return tmp_res
        elif self.dl_frame == "onnx":
            pass

    def get_gradient(self, data, y_true):
        """
        get the gradient of the model on input layer
        :param data: a numpy of image
        :param y_true: a numpy in onehot style
        :return: gradient in numpy format
        """
        if self.dl_frame == "torch":
            data = data.to(self.device)
            y_true = y_true.to(self.device)
            data.requires_grad = True
            # Forward pass the data through the model
            output = self.model(data)
            # get the index of the max log-probability
            # init_pred = output.max(1, keepdim=True)[1]
            # calculate the loss
            loss = F.nll_loss(output, y_true)
            # Zero all existing gradients
            self.model.zero_grad()
            # Calculate gradients of model in backward pass
            loss.backward()
            # Collect datagrad
            data_grad = data.grad.data.numpy()
            return data_grad

        elif self.dl_frame == "keras":
            img = data
            loss_fn = losses.CategoricalCrossentropy(from_logits=True)
            images = tf.cast(img, tf.float32)
            with tf.GradientTape() as tape:
                tape.watch(images)
                preds = self.model(images)
                # top_class = preds[:, y]
                # print(y_true, preds)
                loss_val = loss_fn(y_true, preds)
            grads = tape.gradient(loss_val, images)
            grads = grads.numpy()[0]
            return grads
        elif self.dl_frame == "onnx":
            pass

    def get_inter_output_torch(self, data, layername):
        # the necessary of this function need to be considerate serious!
        pass

    def get_inter_output_keras(self, data, layername):
        # the necessary of this function need to be considerate serious!
        pass
