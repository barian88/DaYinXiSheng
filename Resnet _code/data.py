from torch.utils.data import Dataset
import torch
from pathlib import Path
from skimage.io import imread
from skimage.color import gray2rgb
import numpy as np
import torchvision as tv
from torchvision.transforms.functional import to_pil_image
import pandas as pd
import os

train_mean = [0.59685254, 0.59685254, 0.59685254]
train_std = [0.16043035, 0.16043035, 0.16043035]

class ChallengeDataset(Dataset):
    # TODO implement the Dataset class according to the description
    def __init__(self, dataframe, mode):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            mode (string): 'train' or 'val' indicating the mode of dataset usage.
        """

        self.mode = mode
        self.data_frame = dataframe

        # Define the transformations
        self.transform = tv.transforms.Compose([
            to_pil_image,
            tv.transforms.ToTensor(),
            tv.transforms.Normalize(mean=[0.59685254, 0.59685254, 0.59685254],
                         std=[0.16043035, 0.16043035, 0.16043035])
        ])

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        # Get the static path and correct it if it contains extra characters like ';0;0'
        img_name = self.data_frame.iloc[idx, 0]
        img_name = img_name.split(';')[0]  # Assuming path and other data are separated by a semicolon

        # Ensure the path is complete
        base_dir = r'E:\Projects\src_to_implement'
        full_path = os.path.join(base_dir, img_name)

        image = imread(full_path)
        image = gray2rgb(image) if image.ndim == 2 else image  # Convert grayscale to RGB if necessary

        label = self.data_frame.iloc[idx, 1:]

        label = torch.tensor(label, dtype=torch.float32)

        # Apply transformations
        image = self.transform(image)

        return image, label
