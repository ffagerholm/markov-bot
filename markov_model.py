#!/usr/bin/env python
# -*- coding: utf-8 -*-
import markovify
import nltk
import re


class POSifiedText(markovify.Text):
    """
    Markov chain generator with part-of-speech tagging.
    Words in corpus are tagged with its corresponding grammatical class to
    improve the sentence structure of the generated text.
    **It may take a long time to generate the model for a large corpus!** 
    """
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = ["::".join(tag) for tag in nltk.pos_tag(words)]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


if __name__ == '__main__':
    with open('data/tweets.csv', 'r') as f:
        text = f.read()

    model = POSifiedText(text)

    with open('data/model.json', 'wb') as f:
        f.write(model.to_json())

