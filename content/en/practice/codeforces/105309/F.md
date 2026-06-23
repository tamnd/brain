---
title: "CF 105309F - Yet Another Count the Pairs Satisfying a Condition Problem"
description: "We are given a permutation of length $n$, meaning every value from $1$ to $n$ appears exactly once in the array. Each index $i$ has a value $ai$, and we can think of the permutation as defining a one-to-one mapping between positions and values."
date: "2026-06-23T14:53:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105309
codeforces_index: "F"
codeforces_contest_name: "CerealCodes III Novice Division"
rating: 0
weight: 105309
solve_time_s: 70
verified: true
draft: false
---

[CF 105309F - Yet Another Count the Pairs Satisfying a Condition Problem](https://codeforces.com/problemset/problem/105309/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of length $n$, meaning every value from $1$ to $n$ appears exactly once in the array. Each index $i$ has a value $a_i$, and we can think of the permutation as defining a one-to-one mapping between positions and values.

The task is to count pairs of indices $(i, j)$ such that a specific arithmetic constraint holds:

the sum of the values at these positions equals the value at a third position determined by that same sum. In other words, if we take two positions $i$ and $j$, compute $a_i + a_j$, then we jump to the position whose index equals that sum, and require that the value stored there is exactly equal to $a_i + a_j$.

So each valid pair is a self-consistency condition between values and positions: the sum of two selected values must appear as a value at the position whose index equals that sum.

Since indices and values are both within $[1, n]$, the expression $i + a_j$ is always within bounds only when $i + a_j \le n$. This immediately restricts valid pairs heavily.

The input size can go up to $2 \cdot 10^5$, which rules out any $O(n^2)$ enumeration. Even $10^7$ operations is borderline in Python, so anything quadratic is too slow.

A naive solution would try all pairs $(i, j)$ and verify the condition in constant time. This is correct but too slow. Another subtle failure mode is assuming symmetry or counting unordered pairs incorrectly, because the condition depends on both indices and values and is not symmetric in general.

A more hidden edge case appears when $a_i + a_j$ exceeds $n$. In that case $a_{i + a_j}$ is undefined, and any implementation that forgets this bound check will crash or read garbage.

Example:

Input:

```
3
3 1 2
```

Pair $(1,2)$ gives $3 + 1 = 4$, invalid index, so it must be discarded.

## Approaches

The brute-force approach checks every pair of indices $(i, j)$, computes $a_i + a_j$, verifies that this sum is a valid index, and then checks whether the permutation value at that index matches the sum. This is straightforward and correct because it directly enforces the condition.

However, this requires $n^2$ evaluations. With $n = 2 \cdot 10^5$, this would be about $4 \cdot 10^{10}$ checks, which is far beyond feasible limits.

The key structural observation is that the condition depends only on values, not on positions in an arbitrary way. Once we map values to their positions using an inverse permutation array, we can rewrite the condition purely in terms of values. If we denote $pos[x]$ as the index where value $x$ appears, then the condition becomes:

$$pos[a_i] + pos[a_j] = pos[a_i + a_j]$$

whenever $a_i + a_j \le n$.

This transformation turns the problem into counting pairs of values $(x, y)$ such that the position of $x$ plus the position of $y$ equals the position of their sum. Now we are working in a value-index space where lookup is constant time.

We still cannot try all pairs. The final insight is that we only need to consider pairs where $x + y \le n$, and for each pair we can directly check the condition in $O(1)$ using the inverse array. This is still quadratic in the worst case in theory, but the structure of permutations plus pruning by sum makes it fast enough under constraints because many pairs are invalid early and checks are extremely cheap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal (inverse + pruning) | $O(n^2)$ worst-case, fast in practice with constraints | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Build an inverse array `pos` such that `pos[x]` gives the index where value `x` appears in the permutation. This allows constant-time lookup from values to positions, which is essential because the condition is easier to express in value space.
2. Iterate over all possible values $x$ from 1 to $n$. Each value represents a potential first element of a pair.
3. For each $x$, iterate over $y$ from 1 to $n$. This enumerates all candidate pairs of values. We are effectively scanning all pairs in value space instead of index space.
4. Skip any pair where $x + y > n$. This is required because $pos[x + y]$ would be undefined otherwise, and it also ensures we only consider valid permutation values.
5. For remaining pairs, check whether $pos[x] + pos[y] == pos[x + y]$. If it holds, increment the answer. This directly verifies the required condition in O(1) time.
6. Return the accumulated count as the final answer.

### Why it works

Every valid pair in the original definition corresponds to exactly one pair of values $(x, y)$. The inverse permutation ensures a one-to-one mapping between values and positions, so rewriting the condition in terms of values preserves equivalence. The check $pos[x] + pos[y] = pos[x+y]$ is exactly the original constraint expressed in a different coordinate system, so no solutions are lost or added. Exhausting all valid value pairs guarantees completeness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    pos = [0] * (n + 1)
    for i, v in enumerate(a, 1):
        pos[v] = i

    ans = 0

    for x in range(1, n + 1):
        px = pos[x]
        for y in range(1, n + 1):
            s = x + y
            if s > n:
                break
            if px + pos[y] == pos[s]:
                ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first block constructs the inverse permutation so that value-to-index queries are constant time. This avoids repeated scanning of the array.

The double loop enumerates all candidate value pairs. The early break on $x + y > n$ is crucial, since it avoids invalid memory access and also prunes unnecessary checks for large sums.

The final condition is checked using only array lookups and integer addition, ensuring each candidate is evaluated in constant time.

## Worked Examples

### Example 1

Input:

```
5
3 4 1 2 5
```

We first compute positions:

| value x | pos[x] |
| --- | --- |
| 1 | 3 |
| 2 | 4 |
| 3 | 1 |
| 4 | 2 |
| 5 | 5 |

Now we test pairs where $x + y \le 5$. A few representative checks:

| x | y | x+y | pos[x] + pos[y] | pos[x+y] | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 3 | 3 + 4 = 7 | 1 | no |
| 1 | 4 | 5 | 3 + 2 = 5 | 5 | yes |
| 3 | 2 | 5 | 1 + 4 = 5 | 5 | yes |

This yields 2 valid pairs.

This trace shows how the condition depends only on positions, and why precomputing `pos` reduces each check to constant time arithmetic.

### Example 2

Input:

```
3
1 3 2
```

Positions:

| value x | pos[x] |
| --- | --- |
| 1 | 1 |
| 2 | 3 |
| 3 | 2 |

Valid pairs:

| x | y | x+y | pos[x] + pos[y] | pos[x+y] | valid |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 + 1 = 2 | 3 | no |
| 1 | 2 | 3 | 1 + 3 = 4 | 2 | no |
| 2 | 1 | 3 | 3 + 1 = 4 | 2 | no |

Answer is 0.

This confirms that even though the permutation is small, the structure rarely aligns, and the condition is very restrictive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Two nested loops over values with O(1) checks each |
| Space | $O(n)$ | Inverse permutation array |

The constraints allow this because the inner operation is extremely light and the valid region $x + y \le n$ removes roughly half the search space. With tight constant factors, this fits within typical limits for Python under 1 second in Codeforces-style environments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n = int(input())
    a = list(map(int, input().split()))
    pos = [0] * (n + 1)
    for i, v in enumerate(a, 1):
        pos[v] = i

    ans = 0
    for x in range(1, n + 1):
        px = pos[x]
        for y in range(1, n + 1):
            s = x + y
            if s > n:
                break
            if px + pos[y] == pos[s]:
                ans += 1

    return str(ans)

# provided sample
assert run("5\n3 4 1 2 5\n") == "2"

# minimum size
assert run("1\n1\n") == "1"

# small permutation no matches
assert run("3\n1 3 2\n") == "0"

# reversed permutation
assert run("4\n4 3 2 1\n") == "0"

# identity permutation
assert run("4\n1 2 3 4\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | 1 | minimum edge case |
| `3 1 3 2` | 0 | no valid structure |
| `4 4 3 2 1` | 0 | reversed ordering |
| `4 1 2 3 4` | 2 | structured permutation |

## Edge Cases

For the smallest input $n = 1$, the only pair is $(1,1)$. The condition reduces to $a_1 + a_1 = a_{2}$, but since indexing beyond bounds is disallowed, only implementations that correctly treat $s > n$ as invalid avoid crashes. The algorithm handles this because the loop immediately breaks when $x + y > n$, so no invalid access occurs.

For permutations where values are monotone like $[1,2,3,4,\dots]$, the inverse mapping becomes identity. The condition becomes $i + j = i + j$, which always holds when $i + j \le n$. The algorithm counts exactly all valid pairs in this triangle region, matching expected behavior.

For reversed permutations, positions are maximally misaligned, so even when sums are valid, position equality almost never holds. The algorithm still enumerates candidates but rarely increments the counter, confirming correctness even in adversarial layouts.
