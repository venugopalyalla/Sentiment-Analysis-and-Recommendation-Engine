

def processReviewsFile(fname):
    with open(fname) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

def extractKeywords(content):
    keywordsList = content[0].split(',')
    keywordsList = [x.strip() for x in keywordsList]
    return keywordsList

def checkForKeyword(keyword, line):
    keywordSynonyms = keyword.split('-')
    for synonym in keywordSynonyms:
        synonym = synonym.lower()
        line.lower()
        if synonym in line.lower():
            return True

def analyzeLine(line):
    for keywords in keywordsList:
        if checkForKeyword(keywords, line):
            keyword = keywords.split('-')[0]
            lines = keywordsToReviewsMap.get(keyword)
            lines.append(line)


def analyzeReviews(content):
    for i in range(1, len(content)):
        curReview = content[i]
        lines = curReview.split('.')
        for line in lines:
            analyzeLine(line)

def createKeywordsToReviewsMap():
    keywordsToReviewsMap = {}
    for keywords in keywordsList:
        keywordSynonyms = keywords.split('-')
        keywordsToReviewsMap[keywordSynonyms[0]] =  []
    return keywordsToReviewsMap


fname = "data/s8/samsungS8ScreenProtector2AllReviews.csv"
content = processReviewsFile(fname)
keywordsList = extractKeywords(content)
keywordsToReviewsMap = createKeywordsToReviewsMap()
for key, value in keywordsToReviewsMap.iteritems() :
    print key, value
analyzeReviews(content)
print("==============================================================")
for key, value in keywordsToReviewsMap.iteritems() :
    print key, len(value)
    # outfile = open('data/S8/samsungS8ScreenProtector2' + key + 'AllReviews.csv', 'w')
    # outfile.write('\n'.join([str(myelement).replace(",","").replace("'","").replace("[","").replace("]","") for myelement in value]))


# with open('data/S8/samsungS8ScreenProtector2ProsProtection.csv', 'rb') as f:
#     reader = csv.reader(f)
#     PriceCons = list(reader)
#
# trainingFile = open('data/newS8/samsungS8ScreenProtector2ProsProtection.csv', 'w')
# trainingFile.write('\n'.join([str(myelement).replace(",","").replace("'","").replace("[","").replace("]","") for myelement in PriceCons]))



import csv
with open('data/s8/samsungS8ScreenProtector2ConsPrice.csv', 'rb') as f:
    reader = csv.reader(f)
    PriceCons = list(reader)

with open('data/s8/samsungS8ScreenProtector2ConsEaseOfUse.csv', 'rb') as f:
    reader = csv.reader(f)
    EaseOfUseCons = list(reader)

with open('data/s8/samsungS8ScreenProtector2ProsMaterial.csv', 'rb') as f:
    reader = csv.reader(f)
    MaterialPros = list(reader)

with open('data/s8/samsungS8ScreenProtector2ProsProtection.csv', 'rb') as f:
    reader = csv.reader(f)
    ProtectionPros = list(reader)

for key, value in keywordsToReviewsMap.iteritems() :
    if key == 'price':
        PricePros = [item.replace(",","") for item in value if item not in PriceCons]
    if key == 'use':
        EaseOfUsePros = [item.replace(",","") for item in value if item not in EaseOfUseCons]
    if key == 'material':
        MaterialCons = [item.replace(",","") for item in value if item not in MaterialPros]
    if key == 'protection':
        ProtectionCons = [item.replace(",","") for item in value if item not in ProtectionPros]

mProsFile = open('data/S8/samsungS8ScreenProtector2ProsPrice.csv', 'w')
mProsFile.write('\n'.join([str(myelement) for myelement in PricePros]))

spProsFile = open('data/S8/samsungS8ScreenProtector2ProsUse.csv', 'w')
spProsFile.write('\n'.join([str(myelement) for myelement in EaseOfUsePros]))

fConsFile = open('data/S8/samsungS8ScreenProtector2ConsMaterial.csv', 'w')
fConsFile.write('\n'.join([str(myelement) for myelement in MaterialCons]))

pConsFile = open('data/S8/samsungS8ScreenProtector2ConsProtection.csv', 'w')
pConsFile.write('\n'.join([str(myelement) for myelement in ProtectionCons]))
