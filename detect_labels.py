from google.cloud import vision


labelDict = {}

def create_label_dict(labelDict, labels, uri):
    """Create a label dictionary to look up images having the same label"""

    for label in labels:
        #Make label description all lowercase for easy lookup
        if label.description.lower() not in labelDict:
            labelDict[label.description.lower()] = {uri}
        else:
            labelDict[label.description.lower()].add(uri)
    
    return labelDict


def detect_labels_uri(uri, labelDict):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    create_label_dict(labelDict, labels, uri)

    print('Labels:')

    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


def look_up_by_label(label_text):
    """Look up images based on labels (user's input). Results are returned as Google Cloud URI links"""
    
    label_text.lower() #Turn user's text into lowercase for lookup

    if label_text in labelDict:
        print(f'Images for label "{label_text}":')
        for uri in labelDict[label_text]:
            print(uri)
    else:
        print(f'No images found for label "{label_text}"')