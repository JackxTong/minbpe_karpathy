import pytest
from minbpe import BasicTokenizer
from minbpe.base import Tokenizer, get_stats, merge
import os

class MyEncoder(BasicTokenizer):
    def __init__(self):
        super().__init__()

    def encode(self, text):
        tokens = text.encode("utf-8")
        tokens = list(map(int, tokens))
        for pair, index in self.merges.items():
            print(pair, index)
            tokens = merge(tokens, pair, index)
        return tokens


test_strings = [
    "", # empty string
    "?", # single character
    "hello world!!!? (안녕하세요!) lol123 😉", # fun small string
    "FILE:taylorswift.txt", # FILE: is handled as a special string in unpack()
]

def unpack(text):
    # we do this because `pytest -v .` prints the arguments to console, and we don't
    # want to print the entire contents of the file, it creates a mess. So here we go.
    if text.startswith("FILE:"):
        dirname = os.path.dirname(os.path.abspath(__file__))
        taylorswift_file = os.path.join(dirname, text[5:])
        contents = open(taylorswift_file, "r", encoding="utf-8").read()
        return contents
    else:
        return text

@pytest.mark.parametrize("tokenizer_factory", [BasicTokenizer, MyEncoder])
@pytest.mark.parametrize("text", test_strings)
def test_encode_decode_identity(tokenizer_factory, text):
    text = unpack(text)
    tokenizer = tokenizer_factory()
    ids = tokenizer.encode(text)
    decoded = tokenizer.decode(ids)
    assert text == decoded

@pytest.mark.parametrize("tokenizer_factory", [BasicTokenizer, MyEncoder])
def test_wikipedia_example(tokenizer_factory):
    tokenizer = tokenizer_factory()
    text = "aaabdaaabac"
    tokenizer.train(text, 256 + 3)
    ids = tokenizer.encode(text)
    assert ids == [258, 100, 258, 97, 99]
    assert tokenizer.decode(tokenizer.encode(text)) == text

if __name__ == "__main__":
    pytest.main()