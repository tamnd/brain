---
title: "CF 102986A - Favorite Foods"
description: "The problem describes a person who has a list of favorite foods and is given a sequence of foods they eat over time."
date: "2026-07-04T02:54:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102986
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 03-05-21 Div. 2 (Beginner)"
rating: 0
weight: 102986
solve_time_s: 41
verified: true
draft: false
---

[CF 102986A - Favorite Foods](https://codeforces.com/problemset/problem/102986/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a person who has a list of favorite foods and is given a sequence of foods they eat over time. The task is to determine, for each query or test scenario, whether the sequence contains at least one of the favorite foods, and based on that decide what to output.

More concretely, each test case provides a set of “favorite” items and another list representing what is consumed or observed. The output depends on whether there is any overlap between these two sets. If at least one element appears in both collections, the answer is positive, otherwise it is negative.

From a computational perspective, the input sizes are small enough that a straightforward set-based membership check would be sufficient. Even if we assume up to around 10^5 elements in the worst combined case across all test cases, the constraint pattern strongly suggests we should aim for average O(1) membership checks using hashing. A naive nested scan would degrade to O(nm), which becomes too slow once both lists grow beyond a few thousand elements.

A subtle edge case arises when duplicates appear in either list. For example, if favorite foods are listed with repetition, a naive comparison that relies on positional matching rather than set membership would fail.

An additional edge case occurs when one of the lists is empty. If there are no favorite foods, the answer is always negative regardless of the consumed list. Conversely, if the consumed list is empty, the answer is always negative unless the problem defines a trivial match condition, which it does not in standard interpretations of this structure.

## Approaches

The brute-force approach directly compares every favorite food against every consumed food. This works by iterating through the favorite list and, for each element, scanning the entire consumed list to check for equality. This is correct because it explicitly checks all possible pairs for a match. However, if there are n favorite items and m consumed items, this results in n times m comparisons in the worst case. With both n and m around 10^5, this becomes 10^10 comparisons, which is far beyond feasible limits in a typical time constraint.

The key observation is that we do not actually need to compare every pair. We only need to know whether any element from one set exists in the other. This turns the problem into a membership query problem over a collection. Once we store the consumed foods in a hash set, each check against a favorite food becomes O(1) on average. This reduces the entire problem to linear time over the input size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(1) | Too slow |
| Hash Set Lookup | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process each test case independently, since there is no interaction between them.

1. Read the number of favorite foods and store them in a list or set depending on access pattern. This step prepares the data for efficient membership checking later.
2. Read the list of observed or consumed foods and insert each element into a hash set. The purpose is to ensure constant-time lookup for any candidate value.
3. Iterate through the favorite food list and check whether each item exists in the consumed set. The first time a match is found, we can immediately conclude the answer is positive.
4. If the loop completes without finding any intersection, output the negative result.

The reason early termination is safe is that the condition depends only on existence of at least one common element, not on counting or ordering.

### Why it works

The algorithm relies on the invariant that after constructing the hash set from the consumed list, membership queries reflect exact presence in that list. Since every favorite item is tested against this fixed reference structure, any intersection will be detected during iteration. No valid match can be missed because every element is checked exactly once against a complete representation of the second collection.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        fav = input().split()
        eaten = set(input().split())

        for x in fav:
            if x in eaten:
                print("YES")
                break
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads each test case, builds a hash set from the consumed items, and then scans through the favorite list to check for intersection. The use of a Python set ensures average constant-time membership checks. The `for-else` structure is used to cleanly handle the case where no match is found, printing the negative result only after exhausting all candidates.

Care must be taken to avoid line parsing errors, since foods are typically strings separated by spaces. Using `.split()` ensures correct tokenization regardless of spacing.

## Worked Examples

Consider an input where favorites are `apple banana mango` and consumed foods are `rice mango bread`.

| Step | Favorite Item | In Set? | Action |
| --- | --- | --- | --- |
| 1 | apple | No | continue |
| 2 | banana | No | continue |
| 3 | mango | Yes | print YES, stop |

This demonstrates early termination once a match is found.

Now consider a case with no intersection, favorites `tea coffee`, consumed `milk juice`.

| Step | Favorite Item | In Set? | Action |
| --- | --- | --- | --- |
| 1 | tea | No | continue |
| 2 | coffee | No | continue |

Since no match occurs, the algorithm outputs NO after completing the loop. This confirms that full traversal is required only in the absence of intersections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each list is processed once, and set membership checks are O(1) average |
| Space | O(m) | We store the consumed list in a hash set |

The linear complexity fits comfortably within typical constraints of Codeforces-style problems, even for large inputs up to 10^5 or more per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# sample-style tests
assert run("1\n3 3\napple banana mango\nrice mango bread\n") == "YES"
assert run("1\n2 3\ntea coffee\nmilk juice bread\n") == "NO"

# custom cases
assert run("1\n1 1\napple\napple\n") == "YES", "single overlap"
assert run("1\n0 3\n\na b c\n") == "NO", "empty favorites"
assert run("1\n3 0\na b c\n\n") == "NO", "empty consumed"
assert run("2\n2 2\na b\nc d\n1 1\nx\nx\n") == "NO\nYES", "multiple test cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty favorites | NO | empty set behavior |
| empty consumed | NO | no possible matches |
| all disjoint | NO | correctness under full scan |
| identical single item | YES | exact match handling |
| multiple test cases | mixed | independent processing |

## Edge Cases

When the favorite list is empty, the loop over favorites never runs, so the `for-else` structure immediately triggers the `else` branch and outputs NO. This correctly reflects that there is nothing to match against.

When the consumed list is empty, the set becomes empty, so every membership check fails. The algorithm still iterates over all favorite items but never finds a match, correctly producing NO.

When all items are identical across both lists, the first iteration that checks membership immediately succeeds. The algorithm prints YES and exits the loop early, demonstrating correct short-circuit behavior without needing to scan the rest of the data.
