import tkinter as tk
import pdfplumber
from tkinter import filedialog
import PyPDF2
import re
import nltk
import sumy
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

nltk.download('punkt')

def extract_text():
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, 'rb') as f:
            reader = pdfplumber.open(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        text_entry.delete(1.0, tk.END)
        text_entry.insert(tk.END, text)

def generate_summary():
    summary_length = 0
    length_text = length_entry.get()
    if length_text:
        try:
            summary_length = int(length_text)
        except ValueError:
            summary_length_label.config(text="Error: summary length must be an integer")
            return
    if summary_length <= 0:
        summary_length_label.config(text="Error: summary length must be greater than 0")
        return

    text = text_entry.get("1.0", tk.END)
    summary_text = summarize_text(text, summary_length)
    summary_label.config(text=summary_text)

def summarize_text(text, num_sentences):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    summary_text = ""
    for sentence in summary:
        summary_text += "\u2022 " + str(sentence) + "\n"
    return summary_text

root = tk.Tk()
root.title("Text Summarization Tool")

text_label = tk.Label(root, text="Enter text or select a file:")
text_label.pack()

text_entry = tk.Text(root, height=10, width=50)
text_entry.pack()

length_label = tk.Label(root, text="Enter summary length:")
length_label.pack()

length_entry = tk.Entry(root, width=10)
length_entry.pack()

summary_length_label = tk.Label(root, text="")
summary_length_label.pack()

button = tk.Button(root, text="Select a file", command=extract_text)
button.pack()

summary_button = tk.Button(root, text="Generate summary", command=generate_summary)
summary_button.pack()

summary_label = tk.Label(root, text="")
summary_label.pack()

root.mainloop()