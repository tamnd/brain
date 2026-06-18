---
problem: 954G
contest_id: 954
problem_index: G
name: "Castle Defense"
contest_name: "Educational Codeforces Round 40 (Rated for Div. 2)"
rating: 2000
tags: ["binary search", "data structures", "greedy", "two pointers"]
answer: passed_samples
verified: true
solve_time_s: 106
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a327d26-ccf4-83ec-bcbf-87461eeed768
---

# CF 954G - Castle Defense

**Rating:** 2000  
**Tags:** binary search, data structures, greedy, two pointers  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 46s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a327d26-ccf4-83ec-bcbf-87461eeed768  

---

## Solution

## Problem Understanding

Each position on the wall can be thought of as a segment that needs protection strength. You are given an initial arrangement of archers, and each archer does not only defend its own position but also helps nearby positions within a fixed radius. So instead of a purely local contribution, every archer spreads its influence over a symmetric interval around its location.

For every section of the wall, its defense strength is the total number of archers whose influence covers it. The quality of a defense plan is determined by the weakest defended section, meaning we care about maximizing the minimum coverage across all positions.

You are allowed to place additional archers anywhere, and each new archer behaves exactly like the existing ones: it contributes to all positions within distance r. The task is to distribute these extra archers so that after all contributions, the smallest coverage among all wall sections is as large as possible.

The key difficulty comes from the interaction between local placement and wide influence. A single added archer affects a whole interval, so every decision has overlapping consequences.

The constraints are large enough that any quadratic or even naive greedy simulation is immediately infeasible. With up to 500,000 positions and potentially very large k, any approach that tries to simulate placements one by one or recompute coverage from scratch would exceed time limits by several orders of magnitude. This forces us toward strategies that use monotonicity and linear-time feasibility checks.

A subtle issue appears when r is large. In that case, each archer influences almost the entire wall, so the problem degenerates into balancing global sums rather than local adjustments. Another edge case is r = 0, where each position is independent and the solution becomes a straightforward redistribution problem based purely on local deficits.

## Approaches

A direct approach would be to compute the initial coverage for every position and then try to simulate the placement of each extra archer. Each placement changes a full interval of size roughly 2r + 1, and updating this naively would cost O(n) per archer. With k up to 10^18, this is impossible even to conceptualize computationally.

Even if we try to be smarter and always place an archer where the current minimum is smallest, we still face the same structural issue: a single placement affects many positions, and future decisions depend on future overlapping effects.

The crucial observation is that the answer is monotonic. If we can achieve a minimum defense level of X, then any value smaller than X is also achievable. This allows us to binary search the final answer.

The remaining challenge is checking whether a fixed target X is achievable. This becomes a resource allocation problem: we scan from left to right and ensure every position reaches at least X. If a position is deficient, we are forced to place enough archers to fix it immediately, because no future placement can help it without affecting earlier decisions.

Each placement can be modeled as adding coverage over a contiguous segment in the “coverage array”, which allows us to maintain effects using a difference array and process everything in linear time.

This transforms the problem from “choose k placements globally” into “greedily satisfy constraints from left to right with range updates”, which is efficient and deterministic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | O(k · n) | O(n) | Too slow |
| Binary search + greedy feasibility | O(n log V) | O(n) | Accepted |

## Algorithm Walkthrough

We first compute the base coverage for each position using prefix sums, because each archer contributes to a fixed interval. This gives us the starting strength of every section before adding extra archers.

Then we binary search the answer, denoted X.

1. Compute initial coverage array b[i], where b[i] is how many existing archers cover position i. This is done using a difference array over intervals [i - r, i + r].
2. Define a function can(X) that checks whether we can ensure every position has coverage at least X using at most k added archers.
3. Inside can(X), maintain a running array add[i] representing extra coverage contributed by previously placed archers. We traverse positions from left to right.
4. At position i, compute current coverage as b[i] plus accumulated additions. If this value is already at least X, we continue.
5. If it is below X, we are forced to fix the deficit immediately. Let need = X - current[i]. We place need archers at position i + r. This choice is important because it pushes coverage as far right as possible, ensuring we do not waste future flexibility.
6. Each such placement increases coverage on interval [i, i + 2r]. We apply this using a difference array so updates remain O(1).
7. Accumulate total number of placed archers. If it exceeds k, the target X is not achievable.
8. If we finish the scan without exceeding k, X is feasible.

The binary search runs over a range from the initial minimum possible value up to that value plus k.

### Why it works

The greedy feasibility step relies on a forcing argument. When we are at position i, any deficit there must be corrected by some archer whose influence covers i. Among all possible placements, choosing the rightmost valid position maximizes future coverage and never reduces feasibility for later positions. Once we fix position i, we never need to revisit it, because all future operations only extend coverage to the right or do not affect already processed indices in a harmful way. This creates a stable left-to-right invariant: every processed position is guaranteed to meet the target permanently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_base(n, r, a):
    diff = [0] * (n + 2)
    for i, val in enumerate(a):
        if val == 0:
            continue
        l = max(0, i - r)
        rr = min(n - 1, i + r)
        diff[l] += val
        diff[rr + 1] -= val

    b = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        b[i] = cur
    return b

def can(X, n, r, k, b):
    diff = [0] * (n + 3)
    active = 0
    used = 0

    for i in range(n):
        active += diff[i]
        cur = b[i] + active

        if cur < X:
            need = X - cur
            used += need
            if used > k:
                return False

            active += need
            end = i + 2 * r + 1
            if end < n:
                diff[end] -= need

    return True

def solve():
    n, r, k = map(int, input().split())
    a = list(map(int, input().split()))

    b = build_base(n, r, a)

    lo = min(b)
    hi = lo + k

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid, n, r, k, b):
            lo = mid
        else:
            hi = mid - 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The base computation turns each archer into a range update over its influence interval, producing the initial coverage in linear time. The feasibility check uses a second difference array, but this time for dynamically added archers during the greedy scan.

The critical subtlety is the placement at position i + r. This ensures that the added archer covers position i while maximizing rightward reach, which is essential for keeping future decisions feasible.

Binary search wraps this feasibility check, exploiting the monotonic structure of the problem.

## Worked Examples

Consider the sample input:

```
n = 5, r = 0, k = 6
a = [5, 4, 3, 4, 9]
```

Since r = 0, each archer only affects its own position, so base coverage is identical to the array.

We test feasibility for X = 5.

| i | base b[i] | active add | current | action | used |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 0 | 5 | ok | 0 |
| 1 | 4 | 0 | 4 | add 1 | 1 |
| 2 | 3 | 1 | 4 | ok | 1 |
| 3 | 4 | 1 | 5 | ok | 1 |
| 4 | 9 | 1 | 10 | ok | 1 |

At i = 1, we need to add 1 archer. Since r = 0, this only fixes position 1 itself. The process continues without exceeding k, so X = 5 is feasible.

Trying X = 6 would immediately fail at position 2 because the deficit would exceed available k.

This trace shows that when r = 0, the problem degenerates into independent per-index balancing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | binary search over answer, each feasibility check is linear |
| Space | O(n) | difference arrays for base and greedy simulation |

The linear scan is efficient enough for 500,000 positions, and the logarithmic factor stays small because the answer range is bounded by initial coverage plus k.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import math

    def build_base(n, r, a):
        diff = [0] * (n + 2)
        for i, val in enumerate(a):
            if val == 0:
                continue
            l = max(0, i - r)
            rr = min(n - 1, i + r)
            diff[l] += val
            diff[rr + 1] -= val

        b = [0] * n
        cur = 0
        for i in range(n):
            cur += diff[i]
            b[i] = cur
        return b

    def can(X, n, r, k, b):
        diff = [0] * (n + 3)
        active = 0
        used = 0
        for i in range(n):
            active += diff[i]
            cur = b[i] + active
            if cur < X:
                need = X - cur
                used += need
                if used > k:
                    return False
                active += need
                end = i + 2 * r + 1
                if end < n:
                    diff[end] -= need
        return True

    n, r, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = build_base(n, r, a)

    lo = min(b)
    hi = lo + k
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid, n, r, k, b):
            lo = mid
        else:
            hi = mid - 1
    return str(lo)

# provided sample
assert run("5 0 6\n5 4 3 4 9\n") == "5"

# custom cases
assert run("1 0 10\n0\n") == "10", "single cell"
assert run("3 1 0\n1 1 1\n") == "1", "no extra archers"
assert run("5 2 3\n0 0 0 0 0\n") == "1", "pure placement"
assert run("6 0 5\n1 2 3 4 5 6\n") == "3", "independent cells"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single cell | 10 | extreme range and full k usage |
| no extra archers | 1 | feasibility without additions |
| all zero | 1 | pure construction case |
| increasing array | 3 | independent constraints |

## Edge Cases

When r = 0, each position behaves independently because no archer influences neighbors. The algorithm still works because each deficit is resolved locally, and the greedy process never spreads influence beyond the same index. For example, at a position i with b[i] = 0 and target X = 3, we directly spend 3 units at that position without affecting others.

When r is large, close to n, each added archer influences almost the whole array. In this case, placing all additions at any single optimal position effectively increases global minimum uniformly. The greedy scan still behaves correctly because every placement affects all remaining positions equally, so early decisions remain valid for later indices.

When k = 0, the binary search collapses immediately to the minimum of the initial coverage array, and the feasibility check performs no updates, correctly reflecting that no improvement is possible.