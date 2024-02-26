from pprint import pprint
from utils import *
import jieba
from pypinyin import lazy_pinyin, Style

def pinyin(s):
    return "".join(lazy_pinyin(s, style=Style.TONE))

class WordTokenizer:
    def __init__(self):
        self.ignore = list("_： ，-（）():，。.？！!?,\"'“”⋯  ")

    def tokenize(self, words):
        self.words = words
        self.size = len(self.words)
        self.index = 0

        self.store = []
        self.yield_tokens()
        return self.store

    def eat(self):
        if self.not_done():
            word = self.peek()
            self.index += 1
            return word
        return None

    def peek(self):
        if self.not_done():
            return self.words[self.index]

    def not_done(self):
        return self.index < self.size

    def get_punc(self):
        punctuation = self.eat()
        while self.not_done():
            next_word = self.peek()
            if next_word in self.ignore:
                punctuation += next_word
                self.eat()
            else:
                break
        return punctuation

    def yield_tokens(self):
        while self.index < len(self.words):
            index = self.index
            punctuation = None
            word = None

            if self.peek() in self.ignore:
                punctuation = self.get_punc()
            else:
                word = self.eat()
                if self.peek() in self.ignore:
                    punctuation = self.get_punc()

            payload = {
                "index": index,
                "punctuation": punctuation,
            }

            if word:
                payload["chinese"] = word
                payload["pinyin"]= pinyin(word)

            payload["pos"]= "middle"
            if index == 0:
                payload["pos"]= "start"
            elif self.index == self.size:
                payload["pos"]= "end"

            self.store.append(payload)


def pinyin_chunk(lines):

    tok = WordTokenizer()

    def runner(line):
        if line.get("linebreak"):
            return line
        text = line.get("text")
        words = list(jieba.cut(text))
        tokens = tok.tokenize(words)
        line["tokens"] = tokens
        return line

    return map(lines, runner)

test_sentences = [
  {"text": '“猫猫醒来！”猫猫。 ', "newlines": 1},
  {"text": '猫猫猛然醒了。 是不是听到别人叫他名字？'},
  {"text": '狗狗伤心地离开他朋友。', "linebreak": True},
  {"text": '“猫猫醒来！”', "newlines": 1},
  {"text": '“猫猫醒来！”'},
]
# clip(pinyin_chunk(clip())) # works
