---
title: "CF 6A - Triangle"
description: "We are given four stick lengths, and we must choose exactly three of them. Depending on the relationship between those three lengths, there are three possible outcomes."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "geometry"]
categories: ["algorithms"]
codeforces_contest: 6
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 6 (Div. 2 Only)"
rating: 900
weight: 6
solve_time_s: 78
verified: true
draft: false
---
[CF 6A - Triangle](https://codeforces.com/problemset/problem/6/A)

**Rating:** 900  
**Tags:** brute force, geometry  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four stick lengths, and we must choose exactly three of them. Depending on the relationship between those three lengths, there are three possible outcomes.

If the chosen sticks can form a triangle with positive area, we print `TRIANGLE`. Geometrically, this means the sum of the two smaller sides is strictly greater than the largest side.

If a proper triangle is impossible, we still check whether the sticks can lie on a straight line. That happens when the sum of the two smaller sides is exactly equal to the largest side. In that case we print `SEGMENT`.

If neither condition is possible for any choice of three sticks, we print `IMPOSSIBLE`.

The input size is tiny. We only have four numbers, so there are exactly four different triples to test. Even a brute-force solution that checks every combination runs instantly. With such small constraints, the challenge is not optimization, it is correctly handling the geometry conditions.

The most common mistake is mixing up the strict and non-strict triangle inequalities. A proper triangle requires:

$$a + b > c$$

after sorting the three sides so that $c$ is the largest.

A degenerate triangle, which the problem calls a segment, requires:

$$a + b = c$$

Using `>=` instead of `>` would incorrectly classify segments as triangles.

Consider the input:

```
1 2 3 10
```

The sticks `1 2 3` form a straight segment because `1 + 2 = 3`. The correct output is:

```
SEGMENT
```

A careless implementation using `>=` would incorrectly print `TRIANGLE`.

Another easy mistake is stopping too early after checking only one triple. For example:

```
1 1 2 3
```

The triple `1 1 2` is only a segment, but `1 2 3` is impossible. Since no proper triangle exists anywhere, the correct answer is still:

```
SEGMENT
```

We must examine all four possible triples before deciding.

There is also the opposite situation:

```
4 2 1 3
```

The triple `1 2 3` is only a segment, but `2 3 4` forms a valid triangle because `2 + 3 > 4`. The correct answer is:

```
TRIANGLE
```

An implementation that immediately prints `SEGMENT` after seeing one degenerate case would be wrong. Proper triangles always take priority.

## Approaches

The direct brute-force approach is to generate every set of three sticks from the four available sticks. There are only four such combinations, so we can simply test each one independently.

For every triple, we sort the three lengths. Once sorted, we only need to compare the sum of the two smaller values with the largest one.

If:

$$a + b > c$$

then we already know the answer must be `TRIANGLE`, because a proper triangle has higher priority than every other outcome.

If equality holds instead:

$$a + b = c$$

then we remember that a segment is possible, but we still continue checking other triples in case a real triangle appears later.

The brute-force solution is already fully acceptable because the number of operations is constant. We test only four triples, each involving a tiny sort of three numbers.

There is no meaningful asymptotic optimization beyond this. The key observation is that the input size is fixed and extremely small, so the cleanest solution is also the best solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all triples | O(1) | O(1) | Accepted |
| Optimized observation-based check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four stick lengths into an array.
2. Generate every combination of three sticks from the four available sticks. Since there are only four sticks, this produces exactly four triples.
3. For each triple, sort the three lengths in non-decreasing order.
4. Let the sorted sides be `a`, `b`, and `c`, where `c` is the largest side.
5. If `a + b > c`, immediately print `TRIANGLE` and stop. A valid triangle has the highest priority, so no further checks matter.
6. If `a + b == c`, remember that a degenerate triangle exists. Do not stop yet, because another triple may still form a proper triangle.
7. After checking all triples, print `SEGMENT` if at least one degenerate triangle was found.
8. Otherwise print `IMPOSSIBLE`.

### Why it works

Sorting each triple reduces the triangle condition to a single comparison involving the largest side. For any three sorted sides `a ≤ b ≤ c`, the triangle inequality only needs to check whether `a + b` is greater than `c`.

The algorithm examines every possible choice of three sticks, so it cannot miss a valid configuration. Since `TRIANGLE` has higher priority than `SEGMENT`, immediately returning after finding a proper triangle is correct. If no proper triangle exists but at least one equality case appears, the correct classification is `SEGMENT`. If neither condition occurs, no triangle of any kind can be formed.

## Python Solution

```python
import sys
from itertools import combinations

input = sys.stdin.readline

sticks = list(map(int, input().split()))

segment = False

for triple in combinations(sticks, 3):
    a, b, c = sorted(triple)

    if a + b > c:
        print("TRIANGLE")
        sys.exit()

    if a + b == c:
        segment = True

if segment:
    print("SEGMENT")
else:
    print("IMPOSSIBLE")
```

The solution begins by reading the four stick lengths. Since we need every possible group of three sticks, `itertools.combinations` is the cleanest way to generate them.

Each triple is sorted before checking the triangle condition. This step is essential because the comparison only works correctly when `c` is the largest side. Forgetting to sort can produce incorrect results.

The first condition checks for a proper triangle using strict inequality. The moment such a triple is found, the program prints `TRIANGLE` and exits immediately. No later triple can produce a higher-priority answer.

The second condition checks for equality. Instead of printing immediately, we store the result in the `segment` flag. This avoids the earlier mistake where a later triple could still form a proper triangle.

At the end, if no triangle was found but at least one segment configuration existed, the program prints `SEGMENT`. Otherwise the answer is `IMPOSSIBLE`.

The numbers are extremely small, so integer overflow is impossible in Python. The implementation is mostly about getting the condition order correct.

## Worked Examples

### Example 1

Input:

```
4 2 1 3
```

| Triple | Sorted Triple | Check | Result |
| --- | --- | --- | --- |
| (4,2,1) | (1,2,4) | 1 + 2 < 4 | Impossible |
| (4,2,3) | (2,3,4) | 2 + 3 > 4 | Triangle found |

The algorithm stops immediately after finding `(2,3,4)` because a proper triangle has priority over every other outcome. The final answer is:

```
TRIANGLE
```

This trace demonstrates why we cannot stop after seeing one failed triple. Different selections of sticks may behave differently.

### Example 2

Input:

```
1 2 3 10
```

| Triple | Sorted Triple | Check | Result |
| --- | --- | --- | --- |
| (1,2,3) | (1,2,3) | 1 + 2 = 3 | Segment |
| (1,2,10) | (1,2,10) | 1 + 2 < 10 | Impossible |
| (1,3,10) | (1,3,10) | 1 + 3 < 10 | Impossible |
| (2,3,10) | (2,3,10) | 2 + 3 < 10 | Impossible |

No proper triangle exists, but one degenerate case does exist. The answer becomes:

```
SEGMENT
```

This example confirms the importance of distinguishing strict inequality from equality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only four triples are checked |
| Space | O(1) | Uses a few variables regardless of input size |

The program performs a constant amount of work because the input size is fixed at four numbers. The running time and memory usage are effectively instantaneous compared to the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from itertools import combinations

def solve():
    input = sys.stdin.readline

    sticks = list(map(int, input().split()))

    segment = False

    for triple in combinations(sticks, 3):
        a, b, c = sorted(triple)

        if a + b > c:
            print("TRIANGLE")
            return

        if a + b == c:
            segment = True

    if segment:
        print("SEGMENT")
    else:
        print("IMPOSSIBLE")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("4 2 1 3\n") == "TRIANGLE", "sample 1"

# custom cases
assert run("1 2 3 10\n") == "SEGMENT", "degenerate triangle exists"
assert run("1 1 3 5\n") == "IMPOSSIBLE", "no valid combination"
assert run("5 5 5 5\n") == "TRIANGLE", "all equal sticks"
assert run("100 1 1 2\n") == "SEGMENT", "boundary equality case"
assert run("2 3 4 9\n") == "TRIANGLE", "one valid triple among failures"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2 3 10` | `SEGMENT` | Equality must not count as a triangle |
| `1 1 3 5` | `IMPOSSIBLE` | No triple satisfies any condition |
| `5 5 5 5` | `TRIANGLE` | Proper triangle with equal sides |
| `100 1 1 2` | `SEGMENT` | Large imbalance with one degenerate case |
| `2 3 4 9` | `TRIANGLE` | Later triple may still succeed |

## Edge Cases

Consider the input:

```
1 2 3 10
```

The algorithm checks `(1,2,3)` first. After sorting, we get `1 2 3`, and since `1 + 2 = 3`, the `segment` flag becomes `True`.

The remaining triples all fail the inequality strictly. Since no proper triangle is found, the final output is:

```
SEGMENT
```

This case confirms that equality must be handled separately from a real triangle.

Now consider:

```
4 2 1 3
```

The triple `(1,2,3)` forms only a segment, but later the algorithm checks `(2,3,4)`. Since `2 + 3 > 4`, it immediately prints:

```
TRIANGLE
```

This demonstrates why we cannot stop after seeing a degenerate triangle. A later combination may still form a proper one.

Finally, consider:

```
1 1 3 5
```

Every triple fails the condition:

$$a + b \ge c$$

The algorithm never sets the `segment` flag and never finds a proper triangle. The final answer is:

```
IMPOSSIBLE
```

This verifies that the algorithm correctly rejects configurations where even a straight-line arrangement cannot be formed.
