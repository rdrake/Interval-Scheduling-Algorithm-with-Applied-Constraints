from course import *
import userpreferences


"""
def course_density(Schedule):
   weight = 0.
   counter = 0.
   for iCRN in Schedule:
        for jCRN in Schedule:
            for i in iCRN.timeslots:
                for j in jCRN.timeslots:
                    if ( (int(j.day)*10000+int(j.eTime))-(int(i.day)*10000+int(i.sTime)) )<=10:
                        counter+=1.0
                        weight+=1.0
   return weight/counter# return a float from -1 to 1
"""


def course_density(Schedule):
    weight = 0.
    counter = 0.
    for iCRN in Schedule:
        for jCRN in Schedule:
            for i in iCRN.timeslots:
                for j in jCRN.timeslots:
                    #mints=min(i.sTime)
                    #maxts=max(j.eTime)
                    if i.day==j.day: 
                        time = int(j.eTime) - int(i.sTime)
                        if time<=40:
                            weight+=1.
                            counter+=1.
    return weight/counter


def preferred_crn(Schedule):
    weight=0.
    for CRN in Schedule:
        if CRN ==  UserPrefs.preferredCRNs:
            CRN.weight=1000.0







