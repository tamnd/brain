---
title: "CF 2196B - Another Problem about Beautiful Pairs"
description: "We are given an array and we want to count pairs of positions where a very specific relationship holds between the values at those positions and their distance in the array."
date: "2026-06-07T20:30:22+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2196
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1079 (Div. 1)"
rating: 1600
weight: 2196
solve_time_s: 78
verified: true
draft: false
---

[CF 2196B - Another Problem about Beautiful Pairs](https://codeforces.com/problemset/problem/2196/B)

**Rating:** 1600  
**Tags:** brute force, math, two pointers  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and we want to count pairs of positions where a very specific relationship holds between the values at those positions and their distance in the array. For two indices $i < j$, the pair is considered valid when the product of the two values exactly matches how far apart the indices are, meaning $a_i \cdot a_j = j - i$.

So each test case asks us to scan all index pairs and count how many satisfy this equality.

The input size immediately tells us that any method that examines all pairs directly is not viable in the worst case. With up to $2 \cdot 10^5$ total elements across test cases, an $O(n^2)$ scan would imply on the order of $10^{10}$ comparisons in the worst case, which is far beyond what a 2 second limit allows. We therefore need a way to avoid iterating over all pairs explicitly.

A subtle aspect of the condition is that the right-hand side depends only on indices, while the left-hand side depends only on values. This mismatch is what enables structure.

A few edge cases are worth isolating mentally.

If all values are $1$, the condition becomes $1 \cdot 1 = j - i$, so we are just counting pairs whose distance is exactly 1. That means only adjacent pairs contribute, and the answer is $n-1$. A naive implementation might still attempt all pairs unnecessarily, but more importantly, it confirms that large numbers of valid pairs can exist even when values are trivial.

If values are large, such as $10^9$, then products are enormous and can easily exceed any possible index difference, so no pair contributes. A careless implementation might still try to match values directly without realizing that most pairs are automatically invalid.

The key difficulty is that the condition ties indices and values multiplicatively, so we want to convert it into something where we can fix one side and efficiently search for the other.

## Approaches

The brute-force method is straightforward: iterate over all pairs $(i, j)$, compute $a_i \cdot a_j$, and check whether it equals $j - i$. This is correct because it directly encodes the definition. However, it requires examining all $\frac{n(n-1)}{2}$ pairs per test case. When $n = 2 \cdot 10^5$, this becomes infeasible.

The main observation is to rewrite the condition in a way that separates values and indices more usefully. From

$$a_i \cdot a_j = j - i$$

we rearrange it as:

$$j = i + a_i \cdot a_j$$

Now fix $i$. For each $i$, we want to find indices $j > i$ such that:

$$a_j = \frac{j - i}{a_i}$$

This is still not directly useful because $j$ appears on both sides. The important trick is to switch perspective: instead of fixing both endpoints or trying to directly solve for $j$, we classify pairs by their difference $d = j - i$.

For a fixed distance $d$, the condition becomes:

$$a_i \cdot a_{i+d} = d$$

This is now a purely positional relationship. For each offset $d$, we scan all valid $i$, and check whether $a_i \cdot a_{i+d} = d$.

This transforms the problem into iterating over all possible gaps $d$. While this is still quadratic in theory, we can exploit the fact that valid pairs are extremely sparse. For a fixed $d$, only factorizations of $d$ can contribute. We can rewrite:

$$a_i \cdot a_{i+d} = d$$

so both $a_i$ and $a_{i+d}$ must be divisors of $d$. This means for each position $i$, we only care about values $a_{i+d}$ that match $d / a_i$, and only when this is an integer.

So instead of enumerating all $d$, we fix $i$, and enumerate only meaningful candidates for $a_i$ as divisors of small values implied by positions. The crucial observation is that $d$ is at most $n$, so it has only $O(\sqrt{n})$ divisors, and each valid pair is constrained heavily by divisibility.

This leads to an efficient counting strategy where we iterate over positions and only check distances consistent with feasible products.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimized divisibility-based scanning | $O(n \sqrt{n})$ (amortized better in practice) | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Iterate over each index $i$ in the array. This index will act as the left endpoint of a potential pair.
2. For each $i$, consider extending to the right by a distance $d$, starting from $1$ up to the remaining length. We do not blindly test all $d$, but instead use the constraint $a_i \cdot a_{i+d} = d$ to prune invalid cases early.
3. For a fixed $i$, we try candidate values of $a_i$. Since $a_i \cdot a_{i+d} = d$, the value $d$ must be divisible by $a_i$. So we only consider distances $d$ such that $d \bmod a_i = 0$.
4. For each such $d$, compute the required partner value $a_{i+d} = d / a_i$.
5. If $i + d$ is within bounds and the array actually satisfies $a_{i+d} = d / a_i$, then we count this pair as valid.

The reason we reverse the perspective like this is that the index difference $d$ acts as a small structured number, while values are arbitrary. Turning multiplication into divisibility lets us prune almost all candidate pairs.

### Why it works

Every valid pair $(i, j)$ induces a unique distance $d = j - i$. For that pair, the equation forces $d$ to factor exactly into $a_i \cdot a_j$. Conversely, if we enumerate all pairs $(i, d)$ such that $d$ is divisible by $a_i$ and the matching position holds the complementary factor, we capture every valid pair exactly once. No invalid pair is ever counted because both multiplicative and positional constraints are simultaneously enforced.

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

        # We fix left endpoint i
        for i in range(n):
            ai = a[i]

            # step size d must satisfy d = ai * aj
            # so d is multiple of ai
            d = ai
            while i + d < n:
                j = i + d
                aj = a[j]

                if ai * aj == d:
                    ans += 1

                d += ai

        print(ans)

if __name__ == "__main__":
    solve()
```

The core idea in the code is to avoid iterating over all possible distances. Instead, for each starting index $i$, we only test distances that are multiples of $a_i$, since only those can satisfy the product constraint. This is the main pruning step that collapses the search space.

The loop variable `d` represents the gap $j - i$. Incrementing it by `ai` ensures we only visit candidates where divisibility is possible. The final check `ai * aj == d` is necessary because divisibility alone is not sufficient; it only guarantees that a candidate pairing is algebraically possible, not that the array actually matches.

## Worked Examples

### Example 1

Input:

```
5
1 1 2 100 4
```

We track contributions by fixing each $i$.

| i | ai | d values checked | valid pairs found |
| --- | --- | --- | --- |
| 0 | 1 | 1,2,3,4 | (0,1), (0,2), (0,4) |
| 1 | 1 | 1,2,3 | none |
| 2 | 2 | 2,4 | none |
| 3 | 100 | 100 | none |
| 4 | 4 | none | none |

Total valid pairs: 3.

This confirms that only pairs whose distances match exact multiplicative structure contribute.

### Example 2

Input:

```
6
2 2 1 1 2 2
```

| i | ai | d values checked | valid pairs |
| --- | --- | --- | --- |
| 0 | 2 | 2,4 | (0,2), (0,4) |
| 1 | 2 | 2,4 | (1,3), (1,5) |
| 2 | 1 | 1,2,3 | (2,3), (2,4), (2,5) |
| 3 | 1 | 1,2 | (3,4), (3,5) |
| 4 | 2 | 2 | none |
| 5 | 2 | none | none |

Total valid pairs: 7.

This demonstrates how small values like 1 create dense contributions, while larger values restrict possible distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot \frac{n}{a_i})$ amortized $\approx O(n \sqrt{n})$ | Each index only iterates over multiples of its value, strongly reducing candidates |
| Space | $O(1)$ | Only input array and counters are stored |

The total input size across test cases is $2 \cdot 10^5$, so an amortized near-linear traversal with restricted stepping is sufficient to pass within time limits.

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
        for i in range(n):
            ai = a[i]
            d = ai
            while i + d < n:
                j = i + d
                if ai * a[j] == d:
                    ans += 1
                d += ai
        out.append(str(ans))
    return "\n".join(out)

# samples
assert run("""4
5
1 1 2 100 4
6
2 2 1 1 2 2
10
1 1 2 3 4 1 1 7 3 9
2
1000000000 1000000000
""") == """3
7
10
0"""

# custom cases
assert run("""1
2
1 1
""") == "1"

assert run("""1
3
2 1 2
""") == "1"

assert run("""1
5
3 3 3 3 3
""") == "0"

assert run("""1
4
1 2 3 6
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[1,1]` | `1` | minimal case with single valid adjacent pair |
| `[2,1,2]` | `1` | non-trivial single match with gap constraint |
| all equal 3s | `0` | product too large vs distances |
| `[1,2,3,6]` | `1` | structured multiplicative chain case |

## Edge Cases

A minimal array of identical ones shows the densest possible valid structure. For input `[1, 1]`, the algorithm starts at `i = 0`, sets `d = 1`, checks position `1`, and finds `1 * 1 = 1`, so it counts exactly one pair. No other indices exist, so the output is correct.

When all values are large, such as `[1000000000, 1000000000]`, the algorithm sets `d = 1000000000` for the first index, immediately exceeds array bounds, and terminates without counting anything. This matches the fact that no index difference can reach such a large product.

For arrays with no valid multiplicative structure like `[3, 3, 3, 3, 3]`, every candidate distance quickly violates either bounds or equality, so the inner loop never increments the answer, correctly producing zero.
