# KD-tree-for-k-nn-queries
Knn query: Given a query point q (x and y coordinate) and a value of k, retrieve the k closest points (from the dataset) for the input query point q.


Some Specifications followed for the KD-tree implementation :
(1) Data structures for root, internal nodes and leaves be clearly defined. Internal nodes stores the
following: (a) line used to split, (b) pointer to a left and right child, (c) if the current node is a left or a right child
of the parent, (d) pointer to the parent.
(2) Points on the line go to the left child. Left child of an internal node is left of the line or below the line.
(3) At root level you can define the “region” as the smallest rectangle enclosing all the points in the dataset. This
means that regions at the internal node level are all subsets of this grand region defined at the root. 
(4) The tree is built using a recursive function which carries the whole set of points and divides them
accordingly. Point by point insertion into KD tree is not allowed.
(5) At every level, you should choose the axis which has the largest spread and find the median data point by ordering
the data on the chosen axis.
(6) Region corresponding to a node should not be stored in the internal node, rather it should be generated on the fly
using the lines stored in the parents. 
(7) At any stage during insertion, splitting should not continue further if the current region has only alpha #data
points (parameter to be set in experiments) or less. In such a case, we create a leaf node. This leaf node
would actually store all the alpha #data points. For each of these data points, store the Point ID, x-coordinate and
y-coordinate. Store each point in a new line.
