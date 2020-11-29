from io import StringIO
from collections import defaultdict

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

days = 'MTWRF'

def parse_text(text: str) -> list:
    """
    Return list of lists of lists (3D array).
    Each list contains the time slots for one day of the week, for one person, and each time slot is a list
    Element 0 means Monday, 1 is Tuesday... until Friday.
    [ [["10:00", "11:00"], ["09:00", "09:30"]] , [] ]
    """
    time_slots = [[]]*5
    # Messy stuff will go here.
    # Certain lines look like this Tue, Thu 3:30-4:50 PM;
    # I need to find them all and turn them into my desired output.
    return time_slots

def get_input():
    """
    Ask for number of people, and that number of pdf file directories.
    For each file, make an array of all busy time slots for each day.
    Squash all arrays, then sort the big array.
    """
    all_busy = defaultdict(list)
    
    persons = int(input('How many people, including yourself if applicable, must attend the meeting?'))
    for p in range(persons):
        filename = input('Directory to their LMS-generated pdf schedule please?')
        # filename = 'C:\\Users\\mouss\\Downloads\\StudentSchedule.pdf'
        # I can't see a pattern in this text :(

        filename = 'C:\\Users\\mouss\\Downloads\\All My Courses - Main View _ Learning Management System _ LMS _ Portal.pdf'
        # Much better pattern here though!

        output_string = StringIO()
        with open(filename, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        total_text = output_string.getvalue()
        print(total_text)

        # Now, look for all lines containing days of the week and a time slot,
        # and arrange these in an array of arrays, each for a day.
        time_slots = parse_text(total_text)

        for i, day_busy_slots in enumerate(time_slots):
            for slot in day_busy_slots:
                all_busy[days[i]].append(slot)
                # Each value in this dictionary is a list of lists.

    [all_busy[weekday].sort(key=lambda slot : slot[0]) for weekday in all_busy.keys()]
    
    return all_busy

def merge_slots(all_busy):
    """
    Return distinct blocks of busy times for each weekday.
    """
    distinct_blocks = defaultdict(list)
    for item in all_busy.items():
        [d, val] = item
        i = 0
        while (i < len(val) - 1):  ## Note that length changes constantly.
            this = val[i]
            nxt = val[i+1]
            [start1, end1] = this
            [start2, end2] = nxt
            if end1 < start2:
                # Strictly separate slots.
                i += 1
            else:
                new_slot = [min(start1, start2), max(end1, end2)]
                del val[i:i+2]
                val.insert(i, new_slot)
                # Do not increment i yet, you may still have some more merging to do.
                
        distinct_blocks[d] = val
        # print("distinct", distinct_blocks)
    return distinct_blocks

def find_gaps(distinct_blocks, min_dur=None):
    # Ignoring minimum duration constraint for now.
    
    gaps = default_dict(list)
    for item in distinct_blocks.items():
        [d, s] = item

        for i in range(len(s) - 1):
            gap_start = all_busy[i][1]
            gap_end = all_busy[i+1][0]
            gap = [gap_start, gap_end]
            gaps[d].append(gap)
    return gaps

if __name__ == '__main__':
    all_busy = get_input()
    distinct_blocks = merge_slots(all_busy)
    ans = input("Do you have a minimum duration for a meeting? 'y' or 'n'")
    if ans == 'y':
        min_dur = int(input('Minimum duration in minutes?'))
    gaps = find_gaps(distinct_blocks, min_dur)
    print("You can meet in the following time slots" , gaps)
