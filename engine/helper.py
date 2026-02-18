import re  # Regular expressions for pattern matching, text searching, and text cleaning
import markdown2  # Converts Markdown text into HTML format
from bs4 import BeautifulSoup  # Parses HTML or XML content, useful for extracting data from web pages

def extract_yt_term(command):
    #define a regular expression patter to capture the song name
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    #Use re.search to find the match in the command
    match=re.search(pattern,command,re.IGNORECASE)
    #If a match is found, return the extracted song name;othewise,return None
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

def markdown_to_text(md):
    html=markdown2.markdown(md)
    soup=BeautifulSoup(html,"html.parser")
    return soup.get_text().strip()
