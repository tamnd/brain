---
title: "CF 1945A - Setting up Camp"
description: "We are given a group of participants who must be assigned into tents, where each tent can hold at most three people. The participants come in three types with different constraints on how they are willing to share a tent."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1945
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 935 (Div. 3)"
rating: 800
weight: 1945
solve_time_s: 55
verified: true
draft: false
---

[CF 1945A - Setting up Camp](https://codeforces.com/problemset/problem/1945/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a group of participants who must be assigned into tents, where each tent can hold at most three people. The participants come in three types with different constraints on how they are willing to share a tent.

Introverts refuse to share a tent at all, so each introvert must occupy a tent alone. Extroverts are the opposite extreme: each one insists on being in a full tent of exactly three people, meaning every extrovert must be grouped with two other participants. Universals are flexible and can occupy a tent alone, with one other person, or with two others, as long as the tent size never exceeds three.

The task is to decide whether it is possible to assign everyone to tents while respecting all constraints, and if so, to minimize the number of tents used.

The input size goes up to 10^4 test cases, with counts of each type as large as 10^9. This immediately rules out any simulation over individuals. Any correct solution must reduce each test case to constant time arithmetic.

A naive approach might try to greedily fill tents step by step, repeatedly forming valid groups until people run out. That kind of simulation is dangerous because the order of assignments affects feasibility. For example, if universals are consumed too early, we may later be unable to complete full extrovert groups.

A key edge situation appears when extroverts cannot be placed into full groups of three even after using all universals:

Input:

```
0 1 1
```

One extrovert and one universal cannot form a valid group of three, and the extrovert cannot be alone or in a partial tent. The correct output is `-1`. A greedy algorithm that places universals elsewhere first might incorrectly conclude feasibility by leaving the extrovert stranded.

Another subtle failure arises when introverts consume too many tents early in reasoning without accounting for the fact that universals may later be needed to complete extrovert groups.

These observations suggest we must reason globally about how many universals are required for extroverts before counting remaining tents.

## Approaches

The brute-force interpretation is to literally construct tents. We repeatedly try to assign extroverts into groups of three, then place introverts into single tents, and finally distribute universals among any remaining open slots. For each test case, we might try all possible distributions of universals among extrovert groups and leftover tents.

However, the state space grows with the number of participants. Even a simplified simulation that processes each person once still risks O(a + b + c) per test case, which becomes 10^14 operations in the worst case across all inputs. This is far too slow.

The structure of the problem suggests a more direct decomposition. Introverts are fixed: they always consume exactly one tent each. Extroverts are also rigid: they must form groups of exactly three, so they contribute b tents, but may require help from universals if b is not divisible into perfect triples. Universals are the only flexible resource, and their role is to fill missing spots in extrovert groups and to form leftover partial groups afterward.

The key insight is to treat extrovert grouping first. Each full extrovert group consumes one tent of size three. If b % 3 is nonzero, the remaining 1 or 2 extroverts require universals to complete their groups; otherwise the configuration is impossible if not enough universals exist. After satisfying extroverts, any leftover universals can only reduce the number of tents by packing into groups of three.

This reduces the problem to simple arithmetic rather than assignment search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a + b + c) per test | O(1) | Too slow |
| Optimal | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. First allocate one tent per introvert. This is forced because introverts cannot share. We start the answer with `a`.
2. Next, handle extroverts in groups of three. Each full group of three extroverts consumes exactly one tent, so we add `b // 3` to the answer.
3. Compute the remainder `r = b % 3`. This represents leftover extroverts that cannot form a complete group.
4. If `r > 0`, we must use universals to complete the last incomplete extrovert group. If we have fewer than `3 - r` universals available, we cannot satisfy extrovert constraints and return `-1`.
5. If it is possible to complete the last group, we deduct the required universals. The incomplete group still contributes one tent, so we add `1` to the answer.
6. Now we have remaining universals. They can be packed freely into groups of three, each such group forming one tent. Add `(c_remaining) // 3` to the answer.
7. If universals remain after packing, they still occupy tents, but since each tent can hold up to three people, leftover universals always form at most one extra partial tent. However, this is already accounted for by integer division since leftover 1-2 universals still need one tent.

A more compact formulation emerges: after handling extroverts, simply add remaining universals into tents greedily by filling leftover spots, then grouping triples.

### Why it works

The algorithm separates participants by rigidity. Introverts and extroverts impose fixed structural constraints, while universals are a resource used only to repair incomplete extrovert groups or fill leftover capacity. The invariant is that after processing extroverts, every tent is either fully determined or has exactly one or two free slots, and universals are always placed into these slots before forming new tents. Since universals are never beneficial to leave unused in a partially filled structure when a new tent could be avoided, greedy packing is optimal and cannot increase the number of tents.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())

        # introverts always need their own tents
        ans = a

        # handle extroverts in full groups of 3
        ans += b // 3
        r = b % 3

        if r:
            need = 3 - r
            if c < need:
                print(-1)
                continue
            c -= need
            ans += 1

        # pack remaining universals
        ans += (c + 2) // 3

        print(ans)

if __name__ == "__main__":
    solve()
```

The code first assigns each introvert to a separate tent, since no other configuration is valid. It then packs extroverts into full groups of three. Any leftover extroverts force the creation of an additional tent, but only if enough universals exist to complete that group.

The expression `(c + 2) // 3` is a standard way to count how many tents are needed to pack remaining universals optimally in groups of at most three. It implicitly handles partial final groups without special cases.

A common mistake is to try placing universals before resolving extrovert remainders. That breaks feasibility checking, because universals may be consumed where they are not needed, leaving no way to complete a required extrovert group.

## Worked Examples

We trace two representative cases.

### Example 1

Input:

```
1
1 4 2
```

| Step | a | b | c | Action | tents |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 4 | 2 | introverts | 1 |
| ext full | 1 | 4 | 2 | b//3 = 1 group | 2 |
| remainder | 1 | 1 | 2 | r=1, need 2 universals | 2 |
| fill | 1 | 1 | 0 | use 2 universals | 3 |
| final | 1 | 1 | 0 | no universals left | 3 |

This shows a single incomplete extrovert group must be completed using universals, after which no further flexibility remains.

### Example 2

Input:

```
1
7 0 5
```

| Step | a | b | c | Action | tents |
| --- | --- | --- | --- | --- | --- |
| init | 7 | 0 | 5 | introverts | 7 |
| ext | 7 | 0 | 5 | no extroverts | 7 |
| pack | 7 | 0 | 5 | universals packed | 9 |

The 5 universals form one full tent of 3 and one partial tent of 2, producing two additional tents.

These traces show that the algorithm always prioritizes mandatory constraints before using flexible resources.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case uses constant arithmetic operations |
| Space | O(1) | Only a few integer variables are stored |

The solution easily handles 10^4 test cases since each one is resolved in constant time.

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
        a, b, c = map(int, input().split())
        ans = a
        ans += b // 3
        r = b % 3
        if r:
            need = 3 - r
            if c < need:
                out.append("-1")
                continue
            c -= need
            ans += 1
        ans += (c + 2) // 3
        out.append(str(ans))
    return "\n".join(out)

# provided samples (partial inclusion for brevity)
assert run("10\n1 2 3\n1 4 1\n1 4 2\n1 1 1\n1 3 2\n19 7 18\n0 0 0\n7 0 0\n0 24 0\n1000000000 1000000000 1000000000") == \
"3\n-1\n3\n-1\n3\n28\n0\n7\n8\n1666666667"

# custom cases
assert run("1\n0 1 1") == "-1", "single extrovert impossible without enough universals"
assert run("1\n0 3 0") == "1", "exact full extrovert group"
assert run("1\n0 4 2") == "2", "mixed remainder packing"
assert run("1\n5 0 1") == "6", "introverts dominate"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 1 1 | -1 | impossible extrovert completion |
| 0 3 0 | 1 | exact grouping of extroverts |
| 0 4 2 | 2 | handling remainder with universals |
| 5 0 1 | 6 | pure introvert + universal packing |

## Edge Cases

A critical edge case is when extroverts leave a remainder of one or two after grouping by threes. For example, consider `0 1 2`. The single extrovert cannot form a valid tent without two more people, so the two universals are exactly sufficient. The algorithm detects `r = 1`, checks `c >= 2`, and completes one tent.

Another edge case is when universals are abundant but irrelevant due to strict introvert demands. For `3 0 10`, introverts consume three tents immediately, and the remaining universals simply form `10` people into `4` tents (3,3,3,1), giving total `3 + 4 = 7`.

Finally, when there are no extroverts at all, the problem reduces to packing introverts and universals independently. The algorithm still works because the extrovert branch contributes nothing and universals are grouped optimally using ceiling division.
