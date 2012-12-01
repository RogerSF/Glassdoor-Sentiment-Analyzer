from GlassdoorReview import *
import nltk.data
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import math, collections, pickle
from Sentiment import *
import ClassifierData

#ese dictionaries map an n-gram to a list:
# [neutral_count, pros_count, cons_count, total_count]

# in title for each JJ or ADV: create two probs
# one for pros and one for cons
# whichever is highest, add to the cooresponding probs below

# in pros multiply together all the probs from the pros

# in the cons multiply together all the probs from the cons

# 

def main():	
	correct = 0
	test_set = GlassdoorReview.get_test_set()
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	
	for review in test_set:
		pros_prob = 0
		cons_prob = 0
		
		title = tokenizer.tokenize(review.title)
		pros = tokenizer.tokenize(review.pros)
		cons = tokenizer.tokenize(review.cons)
        
		#tagged_title = pos_tag(word_tokenize(title[0]))
		#tagged_pros = pos_tag(word_tokenize(pros[0]))
		#tagged_cons = pos_tag(word_tokenize(cons[0]))
        
        #might need to iterate. Check structure of tagged_
		for t in title:
			tt = pos_tag(word_tokenize(t))
			pros_prob, cons_prob = get_probs_title(tt, pros_prob, cons_prob)
		for p in pros:
			tp = pos_tag(word_tokenize(p))
			pros_prob, cons_prob = get_probs_pros(tp, pros_prob, cons_prob)
		for c in cons:
			tc = pos_tag(word_tokenize(c))
			pros_prob, cons_prob = get_probs_cons(tc, pros_prob, cons_prob)
        
		sentiment = guess_sentiment(pros_prob, cons_prob)
        
		if sentiment == "Positive" and review.rating > 3:
			correct +=1
		elif sentiment == "Negative" and review.rating < 3:
			correct +=1
		print "Positive Prob: " + str(pros_prob)
		print "Negative Prob: " + str(cons_prob)
		print "Score: " + str(review.rating)
	accuracy = float(correct) / len(test_set)
	print "Correct: "  + str(correct)
	print "Test: "  + str(len(test_set))
	print "Accuracy: " + str(accuracy)
	
if __name__ == "__main__": main()
