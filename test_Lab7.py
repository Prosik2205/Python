from Lab7 import charivna_kulka

def test_correct_answ():
 result_corr_answ = charivna_kulka("Gas prices will rise?")
 corr_answ = ['Yes','No','Maybe']
 assert result_corr_answ.split(": ")[1] in corr_answ
 
def test_non_str():
 result_non_str = charivna_kulka("Gas prices will rise?")
 assert isinstance(result_non_str,str)

def test_empty():
 result_empty = charivna_kulka("Gas prices will rise?")
 assert result_empty

def test_corretct_type():
  try:
   charivna_kulka("Gas prices will rise?")
  except Exception as e:
   raise TypeError(e)
 

