Fun with python NTLK
====================

This project is simply designed to house some fun things that I've done with NLTK.
Most of this is based off of the examples found in the very great
[Natural Language Processing with Python](http://www.amazon.com/gp/product/0596516495/ref=as_li_ss_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=0596516495&linkCode=as2&tag=blogcoredumpe-20 "Natural Language Processing with Python on Amazon.com")

To get started, you'll need to install [NLTK](http://nltk.org/)
You might also want to install simple corpa to test these scripts.

Generation of text in a given style
===================================

You can use the "PhraseGenerator" to generate text following a given style. For example you can generate phrases
that are similar to the style used by Obama in his Inaugural speach in 2009:
	>>> import nltk
	>>> from generator import PhraseGenerator
	>>> gen = PhraseGenerator(nltk.corpus.inaugural, '2009-Obama.txt')

To start a phrase with "I", simply run:
	>>> gen('i')

which might give you something like:
> I thank you to those leaders around the answer is too costly; that finally decides our nation, but because of every end to the question we ask today.
