from copy import deepcopy
#parse the file and return all the trimmed out text
class SatSolver:
    def __init__(self):
        self.solutionVars = {}
        self.matrix = []
        self.numVariables = 0

    def solveFile(self, fileName):
        lineArray = readFile(fileName)
        for line in lineArray:
            xArray = [toBoolean(entry) for entry in line.split(' ')]
            self.matrix.append(xArray)
        self.numVariables = len(self.matrix[0])
        print(self.dpllSatisfiable())

    def dpllSatisfiable(self):
        model = {}
        result, model = self.dpll(self.matrix, model)
        print(model) 
        return result 

    def checkTerminal(self, matrix, model):
        #check all lines against model
        countTrue = 0
        countFalse = 0
        countInconclusive = 0

        for line in matrix:
           result = self.evalLine(line, model)
           if result == True:
               countTrue += 1
           elif result == False:
               countFalse += 1
           else:
               countInconclusive += 1

        if countFalse > 0: 
            return False
        if countTrue == len(matrix):
            return True
        else:
            return None 
 
    def evalLine(self, line, model):
        #if there are any 1s in the line, then it is true
        unmodeled = self.findUnmodeled(model)
        countFalse = 0
        countUnmodeled = 0
        for var, value in model.items():
            if line[var] != None and self.setValue(value, line[var]) == True:
                return True
        #if there are all FALSE or None, return true
        for var in unmodeled:
            if line[var] != None:
                return None
            
        return False 
                   
        #return true and a model, OR return false
    def dpll(self, matrix, model):
        #if every clause in clauses is true in model then return true
        #if some clause in clauses is false in model then return false 
        terminal = self.checkTerminal(matrix, model)
        if terminal != None:
            return terminal, model

        pureSymbol, val = self.findPureSymbol(model)
        if pureSymbol != None:
            model[pureSymbol] = val #putting model as the same val as in the matrix will make it true
            newMatrix = self.evalModel(matrix, model)
            return self.dpll(newMatrix, model)
            #add pure symbol to model that makes it true
        #DONE if pureSymbols not null then return DPLL(clauses, symbols, model)
        #p, value = FindUnitClause(clauses, model)
        #if p is not null then return DPLL(clauses, symbols - P, model U {P=value})
        
        #choose a symbol that's not in model
        unmodeled = self.findUnmodeled(model)
        if len(unmodeled) > 0:
            modelFalse = deepcopy(model)
            model[unmodeled[0]] = True
            trueMatrix = self.evalModel(matrix, model)
            res1, model1 = self.dpll(matrix, model)
            modelFalse[unmodeled[0]] = False
            res2, model2 = self.dpll(matrix, modelFalse)
            if res1 == True:
                return res1, model1
            if res2 == True:
                return res2, model2
            else:
                return res1, model1 
            
        else:
            print("unsatisfiable")
            print("possible bug if we got to here, there should be stuff unmodeled")

        #P = first(symbols; rest = REST(symbols)
        #return DPLL(clauses, rest, model U {P=true} or
        #DPLL(clauses, rest, model U {P=false}
    
    def setValue(self, symbol, value):
        #if we have a symbol that is ~ and a value that is false. It'd be ~false, which is true
        #if we have a symbol that is true (x1) and a value that is false, then it's false
        #if we have a symbol that is false (~x1) and a value that's true, then it's ~true, which is false
        #if we have a symbol that's true and a value that's true, return true
        return symbol == value

    def evalModel(self, matrix, model):
        matrixCopy = deepcopy(matrix)
        for var, value in model.items():
            for row in matrixCopy:
                if row[var] != None:
                    row[var] = self.setValue(row[var], value)
        return matrixCopy

    def findUnmodeled(self, model):
        unmodeled = []
        for i in range(0, self.numVariables):
            if i not in model:
                unmodeled.append(i)
        return unmodeled            

    def findUnitClause(self, model):
        #assume model is just a dictionary  with filled in values to true or false
        #fill in a copy of the matrix
        unmodeled = self.findUnmodeled(model)
        matrixCopy = deepcopy(self.matrix)
        indexDict = {}

        for var, value in model.items():
            for row in matrixCopy:
                if row[var] != None:
                    row[var] = self.setValue(row[var], value) 
        
        for row in matrixCopy:
            count = 0
            resultVar = None
            for var in unmodeled:
                if row[var] != None:
                    count += 1
                    resultVar = var
            if count == 1:
                return resultVar
        
        return None                 

    #for each variable, look for all true-false pairings of that variable. Then set them to '-' or None    
    def removeTrueFalsePairings(self):
        pass

    def findPureSymbol(self, model):

        matrix = self.matrix

        for var in list(set(range(0, self.numVariables)) - set(model.keys())): #this is to prevent us iterating over stuff already in the model
            prev = matrix[0][var]
            current = matrix[0][var] 
            count = 0
            for row in matrix:
                if current != None:
                    prev = current
                if row[var] != None:
                    current = row[var]
                if prev != current:
                    break
                count += 1
            if count == len(matrix):
                return var, matrix[0][var]        
        return None, None                
            
    #check if every clause is true, every clause is false. 
           
def toBoolean(char):
    if char == '1':
        return True
    elif char == '0':
        return False
    else:
        return None

def toChar(boolean):
    if boolean == True:
        return '1'
    elif boolean == False:
        return '0'
    else:
        return '-'

def readFile(fileName):
        lineArray = []
        f = open(fileName, 'r')
        for line in f.readlines():
            line = line.strip()
            if line[0] != "#":
                if "#" in line:
                    line = line[:line.index("#")].strip()
                lineArray.append(line)
        print(lineArray)
        return lineArray

def main():
    satSolver = SatSolver()
    satSolver.solveFile("NV-SAT1-Example1.txt")
 
main()
