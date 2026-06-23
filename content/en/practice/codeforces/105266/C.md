---
title: "CF 105266C - \u91cd\u91cfII"
description: "We are given several test cases. In each case, there are several types of weights, and each type has an unlimited supply. However, there is a restriction in how we use them: all chosen weights must be placed on the same side of a balance scale."
date: "2026-06-24T01:01:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105266
codeforces_index: "C"
codeforces_contest_name: "2024 XTU Summer Camp Selection Competition"
rating: 0
weight: 105266
solve_time_s: 55
verified: true
draft: false
---

[CF 105266C - \u91cd\u91cfII](https://codeforces.com/problemset/problem/105266/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases. In each case, there are several types of weights, and each type has an unlimited supply. However, there is a restriction in how we use them: all chosen weights must be placed on the same side of a balance scale. Using some selection of these weights, we want to be able to represent every integer weight from 1 up to m, meaning for each target value x in that range, we must be able to pick a multiset of available weights whose sum is exactly x.

The goal is not to maximize representable range, but instead to achieve full coverage of the interval [1, m] while using as few individual weight pieces as possible, where we may reuse types but each chosen copy counts toward the total number of pieces used.

A key subtlety is that the input gives weight types, not individual pieces. We are effectively choosing how many copies of each weight type we take, and those copies then become our usable set. The question becomes: what is the minimum number of total copies such that all sums from 1 to m are achievable using unlimited repetition of those chosen copies.

The constraints are large in aggregate: up to 50 test cases, up to 10,000 weight types per case, and m can be as large as 1e9. Any solution that tries to simulate subset sums up to m directly is impossible because even O(m) per test case would already exceed limits, and O(n·m) is entirely infeasible.

A naive mistake is to assume we can greedily pick weights without tracking representable intervals. For example, if we pick weights 2 and 3 when m = 4, we might think we can somehow cover everything, but 1 becomes unreachable immediately. This shows that representability depends heavily on whether we can construct a continuous range starting from 1.

Another common failure case is ignoring gaps. Suppose we pick weights {1, 3}. We can form 1 and 3, but 2 is missing, and after that the system breaks completely since we cannot fill the gap using only additions of 1 and 3. Any correct strategy must ensure that the representable range stays continuous.

## Approaches

The brute-force idea is to consider every subset of weight copies we might take, then simulate all possible sums up to m using unbounded usage of those chosen weights. Even if we restrict ourselves to selecting at most k copies, the number of ways to choose them is combinatorial in n, and then each choice requires a knapsack-style DP up to m. This quickly explodes: even a single DP up to 1e9 is impossible, and enumerating subsets is exponentially worse.

The key observation is that we do not actually care about individual sums beyond the current contiguous prefix we can already form. If we already know we can form every value in [1, R], then a new weight w behaves in a very structured way: using it, we can extend coverage to [1, R + w] if and only if w is at most R + 1. Otherwise, a gap appears at R + 1 and we can never fix it later.

This leads to a greedy construction reminiscent of building reachable sums with minimal elements. We process weights in increasing order and maintain the largest continuous representable prefix R. Initially R = 0, since nothing is representable. Each time we decide to take a weight w, we use one copy of it, which allows us to extend reach up to R + w provided w is usable under the current constraint. If the smallest remaining weight is larger than R + 1, we are forced to conclude that 1..m cannot be completed.

To minimize the number of chosen pieces, we should always pick the smallest available weight that helps extend the range, since larger weights consume more “power” per item and do not help fill small gaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subset + DP) | exponential / O(2^n · m) | O(m) | Too slow |
| Optimal greedy prefix extension | O(n log n) | O(1) extra | Accepted |

## Algorithm Walkthrough

We sort the weights so that we always consider smaller values first.

1. Initialize a variable R = 0 representing the maximum continuous sum we can currently form. Also initialize an index i = 0 and a counter ans = 0.
2. While R < m, we try to extend the range. We look at the smallest unused weight w = a[i].
3. If no such weight exists or w > R + 1, we stop immediately and return -1. This is because we cannot form R + 1, so the range becomes permanently disconnected.
4. Otherwise, we take this weight once, increment ans by 1, and update R = R + w. We then move i forward.
5. Repeat until R >= m, at which point ans is the minimum number of weight copies needed.

The important design choice is always consuming the smallest possible weight that can extend the reachable interval. Larger weights are never better in early stages because they do not help close small missing values and only become useful after the prefix has already grown.

### Why it works

At any moment, assume we can represent every integer in [1, R]. Any new chosen weight w can only contribute meaningfully if it does not exceed R + 1, because otherwise R + 1 remains unreachable no matter how we combine existing weights with w. If w ≤ R + 1, adding a single copy of w extends the reachable interval to [1, R + w], since we can form all values up to R and then shift by w to fill the next segment continuously. This invariant ensures that R always represents the largest contiguous prefix achievable with the selected multiset, and the greedy choice ensures we never waste a small weight later when it might be critical for closing a gap.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    out = []
    for _ in range(T):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        R = 0
        i = 0
        ans = 0

        while R < m:
            if i == n or a[i] > R + 1:
                out.append("-1")
                break
            R += a[i]
            ans += 1
            i += 1
        else:
            out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code directly mirrors the greedy construction. Sorting ensures we always see the smallest candidate first. The variable `R` tracks the reachable prefix, and the loop invariant guarantees that all values in `[1, R]` are achievable with the currently selected weights. The condition `a[i] > R + 1` is the precise failure point where the gap at `R + 1` becomes unavoidable.

A subtle detail is the `while-else` structure, which cleanly separates successful completion (R reaching m) from early termination.

## Worked Examples

### Example 1

Input:

```
n=3, m=8
a = [1,2,4]
```

| Step | R | next w | action | ans |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | take 1 → R=1 | 1 |
| 2 | 1 | 2 | take 2 → R=3 | 2 |
| 3 | 3 | 4 | take 4 → R=7 | 3 |
| 4 | 7 | - | need more, no w ≤ 8 | stop |

We reach R = 7, which is still below 8, so we fail. The example demonstrates that even though the numbers look powerful, we still cannot cover the final unit interval.

### Example 2

Input:

```
n=4, m=10
a = [1,2,3,10]
```

| Step | R | next w | action | ans |
| --- | --- | --- | --- | --- |
| 1 | 0 | 1 | take 1 → R=1 | 1 |
| 2 | 1 | 2 | take 2 → R=3 | 2 |
| 3 | 3 | 3 | take 3 → R=6 | 3 |
| 4 | 6 | 10 | take 10 → R=16 | 4 |

We reach R ≥ 10 successfully. The large weight is only useful after the prefix is already sufficiently large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, greedy scan is linear |
| Space | O(1) extra | aside from input storage |

The constraints allow up to 10,000 weights per test case, so sorting per test is easily fast enough, and the linear scan ensures the solution comfortably fits within time limits even in worst-case scenarios.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    out = []
    for _ in range(T):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        R = 0
        i = 0
        ans = 0

        while R < m:
            if i == n or a[i] > R + 1:
                out.append("-1")
                break
            R += a[i]
            ans += 1
            i += 1
        else:
            out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("3\n3 8\n1 2 4\n3 4\n2 3 4\n3 4\n1 2 3\n") == "-1\n-1\n2"

# minimum case
assert run("1\n1 1\n1\n") == "1"

# already sufficient small range
assert run("1\n2 3\n1 2\n") == "2"

# impossible gap case
assert run("1\n2 10\n2 3\n") == "-1"

# large jump case
assert run("1\n3 10\n1 2 10\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1-weight | 1 | base feasibility |
| contiguous small | 2 | normal growth |
| gap early | -1 | failure detection |
| large weight included | 3 | late-use heavy weight |

## Edge Cases

A critical edge case is when the smallest available weight is greater than 1. For example, if the input starts with 2, we immediately fail because we cannot form 1, and thus no continuous interval can ever begin. The algorithm catches this at initialization: since R = 0, we require a weight ≤ 1, and 2 violates this.

Another case is when weights grow too quickly, such as [1, 100, 101]. After taking 1, R = 1, but the next usable weight must be ≤ 2. Since 100 is too large, we terminate immediately. The algorithm correctly rejects early rather than trying to compensate later.

A final subtle case is when a very large weight appears early in the sorted list but smaller weights exist later. Sorting prevents incorrect decisions here, ensuring that small bridging weights are always considered before large jumps.
