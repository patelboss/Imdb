import string
import os
from config import SESSION 
def split_file_name(file_name):
  """Splits a file name into chunks of 256 characters."""

  chunks = []
  for i in range(0, len(file_name), 256):
    chunks.append(file_name[i:i + 256])
  return chunks

def main():
  """Splits the file name and prints the chunks."""

  file_name = SESSION
  chunks = split_file_name(file_name)
  for chunk in chunks:
    print(chunk)

if __name__ == "__main__":
  main()
  
