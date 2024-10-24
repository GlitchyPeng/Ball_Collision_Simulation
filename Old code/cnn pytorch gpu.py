import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

# 设置设备
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# 定义 CNN 模型
class MyCNN(nn.Module):
    def __init__(self, input_size):
        super(MyCNN, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
        self.conv3 = nn.Conv1d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool1d(kernel_size=2)
        self.dropout = nn.Dropout(p=0.5)

        # Adjusted fully connected layer input size calculation
        self.fc_input_size = (input_size // 4) * 256  # Reduce pooling to avoid zero dimensions
        self.fc1 = nn.Linear(self.fc_input_size, 128)
        self.fc2 = nn.Linear(128, 1)  # Output layer

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv3(x)
        x = self.relu(x)
        # Remove the final pooling layer to prevent zero-sized output
        # x = self.pool(x)  # Commented out
        x = self.dropout(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# Load data while skipping the first row
truth_data = pd.read_csv('0.5_truth_flattened.csv', header=None, skiprows=1).values
trkn_data = pd.read_csv('0.5_trkn_flattened.csv', header=None, skiprows=1).values
trkp_data = pd.read_csv('0.5_trkp_flattened.csv', header=None, skiprows=1).values
emcal_data = pd.read_csv('0.5_emcal_flattened.csv', header=None, skiprows=1).values
hcal_data = pd.read_csv('0.5_hcal_flattened.csv', header=None, skiprows=1).values

# Prepare input and output matrices
XX = np.hstack([trkn_data, trkp_data, emcal_data, hcal_data])
Y = truth_data

# Normalize data
scaler = StandardScaler()
XX_normalized = scaler.fit_transform(XX)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(XX_normalized, Y, test_size=0.2, random_state=42)

# Convert data to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32).to(device)
Y_train_tensor = torch.tensor(y_train, dtype=torch.float32).to(device)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32).to(device)
Y_test_tensor = torch.tensor(y_test, dtype=torch.float32).to(device)

# Reshape for 1D CNN (assuming your features represent some kind of sequence)
X_train_tensor = X_train_tensor.unsqueeze(1)  # Add channel dimension
X_test_tensor = X_test_tensor.unsqueeze(1)

# Get input size for the CNN
input_size = X_train_tensor.shape[2]  # The size of the features dimension

# Initialize model
model = MyCNN(input_size).to(device)  # 将模型移到 GPU

# Create datasets and dataloaders
train_dataset = TensorDataset(X_train_tensor, Y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_dataset = TensorDataset(X_test_tensor, Y_test_tensor)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# Hyperparameters
learning_rate = 0.0001
batch_size = 32
num_epochs = 50

# Initialize loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    for i, (inputs, labels) in enumerate(train_loader):
        inputs, labels = inputs.to(device), labels.to(device)  # 将数据移到 GPU
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        if (i+1) % 100 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(train_loader)}], Loss: {loss.item():.4f}')

# Evaluation and prediction
model.eval()
with torch.no_grad():
    y_pred = []
    y_true = []
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)  # 将数据移到 GPU
        outputs = model(inputs)
        y_pred.append(outputs.cpu().numpy())  # 将输出移回 CPU
        y_true.append(labels.cpu().numpy())

    y_pred = np.concatenate(y_pred).flatten()
    y_true = np.concatenate(y_true).flatten()

mse = np.mean((y_pred - y_true) ** 2)
print(f"Mean Squared Error: {mse:.4f}")

# Save predictions to a CSV file
predictions_df = pd.DataFrame({'True Values': y_true, 'Predicted Values': y_pred})
predictions_df.to_csv('predict.csv', index=False)
print("Predictions saved to predict.csv")
