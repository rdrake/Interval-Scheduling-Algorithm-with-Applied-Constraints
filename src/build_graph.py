import matplotlib.pyplot as plt
import networkx as nx
from JSON_io import JSON_write
from course import *


##NOTE:  At this point, it is assumed that the variable query_results is 
#        a list of all potential courses (as Section() objects), returned 
#        from some database query or web scraping action.

#  populate this list with Section() objects from the query
query_results = []

#  populate this with the total number of sections that should be on
#  the calendar, assuming there are no scheduling impossibilities 
#  (e.g.  1 tutorial, 1 lab and 1 lecture each for 3 courses would 
#  result in requiredNumberOfSections = 9)
requiredNumberOfSections = 10



##start code



#Construct the graph object
G = nx.Graph()

#add all potential courses as nodes to the graph
for Sec in query_results:
   G.add_node(Sec, label=Sec.course[0:2])


#map the type to a float for coloring the graph output
# {
typemapping = { 'Lec': 1.0, 'Tut':0.75, 'Lab':0.25, 'Oth':0.0 }
colors = [typemapping[node.cType] for node in G.nodes() ]
# }

for i,iSec in enumerate(query_results):
   for j,jSec in enumerate(query_results):
      if i<j:
         have_edge = False
         if ( (iSec.cType == jSec.cType) and (jSec.course==iSec.course)):
            #If the two sections are from the same course and are the same type, then they're incompatible.
            #draw an edge between them
            have_edge = True
         for itimeslot in iSec.timeslots:
            for jtimeslot in jSec.timeslots:
               if ((jtimeslot.sTime <= itimeslot.eTime and jtimeslot.eTime >= itimeslot.eTime and jtimeslot.day==itimeslot.day)):
                  #if they overlap in time, and they're on the same day, then they're incompatible.
                  have_edge = True

         if have_edge:
            #If have_edge is true, then these two nodes are incompatible with each other.
            #Add an edge between them
            G.add_edge(iSec,jSec)





successfully_scheduled_sections = 0
tries = 0


while successfully_scheduled_sections < requiredNumberOfSections:
   #compute the maximal independent set.  This is NOT the MAXIMUM independent set. Thus we must loop a few times
   #to attempt to get the best possible optimization.
   yoursched = nx.maximal_independent_set(G)
   successfully_scheduled_sections =  len(yoursched)
   tries +=1
   print "Attempt ",tries
   if tries > 100:
      print "Unsuccessful at making a schedule which includes all courses.  The best one possible has been created, but please check for missing courses/sections"
      break



nx.draw_networkx(G,with_labels=True,labels=nx.get_node_attributes(G,'unique'), cmap=plt.get_cmap('jet'), node_color=colors,vmin=0, vmax=1.0)
plt.savefig('graph.svg')



JSON_write(yoursched, 'w1.json','w2.json')



