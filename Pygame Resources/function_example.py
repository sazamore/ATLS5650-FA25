#=============================================
#      Simplest function
#=============================================

#========== Function Definition ================
def functionName():
    print("This is a task inside of a function.")
    x = 10 # this is a LOCAL variable, it exists ONLY inside of a function
    print(x) # this shows the value of x in the function!

# Running this block of code will store a task to a name.
# This code alone will not execute a task. 

# Deeper Learning
# What do you think will happen if you uncomment the line below?
# print(x) # note the color coding. Is this a recognized variable? Are there any indications of an error?

# Local Variables are local to the function definition block. They only exist briefly,
# while the code is being execuuted. Then they get destroyed.

# Global Variables are defined before the function definition and can be recognized
# inside and outside of the function block. Handy!

#========== Function Call ================
functionName() # note the syntax!

# running this line will execute the lines of indented code in the definition block


#=============================================
#    Function with a returned value
#=============================================

#========== Function Definition ================
def functionReturn():
    print("This is a function with a return value.")
    x = 10 + 10 # this is a LOCAL variable, it exists only when the function is called and deleted after
    return x # now this function has an output. See how it is called! 

# Having parameters makes the function flexible. You can use it in a 
# dynamic way by changing the inputs


#========== Function Call ================
functionReturn() # note the syntax!
savedVal = functionReturn() # you can store the returned value to a variable. Nifty.
print(savedVal) # see???

# Note that you do not HAVE to save the output of a function to a variable


#=============================================
#    Function with a single parameter
#=============================================

#========== Function Definition ================
def functionParam(x_value):
    print("This is a function with a single parameter.")
    x = x_value # this is a LOCAL variable, it now saves the value from the parameter
    print(x) # this shows the value of x in the function!

# Having parameters makes the function flexible. You can use it in a 
# dynamic way by changing the inputs


#========== Function Call ================
functionParam(15) # note the syntax!

# The value placed between parameters is an argument.
# Try changing the argument value and calling the function again.
# What happens?


#=============================================
#    Function with multiple parameters
#=============================================

#========== Function Definition ================
def sum2num(num1, num2):
    """This is a docstring. It should have information about what the function does,
    returns, and the parameters.
    num1 - the first number to be added. Should be int or float.
    num2 - the second number to be added. Should be int or float.
    returns sum of num1 and num2"""
    sum = num1 + num2 
    return sum # alternative: return num1 + num2

# This function can sum any two nuumbers and return the value!
# Hover over the function call below. See if you can find the docstring! Cool, huh?


#========== Function Call ================
sum2num(15,30) # these are arguments. They assign the value to the parameter name, and are used inside of the function.
print(sum2num(15,30)) # displays the outut of the function
sum = sum2num(5,6) # these are Positional Arguments. They assign values based on position.
keySum = sum2num(num2=40, num1=-2) # these are Key Arguments. They assign values based on the paramater name (called a key)

# Try breaking this code. What is the error if...
#     - you only enter  one parameter?
#     - you enter more than 2 parameters?
#     - you mispell the name of the parameter (line 85)?
