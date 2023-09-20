# Cryptanalysis of simple substitution ciphers

**Tasks**:
- Perform cryptanalysis of the text encrypted by the Vigenere cipher. For cryptanalysis, use the Kasiski test.
- Conduct an experimental study of the dependence of the probability of a successful Kasiski attack on the length of the ciphertext. Build graphs. 
- Conduct an experimental study of the dependence of the probability of a successful Kasiski attack on the length of the keyword used in encryption. Build graphs.
	
**Additionally**: propose a mechanism for filtering random repetitions of l-grams.

**Spoiler.** The following was suggested: 
- The ciphertext is analyzed for the presence of repetitive _l-gramms_ in it.
- For each of the _l-gramm_ encountered more than once in the ciphertext, the distances between its neighboring occurrences are calculated.
- Useful divisors are calculated for all distances: from 2 to the assumed MAX_KEY_LENGTH.
- Given that in general, a good choice is the largest factor that appears most often, we have to somehow separate the most common divisors. _Not so much to choose a random factor, and not so little not to choose an unreasonably short word length._ 
- We use the formula: the number of repetitions of the most frequent divisor * PERCENT = threshold for selecting the most frequent divisors.
- And then we choose the largest of the divisors, repeating more than the threshold value.
- In this work PERCENT = 0.8 (_experimentally_)

See the results of the work [here](https://github.com/dora-thea/cybersecurity_labs_2023/blob/e529d37a5d0273f5ea167f6c8b4c4cf5f7894045/lab01_cryptanalysis_vigenere/report/report.md)