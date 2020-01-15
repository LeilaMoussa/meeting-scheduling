## sort by start times

def takeFirst(slot):
    return slot[0]

## busy times on Friday

salima = [["14:40", "15:30"]]
ali = [["12:00", "12:50"], ["17:40", "19:20"]]
fz = []
reda = [["10:00", "10:50"], ["11:00", "11:50"]]
salma = [["10:00", "10:50"], ["14:40", "15:30"]]
youssef = [["09:00", "09:50"], ["10:00", "10:50"]]
othmane = [["11:00", "11:50"]]
imane = [["10:00", "10:50"], ["14:40", "15:30"]]

## find all common empty time slots

"""
1. merge all lists into one list containing all busy times, sorted by starting time ascendingly
 1.1. merge any two consecutive slots where (start1=start2 AND end1 = end2)
                                         OR (end2 < end1)
                                         OR (start1 = start2 AND end2 > end1)
                                         OR (end1 = start2)
                                         OR (start1 < start2 AND end1 = end2)
                                         OR (start2 > start1 AND end2 < end1)
2. return gaps
"""

allBusy = salima + ali + fz + reda + salma + youssef + othmane + imane
allBusy.sort(key = takeFirst)

i = 0
while (i < len(allBusy) - 1):  ## note that len changes constantly
    this = allBusy[i]
    _next = allBusy[i+1]
    start1, end1 = this[0], this[1]
    start2, end2 = _next[0], _next[1]
    if start1<start2 and end1<end2 and end1 != start2:
        ## strictly separate slots
        i += 1
    else:
        new_start = min(start1, start2)
        new_end = max(end1, end2)
        new_slot = []
        new_slot.append(new_start)
        new_slot.append(new_end)
        del allBusy[i:i+2]
        allBusy.insert(i, new_slot)  ## 'i' can be greater than len
        ## do not move on yet

gaps = []
for i in range(len(allBusy) - 1):
    gap_start = allBusy[i][1]
    gap_end = allBusy[i+1][0]
    gap = []
    gap.append(gap_start)
    gap.append(gap_end)
    gaps.append(gap)

## print("ans:" , gaps)
