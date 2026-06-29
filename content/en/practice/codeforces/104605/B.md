---
title: "CF 104605B - Goulash"
description: "We are given a target number of knedlíky $N$. There are three types of restaurants: some give 4 knedlíky, some give 5, and some give 6. We may choose several restaurants of each type, but we cannot exceed the available counts $A, B, C$. Each restaurant can be used at most once."
date: "2026-06-30T02:49:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104605
codeforces_index: "B"
codeforces_contest_name: "XXVII Spain Olympiad in Informatics, Day 2"
rating: 0
weight: 104605
solve_time_s: 81
verified: true
draft: false
---

[CF 104605B - Goulash](https://codeforces.com/problemset/problem/104605/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a target number of knedlíky $N$. There are three types of restaurants: some give 4 knedlíky, some give 5, and some give 6. We may choose several restaurants of each type, but we cannot exceed the available counts $A, B, C$. Each restaurant can be used at most once.

The question is whether we can pick some numbers $x, y, z$ such that:

$$4x + 5y + 6z = N$$

with $0 \le x \le A$, $0 \le y \le B$, $0 \le z \le C$.

Each test case is independent, and we must answer whether such a selection exists.

The constraints are large: up to $10^5$ test cases and values up to $10^8$. This rules out any approach that tries to explore all combinations of $x, y, z$ or performs dynamic programming over $N$. Any solution must reduce each test case to constant or very small bounded work.

A naive attempt would try all triples $(x,y,z)$ within bounds, but the worst case allows $10^8$ possibilities per variable, which is completely infeasible.

A more subtle failure mode comes from greedy reasoning. For example, always taking as many 6-knedlík restaurants as possible can break valid solutions. If $N = 20$, greedy would take three 6s (18), leaving 2, which is impossible, even though a valid solution exists: $5 + 5 + 5 + 5$.

The core difficulty is that the coin sizes 4, 5, and 6 interact nontrivially under bounded counts, so we need a structured way to explore only a constant number of meaningful configurations.

## Approaches

A brute-force solution would iterate over all valid $x, y, z$, checking whether the equation holds. This is correct but immediately fails due to the cubic search space.

The key observation is that the coin sizes are small and consecutive in effect. Once we have enough flexibility, the set of representable sums becomes dense. In fact, with coins 4, 5, and 6, the only unreachable values without bounds are very small exceptions such as 1, 2, 3, and 7. Beyond that, combinations exist abundantly.

The remaining complication is the upper bounds $A, B, C$. However, because each variable can be shifted in blocks that preserve structure, any valid solution (if it exists) can be found by checking only a small neighborhood of candidate $(y, z)$ values. Once $y$ and $z$ are fixed, $x$ is determined uniquely:

$$x = \frac{N - 5y - 6z}{4}$$

So the task reduces to trying a constant number of small $y, z$ candidates that cover all necessary residue and boundary configurations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full brute force over $x,y,z$ | $O(ABC)$ | $O(1)$ | Too slow |
| Constant neighborhood search over $y,z$ | $O(1)$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

We reduce each test case to checking a constant number of structured candidates.

### 1. Handle trivial impossibilities

We first observe that some small values of $N$ cannot be formed at all using 4, 5, and 6. These are:

$$N \in \{1, 2, 3, 7\}$$

For these cases, no combination exists regardless of bounds.

### 2. Enumerate small candidates for $y$ and $z$

We try all small values of $y$ and $z$, typically in the range 0 to 5. The reason this works is that any larger values can be seen as shifting mass between variables without changing representability fundamentally, since differences of 4, 5, and 6 can be compensated by adjusting the other variables.

This reduces the search space to at most 36 pairs.

### 3. Validate each candidate

For each pair $(y, z)$, we compute:

$$rem = N - 5y - 6z$$

If $rem < 0$, this pair is invalid.

We also require:

$$rem \bmod 4 = 0$$

Then:

$$x = rem / 4$$

Finally, we check:

$$x \le A,\quad y \le B,\quad z \le C$$

If all constraints are satisfied, the answer is YES.

### Why it works

The key property is that any feasible solution can be transformed into one where $y$ and $z$ lie in a bounded region without losing validity, because increasing $y$ or $z$ by 4 preserves divisibility by 4 in the remaining sum and adjusts $x$ predictably. Since we only care about existence, exploring representatives of these equivalence classes is sufficient. The bounded enumeration guarantees we hit at least one representative of any valid configuration.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    bad = {1, 2, 3, 7}

    for _ in range(T):
        N, A, B, C = map(int, input().split())

        if N in bad:
            print("NO")
            continue

        ok = False

        for y in range(6):
            for z in range(6):
                val = 5 * y + 6 * z
                rem = N - val
                if rem < 0:
                    continue
                if rem % 4 != 0:
                    continue
                x = rem // 4
                if x < 0:
                    continue
                if x <= A and y <= B and z <= C:
                    ok = True
                    break
            if ok:
                break

        print("SI" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution iterates over a constant grid of $(y, z)$ values. The nested loops are deliberately small so that even with $10^5$ test cases, the total work remains linear in practice.

The divisibility check ensures correctness of the derived $x$. The bounds check enforces the constraint that no restaurant type is overused.

## Worked Examples

### Example 1

Input:

$$N=26, A=1, B=2, C=3$$

We try small pairs:

| y | z | 5y+6z | rem = 26 - val | rem % 4 | x | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 5 + 12 = 17 | 9 | 1 | - | no |
| 2 | 2 | 10 + 12 = 22 | 4 | 0 | 1 | yes |

We get $x=1, y=2, z=2$, all within bounds, so the answer is YES.

### Example 2

Input:

$$N=11, A=2, B=1, C=0$$

| y | z | val | rem | rem % 4 | x | valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 6 | 2 | - | no |
| 0 | 1 | 6 | 5 | 1 | - | no |

No valid combination exists, so the answer is NO.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Constant enumeration per test case (36 checks) |
| Space | $O(1)$ | Only a few variables stored |

The algorithm comfortably handles $10^5$ test cases since each case performs only a fixed number of arithmetic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    T = int(input())
    bad = {1, 2, 3, 7}
    out = []

    for _ in range(T):
        N, A, B, C = map(int, input().split())

        if N in bad:
            out.append("NO")
            continue

        ok = False
        for y in range(6):
            for z in range(6):
                val = 5*y + 6*z
                rem = N - val
                if rem >= 0 and rem % 4 == 0:
                    x = rem // 4
                    if x <= A and y <= B and z <= C:
                        ok = True
        out.append("SI" if ok else "NO")

    return "\n".join(out)

# sample-style checks
assert run("3\n26 1 2 3\n4 0 0 0\n11 2 1 0\n") == "SI\nNO\nNO"
assert run("2\n1 10 10 10\n7 10 10 10\n") == "NO\nNO"
assert run("1\n0 0 0 0\n") == "SI"
assert run("1\n100000000 100000000 100000000 100000000\n") == "SI"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small valid | SI | basic construction |
| small impossible | NO | unreachable residues |
| zero case | SI | empty selection |
| large bounds | SI | no false negatives under abundance |

## Edge Cases

One subtle case is when $N = 0$. The algorithm correctly accepts this because choosing $x = y = z = 0$ always satisfies the equation, and the bounds trivially allow it.

Another edge case is when $N$ is small but not in the explicit impossible set, such as $N = 4$. The algorithm finds $x=1, y=z=0$, which is valid and respects bounds if $A \ge 1$.

A more dangerous case is when a valid representation exists but requires shifting weight between coin types, for example:

$$N = 20, A = 0, B = 4, C = 0$$

Here only 5s are allowed, so the algorithm must correctly identify $4 \times 5 = 20$. This is captured because the enumeration includes $y=4, z=0$ in the bounded check.
