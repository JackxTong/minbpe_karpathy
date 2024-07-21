from minbpe import BasicTokenizer
from minbpe.base import Tokenizer, get_stats, merge
from longtext import long_text as text
tokenizer = BasicTokenizer()
tokenizer.train(text, 256 + 20) # 256 are the byte tokens, then do 20 merges

tokenizer.save("toy") # saving vocab
print(tokenizer.encode('hello world e e !')) # do two "e " as "e" and " " is first merge


class MyEncoder(BasicTokenizer):
    def __init__(self):
        super().__init__()

    def encode(self, text):
        tokens = text.encode("utf-8")
        tokens = list(map(int, tokens))
        for pair, index in self.merges.items():
            # print(pair, index)
            tokens = merge(tokens, pair, index)
        return tokens
    
mytokenizer = MyEncoder()
mytokenizer.train(text, 256+20)
print(mytokenizer.encode("hello world e e !"))
    


