## `content_based_1`

### Description

Improved version of `content_based_0`. Not only it does better preprocessing of the text in the questions, but it also has a more complex measure of the interest of a question:

- `QuestionScore = SizeOfQuestion * Similarity^2`

  Where:

  - `SizeOfSimilar` is the word count (ignoring stop words) of the question answered by the user that resembles the most to the question for which we are calculating the score.
  - `Similarity` is the dot product of the vectorized text with the most similar question (the same as before).

### Information

Display the title of the most similar question and the values of `SizeOfQuestion`, `Similarity` and `QuestionScore`.

### Observations

- The code chunks in the questions are ignored (they are considered noise).
- There are extremely rare cases where the system can crash, if the question contains text that the html parser of BeautifulSoup can't recognize. This has only happened me once with a question about regular expressions.
- The Similarity is squared to reduce the preference of wall of text questions. 

## `content_based_0`

### Description

Model used for the first release. It is an adaptation of the content based recommendation system from [this tutorial](https://www.datacamp.com/community/tutorials/recommender-systems-python). 

### Information

Doesn't return any.

### Observations

- The system is biased to prefer shorter questions.
- The word count is case sensitive.