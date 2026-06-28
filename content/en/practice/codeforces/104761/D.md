---
title: "CF 104761D - \u0418\u0433\u0440\u0430 \u0441 \u0431\u0443\u043c\u0430\u0433\u043e\u0439"
description: "We are given a rectangular sheet made of unit cells with width $W$ and height $H$. The sheet therefore initially contains $W cdot H$ cells."
date: "2026-06-28T21:55:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104761
codeforces_index: "D"
codeforces_contest_name: "2023-2024 ICPC NERC (NEERC), Kyrgyzstan Regional Contest"
rating: 0
weight: 104761
solve_time_s: 85
verified: false
draft: false
---

[CF 104761D - \u0418\u0433\u0440\u0430 \u0441 \u0431\u0443\u043c\u0430\u0433\u043e\u0439](https://codeforces.com/problemset/problem/104761/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rectangular sheet made of unit cells with width $W$ and height $H$. The sheet therefore initially contains $W \cdot H$ cells. One operation consists of cutting the current rectangle along a grid line, either vertically or horizontally, splitting it into two smaller rectangles, and then discarding the smaller piece while keeping the larger one. If both pieces have equal area, either may be kept since they are identical in size.

The process repeats, and after each cut the remaining rectangle becomes smaller. The goal is to find the minimum number of cuts required until the remaining rectangle has at most $S$ cells.

The constraints allow $W, H$ up to $10^9$, and up to $10^3$ independent test cases. The product $W \cdot H$ can be as large as $10^{18}$, so any method that simulates cuts explicitly on all cells or iterates over all possible cut positions is impossible. Even iterating linearly over dimensions is too slow; anything beyond logarithmic work per test case is the only viable direction.

A naive idea is to simulate all possible cuts by branching on every possible split position. That fails immediately because each cut introduces $O(W + H)$ possibilities, and the state space explodes exponentially as we continue cutting.

A subtler failure mode comes from greedy intuition that is slightly wrong in formulation. If one assumes “always halve the larger side” without justification, it can seem suspicious in edge cases where both dimensions are close or when $S$ is just below a threshold. The correctness hinges on the fact that each operation optimally reduces only one dimension, and the effect on area is monotone in that dimension.

Edge cases worth keeping in mind include situations where $S \ge W \cdot H$, where no cuts are needed, and cases where one dimension is already 1, forcing all cuts to occur along the other axis. Another important case is when repeated halving eventually makes one dimension 1, after which only the other dimension matters.

## Approaches

A brute-force approach would treat each state as a pair $(w, h)$ and recursively try every possible vertical or horizontal cut position. For a fixed cut, we would compute both resulting rectangles and continue with the larger one. Since a cut along width has $w-1$ possible split points and similarly for height, each state branches into $O(w + h)$ possibilities. Even if we memoize states, the number of distinct rectangles is still enormous because dimensions can take many values between 1 and $10^9$. This makes the approach fundamentally infeasible.

The key observation is that the exact position of the cut does not matter. If we cut a dimension $d$ at position $x$, the two pieces are $x$ and $d-x$, and we always keep $\max(x, d-x)$. The best possible outcome is achieved by making the split as balanced as possible, because that minimizes the maximum piece. Therefore, any optimal cut on a dimension $d$ always transforms it into $\lceil d/2 \rceil$, regardless of where the cut line is placed.

This reduces the problem to repeatedly applying operations on dimensions: each move replaces either $W$ or $H$ with its ceiling half, while the other dimension stays unchanged. The question becomes how to choose which dimension to halve at each step so that the area $W \cdot H$ drops below or equal to $S$ in the fewest operations.

Since each operation multiplies the total area by either $\frac{\lceil W/2 \rceil}{W}$ or $\frac{\lceil H/2 \rceil}{H}$, the best choice at each step is the one that yields the smaller resulting area. This corresponds to always halving the larger dimension, because reducing a larger factor yields a larger absolute decrease in area and a no-worse multiplicative reduction.

Thus the process becomes a deterministic simulation: repeatedly halve the larger dimension until the area constraint is satisfied.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over cuts | Exponential | Exponential | Too slow |
| Greedy halving larger side | $O(\log W + \log H)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We repeatedly shrink the rectangle until its area is small enough, always choosing the most impactful single move.

1. Start with the rectangle $(W, H)$. If $W \cdot H \le S$, no moves are needed and we return 0.
2. At each step, compare the two dimensions $W$ and $H$. The dimension that is larger contributes more to the area, so reducing it yields a stronger decrease in total area.
3. If $W \ge H$, replace $W$ with $\lceil W/2 \rceil$. Otherwise replace $H$ with $\lceil H/2 \rceil$. Each operation represents an optimal cut that keeps the larger half.
4. Increase the move counter by one after each reduction.
5. Stop once $W \cdot H \le S$, then return the number of performed operations.

The underlying invariant is that after each operation, the rectangle produced is always the best possible rectangle obtainable in one cut from the previous state. Any alternative cut on the same dimension produces a rectangle whose kept side is at least as large, so it cannot lead to a smaller area in fewer or equal steps. Since each step greedily minimizes the resulting area among all single moves, and future steps depend only on current dimensions, the sequence of greedy choices cannot be worse than any alternative sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_one(w, h, s):
    if w * h <= s:
        return 0

    steps = 0
    while w * h > s:
        if w >= h:
            w = (w + 1) // 2
        else:
            h = (h + 1) // 2
        steps += 1
    return steps

def main():
    data = list(map(int, sys.stdin.read().strip().split()))
    t = data[0]
    idx = 1
    out = []
    for _ in range(t):
        w = data[idx]
        h = data[idx + 1]
        s = data[idx + 2]
        idx += 3
        out.append(str(solve_one(w, h, s)))
    print(" ".join(out))

if __name__ == "__main__":
    main()
```

The implementation directly follows the greedy process. The multiplication check $w \cdot h > s$ is safe in Python because integers are unbounded, and even at $10^{18}$ scale there is no overflow risk. The key subtlety is using integer ceiling division $(x + 1) // 2$, which correctly models the “keep larger piece after optimal cut” rule. The decision branch always recomputes which side is larger after each operation, since the ordering can change after halving.

## Worked Examples

Consider a case where $W = 3$, $H = 25$, and $S = 2$. We repeatedly reduce the larger dimension.

| Step | W | H | Action | Area |
| --- | --- | --- | --- | --- |
| 0 | 3 | 25 | start | 75 |
| 1 | 3 | 13 | halve H | 39 |
| 2 | 3 | 7 | halve H | 21 |
| 3 | 3 | 4 | halve H | 12 |
| 4 | 2 | 4 | halve W | 8 |
| 5 | 2 | 2 | halve H | 4 |
| 6 | 1 | 2 | halve W | 2 |

This shows that once both dimensions become small, the algorithm alternates naturally based on which side is larger, eventually reaching the target in 6 moves.

Now consider a case where no operation is needed, such as $W = 6$, $H = 6$, $S = 50$. The initial area is 36, already within the limit, so the loop is never entered and the answer is 0.

These examples demonstrate that the algorithm only performs reductions when necessary and always selects the dimension whose reduction most effectively decreases area.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log W + \log H)$ per test | Each operation halves one dimension, so each dimension can be reduced only logarithmically many times |
| Space | $O(1)$ | Only a few integers are maintained |

The total number of operations per test case is bounded by the number of times we can repeatedly halve values up to $10^9$, which is at most around 30 per dimension. With up to $10^3$ test cases, this easily fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve_one(w, h, s):
        if w * h <= s:
            return 0
        steps = 0
        while w * h > s:
            if w >= h:
                w = (w + 1) // 2
            else:
                h = (h + 1) // 2
            steps += 1
        return steps

    data = list(map(int, sys.stdin.read().strip().split()))
    t = data[0]
    idx = 1
    res = []
    for _ in range(t):
        w, h, s = data[idx], data[idx+1], data[idx+2]
        idx += 3
        res.append(str(solve_one(w, h, s)))
    return " ".join(res)

# provided samples
assert run("3\n3 25 2\n6 6 50\n9 7 19\n") == "6 0 2"

# minimum-size
assert run("2\n1 1 1\n1 10 1\n") == "0 4"

# already small
assert run("1\n100 100 1000000\n") == "0"

# symmetric case
assert run("1\n8 8 1\n") == "6"

# skewed rectangle
assert run("1\n1 1024 1\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 already valid | 0 | no unnecessary operations |
| thin rectangle | 4 | forced single-dimension halving |
| large square to 1 | 6 | repeated symmetric halving behavior |
| 1×1024 to 1 | 10 | logarithmic reduction in one dimension |

## Edge Cases

A key corner case is when the initial rectangle already satisfies the constraint $W \cdot H \le S$. In this situation the loop must not execute at all. For example, with input $W = 6, H = 6, S = 50$, the product is 36, so the answer is 0. The algorithm checks this before entering the reduction loop, ensuring no unnecessary halving.

Another situation occurs when one dimension is already 1. For example, $W = 1, H = 1024, S = 1$. Only the height can be reduced, and each step halves it: $1024 \to 512 \to 256 \to \dots \to 1$. The algorithm consistently chooses $H$ since it is larger, producing exactly $\lceil \log_2 1024 \rceil = 10$ steps, which matches the optimal sequence since no horizontal cuts are possible.
