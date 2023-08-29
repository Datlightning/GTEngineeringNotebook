from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations']

# The ID of a sample presentation.
presentation_id = '1MByAuFt68_guBsYhRuF1cD7__42vdFLdM4oXA7aubwo'


def main():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elements in a sample presentation.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('slides', 'v1', credentials=creds)

        # Call the Slides API
        presentation = service.presentations().get(
            presentationId=presentation_id).execute()
        slides = presentation.get('slides')

        print('The presentation contains {} slides:'.format(len(slides)))
        for i, slide in enumerate(slides):
            print('- Slide #{} contains {} elements.'.format(
                i + 1, len(slide.get('pageElements'))))
    except HttpError as err:
        print(err)

#NO SLASHES IN DATES
def engineer_notebook_entry(date, accomplishments, goals, learning, reflection_question, reflection_answer):
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        pt350 = {
            'magnitude':350,
            'unit':"PT"
        }
        page_id = date + "engineeringnotebook"
        date_id = date + "datebox"
        acc_id = date + "accomplishments"
        goals_id = date + "goals"
        learning_id  = date + "learnings"
        question_id = date + "question"
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': '1',
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                    }
                }
            },
            {
                'createShape': {
                    'objectId': date_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': pt350,
                            'width': pt350
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            },
            {
                'insertText': {
                    'objectId': acc_id,
                    'insertionIndex': 0,
                    'text': date
                }
            },
            {
                'createShape': {
                    'objectId': acc_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': pt350,
                            'width': pt350
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 500,
                            'translateY': 200,
                            'unit': 'PT'
                        }
                    }
                }
            },
            {
                'insertText': {
                    'objectId': acc_id,
                    'insertionIndex': 0,
                    'text': accomplishments
                }
            }
            
        ]

        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print(f"Created slide with ID:"
              f"{(create_slide_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error


if __name__ == '__main__':
    main()