import random
answers = ('Yes','No','Maybe')

def charivna_kulka(question):
 if type(question)!= str:
  raise Exception('Enter normal question')
 

 if len(question) == 0:
  raise Exception('Value is empty')
 

     
 return f'{question} : {random.choice(answers)}'

print(charivna_kulka("Gas prices will rise?"))

   