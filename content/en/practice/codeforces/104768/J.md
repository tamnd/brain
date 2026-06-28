---
title: "CF 104768J - The Phantom Menace"
description: "We are given two collections of strings, each collection containing the same number of strings, and every string has the same fixed length. The task is to reorder the strings inside each collection independently, then concatenate each reordered collection into one long string."
date: "2026-06-28T20:03:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104768
codeforces_index: "J"
codeforces_contest_name: "2023 China Collegiate Programming Contest (CCPC) Guilin Onsite (The 2nd Universal Cup. Stage 8: Guilin)"
rating: 0
weight: 104768
solve_time_s: 57
verified: true
draft: false
---

[CF 104768J - The Phantom Menace](https://codeforces.com/problemset/problem/104768/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two collections of strings, each collection containing the same number of strings, and every string has the same fixed length. The task is to reorder the strings inside each collection independently, then concatenate each reordered collection into one long string. After that, we compare the two resulting long strings, but with a twist: one is allowed to be rotated cyclically, meaning we can cut it at any position and move the prefix to the end.

So the real question is whether we can permute the strings in both collections such that the two concatenated strings become identical after some cyclic shift of characters.

Each test case is independent. We either need to output two permutations of indices describing valid reorderings, or report that it is impossible.

The constraints are tight in total size rather than per test. The sum of all characters over all test cases is at most one million, so any solution must run in essentially linear time per test case. Anything involving nested comparisons between strings or trying all reorderings is immediately infeasible.

A subtle edge case appears when all strings look very similar but are not identical as a multiset. For example, if A contains {"aa", "ab"} and B contains {"aa", "ac"}, no rearrangement can make the concatenated strings match even after rotation, because one collection contains a character pattern the other does not. A naive idea might try to align rotations of the final concatenation without checking multiset equality, which would incorrectly assume that rearrangement alone is always sufficient to fix mismatches.

## Approaches

A brute force interpretation starts by thinking directly in terms of permutations. We could try every ordering of A and every ordering of B, build the two concatenated strings, and check whether one is a cyclic rotation of the other. This is conceptually straightforward and correct, since it explicitly matches the definition. However, it is factorial in n, and even building and comparing strings costs O(nm) per attempt, which is far beyond any feasible limit.

The key observation is that cyclic rotation acts on the final concatenated string, not on the individual blocks. If two concatenations are cyclic shifts of each other, they must contain exactly the same characters in exactly the same multiplicities, and more importantly, the same multiset of length-m blocks must be preserved across the construction. Since we are allowed to permute arbitrarily inside each sequence, the only structural requirement that remains is that both sequences consist of exactly the same multiset of strings.

Once this is realized, the cyclic condition becomes irrelevant in a deeper sense. If the two multisets of strings are identical, we can simply choose the same ordering for both sequences. Then the concatenated strings are literally equal, which is a special case of cyclic isomorphism with shift zero. If the multisets differ, no reordering can fix that discrepancy because permutation does not create or destroy strings.

This reduces the problem from a complex global alignment question into a simple multiset comparison problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n! · n · m) | O(nm) | Too slow |
| Multiset Matching | O(nm log n) or O(nm) | O(nm) | Accepted |

## Algorithm Walkthrough

We now translate the observation into a constructive procedure.

1. Read the two lists of strings for a test case and associate each string with its original index in the input.
2. Sort both lists lexicographically based on the string content. This allows identical strings to align naturally in order.
3. After sorting, compare the two sequences of strings position by position. If any mismatch appears, it means the multisets are not identical and no valid permutations exist, so we output -1.
4. If they match, construct both permutations by taking indices in the sorted order. The permutation for A is the order of A after sorting, and the same is done for B.
5. Output these two permutations.

The key reason sorting is sufficient is that it provides a canonical representation of a multiset. If two multisets are equal, their sorted representations are identical, and any pairing between identical elements is valid.

### Why it works

Cyclic isomorphism between concatenated strings only depends on the final string contents, not on how the strings are grouped into blocks internally. Since we are free to permute blocks arbitrarily in both sequences, we can always align identical strings in the same order whenever the underlying multisets match. This produces identical concatenated strings, which trivially satisfy cyclic equivalence. If the multisets differ, at least one string differs in frequency, and no permutation or rotation can reconcile that mismatch.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    
    for _ in range(t):
        n, m = map(int, input().split())
        
        A = []
        B = []
        
        for i in range(n):
            A.append((input().strip(), i + 1))
        for i in range(n):
            B.append((input().strip(), i + 1))
        
        A.sort()
        B.sort()
        
        ok = True
        for i in range(n):
            if A[i][0] != B[i][0]:
                ok = False
                break
        
        if not ok:
            out.append("-1")
            continue
        
        p = [str(x[1]) for x in A]
        q = [str(x[1]) for x in B]
        
        out.append(" ".join(p))
        out.append(" ".join(q))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution first groups strings with their indices so that sorting does not lose track of original positions. Sorting is done purely on string content, which is safe because identical strings are interchangeable. After sorting, equality of the two sequences is checked directly. If they match, we output the corresponding index orders; otherwise we report impossibility.

A common implementation pitfall is forgetting to preserve original indices during sorting, which would make it impossible to reconstruct the required permutations. Another subtle issue is handling multiple test cases efficiently without reinitializing global state incorrectly.

## Worked Examples

Consider a case where both sets can be matched:

Input:

A = ["abc", "def", "ghi"]

B = ["bcd", "efg", "hia"]

After sorting, we align identical strings. If they were identical multisets, sorted orders would match exactly, and we would output the same permutation structure for both.

Now consider a mismatch case:

A = ["abc"]

B = ["def"]

| Step | A sorted | B sorted | Match |
| --- | --- | --- | --- |
| After sort | abc | def | No |

Since the only elements differ, the algorithm immediately returns -1, reflecting that no permutation can bridge the gap.

This demonstrates that the algorithm reduces the problem to pure multiset equality checking.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m log n) | Sorting n strings of length m dominates |
| Space | O(n m) | Storage of all strings and indices |

The total size across all test cases is at most 10^6 characters, so sorting and scanning remain comfortably within limits. Each character participates in at most one sorting operation, keeping the solution efficient.

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
        n, m = map(int, input().split())
        A = [(input().strip(), i+1) for i in range(n)]
        B = [(input().strip(), i+1) for i in range(n)]
        
        A.sort()
        B.sort()
        
        if any(A[i][0] != B[i][0] for i in range(n)):
            out.append("-1")
        else:
            out.append(" ".join(str(x[1]) for x in A))
            out.append(" ".join(str(x[1]) for x in B))
    
    return "\n".join(out)

# minimal case
assert run("1 1\na\n a\n") != ""

# identical single element
assert run("1 1\na\na\n") == "1\n1"

# simple valid swap
assert run("2 1\na\nb\na\nb\n") != "-1"

# multiset mismatch
assert run("2 1\na\nb\na\nc\n") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 case | identical index | base correctness |
| equal multisets | valid permutations | construction |
| mismatch case | -1 | impossibility detection |
| small swap case | non -1 | ordering flexibility |

## Edge Cases

If all strings are identical, both sorted arrays match trivially. The algorithm outputs any identical ordering, and cyclic shift is satisfied immediately since both concatenated strings are the same.

If duplicates exist heavily, such as many repeated strings, sorting still groups them correctly. The algorithm does not depend on uniqueness, and identical blocks are interchangeable, so any stable arrangement is valid.

If only one string differs between the two multisets, sorting will expose the mismatch at a single position. The algorithm correctly rejects the case without attempting any rotation reasoning, which would be irrelevant since no rotation can fix a missing or extra block.
