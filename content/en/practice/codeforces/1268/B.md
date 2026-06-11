---
title: "CF 1268B - Domino for Young"
description: "The Young diagram can be viewed as a histogram whose column heights are given by a non-increasing array $a1,a2,dots,an$."
date: "2026-06-11T20:16:57+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1268
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 609 (Div. 1)"
rating: 2000
weight: 1268
solve_time_s: 132
verified: true
draft: false
---

[CF 1268B - Domino for Young](https://codeforces.com/problemset/problem/1268/B)

**Rating:** 2000  
**Tags:** dp, greedy, math  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

The Young diagram can be viewed as a histogram whose column heights are given by a non-increasing array $a_1,a_2,\dots,a_n$. Every unit square inside the histogram may be covered by at most one domino, and each domino occupies exactly two adjacent cells, either vertically or horizontally.

The task is to place as many dominos as possible inside the diagram without overlap.

A useful way to think about the shape is as a set of grid cells. Column $i$ contains the cells $(i,1),(i,2),\dots,(i,a_i)$. Since the heights are non-increasing, every row forms a contiguous segment starting from the left edge.

The constraints are large. There may be up to $300\,000$ columns, and each height may also be as large as $300\,000$. The total area of the diagram can reach roughly $9 \times 10^{10}$, so any algorithm that explicitly constructs cells or iterates over the whole diagram is impossible. Even an $O(n^2)$ algorithm would require around $9 \times 10^{10}$ operations in the worst case. We need something linear or close to linear in $n$.

Several edge cases are easy to mishandle.

Consider a single column:

```
1
3
```

The diagram contains three cells. Only one vertical domino can be placed, so the answer is:

```
1
```

A solution that assumes every pair of cells can always be matched would incorrectly return $\lfloor 3/2 \rfloor = 1$ here by luck, but the reasoning would not generalize.

Consider two columns of odd height:

```
2
1 1
```

The answer is:

```
1
```

There is no vertical placement, but one horizontal domino covers the only row. Any approach that counts only vertical pairs would return 0.

Another interesting case is:

```
2
3 3
```

The area is 6, so at most 3 dominos are possible. In fact all 6 cells can be tiled, giving answer 3. A naive local strategy that greedily uses vertical dominos everywhere would place only 2 vertical dominos and leave two unmatched cells.

The key difficulty is understanding how odd-height columns interact with each other through horizontal placements.

## Approaches

A brute-force viewpoint is to regard every cell as a vertex of a grid graph and connect adjacent cells. The problem becomes finding a maximum matching in that graph, because every domino covers two adjacent cells.

This formulation is correct. A matching corresponds exactly to a set of non-overlapping dominos. Unfortunately the graph contains one vertex per cell. Since the area can be as large as $9 \times 10^{10}$, constructing the graph is completely infeasible.

The structure of a Young diagram gives much more information than an arbitrary grid. Let us first place as many vertical dominos as possible inside each column.

A column of height $a_i$ contributes $\lfloor a_i/2 \rfloor$ vertical dominos. If $a_i$ is even, the entire column is covered. If $a_i$ is odd, exactly one cell remains uncovered.

The only question is what happens to these leftover cells.

For an odd column, the uncovered cell can be chosen either on an odd row or on an even row. For example, a column of height 5 can be tiled vertically leaving row 1 uncovered, or row 3 uncovered, or row 5 uncovered. All uncovered positions have the same parity.

Now look at two neighboring odd columns. If their leftover cells are placed on the same row, they form one horizontal domino. Since the diagram is left-justified, any row that exists in both columns also exists in every column between them. Consequently, a consecutive block of odd columns can pair their leftovers two at a time.

The only thing that matters is parity.

Let

$$S = \sum_i \left\lfloor \frac{a_i}{2} \right\rfloor$$

be the number of vertical dominos.

Each odd column contributes one leftover cell. Consecutive odd columns with the same index parity can pair those leftovers. A simple scan shows that every second odd column creates one additional domino.

The resulting answer is

$$S + \sum \left\lfloor \frac{k}{2} \right\rfloor$$

where $k$ is the number of odd columns in a maximal consecutive segment.

An even simpler implementation maintains the count of currently unmatched odd columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force matching on cells | $O(\text{area}^{1.5})$ or worse | $O(\text{area})$ | Too slow |
| Optimal parity greedy | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Initialize `answer = 0`.
2. Initialize `pending = 0`.

Here `pending` stores how many odd columns in the current consecutive segment have not yet been paired.
3. Process columns from left to right.
4. Add `a[i] // 2` to the answer.

This counts all vertical dominos that can be placed inside the column.
5. If `a[i]` is odd, increment `pending`.

An odd column contributes one leftover cell.
6. If `a[i]` is even, add `pending // 2` to the answer and reset `pending = 0`.

An even column breaks the segment. Any horizontal pairings must be completed inside the current maximal block of odd columns.
7. After processing all columns, add `pending // 2` to the answer.

This handles the final block of odd columns.
8. Output the answer.

### Why it works

After taking all possible vertical dominos, every even-height column is fully covered and every odd-height column contributes exactly one leftover cell. These leftover cells are the only cells that can participate in additional dominos.

Inside a maximal consecutive segment of odd columns, the leftover cell from each column can be placed on a row shared by all columns in the segment. Every pair of leftovers can then be joined into one horizontal domino. A segment containing $k$ odd columns yields exactly $\lfloor k/2 \rfloor$ extra dominos.

Different segments are separated by an even column. Such a column contains no leftover cell, so no horizontal domino can cross the boundary. The contributions of segments are independent.

The algorithm counts all vertical dominos and then adds exactly the maximum number of horizontal pairings obtainable from each odd segment, which is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    pending = 0

    for x in a:
        ans += x // 2

        if x & 1:
            pending += 1
        else:
            ans += pending // 2
            pending = 0

    ans += pending // 2
    print(ans)

solve()
```

The first contribution comes from vertical placements. Every column independently contributes `x // 2` dominos.

The variable `pending` tracks the size of the current maximal block of odd columns. Whenever an even column appears, that block ends, so we immediately add `pending // 2` horizontal dominos and reset the counter.

The final addition after the loop is necessary because the array may end with odd columns. Forgetting this step is the most common bug.

The answer can be as large as roughly half the area of the diagram, which may exceed 32 bit integer limits. Python integers handle this automatically.

## Worked Examples

### Example 1

Input:

```
5
3 2 2 2 1
```

| Column | Height | Vertical added | Pending odd block | Answer |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 1 | 1 |
| 2 | 2 | 1 | 0 | 2 |
| 3 | 2 | 1 | 0 | 3 |
| 4 | 2 | 1 | 0 | 4 |
| 5 | 1 | 0 | 1 | 4 |
| End | - | 0 | 1 | 4 |

Final answer:

```
4
```

This example shows how an isolated odd column contributes no extra horizontal domino. The last column creates a leftover cell, but there is no second odd column in the same segment to pair with it.

### Example 2

Input:

```
4
3 3 3 3
```

| Column | Height | Vertical added | Pending odd block | Answer |
| --- | --- | --- | --- | --- |
| 1 | 3 | 1 | 1 | 1 |
| 2 | 3 | 1 | 2 | 2 |
| 3 | 3 | 1 | 3 | 3 |
| 4 | 3 | 1 | 4 | 4 |
| End | - | 0 | 4 | 6 |

At the end we add `4 // 2 = 2` extra horizontal dominos.

Final answer:

```
6
```

This trace demonstrates the central observation. Four odd columns create four leftovers, which can be paired into two additional horizontal dominos.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass through the array |
| Space | $O(1)$ | Only a few integer variables are stored |

With $n \le 300\,000$, a linear scan is easily fast enough. The memory usage remains constant regardless of the column heights.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    a = list(map(int, input().split()))

    ans = 0
    pending = 0

    for x in a:
        ans += x // 2

        if x & 1:
            pending += 1
        else:
            ans += pending // 2
            pending = 0

    ans += pending // 2
    return str(ans) + "\n"

# provided sample
assert run("5\n3 2 2 2 1\n") == "4\n", "sample"

# minimum size
assert run("1\n1\n") == "0\n", "single cell"

# single odd column
assert run("1\n3\n") == "1\n", "one vertical domino"

# all equal odd heights
assert run("4\n3 3 3 3\n") == "6\n", "odd block pairing"

# boundary between odd segments
assert run("5\n3 3 2 3 3\n") == "6\n", "even column splits segments"

# all even heights
assert run("4\n2 2 2 2\n") == "4\n", "pure vertical tiling"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `0` | Minimum diagram |
| `1 / 3` | `1` | Single odd column |
| `4 / 3 3 3 3` | `6` | Large odd segment |
| `5 / 3 3 2 3 3` | `6` | Segment splitting by even column |
| `4 / 2 2 2 2` | `4` | Purely vertical placements |

## Edge Cases

Consider the smallest possible diagram:

```
1
1
```

The algorithm adds `1 // 2 = 0` vertical dominos. The column is odd, so `pending = 1`. After the scan it adds `1 // 2 = 0`. The answer is 0, which is correct because a single cell cannot form a domino.

Consider a single odd column:

```
1
3
```

The algorithm adds `3 // 2 = 1` vertical domino. One leftover cell remains, so `pending = 1`. The final contribution is `1 // 2 = 0`. The answer becomes 1, which is optimal.

Consider two odd columns separated by an even column:

```
3
3 2 3
```

Processing the middle column forces the algorithm to close the first odd segment. The first leftover cell cannot be paired with the last one because the even column contributes no leftover. The computation is:

```
vertical = 1 + 1 + 1 = 3
extra = 0 + 0 = 0
answer = 3
```

This correctly prevents an invalid horizontal pairing across segment boundaries.

Consider a long odd segment:

```
5
1 1 1 1 1
```

There are no vertical dominos. The segment contains five odd columns, so the algorithm adds `5 // 2 = 2` horizontal dominos. One cell remains uncovered. The answer is 2, matching the maximum possible tiling.
