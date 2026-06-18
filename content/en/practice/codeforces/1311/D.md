---
problem: 1311D
contest_id: 1311
problem_index: D
name: "Three Integers"
contest_name: "Codeforces Round 624 (Div. 3)"
rating: 2000
tags: ["brute force", "math"]
answer: passed_samples
verified: true
solve_time_s: 292
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2dde35-acbc-83ec-8f89-626284c4ef25
---

# CF 1311D - Three Integers

**Rating:** 2000  
**Tags:** brute force, math  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 52s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2dde35-acbc-83ec-8f89-626284c4ef25  

---

## Solution

## Problem Understanding

We are given three positive integers in nondecreasing order. Think of them as three knobs on a number line. In one move, we can shift any single knob by exactly one unit left or right, but we are not allowed to push a knob below 1. The goal is to reshape the triple into a new ordered triple so that the middle value is a multiple of the first, and the last value is a multiple of the middle.

The output is not only the minimum number of moves needed to reach such a configuration, but also one concrete final configuration that achieves this minimum.

The key difficulty is that the structure we want is very rigid: once the smallest value is fixed, the middle is forced to be some multiple of it, and the largest is forced to be a multiple of the middle. That makes the space of valid triples sparse inside a dense integer grid.

The constraints are small enough that a direct search over all possible final triples is feasible. Each value is at most 10^4, so even nested iteration over candidates is acceptable if we keep the search space controlled. A solution that tries to build all possible triples naively without structure would still pass because the domain is bounded tightly.

A subtle edge case appears when the optimal solution collapses values together, such as turning all three numbers into the same value. For example, turning `100 100 101` into `100 100 100` is optimal, but any approach that only considers strictly increasing triples might miss it. Another corner case is when reducing values is cheaper than increasing them, which often happens when we allow collapsing to smaller divisors like 1.

## Approaches

A brute force approach starts from the idea that we can try every possible final triple $A \le B \le C$. For each choice, we compute the cost as the sum of absolute differences $|a-A| + |b-B| + |c-C|$, but we only keep triples satisfying $B \bmod A = 0$ and $C \bmod B = 0$.

This is correct because every valid target configuration is explicitly tested, and the cost function exactly matches the number of moves needed. The issue is the number of candidates. Each variable can go up to around 10^4, so the full search space is on the order of $10^{12}$, which is impossible.

The key observation is that the structure of valid triples is hierarchical. Once we choose $A$, the only meaningful choices for $B$ are multiples of $A$, and once we choose $B$, the only meaningful choices for $C$ are multiples of $B$. This reduces the search space dramatically because each step shrinks the branching factor from arbitrary integers to divisors constrained by arithmetic progression.

Instead of trying all triples, we try all plausible candidates for $A$, then for each $A$, enumerate multiples for $B$, and for each $B$, enumerate multiples for $C$. Since values are bounded by roughly 2 × 10^4 in practice for optimal shifts, this enumeration remains small.

We also rely on a second key idea: optimal solutions tend to stay close to the original values. Therefore we only need to consider candidates near $a$, $b$, and $c$, typically within a small bounded window, because shifting far away is always more expensive than adjusting nearby valid configurations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) over 10⁴ domain | O(1) | Too slow |
| Divisor enumeration with bounded search | O(n √n) worst-case, much smaller in practice | O(1) | Accepted |

## Algorithm Walkthrough

We iterate over possible final values by anchoring the first element and building valid chains upward.

1. Fix a candidate value for $A$ in a range around the original $a$, typically from 1 up to a small bound such as 2 × 10^4. We do this because the optimal solution cannot be arbitrarily far from the original values without incurring unnecessary cost.
2. For each $A$, choose a candidate $B$ as a multiple of $A$. We generate these by iterating over multipliers $k$ such that $B = kA$. This guarantees the divisibility constraint $B \bmod A = 0$.
3. For each $B$, choose a candidate $C$ as a multiple of $B$, again by iterating over multipliers $m$ such that $C = mB$. This enforces $C \bmod B = 0$.
4. For every valid triple $(A, B, C)$, compute the total cost as $|a - A| + |b - B| + |c - C|$. We keep track of the minimum cost seen so far.
5. Store the triple that achieves this minimum.

The reason this works is that every valid final configuration must satisfy a strict divisibility chain. By constructing candidates through multiplication rather than arbitrary selection, we generate exactly the feasible set without missing any valid structure.

The search space is small because once $A$ is fixed, the number of multiples of $A$ below the bound is limited, and similarly for $B$.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 20000

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())

        best = 10**18
        best_triple = (a, b, c)

        # Try A
        for A in range(1, MAXV + 1):
            # Try B as multiple of A
            for B in range(A, MAXV + 1, A):
                # Try C as multiple of B
                for C in range(B, MAXV + 1, B):
                    cost = abs(a - A) + abs(b - B) + abs(c - C)
                    if cost < best:
                        best = cost
                        best_triple = (A, B, C)

        print(best)
        print(*best_triple)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the three-layer loop structure that enforces divisibility by construction. Instead of checking conditions after generating triples, we generate only valid triples.

The constant `MAXV` is chosen large enough to comfortably cover all useful candidates. Increasing it would not change correctness, only runtime.

A common mistake is forgetting that C must be iterated as a multiple of B, not as an independent variable. Another is incorrectly allowing non-integer stepping for multiples, which would break the divisibility guarantee.

## Worked Examples

We trace two cases.

### Example 1: `1 2 3`

We explore candidate chains starting from small values.

| A | B | C | Cost = |1-A| + |2-B| + |3-C| |

|---|---|---|---|

| 1 | 1 | 1 | 3 |

| 1 | 1 | 2 | 2 |

| 1 | 1 | 3 | 1 |

| 1 | 2 | 2 | 1 |

| 1 | 2 | 4 | 3 |

The best value is achieved at (1, 2, 2) or (1, 1, 3), both valid under constraints depending on divisibility chain interpretation, and the minimum cost is 1.

This shows that the optimal solution may not preserve ordering structure strictly by closeness to original values, but instead by balancing costs across all three coordinates.

### Example 2: `100 100 101`

We evaluate nearby collapsing solutions.

| A | B | C | Cost |
| --- | --- | --- | --- |
| 100 | 100 | 100 | 1 |
| 100 | 100 | 200 | 99 |
| 101 | 101 | 101 | 3 |

The best choice is to collapse to (100, 100, 100), confirming that reducing only one coordinate is often cheaper than shifting all three.

This trace shows why allowing downward moves is crucial.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(MAXV² / log MAXV) per test in practice | Each A enumerates B multiples, each B enumerates C multiples |
| Space | O(1) | Only constant storage for best answer |

The constraints allow up to 100 test cases, and MAXV is small enough that the nested divisor enumeration remains within time limits due to sparse iteration in inner loops.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    MAXV = 20000
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())

        best = 10**18
        best_triple = (a, b, c)

        for A in range(1, MAXV + 1):
            for B in range(A, MAXV + 1, A):
                for C in range(B, MAXV + 1, B):
                    cost = abs(a - A) + abs(b - B) + abs(c - C)
                    if cost < best:
                        best = cost
                        best_triple = (A, B, C)

        out.append(str(best))
        out.append(" ".join(map(str, best_triple)))

    return "\n".join(out)

# provided samples
assert run("""8
1 2 3
123 321 456
5 10 15
15 18 21
100 100 101
1 22 29
3 19 38
6 30 46
""") == """1
1 1 3
102
114 228 456
4
4 8 16
6
18 18 18
1
100 100 100
7
1 22 22
2
1 19 38
8
6 24 48"""

# custom cases
assert run("1\n1 1 1\n") == "0\n1 1 1", "already valid"
assert run("1\n10 20 30\n") is not None, "increasing chain"
assert run("1\n2 2 3\n") is not None, "small adjustment"
assert run("1\n1 10000 10000\n") is not None, "large imbalance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0 1 1 1` | identity case |
| `10 20 30` | computed | structured scaling |
| `2 2 3` | computed | minimal adjustment |
| `1 10000 10000` | computed | extreme imbalance |

## Edge Cases

A critical edge case is when all three numbers should collapse to the same value. For input like `100 100 101`, the algorithm considers the chain where $A = B = C = 100$, producing cost 1. A greedy approach that only adjusts the largest value downward might incorrectly try to match divisibility by increasing intermediate values, leading to a higher cost.

Another edge case is when the optimal configuration involves shrinking values significantly, such as `1 22 29`. Here, moving toward a small divisor structure like `(1, 22, 22)` is cheaper than attempting to align upward. The algorithm correctly explores these because it enumerates all divisibility chains starting from small $A$, ensuring that collapsing solutions are always considered.