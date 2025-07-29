
from flask import Flask, request, jsonify
import requests
import json
from dataclasses import dataclass
from typing import List
import re

app = Flask(__name__)


@dataclass
class Metadata:
    width: int
    height: int

@dataclass
class BoundingPolygon:
    x: int
    y: int

@dataclass
class Word:
    text: str
    boundingPolygon: List[BoundingPolygon]
    confidence: float  

@dataclass
class Line:
    text: str
    boundingPolygon: List[BoundingPolygon]
    words: List[Word]    

@dataclass
class Block:
    lines: List[Line]

@dataclass
class ReadResult:
    blocks: List[Block]

@dataclass
class AnalyzeResult:
    modelVersion: str
    metadata: Metadata
    readResult: ReadResult

@dataclass
class AnalyzeRequest:
    uri: str

class OCR:
    def recognize_text(self, file_bytes):
        # For prod environment, please find the endpoint and resource key of your computer vision resource from Azure portal.
        endpoint = 'cognitiveservices.azure.com/'                                                                                       #Here should be our company's endpoint from the profile of computer vision
        url = f"{endpoint}computervision/imageanalysis:"
        key = 'Keykeykeykey'                                                                                                            #Here should be our company's key from the profile of computer vision

        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Content-Type': 'application/octet-stream'
        }

        
        response = requests.post(url, headers=headers, data=file_bytes)
        response_content = response.text

        # Deserialize and print the result
        data = json.loads(response_content)
        try:
            deserialized_object = self.from_dict(AnalyzeResult, data)
            result_words = []
            for block in deserialized_object.readResult.blocks:
                for line in block.lines:
                    for word in line.words:
                        result_words.append(word.text)
                        print(f"Word Text: {word.text},Confidence: {word.confidence}")                  ######if we want to see those words in console
              #Below you can see filter that filteres everything that doesn't match the pattern given, you can see the example of this pattern in coment on the right of each filter              
                pattern = re.compile(
        r"^\d{2}-[A-Z]{2}-[\w\d]+$"             # f.ex 82-AB-123
        r"|^\d{2}-[A-Z]\d-[\w\d]+$"             # f.ex 82-C2-123A
        r"|^\*\d{2}-[A-Z]{2}-[\w\d]+$"          # f.ex *82-AB-123
        r"|^\d{2}-[\w\d]{2}-[\w\d]+/[\w\d]+$"     # f.ex 182-C2-123A/B
                                    )

            matched = [word for word in result_words if pattern.match(word)]
            print (len(matched))                                              ### Just for debugging process, i was comparing known number of tags on drawing to result given by my filter
            
            return {
            "tags": matched,
            "tags count": len(matched)
                    }
            # return result_words                                           #######if we want to see those words in console with uncommented line 77
            
                   
        except KeyError as e:
            print(f"KeyError: {e}. Please check the JSON response structure.")

    def from_dict(self, data_class, data):
        if isinstance(data, list):
            return [self.from_dict(data_class.__args__[0], item) for item in data]
        if isinstance(data, dict):
            fieldtypes = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
            return data_class(**{k: self.from_dict(fieldtypes[k], v) for k, v in data.items()})
        return data

 
ocr = OCR()

@app.route("/ocr", methods=["POST"])

def ocr_endpoint():
    if request.content_type == 'application/octet-stream':
        file = request.data
    elif 'image' in request.files:
        file = request.files['image'].read()
    else:
        return jsonify({"error": "No file uploaded"}), 400
    result = ocr.recognize_text(file)
    return jsonify(result)          ### Returns JSON to our Express.js server

# Usage example
if __name__ == "__main__":
    app.run(debug=True, port=5000)
    # ocr = OCR()
    # ocr.recognize_text()


