---
title: "CF 106107G - Count the squares"
description: "We are given several test cases. In each test case there is a collection of squares, each square having an integer side length."
date: "2026-06-19T22:21:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106107
codeforces_index: "G"
codeforces_contest_name: "SCPC Teens 2025"
rating: 0
weight: 106107
solve_time_s: 55
verified: true
draft: false
---

[CF 106107G - Count the squares](https://codeforces.com/problemset/problem/106107/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each test case there is a collection of squares, each square having an integer side length. From this collection we must count how many ways to choose three distinct squares such that these three squares can be placed edge-aligned to exactly tile a rectangle without gaps or overlaps.

Each chosen square must be used entirely, rotations are not needed because squares are symmetric, and we are not allowed to break or merge squares. The question is purely about whether three given square tiles can perfectly form a larger rectangle.

The constraints allow up to a total of 200,000 squares across all test cases, so any solution that tries all triples directly is impossible. A cubic or even quadratic approach per test case will not survive. The intended solution must reduce the problem to counting patterns over frequencies of side lengths.

A subtle point is that we are not arranging squares arbitrarily in the plane, but only checking whether some arrangement exists. This means we are classifying valid geometric tilings, not simulating placements.

A naive pitfall appears when assuming that any three squares can be combined if their areas sum to a rectangle area. For example, squares with sides 1, 2, 3 have total area 14, which is not a perfect rectangle area in any meaningful tiling sense with axis-aligned squares, yet area-based reasoning alone is insufficient and misleading.

Another common mistake is assuming that having two equal squares is always enough. For instance, sides 2, 2, 3 do not form a valid rectangle tiling, even though duplication might suggest symmetry.

The core difficulty is identifying the limited number of valid tiling configurations for exactly three squares.

## Approaches

A brute-force method would try every triple of indices and check whether the three squares can form a rectangle. For each triple, one would attempt all geometric placements or equivalently test all tiling configurations. This leads to roughly $O(n^3)$ triples per test case, which is far beyond feasible limits when $n$ reaches $2 \cdot 10^5$.

Even if we optimize the geometric check, the bottleneck remains the number of triples. The key observation is that the structure of valid tilings with exactly three squares is extremely restricted.

If we imagine constructing a rectangle from squares, there are only two fundamental ways to partition a rectangle into three axis-aligned squares. One is placing three identical squares in a row or column. The other is placing two identical smaller squares forming a strip, with one larger square occupying the remaining space in the other dimension.

This observation transforms the problem from geometry into frequency counting over side lengths. Instead of testing triples, we only need to count two specific patterns in the multiset of values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Frequency counting | $O(n \log n)$ or $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, count how many times each square side length appears. This reduces the problem from individual squares to frequencies of identical sizes.
2. Count triples where all three squares have the same side length. If a value $x$ appears $f$ times, then it contributes $\binom{f}{3}$ valid triples. This corresponds to forming a rectangle as a 3-by-1 strip of identical squares.
3. Count triples where two squares have side length $a$ and one square has side length $2a$. For each value $a$, if $2a$ exists, then the number of ways to choose such triples is $\binom{f[a]}{2} \cdot f[2a]$. This corresponds to a $2 \times 1$ tiling in one dimension and a single square filling the remaining region.
4. Sum both contributions over all values and output the result for the test case.

### Why it works

Any valid tiling of a rectangle using exactly three squares must align squares in a way that forms either a single row or column of three equal squares, or a two-layer structure where one square spans an entire dimension and the other two fill the remaining region symmetrically. There is no way to partition a rectangle into three unequal axis-aligned squares without creating gaps or forcing non-square regions. This restricts all valid configurations to exactly the two counted cases, making the counting complete and exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import Counter

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = Counter(a)
        ans = 0
        
        for x, fx in freq.items():
            if fx >= 3:
                ans += fx * (fx - 1) * (fx - 2) // 6
            
        for a_val, fa in freq.items():
            b_val = 2 * a_val
            if b_val in freq:
                ans += fa * (fa - 1) // 2 * freq[b_val]
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first compresses the input into a frequency map. This is essential because all valid constructions depend only on how many times each side length appears, not their positions.

The combination formula for identical triples directly counts unordered index selections. The second term carefully fixes one value as the larger square and selects two identical smaller ones. Using combinations avoids ordering issues since triples are defined by index sets with $i < j < k$.

A subtle implementation detail is iterating over the frequency map rather than the raw array, ensuring linear behavior per test case.

## Worked Examples

### Example 1

Input:

```
1
4
3 3 3 3
```

We build frequencies:

| value | frequency |
| --- | --- |
| 3 | 4 |

All-equal contribution:

| step | fx | contribution |
| --- | --- | --- |
| 3 identical | 4 | C(4,3) = 4 |

No other values exist, so answer is 4.

This demonstrates the “all equal squares” configuration corresponding to a 1-by-3 tiling.

### Example 2

Input:

```
1
5
2 2 4 2 4
```

Frequencies:

| value | frequency |
| --- | --- |
| 2 | 3 |
| 4 | 2 |

All-equal:

C(3,3) = 1 from value 2.

Mixed case:

For a = 2, b = 4:

C(3,2) * 2 = 3 * 2 = 6.

Final answer is 7.

This shows both configurations coexisting in one multiset.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | Each element is counted once and each frequency is processed once |
| Space | $O(n)$ | Frequency map stores distinct side lengths |

The sum of $n$ over all test cases is $2 \cdot 10^5$, so linear processing across all tests easily fits within the time limit.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    import sys
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = Counter(a)
        ans = 0
        
        for x, fx in freq.items():
            if fx >= 3:
                ans += fx * (fx - 1) * (fx - 2) // 6
        
        for a_val, fa in freq.items():
            b_val = 2 * a_val
            if b_val in freq:
                ans += fa * (fa - 1) // 2 * freq[b_val]
        
        output.append(str(ans))
    
    return "\n".join(output)

# provided sample-style checks
assert run("1\n3\n3 3 3\n") == "1"

# custom cases

# minimum case
assert run("1\n3\n1 2 3\n") == "0"

# all equal large frequency
assert run("1\n5\n5 5 5 5 5\n") == "10"

# mixed valid (a,a,2a)
assert run("1\n3\n2 2 4\n") == "1"

# multiple test cases
assert run("2\n3\n1 1 1\n3\n1 1 2\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 3 1 2 3 | 0 | no valid tiling exists |
| 1 5 5 5 5 5 | 10 | combinatorics for all-equal case |
| 1 3 2 2 4 | 1 | mixed (a,a,2a) case |
| 2 tests combined | 1 1 | multi-test correctness |

## Edge Cases

A corner case arises when all squares are identical. For input `1 1 1`, there is exactly one way to choose all three, and it forms a valid rectangle. The algorithm handles this entirely through the combination term $\binom{f}{3}$, which correctly counts all index triples without extra logic.

Another edge case is when only the mixed pattern exists, such as `2 2 4`. Here the algorithm avoids counting any invalid arrangements because it only considers the strict relationship $b = 2a$, preventing accidental inclusion of unrelated values.

A final subtle case is large frequencies, for example many identical squares. The combination formula grows quickly but remains safe in Python due to big integers, and the computation still runs in linear time because it avoids enumerating triples explicitly.
