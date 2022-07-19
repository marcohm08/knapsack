def getDataInstance(testName):

    testName = repr(testName).replace("'", "")
    benefits = []
    weights = []

    with open(testName) as file:

        firstLine = True
        
        for line in file.readlines():
            
            data = line.split(" ")
            
            if firstLine:
                firstLine = False
                n = int(data[0])
                capacity = int(data[1])
                opt = int(data[2])            
            elif n > 0:
                n -= 1
                benefits = benefits + [int(data[0])]
                weights = weights + [int(data[1])]

    return capacity, opt, benefits, weights