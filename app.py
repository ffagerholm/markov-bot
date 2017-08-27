#!/usr/bin/env python
# encoding: utf-8
import markovify
from markov_model import POSifiedText

def main():
    while True:
        try:
            user_input = raw_input('> ')            
            print model.make_short_sentence(100)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    with open("data/tweets.csv") as f:
        text = f.read()

    model = markovify.NewlineText(text, state_size=2)
    main()

    
