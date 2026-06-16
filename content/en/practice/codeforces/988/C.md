---
title: "CF 988C - Equal Sums"
description: "We are given several independent integer arrays. From each array we are allowed to remove exactly one element, and this creates a “modified sum” for that array, meaning the original sum minus the removed element."
date: "2026-06-17T00:47:39+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 988
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 486 (Div. 3)"
rating: 1400
weight: 988
solve_time_s: 83
verified: false
draft: false
---

[CF 988C - Equal Sums](https://codeforces.com/problemset/problem/988/C)

**Rating:** 1400  
**Tags:** implementation, sortings  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent integer arrays. From each array we are allowed to remove exactly one element, and this creates a “modified sum” for that array, meaning the original sum minus the removed element. The task is to pick two different arrays and choose one removal position in each so that the resulting modified sums become equal.

Rephrasing this in a more structural way, for each sequence we can compute its total sum, and every element in it defines a candidate value obtained by subtracting that element from the total. The problem reduces to finding two sequences that can produce the same such candidate value.

The constraints are tight in a very specific way. The total number of elements across all sequences is at most 200,000, and there can be up to 200,000 sequences. Any solution that attempts to compare every pair of sequences directly would require quadratic behavior in the number of sequences, which is far beyond feasible limits. Even per-sequence quadratic operations are disallowed because the total length is large. This pushes us toward a linear or near-linear aggregation strategy over all elements.

A naive pitfall comes from treating the problem as “match two sequences by comparing all possible removals independently.” For example, if we generate all sums-after-deletion for each sequence and then try to match them globally, we might forget that the same target sum can appear multiple times within a single sequence, and that we must ensure the two chosen removals come from different sequences.

Another subtle failure case occurs if we only store the best removal per sequence or only consider unique sums per sequence. A sequence like `[1, 1, 1]` produces the same candidate sum multiple times, and ignoring multiplicity can eliminate valid matches.

## Approaches

The brute-force idea is straightforward: for each sequence, try removing each element and compute the resulting sum, then compare all pairs of sequences and all their possible removals. If we denote total elements by N, each sequence contributes O(n_i) candidates, so overall there are O(N) candidates, but pairing them across sequences leads to O(N^2) comparisons in the worst case.

This works conceptually because every valid answer must appear somewhere in this complete set of “sum after removing one element” values. The failure point is scale: with 200,000 elements, quadratic comparison produces on the order of 10^10 operations.

The key observation is that each candidate is fully determined by two values: the sequence sum S and the element a removed, producing value S − a. Instead of expanding all candidates, we can process elements one by one and try to detect collisions of these values globally.

We maintain a hash map from “target sum after removal” to the first pair (sequence index, element index) that produces it. As soon as a second occurrence of the same target appears from a different sequence, we immediately have a valid answer.

This transforms the problem into a single pass over all elements with constant-time hashing per element.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We treat every element as defining a potential “resulting sum” if it were removed.

### Steps

1. Compute the sum of each sequence.

This is required because every candidate value depends on subtracting an element from its sequence sum.
2. For every sequence i and every element a at position x, compute the value:

S_i − a.

This represents the sum that would remain after removing that element.
3. Maintain a hash map where the key is this computed value, and the value stores a pair (i, x) describing which sequence and which index produced it first.

We store only the first occurrence because we only need to detect a collision.
4. While iterating, if we compute a value that already exists in the map, and it comes from a different sequence, we immediately return both stored positions.

This guarantees we found two different sequences producing the same reduced sum.
5. If no collision is found after processing all elements, output NO.

### Why it works

Every valid solution corresponds to a value V such that there exist two sequences i and j and elements x in i and y in j satisfying S_i − a[i][x] = S_j − a[j][y]. Our map stores every seen pair (V → first occurrence). The first time a duplicate V appears from another sequence, we have exactly the required equality. Since we process all possible removals exactly once, no valid answer can be missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    k = int(input())
    
    seq = []
    total = []
    
    for i in range(k):
        n = int(input())
        arr = list(map(int, input().split()))
        seq.append(arr)
        total.append(sum(arr))
    
    seen = {}
    
    for i in range(k):
        arr = seq[i]
        S = total[i]
        for j, val in enumerate(arr):
            key = S - val
            if key in seen:
                pi, pj = seen[key]
                if pi != i:
                    print("YES")
                    print(pi + 1, pj + 1)
                    print(i + 1, j + 1)
                    return
            else:
                seen[key] = (i, j)
    
    print("NO")

if __name__ == "__main__":
    solve()
```

The solution begins by reading all sequences and precomputing their sums, since repeated sum computation would otherwise increase the complexity. The main logic then iterates over every element once, computing the candidate reduced sum.

The hash map `seen` stores the first occurrence of each candidate value. When a duplicate appears from a different sequence, we immediately output the two positions. The index checks ensure we never match an element with another element from the same sequence, which would violate the requirement of choosing two distinct sequences.

One subtle implementation detail is storing zero-based indices internally but printing one-based indices, since the problem expects 1-based output.

## Worked Examples

### Example trace

Input:

```
2
3
1 2 3
2
3 3
```

| i | j | value | key = S - value | seen state | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 5 | {5:(0,0)} | store |
| 0 | 1 | 2 | 4 | {5:(0,0),4:(0,1)} | store |
| 0 | 2 | 3 | 3 | {5,4,3} | store |
| 1 | 0 | 3 | 3 | collision with (0,2) | answer |

We detect that removing 3 from both sequences gives equal remaining sums.

This confirms the invariant that identical keys correspond exactly to equal “post-removal sums.”

### Second example

Input:

```
3
2
1 5
2
2 4
2
3 3
```

| i | j | value | key | seen state | action |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 5 | {(5):(0,0)} | store |
| 0 | 1 | 5 | 1 | {(5):(0,0),(1):(0,1)} | store |
| 1 | 0 | 2 | 4 | ... | store |
| 1 | 1 | 4 | 2 | ... | store |
| 2 | 0 | 3 | 3 | ... | store |
| 2 | 1 | 3 | 3 | collision within same sequence ignored |  |

No valid cross-sequence collision occurs, so output is NO.

This shows why same-sequence collisions are ignored: they do not satisfy the requirement of choosing two distinct arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each element is processed once with O(1) hash operations |
| Space | O(N) | Hash map stores at most one entry per element |

The total number of elements is at most 200,000, so a linear scan with hashing easily fits within time limits. Memory usage is also safe because each element contributes only a constant amount of stored metadata.

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
assert run("""2
5
2 3 1 3 2
6
1 1 2 2 2 1
""") == """YES
2 6
1 2"""

# minimum case impossible
assert run("""2
1
5
1
7
""") == "NO"

# simple positive case
assert run("""2
2
1 2
2
2 1
""").startswith("YES")

# identical sequences
assert run("""2
3
1 1 1
3
1 1 1
""").startswith("YES")

# larger mix
assert run("""3
2
1 5
2
2 4
2
3 3
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 sequences, single elements | NO | minimal impossibility |
| symmetric pairs | YES | basic correctness |
| identical arrays | YES | repeated values handling |
| 3 sequences no match | NO | multi-sequence failure case |

## Edge Cases

A key edge case is when multiple elements in the same sequence generate identical candidate sums. For example, `[1, 1, 1]` produces the same reduced sum three times. The algorithm stores only the first occurrence but still processes later duplicates, ensuring they can match against other sequences if needed.

Another case is when the only collisions occur within a single sequence. Consider `[2,2]` and `[1,3]`. The value 2 appears twice in the first sequence, but that does not form a valid answer. The check `pi != i` prevents false positives.

A final case is when sequences are large but no match exists. The algorithm still performs a full linear scan without early assumptions, and the hash map remains bounded by O(N), ensuring predictable behavior even in worst-case inputs.
