## Pytest to test simpler Encoder logic

I noticed the encode() method has extra logic with a while loop to find the lowest merge index:
```python
    def encode(self, text):
        text_bytes = text.encode("utf-8") # raw bytes
        ids = list(text_bytes) # list of integers in range 0..255
        while len(ids) >= 2:
            stats = get_stats(ids)
            pair = min(stats, key=lambda p: self.merges.get(p, float("inf")))
            if pair not in self.merges:
                break # nothing else can be merged anymore
            idx = self.merges[pair]
            ids = merge(ids, pair, idx)
        return ids
```

Can we simplify it like this:

```python
    def encode(self, text):
        tokens = text.encode("utf-8")
        tokens = list(map(int, tokens))
        for pair, index in self.merges.items():
            tokens = merge(tokens, pair, index)
        return tokens
```

Since merge() merges all occurrences, it seems a simple for loop suffices. Is there a reason for the more complex logic? 
I have trained my tokenizer vs the basictokenizer on some text data, and achieved the exact same vocab & encoder.

## Ways to test:
1. Test `BasicTokenizer` with my `encode()` achieves same result on TaylorSwift wiki text.
```bash
python3 -m pytest -v tests/test_encoder
```

2. Play with both tokenizers trained on a long piece of text from `longtext.py` in `play.py`.
Input any text and see what the encoder outputs.
```bash
python3 -m play
```