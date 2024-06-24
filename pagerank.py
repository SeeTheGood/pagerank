import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    # Ininitialize all probabilities to (1 - d) / 
    probabilities = {p: (1-damping_factor)/num_pages for p in corpus}  

    if corpus[page]:    # If the page has links
        num_links = len(corpus[page])  # Number of links on the page
        for linked_page in corpus[page]:  # For each linked page 
            # Add the damping factor divided by the number of links to the linked page
            probabilities[linked_page] += damping_factor / num_links    
    else: 
        for p in corpus:   # If the page has no links, assign equal probability to all pages
            # Add the damping factor divided by the number of pages to all pages
            probabilities[p] += damping_factor / num_pages  
    return probabilities   


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize a dictionary to store the number of times each page is visited
    page_counts = {page: 0 for page in corpus}  

    page = random.choice(list(corpus.keys()))   # Choose a random page to start with

    for i in range(n):        # For each sample
        page_counts[page] += 1     # Increment the count of the current page
        # Get the transition model for the current page
        probabilities = transition_model(corpus, page, damping_factor)     
        page = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]
        # Calculate the page rank for each page
        page_rank = {page: count/n for page, count in page_counts.items()}     
    return page_rank                


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus) 
    # Initialize the page rank for each page to 1 / N
    page_rank = {page: 1 / num_pages for page in corpus} 
    d = damping_factor

    while True:   # Iterate until convergence
        # Initialize a new dictionary to store the new page ranks
        new_page_rank = {} 
        for page in corpus:  
            # For each page initialize the new rank to (1 - d) / N  
            new_rank = (1 - d) / num_pages   
            rank_sum = 0               

            for link in corpus:         # For each link
                if page in corpus[link]:    # If the page is in the links of the link 
                    # Add the page rank of the link divided by the number of links to the rank sum
                    rank_sum += page_rank[link] / len(corpus[link])        

                # Handle pages with no outgoing links
                if len(corpus[link]) == 0:                          
                    # If the link has no outgoing links     
                    rank_sum += page_rank[link] / num_pages   

            new_rank += d * rank_sum   # Add the damping factor times the rank sum to the new rank
            new_page_rank[page] = new_rank  # Update the new page rank                 

        # If the difference between the new rank and the old rank is less than 0.001 for all pages
        if all(abs
                (new_page_rank[page] - page_rank[page]) < 0.001 for page in corpus): 
            break

        page_rank = new_page_rank  # Update the page rank

    return new_page_rank        # Return the page rank


if __name__ == "__main__":               
    main()