import torch
import matplotlib.pyplot as plt
from torch import nn

def display_sample_data(test_data):
    figure = plt.figure(figsize=(10, 8))
    cols, rows = 5, 5
    for i in range(1, cols * rows + 1):
        idx = torch.randint(len(test_data), size=(1,)).item()
        img, label = test_data[idx]
        figure.add_subplot(rows, cols, i)
        plt.title(label)
        plt.axis("off")
        plt.imshow(img.squeeze(), cmap="gray")
    plt.show()

def save_model(model, path):
    torch.save(model.state_dict(), path)
    print(f"Saved PyTorch Model State to {path}")

def load_model(model, path):
    model.load_state_dict(torch.load(path))

def get_loss_fn():
    return nn.CrossEntropyLoss()

def get_optimizer(model, learning_rate=1e-3):
    return torch.optim.SGD(model.parameters(), lr=learning_rate)
