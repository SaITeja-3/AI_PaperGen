import openai

openai.api_key = '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'

filepath = input("Please Enter Filepath: ")
nq = int(input("How many questions would you like? "))
pdf = PyPDF2.PdfReader(filepath)

n = len(pdf.pages)
for i in range(0,n):
  page = pdf.pages[i]
  content = page.extract_text()

print(content)
def convert_to_single_line(text):
    single_line = ' '.join(text.split())

    return single_line

samplestring = convert_to_single_line(content)
print(samplestring)

res = sum(1 for _ in samplestring.split())
while res>2500:
  print("Sorry, the Data must be under 2500 words")
  print(f"Current Word Count:{res}")
  print(f"The Data \n {samplestring}")
  samplestring = input("Enter the updateed samplestring: ")
  res = sum(1 for _ in samplestring.split())
messagesbase = [{"role": "system", "content": "You are a assistant that listens to user."},
                {"role": "user", "content": f"here are my notes design me a {nq} question practice paper with multiple choice questioning each topic of the notes, the answers to the questions must be in the notes and provide all the answers in the end under answers"}]

sampledict = {"role": "user"}
sampledict["content"] = samplestring
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
