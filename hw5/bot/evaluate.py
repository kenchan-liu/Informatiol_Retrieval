from config import *
DEVICE = torch.device("cpu")
class GreedySearchDecoder(nn.Module):
    def __init__(self, encoder, decoder):
        super(GreedySearchDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, input_seq, input_length, max_length):
        # 通过编码器模型转发输入
        encoder_outputs, encoder_hidden = self.encoder(input_seq.to(DEVICE), input_length.to(DEVICE))
        # 准备编码器的最终隐藏层作为解码器的第一个隐藏输入
        decoder_hidden = encoder_hidden[:self.decoder.n_layers]
        # 使用开始符号初始化解码器输入
        decoder_input = torch.ones(1, 1, device=DEVICE, dtype=torch.long) * normal
        # 初始化张量以将解码后的单词附加到
        all_tokens = torch.zeros([0], device=DEVICE, dtype=torch.long)
        all_scores = torch.zeros([0], device=DEVICE)
        # 一次迭代地解码一个词tokens
        for q in range(max_length):
            # 正向通过解码器
            decoder_output, decoder_hidden = self.decoder(decoder_input, decoder_hidden, encoder_outputs)
            # 获得最可能的单词标记及其softmax分数
            decoder_scores, decoder_input = torch.max(decoder_output, dim=1)
            # 记录token和分数
            all_tokens = torch.cat((all_tokens, decoder_input), dim=0)
            all_scores = torch.cat((all_scores, decoder_scores), dim=0)
            # 准备当前令牌作为下一个解码器输入（添加维度）
            decoder_input = torch.unsqueeze(decoder_input, 0)
        # 返回收集到的词tokens和分数
        return all_tokens, all_scores

def evaluate(encoder, decoder, searcher, voc, sentence, max_length=50):
    ### 格式化输入句子作为batch
    # words -> indexes
    indexes_batch = [indexesFromSentence(voc, sentence)]
    # 创建lengths张量
    lengths = torch.tensor([len(indexes) for indexes in indexes_batch])
    # 转置batch的维度以匹配模型的期望
    input_batch = torch.LongTensor(indexes_batch).transpose(0, 1)
    # 使用合适的设备
    input_batch = input_batch.to(DEVICE)
    lengths = lengths.to(DEVICE)
    # 用searcher解码句子
    tokens, scores = searcher(input_batch, lengths, max_length)
    # indexes -> words
    decoded_words = [voc.index2word[token.item()] for token in tokens]
    return decoded_words

def evaluateInput(encoder, decoder, searcher, voc):
    input_sentence = ''
    while (1):
        try:
            # 获取输入句子
            input_sentence = input('> ')
            # 检查是否退出
            if input_sentence == 'q' or input_sentence == 'quit': break
            # 规范化句子
            input_sentence = normalizeS(input_sentence)
            # 评估句子
            output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
            # 格式化和打印回复句
            # output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
            output_words[:] = [x for x in output_words if not (x == 'e' or x == normal)]
            print('Bot:', ' '.join(output_words))

        except KeyError:
            print("Error: Encountered unknown word.")


if __name__=="__main__":
    from train import *
    from config import *

    loadFilename = 'F:\Chat-Bot\data\cornell movie-dialogs corpus\\2-2_500\\120000_checkpoint.tar'
    attn_model = 'dot'

    hidden_size = 500
    encoder_n_layers = 2
    decoder_n_layers = 2
    dropout = 0.1
    batch_size = 64
    checkpoint = torch.load(loadFilename)
    encoder_sd = checkpoint['en']
    decoder_sd = checkpoint['de']
    encoder_optimizer_sd = checkpoint['en_opt']
    decoder_optimizer_sd = checkpoint['de_opt']
    embedding_sd = checkpoint['embedding']
    voc.__dict__ = checkpoint['voc_dict']
    # 初始化探索模块

    embedding = nn.Embedding(voc.num_words, hidden_size)
    encoder = EncoderRNN(500, embedding, encoder_n_layers, dropout)
    decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)
    encoder.eval()
    decoder.eval()

    # 初始化探索模块
    searcher = GreedySearchDecoder(encoder, decoder)

    # 开始聊天（取消注释并运行以下行开始）
    evaluateInput(encoder, decoder, searcher, voc)


