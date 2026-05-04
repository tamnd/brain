---
title: "Algorithm Cookbook"
tags: ["algorithms", "computer-science"]
---

## Chapter 1. Foundations

1. Problem statements
2. Input and output models
3. Correctness arguments
4. Loop invariants
5. Recursion invariants
6. Time complexity
7. Space complexity
8. Big O notation
9. Lower bounds
10. Edge cases
11. Testing algorithms
12. Brute force baselines
13. Greedy choices
14. Divide and conquer
15. Dynamic programming
16. Randomization
17. Amortized analysis
18. Reductions
19. Pseudocode style
20. Implementation discipline
21. Data representation
22. Numerical limits
23. Stability and determinism
24. Benchmarking
25. Common failure modes

## Chapter 2. Arrays and Strings

1. Array traversal
2. Prefix sums
3. Difference arrays
4. Two pointers
5. Sliding windows
6. Partitioning
7. Rotation
8. In-place modification
9. Deduplication
10. String scanning
11. Tokenization
12. Substring search
13. Palindromes
14. Anagrams
15. Frequency tables
16. Run-length encoding
17. Rolling hashes
18. String comparison
19. Unicode concerns
20. Sparse arrays
21. Matrix traversal
22. Spiral order
23. Interval arrays
24. Common patterns
25. Case studies

## Chapter 3. Linked Lists and Pointers

1. Singly linked lists
2. Doubly linked lists
3. Sentinel nodes
4. Reversal
5. Cycle detection
6. Fast and slow pointers
7. Merge patterns
8. Split patterns
9. Deletion patterns
10. Insertion patterns
11. Dummy heads
12. Pointer aliasing
13. Persistent lists
14. Skip lists
15. Intrusive lists
16. Memory ownership
17. Iterators
18. Stack via list
19. Queue via list
20. LRU cache structure
21. Edge cases
22. Testing pointer code
23. Complexity analysis
24. Common bugs
25. Case studies

## Chapter 4. Stacks, Queues, and Deques

1. Stack interface
2. Queue interface
3. Deque interface
4. Monotonic stacks
5. Monotonic queues
6. Parentheses matching
7. Expression parsing
8. Undo stacks
9. Next greater element
10. Histogram rectangles
11. Sliding window maximum
12. BFS queues
13. Circular buffers
14. Priority queues overview
15. Double-ended BFS
16. Work queues
17. Rate-limited queues
18. Buffer management
19. Lock-free concepts
20. Memory layout
21. Amortized bounds
22. Invariant checks
23. Testing
24. Common bugs
25. Case studies

## Chapter 5. Hashing and Maps

1. Hash tables
2. Hash functions
3. Collision handling
4. Chaining
5. Open addressing
6. Load factor
7. Rehashing
8. Sets
9. Maps
10. Counting maps
11. Grouping keys
12. Composite keys
13. Rolling hashes
14. Bloom filters
15. Count-min sketch
16. Consistent hashing
17. Hash joins
18. Hash-based deduplication
19. Cache behavior
20. Attack resistance
21. Deterministic hashing
22. Testing hash logic
23. Complexity guarantees
24. Common bugs
25. Case studies

## Chapter 6. Sorting

1. Sorting contracts
2. Selection sort
3. Insertion sort
4. Merge sort
5. Quick sort
6. Heap sort
7. Counting sort
8. Radix sort
9. Bucket sort
10. Stable sorting
11. Partial sorting
12. Top k selection
13. Quickselect
14. Median selection
15. External sorting
16. Nearly sorted data
17. Custom comparators
18. Sorting records
19. Coordinate compression
20. Inversion counting
21. Lower bounds
22. Parallel sorting
23. Testing sort correctness
24. Common bugs
25. Case studies

## Chapter 7. Binary Search and Ordered Data

1. Binary search template
2. Lower bound
3. Upper bound
4. Search on answer
5. Monotone predicates
6. Floating-point binary search
7. Rotated arrays
8. Peak finding
9. Interval search
10. Ordered maps
11. Balanced trees
12. Binary search trees
13. Tree rotations
14. Treaps
15. Red-black trees
16. AVL trees
17. B-trees
18. Range queries
19. Order statistics
20. Coordinate search
21. Parametric search
22. Boundary bugs
23. Testing
24. Complexity analysis
25. Case studies

## Chapter 8. Trees

1. Tree representation
2. DFS traversal
3. BFS traversal
4. Recursion on trees
5. Tree height
6. Tree diameter
7. Lowest common ancestor
8. Binary lifting
9. Euler tour
10. Subtree queries
11. Rerooting
12. Tries
13. Segment trees
14. Fenwick trees
15. Lazy propagation
16. Persistent trees
17. Heavy-light decomposition
18. Centroid decomposition
19. Suffix trees overview
20. Expression trees
21. Serialization
22. Testing tree algorithms
23. Complexity analysis
24. Common bugs
25. Case studies

## Chapter 9. Graph Fundamentals

1. Graph models
2. Adjacency lists
3. Adjacency matrices
4. Edge lists
5. Directed graphs
6. Undirected graphs
7. Weighted graphs
8. Degree and connectivity
9. DFS
10. BFS
11. Connected components
12. Topological sort
13. Cycle detection
14. Bipartite graphs
15. Strongly connected components
16. Articulation points
17. Bridges
18. Euler paths
19. Hamiltonian paths overview
20. Graph coloring basics
21. Graph representation tradeoffs
22. Testing graph code
23. Complexity analysis
24. Common bugs
25. Case studies

## Chapter 10. Shortest Paths

1. Unweighted shortest paths
2. BFS shortest paths
3. Dijkstra algorithm
4. Priority queue variants
5. Bellman-Ford
6. Negative cycles
7. Floyd-Warshall
8. Johnson algorithm
9. DAG shortest paths
10. Multi-source shortest paths
11. 0-1 BFS
12. A* search
13. Bidirectional search
14. Path reconstruction
15. Distance labels
16. Potentials
17. Sparse vs dense graphs
18. Road networks
19. Grid shortest paths
20. Dynamic shortest paths
21. Correctness proofs
22. Complexity analysis
23. Testing
24. Common bugs
25. Case studies

## Chapter 11. Minimum Spanning Trees and Connectivity

1. Spanning trees
2. Cut property
3. Cycle property
4. Kruskal algorithm
5. Prim algorithm
6. Boruvka algorithm
7. Union-find
8. Path compression
9. Union by rank
10. Offline connectivity
11. Dynamic connectivity overview
12. Minimum bottleneck spanning tree
13. Second-best spanning tree
14. Clustering
15. Network design
16. Sparse graph handling
17. Dense graph handling
18. Correctness proofs
19. Complexity analysis
20. Implementation patterns
21. Testing
22. Common bugs
23. Case studies
24. Variants
25. Exercises

## Chapter 12. Network Flow and Matching

1. Flow networks
2. Residual graphs
3. Ford-Fulkerson
4. Edmonds-Karp
5. Dinic algorithm
6. Push-relabel
7. Min cut
8. Max-flow min-cut theorem
9. Bipartite matching
10. Hopcroft-Karp
11. Assignment problem
12. Hungarian algorithm
13. Min-cost max-flow
14. Circulation with demands
15. Lower bounds on edges
16. Vertex capacities
17. Edge-disjoint paths
18. Project selection
19. Scheduling applications
20. Correctness proofs
21. Complexity analysis
22. Testing flow code
23. Common bugs
24. Modeling patterns
25. Case studies

## Chapter 13. Dynamic Programming

1. DP state design
2. Recurrence relations
3. Memoization
4. Tabulation
5. One-dimensional DP
6. Two-dimensional DP
7. Knapsack
8. Longest common subsequence
9. Longest increasing subsequence
10. Edit distance
11. Interval DP
12. Tree DP
13. Digit DP
14. Bitmask DP
15. Probability DP
16. Counting DP
17. Optimization DP
18. Convex hull trick
19. Divide-and-conquer optimization
20. Knuth optimization
21. DP on graphs
22. Space optimization
23. Correctness proofs
24. Testing
25. Case studies

## Chapter 14. Greedy Algorithms

1. Greedy choice property
2. Exchange arguments
3. Matroids overview
4. Interval scheduling
5. Activity selection
6. Huffman coding
7. Fractional knapsack
8. Job sequencing
9. Minimum refueling stops
10. Prefix constraints
11. Sorting plus greedy
12. Priority queue greedy
13. Two-pointer greedy
14. Graph greedy
15. String greedy
16. Local vs global optimum
17. Counterexamples
18. Correctness proofs
19. Complexity analysis
20. Testing
21. Common bugs
22. Design patterns
23. Case studies
24. Variants
25. Exercises

## Chapter 15. Divide and Conquer

1. Recursion trees
2. Master theorem
3. Merge sort revisited
4. Quick sort revisited
5. Closest pair of points
6. Karatsuba multiplication
7. Strassen multiplication
8. Fast exponentiation
9. Binary splitting
10. Divide-and-conquer DP
11. Parallel divide and conquer
12. Cache-oblivious algorithms
13. Selection algorithms
14. Median of medians
15. Counting inversions
16. Range decomposition
17. Offline queries
18. Recurrence solving
19. Correctness proofs
20. Complexity analysis
21. Testing
22. Common bugs
23. Implementation patterns
24. Case studies
25. Exercises

## Chapter 16. String Algorithms

1. Exact matching
2. Knuth-Morris-Pratt
3. Z algorithm
4. Rabin-Karp
5. Boyer-Moore overview
6. Trie matching
7. Aho-Corasick
8. Suffix arrays
9. LCP arrays
10. Suffix automata
11. Palindromic trees
12. Manacher algorithm
13. Edit distance
14. Longest repeated substring
15. Longest common substring
16. Lexicographic order
17. String hashing
18. Compressed strings
19. Unicode and normalization
20. Token streams
21. Text indexing
22. Complexity analysis
23. Testing
24. Common bugs
25. Case studies

## Chapter 17. Computational Geometry

1. Points and vectors
2. Orientation tests
3. Line intersection
4. Segment intersection
5. Polygon area
6. Point in polygon
7. Convex hull
8. Rotating calipers
9. Closest pair
10. Sweep line
11. Interval geometry
12. Rectangle union area
13. Half-plane intersection
14. Voronoi diagrams overview
15. Delaunay triangulation overview
16. Precision errors
17. Integer geometry
18. Floating-point robustness
19. Geometric hashing
20. Spatial indexes
21. R-trees overview
22. Correctness proofs
23. Testing
24. Common bugs
25. Case studies

## Chapter 18. Number Theory

1. Divisibility
2. Euclidean algorithm
3. Extended gcd
4. Modular arithmetic
5. Modular inverse
6. Fast exponentiation
7. Primality testing
8. Sieve of Eratosthenes
9. Factorization
10. Chinese remainder theorem
11. Euler phi function
12. Mobius function
13. Modular combinatorics
14. Linear congruences
15. Diophantine equations
16. Primitive roots
17. Discrete logarithms overview
18. Miller-Rabin
19. Pollard rho
20. Big integer concerns
21. Cryptographic caveats
22. Correctness proofs
23. Complexity analysis
24. Testing
25. Case studies

## Chapter 19. Randomized and Approximate Algorithms

1. Random variables in algorithms
2. Las Vegas algorithms
3. Monte Carlo algorithms
4. Randomized quicksort
5. Random sampling
6. Reservoir sampling
7. Shuffling
8. Skip lists revisited
9. Hashing with randomness
10. MinHash
11. HyperLogLog
12. Bloom filters revisited
13. Count-min sketch revisited
14. Locality-sensitive hashing
15. Approximation ratios
16. Greedy approximation
17. Set cover approximation
18. Vertex cover approximation
19. Streaming algorithms
20. Online algorithms
21. Competitive analysis
22. Probability bounds
23. Testing randomized code
24. Common bugs
25. Case studies

## Chapter 20. End-to-End Case Studies

1. Autocomplete engine
2. Search ranking pipeline
3. Shortest path service
4. Event scheduler
5. Text diff tool
6. Compression tool
7. Log deduplication
8. Graph analytics job
9. Recommendation prototype
10. Spell checker
11. Rate limiter
12. Cache eviction policy
13. Web crawler frontier
14. Static analyzer
15. Mini database index
16. Packet routing simulation
17. Task dependency planner
18. Plagiarism detector
19. Geometry query engine
20. Constraint solver
21. Streaming analytics
22. External merge sort
23. Matchmaking system
24. Verified algorithm sketch
25. Performance tuning report
