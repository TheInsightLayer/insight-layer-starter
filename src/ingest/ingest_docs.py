import sys
from pathlib import Path

def ingest_markdown(filepath):
    with open(filepath, 'r') as f:
        return f.read()

if __name__ == '__main__':
    # NOTE: Although the input is Markdown (.md), we save the raw content as a .txt for simplicity
    content = ingest_markdown(sys.argv[1])
    Path("data/raw_text.txt").write_text(content)
