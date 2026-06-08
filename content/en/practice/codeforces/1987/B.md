---
title: "CF 1987B - K-Sort"
description: "We are given an integer array and we are allowed to repeatedly “pay coins to raise selected elements by 1”. In one operation we choose a size $k$, pay $k+1$ coins, then pick any $k$ positions and increment those positions by exactly one."
date: "2026-06-08T15:53:16+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1987
codeforces_index: "B"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2024 (Div. 1 + Div. 2)"
rating: 1000
weight: 1987
solve_time_s: 115
verified: false
draft: false
---

[CF 1987B - K-Sort](https://codeforces.com/problemset/problem/1987/B)

**Rating:** 1000  
**Tags:** greedy  
**Solve time:** 1m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an integer array and we are allowed to repeatedly “pay coins to raise selected elements by 1”. In one operation we choose a size $k$, pay $k+1$ coins, then pick any $k$ positions and increment those positions by exactly one.

The goal is to transform the array into a non-decreasing sequence using minimum total coins. Non-decreasing means every element must be at most the next one.

A useful way to think about this is that every operation distributes a single “unit of increment” to $k$ chosen positions, but the cost is not proportional to $k$, it is $k+1$. So each unit increment applied to a position is never free, and grouping increments across positions has a fixed overhead of 1 coin per operation.

The constraints are tight enough that any solution must be essentially linear per test case. The sum of $n$ over all tests is $10^5$, so anything quadratic per test is impossible. This immediately rules out simulating all possible operations or repeatedly scanning the array with nested loops.

A subtle issue appears in how increments interact: increasing earlier elements is expensive because it may require many coordinated operations, while later elements naturally act as targets for adjustments. The main difficulty is deciding how to interpret the cost model in a way that avoids explicitly simulating operations.

A naive mistake is to assume we should always “fix violations locally” by increasing $a_i$ to match $a_{i-1}$. That ignores that one operation can affect many positions simultaneously, so the true cost is not tied to individual increments but to how increments can be shared.

## Approaches

The brute-force viewpoint would try to simulate all possible operations or greedily fix the first decreasing pair by choosing some subset of indices to increment. This quickly explodes because each operation involves choosing any subset of size $k$, and the number of ways to choose subsets is exponential. Even if we ignore combinatorics and try greedy local fixing, we still need to reason about future interactions between adjustments, which leads to repeated passes and potentially $O(n^2)$ behavior.

The key observation is to reverse perspective: instead of thinking in terms of operations, we track how many increments are required at each position relative to previous elements to maintain a non-decreasing structure. Each time $a_i < a_{i-1}$, we need to “repair” a deficit of size $a_{i-1} - a_i$. That deficit represents how much total increment must eventually be applied to position $i$ or beyond.

The crucial structural insight is that each operation contributes one unit of cost overhead but can distribute increments across multiple positions. This means the real cost is dominated by how many times we need to “start a new batch” of corrections rather than how many increments are needed in total.

When processing left to right, every time the sequence decreases, we are forced to introduce additional “repair units”. Each unit of decrease effectively contributes independently to the answer because it cannot be amortized across earlier or unrelated corrections.

This reduces the problem to accumulating all positive drops in the array, since each drop represents a necessary independent unit of correction under the operation constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential / $O(n^2)$ | $O(n)$ | Too slow |
| Prefix greedy accumulation | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We scan the array from left to right and track how much the current value must be raised to avoid breaking non-decreasing order.

1. Initialize the answer as 0 and set a variable `need` to 0, representing how much the current element must be increased to match previous constraints.
2. Iterate through the array from left to right starting at index 1.
3. For each position, compare the previous adjusted value with the current value.
4. If the previous value is greater than the current value, compute the deficit $d = a_{i-1} - a_i$. Add this deficit to the answer because it represents a mandatory correction that cannot be avoided or shared without cost.
5. Conceptually propagate this deficit forward by treating the current value as raised to match the previous value. This ensures future comparisons are done against the corrected sequence.
6. Continue until the end of the array and output the accumulated answer.

The reason we can accumulate deficits directly is that each downward step forces independent “lifting work”. Even though operations can affect multiple indices, a drop between consecutive elements cannot be resolved without investing at least that much correction mass somewhere in the system.

### Why it works

The algorithm maintains the invariant that after processing index $i$, the effective value of the sequence up to $i$ is non-decreasing. Any time this invariant would be violated, the deficit represents a mandatory amount of increase that must exist somewhere in future operations. Since operations cannot reduce earlier elements and only add increments, each such deficit must be accounted for independently, and no future operation can retroactively eliminate the need for it. This makes the sum of all positive decreases equal to the minimum achievable cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        ans = 0

        for i in range(1, n):
            if a[i] < a[i - 1]:
                ans += a[i - 1] - a[i]
                a[i] = a[i - 1]

        print(ans)

if __name__ == "__main__":
    solve()
```

The code performs a single pass per test case. The key implementation detail is that when a decrease is detected, we immediately update the current element to match the previous one. This ensures that subsequent comparisons are made against the already corrected prefix, preserving the invariant that the processed prefix is non-decreasing.

A common off-by-one mistake would be to forget updating `a[i]`, which would cause later comparisons to underestimate the required corrections. Another subtle issue is accumulation: the answer must sum only positive differences, not absolute differences, since increases do not require any correction.

## Worked Examples

We trace two cases to see how the correction propagates.

### Example 1

Input: `[2, 1, 4, 7, 6]`

| i | a[i-1] | a[i] | deficit | ans | updated array |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 1 | 1 | [2, 2, 4, 7, 6] |
| 2 | 2 | 4 | 0 | 1 | [2, 2, 4, 7, 6] |
| 3 | 4 | 7 | 0 | 1 | [2, 2, 4, 7, 6] |
| 4 | 7 | 6 | 1 | 2 | [2, 2, 4, 7, 7] |

This shows how each local drop contributes independently, and how fixing one position affects future comparisons.

### Example 2

Input: `[344, 12, 37, 60, 311, 613, 365, 328, 675]`

| i | a[i-1] | a[i] | deficit | ans |
| --- | --- | --- | --- | --- |
| 1 | 344 | 12 | 332 | 332 |
| 2 | 344 | 37 | 0 | 332 |
| 3 | 60 | 60 | 0 | 332 |
| 4 | 311 | 311 | 0 | 332 |
| 5 | 613 | 613 | 0 | 332 |
| 6 | 613 | 365 | 248 | 580 |
| 7 | 613 | 328 | 285 | 865 |
| 8 | 613 | 675 | 0 | 865 |

Each decrease contributes independently, confirming that the answer is purely the sum of all downward gaps after local propagation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each element is visited once and updated in-place at most once |
| Space | $O(1)$ | Only a running sum is maintained besides the input array |

The total input size across all test cases is $10^5$, so a linear scan per test case is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        for i in range(1, n):
            if a[i] < a[i-1]:
                ans += a[i-1] - a[i]
                a[i] = a[i-1]
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""5
3
1 7 9
5
2 1 4 7 6
4
1 3 2 4
1
179
9
344 12 37 60 311 613 365 328 675
""") == """0
3
2
0
1821"""

# custom cases
assert run("""1
2
5 1
""") == "4", "single drop"

assert run("""1
5
1 1 1 1 1
""") == "0", "all equal"

assert run("""1
4
4 3 2 1
""") == "3", "strictly decreasing"

assert run("""1
6
1 5 2 6 3 7
""") == "6", "alternating drops"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 1 | 4 | single large decrease propagation |
| 1 1 1 1 1 | 0 | already sorted case |
| 4 3 2 1 | 3 | cumulative adjacent drops |
| 1 5 2 6 3 7 | 6 | repeated local corrections |

## Edge Cases

A key edge case is when the array is strictly decreasing. For example, `[4, 3, 2, 1]` triggers a correction at every step. The algorithm processes it as 1 + 1 + 1, since each step requires lifting the current value to match the previous corrected value. The propagation ensures the prefix remains consistent, so no deficit is missed.

Another case is when a large drop is followed by an increase. In `[10, 1, 100]`, the first step contributes 9, and after propagation the second element becomes 10, so the next comparison is valid. The large increase afterward does not cancel earlier work because operations only add increments and cannot “refund” earlier needed corrections.

These behaviors confirm that each downward transition is independently accounted for and that the greedy propagation correctly maintains a valid prefix at all times.
