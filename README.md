# PurePursuit
This is a visual demonstration of the how the Pure Pursuit algorithm smooths out and optimizes a path. 

Made with python and Pygame library.

### How Pure Pursuit Works
Suppose we are given a point object that we want to follow a curvy path on a 2D plane.
1) We create a circle with some radius around the object.
2) We look at the path that the object is meant to follow. If our circle intersects that path, we find the intersection point. If there are multiple intersection points, we take the point furthest along the path. This gives the object a way of "looking ahead" at what comes next on the path.
3) We tell the object to travel towards the intersection point. By doing this, the object will proactively cut corners while never actually losing the path. This makes it far more efficient than moving directly on the given path.

This program randomly generates a path and then implements Pure Pursuit to follow it. The geometry is drawn in real time as the object moves.

![Output sample](https://github.com/Elliott-Song/PurePursuit/blob/master/pursuitdemo.gif)

*As shown above, although the set path is very zig-zaggy, the object's movement is very smooth and efficient*
