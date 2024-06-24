PageRank Algorithm Implementation

This Python script computes PageRank values for a corpus of web pages using both sampling and iterative methods.

Overview:

crawl: Parses HTML pages to extract links between them.
transition_model: Generates a probability distribution for the next page a random surfer would visit.
sample_pagerank: Estimates PageRank using sampling from the transition model.
iterate_pagerank: Calculates PageRank iteratively until convergence.

Usage:

Clone the repository:
bash
Copy code
git clone <repository-url>
cd pagerank
Run the script with a corpus directory:
Copy code
python pagerank.py corpus
Replace corpus with your directory containing HTML files.

Files:

pagerank.py: Main script with PageRank algorithms.
README.md: This file, providing setup, usage, and contribution details.
corpus0: file with 4 html file 
corpus1: corpus file with 7 html files 
corpus2: corpus with 8 html files

Contributing:

Contributions are welcome via pull requests. Please discuss changes by creating an issue first.
