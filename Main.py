import string
import os

def split_file_name(file_name):
  """Splits a file name into chunks of 256 characters."""

  chunks = []
  for i in range(0, len(file_name), 256):
    chunks.append(file_name[i:i + 256])
  return chunks

def main():
  """Splits the file name and prints the chunks."""

  file_name = "BQA-As4Ak-YjE5y8wvvST3R-hVopvyZsClr96OrsrsQ3zW2oZqCFrHjIzZ4YbgV_PnySgPfdN0PH21jb3D8Aq1aM_2aLhZtaW-IrQOOwVd6Ato-QpjBj5xeUM_KoZKDQBt5605Bbwf5TMGSxnNzNY00oqawl5nDXMbb0cSZaPpp7WxoSeZB0wzLj-pkjlBxHuWIw71tG1UmuDZ9h9xj2bdrviKJ1XgDBDbXkySoRgCUqlJwbc_uFzGEBUOVNU_hdJ_vIMNJgXrk8-v2j_9EA-KX-0i-r1dgJgKhQHGznPm6eUPe57bof7n2z6BINS-HLls7FPQZU24pJT1tfoC0zYzggYpXgmAAAAABFr3zOAA"
  chunks = split_file_name(file_name)
  for chunk in chunks:
    print(chunk)

if __name__ == "__main__":
  main()
  
