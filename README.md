# Factiva PDF Generator

Run factiva-pdf-generator.py with 2 arguments
Argument 1 is the magazine name
Argument 2 is the full article title with " changed to '
Argument 3 is the article publish date (YYYYMMDD)
Argument 4 is the article author

To pass the article text, create a text file containing the article text, and place it in the same folder as this python file.
The file name should be the first 50 characters of the article title with punctuation stripped, followed by .txt

Output PDF is stored in the pdf folder.

# Example

python factiva-pdf-generator.py "Barron's" "Example Title Here" "20230901" "Jacob Sonenshine"

File named "Example Title Here.txt" exists in this folder.
