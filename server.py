from flask import Flask
from flask import request
import chess
import encoder
import torch
import AlphaZeroNetwork
app = Flask(__name__)

modelFile = "weights/AlphaZeroNet_20x256.pt"
#toggle for cpu/gpu
cuda = False
if cuda:
    weights = torch.load( modelFile )
else:
    weights = torch.load( modelFile, map_location=torch.device('cpu') )

@app.route('/AI', methods=['POST'] )
def AI():
    #prepare neural network
    alphaZeroNet = AlphaZeroNetwork.AlphaZeroNet( 20, 256 )
    alphaZeroNet.load_state_dict( weights )
    if cuda:
        alphaZeroNet = alphaZeroNet.cuda()
    for param in alphaZeroNet.parameters():
        param.requires_grad = False
    alphaZeroNet.eval()

    fen = request.form['fen' ] 
    board = chess.Board( fen )
    with torch.no_grad():
        value, move_probabilities = encoder.callNeuralNetwork( board, alphaZeroNet )
        maxP = -1
        maxMove = None
        for idx, move in enumerate( board.legal_moves ):
            if( move_probabilities[ idx ] > maxP ):
                maxP = move_probabilities[ idx ]
                maxMove = move
        return maxMove.uci()



