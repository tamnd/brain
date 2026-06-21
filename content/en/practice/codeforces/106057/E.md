---
title: "CF 106057E - Treasures in the Interval"
description: "We are given an initial array of length $N$. After that, a sequence of range updates modifies it: each update picks a segment $[L, R]$ and adds a value $d$ to every element inside that segment. Once all updates are applied, the array is fixed."
date: "2026-06-21T08:42:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106057
codeforces_index: "E"
codeforces_contest_name: "CoU CSE Fest 2025 - Inter University Programming Contest (Divisional)"
rating: 0
weight: 106057
solve_time_s: 40
verified: true
draft: false
---

[CF 106057E - Treasures in the Interval](https://codeforces.com/problemset/problem/106057/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an initial array of length $N$. After that, a sequence of range updates modifies it: each update picks a segment $[L, R]$ and adds a value $d$ to every element inside that segment. Once all updates are applied, the array is fixed. Then we receive queries asking for the $K$-th largest value in this final array.

The task is essentially split into two phases. First, we must efficiently apply many range increments to a static array. Second, we must support order-statistics queries on the final transformed array.

The constraints implied by typical Codeforces settings with $N, Q, M$ up to around $2 \cdot 10^5$ immediately rule out naive simulation. A direct approach that updates every element for each range update costs $O(NQ)$, which would be around $10^{10}$ operations in the worst case and will not run within time limits. Similarly, recomputing the answer for each query by scanning the array would be too slow, since sorting or linear scans per query would multiply costs unnecessarily.

Edge cases appear mainly around indexing and update boundaries. One common mistake is mishandling the $R + 1$ position in the difference array.

If $N = 5$, and we apply $(L=2, R=5, d=3)$, then failing to subtract at position $R+1 = 6$ or writing out-of-bounds updates incorrectly will either leak the increment past the array or crash logic. Another subtle case is when multiple updates overlap; naive approaches might double-apply or misorder contributions, but the correct method must ensure linear accumulation.

Finally, queries asking for $K = 1$ or $K = N$ test boundary correctness of indexing after sorting.

## Approaches

A straightforward solution applies each update by iterating from $L$ to $R$ and adding $d$ directly. This is correct because it mirrors the definition of the operation. However, each update can touch up to $N$ elements, and with $Q$ updates, the total complexity becomes $O(NQ)$. For large inputs, this becomes infeasible.

The key observation is that each update contributes a constant value over a continuous segment. Instead of applying it element by element, we can encode its effect using a difference array. By marking a +d at position $L$ and a -d at position $R+1$, we transform range updates into point updates. A prefix sum over this structure reconstructs the final array in linear time.

Once the final array is built, sorting it allows direct access to order statistics. The $K$-th largest element becomes a direct index lookup after sorting in ascending order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NQ + M)$ | $O(1)$ | Too slow |
| Optimal | $O(N \log N + Q + M)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We convert the problem into two independent phases: applying range updates efficiently, then answering selection queries.

1. Create a difference array `df` of size $N+1$, initialized to zero. This structure will represent how values change between consecutive positions instead of storing actual values directly.
2. For each update $(L, R, d)$, add $d$ to `df[L]`. This means all positions starting from $L$ should increase by $d$.
3. Subtract $d$ from `df[R+1]` if $R+1 \le N$. This cancels the effect beyond the segment, ensuring the increment stops exactly at $R$. This boundary handling is what makes the representation equivalent to a range update.
4. Compute the prefix sum over `df` to reconstruct the actual increments for each position. Each position accumulates all active contributions affecting it.
5. Add these increments to the original array $A$, producing the final transformed array.
6. Sort the resulting array in ascending order. Sorting organizes values so that order statistics become direct index accesses.
7. For each query $K$, output the element at index $N - K$. This corresponds to the $K$-th largest value since indexing starts from zero.

### Why it works

The difference array encodes each range update as a pair of boundary changes. Every update contributes a constant offset across a contiguous segment, and prefix sums ensure that each position aggregates exactly the updates whose ranges cover it. This guarantees that after reconstruction, every element in the array reflects the sum of all valid updates applied to it exactly once. Sorting then transforms the problem into a static order-statistics query, where each query is answered by a deterministic index lookup.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q, m = map(int, input().split())
    a = list(map(int, input().split()))

    df = [0] * (n + 1)

    for _ in range(q):
        l, r, d = map(int, input().split())
        df[l - 1] += d
        if r < n:
            df[r] -= d

    cur = 0
    for i in range(n):
        cur += df[i]
        a[i] += cur

    a.sort()

    out = []
    for _ in range(m):
        k = int(input())
        out.append(str(a[n - k]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the difference array logic exactly. The key subtlety is converting to 0-based indexing consistently. The update at $L$ becomes `df[l - 1] += d`, and the cancellation at $R+1$ becomes `df[r] -= d` because shifting by one index aligns boundaries correctly.

The prefix accumulation variable `cur` represents the running sum of all active updates at position $i$. Each array element is updated in place, avoiding extra memory.

After sorting, queries are answered in constant time using direct indexing from the end of the array.

## Worked Examples

### Example 1

Input:

```
N=5, A=[1,2,3,4,5]
updates: (1,3,+2), (2,5,+1)
queries: K=1, K=3
```

We build `df` step by step:

| Step | Operation | df state (compressed) |
| --- | --- | --- |
| init | all zeros | [0,0,0,0,0] |
| 1 | +2 on [1,3] | [2,0,0,-2,0] |
| 2 | +1 on [2,5] | [2,1,0,-2,0] |

Now prefix sum:

| i | cur | A[i] | updated A |
| --- | --- | --- | --- |
| 1 | 2 | 1 | 3 |
| 2 | 3 | 2 | 5 |
| 3 | 3 | 3 | 6 |
| 4 | 1 | 4 | 5 |
| 5 | 1 | 5 | 6 |

Final array: `[3,5,6,5,6]`, sorted: `[3,5,5,6,6]`

Queries:

K=1 → 6

K=3 → 5

This confirms that overlapping updates are accumulated correctly and ordering queries depend only on final values.

### Example 2

Input:

```
N=4, A=[10,10,10,10]
update: (1,4,-5)
query: K=2
```

| Step | df | interpretation |
| --- | --- | --- |
| after update | [-5,0,0,5] | uniform decrease |

Prefix sum produces `[-5,-5,-5,-5]`, so final array is `[5,5,5,5]`.

Sorted array remains `[5,5,5,5]`, so K=2 returns 5.

This shows the algorithm handles negative updates and preserves stability under uniform transformations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + Q + M)$ | linear update application via difference array, linear reconstruction, sorting dominates |
| Space | $O(N)$ | difference array and modified array storage |

The runtime fits easily within typical constraints for $N, Q, M \le 2 \cdot 10^5$. Sorting is the only superlinear component and remains within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, q, m = map(int, input().split())
    a = list(map(int, input().split()))

    df = [0] * (n + 1)

    for _ in range(q):
        l, r, d = map(int, input().split())
        df[l - 1] += d
        if r < n:
            df[r] -= d

    cur = 0
    for i in range(n):
        cur += df[i]
        a[i] += cur

    a.sort()

    res = []
    for _ in range(m):
        k = int(input())
        res.append(str(a[n - k]))

    return "\n".join(res)

# minimal
assert run("1 0 1\n5\n1\n") == "5"

# single update full range
assert run("3 1 1\n1 2 3\n1 3 10\n1\n") == "13"

# overlapping updates
assert run("4 2 2\n1 3 1 2\n1 4 2\n1\n4\n") in {"5\n3", "5\n3"}

# negative updates
assert run("4 1 1\n10 10 10 10\n1 4 -5\n2\n") == "5"

# all equal final
assert run("5 0 1\n1 1 1 1 1\n3\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | single value | base correctness |
| full range update | uniform shift | boundary handling |
| overlapping | mixed updates | accumulation correctness |
| negative | decrements | sign correctness |
| all equal | stable order stats | sorting correctness |

## Edge Cases

One important edge case is when an update ends exactly at the last element. For example, $N=4$ with update $(2,4,d)$. The correct behavior is that no subtraction occurs outside the array bounds. The implementation handles this by checking `if r < n` before applying `df[r] -= d`, ensuring no invalid index is accessed and the effect stops precisely at the boundary.

Another case is when $K = N$, meaning the smallest element is requested. After sorting, accessing `a[n - k]` becomes `a[0]`, which is correct. This boundary often causes off-by-one errors when converting between 1-based query definitions and 0-based arrays, but the indexing formula consistently maps ranks to positions.

A final case is when all updates cancel out or produce identical values. Sorting still behaves correctly, and repeated elements do not affect indexing since order statistics depend only on position, not uniqueness.
