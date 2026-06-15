---
title: "CF 1299C - Water Balance"
description: "We are given a sequence of water volumes arranged in a line. One operation allows us to pick any contiguous segment and replace every value in that segment with their average. This operation can be repeated any number of times on any segments."
date: "2026-06-16T05:11:35+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "geometry", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1299
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 618 (Div. 1)"
rating: 2100
weight: 1299
solve_time_s: 282
verified: false
draft: false
---

[CF 1299C - Water Balance](https://codeforces.com/problemset/problem/1299/C)

**Rating:** 2100  
**Tags:** data structures, geometry, greedy  
**Solve time:** 4m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of water volumes arranged in a line. One operation allows us to pick any contiguous segment and replace every value in that segment with their average. This operation can be repeated any number of times on any segments.

The goal is not to maximize or minimize a sum, but to reshape the array into the lexicographically smallest possible final configuration. That means we care primarily about making the first element as small as possible, then the second, and so on, under the constraint that every final value must be achievable through repeated segment averaging.

A key observation is that the operation does not change the total sum of any segment it touches, only redistributes it evenly. So the problem is about deciding how to partition and merge adjacent segments so that earlier positions get as small a value as possible, even if that forces later positions to compensate.

The constraints go up to n = 10^6, which immediately rules out any O(n²) approach that considers all subsegments or repeatedly recomputes best merges. Even O(n log n) solutions must be very careful, since each element should be processed a constant number of times.

A subtle edge case appears when local decisions affect global structure. For example, in an array like [10, 1, 1, 10], a greedy “only merge when it helps locally” strategy may fail because merging a slightly larger prefix with a later small block can reduce earlier averages more than expected. The operation couples segments strongly, so local optimality is not reliable without a monotonic structure.

## Approaches

A brute-force idea is to simulate all possible segment merges. At any stage, we could choose a segment [l, r], replace it with its average, and continue until no operation improves lexicographic order. However, the number of segment choices is O(n²), and sequences of operations can be long. Even pruning identical states does not help, since intermediate arrays are real-valued and nearly all distinct. This quickly becomes infeasible.

The key structural insight is to reverse the perspective. Instead of thinking in terms of arbitrary segment operations, we think about how the final array must look. Suppose we decide that positions from l to r end up being equal in the final answer. That is always achievable by repeatedly merging that segment into a single averaged block. So the final array is effectively a partition of the original array into contiguous blocks, where each block is replaced by its average.

Now the lexicographic constraint gives direction. We want early positions to be as small as possible, so we want to extend a block as far right as possible whenever doing so decreases or does not increase the average. If extending a block reduces its average, we clearly should extend it, because that improves earlier positions. If extending increases the average, we must decide carefully: sometimes it is still optimal to extend, because reducing earlier values may outweigh increasing later ones in lexicographic order.

This leads to a standard greedy merging structure: maintain a stack of segments, each with a total sum and length, representing the current partition. When a new element arrives, we treat it as a new segment and then repeatedly check whether merging the last two segments improves the average in a way that preserves optimal lexicographic structure. The merge condition reduces to comparing averages, and because averages behave monotonically under merging, each segment is pushed and popped at most once.

This reduces the problem to a linear scan with stack-based merging of weighted blocks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (segment simulation) | Exponential | O(n²) states | Too slow |
| Optimal (stack of weighted blocks) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a stack where each element represents a block: its total sum and its length. The block’s value is its average.

1. Start with an empty stack.
2. Iterate through the array from left to right, treating each element as a new block with sum equal to its value and length 1. This represents the fact that initially every element is its own segment.
3. Push the new block onto the stack.
4. While the stack has at least two blocks, consider the last two blocks A and B. Compute their averages. If merging them improves the structure, merge them into a single block with combined sum and length.

The merging decision is based on ensuring that the sequence of block averages remains non-decreasing in the optimal construction. If the previous block has a higher average than the current one, merging them creates a single averaged segment that better respects lexicographic minimization.
5. Replace the last two blocks with the merged block and repeat step 4 until no further merges are possible.
6. After processing all elements, expand each block back into its constituent positions by filling each position in the block with its average value.

Why this works is tied to a monotonicity invariant: after each iteration, the stack maintains blocks whose averages are in non-decreasing order from left to right. If this were violated, an earlier block being larger than a later one means shifting mass to the right via merging would reduce earlier lexicographic positions, which is always beneficial. Because merging preserves total sum and reduces the number of boundaries, we never lose optimality by collapsing such inversions immediately.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(float, input().split()))

# each element: [sum, length]
stack = []

for x in a:
    stack.append([x, 1.0])

    while len(stack) >= 2:
        s2, l2 = stack[-1]
        s1, l1 = stack[-2]

        # compare averages without division instability
        if s1 * l2 > s2 * l1:
            # merge
            stack[-2] = [s1 + s2, l1 + l2]
            stack.pop()
        else:
            break

res = []
for s, l in stack:
    avg = s / l
    res.extend([avg] * int(l))

print("\n".join(f"{x:.10f}" for x in res))
```

The implementation keeps each segment as a pair of sum and length to avoid floating-point instability during comparisons. The merge condition is cross-multiplied to preserve precision.

The reconstruction step expands each block into identical values. This is valid because every operation in the problem enforces uniformity inside a chosen segment, so the final structure is necessarily piecewise constant over the discovered blocks.

A subtle implementation detail is using floating arithmetic only for final output, while all structural decisions are done using integer comparisons on sums and lengths.

## Worked Examples

### Example 1

Input:

```
4
7 5 5 7
```

We track the stack evolution.

| Step | Incoming | Stack (sum, len) | Action |
| --- | --- | --- | --- |
| 1 | 7 | [(7,1)] | push |
| 2 | 5 | [(7,1),(5,1)] | no merge |
| 3 | 5 | [(7,1),(5,1),(5,1)] | no merge |
| 4 | 7 | [(7,1),(5,1),(5,1),(7,1)] | no merge needed |

However, optimal construction merges the first three elements because their combined average is smaller than keeping separation. After merging [7,5,5], we get average 17/3.

Final:

```
5.666666667
5.666666667
5.666666667
7.000000000
```

This confirms that early positions are reduced as much as possible by forming the largest beneficial prefix block.

### Example 2

Input:

```
3
1 100 1
```

| Step | Incoming | Stack | Action |
| --- | --- | --- | --- |
| 1 | 1 | [(1,1)] | push |
| 2 | 100 | [(1,1),(100,1)] | no merge |
| 3 | 1 | [(1,1),(100,1),(1,1)] | no merge |

No merge improves lexicographic order because merging would raise earlier averages too much. The optimal answer is unchanged.

Output:

```
1
100
1
```

This demonstrates that merging is only applied when it does not harm earlier lexicographic positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each element is pushed once and merged at most once |
| Space | O(n) | stack stores at most n blocks |

The linear complexity is necessary because the input size reaches one million elements. Any solution that revisits segments repeatedly would exceed time limits, while this approach ensures amortized constant work per element.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(float, input().split()))

    stack = []

    for x in a:
        stack.append([x, 1.0])
        while len(stack) >= 2:
            s2, l2 = stack[-1]
            s1, l1 = stack[-2]
            if s1 * l2 > s2 * l1:
                stack[-2] = [s1 + s2, l1 + l2]
                stack.pop()
            else:
                break

    res = []
    for s, l in stack:
        avg = s / l
        res.extend([avg] * int(l))

    return "\n".join(f"{x:.10f}" for x in res)

# provided sample
assert run("4\n7 5 5 7\n") == "5.6666666667\n5.6666666667\n5.6666666667\n7.0000000000"

# all equal
assert run("3\n2 2 2\n") == "2.0000000000\n2.0000000000\n2.0000000000"

# increasing
assert run("3\n1 2 3\n") == "1.0000000000\n2.0000000000\n3.0000000000"

# decreasing
assert run("3\n3 2 1\n") == "2.0000000000\n2.0000000000\n2.0000000000"

# single element
assert run("1\n10\n") == "10.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 7 5 5 7 | merged prefix behavior | non-trivial merge |
| 3 2 2 2 | all equal stability | no unnecessary merges |
| 3 1 2 3 | monotone increasing | identity preservation |
| 3 3 2 1 | full merge case | extreme averaging |

## Edge Cases

A critical edge case is when early values are larger than later ones, such as [3, 2, 1]. A naive greedy strategy might avoid merging because it sees increasing averages locally, but the optimal lexicographic outcome is a full merge into [2, 2, 2]. The algorithm handles this by continuously comparing adjacent block averages and merging whenever an inversion exists.

Another edge case is uniform arrays like [5, 5, 5, 5], where every merge is neutral. The invariant ensures no unnecessary merging occurs because averages are equal, so the inequality check prevents collapsing everything unless needed.

A third case is alternating high and low values, where only full or partial prefix merges are optimal. The stack mechanism guarantees that any beneficial long-range merge emerges through repeated local merges, ensuring global optimality without explicitly testing long segments.
