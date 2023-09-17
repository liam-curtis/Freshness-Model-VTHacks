import os
import cv2
from PIL import Image
import torch
from torch import nn
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import importlib.util
import matplotlib.pyplot as plt
import sys
sys.path.append('./models')
module_spec = importlib.util.spec_from_file_location("cnn", "./models/cnn.py")
cnn = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(cnn)
##import cnn

class CustomDataset(Dataset):
    def __init__(self, data):
        self.data = []
        self.categories = ['fresh', 'rotten']  # Numeric categories now
        for category, tensors in data.items():
            label = self.categories.index(category)
            for tensor in tensors:
                self.data.append((tensor, label))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

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


def get_optimizer(model, learning_rate=2e-3):
    return torch.optim.SGD(model.parameters(), lr=learning_rate)

from torch.utils.data import Dataset

        
def load_images_as_tensors(directory, base_path="."):
    # Define the transformation pipeline for the images
    transformations = transforms.Compose([
        transforms.Resize((144, 144)),  # Resize to 144x144
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
    ])

    # Fruit categories
    categories = ['freshapples', 'freshbanana', 'freshcucumber', 'freshokra', 'freshoranges', 
                  'freshpotato', 'freshtomato', 'rottenapples', 'rottenbanana', 'rottencucumber', 
                  'rottenokra', 'rottenoranges', 'rottenpotato', 'rottentomato']

    data = {'rotten': [], 'fresh': []}

    for category in categories:
        # Construct the path to the category directory
        category_dir = os.path.join(base_path, directory, category)
        
        # Iterate through each image in the category directory
        for image_name in os.listdir(category_dir):
            image_path = os.path.join(category_dir, image_name)
            
             # Read the image using PIL
            pil_image = Image.open(image_path)

            # If the image has an alpha channel (is RGBA), convert it to RGB
            if pil_image.mode == 'RGBA':
                pil_image = pil_image.convert('RGB')
            tensor_image = transformations(pil_image)
            
            # Append the tensor to the appropriate list
            if "rotten" in category:
                data['rotten'].append(tensor_image)
            else:
                data['fresh'].append(tensor_image)

    return data



def train_and_evaluate_cnn():
    # Download training data from open datasets.
    training_data = load_images_as_tensors('Train', '/srv/freshnessmodel/dataset')
    training_data = CustomDataset(training_data)

    # Download test data from open datasets.
    test_data = load_images_as_tensors('Test', '/srv/freshnessmodel/dataset')
    test_data = CustomDataset(test_data)

    batch_size = 128
    train_dataloader = DataLoader(training_data, batch_size=batch_size, shuffle=True, num_workers=12)
    test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=True, num_workers=12)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using {} device".format(device))

    model = cnn.CNNModel().to(device)
    print(model)

    loss_fn = get_loss_fn()
    learning_rate = 2e-3
    optimizer = get_optimizer(model, learning_rate)

    epochs = 15
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        cnn.train(train_dataloader, model, loss_fn, optimizer, device)
        cnn.test(test_dataloader, model, loss_fn, device)
    print("Done!")

    model_name = get_variable_name(model, locals())
    path = f"/srv/freshnessmodel/VTHacks/{model_name}.pth"
    save_model(model)

    model = cnn.CNNModel()
    load_model(model, path)

    return model
