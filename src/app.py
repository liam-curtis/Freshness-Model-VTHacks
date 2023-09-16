import sys
sys.path.append('srv/freshnessmodel/src')
import utils
import cnn

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor, Lambda, Compose

# Download training data from open datasets.
training_data = # ...

# Download test data from open datasets.
test_data = # ...

batch_size = 64
train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)

# Display sample data
utils.display_sample_data(test_data)

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using {} device".format(device))

cnnmodel = cnn.CNNModel().to(device)
print(cnnmodel)

loss_fn = utils.get_loss_fn()
learning_rate = 1e-3
optimizer = utils.get_optimizer(model, learning_rate)

epochs = 15
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    cnn.train(train_dataloader, cnnmodel, loss_fn, optimizer)
    cnn.test(test_dataloader, cnnmodel)
print("Done!")

utils.save_model(cnnmodel, "/srv/freshnessmodel/cnn.pth")

# cnnmodel = cnn.CNNModel()
# utils.load_model(cnnmodel, "/srv/freshnessmodel/cnn.pth")
