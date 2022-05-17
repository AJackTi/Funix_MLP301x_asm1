import re
import numpy as np

answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"


def FileCheck(filename):
    try:
        f = open(filename, "r")
        print("Successfully opened {}".format(filename))
        return [line.rstrip() for line in f.readlines()]
    except IOError:
        print("File cannot be found.")
        return None


def DataCheck(data):
    lstValid = []
    lstInvalid = []
    for line in data:
        lstLine = line.split(",")
        if ValidLength(lstLine):
            lstInvalid.append(line)
            continue
        if not ValidRegex(lstLine[0]):
            lstInvalid.append(line)
            continue

        lstValid.append(line)

    return (lstValid, lstInvalid)


def ValidLength(lstLine):
    return len(lstLine) != 26


def ValidRegex(str):
    reg = re.findall(r"^N[0-9]{8}", str)
    return len(reg) != 0


def CalculateScore(lstAnswerKey, lstAnswer):
    score = 0

    for i in range(0, len(lstAnswer)):
        if lstAnswer[i] == "":
            score += 0
        elif lstAnswer[i] == lstAnswerKey[i]:
            score += 4
        elif lstAnswer[i] != lstAnswerKey[i]:
            score -= 1

    return score


def CalculateScoreClass(data):
    lstAnswerKey = answer_key.split(",")
    lstStudents = []
    lstScores = []
    for line in data:
        lstAnswer = line.split(",")[1:]
        id = line.split(",")[0]

        score = CalculateScore(lstAnswerKey, lstAnswer)
        student = Student(id, score)
        lstStudents.append(student)
        lstScores.append(score)

    return (lstStudents, lstScores)


class Student:
    def __init__(self, id, score):
        self.id = id
        self.score = score


def ExportResult(fn, data):
    with open(fn, 'w') as f:
        for item in data:
            f.write("%s,%s\n" % (item.id, item.score))


if __name__ == '__main__':
    filename = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
    filename = "{}.txt".format(filename) if "txt" not in filename else filename
    data = FileCheck(filename)

    if data != None:
        print("**** ANALYZING ****")
        lstValid, lstInvalid = DataCheck(data)
        if len(lstInvalid) == 0:
            print("No errors found!")
        else:
            for errLine in lstInvalid:
                if not ValidLength(errLine):
                    print("Invalid line of data: does not contain exactly 26 values:")
                    print("".join(str(x) for x in errLine))
                elif not ValidRegex(errLine[0]):
                    print("Invalid line of data: N# is invalid")
                    print("".join(str(x) for x in errLine))

        print("**** REPORT ****")
        print("Total valid lines of data: {}".format(str(len(lstValid))))
        print("Total invalid lines of data: {}".format(str(len(lstInvalid))))

        lstStudents, lstScores = CalculateScoreClass(lstValid)
        lstScores.sort()
        np_score = np.array(lstScores)

        print("Mean (average) score:", np.mean(np_score))
        print("Highest score:", np.max(np_score))
        print("Lowest score:", np.min(np_score))
        print("Range of scores:", np.max(np_score) - np.min(np_score))
        print("Median score:", np.median(np_score))

        ExportResult("{}_grades.txt".format(filename.split(".")[0]), lstStudents)
