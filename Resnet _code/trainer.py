import os

import torch as t
import numpy as np
from sklearn.metrics import f1_score
from tqdm.autonotebook import tqdm


class Trainer:

    def __init__(self,
                 model,                        # Model to be trained.
                 crit,                         # Loss function
                 optim=None,                   # Optimizer
                 train_dl=None,                # Training data set
                 val_test_dl=None,             # Validation (or test) data set
                 cuda=True,                    # Whether to use the GPU
                 early_stopping_patience=-1):  # The patience for early stopping
        self._model = model
        self._crit = crit
        self._optim = optim
        self._train_dl = train_dl
        self._val_test_dl = val_test_dl
        self._cuda = cuda

        self._early_stopping_patience = early_stopping_patience

        if cuda:
            self._model = model.cuda()
            self._crit = crit.cuda()
            
    def save_checkpoint(self, epoch):
        checkpoint_dir = 'checkpoints'
        os.makedirs(checkpoint_dir, exist_ok=True)  # Ensure directory exists
        checkpoint_path = f'{checkpoint_dir}/checkpoint_{epoch:03d}.ckp'
        t.save({'state_dict': self._model.state_dict()}, checkpoint_path)

    def restore_checkpoint(self, epoch_n):
        checkpoint_path = f'checkpoints/checkpoint_{epoch_n:03d}.ckp'
        ckp = t.load(checkpoint_path, 'cuda' if self._cuda else 'cpu')
        self._model.load_state_dict(ckp['state_dict'])
        
    def save_onnx(self, fn):
        self._model.cpu()
        self._model.eval()
        x = t.randn(1, 3, 300, 300, requires_grad=True)
        y = self._model(x)
        t.onnx.export(self._model,                 # model being run
                      x,                          # model input (or a tuple for multiple inputs)
                      fn,                         # where to save the model (can be a file or file-like object)
                      export_params=True,         # store the trained parameter weights inside the model file
                      opset_version=10,           # the ONNX version to export the model to
                      do_constant_folding=True,   # whether to execute constant folding for optimization
                      input_names=['input'],      # the model's input names
                      output_names=['output'],    # the model's output names
                      dynamic_axes={'input': {0: 'batch_size'},    # variable length axes
                                    'output': {0: 'batch_size'}})
            
    def train_step(self, x, y):
        # perform following steps:
        # -reset the gradients. By default, PyTorch accumulates (sums up) gradients when backward() is called. This behavior is not required here, so you need to ensure that all the gradients are zero before calling the backward.
        # -propagate through the network
        # -calculate the loss
        # -compute gradient by backward propagation
        # -update weights
        # -return the loss
        #TODO
        self._model.train()  # Set model to training mode
        self._optim.zero_grad()  # Reset gradients
        outputs = self._model(x)  # Forward pass
        loss = self._crit(outputs, y)  # Compute loss
        loss.backward()  # Backpropagation
        self._optim.step()  # Update weights
        return loss.item()  # Return loss value


    def val_test_step(self, x, y):
        
        # predict
        # propagate through the network and calculate the loss and predictions
        # return the loss and the predictions
        #TODO
        self._model.eval()  # Set model to evaluation mode
        with t.no_grad():  # Disable gradient computation
            outputs = self._model(x)
            loss = self._crit(outputs, y)
            #preds = outputs.argmax(dim=1)  # Assuming classification task
            preds = (outputs > 0.5).int()
        return loss.item(), preds
        
    def train_epoch(self):
        # set training mode
        # iterate through the training set
        # transfer the batch to "cuda()" -> the gpu if a gpu is given
        # perform a training step
        # calculate the average loss for the epoch and return it
        #TODO
        total_loss = 0
        for x, y in self._train_dl:  # Loop over each batch
            if self._cuda:
                x, y = x.cuda(), y.cuda()  # Move data to GPU if available
            loss = self.train_step(x, y)
            total_loss += loss
        return total_loss / len(self._train_dl)
    
    def val_test(self):
        # set eval mode. Some layers have different behaviors during training and testing (for example: Dropout, BatchNorm, etc.). To handle those properly, you'd want to call model.eval()
        # disable gradient computation. Since you don't need to update the weights during testing, gradients aren't required anymore. 
        # iterate through the validation set
        # transfer the batch to the gpu if given
        # perform a validation step
        # save the predictions and the labels for each batch
        # calculate the average loss and average metrics of your choice. You might want to calculate these metrics in designated functions
        # return the loss and print the calculated metrics
        #TODO
        self._model.eval()  # Ensure the model is in eval mode
        total_loss = 0
        all_preds = []
        all_y = []

        with t.no_grad():
            for x, y in self._val_test_dl:
                if self._cuda:
                    x = x.cuda()
                    y = y.cuda()

                outputs = self._model(x)
                loss = self._crit(outputs, y)
                total_loss += loss.item()

                preds = (outputs > 0.5).int() # Get the predicted classes
                all_preds.append(preds)
                #all_y.append(y.argmax(dim=1) if y.ndim > 1 else y)  # Ensure y is not one-hot encoded
                all_y.append(y)

        all_preds = t.cat(all_preds).cpu()
        all_y = t.cat(all_y).cpu()
        avg_loss = total_loss / len(self._val_test_dl)

        f1 = f1_score(all_y.numpy(), all_preds.numpy(), average='macro')

        print(f"Validation Loss: {avg_loss:.4f}, F1 Score: {f1:.4f}")
        return avg_loss, f1
        
    
    def fit(self, epochs=-1):
        assert self._early_stopping_patience > 0 or epochs > 0
        # create a list for the train and validation losses, and create a counter for the epoch 
        #TODO
        train_losses = []
        val_losses = []
        best_val_loss = np.inf
        epochs_no_improve = 0  # Counter to track non-improving epochs
        epoch = 0
        current_epoch = 0
        
        while True:
            # 进行一次完整的训练周期
            train_loss = self.train_epoch()
            train_losses.append(train_loss)

            # 在验证集上评估当前模型
            val_loss, val_metrics = self.val_test()
            val_losses.append(val_loss)

            # 如果当前验证损失优于之前的最佳损失，则保存模型
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_checkpoint(current_epoch)
                no_improve_epochs = 0  # 重置无改进的周期计数
            else:
                no_improve_epochs += 1

            # 输出当前周期的结果
            print(
                f'Epoch {current_epoch + 1}, Training Loss: {train_loss:.4f}, Validation Loss: {val_loss:.4f}, Metrics: {val_metrics}')

            # 根据早停机制检查是否终止训练
            if self._early_stopping_patience > 0 and no_improve_epochs >= self._early_stopping_patience:
                print("Early stopping triggered.")
                break

            # 根据指定的最大周期数检查是否终止训练
            current_epoch += 1
            if epochs > 0 and current_epoch >= epochs:
                break

        return train_losses, val_losses
            # stop by epoch number
            # train for a epoch and then calculate the loss and metrics on the validation set
            # append the losses to the respective lists
            # use the save_checkpoint function to save the model (can be restricted to epochs with improvement)
            # check whether early stopping should be performed using the early stopping criterion and stop if so
            # return the losses for both training and validation
            #TODO

                    
        
        
        
