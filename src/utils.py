import torch
import matplotlib.pyplot as plt
from torch import nn
from torch.utils.data import DataLoader #
from torchvision import datasets #
from torchvision.transforms import ToTensor, Lambda, Compose #
import sys
sys.path.append('srv/freshnessmodel/Freshness-Model-VTHacks/src')
import cnn

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

def get_variable_name(variable, local_vars):
    return [name for name, value in local_vars.items() if value is variable][0]
    
def save_model(model):
    model_name = get_variable_name(model, locals())
    path = f"/srv/freshnessmodel/{model_name}.pth"
    torch.save(model.state_dict(), path)
    print(f"Saved PyTorch Model State to {path}")

def load_model(model, path):
    model.load_state_dict(torch.load(path))

def get_loss_fn():
    return nn.CrossEntropyLoss()

def get_optimizer(model, learning_rate=1e-3):
    return torch.optim.SGD(model.parameters(), lr=learning_rate)

def train_and_evaluate_cnn():
    # Download training data from open datasets.
    training_data = datasets.FashionMNIST(
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
    )

    # Download test data from open datasets.
    test_data = datasets.FashionMNIST(
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
    )

    batch_size = 64
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using {} device".format(device))

    model = cnn.CNNModel().to(device)
    print(model)

    loss_fn = get_loss_fn()
    learning_rate = 1e-3
    optimizer = get_optimizer(model, learning_rate)

    epochs = 15
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        cnn.train(train_dataloader, model, loss_fn, optimizer)
        cnn.test(test_dataloader, model)
    print("Done!")

    model_name = get_variable_name(model, locals())
    path = f"/srv/freshnessmodel/{model_name}.pth"
    save_model(model)

    model = cnn.CNNModel()
    load_model(model, path)

    return model
