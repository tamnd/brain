---
title: "CF 1367E - Necklace Assembly"
description: "We are given a multiset of colored beads, where each bead is just a lowercase letter. From these beads, we want to choose some subset and arrange it in a circle, forming a necklace. The arrangement is circular, so rotations matter but there is no fixed starting point."
date: "2026-06-18T18:20:43+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "dp", "graphs", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1367
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 650 (Div. 3)"
rating: 1900
weight: 1367
solve_time_s: 68
verified: true
draft: false
---

[CF 1367E - Necklace Assembly](https://codeforces.com/problemset/problem/1367/E)

**Rating:** 1900  
**Tags:** brute force, dfs and similar, dp, graphs, greedy, number theory  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of colored beads, where each bead is just a lowercase letter. From these beads, we want to choose some subset and arrange it in a circle, forming a necklace. The arrangement is circular, so rotations matter but there is no fixed starting point.

A necklace is called k-beautiful if shifting every bead forward by k positions along the circle leaves the necklace unchanged. In other words, if you rotate the circle by k steps, the sequence of colors looks identical to what you started with.

For each test case, we want the maximum possible number of beads in such a k-beautiful circular arrangement, subject to the constraint that we can only use beads available in the given multiset.

The key input is a string describing available beads, and a parameter k that defines the rotational symmetry requirement. The output is a single integer, the largest length of a circular arrangement satisfying this symmetry and feasibility constraint.

The constraints are small enough that the total number of beads across all test cases is at most 2000. This immediately rules out anything worse than roughly O(n^2) per test case, and makes it realistic to try all candidate lengths and verify each one with a fast check.

A naive interpretation that often fails is to think we are simply matching frequencies or building a periodic string greedily. For example, if k is large, one might incorrectly assume symmetry is irrelevant. Consider a case like n = 5, k = 4, and all beads are distinct. A naive greedy approach might try to form length 5, but in reality the symmetry constraint forces a strong structure that may only allow smaller valid cycles depending on frequency distribution.

Another subtle failure case is ignoring that the circular constraint creates cycles of positions. For example, if k = 2 and length is 6, positions split into cycles like (0,2,4) and (1,3,5). A solution that treats positions independently will overcount availability because each cycle requires identical characters.

## Approaches

A brute-force strategy is to try every possible length L from 1 up to n and check whether we can construct a k-beautiful necklace of that length. For each fixed L, we simulate the structure imposed by the rotation rule.

The key structural fact is that rotating by k means indices are connected in cycles. If we label positions 0 to L−1, then position i must match position (i + k) mod L. Repeating this constraint partitions the indices into disjoint cycles. Inside each cycle, all positions must contain the same letter.

The number of cycles is determined by the greatest common divisor of L and k. If we define g = gcd(L, k), then there are g cycles, each of size m = L / g. Each cycle behaves like a single “slot” that must be filled with one letter, but filling one slot consumes m copies of that letter.

So for a fixed L, the problem becomes: we have g slots, each requiring m identical beads, and we have letter frequencies. Each letter c can contribute at most floor(freq[c] / m) slots. We just need to check whether the total number of usable slots across all letters is at least g.

The brute-force works because checking feasibility for one L is only 26 operations. The failure point is the outer loop over L, which runs up to 2000, giving about 52,000 checks per test case, well within limits given the total input size.

There is no need for dynamic programming or graph search beyond this observation, because the cycle decomposition completely linearizes the structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over L with feasibility check | O(n log n) per test case (gcd included) | O(1) extra | Accepted |
| Precomputation / DP | Not needed | O(1) | Overkill |

## Algorithm Walkthrough

We iterate over all possible candidate necklace lengths and test whether each one can be constructed under the symmetry constraint.

1. For a candidate length L, compute g = gcd(L, k). This value determines how positions split into independent cycles under rotation by k. If two positions are in the same cycle, they must share the same color.
2. Compute m = L / g, the size of each cycle. Every chosen color assigned to a cycle must supply m identical beads.
3. Count frequencies of all 26 letters in the input string. This is reused for all L.
4. For each letter c, compute how many full cycles it can support, which is freq[c] // m. This is the number of cycles we can assign this color to.
5. Sum these contributions across all letters. If the total is at least g, then it is possible to assign colors to all cycles, meaning a valid necklace of length L exists.
6. Track the maximum L for which feasibility holds.

The reasoning behind this check is that each cycle is independent once we fix its color, and each cycle consumes exactly m identical beads. So feasibility reduces to packing g identical “cycle demands” into available frequency budgets.

### Why it works

The rotation constraint forces equality along orbits of the transformation i → i + k mod L. These orbits are exactly the gcd(L, k) cycles. Any valid necklace must be constant on each orbit. Conversely, any assignment of colors to cycles automatically satisfies the rotation constraint because shifting by k only permutes positions within each cycle. The feasibility check matches supply (letter counts) against demand (cycles of size m), so it exactly characterizes constructible lengths.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()

        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - 97] += 1

        ans = 1

        for L in range(1, n + 1):
            from math import gcd
            g = gcd(L, k)
            m = L // g

            total = 0
            for f in freq:
                total += f // m

            if total >= g:
                ans = L

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the feasibility condition derived earlier. The frequency array is computed once per test case. For each candidate length L, we recompute the gcd and derive cycle structure. The inner loop over 26 letters ensures constant work per L.

A subtle point is that we never explicitly construct the necklace. All reasoning is done on cycle counts, which avoids any combinatorial explosion.

## Worked Examples

Consider a simplified instance: n = 6, k = 3, s = "abcbac".

We evaluate possible lengths, focusing on L = 6.

For L = 6, g = gcd(6, 3) = 3, so there are 3 cycles, each of size m = 2. Each cycle needs two identical beads. The frequency counts allow us to check how many pairs each letter can provide.

| L | g = gcd(L,k) | m = L/g | usable cycles per letter | total cycles | feasible |
| --- | --- | --- | --- | --- | --- |
| 6 | 3 | 2 | a:1, b:1, c:1 | 3 | yes |

Since we can support 3 cycles, length 6 is achievable.

Now consider a case like n = 3, k = 6, s = "aaa".

For L = 3, g = gcd(3, 6) = 3, so m = 1. Each cycle is a single position, so there are no constraints beyond availability. Each letter contributes freq[c] // 1 cycles, giving 3 cycles total, which matches g.

| L | g | m | total cycles | feasible |
| --- | --- | --- | --- | --- |
| 3 | 3 | 1 | 3 | yes |

This shows that when k is larger than L, the structure degenerates into independent positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 26 · log n) per test case | We try each L up to n, compute gcd in log time, and sum over 26 letters |
| Space | O(1) auxiliary | Only fixed-size frequency array is used |

The total n across test cases is at most 2000, so the worst-case computation is comfortably within limits. Even the full 2000 × 2000 loop is small in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import math
    input = sys.stdin.readline

    def solve():
        t = int(input())
        for _ in range(t):
            n, k = map(int, input().split())
            s = input().strip()

            freq = [0] * 26
            for ch in s:
                freq[ord(ch) - 97] += 1

            ans = 1

            for L in range(1, n + 1):
                g = math.gcd(L, k)
                m = L // g

                total = 0
                for f in freq:
                    total += f // m

                if total >= g:
                    ans = L

            print(ans)

    solve()
    sys.stdout.seek(0)
    return sys.stdout.read().strip()

# provided samples
assert run("""6
6 3
abcbac
3 6
aaa
7 1000
abczgyo
5 4
ababa
20 10
aaebdbabdbbddaadaadc
20 5
ecbedececacbcbccbdec
""") == """6
3
5
4
15
10"""

# custom cases
assert run("""1
1 100
a
""") == "1", "single bead always works"

assert run("""1
2 1
ab
""") == "1", "rotation by 1 forces equality in length 2"

assert run("""1
4 2
aabb
""") == "4", "two cycles of size 2"

assert run("""1
6 2
aaabbb
""") == "6", "balanced distribution across cycles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single bead | 1 | minimal valid structure |
| ab with k=1 | 1 | strong symmetry constraint |
| aabb with k=2 | 4 | correct cycle packing |
| aaabbb with k=2 | 6 | full utilization across cycles |

## Edge Cases

A minimal length case like a single bead demonstrates that the algorithm always accepts L = 1 since g = 1 and m = 1, so every frequency array trivially satisfies the condition.

A case where k = 1 forces every position in a cycle of length L to collapse into a single cycle only when L = 1. For larger L, m = L and only one color can fill the entire structure, which the feasibility check correctly captures because floor(freq[c] / L) becomes zero unless all beads are identical.

A case where k is larger than L behaves like identity rotation with g = L, making every position its own cycle. The algorithm correctly reduces to checking whether total available beads cover L positions, which matches the frequency sum condition implicitly enforced through m = 1.
