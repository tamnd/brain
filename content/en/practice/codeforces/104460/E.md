---
title: "CF 104460E - Turn It Off"
description: "We are given a binary array representing a row of lights, where each position is either on or off. We are allowed to perform an operation that chooses a starting index and flips off a contiguous segment of fixed length $L$."
date: "2026-06-30T13:29:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104460
codeforces_index: "E"
codeforces_contest_name: "The 2019 ICPC China Shaanxi Provincial Programming Contest"
rating: 0
weight: 104460
solve_time_s: 47
verified: true
draft: false
---

[CF 104460E - Turn It Off](https://codeforces.com/problemset/problem/104460/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary array representing a row of lights, where each position is either on or off. We are allowed to perform an operation that chooses a starting index and flips off a contiguous segment of fixed length $L$. Every operation always uses the same $L$, and we may apply at most $k$ such operations. The goal is to determine the smallest possible segment length $L$ such that all initially on lights can be turned off within the allowed number of operations.

The key aspect is that each operation is not adaptive in length, only in position. Once $L$ is fixed, the only freedom is where to place the window, and we want to know whether all ones in the string can be covered by at most $k$ intervals of that length.

The constraints are large enough that any quadratic simulation over all choices of $L$ and all placements is infeasible. Since $n$ can reach $2 \times 10^5$ per test case and the total sum reaches $2 \times 10^6$, we must target roughly linear or near-linear per test case. This rules out any approach that tries to simulate operations per candidate $L$ in a naive way.

A subtle point is that overlaps do not matter except for coverage. We never need to model the exact on-off state during operations; only whether all positions containing ‘1’ are covered by at most $k$ intervals.

A common failure case appears when implementations try greedy placement without correctly tracking how far the previous operation already covers.

For example, consider:

```
n = 5, k = 1
s = 10001
```

If $L = 3$, a naive greedy might place the interval starting at 1 to cover the first 1, but it will miss the last one. The correct placement would fail regardless, because one interval cannot cover two separated regions beyond length 3. Any approach that does not reason about coverage limits precisely will mis-evaluate feasibility.

## Approaches

The brute-force idea is straightforward. For a fixed $L$, we scan the string from left to right. Whenever we encounter a ‘1’ not yet covered, we place an operation starting at that position and cover the next $L$ cells. We repeat until either all ones are covered or we exceed $k$ operations. This is correct because placing an interval as early as possible never reduces future flexibility.

The issue is that checking one $L$ takes $O(n)$, and trying all $L$ values from 1 to $n$ leads to $O(n^2)$, which is too large for $n = 2 \times 10^5$.

The crucial observation is that feasibility is monotonic in $L$. If a certain $L$ is sufficient to cover all ones in at most $k$ operations, then any larger $L$ is also sufficient because each operation covers more cells and never increases the required number of operations. This allows us to binary search the answer.

Now the problem reduces to checking feasibility for a fixed $L$, which can be done greedily in linear time. We scan the string, and whenever we find an uncovered ‘1’, we place an interval starting at that position and skip forward by $L$. The number of intervals used is compared with $k$.

This combination of greedy feasibility check and binary search yields an efficient solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over L with greedy check | $O(n^2)$ | $O(1)$ | Too slow |
| Binary search + greedy check | $O(n \log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We solve each test case independently using binary search on $L$.

1. Define a function `can(L)` that checks whether all ‘1’ positions can be covered using at most $k$ segments of length $L$. We simulate from left to right, tracking how far the last placed segment reaches.
2. Inside `can(L)`, we maintain a pointer `i` scanning the string and a counter `cnt` for how many segments we have used. When we encounter a position `i` with a ‘1’ that is not yet covered, we increment `cnt` and set the coverage to extend from `i` to `i + L - 1`.
3. We then skip all positions covered by this segment by moving `i` forward. This ensures each segment is placed greedily at the earliest possible uncovered ‘1’, minimizing wasted coverage.
4. If at any point `cnt > k`, we stop early and return false because we have exceeded the allowed number of operations.
5. Perform binary search on $L$ from 1 to $n$. For each midpoint, call `can(mid)`. If it is feasible, we try smaller values; otherwise, we increase $L$.
6. Output the smallest $L$ for which `can(L)` returns true.

The greedy placement is optimal for fixed $L$ because placing a segment later than the first uncovered ‘1’ cannot reduce the number of segments needed, and may only leave additional uncovered ones behind.

### Why it works

The correctness rests on a coverage invariant. After each placed segment, all positions up to its right endpoint are fully resolved, meaning no future decision depends on them. Every uncovered ‘1’ forces at least one segment that must start at or before that position. The greedy strategy always satisfies this requirement at the earliest possible point, ensuring no segment is wasted on already-covered regions. Therefore, the number of segments produced is minimal for that $L$, making the feasibility check exact.

Because feasibility is monotone in $L$, binary search over $L$ is valid, and the combination yields the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(s, n, k, L):
    cnt = 0
    i = 0
    while i < n:
        if s[i] == '1':
            cnt += 1
            if cnt > k:
                return False
            i += L
        else:
            i += 1
    return True

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    lo, hi = 1, n
    ans = n

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(s, n, k, mid):
            ans = mid
            hi = mid - 1
        else:
            lo = mid + 1

    print(ans)

if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        solve()
```

The function `can` is a direct implementation of the greedy coverage process. The key detail is that when we hit a ‘1’, we immediately commit to an operation and jump forward by $L$, because any optimal solution must cover that position with some interval, and delaying only risks extra operations later.

Binary search is implemented in the standard way, narrowing the feasible region until the smallest valid $L$ is found.

## Worked Examples

Consider the input:

```
n = 5, k = 2
s = 10101
```

We evaluate feasibility for $L = 2$.

| i | s[i] | action | cnt | next i |
| --- | --- | --- | --- | --- |
| 0 | 1 | place interval [0,1] | 1 | 2 |
| 2 | 1 | place interval [2,3] | 2 | 4 |
| 4 | 1 | place interval [4,5] | 3 | stop |

We used 3 operations, which exceeds $k=2$, so $L=2$ is infeasible.

Now consider $L = 3$.

| i | s[i] | action | cnt | next i |
| --- | --- | --- | --- | --- |
| 0 | 1 | place [0,2] | 1 | 3 |
| 3 | 0 | skip | 1 | 4 |
| 4 | 1 | place [4,6] | 2 | 7 |

Here we use exactly 2 operations, so $L=3$ is feasible.

This shows how increasing $L$ reduces the number of required segments and demonstrates monotonicity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each feasibility check is linear, and binary search runs over $O(\log n)$ values |
| Space | $O(1)$ | Only a few counters and pointers are used |

The total input size across test cases is $2 \times 10^6$, and the logarithmic factor remains small, making the solution efficient enough for the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def can(s, n, k, L):
        cnt = 0
        i = 0
        while i < n:
            if s[i] == '1':
                cnt += 1
                if cnt > k:
                    return False
                i += L
            else:
                i += 1
        return True

    def solve():
        n, k = map(int, input().split())
        s = input().strip()

        lo, hi = 1, n
        ans = n

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(s, n, k, mid):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1

        return ans

    t = int(input())
    out = []
    for _ in range(t):
        out.append(str(solve()))
    return "\n".join(out)

# minimum size
assert run("1\n1 1\n1\n") == "1"

# already all zeros except one far
assert run("1\n5 1\n00001\n") == "1"

# all ones
assert run("1\n5 1\n11111\n") == "5"

# multiple segments needed
assert run("1\n6 2\n101010\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 1 | minimal segment behavior |
| sparse far 1 | 1 | jump correctness |
| all ones, k=1 | n | worst-case single interval |
| alternating pattern | 3 | multiple greedy placements |

## Edge Cases

One edge case is when all ‘1’s are clustered. For example:

```
n = 6, k = 1
s = 011110
```

For $L = 4$, the greedy check places one interval covering all ones in a single segment, so it returns true. If $L$ were smaller, multiple segments would be required, exceeding $k$.

Another edge case is when ones are isolated:

```
n = 5, k = 2
s = 10101
```

As shown in the walkthrough, small $L$ forces one operation per ‘1’, quickly exceeding $k$. The greedy check correctly counts each forced segment.

A final edge case is when $k$ is large enough that any $L=1$ works. For example:

```
n = 10, k = 10
s = 1010101010
```

Each ‘1’ can be handled individually, so the answer becomes 1. The algorithm handles this naturally because `can(1)` immediately returns true.
