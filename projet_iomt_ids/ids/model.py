import torch
import torch.nn as nn
import torch.optim as optim


class CNN_LSTM_Model(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes):
        super(CNN_LSTM_Model, self).__init__()

        # Bloc CNN
        self.cnn = nn.Sequential(
            nn.Conv1d(input_size, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
            nn.Conv1d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )

        # Bloc LSTM
        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2 if num_layers > 1 else 0.0
        )

        # Couches finales
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(2)  # [batch, seq_len, 1]
        x = x.permute(0, 2, 1)  # [batch, 1, seq_len] → [batch, channels, time]

        out = self.cnn(x)       # [batch, 64, reduced_seq_len]
        out = out.permute(0, 2, 1)  # [batch, reduced_seq_len, 64]
        out, _ = self.lstm(out)     # [batch, reduced_seq_len, hidden_size]

        out = self.dropout(out[:, -1, :])  # [batch, hidden_size]
        out = self.fc(out)                # [batch, num_classes]
        return out

