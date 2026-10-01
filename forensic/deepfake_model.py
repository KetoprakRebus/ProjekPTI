import os

import torch
import torch.nn as nn
import torchvision.transforms as transforms

from PIL import Image


# =========================================
# PATH MODEL
# =========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "deepfake_model.pth"
)


# =========================================
# CNN
# Harus sama dengan train.py
# =========================================

class CNN(nn.Module):

    def __init__(self):

        super().__init__()

        self.net = nn.Sequential(

            nn.Conv2d(
                3,
                32,
                3
            ),

            nn.ReLU(),

            nn.MaxPool2d(2),

            nn.Conv2d(
                32,
                64,
                3
            ),

            nn.ReLU(),

            nn.MaxPool2d(2),

            nn.Flatten(),

            nn.Linear(
                64 * 54 * 54,
                128
            ),

            nn.ReLU(),

            nn.Linear(
                128,
                2
            )

        )


    def forward(self, x):

        return self.net(x)


# =========================================
# DEVICE
# =========================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else
    "cpu"
)


# =========================================
# PREPROCESS
# Harus sama dengan training
# =========================================

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor()

])


# =========================================
# LOAD MODEL SEKALI
# =========================================

def load_model():

    if not os.path.exists(
        MODEL_PATH
    ):

        print(
            "Model tidak ditemukan:",
            MODEL_PATH
        )

        return None


    model = CNN()


    state_dict = torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )


    model.load_state_dict(
        state_dict
    )


    model.to(
        DEVICE
    )


    model.eval()


    print(
        "Model berhasil dimuat:",
        MODEL_PATH
    )


    return model


MODEL = load_model()


# =========================================
# PREDIKSI SATU FRAME
# =========================================

def predict_frame(frame):

    if MODEL is None:

        return None


    # OpenCV = BGR
    # PIL = RGB

    rgb = frame[
        :,
        :,
        ::-1
    ]


    image = Image.fromarray(
        rgb
    )


    image = transform(
        image
    )


    image = image.unsqueeze(
        0
    )


    image = image.to(
        DEVICE
    )


    with torch.no_grad():

        output = MODEL(
            image
        )


        probabilities = torch.softmax(
            output,
            dim=1
        )


    # ImageFolder mengurutkan class alphabetically:
    #
    # fake = 0
    # real = 1

    fake_probability = (
        probabilities[0][0].item()
        * 100
    )


    real_probability = (
        probabilities[0][1].item()
        * 100
    )


    return {

        "fake":
        fake_probability,

        "real":
        real_probability

    }