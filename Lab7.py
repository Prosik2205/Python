import random
answers = ["Yes","No","Maybe"]

def charivna_kulka(question):
 if type(question)!= str:
  raise Exception('Enter normal question')
 
 if len(question) == 0:
  raise Exception('Value is empty')
 
 return f'{question} : {random.choice(answers)}'

def configure_magic_ball(new_answers: list):
    for new_answers in new_answers:
      position = random.randint(0,len(answers))
      answers.insert(position,new_answers)

configure_magic_ball(["Yeah man","No way","Think yourself"])  
    
    
print(charivna_kulka("Gas prices will rise?"))

   