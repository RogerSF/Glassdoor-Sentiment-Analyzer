from GlassdoorReview import *
import nltk.data
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
import math, collections, pickle

# These dictionaries map an n-gram to a list:
# [title_count, pros_count, cons_count, total_count]
unigramCounts = collections.defaultdict(lambda: [1,1,1,1])
bigramCounts = collections.defaultdict(lambda: [0,0,0,0])
unigramTotal = 0

def tain_title(title):
	star_weight = 1
    for i in range(0, len(pro)):
    	word1 = pro[i]
    	pos = word1[1]
    	if pos in ['JJ', 'NN', 'NNS', 'RB', 'RBR', 'RBS']:
    		if i+2 < len(pro):
    			word2 = pro[i+1]
    			word3 = pro[i+2]
    			if third_word_test(word1, word2, word3):
    				create_bigram(word1, word2, star_weight, "title")
    				create_unigram(word1, star_weight, "title")
    			#pass
    		elif i+1 < len(pro):
    			word2 = pro[i+1]
    			if second_word_test(word1, word2):
    				create_bigram(word1, word2, star_weight, "title")
    				create_unigram(word1, star_weight, "title")
    			#pass
    		else:
    			create_unigram(word1, star_weight, "title")

def train_pros(pro):
    if review.rating > 3:
        star_weight = create_star_weight(review.rating)
    else:
    	star_weight = 1

    for i in range(0, len(pro)):
    	word1 = pro[i]
    	pos = word1[1]
    	if pos in ['JJ', 'NN', 'NNS', 'RB', 'RBR', 'RBS']:
    		if i+2 < len(pro):
    			word2 = pro[i+1]
    			word3 = pro[i+2]
    			if third_word_test(word1, word2, word3):
    				create_bigram(word1, word2, star_weight, "pro")
    				create_unigram(word1, star_weight, "pro")
    			#pass
    		elif i+1 < len(pro):
    			word2 = pro[i+1]
    			if second_word_test(word1, word2):
    				create_bigram(word1, word2, star_weight, "pro")
    				create_unigram(word1, star_weight, "pro")
    			#pass
    		else:
    			create_unigram(word1, star_weight, "pro")
    #pass

def train_cons(con):
    if review.rating < 3:
        star_weight = create_star_weight(review.rating)
    else:
    	star_weight = 1

    for i in range(0, len(pro)):
    	word1 = pro[i]
    	pos = word1[1]
    	if pos in ['JJ', 'NN', 'NNS', 'RB', 'RBR', 'RBS']:
    		if i+2 < len(pro):
    			word2 = pro[i+1]
    			word3 = pro[i+2]
    			if third_word_test(word1, word2, word3):
    				create_bigram(word1, word2, star_weight, "con")
    				create_unigram(word1, star_weight, "con")
    			#pass
    		elif i+1 < len(pro):
    			word2 = pro[i+1]
    			if second_word_test(word1, word2):
    				create_bigram(word1, word2, star_weight, "con")
    				create_unigram(word1, star_weight, "con")
    			#pass
    		else:
    			create_unigram(word1, star_weight, "con")
    
def create_bigram(word1, word2, star_weight, sentiment):
	bicounts = bigramCounts[(word1[0], word2[0])]
	if seniment == "pro":
    	bicounts[1] += star_weight
    elif sentiment == "con":
    	bicounts[2] += star_weight
    bicounts[3] += star_weight
    
    bigramCounts[(word1[0], word2[0])] = bicounts
    
def create_unigram(word1, star_weight, sentiment):
	unicounts = unigramCounts[word1[0]]
	if unicounts == [1,1,1,1]:
		uniTotal += 1
	if seniment == "pro":
    	unicounts[1] += star_weight
    elif sentiment == "con":
    	unicounts[2] += star_weight
	unicounts[3] += star_weight
	uniTotal += star_weight
	
	unigramCounts[word1[0]] = unicounts

# determines wether or not a bigram should be counted
# depending upon the third word in sequence
def third_word_test(w1, w2, w3):
	if w1[1] == 'JJ':
		if w2[1] in ['NN', 'NNS']:
			return True
		elif w2[1] == 'JJ' and w3[1] not in ['NN', 'NNS']:
			return True
		else:
			return False
	if w1[1] in ['NN', 'NNS']:
		if w2[1] == 'JJ' and w3[1] not in ['NN', 'NNS']:
			return True
		else:
			return False
	if w1[1] in ['RB', 'RBR', 'RBS']:
		if w2[1] == 'JJ' and w3[1] not in ['NN', 'NNS']:
			return True
		elif w2[1] in ['VB', 'VBD', 'VBN', 'VBG']:
			return True
		else:
			return False
	else:
		return False

def second_word_test(w1, w2):
	if w1[1] == 'JJ':
		if w2[1] in ['JJ','NN', 'NNS']:
			return True
		else:
			return False
	if w1[1] in ['NN', 'NNS']:
		if w2[1] == 'JJ':
			return True
		else:
			return False
	if w1[1] in ['RB', 'RBR', 'RBS']:
		if w2[1] in ['JJ', 'VB', 'VBD', 'VBN', 'VBG']:
			return True
		else:
			return False
	else:
		return False

def create_star_weight(rating):
    if rating == 3:
        weight = 1
    elif rating > 3:
        weight = rating - 2
    else:
        weight = 3 - rating
    return weight

def train_classifier(training_set):
    tokenizer = nltk.data.load('tokenizer/punkt/english.pickle')
    for review in training_set:

       # star_weight = create_star_weight(review.rating)
        title = tokenizer.tokenize(review.title)
        pros = tokenizer.tokenize(review.pros)
        cons = tokenizer.tokenize(review.cons)
        
        tagged_title = pos_tag(word_tokenize(title[0]))
        tagged_pros = pos_tag(word_tokenize(pros[0]))
        tagged_cons = pos_tag(word_tokenize(cons[0]))

        train_title(tagged_title)
        train_pros(tagged_pros)
        train_cons(tagged_cons)
        

def main():
    training_set = GlassdoorReview.get_training_set()
    train_classifier(training_set)
    
    bg_output = open('bidata.pkl', 'wb')
    pickle.dump(bigramCounts, bg_output)
    bg_output.close()
    
    unigramCounts["total"] = unigramTotal
    
    ug_output = open('unidata.pkl', 'wb')
    pickle.dump(unigramCounts, ug_output)
    ug_output.close()
    


if __name__ == "__main__": main()
