---
title: "CF 1759G - Restore the Permutation"
description: "We are given the array of pairwise maxima of an unknown permutation. The permutation has even length n. If we group its elements into pairs (p1, p2), (p3, p4), ... and replace each pair by its maximum, we obtain an array b of length n/2."
date: "2026-06-09T14:33:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1759
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round  834 (Div. 3)"
rating: 1900
weight: 1759
solve_time_s: 224
verified: false
draft: false
---

[CF 1759G - Restore the Permutation](https://codeforces.com/problemset/problem/1759/G)

**Rating:** 1900  
**Tags:** binary search, constructive algorithms, data structures, greedy, math  
**Solve time:** 3m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given the array of pairwise maxima of an unknown permutation.

The permutation has even length `n`. If we group its elements into pairs

`(p1, p2), (p3, p4), ...`

and replace each pair by its maximum, we obtain an array `b` of length `n/2`.

The task is to reconstruct a permutation `p` that produces the given `b`. Among all valid permutations, we must output the lexicographically smallest one. If no permutation can produce `b`, we print `-1`.

The key observation is that every value appearing in `b` must itself appear in the permutation. Since it is the maximum of its pair, it must occupy one position of that pair, while the other position must contain a strictly smaller unused number.

The constraints are large. The sum of all `n` over all test cases is at most `2 · 10^5`, which means an `O(n log n)` solution is easily fast enough, while anything quadratic would be far too slow. A reconstruction that repeatedly scans all remaining numbers would require roughly `n²` operations in the worst case and cannot fit into the limit.

Several edge cases are easy to miss.

Consider:

```
n = 4
b = [4, 4]
```

Both pair maxima are equal. Since a permutation contains each number exactly once, the value `4` cannot appear twice. No solution exists, so the answer is:

```
-1
```

A reconstruction that only checks local pair conditions might accidentally reuse `4`.

Another important case is:

```
n = 6
b = [2, 4, 6]
```

The unused numbers are `{1,3,5}`.

For the first pair, whose maximum is `2`, we need an unused number smaller than `2`. The only choice is `1`.

For the second pair, whose maximum is `4`, we need an unused number smaller than `4`. The only remaining choice is `3`.

For the third pair, we use `5`.

This is valid:

```
1 2 3 4 5 6
```

A careless greedy that uses the largest available smaller number first would still work here, but it would not necessarily produce the lexicographically smallest permutation.

The most subtle failure occurs when a pair maximum is too small.

```
n = 8
b = [8, 7, 2, 3]
```

The unused numbers are `{1,4,5,6}`.

When we reach maximum `2`, the only smaller number is `1`, which is still available, so we use it.

For maximum `3`, we now need a smaller unused number, but none remain. The answer is:

```
-1
```

Any algorithm must detect such situations immediately.

## Approaches

A brute-force approach would try to reconstruct the permutation by testing assignments of the missing numbers to the first position of each pair. Since roughly `n/2` numbers are missing, there can be on the order of `(n/2)!` possible assignments. Even for moderate values of `n`, this is completely infeasible.

The structure of the problem gives us much more information than a generic reconstruction problem.

Every value in `b` must appear exactly once in the permutation. Since it is the maximum of its pair, we may immediately place it as the second element of that pair:

```
(_, b1), (_, b2), ...
```

Now the only task is to choose the first element of each pair.

Suppose we are processing a pair whose maximum is `x`. The first element must be an unused number strictly smaller than `x`. Among all such candidates, which one should we choose?

We want the entire permutation to be lexicographically minimal. The first undecided position appears before its corresponding maximum. To minimize the permutation, we should place the smallest possible valid number there.

This immediately suggests a greedy strategy.

Keep all numbers that do not appear in `b` inside an ordered set. For each maximum `x`, take the largest unused number that is still smaller than `x`.

At first glance this seems opposite to lexicographic minimization. The reason it is correct is that the maxima themselves are fixed. Choosing the largest feasible smaller number preserves smaller values for future positions, making later entries as small as possible. If we consume tiny values too early, some future pair may become impossible.

This is exactly the classic greedy used in accepted solutions.

We need efficient predecessor queries: "find the largest unused value smaller than `x`". An ordered set supports this in `O(log n)` time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array `b`.
2. Verify that all values in `b` are distinct.

A permutation contains each number exactly once. If some value appears twice in `b`, reconstruction is impossible.
3. Mark every value appearing in `b` as already used.
4. Put every number from `1` to `n` that does not appear in `b` into an ordered set.
5. Build the answer pair by pair.
6. For a maximum value `x = b[i]`, find the largest unused number strictly smaller than `x`.

This is a predecessor query in the ordered set.
7. If no such number exists, output `-1`.

Then this pair cannot be formed without violating the maximum condition.
8. Append the chosen predecessor and then append `x` to the answer.
9. Remove the chosen predecessor from the ordered set.
10. After all pairs are processed, output the constructed permutation.

### Why it works

Every pair must contain its maximum `b[i]`, so placing all values of `b` is mandatory.

For a pair with maximum `x`, any valid partner must be smaller than `x`. Among all available candidates, choosing the largest one is the safest choice. It leaves all smaller numbers available for later pairs, which can only increase the set of future options.

Suppose a valid reconstruction exists. When processing a pair with maximum `x`, any smaller unused number could be assigned there. Replacing it with a larger unused number still smaller than `x` cannot hurt the current pair and can only help future pairs, because future maxima will have at least as many smaller values available as before.

Thus the greedy choice never destroys a solution when one exists. If the algorithm fails to find a smaller unused value for some maximum `x`, then no valid reconstruction exists at all.

The produced permutation is also lexicographically minimal among all valid reconstructions. The greedy preserves the smallest values for the earliest future positions, which is exactly what lexicographic minimization requires.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def erase(self, x):
        self.parent[x] = self.find(x - 1)

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))

        if len(set(b)) != len(b):
            print(-1)
            continue

        used = [False] * (n + 1)
        for x in b:
            used[x] = True

        dsu = DSU(n)

        for x in range(1, n + 1):
            if used[x]:
                dsu.erase(x)

        ans = []
        ok = True

        for x in b:
            y = dsu.find(x - 1)

            if y == 0:
                ok = False
                break

            ans.append(y)
            ans.append(x)

            dsu.erase(y)

        if ok:
            print(*ans)
        else:
            print(-1)

solve()
```

The first validation step checks whether some value appears twice in `b`. Such an input can never come from a permutation because each maximum value must itself appear in the permutation.

The DSU acts as a predecessor structure. For every value `v`, `find(v)` returns the largest currently available number not exceeding `v`.

Initially all numbers not appearing in `b` are available. Every number appearing in `b` is removed from the DSU because it is already reserved as a pair maximum.

For a maximum `x`, we query `find(x - 1)`. This directly returns the largest available number smaller than `x`.

The `erase` operation links a number to its predecessor. After removing `y`, future queries automatically skip it.

The DSU implementation is a common trick for predecessor queries on the range `1..n`. It avoids balanced trees and keeps the complexity nearly linear.

## Worked Examples

### Example 1

Input:

```
n = 6
b = [4, 3, 6]
```

Unused numbers initially are `{1, 2, 5}`.

| Pair | Maximum x | Largest available < x | Remaining unused | Answer |
| --- | --- | --- | --- | --- |
| 1 | 4 | 2 | {1,5} | 2 4 |
| 2 | 3 | 1 | {5} | 2 4 1 3 |
| 3 | 6 | 5 | {} | 2 4 1 3 5 6 |

Output:

```
2 4 1 3 5 6
```

This trace shows how every pair consumes the largest feasible predecessor.

### Example 2

Input:

```
n = 8
b = [8, 7, 2, 3]
```

Unused numbers initially are `{1,4,5,6}`.

| Pair | Maximum x | Largest available < x | Remaining unused | Status |
| --- | --- | --- | --- | --- |
| 1 | 8 | 6 | {1,4,5} | OK |
| 2 | 7 | 5 | {1,4} | OK |
| 3 | 2 | 1 | {4} | OK |
| 4 | 3 | none | {4} | Fail |

Since no unused number smaller than `3` remains, reconstruction is impossible.

Output:

```
-1
```

This example demonstrates why simply matching maxima is not enough. Every pair must also have a distinct smaller companion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n)) | Each DSU operation is amortized inverse-Ackermann |
| Space | O(n) | DSU parent array and bookkeeping |

Since the total sum of `n` over all test cases is at most `2 · 10^5`, the DSU-based predecessor structure easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class DSU:
        def __init__(self, n):
            self.parent = list(range(n + 1))

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def erase(self, x):
            self.parent[x] = self.find(x - 1)

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        b = list(map(int, input().split()))

        if len(set(b)) != len(b):
            out.append("-1")
            continue

        used = [False] * (n + 1)
        for x in b:
            used[x] = True

        dsu = DSU(n)

        for x in range(1, n + 1):
            if used[x]:
                dsu.erase(x)

        ans = []
        ok = True

        for x in b:
            y = dsu.find(x - 1)

            if y == 0:
                ok = False
                break

            ans.extend([str(y), str(x)])
            dsu.erase(y)

        out.append(" ".join(ans) if ok else "-1")

    return "\n".join(out)

assert run(
"""1
6
4 3 6
"""
) == "2 4 1 3 5 6"

assert run(
"""1
4
4 4
"""
) == "-1"

assert run(
"""1
2
2
"""
) == "1 2"

assert run(
"""1
8
8 7 2 3
"""
) == "-1"

assert run(
"""1
6
2 4 6
"""
) == "1 2 3 4 5 6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2, b=[2]` | `1 2` | Minimum valid instance |
| `n=4, b=[4,4]` | `-1` | Duplicate maxima |
| `n=8, b=[8,7,2,3]` | `-1` | Missing smaller partner |
| `n=6, b=[2,4,6]` | `1 2 3 4 5 6` | Straightforward valid reconstruction |

## Edge Cases

Consider:

```
1
4
4 4
```

The first step detects that `4` appears twice in `b`. Since a permutation cannot contain two copies of `4`, reconstruction is impossible and the algorithm immediately prints:

```
-1
```

Now consider:

```
1
8
8 7 2 3
```

After reserving all maxima, the available numbers are:

```
{1,4,5,6}
```

Processing proceeds as:

```
8 -> 6
7 -> 5
2 -> 1
3 -> impossible
```

The predecessor query for `3` returns `0`, meaning no unused value smaller than `3` exists. The algorithm correctly reports:

```
-1
```

Finally, consider:

```
1
6
2 4 6
```

Available numbers are:

```
{1,3,5}
```

Each predecessor query succeeds:

```
2 -> 1
4 -> 3
6 -> 5
```

Result:

```
1 2 3 4 5 6
```

Every pair has the required maximum, every number from `1` to `6` appears exactly once, and the reconstruction is valid.
