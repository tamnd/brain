---
title: "CF 978D - Almost Arithmetic Progression"
description: "We are given a sequence of integers, and we are allowed to slightly “tweak” each element independently by choosing to either decrease it by one, increase it by one, or leave it unchanged."
date: "2026-06-17T01:23:37+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 978
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 481 (Div. 3)"
rating: 1500
weight: 978
solve_time_s: 79
verified: true
draft: false
---

[CF 978D - Almost Arithmetic Progression](https://codeforces.com/problemset/problem/978/D)

**Rating:** 1500  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we are allowed to slightly “tweak” each element independently by choosing to either decrease it by one, increase it by one, or leave it unchanged. After applying these tiny adjustments, we want the resulting sequence to form an arithmetic progression, meaning the difference between consecutive elements becomes constant across the whole array.

The goal is not just to decide whether this is possible, but to minimize how many positions we actually modify. A position counts as modified if we apply either +1 or −1 to it. Leaving it unchanged costs nothing.

The key difficulty comes from the fact that each element has three possible final values, so the space of all modified sequences is exponential. With up to 100,000 elements, brute forcing all combinations of adjustments is impossible.

A useful way to think about the constraints is that any valid solution is fully determined by two parameters: the first element after modification, and the common difference. Once those are fixed, every element’s target value is forced. The only remaining freedom is choosing whether each position matches its original value, or must be shifted by exactly one to match the target.

A subtle edge case arises when no valid arithmetic progression can be formed even after modifications. For example, if the required differences force some element to be more than one unit away from its original value, that candidate progression is invalid. Another edge case is sequences of length 1 or 2, where any values always form an arithmetic progression, so the answer is always zero.

## Approaches

A brute-force approach would try every possible combination of adjustments, which means every element is in one of three states. That leads to 3^n possibilities, which is completely infeasible for n up to 100,000.

A more structured brute-force is to observe that an arithmetic progression is defined by its first two elements. If we guess the adjusted values of the first two positions, the rest of the sequence is forced. Since each of the first two positions has three options, we only have 9 candidate starting pairs. For each pair, we propagate the required common difference and check whether every element can be matched within ±1 of its original value.

This reduces the problem to a constant number of linear scans. The key insight is that once the first term and difference are fixed, every other term is determined uniquely, so we are no longer exploring combinations, only validating consistency.

During validation, each position contributes either 0 cost (if already correct) or 1 cost (if we must adjust by ±1). If any position is off by more than 1 from its target, that candidate progression is invalid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(3^n) | O(1) | Too slow |
| Try first two positions (9 cases) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We rely on the fact that an arithmetic progression is uniquely determined by its first two values.

### Steps

1. Extract candidate values for the first element: $b_0 - 1, b_0, b_0 + 1$. Do the same for the second element. These define at most 9 starting configurations.

Each configuration represents a possible choice of adjusted values for positions 0 and 1.
2. For each candidate pair $(x_0, x_1)$, compute the common difference $d = x_1 - x_0$.

This step is necessary because once the first two terms are fixed, all later terms must follow this exact difference.
3. Initialize a counter for modifications required. If $x_0 \neq b_0$, add one. If $x_1 \neq b_1$, add one.

This accounts for whether we used ±1 adjustments at the first two positions.
4. Iterate through the rest of the array. For each index $i \ge 2$, compute the required value:

$$target_i = x_0 + i \cdot d$$
5. Check feasibility for each position:

If $|b_i - target_i| > 1$, this candidate is impossible and must be discarded immediately.

Otherwise, if $b_i \neq target_i$, increment the modification counter.
6. Track the minimum cost over all valid candidate pairs.
7. If no candidate pair is valid, return -1. Otherwise return the minimum cost.

### Why it works

Every valid final sequence must be an arithmetic progression, so it must have some first term and common difference. Because each element can change by at most one, the true first two elements must lie in the sets $\{b_0-1, b_0, b_0+1\}$ and $\{b_1-1, b_1, b_1+1\}$. Therefore every valid solution is covered by one of the 9 candidate starting pairs.

Once a pair is fixed, the rest of the sequence has no freedom. Any deviation from the original array contributes exactly one cost, and any deviation greater than one makes the candidate impossible. This guarantees we neither miss valid solutions nor accept invalid ones.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    b = list(map(int, input().split()))

    if n <= 2:
        print(0)
        return

    INF = 10**18
    ans = INF

    for a0_delta in (-1, 0, 1):
        for a1_delta in (-1, 0, 1):
            x0 = b[0] + a0_delta
            x1 = b[1] + a1_delta

            d = x1 - x0
            cost = 0

            if x0 != b[0]:
                cost += 1
            if x1 != b[1]:
                cost += 1

            ok = True

            for i in range(2, n):
                expected = x0 + i * d
                diff = b[i] - expected

                if abs(diff) > 1:
                    ok = False
                    break

                if diff != 0:
                    cost += 1

            if ok:
                ans = min(ans, cost)

    print(-1 if ans == INF else ans)

if __name__ == "__main__":
    solve()
```

The implementation explicitly enumerates all valid initial perturbations for the first two elements. The rest of the sequence is validated in a single pass per candidate. The cost computation is tied directly to whether each element is already equal to its target or needs a ±1 adjustment.

A common pitfall is forgetting that we must check feasibility using absolute difference. Another is incorrectly recomputing differences incrementally without fixing the first two values, which can lead to inconsistent propagation.

## Worked Examples

### Example 1

Input:

```
4
24 21 14 10
```

We test a candidate starting pair. Suppose we choose (24, 21), giving d = -3.

| i | b[i] | expected | diff | valid | cost |
| --- | --- | --- | --- | --- | --- |
| 0 | 24 | 24 | 0 | yes | 0 |
| 1 | 21 | 21 | 0 | yes | 0 |
| 2 | 14 | 18 | -4 | no | - |

This candidate fails. Trying other combinations, one valid progression is [25, 20, 15, 10], which corresponds to (25, 20) with d = -5.

| i | b[i] | expected | diff | valid | cost |
| --- | --- | --- | --- | --- | --- |
| 0 | 24 | 25 | -1 | yes | 1 |
| 1 | 21 | 20 | 1 | yes | 2 |
| 2 | 14 | 15 | -1 | yes | 3 |
| 3 | 10 | 10 | 0 | yes | 3 |

The best achievable cost is 3.

### Example 2

Input:

```
5
1 3 5 7 9
```

This is already an arithmetic progression with difference 2.

Choosing (1, 3) gives d = 2.

| i | b[i] | expected | diff | valid | cost |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | yes | 0 |
| 1 | 3 | 3 | 0 | yes | 0 |
| 2 | 5 | 5 | 0 | yes | 0 |
| 3 | 7 | 7 | 0 | yes | 0 |
| 4 | 9 | 9 | 0 | yes | 0 |

Answer is 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(9n) | We try 9 starting pairs and validate each in a single pass over the array |
| Space | O(1) | Only a few variables are used regardless of input size |

The linear scan over at most nine candidates fits comfortably within constraints for n up to 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    n = int(input())
    b = list(map(int, input().split()))

    if n <= 2:
        return "0"

    INF = 10**18
    ans = INF

    for a0 in (-1,0,1):
        for a1 in (-1,0,1):
            x0 = b[0] + a0
            x1 = b[1] + a1
            d = x1 - x0

            cost = (a0 != 0) + (a1 != 0)
            ok = True

            for i in range(2, n):
                expected = x0 + i*d
                diff = b[i] - expected
                if abs(diff) > 1:
                    ok = False
                    break
                if diff != 0:
                    cost += 1

            if ok:
                ans = min(ans, cost)

    return "-1" if ans == INF else str(ans)

# provided sample
assert run("4\n24 21 14 10\n") == "3"

# all already AP
assert run("5\n1 3 5 7 9\n") == "0"

# minimum size
assert run("1\n100\n") == "0"

# impossible case
assert run("3\n1 100 1\n") == "-1"

# near-valid with small fixes
assert run("4\n2 4 6 9\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 0 | trivial AP |
| already AP | 0 | zero cost case |
| impossible | -1 | infeasible propagation |
| near-valid | 1 | single correction suffices |

## Edge Cases

A key edge case is when the optimal solution does not use the original first or second value. For instance, if shifting both by ±1 creates a valid progression but keeping them fixed does not, the algorithm must still explore those candidates. The enumeration of all 9 starting states guarantees this is covered, since (b0±1, b1±1) is always included.

Another edge case occurs when early positions look valid but later positions exceed the ±1 tolerance. In such cases, the algorithm must reject the entire candidate immediately rather than trying to “fix” later mismatches greedily. The absolute difference check enforces this strictly, preventing incorrect partial acceptance.

Finally, sequences of length 1 or 2 bypass all logic, since any two numbers always form an arithmetic progression.
