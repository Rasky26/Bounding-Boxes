

#Imports this dictionary, not sure what it does, check later.
from collections import defaultdict
import sys

#--------------
#Simply used for an easy stopping mechanism for bug and error checking.
def yes_no():

    continue_check = input("Continue? y/n ")
    
    if continue_check == 'n':
        raise ValueError("""

User stopped script.

""")

    return()

#--------------
#Defines my function for seeing if duplicates are listed.
def list_duplicates(seq):
    
    #Seems to generate a running list of all inputs to see if a duplicate
    #is raised.
    tally = defaultdict(list)

    #Checks what the incoming item is and its location in the list of items.
    #If it is new, it starts a new tally list, if one exists, it appends
    #the location of the duplicate.
    for i,item in enumerate(seq):
        tally[item].append(i)

    #Returns the findings. len(locs)>0 returns all, >1 returns duplicates.
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)


#--------------
#Defines my function to list the locations of duplicate items in various lists.
#This list only returns the location within the array of the evaluated list.
#Additionally, it calls the 'list_duplicates' array to initially search for the
#potential duplicates and return the results.
def duplicate_locations(source):

    #Sets a blank array.
    skip_list = []

    #Calls the 'list_duplicates' function to see if duplicates are listed.
    for duplicate in sorted(list_duplicates(source)):

        #For any duplicates found, it calls the second array (the enumerated
        #portion of the return) and finds how many locations were found.
        #It will cycle through the length of that list minus one.
        for n in range(len(duplicate[1])-1):

            #We use +1 to make sure the inital time the value is seen is still
            #utilized during this function. All other instances can be skipped,
            #and therefore added to the skip_list.
            skip_list.append(duplicate[1][n+1])

    #Finally, it sorts the list based on value.
    skip_list.sort()

    #Returns the findings.
    return(skip_list)

#--------------
#Takes two points being evaluated and finds the line formed by them.
#This is important for seeing where it crossing the bounding box and aiding
#in reducing that box to its core area.
def optimal_box(point_1, point_2, bound_1, bound_2):

    #Find the point halfway between the two points being evaluated.
    ###--print("OB aa: Incoming points, main & check:", point_1, point_2, bound_1, bound_2)
    #!midpoint_line = (((point_1[0] + point_2[0]) / 2), ((point_1[1] + point_2[1]) / 2))

    #!print("ab: New midpoint:", midpoint_line)
    #Checks if the points are along a vertical line with each other. If they
    #are, the line has no slope.
    if round(point_2[0], z) == round(point_1[0], z):
        ###--print("ac: The points are vertical")
        p_slope_line = None
        p_y_intersection_line = None
    else:
        p_slope_line = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
        p_y_intersection_line = point_1[1] - (p_slope_line * point_1[0])
        ###--print("ad: point slope & int", p_slope_line, p_y_intersection_line)

    #Checks if the boundaries are along a vertical line with each other. If they
    #are, the line has no slope.
    if round(bound_2[0], z) == round(bound_1[0], z):
        ###--print("ae: The line are vertical")
        b_slope_line = None
        b_y_intersection_line = None
    else:
        b_slope_line = (bound_2[1] - bound_1[1]) / (bound_2[0] - bound_1[0])
        b_y_intersection_line = bound_1[1] - (b_slope_line * bound_1[0])
        ###--print("af: bound slope & y int:", b_slope_line, b_y_intersection_line)


    ########
    #Checks if the bounding slope and the perpendicular slope are parallel.
    #If they are, they never cross and both x and y are set to None.
    #First we check if both slopes are vertical.
    if (b_slope_line == None) and (p_slope_line == None):
        x_intercept_line = None
        y_intercept_line = None


    #If the bounding slope is vertical, but the point slope was NOT
    #parallel to it that means they cross at some point.
    elif b_slope_line == None:
        ###--print("ah: Accessed 1A")
        x_intercept_line = bound_1[0]
        y_intercept_line = (p_slope_line * bound_1[0]) + p_y_intersection_line

    #If the point slope is vertical, but the bounding slope was NOT
    #parallel to it that means they cross at some point.
    elif p_slope_line == None:
        ###--print("ai: Accessed 2B")
        x_intercept_line = point_1[0]
        y_intercept_line = (b_slope_line * point_1[0]) + b_y_intersection_line

    elif round(p_slope_line, z) == round(b_slope_line, z):
        ###--print("ag: Slopes are parallel! (b, p)", b_slope_line, p_slope_line)
        x_intercept_line = None
        y_intercept_line = None
        
    #Otherwise, if neither line is vertical OR parallel then they cross at
    #some point.
    else:
        ###--print("aj: Accessed 3C")
        x_intercept_line = ((b_y_intersection_line - p_y_intersection_line)
                            / (p_slope_line - b_slope_line))
        y_intercept_line = (p_slope_line * x_intercept_line) + p_y_intersection_line

    ###--print("***ak: CHECK HERE: x & y results:", x_intercept_line, y_intercept_line)

    ###--want_to_check = yes_no()

    #---------
    #This one will be flagged if both lines were parallel and therefore never
    #cross. The intersection point does not exist.
    if (x_intercept_line == None) or (y_intercept_line == None):
        ###--print("al: Made Option 1")
        line_result = (None, None)

    #This long check is to see if the midway point between our main point
    #and the check point is inside the bounding box.
    #The purpose is to reduce runtime: if the midway point is inside the
    #bounding box, then continue with the main loop below;
    #otherwise, there is no need for further calculations for that check point.
    #
    #If the intersection point lies on both the half-line segment (main to
    #midpoint, AND lies on the boundary segment, then it 
    elif   ((min(round(point_1[0], z), round(point_2[0], z)) <= round(x_intercept_line, z) <= max(round(point_1[0], z), round(point_2[0], z)))
        and (min(round(point_1[1], z), round(point_2[1], z)) <= round(y_intercept_line, z) <= max(round(point_1[1], z), round(point_2[1], z)))
        and (min(round(bound_1[0], z), round(bound_2[0], z)) <= round(x_intercept_line, z) <= max(round(bound_1[0], z), round(bound_2[0], z)))
        and (min(round(bound_1[1], z), round(bound_2[1], z)) <= round(y_intercept_line, z) <= max(round(bound_1[1], z), round(bound_2[1], z)))):

        ###--print("am: &&&&&&&&Lots of stuff here!!!!!&")
        line_result = (x_intercept_line, y_intercept_line)

    else:
        line_result = (None, None)

    if line_result == (None, None):
        boundary_flag = None
        bounds_found = None
##    elif (((line_result == bound_1) or (line_result == bound_2))
##          and ((line_result == point_1) or (line_result == point_2))):

    elif ((((round(line_result[0], z), round(line_result[1], z)) == (round(bound_1[0], z), round(bound_1[1], z)))
        or ((round(line_result[0], z), round(line_result[1], z)) == (round(bound_2[0], z), round(bound_2[1], z))))
      and (((round(line_result[0], z), round(line_result[1], z)) == (round(point_1[0], z), round(point_1[1], z)))
        or ((round(line_result[0], z), round(line_result[1], z)) == (round(point_2[0], z), round(point_2[1], z))))):

        ###--print("Hit a corner intersection")
        boundary_flag = True
        bounds_found = (bound_1, bound_2)
    else:
        ###--print("Boundary Flag Raised:!", line_result)
        boundary_flag = False
        bounds_found = (bound_1, bound_2)

    ###--want_to_check = yes_no()

    return(line_result, boundary_flag, bounds_found)




#--------------
def point_intersection(point1, point2, bound1, bound2):

    #--print("Check here, (x-coords):", b_1, b_2, b_1[0], b_2[0])
    #If the x-coordinates of the two bounding points are the same, the line
    #is vertical, and therefore set to None. Additionally, there is no
    #y-intercept, so that is set to None too.

    if round(point1[0], z) == round(point2[0], z):
        point_slope = None
        point_intercept = None
    else:
        point_slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
        point_intercept = point1[1] - (point_slope * point1[0])

    if round(bound1[0], z) == round(bound2[0], z):
        ###--print("Boundary lines are vertical")
        bound_slope = None
        bount_intercept = None
    #Otherwise, calculate the bounding points' slope and y-intercept.
    else:
        bound_slope = (bound1[1] - bound2[1]) / (bound1[0] - bound2[0])
        bound_intercept = bound1[1] - (bound_slope * bound1[0])

        
    #--print("Boundary lines slope, int:", b_slope, b_int)

    ###--want_to_check = yes_no()

    #Checks if the bounding slope and the perpendicular slope are parallel.
    #If they are, they never cross and both x and y are set to None.
    #
    #First we check if both slopes are vertical.
    if (point_slope == None) and (bound_slope == None):
        xt_intercept = None
        yt_intercept = None

    #If the bounding slope is vertical, but the perpendicular slope was NOT
    #parallel to it that means they cross at some point.
    elif bound_slope == None:
        #--print("Accessed 1A")
        xt_intercept = bound1[0]
        yt_intercept = (point_slope * bound1[0]) + point_intercept

    #If the perpendicular slope is vertical, but the bounding slope was NOT
    #parallel to it that means they cross at some point.
    elif point_slope == None:
        #--print("Accessed 2B")
        xt_intercept = point1[0]
        yt_intercept = (bound_slope * point1[0]) + bound_intercept

    #If both slopes are not vertical, they need to be checked whether they
    #are parallel. Because of rounding errors, we have to limit the number
    #of decimal places we use.
    elif round(point_slope, z) == round(bound_slope, z):
        #--print("Slopes are parallel! (b, p)", b_slope, p_slope)
        xt_intercept = None
        yt_intercept = None

    #Otherwise, if neither line is vertical OR parallel then they cross at
    #some point.
    else:
        #--print("Accessed 3C")
        xt_intercept = (bound_intercept - point_intercept) / (point_slope - bound_slope)
        yt_intercept = (point_slope * xt_intercept) + point_intercept

    ###--print("xt, yt", xt_intercept, yt_intercept)

    ###--want_to_check = yes_no()

    #--print("***CHECK HERE: x & y results:", x_intercept, y_intercept)

    #---------
    #Many of these are redundant and probably will be deleted later, but are
    #currently listed to maintain clarity and readability.
    #
    #This one will be flagged if both lines were parallel and therefore never
    #cross. The intersection point does not exist.
    if (xt_intercept == None) or (yt_intercept == None):
        ###--print("Made Option 1")
        points_new = (None, None)

    #If the intersection point is the same as one of the two bounding points
    #then that point already exists as a boundary and does not need to be
    #recalculated.
    
    elif (((round(xt_intercept, z), round(yt_intercept, z)) == (round(bound1[0], z), round(bound1[1], z)))
       or ((round(xt_intercept, z), round(yt_intercept, z)) == (round(bound2[0], z), round(bound2[1], z)))):
        ###--print("Made Option 2")
        points_new = (None, None)

    #Finally, if an intersection point exists we need to make sure it falls
    #between the two boundary points. We make sure the intersection's
    #x-coordinate falls between the low and high values for the bounding
    #x-points. We ALSO need the intersection's y-coordinate to fall between
    #the low and high values for the bounding y-points too.
    #
    #If both are True, the new point is created. Otherwise, it is set to None.
    elif ((min(round(bound1[0], z), round(bound2[0], z)) <= round(xt_intercept, z) <= max(round(bound1[0], z), round(bound2[0], z)))
      and (min(round(bound1[1], z), round(bound2[1], z)) <= round(yt_intercept, z) <= max(round(bound1[1], z), round(bound2[1], z)))):
        ###--print("Made Option 3")
        points_new = (xt_intercept, yt_intercept)
    else:
        ###--print("Made Option 4")
        points_new = (None, None)

    if points_new == (None, None):
        distances = None
    else:
        distances = abs(((points_new[0] - point1[0])*(points_new[0] - point1[0])) +
                        ((points_new[1] - point1[1])*(points_new[1] - point1[1])))**(1/2.)

    ###--print("Points New:", points_new, distances)

    ###--want_to_check = yes_no()
    
    return(points_new, distances)


#--------------
#Takes two points being evaluated and finds the perpendicular bisecting line.
#This is important for seeing where it crossing the bounding box and aiding
#in reducing that box to its core area.
def perp_bisector(x_1, y_1, x_2, y_2, midpoint_new = (None, None)):

    #Find the point halfway between the two points being evaluated.
    #--print("Incoming points, main & check:", x_1, y_1, x_2, y_2, midpoint_new)
    midpoint_new = (((x_1 + x_2) / 2), ((y_1 + y_2) / 2))

    #--print("New midpoint:", midpoint_new)
    #Checks if the points are along a horizontal line with each other. If they
    #are, the perpendicular line to that will be vertical and therefore have
    #no slope.
    if round(y_2, z) == round(y_1, z):
        #--print("The perpendicular line is vertical")
        slope_perpendicular = None
        y_intersection_perpendicular = None
    else:
        slope_perpendicular = (x_1 - x_2) / (y_2 - y_1)
        y_intersection_perpendicular = midpoint_new[1] - (slope_perpendicular * midpoint_new[0])
        #--print("perp slope & y int:", slope_perpendicular, y_intersection_perpendicular)

    return(slope_perpendicular, y_intersection_perpendicular, midpoint_new)
    

#--------------
#Needs midpoint(x,y), perpendicular slope, the perpendicular intercept,
#bound points x, and x-1. If p_slope == None, use the mid_p[0] for the x-value.
def line_intersection(mid_p, p_slope, p_y_int, b_1, b_2):

    #--print("Check here, (x-coords):", b_1, b_2, b_1[0], b_2[0])
    #If the x-coordinates of the two bounding points are the same, the line
    #is vertical, and therefore set to None. Additionally, there is no
    #y-intercept, so that is set to None too.
    if round(b_1[0], z) == round(b_2[0], z):
        #--print("Boundary lines are vertical")
        b_slope = None
        b_int = None
    #Otherwise, calculate the bounding points' slope and y-intercept.
    else:
        b_slope = (b_1[1] - b_2[1]) / (b_1[0] - b_2[0])
        b_int = b_1[1] - (b_slope * b_1[0])

        
    #--print("Boundary lines slope, int:", b_slope, b_int)

    #Checks if the bounding slope and the perpendicular slope are parallel.
    #If they are, they never cross and both x and y are set to None.
    #
    #First we check if both slopes are vertical.
    if (p_slope == None) and (b_slope == None):
        x_intercept = None
        y_intercept = None

    #If the bounding slope is vertical, but the perpendicular slope was NOT
    #parallel to it that means they cross at some point.
    elif b_slope == None:
        #--print("Accessed 1A")
        x_intercept = b_1[0]
        y_intercept = (p_slope * b_1[0]) + p_y_int

    #If the perpendicular slope is vertical, but the bounding slope was NOT
    #parallel to it that means they cross at some point.
    elif p_slope == None:
        #--print("Accessed 2B")
        x_intercept = mid_p[0]
        y_intercept = (b_slope * mid_p[0]) + b_int

    #If both slopes are not vertical, they need to be checked whether they
    #are parallel. Because of rounding errors, we have to limit the number
    #of decimal places we use.
    elif round(p_slope, z) == round(b_slope, z):
        #--print("Slopes are parallel! (b, p)", b_slope, p_slope)
        x_intercept = None
        y_intercept = None

    #Otherwise, if neither line is vertical OR parallel then they cross at
    #some point.
    else:
        #--print("Accessed 3C")
        x_intercept = (b_int - p_y_int) / (p_slope - b_slope)
        y_intercept = (p_slope * x_intercept) + p_y_int

    #--print("***CHECK HERE: x & y results:", x_intercept, y_intercept)

    #---------
    #Many of these are redundant and probably will be deleted later, but are
    #currently listed to maintain clarity and readability.
    #
    #This one will be flagged if both lines were parallel and therefore never
    #cross. The intersection point does not exist.
    if (x_intercept == None) or (y_intercept == None):
        #--print("Made Option 1")
        point_new = (None, None)

    #If the intersection point is the same as one of the two bounding points
    #then that point already exists as a boundary and does not need to be
    #recalculated.
    
    elif (((round(x_intercept, z), round(y_intercept, z)) == (round(b_1[0], z), round(b_1[1], z)))
       or ((round(x_intercept, z), round(y_intercept, z)) == (round(b_2[0], z), round(b_2[1], z)))):
        #--print("Made Option 2")
        point_new = (None, None)

    #Finally, if an intersection point exists we need to make sure it falls
    #between the two boundary points. We make sure the intersection's
    #x-coordinate falls between the low and high values for the bounding
    #x-points. We ALSO need the intersection's y-coordinate to fall between
    #the low and high values for the bounding y-points too.
    #
    #If both are True, the new point is created. Otherwise, it is set to None.
    elif ((min(round(b_1[0], z), round(b_2[0], z)) <= round(x_intercept, z) <= max(round(b_1[0], z), round(b_2[0], z)))
      and (min(round(b_1[1], z), round(b_2[1], z)) <= round(y_intercept, z) <= max(round(b_1[1], z), round(b_2[1], z)))):
        #--print("Made Option 3")
        point_new = (x_intercept, y_intercept)
    else:
        #--print("Made Option 4")
        point_new = (None, None)

    return(point_new)

    #Once returned, check if false. If they have actual values, store the new
    #point in an array.


#---------------
def distances(a, b):
    return abs((((a[0] - b[0]) * (a[0] - b[0])) + ((a[1] - b[1]) * (a[1] - b[1])))**(1./2))

def is_between(a, c, b, epsilon = sys.float_info.epsilon):
    return ((epsilon * -1) < (round(distances(a, c), z) + round(distances(c, b), z) - round(distances(a, b), z)) < epsilon)

#---------------
#---------------
#
#   *********
# THIS IS THE STARTING POINT OF THE PROGRAM
#   *********
#
#---------------
#---------------
#This section will be for importing the bounding box and each individual
#location.
#
#The bounding box will need to be listed sequentially from one point immediately
#followed by its linked point and continuing on until a closed polygon is formed.

bounds = [
    (1, 0),
    (1, 1),
    (0, 1),
    (0, 2),
    (3, 2),
    (3, 1),
    (2, 1),
    (2, 0),
    (1.5, -1)]

#Points can be listed in any order
points = [
    (1.5, -0.5),
    (0.1, 1.5),
    (2.9, 1.5)]

#This is dealing with rounding errors. 'z' is set to how many decimals you want.
z = 12

#--------------
#This section will make a pass through the bounding box list and then the
#points list to identify any duplicates. This will ensure the program doesn't
#recalculate the same point again or potentially raise errors.
#It references the above listed 'list_duplicates' definition.
#
#Finally, it will remove any duplicates it finds from the main lists.

#Calls above function to find duplicates and generate a list of their positions.
###***bounds_duplicates = duplicate_locations(bounds) #list of duplicate bounds
points_duplicates = duplicate_locations(points) #list of duplicate points

#Removes duplicates from main list, reversed loop direction is to negate errors.
###***This needs to be removed or re-thought through, because some shapes have
###***the same bounds in order to maintain a valid shape.
###***i.e. the shape of a capital I crossing itselt perpendicularily.
###***for n in reversed(bounds_duplicates):
###***    del(bounds[n])

for n in reversed(points_duplicates):
    del(points[n])

###***del(bounds_duplicates, points_duplicates)
del(points_duplicates)

#-------------
#Time to get the core of this script where we generate our best-fit polygons.
#
#First, we set the array for our final polygons so we can populate it
#once we start finding results.
all_polygons = []


#-------------
#THIS IS THE MAIN LOOP!
#-------------
#
#This loop iterates through all the points that are listed.
#
#The variable 'main' will be the main point that we are creating the polygon
#around each cycle.
#
#Each 'main' point will be compared against all other listed points to find
#the optimal polygon for enclosure. 'main_count' is used as a counting
#integer to compare against the counting integer 'check_count' (listed
#lower) to make sure the point doesn't iterate against itself.
for main_count, main in enumerate(points):
    
    #Each time the main loop is cycled, the bounding box around the point
    #is reset to the outermost bounding box.
    #
    #Shrinking_box will be updated at the end of the next loop below. When the
    #next loop is completed, shrinking_box should (hypothetically) be the
    #best fit polygon around the main point being iterated over.
    #
    #That point and shrinking_box will then be added to the 'all_polygons'
    #list so that all variables can be reset.
    shrinking_box = bounds

    #--print("0, points:", points)
    #--print("1, temp_box:", shrinking_box)




    t_array = []

    for point_count, pointers in enumerate(shrinking_box):

        count = 0

        print("""

Currently in POINTS loop:

""")
        bound_flag = None
        corner_bounds_array = []
        crossing_bounds_array = []

        
        for b_num, bound_p in enumerate(shrinking_box):

            count += 1
            ###--print("Count =", count)

            ###--want_to_check = yes_no()

            new_point, bound_flag, found_bounds = optimal_box(main, pointers,
                                                  shrinking_box[b_num - 1],
                                                  bound_p)

            ###--print("New Stuff:", new_point, bound_flag, found_bounds)

            #--want_to_check = yes_no()

            if bound_flag == True:
                corner_bounds_array.append(found_bounds)
            elif bound_flag == False:
                crossing_bounds_array.append(found_bounds)

            if bound_flag == False:
                seeker_line = True
                last_good_point = (None, None)
                ###--print("*****************BREAKING******************")
                break
            elif bound_flag == True:
                last_good_point = new_point

            ###--print("Corner Bounds Array:", corner_bounds_array)
            ###--print("Crossing Bounds Array:", crossing_bounds_array)
            ###--print("Last good point check:", last_good_point)

            #--want_to_check = yes_no()

        ###--print("Corner Bounds Array:", corner_bounds_array)
        ###--print("Crossing Bounds Array:", crossing_bounds_array)

        
        if (last_good_point != (None, None)) and (last_good_point not in t_array):
            t_array.append(last_good_point)
        ###--print("This is a NEW POINT:", t_array)

        #--want_to_check = yes_no()

        if (last_good_point != (None, None)) and (len(corner_bounds_array) == 2):
            compare_point_1 = (((corner_bounds_array[0][0][0] + corner_bounds_array[0][1][0]) / 2),
                               ((corner_bounds_array[0][0][1] + corner_bounds_array[0][1][1]) / 2))
            compare_point_2 = (((corner_bounds_array[1][0][0] + corner_bounds_array[1][1][0]) / 2),
                               ((corner_bounds_array[1][0][1] + corner_bounds_array[1][1][1]) / 2))


            compare_1 = (((compare_point_1[0] - main[0]) * (pointers[1] - main[1])) -
                         ((compare_point_1[1] - main[1]) * (pointers[0] - main[0])))
            compare_2 = (((compare_point_2[0] - main[0]) * (pointers[1] - main[1])) -
                         ((compare_point_2[1] - main[1]) * (pointers[0] - main[0])))

            ###--print(compare_point_1, compare_point_2, compare_1, compare_2)

            distance_points = abs(((main[0] - pointers[0]) * (main[0] - pointers[0])) +
                                  ((main[1] - pointers[1]) * (main[1] - pointers[1])))

            #--want_to_check = yes_no()

            if ((compare_1 < 0) and (compare_2 < 0)) or ((compare_1 > 0) and (compare_2 > 0)):

                shortest_distance = [(None, None), 999999999]
                distance_array = []

                for b1_num, bound1 in enumerate(shrinking_box):
                
                    point_found, distance = point_intersection(main, last_good_point,
                                                               shrinking_box[b1_num - 1],
                                                               bound1)
                    ###--print("Distances:", distance_points, shortest_distance[1], distance)

                    if distance != None:
                        distance_array.append((point_found, distance))

                print("Distance Array:", distance_array)
                for test in distance_array:
                    ###
##                    print(test[1] < shortest_distance[1])
##                    print(test[1] > distance_points)
##                    print(abs((pointers[0] - main[0]) + (test[0][0] - main[0])) ==
##                          abs(pointers[0] - main[0]) + abs(test[0][0] - main[0]))
##                    print(abs((pointers[1] - main[1]) + (test[0][1] - main[1])) ==
##                          abs(pointers[1] - main[1]) + abs(test[0][1] - main[1]))
##                    ###
                    if ((test[1] < shortest_distance[1]) and (test[1] > distance_points)
                      and (abs((pointers[0] - main[0]) + (test[0][0] - main[0])) ==
                           abs(pointers[0] - main[0]) + abs(test[0][0] - main[0]))
                      and (abs((pointers[1] - main[1]) + (test[0][1] - main[1])) ==
                           abs(pointers[1] - main[1]) + abs(test[0][1] - main[1]))):
                        
                        shortest_distance = [test[0], test[1]]

                        print("Shortest Distance:", shortest_distance)                
                
                        #--want_to_check = yes_no()

            if ((compare_1 < 0) and (compare_2 < 0)):
                t_array.append(shortest_distance[0])
            elif ((compare_1 > 0) and (compare_2 > 0)):
                t_array.insert(-1, shortest_distance[0])

            print(" ")
            print("T Array:", t_array)
            print(" ")

    shrinking_box = t_array

    print("ShrinkingBox:", shrinking_box)

    want_to_check = yes_no()

    #Each 'check' point is the comparitive point to the 'main' point.
    #
    #This loop goes through all points listed to ensure an optimally
    #compact polygon is achieved.
    for check_count, check in enumerate(points):

        #This is a simple check to make sure we aren't comparing the same points
        #against each other.
        if check_count != main_count:

            #BUILD Inside / Outside Check Here:
            #Can probably be deleted...

##            proxy_check_result = []
##            
##            for n_boundary_count, n_boundary in enumerate(shrinking_box):
##                proximity_check = in_or_out(main, check, n_boundary, shrinking_box[n_boundary_count-1])
##
##                proxy_check_result.append(proximity_check)
##
##            print("Proximity Check:", proxy_check_result)


            #--print("""

#--*************RESTARTING 2nd POINT LOOP**********

#--***Calling 'perp_bisector' function***

#--""")
            #This calls the above function 'perp_bisector' passing the
            #x & y-coordinates from the two evalatued points to it.
            #In that function, the midpoint is found and the perpendicular
            #bisector is calculated. We are returned with its slope, y-intercept,
            #and the midpoint values.
            print("Lookie here:", check, main)
            slope_p, y_int_p, midpoint = perp_bisector(main[0], main[1],
                                                       check[0], check[1])
            #--print("--11--:, slope, y_int, midp:", slope_p, y_int_p, midpoint)

            #Since we don't want to iterate over our shrinking box, we need
            #a temporary box to store our findings for where new intersections
            #are found.
            temporary_shrinking_box = []

            #The purpose of this loop is to iterate through our primary point
            #and another random point. Those points will create a midpoint and
            #therefore a perpendicular line. Then, that line will be compared
            #against a line formed by the two boundary points from the loop
            #below.
            #
            #If the result comes back as None, continue with the loop. See
            #reasons for them being false in the above function.
            #
            #If the result returns a value, add that value and the coorelated
            #boundary points into the temporary list using the boundary_count
            #to properly position it.
            for boundary_count, boundary in enumerate(shrinking_box):
                #--print("""

#--***********RESTART BOUNDARY LOOP***************

#--***Calling 'line_intersection' function***

#--""")
                #--print("Passing midp, slope_p, p_int, b, b-1:", midpoint,
                #--      slope_p, y_int_p, boundary, shrinking_box[boundary_count-1])
                new_point = line_intersection(midpoint, slope_p, y_int_p,
                                              boundary,
                                              shrinking_box[boundary_count-1])

                #Check if the point discovered has a value, or 'None.'
                #If new_point is 'None' for either value, no new point
                #was found. Simply add the old boundary point and continue.
                if (new_point[0] == None) or (new_point[1] == None):
                    #--print("Value Check:", new_point)
                    temporary_shrinking_box.append(boundary)
                    #--print("1: Adding to shrinking box:", temporary_shrinking_box)

                #If a new point has been calculated, add it to the
                #temporary_shrinking_box at the correct location.
                #Then add the following boundary point.
                else:
                    temporary_shrinking_box.append(new_point)
                    temporary_shrinking_box.append(boundary)
                    #--print("2: Adding to shrinking box:", temporary_shrinking_box)
                    
            
            #This is the clean-up section for our new boundaries around
            #the evaluated point. While our temporary array is now overly
            #full, our array 'shrinking_box' that we iterated over now
            #needs to be set to zero so we can evaluate and correctly
            #input the coordinates for our new polygon formed about the point.
            shrinking_box = []
            #--print("total temp:", temporary_shrinking_box, shrinking_box)

            #Now we test each boundary point we calculated to make our
            #new polygon optimally small.
            #
            #The idea here is to draw a line from our point to a boundary
            #point and see if crosses our perpendicular line.
            #If it crosses, it will raise a new coordinate where that
            #intersection which means that boundary point is not
            #optimally close. That point will then be removed from
            #the 'shrinking_box' array.
            #
            #Finally, remember that the 'shrinking_array' will exist for
            #the entirety of the loop for the 'check' points. This mean
            #each sequential pass of that loop may potentially shrink
            #the polygon size. See below for when the 'check' loop ends.
            for test_boundary in temporary_shrinking_box:

                #Looks if that line (reference just above) returns with
                #an actual value.
                check_point = line_intersection(midpoint, slope_p, y_int_p,
                                                test_boundary, main)

                #If the function referenced returns with 'None,' then
                #an optimally close boundary point has been found.
                if check_point == (None, None):
                    #Simply included to make sure duplicates are not listed
                    if test_boundary not in shrinking_box:
                        #If no duplicates are found, add the boundary
                        #to the iterable array.
                        shrinking_box.append(test_boundary)



            #--print("""
#--********************
#--After all this work,
#--Here are the results
#--********************
#--""")
            #--print(shrinking_box)



                

    print("Adds new point and its bounding box to the total list")
    all_polygons.append((main, (shrinking_box)))


#uncovered = []


#This section is for verifying whether a point lies on a line between two
#other points. If a point does fall on that line, it can be removed from
#that point's boundary array as it is redundant.
for b_num, b_check in enumerate(bounds):
    for point_n_box in all_polygons:
        for seg_num, line_seg in enumerate(point_n_box[1]):
##            print("")
##            print(bounds[b_num - 1], b_check, line_seg, point_n_box[1][seg_num - 1])
##            print("")
##            print(is_between(bounds[b_num - 1], point_n_box[1][seg_num - 1], b_check))
##            print(is_between(bounds[b_num - 1], line_seg, b_check))

            if ((is_between(bounds[b_num - 1], point_n_box[1][seg_num - 1], b_check))
                and (is_between(bounds[b_num - 1], line_seg, b_check))):
                print("This worked")
                print(bounds[b_num - 1], b_check)
                print(bounds[b_num - 1], b_check, line_seg, point_n_box[1][seg_num - 1])


### PICK UP HERE ###

### Draw out the boundary and the grids to remember what you were trying to do.




print("""

""")
print("Results")
print("""

""")
for Wowwie in all_polygons:
    print(Wowwie)
    print("----------")

print("""

""")
