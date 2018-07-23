# SMP EUPT
In order to improve the accuracy of training model, we defind thirteen features to help train the model.We find that robot writing and human writing are different in three aspects:

* Word order 

* Semantics

* Syntax 

So we use ppl and topic distribution to distinguish these two tpyes.

## Main codes
* data_process.py
preprocess the data to extract what I need
* mySRILm.py
use SRILM model to compute sentencen perplexity
* lda_infer_demo.py
This file is in Familia model. Because I get stuck in using the model, I modify the original one.So you should use it under the model condition
* myLDA.py
run the code in the terminal and get what I need
* myFeature.py
contain 13 features and return the vector
* normal_process.py
normalize the result vector

## Operating environment
Based on python2.7

* pandas
* pyltp
* numpy
* familia_wrapper
* sklearn

## Operation instructions
* first step

run myLDA.py

* second step

run myFeature.py

* third step

run normal_process.py




