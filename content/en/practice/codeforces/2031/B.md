---
title: "CF 2031B - Penchick and Satay Sticks"
description: "We have a permutation of the numbers $1$ through $n$. The target is the sorted permutation $[1,2,dots,n]$. The only allowed operation swaps two neighboring positions when the values differ by exactly $1$. For example, $3$ and $4$ may be swapped, but $3$ and $5$ may not."
date: "2026-06-08T11:51:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2031
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 987 (Div. 2)"
rating: 900
weight: 2031
solve_time_s: 120
verified: true
draft: false
---

[CF 2031B - Penchick and Satay Sticks](https://codeforces.com/problemset/problem/2031/B)

**Rating:** 900  
**Tags:** brute force, greedy, sortings  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation of the numbers $1$ through $n$. The target is the sorted permutation $[1,2,\dots,n]$.

The only allowed operation swaps two neighboring positions when the values differ by exactly $1$. For example, $3$ and $4$ may be swapped, but $3$ and $5$ may not.

The task is to determine whether the permutation can be transformed into sorted order using any number of such swaps.

The constraints are large. Across all test cases, the total length is at most $2 \cdot 10^5$. Any algorithm that simulates many swaps or repeatedly scans the array would become too slow. Quadratic approaches are ruled out because $n^2$ operations would reach roughly $4 \cdot 10^{10}$ in the worst case. We need a linear or near-linear solution.

A subtle edge case is a reversed adjacent pair. Consider:

```
2 1 3 4
```

The values $2$ and $1$ differ by exactly $1$, so they can be swapped directly. The answer is `YES`.

Another important case is:

```
3 1 2
```

The value $3$ must move right, but it can never swap with either $1$ or $2$, because the differences are $2$ and $1$ only after $1$ and $2$ become adjacent. The correct answer is `NO`. A naive approach that only checks inversion count would miss this.

A particularly revealing example is:

```
4 2 3 1
```

The pair $(2,3)$ can swap forever, but the value $4$ can never cross either $2$ or $1$. The permutation cannot be sorted, so the answer is `NO`.

## Approaches

A brute-force approach would treat each valid swap as an edge in a state graph and search whether the sorted permutation is reachable. This is correct because every legal sequence of operations corresponds to a path in that graph.

Unfortunately, there are $n!$ permutations. Even for moderate $n$, exploring states becomes impossible.

The key observation is that only consecutive values can ever swap.

Consider two values whose difference exceeds $1$, such as $2$ and $5$. They can never be swapped directly. Since every allowed operation exchanges only consecutive numbers, the relative order of $2$ and $5$ can never change.

This means that for every pair $x < y-1$, their order is invariant throughout the entire process.

The only pairs whose relative order may change are consecutive values:

$$(1,2),\ (2,3),\ (3,4),\ \dots,\ (n-1,n).$$

Suppose a value is more than one position away from where it belongs. Fixing that would require changing its order relative to some non-consecutive value, which is impossible.

This immediately leads to a simple characterization. Every element must already be at its own position or adjacent to it. In permutation notation,

$$|p_i - i| \le 1$$

for every position $i$.

If this condition holds, the permutation consists only of disjoint adjacent inversions such as

$$[2,1,4,3,5].$$

Each inversion involves consecutive values and can be repaired independently with one legal swap.

If the condition fails anywhere, sorting is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the permutation.
2. Scan every position $i$.
3. Check whether

$$|p_i - (i+1)| \le 1.$$

The array is 0-indexed in code, so the correct position of value $i+1$ is represented by $i+1$.

1. If any position violates this condition, output `NO`.

A value that is two or more positions away from its destination would need to cross a non-consecutive value, which can never happen.

1. If all positions satisfy the condition, output `YES`.

The permutation is then composed entirely of fixed points and adjacent swaps of consecutive values, all of which can be corrected legally.

### Why it works

The relative order of any two values whose difference exceeds $1$ never changes, because they can never participate in a legal swap.

Suppose some element $x$ is located at least two positions away from its final position. To reach its destination, $x$ must pass some value $y$ with $|x-y|>1$. That would require changing their relative order, which is impossible.

Hence every sortable permutation must satisfy $|p_i-i|\le1$ in 1-indexed notation.

Conversely, if every element is at most one position away from its correct position, the permutation is a collection of disjoint adjacent inversions $(i+1,i)$. Each such inversion consists of consecutive values and can be fixed with a single legal swap. Performing these swaps sorts the permutation.

Therefore the condition is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        ok = True
        for i, x in enumerate(p, start=1):
            if abs(x - i) > 1:
                ok = False
                break

        ans.append("YES" if ok else "NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation directly checks the characterization proved above.

The loop uses `enumerate(..., start=1)` so that the index matches the permutation's natural 1-based positions. This avoids repeated `+1` adjustments and eliminates a common off-by-one mistake.

The scan stops immediately after finding a violation. No further information is needed once one element is more than one position away from its target.

No simulation is performed. The proof shows that the displacement condition completely determines the answer.

## Worked Examples

### Example 1

Input:

```
2 1 3 4
```

| Position | Value | $|p_i-i|$ |

|---|---:|---:|

| 1 | 2 | 1 |

| 2 | 1 | 1 |

| 3 | 3 | 0 |

| 4 | 4 | 0 |

All values satisfy the condition.

Output:

```
YES
```

The inversion $(2,1)$ involves consecutive values, so one legal swap sorts the array.

### Example 2

Input:

```
4 2 3 1
```

| Position | Value | $|p_i-i|$ |

|---|---:|---:|

| 1 | 4 | 3 |

| 2 | 2 | 0 |

| 3 | 3 | 0 |

| 4 | 1 | 3 |

The first position already violates the condition.

Output:

```
NO
```

The value $4$ is three positions away from where it belongs. Fixing that would require crossing values whose difference from $4$ exceeds $1$, which is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One pass through the permutation |
| Space | $O(1)$ | Only a few variables besides the input array |

The sum of all $n$ values is at most $2 \cdot 10^5$, so a linear scan across each test case easily fits within the time limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))

        ok = True
        for i, x in enumerate(p, start=1):
            if abs(x - i) > 1:
                ok = False
                break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided sample
assert run("""2
4
2 1 3 4
4
4 2 3 1
""") == """YES
NO"""

# minimum size
assert run("""1
1
1
""") == "YES"

# single adjacent swap
assert run("""1
2
2 1
""") == "YES"

# displacement greater than one
assert run("""1
3
3 1 2
""") == "NO"

# multiple disjoint adjacent inversions
assert run("""1
6
2 1 4 3 6 5
""") == "YES"

# reversed permutation
assert run("""1
5
5 4 3 2 1
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1]` | `YES` | Minimum size |
| `[2,1]` | `YES` | Single legal swap |
| `[3,1,2]` | `NO` | Element displaced by more than one position |
| `[2,1,4,3,6,5]` | `YES` | Multiple independent adjacent inversions |
| `[5,4,3,2,1]` | `NO` | Large displacements make sorting impossible |

## Edge Cases

Consider:

```
1
2
2 1
```

The displacements are $1$ and $1$. The algorithm accepts. A single legal swap exchanges $2$ and $1$, producing the sorted permutation.

Consider:

```
1
3
3 1 2
```

The first element has displacement $2$. The algorithm immediately rejects. The value $3$ would need to move past $1$, and these values differ by $2$, so their relative order can never change.

Consider:

```
1
6
2 1 4 3 6 5
```

Every displacement equals either $0$ or $1$. The algorithm accepts. Each inverted pair consists of consecutive values and can be fixed independently.

Consider:

```
1
5
5 4 3 2 1
```

The first element has displacement $4$. The algorithm rejects at once. Sorting would require changing the relative order of many non-consecutive value pairs, which no legal operation can accomplish.
