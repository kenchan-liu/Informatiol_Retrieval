import torch.nn as nn
import torch.nn.functional as F
from torch.utils import checkpoint
import os
import torch
USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")
model_name = 'cb_model'
attn_model = 'dot'
# attn_model = 'general'
# attn_model = 'concat'
hidden_size = 300
encoder_n_layers = 2
decoder_n_layers = 2
dropout = 0.1
batch_size = 64
normal = 0  # Used for padding short sentences
start = 1  # Start-of-sentence token
end = 2  # End-of-sentence token
corpus = "cornell movie-dialogs corpus"
corpus_name = os.path.join("F://Chat-Bot//data//", corpus)
datafile = "F://Chat-Bot//data//cornell movie-dialogs corpus//formattedlines.txt"