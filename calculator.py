def sum(a,b):
    print(a+b)

def min(a,b):
    print(a-b)    

def dob(a,b):
    print(a*b)    

def dil(a,b):
    while True:
        try:
            a/b
            break
        except ZeroDivisionError:
            print("You can't divide by zero. Please enter a new value for 'b'.")
            b = float(input("Enter a new value for b: "))  
            
    print(a/b)  
      

while True:
    try:
        num1 = float(input("Write first number:"))
        num2 = float(input("Write second number:"))
        break
    except Exception as e:
        print("Write correct number")

while True:
    x = input("Choose operation:\n1.sum\n2.min\n3.dobn\n4.dil\n0.Exit\n")
    # x = input("""Choose operation:
    #           1.sum
    #           2.min
    #           3.dobn
    #           4.dil
    #           0.Exit\n""")

    match(x):
        case'1':
            sum(num1,num2)
        case'2':
            min(num1,num2)
        case'3':
            dob(num1,num2)
        case'4':
            dil(num1,num2)
        case'0':
            break            
        case _:
            print("Something wrong")
          