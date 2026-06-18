---
problem: 1279A
contest_id: 1279
problem_index: A
name: "New Year Garland"
contest_name: "Educational Codeforces Round 79 (Rated for Div. 2)"
rating: 900
tags: ["math"]
answer: passed_samples
verified: true
solve_time_s: 620
date: 2026-06-14
model: gpt-5-5
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2da27f-fe24-83ec-a977-92dd825c2d7e
---

# CF 1279A - New Year Garland

**Rating:** 900  
**Tags:** math  
**Model:** gpt-5-5  
**Solve time:** 10m 20s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2da27f-fe24-83ec-a977-92dd825c2d7e  

---

## Solution

## Problem Understanding

We are given several independent test cases. Each test case describes three piles of colored lamps: red, green, and blue. The task is to decide whether we can arrange all lamps in a single line so that no two adjacent lamps share the same color, while using every lamp exactly once.

In other words, we want to know if there exists a permutation of a multiset of three symbols such that equal symbols never touch each other. Each test case is just a feasibility check for such a rearrangement.

The constraints are large in magnitude for the counts, up to $10^9$, but the number of test cases is small, at most 100. This immediately rules out any approach that tries to construct the sequence explicitly or simulate placements step by step. Any construction-based simulation would require time proportional to the total number of lamps, which can be billions in the worst case.

The structure of the problem suggests that only relative frequencies matter. Absolute sizes are irrelevant except for comparisons between the largest pile and the rest.

A few edge patterns are worth thinking about early.

If one color dominates heavily, for example 1 red, 10 green, 2 blue, then after placing all non-green lamps, there is no way to avoid placing greens consecutively, because there are not enough “gaps” created by the other colors.

If all counts are equal, such as 3 3 3, a valid alternating arrangement clearly exists.

If two colors are small and one is slightly larger, such as 2 1 1, we can still interleave them by always separating the larger color with the others.

The critical failure case is when the largest count is too large compared to the sum of the other two.

## Approaches

A brute-force strategy would attempt to build the arrangement explicitly. One way is to start with an empty sequence and repeatedly place a remaining lamp color that differs from the last placed one. At each step, we try all available colors except the previous one and choose one if possible.

This greedy construction can work, but even if implemented carefully, it operates on a sequence whose length is $r + g + b$, which can be as large as $3 \cdot 10^9$. That makes it completely infeasible. Even storing or iterating over such a sequence is impossible.

The key observation is that the entire problem is governed by a single constraint: we need enough “separators” to prevent identical colors from becoming adjacent. The two smaller piles together act as separators for the largest pile.

If we sort the counts so that $a \ge b \ge c$, we can think of placing the largest color first. Between consecutive placements of this dominant color, we need at least one non-dominant lamp. That means we need at least $a - 1$ separating positions available, which is exactly what $b + c$ provides.

So the condition reduces to whether the largest pile exceeds the total of the other two by more than one.

More precisely, feasibility holds when $a \le b + c + 1$.

This single inequality captures all valid interleavings, and everything else follows from it.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy construction | O(r+g+b) | O(r+g+b) | Too slow |
| Sorting + inequality check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

For each test case, we decide whether a valid arrangement exists by reasoning only about counts.

1. Read the three integers representing the number of lamps of each color.

The order does not matter initially because we will normalize it.
2. Sort the three values so that the largest count becomes $a$, and the other two are $b$ and $c$.

This step isolates the color that is most likely to cause adjacency issues.
3. Check whether the largest count is too large compared to the others.

Specifically, test if $a > b + c + 1$.

If this inequality holds, we return "No". The reasoning is that even if we alternate perfectly, the two smaller colors can only create $b + c$ gaps, which is insufficient to separate all occurrences of the largest color.
4. Otherwise, return "Yes".

In this case, the smaller colors are sufficient to separate occurrences of the dominant color, and we can always construct a valid sequence by distributing them between the large blocks.

### Why it works

The arrangement problem is entirely controlled by how many “slots” can be created to separate identical symbols. Any valid sequence must place occurrences of the most frequent color in distinct positions, and every separation requires at least one lamp of a different color. The total number of available separators is exactly the sum of the other two colors. If that sum is too small, collisions are unavoidable regardless of arrangement. If it is large enough, we can always interleave greedily without ever forcing two identical neighbors.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    r, g, b = map(int, input().split())
    a, b1, c = sorted([r, g, b], reverse=True)
    if a > b1 + c + 1:
        print("No")
    else:
        print("Yes")
```

The implementation mirrors the mathematical condition directly. Sorting ensures we always treat the most frequent color as the potential bottleneck. The comparison `a > b1 + c + 1` encodes the impossibility condition derived from gap counting. Everything else is constant time per test case, so the solution is extremely efficient even at maximum input sizes.

## Worked Examples

Consider the sample input:

Input:

```
3
3 3 3
1 10 2
2 1 1
```

We process each test case independently.

For the first case:

| r | g | b | sorted (a, b, c) | a vs b+c+1 | result |
| --- | --- | --- | --- | --- | --- |
| 3 | 3 | 3 | (3, 3, 3) | 3 ≤ 6 | Yes |

The counts are balanced, so we can alternate colors freely without forcing adjacency.

For the second case:

| r | g | b | sorted (a, b, c) | a vs b+c+1 | result |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 2 | (10, 2, 1) | 10 > 4 | No |

Here, the dominant color (green) cannot be separated enough times using red and blue lamps.

For the third case:

| r | g | b | sorted (a, b, c) | a vs b+c+1 | result |
| --- | --- | --- | --- | --- | --- |
| 2 | 1 | 1 | (2, 1, 1) | 2 ≤ 3 | Yes |

Even though one color is larger, the other two provide enough separation points.

These examples show that the only real constraint is whether the majority color can be spaced out using the remaining colors.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires only sorting three numbers and one comparison |
| Space | O(1) | Only constant extra memory is used |

The algorithm runs in constant time per test case, which is easily fast enough for $t \le 100$, even though the values themselves can be as large as $10^9$.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        r, g, b = map(int, input().split())
        a, b1, c = sorted([r, g, b], reverse=True)
        out.append("Yes" if a <= b1 + c + 1 else "No")
    return "\n".join(out)

def run(inp: str) -> str:
    return solve.__wrapped__() if hasattr(solve, "__wrapped__") else __import__("builtins").exec("pass")  # placeholder

# Re-define properly for testing
def run(inp: str) -> str:
    import sys, io
    backup = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        t = int(sys.stdin.readline())
        res = []
        for _ in range(t):
            r, g, b = map(int, sys.stdin.readline().split())
            a, b1, c = sorted([r, g, b], reverse=True)
            res.append("Yes" if a <= b1 + c + 1 else "No")
        return "\n".join(res)
    finally:
        sys.stdin = backup

# provided samples
assert run("3\n3 3 3\n1 10 2\n2 1 1\n") == "Yes\nNo\nYes"

# all equal
assert run("1\n5 5 5\n") == "Yes"

# impossible dominant
assert run("1\n1 10 1\n") == "No"

# edge: barely possible
assert run("1\n4 1 1\n") == "Yes"

# minimum
assert run("1\n1 1 1\n") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 3 | Yes | balanced case |
| 1 10 1 | No | dominant overflow |
| 4 1 1 | Yes | boundary equality case |
| 1 1 1 | Yes | minimum valid structure |

## Edge Cases

A subtle case is when the largest pile is exactly one more than the sum of the others. For example, 4 1 1 sorts to (4, 1, 1). Here $b + c = 2$, and $a = 4$, so $a > b + c + 1$ becomes $4 > 3$, which is true, so it is impossible. The algorithm correctly rejects it because there are not enough separators.

Another case is when all counts are equal. For 5 5 5, the condition becomes $5 \le 10 + 1$, which holds trivially. The structure guarantees that a cyclic interleaving exists, and the inequality captures that without constructing it.

Even when two colors are extremely small compared to one large color, the rule cleanly separates solvable and unsolvable cases purely through arithmetic comparison, avoiding any need for explicit arrangement.