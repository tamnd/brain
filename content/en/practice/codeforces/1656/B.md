---
title: "CF 1656B - Subtract Operation"
description: "We start with an array of integers. In one operation, we pick an element, remove it from the array, and subtract its value from every remaining element. After exactly $n-1$ operations, only one number remains."
date: "2026-06-10T03:32:17+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1656
codeforces_index: "B"
codeforces_contest_name: "CodeTON Round 1 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1100
weight: 1656
solve_time_s: 109
verified: true
draft: false
---

[CF 1656B - Subtract Operation](https://codeforces.com/problemset/problem/1656/B)

**Rating:** 1100  
**Tags:** data structures, greedy, math, two pointers  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an array of integers. In one operation, we pick an element, remove it from the array, and subtract its value from every remaining element.

After exactly $n-1$ operations, only one number remains. The question is whether there exists some order of removals that leaves the final remaining value equal to a given target $k$.

At first glance this looks like a simulation or state-search problem because every operation changes all remaining values. The number of possible operation sequences is enormous, roughly $n!$, so directly exploring them is impossible.

The constraints give a strong hint that the intended solution is much simpler. The total number of array elements across all test cases is at most $2 \cdot 10^5$. This allows algorithms such as $O(n)$ or $O(n \log n)$, but anything quadratic in the total input size would be too expensive.

The tricky part is recognizing what information from the array actually matters. A naive reader may focus on the repeated transformations of the array, but the final value turns out to depend only on differences between original elements.

One non-obvious edge case is when the target already appears in the array.

Input:

```
1
2 17
17 0
```

Output:

```
YES
```

With only two elements, removing 0 leaves 17 unchanged. A solution that searches only for a difference equal to $k$ among distinct transformed states might miss this simple case.

Another subtle case is when duplicate values exist.

Input:

```
1
4 5
4 2 2 7
```

Output:

```
YES
```

The answer comes from the pair $(2,7)$, whose difference is 5. The duplicates are irrelevant. A careless implementation that removes duplicates too early and then reasons incorrectly about the operations could produce the wrong result.

Negative numbers are also possible.

Input:

```
1
3 7
-5 2 9
```

Output:

```
YES
```

Since $2 - (-5) = 7$, the answer is positive even though some values are negative. Any solution that assumes all numbers are non-negative would fail.

## Approaches

A brute-force approach would try every possible sequence of removals. For each step we choose one of the remaining elements, update all others, and continue recursively.

This approach is correct because it explicitly explores every legal sequence. The problem is the number of possibilities. With $n$ elements there are $n!$ possible removal orders. Even for $n=15$, this is already far beyond practical limits.

To find a better solution, let us examine what happens to the final remaining value.

Suppose two elements $a$ and $b$ remain at some point. If we remove $a$, the final value becomes $b-a$. If we remove $b$, the final value becomes $a-b$.

The key observation is that every sequence of operations ultimately produces the difference between two original array elements. In fact, if we want the final value to be $k$, there must exist two original elements whose difference is exactly $k$.

Why? Consider the last operation. Just before it, two numbers remain. Those two numbers themselves can be traced back to original elements through previous subtractions. The editorial observation for this problem is that achieving $k$ is equivalent to finding two original numbers $x$ and $y$ such that $y-x=k$.

This completely removes the need to simulate operations. The problem becomes:

Does the array contain a pair of values whose difference is exactly $k$?

Once reformulated this way, a hash set solves the problem immediately. For every value $x$, check whether $x+k$ also exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the array and insert all values into a hash set.
2. For every element $x$ in the array, check whether $x+k$ exists in the set.
3. If such a value exists, output `YES`.

The pair $(x, x+k)$ has difference exactly $k$, which is precisely the condition required.
4. If no element satisfies the condition after scanning the entire array, output `NO`.

### Why it works

The crucial property is that the operation process can produce $k$ if and only if there exist two original array elements whose difference equals $k$.

The forward direction is that any successful sequence ultimately corresponds to a difference between two original values. The reverse direction is that if two elements $x$ and $x+k$ exist, we can arrange the operations so that the final value becomes $(x+k)-x=k$.

The algorithm checks exactly this condition. If such a pair exists, it returns `YES`; otherwise it returns `NO`. Since the condition is both necessary and sufficient, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        s = set(a)

        found = False
        for x in a:
            if x + k in s:
                found = True
                break

        ans.append("YES" if found else "NO")

    sys.stdout.write("\n".join(ans))

solve()
```

The implementation follows the algorithm directly.

A hash set stores all array values, giving expected $O(1)$ membership checks. For each element $x$, we test whether $x+k$ is present. The first successful match is enough to answer `YES`.

Using a set is important. A nested loop would require $O(n^2)$ comparisons, which is unnecessary. The total input size reaches $2 \cdot 10^5$, so linear processing is preferred.

There are no overflow concerns in Python because integers have arbitrary precision. The values remain well within normal integer ranges anyway.

The condition must be checked as `x + k in s`, not `abs(x - y) == k`. The problem requires a difference of exactly $k$, and the editorial characterization is based on the ordered pair $y - x = k$.

## Worked Examples

### Example 1

Input:

```
4 5
4 2 2 7
```

| Step | x | x + k | Present in set? |
| --- | --- | --- | --- |
| 1 | 4 | 9 | No |
| 2 | 2 | 7 | Yes |

The algorithm stops immediately and prints `YES`.

This demonstrates the central observation. The pair $(2,7)$ differs by 5, so the target can be achieved regardless of the detailed sequence of operations.

### Example 2

Input:

```
5 4
1 9 1 3 4
```

| Step | x | x + k | Present in set? |
| --- | --- | --- | --- |
| 1 | 1 | 5 | No |
| 2 | 9 | 13 | No |
| 3 | 1 | 5 | No |
| 4 | 3 | 7 | No |
| 5 | 4 | 8 | No |

No valid pair exists, so the answer is `NO`.

This example shows that duplicates do not automatically help. What matters is the existence of a pair whose difference is exactly $k$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | One pass to build the set and one pass to check pairs |
| Space | $O(n)$ | Storage for the hash set |

Since the sum of all $n$ values across test cases is at most $2 \cdot 10^5$, the total running time is linear in the input size. This comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    def solve():
        input = sys.stdin.readline
        t = int(input())
        ans = []

        for _ in range(t):
            n, k = map(int, input().split())
            a = list(map(int, input().split()))

            s = set(a)
            ok = any(x + k in s for x in a)

            ans.append("YES" if ok else "NO")

        return "\n".join(ans)

    return solve()

# provided sample
assert run(
"""4
4 5
4 2 2 7
5 4
1 9 1 3 4
2 17
17 0
2 17
18 18
"""
) == """YES
NO
YES
NO"""

# minimum size, positive answer
assert run(
"""1
2 1
5 6
"""
) == "YES"

# minimum size, negative answer
assert run(
"""1
2 1
5 7
"""
) == "NO"

# all equal values
assert run(
"""1
5 3
8 8 8 8 8
"""
) == "NO"

# negative values present
assert run(
"""1
3 7
-5 2 9
"""
) == "YES"

# large boundary-style pattern
n = 200000
arr = " ".join(map(str, range(n)))
inp = f"1\n{n} 199999\n{arr}\n"
assert run(inp) == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 5 6` | YES | Smallest valid positive case |
| `2 1 / 5 7` | NO | Smallest valid negative case |
| All values equal | NO | Duplicate handling |
| `-5 2 9`, `k=7` | YES | Negative numbers |
| Large consecutive array | YES | Performance at maximum size |

## Edge Cases

Consider:

```
1
2 17
17 0
```

The set is `{17, 0}`. When `x = 0`, the algorithm checks `0 + 17 = 17`, which exists. The answer becomes `YES`. This handles the smallest possible array size correctly.

Consider:

```
1
4 5
4 2 2 7
```

The set is `{2, 4, 7}`. When `x = 2`, the algorithm finds `7` in the set and returns `YES`. Duplicate values do not affect correctness because the condition depends only on existence.

Consider:

```
1
3 7
-5 2 9
```

The set is `{-5, 2, 9}`. For `x = -5`, the algorithm checks `-5 + 7 = 2`, which exists. The answer is `YES`. Negative values require no special handling because hash-set lookups work identically for negative and positive integers.

Consider:

```
1
5 3
8 8 8 8 8
```

The set contains only `{8}`. Every check asks whether `11` exists. It does not, so the algorithm outputs `NO`. This confirms that duplicates alone cannot create a difference of 3.
