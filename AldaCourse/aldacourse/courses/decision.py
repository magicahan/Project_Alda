'''
---------------------------------------------------------------------------
CAPP 30122: AldaCourse
Python Version: 3.5
Seed: None

This is a Python script for CAPP 30122 for the final project named AldaCourse. 
decision.py is a the script used to build the actual schedules using the 
utility script called builder.py in the same direcctory
---------------------------------------------------------------------------
The current script defines the following functions:
    * combinations()
    * clean_conflicts()
    * create_schedule()
---------------------------------------------------------------------------
'''
from .builder import *
import itertools

# this python script is used to determine:
    # 1. obtain all possible combinations given a list of courses
    # 2. generate schedules for combinations that do not have conflict
    #    while discard courses for combination that do have conflicts

def combinations(course_list):
    '''
    This function identifies all possible combinations of three courses
    '''
    # identify unique courses
    unique_ccn = set()
    for course in course_list:
        unique_ccn.add(course[0])

    mapping = {key:[] for key in unique_ccn}

    for index, course in enumerate(course_list):
        mapping[course[0]].append(index)
    
    all_combinations = list(itertools.product(*mapping.values()))

    return all_combinations


def clean_conflicts(course_list):
    '''
    remove all conflict triplets
    '''
    combos = combinations(course_list)
    conflicts = []

    for combo in combos:
        triplet = [course_list[i] for i in combo]
        course1, course2, course3 = triplet
        
        # get course time information
        course1_info = course_info(course1[-1])
        course2_info = course_info(course2[-1])
        course3_info = course_info(course3[-1])

        for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
            if day in course1_info[0]:
                start1, end1 = course1_info[1:3]
            if day in course2_info[0]:
                start2, end2 = course2_info[1:3]
            if day in course3_info[0]:
                start3, end3 = course3_info[1:3]
    
            # course1 benchmark comparing with course2
            if start2 < start1 < end2 or start2 < end1 < end2:
                conflicts.append(combo)    
            # course1 benchmark comparing with course3
            if start3 < start1 < end3 or start3 < end1 < end3:
                if combo not in conflicts:
                    conflicts.append(combo)
            # course2 benchmark comapring with course3
            if start3 < start2 < end3 or start3 < end2 < end3:
                if combo not in conflicts:
                    conflicts.append(combo)
    if len(set(conflicts)) > 0:
        for element in list(set(conflicts)):
            combos.remove(element)
    return combos


def create_schedules(example_list):
    '''
    THis function takes a list of courses and would generate all feasible 
    schedules in spreadsheet (xlms) format
    '''
    combos = clean_conflicts(example_list)

    file_names = []
    for i in range(1, len(combos) + 1):
        file_names.append('schedule' + str(i) + '.xlsx')

    for triplet, file_name in zip(combos, file_names):
        course_list = [example_list[i] for i in triplet]
        builder(course_list, file_name)

    if combos == []:
        return 0
    else:
        return len(combos)
