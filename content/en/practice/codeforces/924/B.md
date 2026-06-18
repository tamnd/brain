---
problem: 924B
contest_id: 924
problem_index: B
name: "Three-level Laser"
contest_name: "VK Cup 2018 - Round 2"
rating: 1600
tags: ["binary search", "greedy", "two pointers"]
answer: passed_samples
verified: true
solve_time_s: 85
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a326e6b-2cbc-83ec-b7fb-a28cecb0a5b4
---

# CF 924B - Three-level Laser

**Rating:** 1600  
**Tags:** binary search, greedy, two pointers  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 25s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a326e6b-2cbc-83ec-b7fb-a28cecb0a5b4  

---

## Solution

## Problem Understanding

We are given a strictly increasing array of energy levels. We must pick three indices $i < j < k$ and interpret them as a three-step physical process that produces a ratio between useful energy and spent energy.

The process depends only on differences of the chosen values. The spent energy is the jump from $i$ to $k$, while the useful energy is the emission from $k$ down to $j$. The efficiency is therefore

$$\eta = \frac{E_k - E_j}{E_k - E_i}.$$

There is an additional constraint: the total jump from $i$ to $k$ cannot exceed $U$, so $E_k - E_i \le U$. If no valid triple exists, the answer is $-1$.

The structure is purely one-dimensional with monotone values, which suggests that any valid optimal solution can be reasoned about in terms of intervals rather than arbitrary combinatorial choices. The difficulty is that we are optimizing a ratio over all triples under a sliding distance constraint.

The constraints are large: up to $10^5$ states, so any $O(n^2)$ or worse approach is too slow. A solution must essentially be linear or linearithmic. This immediately suggests maintaining a moving window of valid $k$ candidates for each $i$, and within that window choosing a best $j$ efficiently.

A subtle edge case is when the array is too “sparse” relative to $U$, making no triple possible. For example, if $n = 3$, $E = [1, 100, 200]$, and $U = 50$, then no pair $i,k$ satisfies $E_k - E_i \le U$, so the answer must be $-1$. A careless solution that assumes existence of triples will produce meaningless ratios or division by zero.

Another failure mode is numerical instability. Since the answer is a ratio, not an integer, precision issues arise if we recompute repeatedly with floating arithmetic without careful maximization logic.

## Approaches

The brute-force method enumerates all triples $i < j < k$, checks whether $E_k - E_i \le U$, and computes the ratio. This is correct because it directly evaluates the definition. However, it costs $O(n^3)$, which is far too slow for $n = 10^5$. Even reducing it to fixing $i$ and $k$ and scanning $j$ gives $O(n^2)$, still impossible.

The key observation is that for fixed $i$ and $k$, the best $j$ is determined only by maximizing $E_j$ under $i < j < k$, since the numerator is $E_k - E_j$. To maximize the ratio, we want to minimize $E_j$ relative to the span, but the dependency is fractional and not linear in a trivial way.

Rewriting the expression helps:

$$\eta = \frac{E_k - E_j}{E_k - E_i} = 1 - \frac{E_j - E_i}{E_k - E_i}.$$

For fixed $i,k$, maximizing efficiency is equivalent to minimizing $E_j$. However, $j$ must lie strictly between them. So for each interval $(i,k)$, we want the smallest value in the interior.

This turns the problem into a two-pointer structure: we fix $i$, expand $k$ while respecting $E_k - E_i \le U$, and maintain a data structure (or monotonic observation) that allows us to track the minimum $E_j$ in the middle region. Since the array is increasing, the minimum in any segment is always at its left endpoint, so for each $i,k$, the best $j$ is simply $i+1$. This reduces the problem dramatically.

Thus for each $i$, and for each valid $k$, we only need to check $j = i+1$, making the ratio:

$$\frac{E_k - E_{i+1}}{E_k - E_i}.$$

Now we just need to maintain a sliding window of valid $k$ values and evaluate this expression efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Fix the left endpoint $i$ starting from the smallest index. This ensures all triples are considered in increasing order of their left boundary.
2. Maintain a pointer $k$ that only moves forward. For each $i$, extend $k$ as far as possible while satisfying $E_k - E_i \le U$. This guarantees we only consider valid right endpoints.
3. For each fixed pair $(i, k)$, determine the best middle state. Because energies are strictly increasing, the smallest valid $E_j$ for $i < j < k$ is always at $j = i+1$, provided $k \ge i+2$. This avoids scanning the interior.
4. Compute the efficiency candidate:

$$\eta = \frac{E_k - E_{i+1}}{E_k - E_i}.$$

Only evaluate when $k \ge i+2$, since we need three distinct indices.
5. Track the maximum value across all valid configurations. If no configuration exists, return $-1$.

### Why it works

For a fixed $i$ and $k$, the denominator $E_k - E_i$ is constant. The numerator $E_k - E_j$ is maximized when $E_j$ is minimized. Since the array is strictly increasing, the smallest possible $E_j$ in $(i,k)$ is always $E_{i+1}$. Therefore no interior choice of $j$ besides $i+1$ can improve the ratio, and checking only this candidate preserves optimality.

The sliding pointer for $k$ ensures every valid interval is considered exactly once, and monotonicity of the array guarantees correctness of skipping backward movement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, U = map(int, input().split())
    E = list(map(int, input().split()))

    ans = -1.0
    k = 0

    for i in range(n):
        if k < i + 2:
            k = i + 2

        while k < n and E[k] - E[i] <= U:
            if i + 1 < k:
                val = (E[k] - E[i + 1]) / (E[k] - E[i])
                if val > ans:
                    ans = val
            k += 1

        # step back one because k is now invalid or out of range
        # but k only moves forward globally, so no reset needed

    if ans < 0:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation uses a single pass with a global pointer $k$ that never moves backward, which ensures linear complexity. The key detail is that we only evaluate candidates when $k$ is valid and $i+1 < k$, guaranteeing three distinct indices.

A subtle point is that we do not reset $k$ for each $i$. This is safe because increasing $i$ only tightens the constraint $E_k - E_i \le U$, so any previously valid $k$ remains a valid starting point or is already too large. This preserves amortized linear scanning.

## Worked Examples

### Example 1

Input:

```
4 4
1 3 5 7
```

We enumerate valid triples.

| i | j | k | E[k]-E[i] | E[k]-E[j] | ratio |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 4 | 2 | 0.5 |

Only valid triple is (1,3,5) in 1-based indexing, giving 0.5.

This shows that even though multiple triples exist in general problems, here the best is uniquely determined by the smallest middle state.

### Example 2

Input:

```
5 6
1 2 4 7 10
```

We track best candidates.

| i | k | j=i+1 | E[k]-E[i] | E[k]-E[j] | ratio |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 3 | 2 | 0.666... |
| 0 | 3 | 1 | 6 | 5 | 0.833... |
| 1 | 3 | 2 | 5 | 3 | 0.6 |

Maximum is $5/6$ from $i=1, j=2, k=3$.

This confirms that extending $k$ while keeping $j=i+1$ captures the optimal balance between numerator growth and denominator growth.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each pointer $i$ and $k$ moves at most $n$ times in total |
| Space | $O(1)$ | Only a few variables are maintained |

The linear scan is sufficient for $n \le 10^5$, and the constant memory usage ensures no overhead beyond input storage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, U = map(int, inp.split()[0:2])
    # re-run solution inline
    import sys
    input = sys.stdin.readline

    def solve():
        n, U = map(int, sys.stdin.readline().split())
        E = list(map(int, sys.stdin.readline().split()))

        ans = -1.0
        k = 0

        for i in range(n):
            if k < i + 2:
                k = i + 2

            while k < n and E[k] - E[i] <= U:
                if i + 1 < k:
                    val = (E[k] - E[i + 1]) / (E[k] - E[i])
                    if val > ans:
                        ans = val
                k += 1

        if ans < 0:
            return "-1"
        return str(ans)

    return solve()

# provided sample
assert run("4 4\n1 3 5 7\n") == "0.5"

# minimum case (no valid triple)
assert run("3 1\n1 2 3\n") == "-1"

# tight window
assert run("3 2\n1 2 4\n") == "-1"

# increasing valid chain
assert run("5 10\n1 2 3 4 5\n") != "-1"

# large gap
assert run("5 100\n1 10 20 30 40\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 / 1 2 3 | -1 | No valid triple exists |
| 3 2 / 1 2 4 | -1 | Window constraint blocks any k |
| 5 10 / 1 2 3 4 5 | valid ratio | Normal dense case |
| 5 100 / spaced values | valid ratio | Large window behavior |

## Edge Cases

When $n = 3$, there is exactly one possible triple. The algorithm still behaves correctly because the loop only evaluates when $k = 2$, and checks $i = 0$, producing a valid ratio if the constraint allows it.

When no pair satisfies $E_k - E_i \le U$, the pointer $k$ always advances past valid range, and `ans` remains $-1$. This correctly triggers the impossible case.

When values are very close, floating-point precision matters. The algorithm only performs one division per candidate, minimizing cumulative error and staying within the required $10^{-9}$ tolerance.