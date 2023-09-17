import torch
from torch import nn

# Creates a class for the convolutional neural network inheriting from the pytorch library

# Define model - takes input as 144*144*3
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.network = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1),  # Using stride 2 to reduce dimensions
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 36x36 feature maps
            
            nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),  # Using stride 2 again
            nn.ReLU(),
            nn.MaxPool2d(2, 2),  # 9x9 feature maps
            
            nn.Flatten(),
            nn.Linear(9 * 9 * 32, 256),  # Adjusted based on the output size of the last conv layer
            nn.ReLU(),
            nn.Linear(256, 2)
        ) 
      
    def forward(self, x):
        return self.network(x)

# Makes predictions on data and uses prediction error to modify model parameters

def train(dataloader, model, loss_fn, optimizer, device):
    size = len(dataloader.dataset)
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

# Check model performance against test dataset

def test(dataloader, model, loss_fn, device):
    size = len(dataloader.dataset)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= size
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
