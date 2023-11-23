import numpy
import json
import Conv

def sigmoid(x):
    return 1/(1+numpy.exp(-x))

def relu(x):
    return numpy.maximum(numpy.minimum(x, 1), 0)

def advancedRELU(x):
    return numpy.maximum(numpy.minimum(x, 1), -1)

def nothing(x):
    return x

def STR2ACT(act, typ:bool = False):
    if not typ:
        #print(str(act), type(act))
        if 'sigmoid' in str(act):
            return "sigm"
        elif 'relu' in str(act):
            return "relu"
        elif 'advancedRELU' in str(act):
            return "adRELU"
        elif 'nothing' in str(act):
            return "noth"
        else:
            return "ERROR"

    else:
        if act == "sigm":
            return sigmoid
        elif act == "relu":
            return relu
        elif act == "adRELU":
            return advancedRELU
        elif act == "noth":
            return nothing

class NeuralNetwork:

    def __init__(self, inp, hidden1, hidden2, hidden3, out, act1, act2, act3, act4):
        self.syn0 = 2*numpy.random.random((inp, hidden1))-1
        self.syn1 = 2*numpy.random.random((hidden1, hidden2))-1
        self.syn2 = 2*numpy.random.random((hidden2, hidden3))-1
        self.syn3 = 2*numpy.random.random((hidden3, out))-1
        
        self.inp = inp
        self.hidden1 = hidden1
        self.hidden2 = hidden2
        self.hidden3 = hidden3
        self.out = out

        self.act1 = act1
        self.act2 = act2
        self.act3 = act3
        self.act4 = act4

    def addSyn(self, syn0, syn1, syn2, syn3):
        self.syn0 += syn0
        self.syn1 += syn1
        self.syn2 += syn2
        self.syn3 += syn3

    def setSyn(self, syn0, syn1, syn2, syn3):
        self.syn0 = syn0
        self.syn1 = syn1
        self.syn2 = syn2
        self.syn3 = syn3

    def predict(self, inp):
        inh1 = self.act1(numpy.dot(inp, self.syn0))
        h1h2 = self.act2(numpy.dot(inh1, self.syn1))
        h2h3 = self.act3(numpy.dot(h1h2, self.syn2))
        h3out = self.act4(numpy.dot(h2h3, self.syn3))
        return h3out

    def Mutate(self, coof):
        self.syn0 += (2*numpy.random.random((self.inp, self.hidden1))-1)*coof
        self.syn1 += (2*numpy.random.random((self.hidden1, self.hidden2))-1)*coof
        self.syn2 += (2*numpy.random.random((self.hidden2, self.hidden3))-1)*coof
        self.syn3 += (2*numpy.random.random((self.hidden3, self.out))-1)*coof

    def Save(self, file, ret: bool = False):
        data = {"inp":self.inp, "hidden1":self.hidden1, "hidden2":self.hidden2, "hidden3":self.hidden3, "out":self.out,
               "act1":STR2ACT(self.act1), "act2":STR2ACT(self.act2), "act3":STR2ACT(self.act3), "act4":STR2ACT(self.act4),
              "syn0":Conv.Convert(self.syn0), "syn1":Conv.Convert(self.syn1), "syn2":Conv.Convert(self.syn2), "syn3":Conv.Convert(self.syn3)}
        if ret:
            return data
        else:
            json.dump(data, file)

    def Load(self, f, ret: bool = False):
        #print(type(f))
        if type(f) == dict:
            self.inp = f["inp"]
            self.hidden1 = f["hidden1"]
            self.hidden2 = f["hidden2"]
            self.hidden3 = f["hidden3"]
            self.out = f["out"]
            self.act1 = STR2ACT(f["act1"], True)
            self.act2 = STR2ACT(f["act2"], True)
            self.act3 = STR2ACT(f["act3"], True)
            self.act4 = STR2ACT(f["act4"], True)
            self.syn0 = Conv.Convert(f["syn0"], True)
            self.syn1 = Conv.Convert(f["syn1"], True)
            self.syn2 = Conv.Convert(f["syn2"], True)
            self.syn3 = Conv.Convert(f["syn3"], True)
        else:
            data = json.load(f)
            self.inp = data["inp"]
            self.hidden1 = data["hidden1"]
            self.hidden2 = data["hidden2"]
            self.hidden3 = data["hidden3"]
            self.out = data["out"]
            self.act1 = STR2ACT(data["act1"], True)
            self.act2 = STR2ACT(data["act2"], True)
            self.act3 = STR2ACT(data["act3"], True)
            self.act4 = STR2ACT(data["act4"], True)
            self.syn0 = Conv.Convert(data["syn0"], True)
            self.syn1 = Conv.Convert(data["syn1"], True)
            self.syn2 = Conv.Convert(data["syn2"], True)
            self.syn3 = Conv.Convert(data["syn3"], True)

    def __str__(self):
        return f'NEURAL NETWORK:\nact1:{self.act1}, act2:{self.act2}'
if __name__ == "__main__":
    n = NeuralNetwork(2, 3, 3, 3, 3, relu, sigmoid, relu, relu)
    print(n.syn0, '\n', n.syn1, '\n', n.act1, '\n', n.act2, '\n')
    f = open("test.json", "w")
    n.Save(f)
    f.close()
    f = open("test.json", "r")
    n = NeuralNetwork(5, 5, 5, 3, 3, sigmoid, relu, relu, relu)
    n.Load(f)
    print(n.syn0, '\n', n.syn1, '\n', n.act1, '\n', n.act2, '\n')