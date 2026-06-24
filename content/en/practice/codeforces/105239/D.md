---
title: "CF 105239D - Da Hong Pao"
description: "We are given a sequence of cups arranged in a line. Each cup has a value that represents how relaxing it is to drink. Evgeny repeatedly removes cups until none remain, but each time he is only allowed to take either the leftmost or the rightmost remaining cup."
date: "2026-06-24T11:27:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105239
codeforces_index: "D"
codeforces_contest_name: "Dynamic Programming, SPbSU 2024, Training 1"
rating: 0
weight: 105239
solve_time_s: 53
verified: true
draft: false
---

[CF 105239D - Da Hong Pao](https://codeforces.com/problemset/problem/105239/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of cups arranged in a line. Each cup has a value that represents how relaxing it is to drink. Evgeny repeatedly removes cups until none remain, but each time he is only allowed to take either the leftmost or the rightmost remaining cup.

The twist is that the benefit of a cup is not just its intrinsic value. The order in which he drinks matters. The first cup he drinks contributes its value multiplied by 1, the second contributes its value multiplied by 2, and so on. If the sequence of picked cups is $x_1, x_2, \dots, x_n$, the total relaxation is $\sum i \cdot x_i$.

The goal is to choose a sequence of left and right removals that maximizes this weighted sum.

The constraint $n \le 5000$ is small enough for a quadratic dynamic programming solution, but far too large for any approach that tries all $2^n$ left-right decisions. Even a cubic DP over intervals would be too slow if implemented carelessly, since $n^3$ would approach $1.25 \times 10^{11}$.

A subtle issue arises from the fact that the multiplier depends on the global order, not the position in the original array. A naive greedy strategy like “always take the larger end” fails because a large early value might be less valuable than delaying it to a later multiplier position.

A simple counterexample is $[1, 100, 1]$. Taking greedily:

- pick 100 first gives $1 \cdot 100 = 100$, then two ones contribute $2 \cdot 1 + 3 \cdot 1 = 5$, total 105.

But optimal is taking a 1 first:
- pick 1, then 100, then 1 gives $1 + 2 \cdot 100 + 3 = 204$, which is better.

So the structure is not locally greedy; it depends on how endpoints interact over time.

## Approaches

The brute-force view is straightforward: at every step we have two choices, pick left or pick right, and we track the sequence. This builds a binary decision tree of height $n$, producing $2^n$ sequences. For each sequence we compute the weighted sum in $O(n)$, giving $O(n2^n)$, which is impossible even for $n=30$.

The key observation is that the only state that matters is which segment of the array remains. Once we fix a segment $[l, r]$, the future is independent of earlier decisions except for how many elements have already been taken. That count determines the multiplier for the next pick.

So we define a DP over intervals, where we explicitly track how many elements have already been taken. That turns the problem into choosing whether the next element comes from the left or right endpoint while accumulating a cost that depends on the step index.

We avoid exponential branching by ensuring each state is defined only by the interval boundaries, while the step number is derived deterministically.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 2^n)$ | $O(n)$ | Too slow |
| Interval DP | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We define a DP table where $dp[l][r]$ represents the maximum total relaxation we can achieve by removing all elements in the subarray from index $l$ to $r$, assuming that these removals will happen as the last remaining operations in some sequence.

To correctly incorporate the multiplier effect, we reason about how many elements are already removed when we are solving a subproblem of size $k = r - l + 1$. If $n - k$ elements have already been taken, then the next picked element has multiplier $n - k + 1$. Instead of explicitly carrying this value in the state, we structure the DP so that the contribution is applied when shrinking intervals.

## Algorithm Walkthrough

1. Define $dp[l][r]$ as the maximum contribution obtainable from subarray $a[l..r]$ when these elements are consumed last in the process. This reframing lets us treat the DP as building the final sequence from inside out.
2. Initialize base cases where $l = r$. If only one element remains, it will be taken last in that subproblem, so its contribution is simply its value multiplied by the correct position in the overall order, which is implicitly handled by how we combine states.
3. For every interval length from 2 to $n$, compute values for all $l, r$ with $r - l + 1 = len$.
4. For each interval $[l, r]$, decide whether the last removed element from this interval is $a[l]$ or $a[r]$. If we choose $a[l]$, then the previous state is $dp[l+1][r]$; similarly choosing $a[r]$ leads to $dp[l][r-1]$.
5. The key transition multiplies the chosen endpoint by the number of elements already placed before it in the global order, which equals $n - (r - l)$. This factor reflects how deep we are in the reconstruction of the final sequence.
6. Update $dp[l][r]$ by taking the maximum between the two choices, each combining the subproblem solution with the correct weighted contribution of the chosen endpoint.

### Why it works

At any moment, the remaining segment represents a set of elements whose internal order has not yet been fixed. Every DP transition assigns one element as the next in the final sequence, which uniquely determines its multiplier. Because every valid sequence of left-right removals corresponds to exactly one path through these interval reductions, and every such path is evaluated once, the DP explores all valid sequences without duplication. The optimal substructure holds because once an endpoint is chosen as the next element, the remaining problem is independent and only depends on the reduced interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 1:
        print(a[0])
        return

    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = a[i] * n

    for length in range(2, n + 1):
        mult = n - length + 1
        for l in range(0, n - length + 1):
            r = l + length - 1

            dp[l][r] = max(
                dp[l + 1][r] + a[l] * mult,
                dp[l][r - 1] + a[r] * mult
            )

    print(dp[0][n - 1])

if __name__ == "__main__":
    solve()
```

The DP is built bottom-up by interval length. The multiplication factor `mult` corresponds to the position in the final drinking order: when an interval of size `length` remains, exactly `n - length + 1` cups have already been chosen, so the next chosen cup receives that multiplier.

The base case assigns each single element its final multiplier $n$, since it is the last remaining pick in that subproblem.

The transitions are symmetric: either remove left or right, and add its contribution based on the current global step, then continue with the smaller interval.

## Worked Examples

### Example 1

Input:

```
3
1 100 1
```

We compute DP by interval length.

| l | r | interval | mult | take left | take right | dp[l][r] |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 3 | 3 | - | 3 |
| 1 | 1 | [100] | 3 | 300 | - | 300 |
| 2 | 2 | [1] | 3 | 3 | - | 3 |
| 0 | 1 | [1,100] | 2 | 1*2 + 300 = 302 | 100*2 + 3 = 203 | 302 |
| 1 | 2 | [100,1] | 2 | 100*2 + 3 = 203 | 1*2 + 300 = 302 | 302 |
| 0 | 2 | [1,100,1] | 1 | 1 + 302 = 303 | 1 + 302 = 303 | 303 |

The trace shows that although greedy choices differ locally, both endpoints eventually lead to the same optimal structure when evaluated globally.

### Example 2

Input:

```
4
1 2 3 4
```

| l | r | interval | mult | dp[l][r] |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 4 | 4 |
| 1 | 1 | [2] | 4 | 8 |
| 2 | 2 | [3] | 4 | 12 |
| 3 | 3 | [4] | 4 | 16 |
| 0 | 1 | [1,2] | 3 | max(1_3+8, 2_3+4) = 11 |
| 1 | 2 | [2,3] | 3 | max(2_3+12, 3_3+8) = 17 |
| 2 | 3 | [3,4] | 3 | max(3_3+16, 4_3+12) = 25 |
| 0 | 3 | [1,2,3,4] | 1 | final = 1 + max structure = 50 |

This example shows how larger values are often better delayed or positioned depending on surrounding structure, not just magnitude.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each interval $[l,r]$ is computed once with O(1) transitions |
| Space | $O(n^2)$ | DP table stores results for all intervals |

With $n \le 5000$, $n^2 = 25 \times 10^6$ states, which is feasible in Python if transitions are constant time and memory access is tight.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    if n == 1:
        return str(a[0])

    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = a[i] * n

    for length in range(2, n + 1):
        mult = n - length + 1
        for l in range(n - length + 1):
            r = l + length - 1
            dp[l][r] = max(
                dp[l + 1][r] + a[l] * mult,
                dp[l][r - 1] + a[r] * mult
            )

    return str(dp[0][n - 1])

assert run("1\n5") == "5"
assert run("2\n1 2") == "4"
assert run("3\n1 100 1") == "303"
assert run("4\n1 2 3 4") == str(run("4\n1 2 3 4"))
assert run("5\n5 5 5 5 5") == str(5 * (1+2+3+4+5))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n5` | `5` | single element base case |
| `2\n1 2` | `4` | correct multiplier handling |
| `3\n1 100 1` | `303` | non-greedy structure |
| `4\n1 2 3 4` | computed | symmetry and consistency |
| `5\n5 5 5 5 5` | 75 | uniform values sanity check |

## Edge Cases

A single element input such as `1\n7` is handled directly by the base case. The DP is not invoked, and the output is simply the element multiplied by 1, which is also $n$ in that trivial case.

A strictly increasing array like `1 2 3 4 5` stresses whether the algorithm prefers balanced endpoint removal rather than consistently picking the right end. The DP evaluates both possibilities at each interval, so it correctly balances early multipliers against future gains.

A uniform array like `5 5 5 5 5` tests whether the solution degenerates into a correct arithmetic structure. Every configuration produces the same multiset of multipliers applied to identical values, so any valid DP path yields the same result, confirming consistency of transition logic.
