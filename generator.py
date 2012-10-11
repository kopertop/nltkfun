'''
Author: Chris Moyer <cmoyer@newstex.com>
Description: Generation utilities, mostly
just testing functions based on my
learning from the NLP Book
'''
import nltk
import random
WORD_TERMINATORS = ['.', '!', '?']
SPLIT_SYMBOLS = [',', ';']
VALID_SYMBOLS = WORD_TERMINATORS + SPLIT_SYMBOLS
class PhraseGenerator(object):
	'''A simple Phrase Generator.
	Starting with a simple input Text corpa,
	creates a Conditional Frequency Distribution (CDF), and
	then allows you to call this module with a word and optional
	number of words you'd like in the sentence.

	This lets you produce likely phrases given a source word and the author's
	style of writing.
	>>> gen = PhraseGenerator(nltk.corpus.brown)
	>>> print gen('living')
	
	You can also provide a keyword
	>>> gen = PhraseGenerator(nltk.corpus.brown, categories='news')
	>>> print gen('news')
	
	Or a specific file
	>>> gen = PhraseGenerator(nltk.corpus.inaugural, '2009-Obama.txt')
	>>> print gen('i')
	>>> print gen('you')
	
	Note that some randomization is involved, so you may get different results
	if you run the same request twice

	You can also pass in your own text blob directly, creating your own
	style.
	'''

	def __init__(self, corpa, *args, **kwargs):
		'''Initialize the PhraseGenerator with a starting corpus. This can
		be either a text blob, or a Class that responds to functions
		"words" and "sents", with optional args and kwargs as passed in to this initializer
		'''
		if isinstance(corpa, basestring):
			words = nltk.word_tokenize(corpa)
			sents = nltk.sent_tokenize(corpa)
		else:
			words = corpa.words(*args, **kwargs)
			sents = corpa.sents(*args, **kwargs)
		bigrams = nltk.bigrams([w.lower() for w in words])
		self.cdf = nltk.ConditionalFreqDist(bigrams)
		self.case_cdf = nltk.ConditionalFreqDist([(w.lower(), w) for w in words])
		self.avg_sent_len = int(len(words)/len(sents))

	def __call__(self, word):
		'''Produces a likely phrase based on the initial "seed word" provided
		:param word: Seed word to start the phrase with
		:type word: str

		:return: A likely string that would come from this corpa, based on the seed word
		:rtype: str
		'''
		word = word.lower()
		if ' ' in word:
			ret = nltk.word_tokenize(word)
			word = ret[-1]
		else:
			ret = [word]
		while word not in WORD_TERMINATORS:
			if ret[-1] in SPLIT_SYMBOLS:
				prev_word = ret[-1]
			else:
				prev_word = ret[-1]
			for new_word in self.cdf[word]:
				# Don't duplicate words
				if new_word == word:
					continue
				# Don't accept any symbols
				if not (new_word.isalpha() or new_word.isdigit()) and not new_word in VALID_SYMBOLS:
					continue
				# Don't allow the sentence to be less then half
				# of the average sentence length
				if new_word in WORD_TERMINATORS and len(ret) < self.avg_sent_len/2:
					continue
				if not new_word in ret[-len(ret)/2:]:
					prev_phrase = [prev_word, new_word]
					if not ' '.join(prev_phrase) in ' '.join(ret):
						# If this word is less then 4 characters
						# and so was the previous one, on average we skip it,
						# with only a small chance to keep it
						if not (len(new_word) < 4 and (len(prev_word) < 4) and not random.randint(0,6)):
							word = new_word
							# Randomly we'll try to skip this word, but we set our previous match to this
							# just in case we don't find a new one
							if not random.randint(0,2):
								break
			if word == ret[-1]:
				ret.append('...')
				break
			ret.append(word)

		for x, w in enumerate(ret[:]):
			d = self.case_cdf[w]
			if d:
				ret[x] = d.max()
		ret = ' '.join(ret)

		ret = ret[0].upper() + ret[1:]
		
		for symbol in VALID_SYMBOLS:
			ret = ret.replace(' %s' % symbol, symbol)
		return ret
