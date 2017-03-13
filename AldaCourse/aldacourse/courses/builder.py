'''
---------------------------------------------------------------------------
CAPP 30122: AldaCourse
Python Version: 3.5
Seed: None

This is a Python script for CAPP 30122 for the final project named AldaCourse. 
builder.py is a utility script used to build the schedules using the list
of courses users input.
---------------------------------------------------------------------------
The current script defines the following functions:
    * time_calculator()
    * course_info()
    * merger_pattern() 
    * write_schedule()
    * builder() 
---------------------------------------------------------------------------
'''
import openpyxl
from openpyxl import load_workbook
import re
import numpy as np

wb =load_workbook(filename = 'template.xlsx')
template = wb.active


def time_calculator(time):
    '''
    This function is used to convert time format
        for example: 13:30 to 13.5
    '''
    hours = int(time)
    hours_decimal = round(time - int(time), 1)
    mins = hours_decimal * 100 / 60
    hours_float = hours + mins
    return hours_float
    

# get the number of cells spans of that particular course
def course_info(time):
    '''
    This function is to convert course information to desired data structure
    input: time = '12:30 PM-01:00 PM'
    return: (12.5, 13.0, 1.0, 1)
    '''
    span_nums_str = re.findall('\d+', time)
    end_time = float(span_nums_str[-2] + '.' + span_nums_str[-1])
    start_time = float(span_nums_str[0] + '.' + span_nums_str[1])
    AM_PM = re.findall('(AM|PM)', time)
    days = re.findall('(Mon|Tue|Wed|Thu|Fri|Sat|Sun)', time)

    if AM_PM[0] == 'PM' and int(start_time) != 12:
        start_time += 12
    if AM_PM[-1] == 'PM' and int(end_time) != 12:
        end_time += 12

    # time conversion
    end_time = time_calculator(end_time)
    start_time = time_calculator(start_time)

    # convert to hours
    num_hours = end_time - start_time
    # convert to minutes
    num_mins = round(num_hours * 60, 0)
    # convert to 30mins
    num_15mins = num_mins / 15

    #special case
    if num_15mins - int(num_15mins) != 0:
        num_15mins += 1
    num_cells = round(num_15mins, 0)

    return days, start_time, end_time, num_mins, num_cells


# get a list of all time slots
time_cells = []
for index in range(3, 60, 2):
    time_cells.append('A' + str(index))

# get a list of time slots corresponding the the number of cells
time_slots = []
for cells in time_cells:
    time_slots.append(template[cells].value)

################### Matching days to columns ###################
days_map = {'Mon':'B', 'Tue':'C', 'Wed':'D', \
            'Thu':'E', 'Fri':'F', 'Sat':'G', 'Sun':'H'}


################## Matching times to rows ###################
slots_map = {}
for slots, index in zip(time_slots, range(3, 60, 2)): 
    days, start_time, end_time, \
            num_mins, num_cells = course_info(slots)
    slots_map[start_time] = index # need to count title rows


def merger_pattern(days, start_time, num_cells):
    '''
    This function takes in the days and the start_time of a course, and it 
    would figure out the location and the number of excel cells that particular
    course would occupy
    '''
    cols = []
    for day in days:
        cols.append(days_map[day])
    
    starting_row= int(slots_map[start_time])
    ending_row = int(starting_row + num_cells - 1)

    merge_patterns = []
    starting_cells = []
    for col in cols:
        starting_cells.append(col+str(starting_row))
        merge_patterns.append(col+str(starting_row)\
                                +':'+col+str(ending_row))
    return starting_cells, merge_patterns


def write_schedule(template, starting_cells,\
                    merge_patterns, course):
    '''
    This function is used to write the actual course information to the 
    spreadsheet template
    '''
    ccn, name, loc, time = course
    days, start_time, end_time, num_mins, \
            num_cells = course_info(time)
    content = name + '\n' + '\n' + 'Location: ' + loc
    # merge cells and write it
    for start, pattern in zip(starting_cells, merge_patterns):
        template.merge_cells(pattern)
        template[start] = content


def builder(course_list, file_name):
    '''
    This function is used to build the course schedules using all auxiliary
    function composed above
    '''
    wb =load_workbook(filename = 'template.xlsx')
    template = wb.active

    for course in course_list:
        ccn, name, loc, time = course
        days, start_time, end_time, \
                num_mins, num_cells = course_info(time)
        starting_cells, merge_patterns = merger_pattern(days, \
                                                        start_time,\
                                                        num_cells)
        write_schedule(template, starting_cells, \
                       merge_patterns, course)

    wb.save(file_name)
