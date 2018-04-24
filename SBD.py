#EECS 498, ISAIAH DAVIS, ijnd
import sys
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing

def vectorize(trainfile, word_list):
	traindata = open(trainfile, "r")
	feature_vectors=[]
	label_list=[]
	le = preprocessing.LabelEncoder()
	#Boolean for finding R
	looking_for_R = False
	for line in traindata:
		(wid, word, token) = line.split()
		if token != "TOK":
			feature_vector = []
			#First feature, L is measured based on label encoder. Encoder not used yet.
			stripped_word = word.replace(".","")
			stripped_word = stripped_word.lower()
			word_list.append(stripped_word)
			feature_vector.append(stripped_word)
			#Second feature, R, will be added later.
			feature_vector.append("") #placeholder
			looking_for_R = True
			#Third feature, is L < 3
			temp_var = len(stripped_word)
			feature_vector.append(temp_var < 3)
			#Fourth feauture, is L capitalized
			feature_vector.append(word[0].isupper())
			#Fifth feature, is R capitalized **placeholder
			feature_vector.append(False)
			#Additional features
			#Sixth feature- L has a vowel
			chars = set('aeiou')
			if any((c in chars) for c in stripped_word):
				feature_vector.append(True)
			else:
				feature_vector.append(False)
			#Seventh feature- L ends with r
			feature_vector.append(stripped_word.endswith("r"))
			#Eigth feature- is R punctuation *placeholder
			feature_vector.append(False)
			#Add the feature vector to the proper list
			feature_vectors.append(feature_vector)
			label_list.append(token)

		elif looking_for_R:
			#Fill in the placeholders from the last line with the new word in this line
			(wid, word, token) = line.split()
			#First we fill in the second feature
			lower_word = word.lower()
			word_list.append(lower_word)
			R = lower_word
			#Next we check if R is capitalized
			is_caps = word[0].isupper()
			#Finally check if R is punctuation
			is_alnum = not word[0].isalnum()
			feature_vectors[len(feature_vectors) - 1][1] = R
			feature_vectors[len(feature_vectors) - 1][4] = is_caps
			feature_vectors[len(feature_vectors) - 1][7] = is_alnum
			looking_for_R = False
	#Replaced all words
	L_words = [vec[0] for vec in feature_vectors]
	R_words = [vec[1] for vec in feature_vectors]
	le.fit(word_list)
	transformed_L = le.transform(L_words)
	transformed_R = le.transform(R_words)
	for x in range(len(feature_vectors)):
		feature_vectors[x][0]=transformed_L[x]
		feature_vectors[x][1]=transformed_R[x]

	return [feature_vectors, label_list]

def main(argv):
	trainfile = argv[1]
	word_list = []
	testfile = argv[2]
	train_vectors = vectorize(trainfile, word_list)
	test_vectors = vectorize(testfile, word_list)
	tree = DecisionTreeClassifier(random_state=0)
	tree.fit(train_vectors[0], train_vectors[1])
	predicted_list = tree.predict(test_vectors[0])
	score = tree.score(test_vectors[0], test_vectors[1])
	print(score)

if __name__ == "__main__":
	main(sys.argv)