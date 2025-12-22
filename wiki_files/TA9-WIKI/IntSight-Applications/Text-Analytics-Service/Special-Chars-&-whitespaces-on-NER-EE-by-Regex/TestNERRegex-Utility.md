[[_TOC_]]
# Intro
This utility is for regular expression tests.
It imitates the regex matching as it's being done by our TextAnalytics' _NER_ engine (**NOT Basis**).

Use it to test your regular expressions easily.

Project is located on `Utils/TestNERRegex`

The utility expects 2 parameters:
1. Input regular expressions file
1. Input text content to match given regular expressions

# Usage
## Choose how to use it
1. From within the IDE
1.1 Maven restore
1.2 Create Run/Debug configuration: Application
1.3 Specify Debug/Run parameters
1. From command line:
2.1 Compile the project (maven restore & install)
2.2 Use the created JAR (/target folder)
java -jar TestNERRegex.jar <PATH_TO_REGEX_FILE> <PATH_TO_CONTENT_TEST>
<PATH_TO_REGEX_FILE> - should contain line for each regular expression: REGEX TYPE. Sample: [0-9]{5}  SomeNumber. (separator is a single tab - \t)
<PATH_TO_CONTENT_TEST> - should contain sample text. Regular expressions from <PATH_TO_REGEX_FILE> will be evaluated against file's text

## Sample Input files
[regex.txt](/.attachments/regex-6d3d5869-cdd2-4815-9a7d-d33e51d5810f.txt)
[regex_content.txt](/.attachments/regex_content-c8a56ef1-d100-4f27-acab-263eac0bf9af.txt)


## Output
The program outputs 3 indications (to console):
1. INPUT: the input text as read by the program
1. INPUT TOKNIZED: the tokens produced by the engine tokenizer
1. REGEX: the regular expressions input as read by the program
1. RESULT: the result text after trying to match the regular expressions on input text