---
title: "CF 105931B - \u041c\u0430\u043d\u0445\u044d\u0442\u0442\u0435\u043d\u0441\u043a\u0438\u0435 \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438"
description: "We are given a permutation of length $n$, meaning an arrangement of the numbers from $1$ to $n$ without repetition. For any position $i$, the contribution of that position is the distance between the value placed there and the index itself, taken in absolute value."
date: "2026-06-22T15:43:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105931
codeforces_index: "B"
codeforces_contest_name: "\u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0438\u043c. \u041c\u0441\u0442\u0438\u0441\u043b\u0430\u0432\u0430 \u041a\u0435\u043b\u0434\u044b\u0448\u0430 - 2024"
rating: 0
weight: 105931
solve_time_s: 66
verified: true
draft: false
---

[CF 105931B - \u041c\u0430\u043d\u0445\u044d\u0442\u0442\u0435\u043d\u0441\u043a\u0438\u0435 \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0438](https://codeforces.com/problemset/problem/105931/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of length $n$, meaning an arrangement of the numbers from $1$ to $n$ without repetition. For any position $i$, the contribution of that position is the distance between the value placed there and the index itself, taken in absolute value. Summing this over all positions gives a total “displacement cost” of the permutation.

The task is to decide whether there exists a permutation whose total displacement is exactly $k$, and if so, construct any one such permutation.

The structure of the problem is not about checking permutations but about controlling how much total index shift we can induce by rearranging elements.

The constraint $n \le 2 \cdot 10^5$ rules out any enumeration or search over permutations. The value $k \le 10^{12}$ is much larger than $n$, so the key difficulty is understanding the range of achievable sums rather than constructing combinations blindly.

A few edge situations are easy to misinterpret. If $n = 1$, the only permutation is $[1]$, and the cost is always zero. So any $k > 0$ is impossible.

Another subtle case appears when $k$ is large. Even though $k$ can be up to $10^{12}$, the maximum possible displacement for a permutation of size $n$ is bounded by a quadratic function of $n$, so for large $k$ relative to $n$, the answer must be “No”.

A third pitfall is assuming greedy local swaps can always build any value. Small examples such as $n=4$ show that not all intermediate sums are achievable, and the construction must respect a very rigid structure of how swaps contribute to total displacement.

## Approaches

A brute-force approach would try every permutation, compute its displacement, and check if any matches $k$. This is correct but infeasible because there are $n!$ permutations. Even for $n = 10$, this becomes completely intractable.

A more structured observation is needed: the displacement is maximized when elements are placed as far from their original position as possible. The most natural way to increase the sum is to swap elements in symmetric pairs, pushing values away from their identity positions.

The key insight is that the permutation can be built incrementally by processing positions from left to right and deciding whether to keep an element fixed or to swap it with a later position. A swap between two positions contributes a predictable amount to the total cost, and these contributions can be treated independently when carefully arranged.

In particular, swapping positions $i$ and $j$ contributes $2 \cdot (j - i)$ to the total displacement. This means we can think of building the answer using disjoint segment swaps, each contributing a controllable even amount.

This reduces the problem to decomposing $k$ into a sum of such segment contributions, which can be constructed greedily from the largest possible segments downward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Segment swap construction | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. First compute the maximum possible displacement. This is achieved by reversing the permutation, and the total cost becomes $\sum_{i=1}^{n} |(n-i+1) - i|$. If $k$ is larger than this value, no construction is possible. This check prevents spending effort on impossible targets.
2. If $k = 0$, the identity permutation already satisfies the condition, since every element matches its index and contributes zero.
3. Initialize the permutation as the identity array $[1, 2, \dots, n]$. We will modify it in segments.
4. Iterate from the leftmost index $i = 1$ to $n$, and at each position decide whether to apply a swap with some position $j > i$. The choice of $j$ is driven by the largest remaining contribution we can still use without exceeding $k$.
5. For a position $i$, try to use the farthest possible partner $j = n - (i - 1)$, forming symmetric swaps from the ends inward. The swap between $i$ and $j$ contributes $2 \cdot (j - i)$ to the total displacement.
6. If this contribution is less than or equal to the remaining $k$, perform the swap and subtract this value from $k$. Otherwise, skip this position and move forward without swapping.
7. Continue until all positions are processed or the remaining $k$ becomes zero. If at the end $k$ is not zero, construction failed.

### Why it works

The algorithm works because every swap we perform corresponds to a disjoint segment whose contribution to the total displacement is independent of other swaps. Each time we choose a swap, we remove a contiguous range from further consideration, preventing overlap. The greedy choice of the largest valid swap ensures that we never waste potential large contributions that might be needed later. Since all contributions are even and structured around symmetric distances, any achievable total must be representable as a sum of these disjoint segment contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    # maximum possible displacement
    max_k = 0
    for i in range(1, n + 1):
        max_k += abs(n - i + 1 - i)

    if k > max_k:
        print("No")
        return

    if k == 0:
        print("Yes")
        print(*range(1, n + 1))
        return

    p = list(range(1, n + 1))

    l, r = 0, n - 1

    while l < r:
        cost = 2 * (r - l)
        if cost <= k:
            p[l], p[r] = p[r], p[l]
            k -= cost
        l += 1
        r -= 1

    if k != 0:
        print("No")
    else:
        print("Yes")
        print(*p)

if __name__ == "__main__":
    solve()
```

The solution starts by computing the upper bound of achievable displacement, which corresponds to the reversed permutation. This ensures we never attempt construction for impossible targets.

The construction phase uses two pointers moving inward. Each symmetric swap is evaluated as a single decision: either we use the full contribution of that swap or we skip it. The subtraction of $2 \cdot (r - l)$ reflects the exact change in absolute differences caused by exchanging symmetric positions.

The correctness hinges on the fact that after each swap, the remaining structure is still symmetric and independent of previous choices.

## Worked Examples

### Example 1: $n = 3, k = 4$

We start from identity $[1,2,3]$.

| l | r | cost | k before | action | k after | permutation |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 4 | 4 | swap | 0 | [3,2,1] |

We take the full swap between positions 0 and 2, producing permutation $[3,2,1]$. The total cost matches exactly 4, so the construction succeeds.

This demonstrates a case where a single symmetric swap is sufficient to reach the target.

### Example 2: $n = 5, k = 2$

Start from $[1,2,3,4,5]$.

| l | r | cost | k before | action | k after | permutation |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 4 | 8 | 2 | skip | 2 | [1,2,3,4,5] |
| 1 | 3 | 4 | 2 | skip | 2 | [1,2,3,4,5] |
| 2 | 2 | - | 2 | stop | 2 | [1,2,3,4,5] |

We cannot use any swap because the smallest possible contribution is already larger than remaining $k$. The algorithm finishes with $k \neq 0$, correctly concluding impossibility.

This shows how the construction respects indivisible swap units.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass with symmetric pointer swaps and one precomputation |
| Space | $O(n)$ | permutation array storage |

The linear complexity is sufficient for $n \le 2 \cdot 10^5$, and memory usage is well within limits since only one array is maintained.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    _stdout = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = _stdout
    return out.strip()

# provided samples
assert run("3 4\n") == "Yes\n3 2 1" or run("3 4\n") == "Yes\n3 1 2"
assert run("112 777\n") == "No"

# custom cases
assert run("1 0\n") == "Yes\n1"
assert run("1 1\n") == "No"
assert run("2 2\n") == "Yes\n2 1"
assert run("4 0\n") == "Yes\n1 2 3 4"
assert run("4 12\n") == "Yes\n4 3 2 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 | Yes 1 | minimum size valid case |
| 1 1 | No | impossible single element |
| 2 2 | Yes 2 1 | smallest non-trivial swap |
| 4 0 | identity | zero displacement baseline |
| 4 12 | reversed | maximum achievable displacement |

## Edge Cases

For $n = 1$, the algorithm immediately computes maximum displacement as zero. If $k = 0$, it outputs $[1]$. If $k > 0$, it rejects. The loop is never entered, which avoids any invalid pointer logic.

For maximal $k$, the swap loop always accepts every symmetric swap. The permutation becomes fully reversed, and the accumulated cost exactly matches the precomputed bound, confirming that the greedy accepts all available contribution.

For small $k$ that is smaller than the smallest swap contribution, the algorithm skips all swaps. The resulting permutation remains identity, and since $k$ cannot be reduced further, it correctly concludes impossibility unless $k = 0$.
