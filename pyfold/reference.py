import requests

### Meta's PoC Database of Proteins & Fast folding model
url = "https://api.esmatlas.com/foldSequence/v1/pdb/"


def reference_fold(sequence):
    return requests.post(url, data=sequence).text
