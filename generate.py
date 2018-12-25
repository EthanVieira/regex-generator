import re

# get rid of repetitions n steps away
def shrink(inputStr, nbSteps):
    idx = 0
    output = ""
    while idx < len(inputStr):
        print(idx)

        # get the current letter and append to output
        letter = inputStr[idx:idx+nbSteps]
        print("letter:", letter)

        # get the index of the next character
        innerIdx = idx + nbSteps

        # get tokens n steps long and compare with current token
        compLetter = inputStr[innerIdx:innerIdx+nbSteps]
        print("compLetter:", compLetter)
        isSkipped = False
        while compLetter == letter:
            innerIdx += nbSteps
            isSkipped = True
            if innerIdx > len(inputStr):
                break
            compLetter = inputStr[innerIdx:innerIdx+nbSteps]

        # if any character was skipped, add + token
        if isSkipped:
            output += "(" + letter + ")+"
            isSkipped = False
            idx = innerIdx
        # set the index to reflect the skip
        else:
            output += letter[0]
            idx += 1

    return output

# compose a [max strlen] x [# of strings] char matrix given input strings
def composeMatrix(inputStrings):
    # initialize a list with the length of the input strings
    inputStringsLen = [len(s) for s in inputStrings]

    # get the maximum string length
    maxStrLen = 0
    for s in inputStrings:
        maxStrLen = max(inputStringsLen)

    # create the matrix of input string characters
    m = [[] for x in range(maxStrLen)]
    for row in range(maxStrLen):
        for s in inputStrings:
            if row < len(s):
                m[row].append(s[row])
            else:
                m[row].append("EOS")

    return m

# check if all items in a list are the same item
def hasSameItem(row):
    return all(item == row[0] for item in row)

# compare all input strings and compile a general regex
def createCommPattern(inputStrings):
    # sort the input strings by length
    inputStrings.sort(key=len, reverse=True)

    # check which case the input strings fall into
    areSameLength = all(len(s) == len(inputStrings[0]) for s in inputStrings)
    print(areSameLength)

    # initial variables
    commPattern = ""
    inputMatrix = composeMatrix(inputStrings)
    idxAdjustments = [0 for x in range(len(inputMatrix[0]))]

    # if the input strings have the same length, don't use any adjustments
    if areSameLength:
        for rowIdx, row in enumerate(inputMatrix):
            if hasSameItem(row):
                commPattern += row[0]
            else:
                commPattern += "["
                for item in row:
                    commPattern += item
                commPattern += "]"
        return commPattern

    # loop through each row in the matrix
    for rowIdx, row in enumerate(inputMatrix):
        # make the adjusted row
        adjustedRow = []
        for i in range(len(row)):
            adjustment = idxAdjustments[i]
            if rowIdx + adjustment >= len(inputMatrix):
                return commPattern
            adjustedRow.append(inputMatrix[rowIdx + adjustment][i])

        # skip rows
        if hasSameItem(adjustedRow):
            print(adjustedRow)
            if adjustedRow[0] == "EOS":
                return commPattern

            commPattern += adjustedRow[0]
            continue

        # try naive approach: if not same letter, skip to next row
        adjustment = idxAdjustments[0]
        while inputMatrix[rowIdx+adjustment][0] != row[1]:
            commPattern += inputMatrix[rowIdx+adjustment][0] + "?"
            adjustment += 1

            if (rowIdx+adjustment) >= len(inputMatrix):
                print("?????")
                return commPattern

        idxAdjustments[0] = adjustment

        # make the adjusted row
        adjustedRow = []
        for i in range(len(row)):
            adjustment = idxAdjustments[i]
            if rowIdx + adjustment >= len(inputMatrix):
                return commPattern
            adjustedRow.append(inputMatrix[rowIdx + adjustment][i])

        # print the result
        if adjustedRow[0] == "EOS":
            return commPattern
        commPattern += adjustedRow[0]
        print(adjustedRow)

    return commPattern

if __name__ == '__main__':
    ### Test 1 ###
    print("Testing shrink():")

    # initial variables
    inputStr = "aaaaaaaabcabcabca"
    maxChars = len(inputStr) / 2

    # tests
    output = shrink(inputStr, 1)
    output = shrink(output, 2)
    output = shrink(output, 3)

    # print the resulting shortened regex string
    print("Result:", output)


    ### Test 2 ###
    print("Testing composeMatrix():")
    inputStrings = ["aabc", "abc"]
    m = composeMatrix(inputStrings)
    print(m)


    ### Test 3 ###
    print("Testing createCommPattern():")
    inputStrings = ["sed", "abc"]
    commPattern = createCommPattern(inputStrings)
    print(commPattern)
