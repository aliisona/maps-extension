from intersections import *
import statistics
from collections import defaultdict
import matplotlib.pyplot as plt

crashes = []
crashCount = defaultdict(int)
with open(json_file, 'r') as f:
    data = json.load(f)
    for x in data.values():
        crashes.append(x[0])
    for x in crashes:
        crashCount[x] += 1

print(sorted(crashes))
print(statistics.mean(crashes))
print(statistics.median(crashes))

# how I got data
sorted_crashCount = dict(sorted(crashCount.items()))
print(sorted_crashCount)
# cut this out: 1: 11626, 2: 2701, 3: 1168, 

amountCrashses = {1: 11626, 2: 2701, 3: 1168, 4: 681, 5: 373, 6: 290, 7: 206, 8: 156, 9: 122, 10: 82,
                  11: 99, 12: 60, 13: 66, 14: 48, 15: 28, 16: 42, 17: 36, 18: 26, 19: 39, 20: 19,
                  21: 18, 22: 17, 23: 14, 24: 21, 25: 28, 26: 16, 27: 9, 28: 10, 29: 5, 30: 8, 31: 7,
                  32: 10, 33: 7, 34: 8, 35: 5, 36: 8, 37: 9, 38: 5, 39: 9, 40: 8, 41: 5, 42: 3, 43: 7,
                  44: 3, 45: 4, 46: 3, 47: 4, 48: 5, 49: 2, 50: 6, 51: 2, 52: 1, 53: 1, 55: 2, 56: 1,
                  58: 1, 59: 1, 60: 4, 61: 1, 62: 1, 64: 2, 65: 6, 66: 2, 67: 1, 69: 3, 70: 4, 71: 2,
                  72: 3, 73: 1, 74: 3, 76: 1, 77: 1, 78: 1, 79: 1, 80: 1, 82: 1, 83: 1, 84: 1, 86: 1,
                  87: 1, 88: 1, 90: 2, 91: 1, 92: 2, 94: 3, 96: 1, 97: 1, 98: 1, 100: 1, 102: 4, 108: 1,
                  110: 1, 113: 1, 116: 1, 122: 2, 127: 2, 128: 1, 131: 1, 133: 1, 135: 1, 141: 1, 148: 1,
                  156: 4, 166: 1, 185: 1, 225: 1, 226: 1, 236: 1, 324: 1, 334: 1, 350: 1, 368: 1, 396: 1,
                  398: 1, 439: 1, 486: 1, 566: 1, 595: 1, 630: 1, 667: 1, 716: 1, 1154: 1}

x = list(amountCrashses.keys())[1:]
y = list(amountCrashses.values())[1:]



plt.plot(x, y)

plt.xlabel('Keys (Crash ID)')
plt.ylabel('Values (Crash Count)')
plt.title('Crash Data Line Graph')


plt.show()
