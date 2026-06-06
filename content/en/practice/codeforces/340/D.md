---
title: "CF 340D - Bubble Sort Graph"
description: "given a permutation of the Problem Understanding We are given a permutation of numbers from 1 to n. the numbers from 1 to n. ImagineImagine running bubble sort on this permutation running ordinary bubble sort on this."
date: "2026-06-06T17:17:43+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 340
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 198 (Div. 2)"
rating: 1500
weight: 340
solve_time_s: 125
verified: true
draft: false
---

[CF 340D - Bubble Sort Graph](https://codeforces.com/problemset/problem/340/D)

**Rating:** 1500  
**Tags:** binary search, data structures, dp  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
given a permutation of the## Problem Understanding

We are given a permutation of numbers from `1` to `n`.

 the numbers from 1 to n. ImagineImagine running bubble sort on this permutation running ordinary bubble sort on this. Every time bubble sort finds two adjacent elements in the permutation. Every time bubble sort performs a swap between two adjacent wrong order and swaps them, we add an undirected edge between elements, we add an undirected edge between the two the values being swapped. The graph values being swapped.

After bubble sort finishes, we's vertices are the values `1...n`.

After bubble sort obtain a graph whose vertices are the numbers 1 through n. The task is finishes, we obtain a graph whose edges record every not to simulate the graph itself, but to find swap that occurred. The task is to find the size of the largest the size of its maximum independent set, meaning the largest collection independent set in that graph, meaning the largest of vertices with no edge between any pair collection of vertices with no edge of them.

The first challenge between any pair of them.

The first is understanding what graph bubble sort actually creates. A direct challenge is understanding what graph simulation of bubble sort may perform bubble sort actually creates. Directly simulating bubble sort up to O(n²) swaps. With n as can require `O(n² large as 100000, that would be roughly 10¹⁰ operations in)` swaps. With `n` up to ` the worst case, which is completely impossible within a100000`, that would be around one-second time limit.

The constraint that `10^10` operations in the worst case, which the input is a permutation is extremely important. Every is completely impossible within one second.

The constraints strongly value appears exactly once, which creates suggest that the graph has some hidden structure. strong structure in the swaps.

A common We need an algorithm around `O(n log n)`.

A mistake is to think common mistake is that every inversion becomes to think that every inversion becomes an edge. Consider:

```text
3
3 1 2
```

The inversions are (3, an edge. Consider:

```text
3
3 1 2
```

The inversions are `(3,1)` and `(3,1) and (3,2). Bubble sort indeed2)`, and indeed both creates edges (3,1) and (3,2), so become edges. But this is this example does not true because not reveal the difference.

A more revealing example is:

``` of inversions in general,text
4
4 1 3  it is true because bubble sort eventually2
```

The inversion swaps those pairs directly.

Another tempting pair (4,2) exists, but these mistake is to construct the graph explicitly values are never swapped directly. Bubble sort swaps adjacent elements only and then run a maximum independent set algorithm. Maximum independent set. Treating every inversion as an edge is NP-hard on arbitrary graphs, so would build the wrong graph.

Another easy such an approach would immediately look mistake is to explicitly construct the graph and then hopeless. The key observation is that this graph is solve a maximum independent set problem on it. General maximum independent set very special.

Consider:

```text
4
 is NP-hard, so if the graph were arbitrary this4 1 2 3
```

Bubble would be hopeless. The hidden structure of the sort creates edges `(4,1)`, `(4,2)`, `(4,3)`. graph is the entire The maximum independent set has size `3`, namely point of the problem.

A final subtle `{1,2,3}`. A generic graph case is an already sorted permutation:

 algorithm would miss the fact that this graph comes```text
5
1 2 3 4 5
 from a very structured process.

A useful edge case is an```

No swaps occur, so the graph already sorted permutation:

```text
5
1 2 3 4  has no edges. The answer is 55
```

No swaps occur, so the graph has no edges. The maximum independent set contains every vertex, since every vertex can belong to the independent set. Any solution that assumes, and the answer is `5`.

At the opposite extreme:

```text
5
 at least one edge exists will fail here.

## Approaches

5 4 3 2 1
```

Every pairThe most direct idea is to simulate bubble forms an inversion. Bubble sort exactly as described sort eventually swaps every inverted pair exactly. Every time two once, producing a complete graph. The maximum independent set size is `1`.

Understanding adjacent values are swapped, we add an edge between them. After collecting why these two extremes correspond to empty all edges, we could try to compute the and complete graphs leads directly to the main insight.

## Approaches maximum independent set.

The simulation

The brute-force interpretation is straightforward. Simulate bubble sort itself already costs O(n²) in exactly as described, add every edge, the worst case because bubble sort may perform Θ build the resulting graph, and then compute its(n²) swaps. For n = 100000 maximum independent set.

Even constructing the graph this this is far beyond feasible.

Even worse way is too slow. Bubble sort performs, finding a maximum independent set in a general graph is computational `O(n²)` comparisons andly difficult. So brute force fails both because graph swaps. For `n =  construction is too expensive and because the resulting optimization problem appears in100000`, the operation count is fartractable.

The key observation is that the graph produced by bubble beyond practical limits.

The next observation is sort is highly special the crucial one: in.

Consider two values x and y with x > y.

 bubble sort, two values are swappedIf x appears before y in if and only if they form an inversion in the original permutation.

Take the permutation, then they form an inversion. two values `x > y`. If `x` During bubble sort, x must eventually move past y. Since appears before `y`, they form an inversion. Bubble swaps are adjacent, there is exactly one moment when x and y become adjacent and are swapped sort eventually moves `x` right. At that moment an edge (x,y)ward and `y` leftward until they become adjacent, at is added.

If x appears after y initially, they are already which point they are swapped exactly once. If they are in the correct relative order and never swap.

This not an inversion initially, their relative order never changes means:

Two vertices are connected and they are never swapped.

This means the if and only if they form an inversion in the original permutation.

 graph contains exactly one edge for every inversion pair.

Now suppose we selectNow rewrite the inversion condition in terms of vertices that form an independent set. No positions. Let `pos[v]` be the position of value `v` in the permutation.

For values `u < two selected vertices may form an inversion. Thus, among the selected v`, they are adjacent in the graph values, their order in the permutation must already be exactly when

```text
pos[u] > pos[v]
`` increasing.

That is exactly the definition of an`

In other words, the graph is a increasing subsequence.

Conversely, every increasing subsequence contains no permutation graph.

An independent set cannot inversion pair, so its vertices form an independent set.

We have established a bijection:

Maximum independent set contain two vertices connected by an edge. Therefore, if we choose values size = Longest Increasing Subsequence length.

Once

```text
x1 < x2 < ... < x the problem is reduced to LIS, wek
```

inside an independent set, we must have

```text
 can solve it in O(n log n) using the standardpos[x1] < pos[x2] < ... < pos[xk]
```

Otherwise patience-sorting technique with binary search.

| Approach | Time Complexity some pair would form an inversion and create an edge.

So | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force an independent set corresponds exactly to a subsequence of values whose positions are bubble-sort simulation + graph reasoning increasing.

If we list the positions in | O(n²) or worse | O(n² value order:

```text
pos[1], pos[2], ...,) | Too slow |
| LIS reduction pos[n]
```

then the | O(n log n) | O(n) | Accepted |

## Algorithm answer becomes the length of the Longest Increasing Subsequence Walkthrough

1. Read the permutation.

2. Maintain an of this sequence.

Computing LIS in ` array `tails`.

   `tails[i]`O(n log n)` is a standard technique will store the smallest possible ending value of and easily fits the constraints.

| Approach | Time Complexity | an increasing subsequence of length `i + 1`.

3. Process Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | the permutation from left to right.

4. O(n²) or worse | O(n² For the current value `x`,) | Too slow |
| Optimal (LIS) | O(n log n) | find the first position in `tails` whose O(n) | Accepted |

## Algorithm Walkthrough value is greater than or equal to `x`.

   This

1. Read the permutation.

2. Build an array ` position can be found with binary search.

5. If nopos` where `pos[v]` stores the position such position exists, append `x` to `tails`.

   This of value `v` in the permutation.

3. Construct the sequence:

   means we have found a longer increasing subsequence than any ```text
   pos[1], pos[2], seen before.

6. Otherwise, replace that ..., pos[n]
   ```

   This sequence describes position with `x`.

   A smaller ending value is where each value appears.

4. Compute the Long always better because it leaves more room forest Increasing Subsequence of this sequence using the standard patience future elements to extend the subsequence.

7. After-sorting method.

5. Maintain an all values are processed, the array `tails`.

   `tails[len-1]` stores length of `tails` equals the length of the the smallest possible ending value of Longest Increasing Subsequence.

8. Output that length.

### Why it works an increasing subsequence of length `len`.

6. Process the

An edge exists exactly between pairs of position sequence from left to right.

   For each position value ` values that form inversions in the original permutation.

x`, find the first element in `tails` thatAn independent set cannot contain two adjacent vertices of the graph is greater than or equal to `x`.

7. If. Therefore it cannot contain an inversion pair. The no such element exists, append `x` to `tails`.

   This selected values must appear in increasing order within the permutation.

Convers means we found a longer increasing subsequence.

8. Otherwise replace that element with `x`.

ely, every increasing subsequence contains no inversion pair. Since   A smaller tail is always no inversion pair exists, no edge exists between any two preferable because it leaves more room for future extensions.

9. After processing all elements, the chosen vertices, making it an independent set.

Thus independent sets and increasing subsequences length of `tails` is the LIS length.

10. Output are exactly the same objects viewed that length.

### Why it works

Every graph from two different perspectives. Maximizing one is edge corresponds to an inversion pair.

Take any independent set and equivalent to maximizing the other.

The patience-sorting LIS algorithm is sort its vertices by value:

```text
v known to compute the maximum increasing subsequence length because1 < v2 < ... < vk
```

Since no pair `tails[k]` always stores the smallest achievable ending value is connected, none of these pairs forms of a subsequence of length `k + 1`. Binary an inversion. Hence

```text
pos[v1] < pos[v2] < ... < search preserves this invariant after every update.

## Python Solution

``` pos[vk]
```

The positions form an increasing subsequencepython
import sys
from bisect import bisect_left

input =.

Conversely, suppose values

```text
 sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int,v1 < v2 < ... < vk
```

have increasing input().split()))

    tails = []

    for x in a:
        pos = bisect_left positions. Then no pair forms an inversion, so no edge exists between any pair.(tails, x)

        if pos == len(tails):
            tails.append(x)
 They form an independent set.

Thus there is a one        else:
            tails[pos] = x

    print(len(tails))

if __name__ == "__main__":
   -to-one correspondence between independent sets and increasing subsequences of

```text
pos[1], solve()
```

The solution never pos[2], ..., pos[n].
```

The maximum independent set size is constructs the graph.

The crucial observation is the equivalence between exactly the LIS length of that sequence.

## Python Solution

```python
import graph independent sets and increasing subsequences. Once that reduction sys
from bisect import bisect_left

input = is established, the remainder is a standard LIS sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

 computation.

The array `tails` is maintained in sorted order.    pos = [0] * (n + 1)
 Using `bisect_left` finds the    for i, v in enumerate(a):
        pos[v] = i

    tails = []

 first position where the current value can replace an existing tail. Since    for v in range(1, n + 1):
        x = pos[v]
 the input is a permutation, all values are distinct, but        idx = bisect_left(tails, x)

        if idx == len(tails):
            `bisect_left` is still the correct choice for the tails.append(x)
        else:
            tails[idx] = x

    standard strictly-increasing LIS algorithm.

When `pos == print(len(tails))

if __name__ == "__main__":
    solve len(tails)`, the current value extends the longest subsequence found so far()
```

The first part builds the inverse. Otherwise we replace an existing tail. permutation `pos`. Instead of asking which value sits at each position, The replacement does not reduce any achievable subsequence length, it we ask where each value sits.

The sequence `pos[1], pos[ only improves future extension opportunities by making the ending2], ..., pos[n]` is exactly value smaller.

No overflow concerns the object whose LIS we need.

The ` exist because all values are at most 100000.

## Worked Examples

###tails` array implements the standard ` Example 1

Input:

```text
3
3 1 2
O(n log n)` LIS algorithm. Using `bisect_left````

| Current value | is the correct choice because LIS requires strictly increasing values tails before | Position. Replacing the first tail | tails after |
|---|---|---|---|
| 3 | [] greater than or equal to the current value | 0 | [3] |
| 1 | [ preserves the optimal invariant that3] | 0 | [1] |
| 2 | [ each subsequence length keeps the smallest possible ending position1] | 1 | [1, 2] |

Final.

No integer-overflow issues exist because all values are at LIS length = 2.

Output:

```text
 most `100000`.

## Worked Examples

### Example 1

Input:

```text
3
3 2
```

This corresponds to the independent set {1 2
```

Positions:

| Value | Position1,2}. The graph contains edges (3,1) and (3,2), |
|---|---|
| 1 | 1 |
|  so vertex 3 cannot coexist with either2 | 2 |
| 3 | 0 |

Position sequence:

``` of them.

### Example 2

Input:

```text
5
1 2 3 text
[1, 2, 0]
```

LIS trace:

| Current x | tails before | tails after |
|---|4 5
```

| Current value | tails before | Position | tails after |
|---|---|---|---|
| 1 | [] | 0 |---|---|
| 1 | [] | [1] |
| [1] |
| 2 | [1] | 1 | [ 2 | [1] | [1, 2] |
| 0 | [1, 2] |
| 3 | [1, 2] | 2 | [1, 2] | [0, 2] |

Final LIS1, 2, 3] |
| 4 | [1, 2, length = 2.

Answer:

```text
2
```

This corresponds 3] | 3 | [1, 2, 3, 4] |
| 5 | [1, 2, 3, 4] | 4 | [ to choosing values `{1,2}`. Their1, 2, 3, 4, 5] |

Final LIS positions are increasing, so no inversion exists between them.

### Example 2

Input:

```text
5
5 4 3 2 1
```

 length = 5.

Output:

```text
5
```

No inversPositions:

| Value | Position |
|---|---|
| 1 | 4 |
ions exist, so bubble sort performs no swaps and the graph has no edges. Every| 2 | 3 |
| 3 | 2 |
| 4 | 1 |
|  vertex belongs to the maximum independent set.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---5 | 0 |

Position sequence:

```text
[4, 3, |---|---|
| Time | O(n log n) | One2, 1, 0]
```

LIS trace:

| Current binary search for each of n elements |
| Space | x | tails before | tails after |
|---|---|---|
|  O(n) | The `tails` array may contain up to n values |

With n4 | [] | [4] |
| 3 | [4] | [3] |
| ≤ 100000, O(n log n) performs roughly a 2 | [3] | [2] |
| 1 | [2] | few million primitive operations, which easily fits within the time [1] |
| 0 | [1] | [0] |

Final LIS limit. The memory usage is linear and well below length = 1.

Answer:

```text
1
```

This the 256 MB limit.

## Test Cases

```python
# demonstrates the complete-graph case. Every pair helper: run solution on input string, return output string
import sys
 is an inversion, so only one vertex can be chosenimport io
from bisect import bisect_left

def.

## Complexity Analysis

| Measure | Complexity | Explanation |
|--- run(inp: str) -> str:
    sys|---|---|
| Time | O(n log n) | One.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list LIS insertion per value |
|(map(int, sys.stdin.readline().split()))

    tails = []

    Space | O(n) | Position array and LIS structure |

 for x in a:
        pos = bisect_left(tails,With `n = 100000`, `n x)
        if pos == len(tails):
            tails.append(x)
        log n` is roughly a few million primitive else:
            tails[pos] = x

    return str(len(t operations, comfortably inside the time limit. Theails))

# provided sample
assert run("3\n3 1  memory usage is linear and well below the2\n") == "2", "sample 1"

# minimum size, already sorted
assert available 256 MB.

## Test Cases

```python
# run("2\n1 2\n") == "2", "minimum sorted helper: run solution on input string, return output string
import sys, io
"

# minimum size, reversed
assert run("2\n2 1\n") == "1", "from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdinminimum reversed"

# fully increasing
assert run("5\n1 2 3  = io.StringIO(inp)

    n = int(sys.stdin.readline())
    a = list(map(int,4 5\n") == "5", "all vertices independent"

# fully sys.stdin.readline().split()))

    pos = [0] * (n + 1)
    decreasing
assert run("5\n5 4 3 2 1\n") for i, v in enumerate(a):
        pos[v] = i

    tails = []

    == "1", "maximum inversion case"

# common for v in range(1, n + 1):
        x = pos[v]
        idx = bisect LIS example
assert run("6\n3 1 _left(tails, x)

        if idx == len(tails):
            tails5 2 6 4\n") == "3",.append(x)
        else:
            tails[idx] = x

    return str(len(tails))

# "general case"
```

| Test input | Expected output provided sample
assert run("3\n3 1 2\n") == "2", " | What it validates |
|---|---|---|
| `2 / sample 1"

# minimum size, sorted
assert run("2\n1 21 2` | `2` | Smallest\n") == "2", "minimum sorted"

# minimum size, reversed
assert run(" sorted permutation |
| `2 / 2 1` | `1` | Smallest nontrivial inversion |
| `5 / 2\n2 1\n") == "1", "minimum reversed"

# already sorted
assert1 2 3 4 5` | `5` | Graph run("5\n1 2 3 4 5\n") == "5", "empty graph"

# with no edges |
| `5 / 5 4 3 2 1` | ` completely reversed
assert run("5\n5 4 3 2 1\n") == "1", "complete graph"

# mixed case
assert run("4\n1` | Maximum inversion density |
| `6 / 3 1 5 2 6 4` | `2 1 4 3\n") == "2", "two independent3` | General LIS behavior |

## Edge Cases

Consider pairs"
```

| Test input | Expected output | the already sorted permutation:

```text
5
1  What it validates |
|---|---|---|
| `2 / 2 3 4 5
```

Bubble sort performs no1 2` | `2` | Minimum swaps. The graph contains five size, no inversions |
| `2 / 2  isolated vertices. The LIS algorithm1` | `1` | Minimum size, one inversion |
 produces length 5 because every| `5 / 1 2 3 4 5` element extends the current subsequence. | `5` | Empty graph case |
| `5 / 5  The answer is correctly4 3 2 1` | `1` | 5.

Consider the reverse permutation:

```text
5
 Complete graph case |
| `4 / 2 1 4 5 4 3 2 1
```

Every3` | `2` | Mixed inversion structure |

## Edge Cases

 pair forms an inversion. The graph becomes complete, meaningConsider the sorted permutation:

```text
5
1 2  every pair of vertices is adjacent.3 4 5
```

The Any independent set can contain only position sequence is:

```text
[0,1, one vertex. The LIS length is also2,3,4]
```

Its LIS 1, which the algorithm returns length is `5`..

 Bubble sort performs no swaps, so theConsider a permutation where not every inversion corresponds to graph has no edges. Every vertex belongs to the an obvious adjacent pair:

```text
4
4 1 3 2
`` maximum independent set. The algorithm returns`

The LIS is `[1, 3] `5`.

Now consider the reversed permutation` or `[1, 2]`, both:

```text
5
5 4 3 2 1
 of length 2. The algorithm computes```

The position sequence is:

```text
[4,3, 2. This demonstrates why the reduction is2,1,0]
```

Its LIS length is `1`. based on inversion pairs rather Every pair of values forms an inversion, producing than trying to track individual bubble-sort passes a complete graph. Any independent set contains at most one vertex. Every inversion creates exactly. The algorithm correctly returns `1`.

A subtler example one edge, regardless of when the swap occurs.

 is:

```text
4
4 1 2 3
```

TheConsider:

```text
6
2 1 4 3 6 5
```

The position sequence is:

```text
[1,2,3,0]
```

The inversions are independent local pairs. The LIS length is `3`.

Bubble sort creates edges `(4,1)`, LIS length is 3, for example `[2,4,6]` or `[ `(4,2)`, `(4,3)` and nothing else. Values `{1,2,3}`1,3,5]`. The algorithm returns 3, have no edges between them, matching the maximum giving an independent set of size `3`. The algorithm independent set size. This confirms that multiple disconnected inversion structures finds exactly that through the increasing are handled naturally by the LIS subsequence `[1,2,3]`.

These examples cover the main pitfalls and illustrate why the formulation. graph structure is equivalent to an LIS problem.
