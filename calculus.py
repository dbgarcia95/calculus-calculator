#This is a derivative and integral calculator

def findTerms(exp):
#Takes an expression and splits it into its individual terms
    plusArr=exp.split('+')
    #Splits 2x^2-5x+3 into ['2x^2-5x', '3']
    minusArr=[]
    fullArr=[]
    
    for term in plusArr:
        if '-' in term:
        #Creates an array of the terms not caught by the previous split ['2x^2-5x', '3']==>['2x^2', '5x']
            secondArray=term.split('-')
            for i in secondArray:
                minusArr.append(i)
        else:
        #Start adding to the full list of terms
            fullArr.append(term)

    for term in minusArr:
        fullArr.append(term)
    return fullArr
    #Returns ['3','2x^2','5x']

def analyzeTerms(exp):
#Extract a term's coefficient, variable, and exponent for future manipulation
#Then sorts in descending exponential order
    terms=findTerms(exp)
    dissectedTermArray=[]
    coString=''
    exponent=''
    sortedTermArray=[]
    raisedTermArray=[]
    def basicPolySort(i):
        return int(i[2])
    
    for term in terms:
        dissectedTerm=[]
        if 'x' not in term:
        #Checks if term is only an integer
            dissectedTerm=[term]
        elif '^' not in term and 'x' in term:
        #Checks if term contains only a first-power variable
            if 'x'==term[0]:
                coString='1'
            #When no coefficient is written, sets it equal to 1
            else:
                coString=term[:term.index('x')]
                
            dissectedTerm.append(coString)
            dissectedTerm.append('x')
            
        elif 'x' in term and '^' in term:
        #Dissects exponential terms
            if 'x'==term[0]:
                coString='1'
            else:
                coString=term[:term.index('x')]
                
            dissectedTerm.append(coString)
            dissectedTerm.append('x')
            exponent=term[term.index('^')+1:]
            dissectedTerm.append(exponent)
        dissectedTermArray.append(dissectedTerm)

    for term in dissectedTermArray:
        if len(term)==3:
            raisedTermArray.append(term)

    raisedTermArray.sort(key=basicPolySort, reverse=True)
    #Sorts the terms in traditional descending polynomial order
    for term in raisedTermArray:
        sortedTermArray.append(term)
    for term in dissectedTermArray:
        if len(term)==2:
            sortedTermArray.append(term)
    for term in dissectedTermArray:
        if len(term)==1:
            sortedTermArray.append(term)

    return sortedTermArray   
    #5x^3-2x^2+3x-5 returns [['5', 'x', '3'], ['2', 'x', '2'], ['3', 'x'], ['5']]



#The Power Rule says that the derivative of ax^n is nax^n-1 and the antiderivative of x^n is ((x^n+1)/n+1)+C
def powerRuleDerivative(exp): #Applies the Power Rule
    terms=analyzeTerms(exp)
    fullDerArr=[]
    operators=[]
    operatorIndex=1
    for char in exp:
        if char=='+' or char=='-':
            operators.append(char)
        
    for term in terms:
        termDer=''
        if len(term)==2:
            termDer+=str(term[0])
        #The derivative of a*x is a
        elif len(term)==3:
            co=int(term[0])
            var=term[1]
            pwr=int(term[2])
            derCo= pwr*co
            derPwr= pwr-1
            if derPwr==1:
                termDer+= '%s%s' % (derCo, var)
            #Not necessary to write exponent of 1
            else:
                termDer+= '%s%s^%s' % (derCo, var, derPwr)

        if len(termDer)>0:
            fullDerArr.append(termDer)

    for x in operators:
        fullDerArr.insert(operatorIndex, x)
        operatorIndex+=2

    if fullDerArr[len(fullDerArr)-1]=='+' or fullDerArr[len(fullDerArr)-1]=='-':
        del fullDerArr[len(fullDerArr)-1]

    derivative=''.join(fullDerArr)

    return derivative
    #Takes 3x^3-7x^2+16x+7 and returns 9x^2-14x+16

#The chain rule states that the derivative of f(g(x))= f'(g(x))*g'x
#Example: d/dx (3x^2-7)^2 = 2*(3x^2-7)*6x or 12x(3x^2-7) or 36x^3-84x
def chainRuleDerivative(exp):
    if '(' != exp[0]:
        outerCo=int(exp[:exp.index( '(' )])
    else:
        outerCo= 1
    uVal=exp[exp.index( '(' ):exp.index( ')' )].replace( '(' , '' )
    #Extracts 3x^2-7
    uPrime=powerRuleDerivative(uVal)
    #Differentiates 6x, the inner value
    sub='%s%s' % (outerCo, exp[exp.index( '(' )+1:].replace(uVal, 'x').replace( ')', ''))
    #Creates the substituted function (3x^2-7)^2 ==> x^2
    subDer=powerRuleDerivative(sub)
    #Differentiates the outer value x^2 ==> 2x
    subDerTerms=analyzeTerms(subDer)[0]
    outerCoDer=int(subDerTerms[0])
    if len(subDerTerms)==3:
        outerPwrDer=int(subDerTerms[2])
        der='%s(%s)^%s(%s)' % (outerCoDer, uVal, outerPwrDer, uPrime)
    else:
        der='%s(%s)(%s)' % (outerCoDer, uVal, uPrime)
    
    return der

#Start of the actual program loop
while True:
    print('Enter a one-variable expression in descending exponential order\nto find its derivative with respect to x')
    print('Or type "exit" to exit the program')
    expression=input().lower()
    #Code to determine which rule(s) to apply to the given expression
    if expression=='e^x':
        print('e^x')
    elif expression=='exit':
        break
    elif '(' in expression and ')' in expression:
        print(chainRuleDerivative(expression))
    else:
        print(powerRuleDerivative(expression))
