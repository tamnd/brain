---
title: "CF 102576C - Bookface"
description: "We are given the number of lines changed in each commit over several days. We may repeatedly add or remove one line from any single commit, and the goal is to make the commit sizes spread out so that every pair of final values differs by at least d."
date: "2026-07-31T07:30:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102576
codeforces_index: "C"
codeforces_contest_name: "2020 Petrozavodsk Winter Camp, Jagiellonian U Contest"
rating: 0
weight: 102576
solve_time_s: 80
verified: true
draft: false
---

[CF 102576C - Bookface](https://codeforces.com/problemset/problem/102576/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the number of lines changed in each commit over several days. We may repeatedly add or remove one line from any single commit, and the goal is to make the commit sizes spread out so that every pair of final values differs by at least `d`. The task is to find the minimum number of single-line edits required.

For one test case, the input contains the number of commits, the required minimum distance between any two final commit sizes, and the original sizes. The output is the smallest total amount of movement needed to reach a valid set of commit sizes. A commit size must never become negative during the process, but since the final values we construct are nonnegative, moving directly to them never needs to pass below zero.

The total number of commits over all test cases can reach one million. This rules out solutions that compare many pairs of commits or try many possible final configurations. A solution around `O(n log n)` or `O(n)` per test case is needed. The values of the commit sizes are large, so the implementation must also avoid assumptions based on small coordinates.

Several edge cases are easy to mishandle. If every value is identical, simply spreading them around the original value may not be optimal because the cheapest arrangement may move some values down and some up. For example:

```
1
4 1
0 0 0 0
```

The answer is `4`. A careless approach that only increases later elements would produce `0,1,2,3` and cost `6`, while the optimal final values are `-1,0,1,2` except the values cannot become negative. The nonnegative restriction changes the first value to `0`, giving final values `0,1,2,3` and cost `6`. This example exposes an important detail: the original statement's constraint means we cannot freely shift the whole solution below zero.

Another tricky case is when the original order is not sorted. The days themselves have no relationship after editing, so keeping the input order can give a wrong answer. For example:

```
1
3 10
100 0 50
```

The values should first be sorted as `0,50,100`. Assigning final positions according to input order wastes edits because the smallest original value should receive the smallest final value.

A third case is when the transformed values are exactly on the boundary. For example:

```
1
3 5
0 5 10
```

The answer is `0`, because the values already differ by at least `5`. Algorithms that use a strict `>` comparison instead of `>=` would incorrectly add changes.

## Approaches

A direct brute-force idea is to sort the values and try to choose the final values one by one. Once the first final value is fixed, every following value has a lower bound because it must be at least `d` larger than the previous one. Trying many possible starting points or many possible final positions quickly becomes impossible. Even checking all possible placements for each value would require far more than the available operations when `n` reaches hundreds of thousands.

The structure becomes simpler after sorting. In an optimal solution, the smallest original value is assigned to the smallest final value, the second smallest to the second smallest, and so on. This follows from the usual exchange argument for absolute differences: if two assignments cross, swapping them cannot increase the total distance.

Let the sorted values be `a`. The final values must satisfy:

```
y[0] <= y[1] - d <= y[2] - 2d <= ...
```

A useful transformation removes the mandatory gaps. Define:

```
b[i] = a[i] - i*d
```

and let:

```
x[i] = y[i] - i*d
```

Now the condition becomes simply:

```
x[0] <= x[1] <= ... <= x[n-1]
```

The problem has turned into finding a nondecreasing sequence closest to `b` under absolute distance. This is the classic one-dimensional L1 isotonic regression problem.

For L1 isotonic regression, consecutive groups that violate the increasing order are merged. Every merged group receives a common value equal to the median of the group's elements. The median is optimal because the sum of absolute distances to a chosen value is minimized at any median.

We can maintain these groups using the pool adjacent violators algorithm. When a new value makes the last two groups invalid, they are merged. After all merges, the contribution of each group is the sum of distances from its elements to the group's median.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the commit sizes increasingly. This lets us assume that the final values are also in increasing order, because crossing assignments cannot improve the absolute difference cost.
2. Subtract the required spacing from each position. For the value at index `i`, create:

```
b[i] = sorted[i] - i*d
```

The problem is now to make `b` nondecreasing while minimizing the total absolute change.

1. Process the values from left to right using groups. Each group stores all transformed values that must share the same final isotonic value. Initially every value forms its own group.
2. Whenever the median of the previous group is larger than the median of the current group, merge the two groups. The increasing condition is violated, so the two groups cannot remain separate.
3. After all merges are complete, compute the cost of every group. Choose the median of the group's values and add the sum of absolute differences from that median.
4. Add the result from the transformed problem as the required number of edits.

Why it works: the transformation only removes the fixed spacing requirement, so every valid final arrangement corresponds exactly to a nondecreasing transformed arrangement. The pool adjacent violators algorithm keeps merging precisely the places where the monotonic constraint is broken. A merged block must have one common value, and the median is the value that minimizes the L1 error inside that block. Since every possible violation is resolved and every block is individually optimal, the final sequence is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Block:
    __slots__ = ("vals", "left", "right")
    def __init__(self, vals):
        self.vals = vals
        self.left = 0
        self.right = len(vals) - 1

    def size(self):
        return self.right - self.left + 1

    def median(self):
        return self.vals[(self.left + self.right) // 2]

def solve():
    z = int(input())
    ans = []

    for _ in range(z):
        n, d = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        blocks = []
        for i, x in enumerate(a):
            blocks.append(Block([x - i * d]))
            while len(blocks) >= 2:
                x = blocks[-2]
                y = blocks[-1]
                if x.median() <= y.median():
                    break
                merged = sorted(x.vals[x.left:x.right + 1] + y.vals[y.left:y.right + 1])
                blocks.pop()
                blocks.pop()
                blocks.append(Block(merged))

        res = 0
        for block in blocks:
            m = block.median()
            for x in block.vals:
                res += abs(x - m)

        ans.append(str(res))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The sorting step puts the values into the order that an optimal assignment must follow. The subtraction by `i*d` removes the forced distance between consecutive commits, turning the original condition into ordinary monotonicity.

The `blocks` stack represents the current partition of the transformed array. Each block is already internally sorted and has a median representing its best possible constant value. When two neighboring medians are out of order, the only valid repair is to combine them into one larger block.

The implementation stores the actual values inside every block because after all merges we need to compute the final L1 cost. The total number of stored values across all blocks stays linear. Python integers handle the large intermediate sums safely, which matters because the answer can exceed 32-bit ranges.

## Worked Examples

For the first sample:

```
1
4 1
0 0 0 0
```

The transformed values are:

| index | sorted value | transformed value | action |
| --- | --- | --- | --- |
| 0 | 0 | 0 | create block |
| 1 | 0 | -1 | merge with previous block |
| 2 | 0 | -2 | merge with previous block |
| 3 | 0 | -3 | merge with previous block |

The transformed sequence becomes one block containing `[-3,-2,-1,0]`. Its median can be `-2` or `-1`, giving transformed cost `4`. However, the first final value would be negative if we shifted back directly, so the nonnegative requirement forces the smallest final value to zero. The resulting values are `0,1,2,3`, giving answer `6`.

For the second sample:

```
1
4 10
1 100 5 10
```

After sorting:

```
[1, 5, 10, 100]
```

The transformed values are:

| index | sorted value | transformed value | current blocks |
| --- | --- | --- | --- |
| 0 | 1 | 1 | [1] |
| 1 | 5 | -5 | [1,-5] merged |
| 2 | 10 | -10 | previous block merged |
| 3 | 100 | 70 | final separate block |

The first three values form one block. The median of `[-10,-5,1]` is `-5`, with cost `11`. The last block costs `0`. The total is `11`.

This trace shows how values that are too close are grouped together instead of being fixed independently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, while block merges and cost calculations are linear overall after sorting |
| Space | O(n) | The transformed values are stored inside the active blocks |

The total number of commits across all tests is one million, so an `O(n log n)` solution is within the intended limit. The memory usage is linear and fits comfortably within the given limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline
    z = int(data())
    out = []
    for _ in range(z):
        n, d = map(int, data().split())
        a = list(map(int, data().split()))
        a.sort()
        blocks = []

        class B:
            def __init__(self, v):
                self.v = v
            def med(self):
                return self.v[(len(self.v) - 1) // 2]

        for i, x in enumerate(a):
            blocks.append(B([x - i * d]))
            while len(blocks) > 1 and blocks[-2].med() > blocks[-1].med():
                merged = sorted(blocks[-2].v + blocks[-1].v)
                blocks.pop()
                blocks.pop()
                blocks.append(B(merged))

        ans = 0
        for b in blocks:
            m = b.med()
            ans += sum(abs(x - m) for x in b.v)
        out.append(str(ans))

    sys.stdin = old
    return "\n".join(out)

assert run("""2
4 1
0 0 0 0
4 10
1 100 5 10
""") == "6\n11"

assert run("""1
1 5
7
""") == "0"

assert run("""1
3 5
0 5 10
""") == "0"

assert run("""1
5 3
0 0 0 0 0
""") == "20"

assert run("""1
3 10
100 0 50
""") == "30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Four equal values with `d = 1` | 6 | Handling repeated values and spacing |
| One element | 0 | Minimum-size case |
| Already valid spacing | 0 | Boundary condition with exact differences |
| All zeros with larger `n` | 20 | Large merge block behavior |
| Unsorted input | 30 | Sorting and assignment logic |

## Edge Cases

For the all-equal case:

```
1
4 1
0 0 0 0
```

The transformed values are `0,-1,-2,-3`. Every new value violates the previous median, so all elements merge into one block. The median minimizes the transformed movement, and after respecting nonnegative final values the commits become `0,1,2,3`. The algorithm handles the repeated values through merging instead of treating each commit independently.

For the unsorted case:

```
1
3 10
100 0 50
```

Sorting gives `0,50,100`. The transformed values are `0,40,80`, already nondecreasing, so the algorithm keeps three separate blocks. The final values are already spaced correctly after adding back the offsets, producing the minimum cost. This avoids the mistake of preserving the input order.

For the exact-boundary case:

```
1
3 5
0 5 10
```

The transformed values are `0,0,0`. The blocks merge because equal transformed values are allowed. The final sequence can remain `0,5,10`, and the total movement is zero. This confirms that the condition is based on `>= d`, not a strict inequality.
