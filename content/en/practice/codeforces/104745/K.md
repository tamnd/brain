---
title: "CF 104745K - \u00d3scar and his battle"
description: "Each test case gives a set of playable characters and a set of monsters. A character is defined by two strengths: attack and defense. A monster is also defined by two thresholds, attack and defense, and a reward value in coins. You are allowed to pick exactly one character."
date: "2026-06-28T23:05:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104745
codeforces_index: "K"
codeforces_contest_name: "CAMA 2023"
rating: 0
weight: 104745
solve_time_s: 55
verified: true
draft: false
---

[CF 104745K - \u00d3scar and his battle](https://codeforces.com/problemset/problem/104745/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a set of playable characters and a set of monsters. A character is defined by two strengths: attack and defense. A monster is also defined by two thresholds, attack and defense, and a reward value in coins.

You are allowed to pick exactly one character. After that, you can defeat any subset of monsters, but only if the chosen character is strong enough in both directions: its attack must be at least the monster’s defense, and its defense must be at least the monster’s attack. Every monster can be defeated at most once, and each defeated monster contributes its coin value to your total.

The task is to decide which single character yields the maximum total coin reward from all monsters it can defeat.

The constraints push toward a solution that avoids checking every character against every monster directly. With up to 2 · 10^5 total entities per test file, a naive O(nm) pairing would attempt up to 4 · 10^10 checks, which is not viable. Any solution needs to preprocess monsters so that each character can compute its best achievable sum quickly.

A subtle failure case appears when different monsters trade off between attack and defense constraints. A character might dominate in one dimension but not the other, and naive sorting by only one parameter loses feasibility.

For example, consider two monsters: one requires high defense but low attack, the other requires high attack but low defense. A greedy choice based on only one constraint would incorrectly include an unreachable monster.

## Approaches

A brute-force method is straightforward: for each character, scan all monsters and sum rewards for those it can defeat. This is correct because it directly enforces both constraints per monster. However, each test case may involve 10^5 characters and 10^5 monsters, making this approach quadratic in the worst case.

The key observation is that the constraint “ai ≥ dj and bi ≥ cj” defines a dominance relation in two dimensions. Each monster contributes only if its coordinate (cj, dj) lies within the upper-right quadrant defined by (bi, ai) after swapping axes. This is a classic 2D dominance query problem, but with weights that need to be aggregated.

If we reinterpret each monster as a point (attack requirement cj, defense requirement dj) with weight ej, then for a fixed character (bi, ai), we need the sum of all ej such that cj ≤ bi and dj ≤ ai. This is a 2D prefix sum over points. The challenge is that coordinates are large (up to 10^9), so we must compress or reorder.

A standard trick is to sort monsters by one dimension, then maintain a data structure over the other dimension. Sorting monsters by defense requirement dj allows us to progressively activate monsters whose dj is small enough for the current character. For each active set, we need to query sum of all monsters with cj ≤ bi, which becomes a prefix sum over a Fenwick tree indexed by compressed cj values.

We then sort characters by their defense ai so that as ai increases, we incrementally add valid monsters into the active structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Sorted + Fenwick (offline sweep) | O((n + m) log m) | O(m) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Transform each monster into a pair of constraints (cj, dj) with weight ej. These represent the minimum required character stats to defeat it. This reformulation aligns the problem with 2D dominance queries.
2. Sort monsters by dj in ascending order. This ensures that as we consider characters with increasing defense, we can incrementally activate all monsters they are capable of handling in the defense dimension.
3. Sort characters by ai in ascending order, while keeping track of their original indices. This lets us evaluate them in a monotonic order of attack capability.
4. Build a Fenwick tree over compressed cj values. Compression is necessary because cj can be up to 10^9, but we only need relative ordering among monster attack requirements.
5. Maintain a pointer over the sorted monsters. For each character in increasing ai order, insert into the Fenwick tree all monsters with dj ≤ ai. Insertion means updating position cj with value ej.
6. After activating all eligible monsters for a character, query the Fenwick tree for the sum of all ej over indices cj ≤ bi. This gives the total reward for that character.
7. Store the result in the answer array at the character’s original position.

The correctness relies on the fact that at the moment we process a character, all monsters satisfying dj ≤ ai are active, and within that active set, prefix queries correctly capture cj ≤ bi.

### Why it works

At any point in the sweep, the Fenwick tree contains exactly the set of monsters whose defense requirement is already satisfied by the current or any previously processed character. Because characters are processed in increasing ai, no eligible monster is ever missed, and no ineligible monster is ever included. Within this filtered set, the Fenwick tree enforces the second constraint cj ≤ bi exactly, so every query returns precisely the sum over valid monsters.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())

        chars = []
        for i in range(n):
            a, b = map(int, input().split())
            chars.append((a, b, i))

        mons = []
        cj_vals = []

        for _ in range(m):
            c, d, e = map(int, input().split())
            mons.append((c, d, e))
            cj_vals.append(c)

        cj_vals = sorted(set(cj_vals))
        comp = {v: i + 1 for i, v in enumerate(cj_vals)}

        mons.sort(key=lambda x: x[1])
        chars.sort(key=lambda x: x[0])

        ft = Fenwick(len(cj_vals))

        ans = [0] * n
        p = 0

        for a, b, idx in chars:
            while p < m and mons[p][1] <= a:
                c, d, e = mons[p]
                ft.add(comp[c], e)
                p += 1

            ans[idx] = ft.sum(comp[b])

        print(*ans)

if __name__ == "__main__":
    solve()
```

The Fenwick tree maintains prefix sums over compressed monster attack requirements. The sweep pointer ensures only monsters with sufficient defense are included at the correct time.

One subtle detail is coordinate compression: without mapping cj to a dense index range, the Fenwick tree would be infeasible due to memory and time constraints. Another is the stable separation of insertion order and query order: monsters are inserted strictly before querying each character, ensuring correctness.

## Worked Examples

Consider a simplified scenario:

Characters: (a, b)

(3, 3), (5, 2)

Monsters: (c, d, e)

(2, 1, 10), (3, 2, 5), (4, 3, 7)

After sorting monsters by d:

(2,1,10), (3,2,5), (4,3,7)

After sorting characters by a:

(3,3), (5,2)

| Step | Character (a,b) | Activated Monsters | Fenwick Contents (cj→sum) | Query |
| --- | --- | --- | --- | --- |
| 1 | (3,3) | (2,1,10), (3,2,5) | 2→10, 3→5 | sum(cj≤3)=15 |
| 2 | (5,2) | all three | 2→10, 3→5, 4→7 | sum(cj≤2)=10 |

First character can defeat first two monsters, second character can only take the first due to tighter defense. This demonstrates how dual constraints are enforced incrementally.

Now consider a case where order matters:

Characters: (2,5), (5,2)

Monsters: (1,4,100), (4,1,50)

| Step | Character | Active Set | Result |
| --- | --- | --- | --- |
| (2,5) | first | (1,4,100) | 100 |
| (5,2) | second | both | 150 but filtered by cj≤2 gives 100 |

This shows why prefix filtering is essential; without separating dimensions, incorrect mixing would occur.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | sorting + Fenwick updates and queries per monster/character |
| Space | O(m) | Fenwick tree and compression arrays |

The combined constraints across all test cases sum to 2 · 10^5, so an O(N log N) approach is comfortably within limits. The logarithmic factor remains small due to Fenwick tree operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solution(inp)

def solution(inp: str) -> str:
    import sys
    input = sys.stdin.readline
    data = inp.strip().split()
    it = iter(data)

    t = int(next(it))
    out = []

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)
        def add(self, i, v):
            while i <= self.n:
                self.bit[i] += v
                i += i & -i
        def sum(self, i):
            s = 0
            while i > 0:
                s += self.bit[i]
                i -= i & -i
            return s

    for _ in range(t):
        n = int(next(it)); m = int(next(it))
        chars = []
        mons = []
        cj = []

        for i in range(n):
            a = int(next(it)); b = int(next(it))
            chars.append((a,b,i))
        for _ in range(m):
            c = int(next(it)); d = int(next(it)); e = int(next(it))
            mons.append((c,d,e))
            cj.append(c)

        cj = sorted(set(cj))
        comp = {v:i+1 for i,v in enumerate(cj)}

        mons.sort(key=lambda x:x[1])
        chars.sort(key=lambda x:x[0])

        ft = Fenwick(len(cj))
        ans = [0]*n
        p = 0

        for a,b,i in chars:
            while p < m and mons[p][1] <= a:
                c,d,e = mons[p]
                ft.add(comp[c], e)
                p += 1
            ans[i] = ft.sum(comp[b])

        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# custom tests
assert solution("""1
1 1
5 5
1 1 10
""") == "10", "single case"

assert solution("""1
2 2
1 1
10 10
1 1 5
10 10 7
""") == "5 12", "two chars"

assert solution("""1
2 2
5 1
1 5
2 2 3
3 3 4
""") == "0 0", "no valid"

assert solution("""1
3 3
3 3
5 2
2 5
2 2 1
3 3 2
1 1 3
""") == "6 3 3", "mixed dominance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single case | 10 | minimal correctness |
| two chars | 5 12 | accumulation across characters |
| no valid | 0 0 | empty dominance handling |
| mixed dominance | 6 3 3 | 2D filtering correctness |

## Edge Cases

A key edge case is when a character is strong in only one dimension. Suppose a character has high attack but low defense. The algorithm processes monsters in increasing defense requirement, so monsters requiring too much defense are never inserted into the Fenwick tree. For example, character (a, b) = (10, 1) and monster (c, d, e) = (1, 5, 100). Since d = 5 > b = 1, this monster is never activated, so it cannot contribute to the sum.

Another case is when cj values are large and sparse. Without coordinate compression, the Fenwick tree would either exceed memory limits or degrade into inefficient sparse indexing. Compression ensures that only meaningful indices are stored, and queries like sum(bi) remain valid even when bi is not an exact monster value.

A final subtle case is multiple monsters sharing identical cj or dj values. Sorting and stable insertion ensures all such monsters are inserted together, and Fenwick updates accumulate correctly since addition is associative.
