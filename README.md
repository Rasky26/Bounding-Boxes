# Bounding-Boxes
Python Script to Making Best-Fit Boundaries About Points

I am seeking assistance with handling a seemingly logical problem (on paper at least),
and creating the code/script necessary to fix it.

The script runs fine (but there are a few points you will need to type 'y' or hit -enter- to continue),
but I need to identify unassigned areas and associating them with the logical closest point.

Once the script is done, you'll see the word 'Results' followed by numbers. The first number
pairing is the point which the polygon was built around, and the array with the number
pairings are the boundary points listed in order (play connect-the-dots with the array points).
If you physcially draw the points and then the boundaries with connecting lines on a grid and compare
it to the boundaries listed starting at line 462 of my script, you will notice there are two
pockets along the lower vertical lines that are unassigned.

I am seeking help finding an effecient way to incorporate those blank polygons into the
logically closest point where none of the interior points of that blank polygon cross
the boundary lines listed at line 462 in the script. The idea is that you can simply check
from any location within that unassigned polygon and find the closest point where a line
drawn between the two does not cross any of the boundaries listed in line 462.

Once the proper point is identified, I thenwant to update that closest point's
boundaries with those of the unassigned area.

In this specific Python exammple, those blank polygons should be incorporated with the point
(1.5, -0.5) initialized in line 475. (Sorry for all the decimals).

Current:

((1.5, -0.5), [(1, 0.0), (1.0, 0.64), (1.5000000000000002, 0.99), (2.0, 0.6400000000000001), (2.0, 0.0), (1.5, -1.0)])
----------
((0.1, 1.5), [(1.5, 0.9900000000000001), (1.286725663716814, 0.8407079646017699), (1.0, 1.0), (0, 1.0), (-0.0, 2.0), (1.5, 2.0)])
----------
((2.9, 1.5), [(1.5, 0.9900000000000002), (1.5, 1.9999999999999991), (3, 1.9999999999999982), (3.0, 1.0000000000000018), (2, 1.0), (1.713274336283186, 0.8407079646017699)])
----------

Wanted:

((1.5, -0.5), [(1, 0.0), (1.0, 1.0), (1.286725663716814, 0.8407079646017699), (1.5000000000000002, 0.99), (1.713274336283186, 0.8407079646017699), (2.0, 1.0), (2.0, 0.0), (1.5, -1.0)])
----------
((0.1, 1.5), [(1.5, 0.9900000000000001), (1.286725663716814, 0.8407079646017699), (1.0, 1.0), (0, 1.0), (-0.0, 2.0), (1.5, 2.0)])
----------
((2.9, 1.5), [(1.5, 0.9900000000000002), (1.5, 1.9999999999999991), (3, 1.9999999999999982), (3.0, 1.0000000000000018), (2, 1.0), (1.713274336283186, 0.8407079646017699)])
----------

I've been working to make a Python script that will calculate the optimal boundaries about
about points listed. I did my best to comment out the code (mostly for my own sake), but
feel free to ask questions. I'm self-taught and not great at programming so I'm sorry
for all the commented sections where I was testing or error-checking.

Thanks.
