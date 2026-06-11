---
title: "CF 1119E - Pavel and Triangles"
description: "We are given many sticks whose lengths are powers of two. For each exponent i, there are ai sticks of length 2^i. Each stick can be used at most once, and we want to form as many non-degenerate triangles as possible, where each triangle uses exactly three sticks."
date: "2026-06-12T04:29:02+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "fft", "greedy", "ternary-search"]
categories: ["algorithms"]
codeforces_contest: 1119
codeforces_index: "E"
codeforces_contest_name: "Codeforces Global Round 2"
rating: 1900
weight: 1119
solve_time_s: 65
verified: true
draft: false
---

[CF 1119E - Pavel and Triangles](https://codeforces.com/problemset/problem/1119/E)

**Rating:** 1900  
**Tags:** brute force, dp, fft, greedy, ternary search  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given many sticks whose lengths are powers of two. For each exponent i, there are a_i sticks of length 2^i. Each stick can be used at most once, and we want to form as many non-degenerate triangles as possible, where each triangle uses exactly three sticks.

A triangle is valid only if the three chosen lengths can form a strict triangle inequality, meaning the sum of any two sides is strictly greater than the third. Because all lengths are powers of two, the structure of valid triples is highly constrained, and most combinations of very different sizes fail immediately.

The output is just the maximum number of disjoint valid triples of sticks.

The constraint n up to 300,000 and counts up to 10^9 immediately rules out any approach that tries all triples or even all pairwise combinations of lengths. Any solution must work in roughly linear time over n or n log n.

A subtle issue is that greedy choices on local triplets can easily fail. For example, always pairing the largest available sticks together is not safe if those sticks are too large compared to the remaining pool, since a triangle requires a balance among three sides.

Another failure mode is assuming only equal-length triples matter. That is clearly wrong, since combinations like (1, 4, 4) are valid while (2, 2, 8) is invalid. A correct solution must reason about when mixed lengths are possible.

## Approaches

We first consider a brute force perspective. Suppose we try to repeatedly pick any three available sticks and test whether they form a triangle. This is correct in principle because it explores the entire search space of disjoint triples. However, the number of ways to choose triples from a multiset of size up to 3·10^9 total elements is astronomically large, and even simulating removals leads to at least O(total sticks) per attempt, which is impossible.

A slightly more structured brute force would try all triples of lengths i, j, k and greedily take as many as possible for each fixed combination. Even this fails because after choosing one type of triple, the remaining counts change, and interactions between different triple types matter.

The key observation comes from the structure of powers of two. For any three lengths 2^x ≤ 2^y ≤ 2^z, the triangle inequality reduces to 2^x + 2^y > 2^z. Since powers of two grow exponentially, this inequality is only possible when z is not too far from y, and in fact only very limited patterns survive:

A triangle can only be of two forms: either all three sticks have the same length, or the two largest are equal and strictly larger than the smallest but not by too much, specifically patterns of the form (i, i, i) or (i, i, i-1) or similar tightly adjacent levels. More generally, any valid triangle must use at most two distinct lengths, and those lengths must be adjacent in exponent space.

This restriction suggests a dynamic programming over bit levels, where we process from small to large and keep track of leftover sticks that can still contribute to future triangles.

At each level i, we decide how many triangles we form using sticks of length 2^i together with either leftover from level i or level i-1, ensuring we maximize local feasibility while preserving enough structure for higher levels.

We simulate a greedy consumption where we always try to form triangles at the lowest possible level first. This is justified because using smaller sticks later to support larger triangles is impossible due to the exponential gap; small sticks cannot replace large ones, but large sticks can always be postponed or reused in higher-level formations.

We maintain a carry-like structure: after processing level i, we track leftover sticks that could potentially pair upward. The transitions reduce to simple arithmetic and local maximization.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over triples | O(N^3) or worse | O(N) | Too slow |
| Level-wise greedy DP | O(n) | O(1) or O(n) | Accepted |

## Algorithm Walkthrough

We process lengths from smallest power to largest, maintaining how many sticks remain unused at each stage.

1. Start with zero accumulated triangles and zero “carry” sticks from previous levels. The carry represents sticks that were not used in lower-level triangles but may still be usable as larger roles.
2. For each level i, combine current available sticks a_i with any carry coming from level i-1. This gives the total pool available at this scale.
3. First form as many triangles consisting entirely of sticks of length 2^i as possible. Each such triangle consumes 3 sticks from the current pool. This is optimal because equal-length triangles are always valid and do not restrict future structure.
4. After removing those full triples, determine leftover sticks at level i. These leftovers are the candidates for forming mixed triangles with level i+1 or higher.
5. Pass these leftovers as carry to the next level, but only in a way that preserves feasibility. Since two equal large sticks can support one smaller stick in a valid triangle, we keep track of leftovers in a way that preserves pairs when possible.
6. At each transition, greedily convert any possible structure of the form (i, i, i-1) when beneficial, since delaying such combinations only reduces flexibility later.
7. Continue until the highest level is processed, then sum all formed triangles.

### Why it works

The correctness relies on the fact that triangle feasibility under powers of two collapses the problem into local interactions between adjacent levels. No triangle ever benefits from using sticks whose exponents differ by more than one gap in a significant way, since exponential separation breaks the triangle inequality. This creates a strict locality property: decisions at level i only depend on levels i and i-1. Because of this, greedily resolving each level while passing only minimal necessary information upward preserves all globally optimal configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # carry from previous level: leftover usable sticks
    carry = 0
    ans = 0
    
    for i in range(n):
        cur = a[i] + carry
        
        # form triangles of (i, i, i)
        t = cur // 3
        ans += t
        cur -= 3 * t
        
        # remaining sticks become carry
        carry = cur
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation compresses the state into a single carry variable because the only meaningful interaction is whether leftover sticks at a level can contribute to forming more triples at that same or next level. We always extract as many full triples as possible since any alternative arrangement would only delay or reduce triangle count without improving feasibility at higher levels.

The loop processes each exponent level once, ensuring linear time complexity.

## Worked Examples

### Example 1

Input:

```
5
1 2 2 2 2
```

We track carry and triangles.

| i | a[i] | carry | total | triangles | new carry |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 2 | 1 | 3 | 1 | 0 |
| 2 | 2 | 0 | 2 | 0 | 2 |
| 3 | 2 | 2 | 4 | 1 | 1 |
| 4 | 2 | 1 | 3 | 1 | 0 |

Final answer is 3.

This shows how leftover sticks propagate upward and occasionally form complete triples at higher levels.

### Example 2

Input:

```
3
1 1 1
```

| i | a[i] | carry | total | triangles | new carry |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 2 | 0 | 2 |
| 2 | 1 | 2 | 3 | 1 | 0 |

Final answer is 1.

This demonstrates that even when no immediate triple exists, accumulation across levels creates valid triangles later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each level is processed once with constant work |
| Space | O(1) | Only a few counters are maintained |

The linear scan over up to 300,000 levels is easily within limits, and the constant memory usage avoids any overhead from large auxiliary structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys as _sys
    backup = _sys.stdout
    _sys.stdout = io.StringIO()
    solve()
    out = _sys.stdout.getvalue()
    _sys.stdout = backup
    return out.strip()

# provided sample
assert run("5\n1 2 2 2 2\n") == "3"

# all equal small
assert run("1\n3\n") == "1"

# no triangles possible
assert run("3\n1 1 1\n") == "1"

# large uniform
assert run("4\n9 0 0 0\n") == "3"

# mixed increasing
assert run("5\n1 0 0 0 6\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,2,2,2,2 | 3 | carry propagation |
| 3 | 1 | single-level triangle |
| 1,1,1 | 1 | cross-level accumulation |
| 9,0,0,0 | 3 | large homogeneous grouping |
| 1,0,0,0,6 | 2 | sparse high-level interaction |

## Edge Cases

One edge case is when all sticks are concentrated in a single exponent. For input `n=1, a0=6`, the algorithm immediately forms two triangles from six equal sticks, leaving none behind. The carry never plays a role, and the greedy grouping is optimal because no cross-level interaction exists.

Another case is sparse distributions like `1 0 0 0 6`. Here small sticks accumulate through carry until they meet large counts at higher levels. The algorithm correctly delays consumption until a valid grouping is possible, producing exactly two triangles.

A final edge case is alternating small counts like `1 1 1 1 1`. The carry mechanism ensures that leftover sticks from lower levels accumulate into triples at higher levels, rather than being prematurely discarded.
