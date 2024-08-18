from PIL import Image
from pytesseract import pytesseract
import enum
import os
from pdf2image import convert_from_path
import openai

openai.api_key = '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'


def pdftoimage(pdfpath):
    poppler_path = r'C:\Program Files\poppler-23.05.0\Library\bin'
    # Store Pdf with convert_from_path function
    images = convert_from_path(pdfpath)
    os.makedirs(pdfpath.rstrip('.pdf'), exist_ok=True)
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(os.path.join(pdfpath.rstrip('.pdf'), 'page'+ str(i) + '.jpg'), 'JPEG')
    return pdfpath.rstrip('.pdf')


class OS(enum.Enum):
    Mac = 0
    Windows = 1


class Language(enum.Enum):
    ENG = 'eng'
    RUS = 'rus'
    ITA = 'ita'


class ImageReader:
    # We provide the setup in our initializer
    def __init__(self, os: OS):
        if os == OS.Mac:
            # Tesseract is already installed via Homebrew
            print('Running on: MAC\n')

        if os == OS.Windows:
            # This should be replaced with your own path to: tesseract.exe
            windows_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pytesseract.tesseract_cmd = windows_path
            print('Running on: WINDOWS\n')

    # Specify the image and language for the text you want to extract
    def extract_text(self, image: str, lang: Language) -> str:
        img = Image.open(image)
        extracted_text = pytesseract.image_to_string(img, lang=lang.value)
        return extracted_text


if __name__ == '__main__':
    totaltext = ''
    ir = ImageReader(OS.Windows)
    filepath = input("Please Enter File Path: ")
    nq = int(input("How many questions would you like? "))
    directory = pdftoimage(filepath)
    for page in os.listdir(directory):
        # Get the full path of the file
        page_path = os.path.join(directory, page)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(page_path):
            # Do something with the file

            # Multiple languages can be used with: 'eng+ita+rus'
            text = ir.extract_text(image=page_path, lang=Language.ENG)

            # Do some light processing before printing the text
            processed_text = ' '.join(text.split())
            totaltext += processed_text
    print(totaltext)
    res = sum(1 for _ in totaltext.split())
    while res > 2500:
        print("Sorry, the Data must be under 2500 words")
        print(f"Current Word Count:{res}\n")
        print(f"The Data\n\n{totaltext}\n")
        totaltext = input("Enter the updated totaltext: ")
        res = sum(1 for _ in totaltext.split())
    messagesbase = [{"role": "system", "content": "You are a assistant that listens to user."},
                    {"role": "user",
                     "content": f"here are my notes design me a {nq} question practice paper with multiple choice questioning each topic of the notes, the answers to the questions must be in the notes and provide all the answers in the end under answers"}]

    sampledict = {"role": "user"}
    sampledict["content"] = totaltext
    messagesbase.append(sampledict)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messagesbase
    )
    print(response)
    x = [y for y in response['choices'][0]["message"]["content"].split("Answers:")]
    print(x[0])
    z = input("If you are ready for the answers please type yes:  ")
    if z.lower() == "yes":
        print(x[1])


