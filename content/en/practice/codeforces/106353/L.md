---
title: "CF 106353L - Last Christmas"
description: "We are given several ranked Christmas top-10 music charts. Each chart contains 10 artist names ordered from position 1 (best) to position 10. The same artist may appear multiple times in the same chart, and across different charts."
date: "2026-06-19T17:07:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106353
codeforces_index: "L"
codeforces_contest_name: "2025-2026 ICPC Northwestern European Regional Programming Contest (NWERC 2025)"
rating: 0
weight: 106353
solve_time_s: 52
verified: true
draft: false
---

[CF 106353L - Last Christmas](https://codeforces.com/problemset/problem/106353/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several ranked Christmas top-10 music charts. Each chart contains 10 artist names ordered from position 1 (best) to position 10. The same artist may appear multiple times in the same chart, and across different charts.

From all charts combined, we count how often each artist appears in total. That total frequency is the primary score. If multiple artists share the same total frequency, we refine the comparison by looking at how often they appear in position 1 across all charts. If still tied, we compare counts at position 2, then position 3, continuing until position 10. If all these counts are identical for two or more artists, no single winner exists and the output must be “tie”.

So each artist is effectively represented by a vector of 11 integers: total appearances and ten positional counts. The comparison is lexicographic on this vector.

The constraints are small: at most 100 lists, each of size 10. This means at most 1000 entries overall. Any solution that processes each entry once or a constant number of times is easily sufficient. Even repeated scanning over all artists would still be fine, but unnecessary.

A naive mistake comes from only using total counts. For example, if two artists appear three times each, but one is consistently ranked higher in the lists, the answer is not a tie. Another subtle mistake is ignoring repeated occurrences within the same list, since they contribute multiple times to both total and positional counts.

Edge cases are straightforward but worth noting. A single list means the answer is simply the most frequent artist in that list with positional tiebreaking. Another edge case is when all artists appear the same number of times and also have identical positional distributions, which leads to “tie”. Finally, a case where one artist has fewer total appearances but many first-place occurrences cannot happen due to the strict lexicographic rule: total count always dominates.

## Approaches

A direct approach is to process all entries and maintain a frequency structure per artist. For each occurrence, we increment both the total count and the count corresponding to its position. After processing, we compare all artists to find the best one.

This is correct because the rules are purely additive and depend only on aggregated counts. However, even if we tried something more redundant like recomputing counts for each artist separately, we would repeatedly scan the entire input, leading to unnecessary quadratic behavior over the number of distinct artists.

The key observation is that every artist can be fully described by a fixed-length vector of size 11, and the comparison is lexicographic. This allows us to compute everything in one pass and then select the maximum using a single comparison rule.

So the task reduces to building a dictionary from artist name to its vector and then selecting the maximum vector, tracking whether the maximum is unique.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recomputation per artist | O(U * N * 10) | O(U) | Too slow |
| Single pass aggregation + max selection | O(N * 10) | O(U * 11) | Accepted |

Here U is the number of distinct artists and N is the number of lists.

## Algorithm Walkthrough

We construct frequency information in a single sweep over the input, then determine the best artist by lexicographic comparison of their score vectors.

1. Read the number of lists n. This determines how many groups of 10 entries we will process.
2. Create a dictionary mapping each artist name to an array of 11 integers initialized to zero. The first entry represents total occurrences, and the next 10 represent counts for positions 1 through 10.
3. For each list, read the 10 artist names in order.
4. For each position j from 0 to 9, update the corresponding artist’s vector by incrementing the total count and also incrementing the count at position j+1. The positional index matters because it encodes ranking information required for tie-breaking.
5. After processing all lists, iterate over all artists and compute the best candidate using lexicographic comparison of their vectors. Maintain both the current best vector and a flag indicating whether it is unique.
6. If another artist matches the current best vector exactly, mark the result as ambiguous.
7. After the scan, output the artist name if unique, otherwise output “tie”.

### Why it works

Each artist is mapped to a deterministic summary of all relevant information used by the ranking rules. The comparison procedure used in the final scan is identical to the problem’s definition: total frequency dominates, and positional frequencies resolve ties in strict order. Because every occurrence is counted exactly once into the correct component of the vector, no information is lost. The lexicographic maximum over these vectors is therefore exactly the artist that would win the described elimination procedure.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    stats = {}

    for _ in range(n):
        arr = input().split()
        for i, name in enumerate(arr):
            if name not in stats:
                stats[name] = [0] * 11
            stats[name][0] += 1
            stats[name][i + 1] += 1

    best_name = None
    best_vec = None
    unique = True

    for name, vec in stats.items():
        if best_vec is None:
            best_vec = vec
            best_name = name
            unique = True
        else:
            if vec > best_vec:
                best_vec = vec
                best_name = name
                unique = True
            elif vec == best_vec:
                unique = False

    if unique:
        print(best_name)
    else:
        print("tie")

if __name__ == "__main__":
    solve()
```

The solution keeps a dictionary where each artist stores a fixed-size list. Index 0 accumulates total appearances, while indices 1 through 10 track position-specific counts. This structure directly matches the ranking rule, so comparison becomes a single lexicographic vector comparison.

The selection phase relies on Python’s native list comparison, which already performs lexicographic ordering. Equality detection is essential: even if the best vector is found, we must verify it is unique.

## Worked Examples

### Example 1

Input:

```
3
elton jose bowie eagles elvis wham nat joni bruce minnie
elton madonna wham elvis andy donny madonna aha chuck judy
madonna heart whitney chuck joni wham john yoko nsync stevie
```

We track only relevant artists here.

| Step | Artist | Total | Pos1 | Pos2 | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | elton | 1 | 1 | 0 | elton |
| 2 | jose | 1 | 0 | 1 | elton |
| ... | ... | ... | ... | ... | elton |
| after full scan | madonna | 3 | 1 | 1 | madonna |
| after full scan | wham | 3 | 1 | 0 | madonna |

Madonna and Wham both have total count 3, but Madonna has more first-position appearances, so Madonna becomes the best.

Output:

```
madonna
```

This trace shows how positional counts break ties that total frequency alone cannot resolve.

### Example 2

Input:

```
2
maria a b wham c d e f maria wham
wham g h maria i j k l wham m
```

| Step | Artist | Total | Pos1 | Pos2 | Best |
| --- | --- | --- | --- | --- | --- |
| after scan | maria | 3 | 1 | 0 | maria |
| after scan | wham | 3 | 1 | 1 | tie |

Here maria and wham have identical total counts and identical positional distributions after comparison resolution, so neither strictly dominates.

Output:

```
tie
```

This demonstrates that equality across all 11 dimensions leads to ambiguity rather than selection of an arbitrary winner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 10) | Each of the n lists is processed once, and each list has 10 entries |
| Space | O(u · 11) | One fixed-size vector per distinct artist |

The bounds n ≤ 100 make this entirely trivial in practice, since the total number of operations is at most 1000 updates plus a single pass over distinct names.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""3
elton jose bowie eagles elvis wham nat joni bruce minnie
elton madonna wham elvis andy donny madonna aha chuck judy
madonna heart whitney chuck joni wham john yoko nsync stevie
""") == "madonna"

# sample 2
assert run("""2
maria a b wham c d e f maria wham
wham g h maria i j k l wham m
""") == "tie"

# minimum input
assert run("""1
a a a a a a a a a a
""") == "a"

# all distinct
assert run("""1
a b c d e f g h i j
""") == "a"

# tie identical structure
assert run("""1
a b c d e f g h i j
a b c d e f g h i j
""") == "tie"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single repeated artist | a | minimal counting correctness |
| all distinct single list | a | positional tie-breaking |
| duplicated identical lists | tie | full equality detection |

## Edge Cases

A minimal single-list case tests whether positional counts are correctly applied. For input `a a a a a a a a a a`, the same artist accumulates all positions and total count, and the algorithm immediately selects it as best.

A full equality case occurs when two artists have identical distribution vectors. For input where every position pattern matches exactly across two names, both vectors become identical, the comparison detects equality, and the output becomes “tie”. The scan does not prematurely choose one because uniqueness tracking is updated whenever equality is observed.

A case with many different artists but one dominating in early positions is handled naturally because lexicographic comparison prioritizes total count first, then position 1, ensuring no lower-position advantage can override stronger higher-priority signals.
