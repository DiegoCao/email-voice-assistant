'''
API for text summarization

https://deepai.org/machine-learning-model/summarization


'''

import requests
import io
import re

class Summarize():

    def __init__(self):
        pass

    def summarize(self, text, verbose=False):
        '''
        text:       either 'file', 'url' or 'raw', corresponding to a file handle, a url to text, or the raw text respectively
        returns:    a string containing the summary
        '''

        response = requests.post(
            "https://api.deepai.org/api/summarization",
            data={
                'text': text,
            },
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        )

        summary = response.json()['output']

        if verbose:
            print(summary)

        return summary

if __name__ == '__main__':
    summarizer = Summarize()
    text = """The section describes what data you will use for the project. For the update, you
            should already have the data on hand. You should describe the source of the data, how you obtained
            it, what type of preprocessing steps you took, and (if not sensitive data) include a few examples.
            We strongly encourage you to include some very rough statistics (e.g., how many instances you
            have, the class distribution if doing classification, relevance score distribution) in a table format.
            If you had to create your own dataset or needed to annotate a ground truth relevance, this section
            should specify how you did it and provide details on the relevance scores."""
    
    summarizer.summarize(text, verbose=True)

''' documentation

# Example posting a text URL:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_URL',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example posting a local text file:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    files={
        'text': open('/path/to/your/file.txt', 'rb'),
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


# Example directly sending a text string:

import requests
r = requests.post(
    "https://api.deepai.org/api/summarization",
    data={
        'text': 'YOUR_TEXT_HERE',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())


###############################################################################

import base64

# Let's use deepAI developed API
# https://docs.deepaffects.com/docs/text-summary-api.html

url = "https://proxy.api.deepaffects.com/text/generic/api/v1/async/summary"

querystring = {"apikey":"<API_KEY>", "webhook":"<WEBHOOK_URL>"}

payload = {"summaryType": "abstractive", "model": "iamus", "summaryData": [{"speakerId":"spk", "text":"text blob for speaker"}]}

headers = {
    'Content-Type': "application/json",
}

response = requests.post(url, json=payload, headers=headers, params=querystring)


'''