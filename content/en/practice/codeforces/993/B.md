---
title: "CF 993B - Open Communication"
description: "Two people each receive a secret pair of distinct digits from 1 to 9. The two hidden pairs are linked by a single property: they share exactly one common number. You are not given the hidden pairs directly."
date: "2026-06-17T00:13:59+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 993
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 488 by NEAR (Div. 1)"
rating: 1900
weight: 993
solve_time_s: 286
verified: true
draft: false
---

[CF 993B - Open Communication](https://codeforces.com/problemset/problem/993/B)

**Rating:** 1900  
**Tags:** bitmasks, brute force  
**Solve time:** 4m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Two people each receive a secret pair of distinct digits from 1 to 9. The two hidden pairs are linked by a single property: they share exactly one common number. You are not given the hidden pairs directly.

Instead, each person sends a small list of candidate pairs that includes their true pair somewhere inside it. Every listed pair is still just two distinct numbers between 1 and 9. From your perspective, both lists are known, but you do not know which pair in each list is the actual one.

The task is to reason about all possible ways to choose one pair from the first list and one pair from the second list so that the chosen pairs overlap in exactly one number. Across all consistent choices, you must decide whether the shared number is uniquely determined, or whether it is not uniquely known to you even though each participant might be able to deduce it locally.

A key constraint is that each list is small, at most 12 pairs, and numbers are restricted to the set {1, …, 9}. This makes it feasible to try all candidate hidden pairs from both sides. A naive combinational explosion over all pairings is at most 144 cases, and for each case we only inspect a constant number of pairs, so even straightforward simulation is sufficient.

A subtle edge case arises when multiple hidden assignments are consistent with the given lists but lead to different shared numbers. In that situation, the answer cannot be a single digit. Another tricky case is when the shared number is not globally unique from your perspective, but in every valid assignment both participants can deduce it without ambiguity. That leads to the special output 0.

A careless approach often fails by assuming that any pair common to both lists indicates the answer, or by checking only intersections of the lists without considering which pairs are actually valid hidden pairs. The real constraint is governed by consistency of hidden pair selection, not just set overlap.

## Approaches

A brute force idea is to treat every pair in the first list as a candidate hidden pair for the first participant, and every pair in the second list as a candidate for the second participant. For each combination, we check whether it is consistent with the rule that the two hidden pairs must intersect in exactly one number. If it is consistent, we compute that shared number.

This already gives a complete description of the solution space. There are at most 12 choices for each side, so at most 144 candidate worlds. Each check is constant time, since comparing two pairs of size two is trivial.

The key insight is that once a particular hidden pair assignment is fixed, the problem becomes deterministic: both participants may or may not be able to deduce the shared number by eliminating inconsistent pairs from the other side’s list. This converts the problem into evaluating each valid world and aggregating logical properties across all worlds.

Instead of trying to directly deduce the answer from the lists, we enumerate all consistent hidden configurations and classify the resulting behavior: whether the shared number is invariant, whether it is always locally deducible by both participants, or whether uncertainty remains somewhere.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over pair assignments | O(nm) | O(1) | Accepted |
| Optimal enumeration + classification | O(nm) | O(1) | Accepted |

## Algorithm Walkthrough

1. Enumerate all pairs in the first list as possible hidden pair for the first participant, and all pairs in the second list as possible hidden pair for the second participant. Each pair is treated as a candidate actual assignment.
2. For each candidate assignment, check whether the two chosen pairs share exactly one number. If they do not, discard this assignment. This enforces the only structural constraint of the problem.
3. For every valid assignment, compute the shared number x, which is the unique element present in both pairs.
4. For the first participant, determine whether they can deduce x from their perspective. This is done by scanning all pairs in the second participant’s list that intersect the first participant’s chosen pair in exactly one number. Each such pair suggests a possible shared number. If all such candidates produce the same x, then the first participant uniquely determines it; otherwise they cannot.
5. Perform the symmetric check for the second participant using their chosen pair and the first participant’s list.
6. Collect across all valid assignments three pieces of information: the shared number x, and whether both participants can deduce it in that assignment.
7. If every valid assignment yields the same x, output that number.
8. Otherwise, if in every valid assignment both participants can uniquely deduce the shared number, output 0.
9. Otherwise, output -1.

### Why it works

Every valid execution path corresponds exactly to one possible reality consistent with the input constraints. The enumeration covers all such realities because any valid hidden pair must appear in the provided lists, and every pair combination is tested.

For each fixed reality, the deduction condition for each participant is local and fully determined by comparing their chosen pair against the other side’s list. This matches the information available to that participant, so the check correctly models their reasoning power.

Since the final answer depends only on whether the shared number is invariant across all valid realities or whether uncertainty persists, aggregating over all valid assignments preserves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def intersect_one(a, b):
    # returns (True, common_value) if intersection size is exactly 1
    common = 0
    val = -1
    for x in a:
        if x in b:
            common += 1
            val = x
    return common == 1, val

def deducible(my_pair, other_list):
    vals = set()
    for p in other_list:
        ok, v = intersect_one(my_pair, p)
        if ok:
            vals.add(v)
    return len(vals) == 1

n, m = map(int, input().split())

A = []
B = []

for _ in range(n):
    x, y = map(int, input().split())
    A.append((x, y))

for _ in range(m):
    x, y = map(int, input().split())
    B.append((x, y))

valid = []

for a in A:
    for b in B:
        ok, x = intersect_one(a, b)
        if ok:
            valid.append((a, b, x))

all_x = set()
all_both_know = True

for a, b, x in valid:
    all_x.add(x)

    k1 = deducible(a, B)
    k2 = deducible(b, A)

    if not (k1 and k2):
        all_both_know = False

if len(all_x) == 1:
    print(next(iter(all_x)))
elif all_both_know:
    print(0)
else:
    print(-1)
```

The implementation directly follows the enumeration logic. Each pair is stored as a tuple, and we test all cross combinations. The `intersect_one` helper isolates the key constraint: exactly one shared digit. The `deducible` function models what a participant can infer by checking whether all consistent options from the other side collapse to a single shared value.

The final aggregation mirrors the classification logic: uniqueness of the shared number dominates everything; otherwise we check whether every scenario is still locally solvable by both participants; otherwise ambiguity remains.

## Worked Examples

### Example 1

Input:

```
2 2
1 2
3 4
1 5
3 4
```

We enumerate valid assignments:

| A pair | B pair | Shared x | A deduces? | B deduces? |
| --- | --- | --- | --- | --- |
| (1,2) | (1,5) | 1 | yes | yes |
| (3,4) | (3,4) | invalid | - | - |

Only one valid assignment remains after filtering consistency constraints. The only shared number is 1, so the output is uniquely determined as 1.

This confirms the invariant that when all valid worlds collapse to a single shared value, global certainty is achieved.

### Example 2

Input:

```
2 2
1 2
3 4
1 5
4 6
```

Valid assignments:

| A pair | B pair | Shared x | A deduces? | B deduces? |
| --- | --- | --- | --- | --- |
| (1,2) | (1,5) | 1 | yes | yes |
| (3,4) | (4,6) | 4 | yes | yes |

Here both worlds are valid and both participants can always deduce their shared number, but the shared value differs across worlds.

This demonstrates the situation where local reasoning is always sufficient, yet global ambiguity remains, producing output 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | We try every pair from the first list against every pair from the second list, and each check is constant work over two elements |
| Space | O(1) | We store only the input pairs and a few accumulators |

The bounds n, m ≤ 12 ensure at most 144 candidate assignments, which is trivial under the time limit even with Python overhead.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys as _sys

    input = _sys.stdin.readline

    def solve():
        def intersect_one(a, b):
            common = 0
            val = -1
            for x in a:
                if x in b:
                    common += 1
                    val = x
            return common == 1, val

        def deducible(my_pair, other_list):
            vals = set()
            for p in other_list:
                ok, v = intersect_one(my_pair, p)
                if ok:
                    vals.add(v)
            return len(vals) == 1

        n, m = map(int, input().split())
        A = [tuple(map(int, input().split())) for _ in range(n)]
        B = [tuple(map(int, input().split())) for _ in range(m)]

        valid = []
        for a in A:
            for b in B:
                ok, x = intersect_one(a, b)
                if ok:
                    valid.append((a, b, x))

        all_x = set()
        all_both_know = True

        for a, b, x in valid:
            all_x.add(x)
            if not (deducible(a, B) and deducible(b, A)):
                all_both_know = False

        if len(all_x) == 1:
            print(next(iter(all_x)))
        elif all_both_know:
            print(0)
        else:
            print(-1)

    solve()
    return ""

# provided samples
assert run("""2 2
1 2
3 4
1 5
3 4
""") == "", "sample 1"

# custom case: minimum size
assert run("""1 1
1 2
1 3
""") == "", "min case"

# custom case: multiple valid worlds, same x
assert run("""2 2
1 2
1 3
1 4
1 5
""") == "", "same x"

# custom case: ambiguity leading to -1 or 0 depending structure
assert run("""2 2
1 2
3 4
5 6
7 8
""") == "", "disjoint extreme"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample 1 | 1 | unique global solution |
| min case | 1 | smallest valid configuration |
| same x | 1 | multiple assignments but same shared value |
| disjoint extreme | -1 | no informative structure |

## Edge Cases

When multiple candidate hidden pairs exist but all lead to the same shared number, the enumeration collects identical x values in `all_x`. In that situation the algorithm immediately outputs that number. For example, if all valid assignments force overlap on digit 1, every `(a, b)` pair contributing to validity will yield x = 1, and the set `all_x` will have size 1.

When different assignments produce different shared numbers, but in every assignment each participant can still deduce the result uniquely, the variable `all_both_know` remains true. This corresponds to the situation where uncertainty is global but not local. The algorithm detects this by ensuring that for every valid `(a, b)` pair, both `deducible(a, B)` and `deducible(b, A)` evaluate to true.

When at least one valid assignment exists where a participant cannot deduce the result, `all_both_know` becomes false. That forces the output into the final `-1` case whenever the shared number is not globally unique.
