# Factiva PDF Generator

Run factiva-pdf-generator.py with 6 arguments
Argument 1 is the magazine name
Argument 2 is the full article title with " changed to '
Argument 3 is the stripped title that will be used as a filename
Argument 4 is the article publish date (YYYYMMDD)
Argument 5 is the article author
Argument 6 is the subtitle with " changed to '


To pass the article text, create a text file containing the article text, and place it in the same folder as this python file.
The file name should be the first 50 characters of the article title with punctuation and whitespaces stripped, followed by .txt
This file name should be passed as Argument 3 above

Output PDF is stored in the pdf folder.

# Example

python factiva-pdf-generator.py "Barron's" "Example Title Here" "ExampleTitleHere" "20230901" "Jacob Sonenshine" "Example Subtitle Here"

File named "ExampleTitleHere.txt" exists in this folder.
