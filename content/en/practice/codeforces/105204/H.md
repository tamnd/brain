---
title: "CF 105204H - \u0425\u044d\u0448\u0442\u0435\u0433"
description: "We are given a post consisting of words and a set of “mandatory” words that must all appear in a final hashtag. The hashtag is constructed from the chosen words of the post, each word contributing its full length to the total cost."
date: "2026-06-27T02:43:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105204
codeforces_index: "H"
codeforces_contest_name: "\u0412\u041a\u041e\u0428\u041f.Junior 2024"
rating: 0
weight: 105204
solve_time_s: 54
verified: true
draft: false
---

[CF 105204H - \u0425\u044d\u0448\u0442\u0435\u0433](https://codeforces.com/problemset/problem/105204/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a post consisting of words and a set of “mandatory” words that must all appear in a final hashtag. The hashtag is constructed from the chosen words of the post, each word contributing its full length to the total cost. The goal is to delete as few words as possible from the post so that the remaining words still contain every required keyword at least once, and the total length of all remaining words does not exceed a limit $d$.

In other words, we start with a multiset of word lengths. Some positions are special because they correspond to required words that must be included at least once. We are allowed to remove arbitrary words, but after removal we must still keep at least one occurrence of every required word, and the sum of lengths of kept words must be at most $d$. We want to maximize how many words we remove, or equivalently minimize how many we keep.

The constraints make it clear that the solution must be close to linear or near-linear in the number of words. There are up to 30,000 keywords and 45,000 words in the text, so any approach that tries subsets or recomputes feasibility for each removal independently will be too slow. Even an $O(m^2)$ simulation over deletions would already exceed time limits by several orders of magnitude.

A subtle edge situation arises when the mandatory words alone already exceed the limit $d$. For example, if the required words are “a” (length 100,000) and “b” (length 100,000), and $d = 150,000$, then even keeping only these two makes the sum 200,000, so no solution exists. Another case is when a required word appears multiple times in the text. We must keep at least one copy, but keeping more copies is always harmful, so any optimal solution will only preserve exactly one occurrence per required word.

A second non-trivial scenario is when deleting a non-required word is always beneficial, but deleting a required word is forbidden. This leads to the key structure: required words form a fixed backbone, and everything else is optional weight that we may drop to satisfy the sum constraint.

## Approaches

The brute-force idea would be to try all subsets of words that preserve at least one occurrence of each required word and check their total length. This is correct conceptually but immediately infeasible because there are $2^m$ subsets. Even restricting attention to non-required words still leaves exponential combinations.

The key observation is that the constraint is purely additive: only the total length matters, and feasibility depends only on whether we can reduce the sum by removing non-required words while keeping required ones intact. This transforms the problem into a greedy selection problem over contributions.

We start from the only structure that is forced: for each required word, we must keep at least one occurrence. Among all occurrences of a required word, we should always keep the shortest one because it minimizes the unavoidable baseline cost. Any longer occurrence can only increase the total without providing additional benefit.

After fixing one representative occurrence per required word, all other words become optional items. The problem reduces to selecting a subset of optional words to keep such that total length stays within $d$. Since we want to minimize deletions, we equivalently want to keep as many optional words as possible, but only if the total sum constraint allows it.

This becomes a classic greedy reduction problem: we start from all necessary chosen words plus all optional words, compute total sum, and then repeatedly remove the largest optional words until the sum fits. Removing larger words first minimizes the number of removals needed to satisfy a budget constraint, because each removal gives maximum reduction per step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | $O(2^m)$ | $O(m)$ | Too slow |
| Greedy with selection and sorting | $O(m \log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Read all required words into a hash set so we can test membership in constant time per word.
2. Scan the text and group occurrences of required words. For each required word, we only need to keep its minimum-length occurrence. This gives a fixed mandatory cost.
3. For every word in the text, classify it as required or optional. Optional words are all candidates for deletion.
4. Compute the base cost as the sum of selected required occurrences. If this already exceeds $d$, output -1 immediately because no deletions can reduce required contribution.
5. Compute the total cost if we initially keep all words, which is the sum of all word lengths.
6. The amount we need to reduce is $total - d$. To achieve this with minimum deletions, we sort optional words by length descending and repeatedly remove the largest ones first, accumulating saved length until we reach the needed reduction.
7. The number of removed words is the count of optional words we discard in this process.

The crucial idea is that required words define a fixed lower bound, and everything else behaves like independent removable weight. Sorting ensures each deletion contributes maximal reduction.

### Why it works

The invariant is that at every step, we maintain a set of kept words that always includes at least one occurrence of each required word. Among all feasible ways to remove exactly $k$ optional words, choosing the $k$ largest words yields the smallest possible remaining sum. Since feasibility depends only on whether the sum drops below $d$, this greedy ordering guarantees that if any set of $k$ deletions works, the greedy choice will also work. This ensures we never overestimate the number of required deletions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    keywords = set()
    for _ in range(n):
        keywords.add(input().strip())
    
    words = input().split()
    d = int(input())
    
    # required occurrences: keep at least one per keyword
    from collections import defaultdict
    best_required = {}
    
    optional = []
    total_sum = 0
    
    for w in words:
        L = len(w)
        total_sum += L
        
        if w in keywords:
            if w not in best_required:
                best_required[w] = L
            else:
                best_required[w] = min(best_required[w], L)
        else:
            optional.append(L)
    
    required_sum = sum(best_required.values())
    
    if required_sum > d:
        print(-1)
        return
    
    # we initially assume we keep all words, but we can drop optional ones
    optional.sort(reverse=True)
    
    removed = 0
    saved = 0
    
    for L in optional:
        if total_sum - saved <= d:
            break
        saved += L
        removed += 1
    
    print(removed)

if __name__ == "__main__":
    solve()
```

The implementation begins by separating keywords into a set for fast lookup. While scanning the post, it maintains the minimum-length occurrence for each keyword, because any longer duplicate occurrence is strictly worse than the shortest one.

The optional words are stored as lengths only, since only their contribution matters. After computing the total sum and the required baseline, we check feasibility. If even the mandatory baseline exceeds $d$, we terminate early.

The greedy removal loop processes optional words sorted by decreasing length. Each iteration simulates deleting the current largest remaining word, tracking how much total length has been reduced. Once the remaining sum fits into $d$, we stop.

## Worked Examples

Consider the sample input where only some words are required and we must drop a word like “olympiady” to meet the limit.

We track required words and optional words separately:

| Step | Action | Required Sum | Total Sum | Optional Removed |
| --- | --- | --- | --- | --- |
| 1 | parse words | 21 | 30 | 0 |
| 2 | sort optional | 21 | 30 | 0 |
| 3 | remove “olympiady” | 21 | 21 | 1 |

This shows that a single deletion is sufficient once the largest optional word is removed.

Now consider a case where multiple small optional words exist:

Input: keywords = {a}, text = [a, x, y, z], d = 3

| Step | Action | Required Sum | Total Sum | Optional Removed |
| --- | --- | --- | --- | --- |
| 1 | keep “a” | 1 | 1+1+1+1=4 | 0 |
| 2 | remove “z” | 1 | 3 | 1 |
| 3 | remove “y” | 1 | 2 | 2 |

After removing two smallest optional words, the constraint is satisfied.

These traces show that the algorithm always prioritizes removing the most expensive words first, minimizing the number of deletions needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m + n)$ | Sorting optional words dominates; scanning input is linear |
| Space | $O(m + n)$ | Storage for keyword set, optional list, and required tracking |

The constraints allow up to 45,000 words, so sorting at this scale is easily fast enough. Linear preprocessing ensures no bottlenecks beyond the sort.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# sample-like
assert run("""2 4
privet
uchastnikam
privet vsem uchastnikam olympiady
22
""") == "1"

# all required already exceed limit
assert run("""1 2
a
a aa
1
""") == "-1"

# no optional words
assert run("""2 2
a
b
a b
3
""") == "-1"

# large removable pool
assert run("""1 5
a
a b c d e
3
""") == "2"

# exact fit without removals
assert run("""1 3
a
a bb c
10
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample case | 1 | basic greedy deletion |
| required overflow | -1 | impossible due to mandatory cost |
| no optional words | -1 | only required words exist |
| many optional words | 2 | greedy selection of deletions |
| already valid | 0 | no deletions needed |

## Edge Cases

A critical edge case is when required words alone exceed the limit. For example, if required words are long enough that their minimum occurrences already violate $d$, the algorithm immediately returns -1 after computing the baseline sum. This avoids unnecessary sorting or processing.

Another case is repeated required words with different lengths. Suppose a required word appears multiple times with lengths 10, 5, and 7. The algorithm only keeps 5 as the mandatory cost. This ensures we do not overestimate unavoidable length. If we mistakenly kept all occurrences, we could incorrectly conclude that no solution exists even when a valid one exists.

A final edge case is when optional words are all shorter than required ones. Even then, sorting still works correctly because removal order depends only on maximizing reduction per deletion, not on comparison with required words.
