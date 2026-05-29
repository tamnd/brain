---
title: "CF 421A - Pasha and Hamsters"
description: "We are given a line of apples numbered from 1 to n. Each apple can be given to exactly one of two hamsters, Arthur or Alexander. The only restriction is that Arthur must receive only apples he likes, and Alexander must receive only apples he likes."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 421
codeforces_index: "A"
codeforces_contest_name: "Coder-Strike 2014 - Finals (online edition, Div. 2)"
rating: 800
weight: 421
solve_time_s: 60
verified: true
draft: false
---

[CF 421A - Pasha and Hamsters](https://codeforces.com/problemset/problem/421/A)

**Rating:** 800  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of apples numbered from 1 to n. Each apple can be given to exactly one of two hamsters, Arthur or Alexander. The only restriction is that Arthur must receive only apples he likes, and Alexander must receive only apples he likes. Some apples may be liked by both, and those can go to either hamster, but still only one of them.

Our task is to assign every apple to exactly one hamster while respecting both preference lists. The input gives n, then a list of indices Arthur likes, and a list of indices Alexander likes. We must output a length-n string of 1s and 2s indicating ownership.

The constraints are small: n is at most 100. That immediately tells us that even O(n²) or brute assignment strategies are easily fast enough. There is no need for advanced data structures or optimization tricks. The problem is fundamentally about resolving overlaps consistently.

A key subtlety is apples that belong to neither list. The statement guarantees a solution exists, but a naive implementation might ignore these cases or fail to assign them deterministically.

A second subtle case is overlap between preferences. If an apple is liked by both hamsters, assigning it arbitrarily still works, but if we try to “balance” or “optimize” without care, we can accidentally leave some apples unassigned.

## Approaches

A brute-force perspective would be to try all possible assignments of n apples to two hamsters and check validity. Each apple has 2 choices, so there are 2^n assignments. For each assignment, we verify that no apple is given to a hamster that does not like it. Verification costs O(n), so total work is O(n·2^n), which becomes unnecessary even for n = 100.

The structure of the problem makes brute force overkill because there is no global constraint interaction beyond individual compatibility. Each apple is independent. That means we do not need to search at all; we only need to assign locally per apple.

The key observation is that every apple falls into one of three categories: liked only by Arthur, liked only by Alexander, or liked by both (or potentially neither). Since the statement guarantees a solution exists, apples that are liked by neither must not exist in a problematic way, or they can be assigned arbitrarily without breaking validity. So each position can be decided independently.

This reduces the problem to a simple scan: for each apple, assign it to any hamster that likes it. If both like it, choose either consistently or arbitrarily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Greedy assignment | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read n, a, b and the two preference lists.

We will convert preference lists into fast lookup structures so we can test membership in constant time.
2. Build two boolean arrays or sets: one for Arthur’s liked apples and one for Alexander’s liked apples.

This ensures O(1) membership checks per apple.
3. Initialize an answer array of length n.
4. Iterate over all apples from 1 to n.

For each apple, decide its owner based only on preferences.
5. If the apple is liked by Arthur and not necessarily restricted, assign it to Arthur (output 1).

This choice is arbitrary in overlap cases but consistent and safe.
6. Otherwise, assign it to Alexander (output 2).

Since the input guarantees feasibility, every apple must be liked by at least one hamster, so this fallback is always valid.
7. Print the resulting assignment.

### Why it works

The correctness comes from independence of decisions. Each apple has no dependency on any other apple. The only constraint is local validity: an apple assigned to Arthur must be in Arthur’s set, and similarly for Alexander. Because we only assign apples to hamsters that like them, every constraint is satisfied. Overlaps do not create conflicts because we never assign an apple to a hamster who dislikes it. Since each apple is processed exactly once and assigned immediately, there is no possibility of later contradiction.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, a, b = map(int, input().split())

arthur = set(map(int, input().split()))
alex = set(map(int, input().split()))

res = []

for i in range(1, n + 1):
    if i in arthur:
        res.append("1")
    else:
        res.append("2")

print(" ".join(res))
```

### Implementation Notes

We use sets for membership checks because they give average O(1) lookup, which keeps the solution linear.

The decision rule prioritizes Arthur whenever possible. This is arbitrary; choosing Alexander first would also work as long as we respect membership constraints.

We print space-separated characters as required by the statement format.

## Worked Examples

### Example 1

Input:

```
4 2 3
1 2
2 3 4
```

We build:

Arthur = {1, 2}

Alexander = {2, 3, 4}

Now we process each apple:

| i | in Arthur | in Alexander | decision |
| --- | --- | --- | --- |
| 1 | yes | no | 1 |
| 2 | yes | yes | 1 |
| 3 | no | yes | 2 |
| 4 | no | yes | 2 |

Output:

```
1 1 2 2
```

This demonstrates that overlaps (apple 2) are safely resolved without conflict.

### Example 2

Input:

```
3 1 2
1
2 3
```

Arthur = {1}

Alexander = {2, 3}

| i | in Arthur | in Alexander | decision |
| --- | --- | --- | --- |
| 1 | yes | no | 1 |
| 2 | no | yes | 2 |
| 3 | no | yes | 2 |

Output:

```
1 2 2
```

This shows clean separation when preferences do not overlap.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each apple is processed once with O(1) set lookup |
| Space | O(n) | Sets store up to n elements |

The constraints n ≤ 100 are far above what is needed for this solution. Even if n were much larger (like 2e5), the same approach would still be optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO as _StringIO

    n, a, b = map(int, sys.stdin.readline().split())
    arthur = set(map(int, sys.stdin.readline().split()))
    alex = set(map(int, sys.stdin.readline().split()))

    res = []
    for i in range(1, n + 1):
        if i in arthur:
            res.append("1")
        else:
            res.append("2")

    return " ".join(res)

# provided sample
assert run("4 2 3\n1 2\n2 3 4\n") == "1 1 2 2"

# all liked by Arthur only
assert run("3 3 0\n1 2 3\n\n") == "1 1 1"

# all liked by Alexander only
assert run("3 0 3\n\n1 2 3\n") == "2 2 2"

# overlap everywhere
assert run("2 2 2\n1 2\n1 2\n") == "1 1"

# single element
assert run("1 1 1\n1\n1\n") in ["1", "2"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mixed sample | 1 1 2 2 | overlap handling |
| all Arthur | 1 1 1 | single-valid-assignment case |
| all Alexander | 2 2 2 | fallback correctness |
| full overlap | 1 1 | arbitrary tie-breaking |
| n=1 case | 1 or 2 | boundary condition |
