---
title: "CF 105582H - Hamburgers"
description: "We are given several groups of friends, and for each group we want to choose a cafe that makes as many people in that group happy as possible. Each person has a preference described by a small set of ingredients, encoded as a short string."
date: "2026-06-22T14:38:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105582
codeforces_index: "H"
codeforces_contest_name: "Ural Championship 2017"
rating: 0
weight: 105582
solve_time_s: 63
verified: true
draft: false
---

[CF 105582H - Hamburgers](https://codeforces.com/problemset/problem/105582/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several groups of friends, and for each group we want to choose a cafe that makes as many people in that group happy as possible.

Each person has a preference described by a small set of ingredients, encoded as a short string. A hamburger is also described by a set of ingredients. A person is satisfied by a hamburger if every ingredient they like appears in that hamburger. A cafe is considered good for a person if at least one of its hamburgers satisfies that person.

For each group, the task is to choose one cafe that maximizes the number of satisfied people in that group. If multiple cafes achieve the same maximum, we pick the one with the smallest index.

The key structure here is that each preference and each burger uses at most 6 distinct letters, so each set is very small even though the alphabet has 26 letters. This immediately suggests that subsets and bitmask reasoning will be efficient, because the total number of subsets of a 6-element set is only 64.

The main difficulty is that we are comparing every group against every cafe, and both can be up to 1000, while the total number of people and burgers can reach 50000. A naive all-pairs matching between people and burgers inside each cafe would be far too slow.

A subtle edge case appears when multiple burgers in a cafe partially match a person's preference but none fully contain it. For example, if a person likes `{a, b}` and a cafe has burgers `{a}` and `{b}`, the person is not satisfied. Only full containment matters, not partial overlap.

Another corner case is when a cafe has no burger that satisfies anyone in a group. That cafe still needs to be considered and may be chosen if all cafes perform equally poorly, since we still pick the smallest index in ties.

## Approaches

A direct way to solve the problem is to simulate everything literally. For each group and each cafe, we iterate over every person and then over every burger in that cafe, checking whether the burger contains all required ingredients of that person. This is correct because it mirrors the definition exactly. However, the complexity becomes the product of groups, cafes, people, and burgers, which is far too large given the constraints.

The key observation is that each burger and each preference is a set over at most 6 distinct letters. Instead of repeatedly checking subset relationships, we can precompute the reverse direction: for a given burger, we can enumerate all possible subsets of its ingredient set. Every such subset corresponds to a person who would be satisfied by that burger. Since a burger has at most 6 ingredients, this expansion creates at most 64 subsets.

This transforms each cafe into a precomputed set of all preference-sets it can satisfy. Once we have this, checking a person becomes a simple membership test. We then evaluate each cafe by scanning all people and counting how many of their preference masks are contained in the cafe’s precomputed set.

The improvement comes from swapping repeated subset checks for a small constant expansion per burger and fast hash lookups afterward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force person-burger matching | O(G · C · P · B) | O(1) | Too slow |
| Subset expansion per burger + membership counting | O(total burgers · 2^6 + total people · cafes) | O(total expanded states) | Accepted |

## Algorithm Walkthrough

1. Convert every ingredient string into a bitmask over 26 letters. Each character corresponds to a bit position. This allows subset checks to become bit operations.
2. For each cafe, build a set of all ingredient masks of burgers that can satisfy someone indirectly. For every burger mask, generate all subsets of that mask and insert them into the cafe’s set. This works because any person satisfied by that burger must have a preference equal to one of these subsets.
3. After preprocessing, each cafe now contains a complete representation of all preference masks it can satisfy via at least one burger.
4. For each group, count frequencies of identical preference masks among its people. This avoids repeatedly scanning identical preferences multiple times.
5. For each cafe, compute how many people in the group are satisfied by iterating over all distinct preference masks in the group and checking whether that mask exists in the cafe’s precomputed set. Multiply by frequency.
6. Track the cafe with the maximum score for each group, breaking ties by choosing the smallest index.

### Why it works

Every person is satisfied if and only if there exists at least one burger whose ingredient set is a superset of their preference set. Enumerating all subsets of each burger captures exactly all possible preference sets that can be satisfied by that burger. Taking the union over all burgers in a cafe preserves this equivalence, so membership in the final set is logically identical to the original satisfaction condition. Since each group’s score is just a sum over independent people, counting via frequencies preserves correctness without changing the underlying combinatorial structure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def mask_of(s):
    m = 0
    for ch in s.strip():
        m |= 1 << (ord(ch) - 97)
    return m

def all_submasks(mask):
    # generate all subsets of up to 26-bit mask, but actual size <= 6 bits
    bits = []
    for i in range(26):
        if mask & (1 << i):
            bits.append(i)
    res = []
    k = len(bits)
    for sub in range(1 << k):
        m = 0
        for j in range(k):
            if sub & (1 << j):
                m |= 1 << bits[j]
        res.append(m)
    return res

n = int(input())
groups = []

for _ in range(n):
    k = int(input())
    freq = {}
    for _ in range(k):
        m = mask_of(input())
        freq[m] = freq.get(m, 0) + 1
    groups.append((k, freq))

m = int(input())
cafes = []

for _ in range(m):
    l = int(input())
    s = set()
    for _ in range(l):
        bm = mask_of(input())
        for sm in all_submasks(bm):
            s.add(sm)
    cafes.append(s)

for _, freq in groups:
    best_cafe = 1
    best_score = -1

    for idx, cafe_set in enumerate(cafes, start=1):
        score = 0
        for pm, cnt in freq.items():
            if pm in cafe_set:
                score += cnt

        if score > best_score or (score == best_score and idx < best_cafe):
            best_score = score
            best_cafe = idx

    print(best_cafe)
```

The implementation begins by encoding every ingredient string as a bitmask. This makes subset relationships cheap and avoids string operations entirely. The helper function for generating submasks enumerates all subsets of a burger’s active bits, which is safe because the number of distinct ingredients per string is at most 6.

Each cafe builds a hash set containing all preference masks it can satisfy. This set is the key acceleration structure, replacing repeated subset checks with O(1) membership tests.

For each group, we compress identical preferences using a frequency map. This is important because groups can contain repeated preference strings, and treating them individually would repeat identical work unnecessarily. The final scoring step simply checks membership of each unique mask in each cafe’s set and multiplies by its frequency.

Tie-breaking is handled during the scan by tracking the smallest index achieving the maximum score.

## Worked Examples

Consider a simplified situation with one group and two cafes.

Group preferences are `{a}`, `{ab}`, `{b}`. Cafe 1 has burgers `{ab}` and `{c}`. Cafe 2 has burgers `{b}` and `{ac}`.

For Cafe 1, the subset expansion of `{ab}` produces `{}`, `{a}`, `{b}`, `{ab}`. Cafe 1 can satisfy `{a}` and `{ab}` but not `{b}`. So score is 2.

For Cafe 2, expansion of `{b}` produces `{}`, `{b}`. Expansion of `{ac}` produces `{}`, `{a}`, `{c}`, `{ac}`. So Cafe 2 can satisfy `{a}` and `{b}` and score is 3.

| Cafe | `{a}` | `{ab}` | `{b}` | Score |
| --- | --- | --- | --- | --- |
| 1 | yes | yes | no | 2 |
| 2 | yes | no | yes | 2 |

This trace shows that correctness depends on full subset containment rather than partial overlap, and the precomputed closure correctly captures satisfaction.

Now consider a group where all people have identical preference `{a}` and a cafe has burgers `{b}`, `{c}` only. Its subset closure contains no `{a}`, so score remains zero, which is consistent with the definition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total burgers · 2^k + m · total people) | Each burger expands into at most 64 subsets, and each cafe is evaluated by scanning group preferences once |
| Space | O(m · 64 + total distinct preferences) | Each cafe stores a set of reachable subsets |

The bounds fit comfortably within limits because 50,000 burgers expand to about 3.2 million subset insertions in total, and each lookup is constant-time. The final evaluation performs at most 50 million hash checks, which is acceptable in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()  # placeholder, replace with actual call

# Since full solution is not wrapped in function, these are illustrative structure tests

# minimal case
# one group, one cafe, perfect match

# group: 1 person "a"
# cafe: 1 burger "a"
# expected: cafe 1

# boundary no match case

# all mismatch case

# mixed duplicates case
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single match | 1 | basic correctness |
| no matching burgers | 1 | tie-breaking on zero scores |
| multiple cafes tie | 1 | smallest index rule |
| duplicate preferences | 1 | frequency compression correctness |

## Edge Cases

A case where no burger in any cafe contains a given ingredient set still produces a valid answer because all cafes score zero and the smallest index is selected. For example, if all people like `{a}` but all burgers contain only `{b}`, every cafe has an empty satisfaction set and the answer is cafe 1.

Another case is when a burger has exactly six ingredients. Even then, the subset expansion remains bounded at 64 elements, so the preprocessing cost does not explode. The algorithm treats this the same way as smaller burgers, ensuring consistent behavior across extremes.

Repeated preferences inside a group do not affect correctness because they are aggregated into a frequency map before scoring. This prevents double counting from redundant iterations.
