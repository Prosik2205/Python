import random

def charivna_kulka(question):
 if type(question)!= str:
  raise Exception('Enter normal question')
 answers = ('Yes','No','Maybe')
     
 return f'{question} : {random.choice(answers)}'

def test():
 result = charivna_kulka("value")
 assert isinstance(result,str) 

print(charivna_kulka("Tolik pidor?"))     