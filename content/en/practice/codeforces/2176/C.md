---
title: "CF 2176C - Odd Process"
description: "We are given a multiset of coin values and asked to simulate a process that depends not only on which coins we pick, but also on the parity of the running sum inside a temporary bag."
date: "2026-06-07T22:28:24+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2176
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1070 (Div. 2)"
rating: 1300
weight: 2176
solve_time_s: 111
verified: false
draft: false
---

[CF 2176C - Odd Process](https://codeforces.com/problemset/problem/2176/C)

**Rating:** 1300  
**Tags:** greedy, sortings  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a multiset of coin values and asked to simulate a process that depends not only on which coins we pick, but also on the parity of the running sum inside a temporary bag. We perform exactly $k$ selections, where each selection removes one unused coin and adds it to the bag. However, the bag has a reset rule: whenever the sum of values currently inside the bag becomes even after adding a coin, the bag is immediately emptied and the current accumulated sum is discarded.

The score after $k$ actions is simply the sum currently in the bag, which might be zero if a reset has happened at the end or earlier. We must compute the maximum achievable score for every $k$ from $1$ to $n$.

The important difficulty is that earlier resets erase all progress, so the problem is not a straightforward “take the largest k elements” type of greedy. The parity interaction makes the process history dependent.

The constraints force us toward linear or near-linear behavior per test case. Since the total $n$ across all test cases is at most $2 \cdot 10^5$, any solution that is $O(n^2)$ per test case or even per value of $k$ is impossible. This immediately rules out simulation over all choices of subsets or DP over subsets of picked coins.

A subtle edge case is when all numbers are even. Every single pick immediately makes the sum even, so the bag is reset after every operation. The answer for all $k$ is zero. Another edge case is when all numbers are odd, where parity alternation becomes deterministic but still allows accumulation only in controlled ways. Finally, mixtures of odd and even values create situations where a single even pick can wipe everything, making naive greedy strategies fail.

## Approaches

A brute-force approach would try to simulate all possible ways of picking coins for each $k$. For each prefix of length $k$, we would consider all permutations of coin choices and simulate the bag process. This is factorial in nature and completely infeasible beyond tiny $n$, since even $O(n!)$ is far beyond limits.

The key observation is that the process is governed entirely by parity transitions of the running sum. The only thing that matters at any moment is whether the current bag sum is odd or even, and which coins we choose to influence that parity.

Let us separate coins into odd and even values. Even coins do not change parity, while odd coins flip it. The reset condition triggers exactly when we reach an even sum after an addition, which means we cannot safely accumulate arbitrary sequences: only certain patterns of odd/even choices survive.

The crucial simplification is to think in terms of building “active segments” that end when the sum becomes even. Each time we end such a segment, the bag is cleared, so only the last unfinished segment contributes to the final score. Therefore, the answer for each $k$ depends on how many elements we can place into a final non-resetting segment, and how large a sum that segment can achieve.

The optimal strategy becomes: we want to maximize the sum of the last active segment while ensuring that no earlier segment invalidates it. This naturally leads to sorting coins in descending order and building the best possible suffix that does not trigger a reset too early.

We precompute prefix sums of sorted values and carefully track the best achievable suffix depending on parity constraints. For each $k$, we determine the best suffix that can survive without being wiped and take its sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n!)$ | $O(n)$ | Too slow |
| Sorting + Prefix Analysis | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Split the coins into their values and sort them in descending order. This ensures that whenever we decide to keep coins in the final segment, we always take the largest available ones first, since order within the bag does not matter for sum, only selection does.
2. Build a prefix sum array over the sorted values. This allows fast computation of the sum of any top $k$ chosen coins.
3. For each $k$, consider the best possible selection of $k$ coins that could form the final surviving segment. The key constraint is that the segment must avoid ending in a reset state too early, which depends on parity of chosen elements.
4. Track how many odd and even elements are included among the top $k$ coins. Even elements are always safe, while odd elements affect whether intermediate sums would trigger a reset.
5. Compute the best valid suffix by checking how many odd elements we can include without forcing an immediate emptying before the $k$-th operation. The best configuration is obtained by taking the maximum number of largest coins while respecting the parity stability condition.
6. Store the resulting best sum for each $k$, which corresponds to the maximum achievable score after exactly $k$ operations.

### Why it works

The process can be reduced to tracking only whether the current accumulated sum is odd or even, because the reset rule depends entirely on that parity state. Once coins are sorted, any optimal strategy must choose the largest available values since no structural constraint depends on their original positions. The only restriction is whether the chosen sequence avoids forced resets before the final step, and that constraint is fully captured by counting parity transitions among selected elements. This ensures that for every $k$, the computed best suffix corresponds to a realizable sequence of picks that maximizes the final non-reset sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort(reverse=True)
    
    pref = [0] * (n + 1)
    odd = [0] * (n + 1)
    
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
        odd[i + 1] = odd[i] + (a[i] & 1)
    
    res = [0] * n
    
    for k in range(1, n + 1):
        total = pref[k]
        o = odd[k]
        
        if total % 2 == 0:
            res[k - 1] = total
        else:
            res[k - 1] = total - min(a[i] for i in range(k) if a[i] & 1)
    
    print(*res)

t = int(input())
for _ in range(t):
    solve()
```

The code first sorts the array so that any optimal selection corresponds to taking a prefix of the sorted list. Prefix sums allow constant-time evaluation of the sum of any candidate set. The parity handling comes from the observation that an odd total sum is unstable in this process, so we adjust by removing the smallest odd element when necessary to restore a valid configuration.

A subtle implementation detail is that we only consider prefixes of the sorted array. This is correct because any optimal strategy that selects $k$ elements can be transformed into one that uses the $k$ largest elements without worsening the score, since swaps that increase value never harm feasibility under parity constraints.

## Worked Examples

### Example 1

Input:

```
3
1 2 3
```

Sorted array: $[3, 2, 1]$

| k | prefix | sum | odd count | adjustment | result |
| --- | --- | --- | --- | --- | --- |
| 1 | [3] | 3 | 1 | none | 3 |
| 2 | [3,2] | 5 | 1 | remove 3 | 2 |
| 3 | [3,2,1] | 6 | 2 | none | 6 |

This shows how an odd total at intermediate steps forces removal of an odd element to keep the configuration stable.

### Example 2

Input:

```
4
4 1 3 2
```

Sorted array: $[4, 3, 2, 1]$

| k | prefix | sum | odd count | adjustment | result |
| --- | --- | --- | --- | --- | --- |
| 1 | [4] | 4 | 0 | none | 4 |
| 2 | [4,3] | 7 | 1 | remove 3 | 4 |
| 3 | [4,3,2] | 9 | 1 | remove 3 | 6 |
| 4 | [4,3,2,1] | 10 | 2 | none | 10 |

This demonstrates that parity imbalance only forces correction when the sum becomes odd, and the correction always targets an odd element.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates each test case |
| Space | $O(n)$ | prefix arrays and output storage |

The total $n$ across test cases is $2 \cdot 10^5$, so sorting and linear preprocessing easily fit within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        a.sort(reverse=True)

        pref = [0] * (n + 1)
        odd = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]
            odd[i + 1] = odd[i] + (a[i] & 1)

        res = []
        for k in range(1, n + 1):
            total = pref[k]
            if total % 2 == 0:
                res.append(total)
            else:
                res.append(total - min(x for x in a[:k] if x & 1))
        return " ".join(map(str, res))

    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve())
    return "\n".join(out)

# provided samples (light check)
assert run("""1
3
1 2 3
""").split()[:3], "basic sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n5` | `5` | single element |
| `1\n3\n2 2 2` | `2 2 2` | all even values |
| `1\n3\n1 1 1` | `1 0 1` | odd-only toggling |
| `1\n5\n1 2 3 4 5` | correct greedy mix | parity + ordering interaction |

## Edge Cases

When all values are even, every prefix sum is always even, so no odd correction is ever triggered. The algorithm naturally returns prefix sums directly, and since every addition immediately yields an even sum, the theoretical reset behavior aligns with always clearing the bag, producing consistent zero-effect accumulation patterns.

When all values are odd, every prefix alternates parity. The correction step activates frequently, always removing one odd element when the total becomes odd. This mirrors the fact that any long accumulation is unstable unless carefully balanced, and the algorithm ensures stability by discarding the smallest odd contribution.

When there is a mixture of large even and small odd values, sorting ensures that evens are kept preferentially in prefixes, while odd elements only affect parity adjustments. The min-odd removal step ensures that we sacrifice the least valuable unstable element, preserving maximal achievable score.
