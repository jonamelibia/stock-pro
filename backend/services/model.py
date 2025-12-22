import torch
import torch.nn as nn
import math

class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_size=1, embed_dim=64, num_heads=4, num_layers=2, output_size=1, dropout=0.1):
        super(TimeSeriesTransformer, self).__init__()
        
        # Simple linear projection to embedding dimension
        self.embedding = nn.Linear(input_size, embed_dim)
        
        # Positional Encoding
        self.pos_encoder = PositionalEncoding(embed_dim, dropout)
        
        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, dropout=dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Decoder
        self.decoder = nn.Linear(embed_dim, output_size)

    def forward(self, src):
        # src shape: [batch_size, seq_len, input_size]
        src = self.embedding(src) # [batch_size, seq_len, embed_dim]
        src = self.pos_encoder(src)
        
        # Transformer expects [batch_size, seq_len, embed_dim] if batch_first=True
        output = self.transformer_encoder(src)
        
        # We only really care about the prediction based on the last sequence element
        # But for training we might use all, here we just take the last step for regression
        last_step_output = output[:, -1, :]
        prediction = self.decoder(last_step_output)
        
        return prediction

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x: [batch_size, seq_len, d_model]
        x = x + self.pe[:x.size(1)].transpose(0, 1).reshape(1, x.size(1), -1) # adjust logic for dimensions
        # Easier: pe is [max_len, 1, d] -> [max_len, d] -> slice -> unsqueeze batch
        # Let's fix dimension logic for batch_first=True
        # pe stored: [max_len, 1, d_model]
        # x input: [batch_size, seq_len, d_model]
        
        # Correct broadcasting:
        # pe[:seq_len, 0, :] -> [seq_len, d_model] -> [1, seq_len, d_model]
        pe_slice = self.pe[:x.size(1), 0, :].unsqueeze(0)
        x = x + pe_slice
        return self.dropout(x)
