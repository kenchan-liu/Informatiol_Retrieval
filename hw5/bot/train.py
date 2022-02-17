from torch import optim

from model import *

if __name__=="__main__":
    # 配置训练/优化
    model_name = 'cb_model'
    attn_model = 'dot'
    hidden_size = 500
    encoder_n_layers = 2
    decoder_n_layers = 2
    dropout = 0.1
    batch_size = 64

    # 设置检查点以加载; 如果从头开始，则设置为None
    loadFilename = None
    checkpoint_iter = 1000
    #loadFilename = os.path.join(save_dir, model_name, corpus_name,
     #                           '{}-{}_{}'.format(encoder_n_layers, decoder_n_layers, hidden_size),
      #                          '{}_checkpoint.tar'.format(checkpoint_iter))

    # 如果提供了loadFilename，则加载模型
    if loadFilename:
        # 如果在同一台机器上加载，则对模型进行训练
        checkpoint = torch.load(loadFilename)
        encoder_sd = checkpoint['en']
        decoder_sd = checkpoint['de']
        encoder_optimizer_sd = checkpoint['en_opt']
        decoder_optimizer_sd = checkpoint['de_opt']
        embedding_sd = checkpoint['embedding']
        voc.__dict__ = checkpoint['voc_dict']

    print('Building encoder and decoder ...')
    # 初始化词向量
    embedding = nn.Embedding(voc.num_words, hidden_size)
    if loadFilename:
        embedding.load_state_dict(embedding_sd)
    # 初始化编码器 & 解码器模型
    encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
    decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
    if loadFilename:
        encoder.load_state_dict(encoder_sd)
        decoder.load_state_dict(decoder_sd)
    # 使用合适的设备
    encoder = encoder.to(device)
    decoder = decoder.to(device)
    print('Models built and ready to go!')
    clip = 50.0
    teacher_forcing_ratio = 1.0
    learning_rate = 0.0001
    decoder_learning_ratio = 5.0
    n_iteration = 120000
    print_every = 1
    save_every = 10000

    # 确保dropout layers在训练模型中
    encoder.train()
    decoder.train()

    # 初始化优化器
    print('Building optimizers ...')
    encoder_optimizer = optim.Adam(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = optim.Adam(decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
    if loadFilename:
        encoder_optimizer.load_state_dict(encoder_optimizer_sd)
        decoder_optimizer.load_state_dict(decoder_optimizer_sd)

    # 运行训练迭代
    print("Starting Training!")
    trainIters(model_name, voc, pairs, encoder, decoder, encoder_optimizer, decoder_optimizer,
               embedding, encoder_n_layers, decoder_n_layers, save_dir, n_iteration, batch_size,
               print_every, save_every, clip, corpus_name, loadFilename)
