import torch as t
from torch.utils.data import DataLoader
from torch.optim import lr_scheduler

from data import ChallengeDataset
from trainer import Trainer
import model
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

# Load data and split it
data_df = pd.read_csv('data.csv', delimiter=';')
train_df, val_df = train_test_split(data_df, test_size=0.2, random_state=42)

# Setup data loaders
train_dataset = ChallengeDataset(dataframe=train_df, mode='train')
val_dataset = ChallengeDataset(dataframe=val_df, mode='val')

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Instantiate the model
net = model.ResNet().cuda()

# Setup loss function for multi-label classification
criterion = t.nn.BCELoss()

# Setup optimizer
optimizer = t.optim.AdamW(net.parameters(), lr=0.003, weight_decay=1e-5)

# Setup learning rate scheduler
scheduler = lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# Create a trainer object
trainer = Trainer(
    model=net,
    crit=criterion,
    optim=optimizer,
    train_dl=train_loader,
    val_test_dl=val_loader,
    cuda=True,  # Ensure your environment supports CUDA
    early_stopping_patience=10
)

# Start training
res = trainer.fit(epochs=20)

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(np.arange(len(res[0])), res[0], label='Train Loss')
plt.plot(np.arange(len(res[1])), res[1], label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.yscale('log')
plt.legend()
plt.title('Training and Validation Losses')
plt.savefig('losses.png')