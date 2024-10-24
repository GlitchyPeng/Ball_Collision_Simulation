import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, random_split
import matplotlib.pyplot as plt
import cv2

# Define the DoubleConv and UNet classes
class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()
        self.double_conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.double_conv(x)

class UNet(nn.Module):
    def __init__(self, n_channels, n_classes):
        super(UNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes

        # Encoder part
        self.conv1 = DoubleConv(n_channels, 64)
        self.conv2 = DoubleConv(64, 128)
        self.conv3 = DoubleConv(128, 256)
        self.conv4 = DoubleConv(256, 512)
        self.conv5 = DoubleConv(512, 1024)

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Decoder part
        self.upconv4 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.conv4d = DoubleConv(1024, 512)

        self.upconv3 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.conv3d = DoubleConv(512, 256)

        self.upconv2 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.conv2d = DoubleConv(256, 128)

        self.upconv1 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.conv1d = DoubleConv(128, 64)

        self.out_conv = nn.Conv2d(64, n_classes, kernel_size=1)

    def forward(self, x):
        # Encoding path
        c1 = self.conv1(x)
        p1 = self.pool(c1)

        c2 = self.conv2(p1)
        p2 = self.pool(c2)

        c3 = self.conv3(p2)
        p3 = self.pool(c3)

        c4 = self.conv4(p3)
        p4 = self.pool(c4)

        c5 = self.conv5(p4)

        # Decoding path
        u4 = self.upconv4(c5)
        c4 = self.crop_tensor(c4, u4)
        u4 = torch.cat([u4, c4], dim=1)
        c4d = self.conv4d(u4)

        u3 = self.upconv3(c4d)
        c3 = self.crop_tensor(c3, u3)
        u3 = torch.cat([u3, c3], dim=1)
        c3d = self.conv3d(u3)

        u2 = self.upconv2(c3d)
        c2 = self.crop_tensor(c2, u2)
        u2 = torch.cat([u2, c2], dim=1)
        c2d = self.conv2d(u2)

        u1 = self.upconv1(c2d)
        c1 = self.crop_tensor(c1, u1)
        u1 = torch.cat([u1, c1], dim=1)
        c1d = self.conv1d(u1)

        out = self.out_conv(c1d)

        # Ensure output size is 56x56
        out = F.interpolate(out, size=(56, 56), mode='bilinear', align_corners=False)
        return out

    def crop_tensor(self, encoder_tensor, decoder_tensor):
        """
        Crop the encoder tensor to match the size of the decoder tensor.
        """
        _, _, H, W = decoder_tensor.size()
        encoder_tensor = F.interpolate(encoder_tensor, size=(H, W), mode='bilinear', align_corners=False)
        return encoder_tensor

import cv2

class CustomDataset(Dataset):
    def __init__(self, file_paths, truth_paths, indices, target_size=(56, 56)):
        self.file_paths = file_paths
        self.truth_paths = truth_paths
        self.indices = indices
        self.target_size = target_size

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, idx):
        index = self.indices[idx]
        file_paths_for_index = [fp.format(index=index) for fp in self.file_paths]

        inputs = []
        for input_path in file_paths_for_index:
            input_image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
            if input_image is None:
                raise ValueError(f"Image file {input_path} could not be opened by OpenCV.")

            input_image = cv2.resize(input_image, self.target_size)  # 调整图像大小
            input_data = np.array(input_image)

            input_data = input_data / np.max(input_data)  # 归一化

            input_data = torch.tensor(input_data, dtype=torch.float32)
            inputs.append(input_data)
        inputs = torch.stack(inputs, dim=0)

        # 读取与输入对应的掩码文件（也是 TIFF 文件）
        truth_path = self.truth_paths.format(index=index)
        truth_image = cv2.imread(truth_path, cv2.IMREAD_UNCHANGED)
        if truth_image is None:
            raise ValueError(f"Truth file {truth_path} could not be opened by OpenCV.")
        
        truth_image = cv2.resize(truth_image, self.target_size)  # 调整掩码大小
        truth_data = np.array(truth_image)
        
        truth_data = truth_data / np.max(truth_data)

        truth_data = torch.tensor(truth_data, dtype=torch.float32)

        return {'image': inputs, 'mask': truth_data}


def train_model(model, train_loader, criterion, optimizer, device):
    model.train()
    epoch_loss = 0
    for batch in train_loader:
        images = batch['image'].to(device)
        masks = batch['mask'].to(device)

        masks = masks.unsqueeze(1)

        optimizer.zero_grad()
        predictions = model(images)
        loss = criterion(predictions, masks)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
    return epoch_loss / len(train_loader)

def validate_model(model, val_loader, criterion, device):
    model.eval()
    val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            images = batch['image'].to(device)
            masks = batch['mask'].to(device)
            masks = masks.unsqueeze(1)
            predictions = model(images)
            loss = criterion(predictions, masks)
            val_loss += loss.item()
    return val_loss / len(val_loader)

def save_predictions(model, val_loader, device):
    model.eval()
    all_predictions = []
    with torch.no_grad():
        for batch in val_loader:
            images = batch['image'].to(device)
            predictions = model(images)
            predictions = torch.sigmoid(predictions).cpu().numpy()
            all_predictions.append(predictions)
    all_predictions = np.concatenate(all_predictions, axis=0)
    np.savetxt('Y_pred_unet.csv', all_predictions.reshape(-1), delimiter=',')
    print('Predictions saved to Y_pred_unet.csv')
    return all_predictions

def visualize_predictions(dataset, all_predictions, num_images=5):
    for i in range(num_images):
        plt.figure()
        plt.subplot(1, 2, 1)
        plt.title('Truth')
        plt.imshow(dataset[i]['mask'].numpy(), cmap='gray')
        plt.subplot(1, 2, 2)
        plt.title('Prediction')
        plt.imshow(all_predictions[i][0], cmap='gray')
        plt.show()

def main():
    file_paths = [
        '/Users/lexiezhou/Desktop/2/Gauss_S1.00_NL0.30_B0.50/emcal_{index}.tiff',
        '/Users/lexiezhou/Desktop/2/Gauss_S1.00_NL0.30_B0.50/trkp_{index}.tiff',
        '/Users/lexiezhou/Desktop/2/Gauss_S1.00_NL0.30_B0.50/trkn_{index}.tiff',
        '/Users/lexiezhou/Desktop/2/Gauss_S1.00_NL0.30_B0.50/hcal_{index}.tiff'
    ]
    
    # 假设掩码也存储为 TIFF 文件
    truth_paths = '/Users/lexiezhou/Desktop/2/Gauss_S1.00_NL0.30_B0.50/truth_{index}.tiff'
    indices = range(0, 9999)

    dataset = CustomDataset(file_paths, truth_paths, indices)

    n_val = int(0.1 * len(dataset))
    n_train = len(dataset) - n_val
    train_set, val_set = random_split(dataset, [n_train, n_val], generator=torch.Generator().manual_seed(0))

    train_loader = DataLoader(train_set, batch_size=4, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_set, batch_size=4, shuffle=False, num_workers=0, pin_memory=True)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = UNet(n_channels=4, n_classes=1)
    model.to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-4)  # 添加 weight_decay 正则化
    scheduler = lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5, verbose=True)

    n_epochs = 50  # 增加训练轮数
    for epoch in range(n_epochs):
        train_loss = train_model(model, train_loader, criterion, optimizer, device)
        val_loss = validate_model(model, val_loader, criterion, device)
        
        print(f'Epoch {epoch + 1}/{n_epochs}, Loss: {train_loss}')
        print(f'Validation Loss: {val_loss}')
        
        # Step the scheduler with the validation loss
        scheduler.step(val_loss)

    all_predictions = save_predictions(model, val_loader, device)
    visualize_predictions(dataset, all_predictions, num_images=5)

if __name__ == "__main__":
    main()
