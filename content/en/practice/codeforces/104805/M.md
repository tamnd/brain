---
title: "CF 104805M - Choosing a name"
description: "We are given four collections of names. Igor has a list of names he likes and a list of names he dislikes. Ira also has a list of names she likes and a list of names she dislikes. A name is considered usable only if both people like it and neither of them explicitly dislikes it."
date: "2026-06-28T13:22:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104805
codeforces_index: "M"
codeforces_contest_name: "Central Russia Regional Contest, 2022"
rating: 0
weight: 104805
solve_time_s: 66
verified: true
draft: false
---

[CF 104805M - Choosing a name](https://codeforces.com/problemset/problem/104805/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four collections of names. Igor has a list of names he likes and a list of names he dislikes. Ira also has a list of names she likes and a list of names she dislikes. A name is considered usable only if both people like it and neither of them explicitly dislikes it. The task is to output every such usable name, without duplicates and sorted lexicographically.

A useful way to think about this is that each person defines two sets: a “must contain” set and a “forbidden” set. The final answer is the intersection of the two must contain sets, with all elements that appear in either forbidden set removed.

The input sizes are small enough that all operations involving hashing or sorting individual names are easily fast enough. Even in the worst case, there are at most a few thousand names total. This immediately rules out anything involving quadratic comparison of strings across lists, since that would imply on the order of 10^6 comparisons per pair of lists, but also suggests that a straightforward use of hash sets or sorting is sufficient.

A subtle issue is duplication inside the input lists. A name can appear multiple times within the same list, which means treating lists as simple arrays and intersecting them positionally would produce duplicates in the output or incorrect filtering. Another issue is that a name might be liked and disliked by the same person. In that case, the dislike should override, because the condition explicitly requires that no one dislikes the chosen name.

A concrete edge case is when a name is liked by both but also appears in one dislike list.

Input:

```
1 1 1 0
alex
alex
alex
```

Here both like “alex” but Igor dislikes it. The correct output is empty. A naive approach that only checks the like lists would incorrectly output “alex”.

Another edge case is duplication causing repeated outputs.

Input:

```
2 2 0 0
mike
mike
mike
mike
```

Correct output:

```
mike
```

A naive intersection over raw lists would output “mike” multiple times unless deduplication is explicitly handled.

## Approaches

The brute-force idea is to treat each name in Igor’s liked list and check whether it appears in Ira’s liked list while also scanning both dislike lists to ensure it is not forbidden. For each candidate name, this requires scanning up to four lists linearly. In the worst case, if all lists contain n elements, this becomes O(n^2) string comparisons. With string comparison costing up to 20 characters, this still becomes comfortably too slow at the upper bound.

The key observation is that membership checks, not scans, are what we actually need. Once we recognize that each condition is purely set-based, each list can be converted into a hash set. Then checking whether a name is valid becomes O(1) average time per condition. The entire problem reduces to building sets for likes and dislikes, intersecting the two like sets, and subtracting the union of dislike sets.

This turns the problem from repeated scanning into a single pass over a candidate set, followed by constant-time filtering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n1 + n2) · (n1 + n2 + m1 + m2)) | O(1) extra | Too slow |
| Optimal (hash sets) | O(n1 + n2 + m1 + m2) | O(n1 + n2 + m1 + m2) | Accepted |

## Algorithm Walkthrough

1. Read all four integer counts, then read all names from input into four separate collections corresponding to Igor likes, Ira likes, Igor dislikes, and Ira dislikes. The grouping matters because each group represents a different constraint role in the final filtering.
2. Insert all names from each list into separate sets. This removes duplicates automatically and transforms membership queries into constant-time operations.
3. Construct a candidate set by taking the intersection of Igor’s liked set and Ira’s liked set. This ensures that every remaining name satisfies the “both like it” requirement.
4. Remove from this candidate set every name that appears in either Igor’s dislike set or Ira’s dislike set. This enforces the constraint that neither person can dislike the chosen name.
5. Convert the final set into a sorted list and output it in lexicographical order. Sorting is required because sets do not preserve order, while the problem explicitly demands ordered output.

The reasoning behind the correctness is that at every stage we are narrowing the universe of names by applying a constraint that is both necessary and sufficient. A name survives the first filter if and only if it is liked by both. A name survives the second filter if and only if it is not explicitly forbidden by either party. No other conditions exist in the problem, so the final set exactly matches the valid answers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n1, n2, m1, m2 = map(int, input().split())

    igor_like = [input().strip() for _ in range(n1)]
    ira_like = [input().strip() for _ in range(n2)]
    igor_bad = [input().strip() for _ in range(m1)]
    ira_bad = [input().strip() for _ in range(m2)]

    s1 = set(igor_like)
    s2 = set(ira_like)
    bad1 = set(igor_bad)
    bad2 = set(ira_bad)

    candidates = s1 & s2
    forbidden = bad1 | bad2

    result = sorted(x for x in candidates if x not in forbidden)

    sys.stdout.write("\n".join(result))

if __name__ == "__main__":
    main()
```

The implementation mirrors the algorithm almost directly. Each input block is immediately converted into a set to ensure both deduplication and efficient lookup. The intersection operator is used to enforce the shared preference condition. The union of dislike sets forms a single exclusion filter, since any appearance in either list disqualifies a name. The final comprehension performs a single pass over the candidate set, and sorting is applied only at the end to satisfy output requirements.

A common implementation mistake is forgetting to deduplicate before sorting, which leads to repeated names in output. Another is applying the dislike filter before intersection incorrectly, which can remove names that should still be considered if they are only disliked by the person who does not require them in the final intersection step.

## Worked Examples

### Example 1

Input:

```
5 4 2 3
kirill
ruslan
sonya
veronika
vasya
ruslan
alina
sonya
veronika
nastya
masha
sasha
masha
natasha
```

We track the transformation step by step.

| Step | Igor like | Ira like | Intersection | Forbidden | Output candidates |
| --- | --- | --- | --- | --- | --- |
| Initial | {kirill, ruslan, sonya, veronika, vasya} | {ruslan, alina, sonya, veronika} | - | - | - |
| After intersection | - | - | {ruslan, sonya, veronika} | - | - |
| After filtering | - | - | - | {masha, sasha, natasha, alina, sonya?, veronika?} | {ruslan, sonya, veronika} |

The final result is sorted:

```
ruslan
sonya
veronika
```

This confirms that only names simultaneously liked and not disqualified survive the filtering pipeline.

### Example 2

Input:

```
3 3 1 1
a
b
c
a
b
d
c
```

Step-by-step:

| Step | Igor like | Ira like | Intersection | Forbidden | Output candidates |
| --- | --- | --- | --- | --- | --- |
| Initial | {a, b, c} | {a, b, d} | - | - | - |
| After intersection | - | - | {a, b} | - | - |
| After filtering | - | - | - | {c, d} | {a, b} |

Final output:

```
a
b
```

This example shows that names appearing only in one dislike list do not affect valid candidates unless they are in the intersection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n1 + n2 + m1 + m2 + k log k) | Building sets is linear, filtering is linear in candidate size, sorting dominates with k candidates |
| Space | O(n1 + n2 + m1 + m2) | Storage for all unique names across input lists |

The constraints are small enough that both linear set operations and sorting a few thousand strings easily fit within limits. Even with worst-case input sizes, the number of string operations remains negligible for a 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys

    n1, n2, m1, m2 = map(int, sys.stdin.readline().split())
    igor_like = [sys.stdin.readline().strip() for _ in range(n1)]
    ira_like = [sys.stdin.readline().strip() for _ in range(n2)]
    igor_bad = [sys.stdin.readline().strip() for _ in range(m1)]
    ira_bad = [sys.stdin.readline().strip() for _ in range(m2)]

    s1 = set(igor_like)
    s2 = set(ira_like)
    bad1 = set(igor_bad)
    bad2 = set(ira_bad)

    res = sorted(x for x in (s1 & s2) if x not in (bad1 | bad2))
    return "\n".join(res).strip()

# sample 1
assert run("""5 4 2 3
kirill
ruslan
sonya
veronika
vasya
ruslan
alina
sonya
veronika
nastya
masha
sasha
masha
natasha
""") == "ruslan\nsonya\nveronika"

# minimal case, no overlap
assert run("""1 1 0 0
a
b
""") == ""

# all overlap, no bad
assert run("""2 2 0 0
a
b
a
b
""") == "a\nb"

# conflict removal
assert run("""2 2 1 0
a
b
a
b
a
""") == "b"

# full exclusion
assert run("""2 2 1 1
a
b
a
b
a
b
""") == ""

# duplicates inside lists
assert run("""4 4 0 0
x
x
y
z
x
y
y
z
""") == "x\ny\nz"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal no overlap | empty | no false positives when intersection is empty |
| all overlap no bad | sorted full set | deduplication and ordering |
| conflict removal | b | dislike overrides like-set membership |
| full exclusion | empty | combined forbidden set works |
| duplicates inside lists | x y z | correct deduplication |

## Edge Cases

One important edge case is when a name appears in both a like list and a dislike list of the same person. For example:

```
1 0 1 0
alex
alex
```

Igor likes and dislikes “alex” simultaneously. In the set construction phase, both “like” and “dislike” sets contain the same element. During candidate formation, “alex” is included only if it exists in both like sets, but since Ira has no likes, it never enters the intersection. The correct output is empty. The algorithm naturally handles this because intersection is computed before filtering, so contradictions inside a single person’s lists do not incorrectly preserve a name.

Another edge case is when all lists contain identical names but all are disliked by at least one person. For instance:

```
1 1 1 1
bob
bob
bob
bob
```

After intersection, “bob” is a candidate, but it is removed because it appears in both dislike sets. The final output is empty, which matches the requirement that any single dislike is disqualifying.
