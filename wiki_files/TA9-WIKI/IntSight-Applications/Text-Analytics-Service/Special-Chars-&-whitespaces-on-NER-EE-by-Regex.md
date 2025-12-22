[[_TOC_]]
# Intro
NER EE by Regex is working as the following process:
1. Tokenizing the sentences
1. Running each regular expression on each token, considering whitespace/s between tokens

# On IntSight
Our usage of NER is using [PTBTokenizer](https://nlp.stanford.edu/nlp/javadoc/javanlp/edu/stanford/nlp/process/PTBTokenizer.html) to tokenize the input text.

# Guidelines
Here are some guidelines on how to handle special _characters & whitespaces_:
1. To connect between tokens, we use regular whitespace in our regular-expression 
1. **Whitespace** - just put a whitespace on the regular expression, eg: `[A-Z]{2} \d{7}`
2.1. **Non-Breaking-Whitespace** - Sometimes, NER does not break (tokenize) input text by whitespace, but instead uses a non-breaking-whitespace. So, in that case we would use that special char in our regular expression regularly, eg: `(\+65|65)?( )?(6|8|9)[0-9]{3} [0-9]{4,4}` (first whitespace is non-breaking, second is a regular whitespace, but they look the same )
1. **Special Chars** - usually* the tokenizer splits tokens when encountering special characters, so on our regular expression we should add whitespace before and after the special character, eg: `[A-Z] \- [A-Z]`


# Tests
For tests, there's a utility that's doing the same RegEx processing as our TextAnalytics' NER engine. You can use it to test regular expressions matching on input text content. See [TestNERRegex Utility](https://dev.azure.com/ta-9/Argus/_wiki/wikis/Argus.wiki/434/TestNERRegex-utility) for more.