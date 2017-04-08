import csv
import re

filename = "issue_updated.csv"

total = 0
freeCnt = 0
noMatch = 0
priceAlone = 0
totalNonNull = 0
totalNull = 0
onlyPriceAndFranchiseCnt = 0

attribute = "price"

with open(filename) as f:
	reader = csv.DictReader(f)
	for row in reader:
		total += 1

		if re.search(r"\d{1,5}.?\d{0,5}\s{0,2}[A-Za-z]{3}", row[attribute]):
			onlyPriceAndFranchiseCnt += 1

		elif re.search(r"^\d{0,5}\.?\d{0,3}$", row[attribute]):
			priceAlone += 1

		elif re.search(r"free", row["price"], re.IGNORECASE) or row["price"] in ["gratis", "Gratis", "0.00", "None [Giveaway]", "[gratis]", "[Gratis]"]:
			freeCnt += 1

		elif row["price"] != "NULL":
			noMatch += 1
			print(row["price"])
			
		elif row["price"] == "NULL":
			totalNull += 1

totalNonNull = total - totalNull

print()
print("=========================")
print("""TOTAL = {}""".format(total))
print("""TOTAL NULL = {}""".format(totalNull))
print("""TOTAL NON NULL = {}""".format(totalNonNull))
print("PROPORTION ON PRICE TYPE ON NON NULL PRICE")
print("""onlyPriceAndFranchiseCnt = {} <=> {}%""".format(onlyPriceAndFranchiseCnt, round(onlyPriceAndFranchiseCnt/float(totalNonNull) * 100, 2)))
print("""free : {} <=> {}%""".format(freeCnt, round(freeCnt/float(totalNonNull) * 100, 2)))
print("""No match = {} <=> {}%""".format(noMatch, round(noMatch/float(totalNonNull) * 100, 2)))
print("""price without franchise = {} <=> {}%""".format(priceAlone, round(priceAlone/float(totalNonNull) * 100, 2)))
print("=========================")
print()