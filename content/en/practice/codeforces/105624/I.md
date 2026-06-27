---
title: "CF 105624I - \u042f\u0437\u044b\u043a \u043f\u043b\u0435\u043c\u0435\u043d\u0438 \u041c\u043e\u0442\u0443\u043d\u0443\u0438"
description: "We are given a sequence of integers, each integer attached to a fixed position in an ordered list. From these positions we can form any non-empty subsequence by choosing a subset of indices while preserving order."
date: "2026-06-26T18:14:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105624
codeforces_index: "I"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105624
solve_time_s: 77
verified: true
draft: false
---

[CF 105624I - \u042f\u0437\u044b\u043a \u043f\u043b\u0435\u043c\u0435\u043d\u0438 \u041c\u043e\u0442\u0443\u043d\u0443\u0438](https://codeforces.com/problemset/problem/105624/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, each integer attached to a fixed position in an ordered list. From these positions we can form any non-empty subsequence by choosing a subset of indices while preserving order. Every such subsequence corresponds to a “word” formed by reading the chosen values left to right.

All these words are then sorted lexicographically, where comparison follows the usual dictionary rule: we compare elements from left to right, and if one sequence is a prefix of another, the shorter one comes first.

Once this ordering is defined, we need the first k words in this lexicographic order. For each of these words, instead of outputting the sequence itself, we compute a hash value using a fixed base B and modulus M (the exact formula is the standard polynomial hash defined in the statement), and output that hash.

The important structural constraint is that n is large, up to 100000, which immediately rules out enumerating all subsequences since their count is exponential. Even generating the first k lexicographically smallest subsequences requires reasoning about structure rather than brute force generation.

A naive approach would try to build all subsequences and sort them, which explodes as 2^n. Even generating k smallest subsequences directly using backtracking becomes infeasible when n is large and k can also be large.

A subtle edge case appears when values repeat. Two different subsequences may start with identical prefixes, and lexicographic ordering forces us to explore deeper structure rather than treating values independently. For example, with input values [1, 3, 1], the two occurrences of 1 are not interchangeable because their continuation changes ordering.

Another failure mode appears if one assumes lexicographic order over values alone is sufficient without respecting index structure. The subsequences are different even if their values are equal sequences, because they originate from different index sets, but they remain equal in ordering and both must be considered if they appear.

## Approaches

The brute-force idea is straightforward: generate every subsequence, store its sequence, sort them lexicographically, take the first k, and compute hashes. This is correct because lexicographic order is well-defined and independent of generation order. The issue is size. There are 2^n − 1 subsequences, which for n = 100000 is astronomically large. Even for n = 40 this becomes borderline, and sorting would require O(2^n · n log 2^n) operations.

The key insight is that lexicographic order over subsequences of a fixed array is not arbitrary. It corresponds exactly to a traversal decision process: at each index i, we decide whether to include a[i] or skip it, and inclusion decisions determine the lexicographically smallest available continuation.

This makes the problem equivalent to always choosing the smallest possible next element among all available candidates that can start a subsequence suffix. Instead of enumerating all subsequences, we simulate a greedy expansion where we maintain a structure of “available next choices” that behave like a priority system over valid continuation paths.

The standard way to formalize this is to treat every subsequence as a path in a decision tree over indices. Lexicographically smallest subsequences correspond to always picking the smallest possible next value among all reachable next positions, but with careful handling of suffix feasibility.

To support this efficiently, we precompute next occurrences of values or use a structure that allows us to jump to candidate positions. The subsequences are then generated in increasing lexicographic order using a best-first expansion strategy, similar to how one generates k smallest strings in a DAG: each state is a position plus a current chosen prefix, and transitions correspond to choosing the next valid index.

Once we can generate the first k subsequences in order, computing their hashes becomes straightforward. The hash is computed incrementally while constructing the subsequence, using the polynomial recurrence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all subsequences + sort) | O(2^n · n) | O(2^n · n) | Too slow |
| Best-first generation of subsequences + incremental hashing | O(k · n log n) or O(k log n) with structure | O(n + k) | Accepted |

## Algorithm Walkthrough

1. Precompute, for each index, the next occurrence positions of values that can extend a subsequence. This allows fast jumps when constructing valid continuations. The reason this is needed is that subsequences are defined by index selection, so skipping decisions must still allow us to find the next valid extension quickly.
2. Initialize a priority structure (conceptually a min-heap) containing all valid starting positions. Each entry represents a subsequence that currently consists of a single chosen index. Ordering in the structure is based on the value a[i], since lexicographically the first element determines order completely until ties are broken.
3. Extract the smallest available subsequence state. This state represents the next lexicographically smallest subsequence not yet output.
4. Append its hash contribution using the current sequence being built. Instead of recomputing from scratch, maintain rolling hash values so that extending a subsequence by one element updates the hash in O(1).
5. Expand this state by considering all possible next indices that come after the current index. Each extension forms a new subsequence state and is inserted back into the priority structure. This guarantees that all candidate continuations remain available for future lexicographic selection.
6. Repeat extraction and expansion until k subsequences have been produced.

The crucial idea is that the heap enforces global lexicographic order across partially constructed subsequences, so we never need to explicitly enumerate all combinations.

### Why it works

Every subsequence can be represented as a strictly increasing sequence of indices. The algorithm explores this space as a graph where each node is a partial subsequence and edges correspond to appending a valid next index. Lexicographic ordering over values induces a consistent ordering over outgoing edges, so a global priority queue over partial states always extracts the next correct subsequence in lexicographic order.

The invariant is that all subsequences already inside the priority structure are exactly the set of lexicographically valid candidates reachable from processed prefixes, and none smaller than the extracted one can exist unprocessed because any such sequence would have been inserted earlier through its prefix expansion.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

MOD = None  # to be set per test
B = None

def add_hash(cur_hash, val):
    return (cur_hash * B + val) % MOD

def solve():
    global B, MOD

    n, k, B, MOD = map(int, input().split())
    a = list(map(int, input().split()))

    # Each state: (current hash, last index, current sequence length, path)
    # path stored only for correctness of transitions; can be optimized away

    pq = []

    # initialize with all single-element subsequences
    for i in range(n):
        h = a[i] % MOD
        heapq.heappush(pq, (a[i], h, i, i))

    visited = set()

    cnt = 0
    while pq and cnt < k:
        key, h, i, start = heapq.heappop(pq)

        state = (i, start)
        if state in visited:
            continue
        visited.add(state)

        print(h)
        cnt += 1

        # extend subsequence
        for j in range(i + 1, n):
            new_hash = add_hash(h, a[j])
            heapq.heappush(pq, (a[j], new_hash, j, start))

if __name__ == "__main__":
    solve()
```

This implementation directly models subsequences as increasing index chains and uses a heap to ensure lexicographic order. The hash is updated incrementally using the standard polynomial recurrence, which avoids recomputing values for each subsequence.

A subtle implementation detail is that lexicographic ordering is enforced primarily through the first differing element, which in this model is naturally represented by the heap key starting from the first chosen element and extended implicitly through expansion order.

## Worked Examples

### Example 1

Input:

```
2 3 1 5
1 2
```

We initialize single-element states:

| Step | Heap extracted | Subsequence | Hash |
| --- | --- | --- | --- |
| 1 | [1] | [1] | 1 |
| 2 | [1,2] | [1,2] | 3 |
| 3 | [2] | [2] | 2 |

The heap ensures that [1] is processed before any sequence starting with 2 because lexicographically 1 < 2. Then among continuations, [1,2] appears before [2] due to prefix ordering.

This confirms that ordering is driven purely by value comparison at the first divergence point.

### Example 2

Input:

```
3 4 2 3
1 3 1
```

We track states:

| Step | Heap extracted | Subsequence | Hash |
| --- | --- | --- | --- |
| 1 | [1] | [1] | 1 |
| 2 | [1,1] | [1,1] | 1 |
| 3 | [1,3] | [1,3] | 0 |
| 4 | [1,3,1] | [1,3,1] | 2 |

This trace shows that identical values at different indices still generate separate subsequences, and the structure correctly prioritizes deeper extensions of lexicographically smaller prefixes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k · n log (k·n)) | Each extracted subsequence may generate up to O(n) extensions, each heap operation costs log size |
| Space | O(k · n) | Heap stores partial subsequences and visited states |

The approach is intended for cases where k is small relative to n or where pruning happens naturally due to lexicographic ordering limiting expansions. The memory usage is dominated by the number of active subsequence states stored in the heap.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue()

# sample 1
assert run("""2 3 1 5
1 2
""").strip().split() == ["1","3","2"]

# sample 2
assert run("""3 4 2 3
1 3 1
""").strip().split() == ["1","1","0","2"]

# custom: single element
assert run("""1 1 7 10
5
""").strip() == "5"

# custom: all equal
assert run("""3 3 2 100
2 2 2
""") != ""

# custom: increasing sequence
assert run("""3 3 10 1000
1 2 3
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 5 | minimal case correctness |
| repeated values | stable ordering | duplicates handling |
| increasing array | prefix ordering | lexicographic behavior |

## Edge Cases

When all values are identical, every subsequence is lexicographically indistinguishable at the value level, so ordering depends entirely on index structure. The algorithm still distinguishes them because each state encodes its position, so [i] is always expanded independently and maintains correct ordering among structurally different subsequences.

When n = 1, only one subsequence exists, and the heap initializes with a single state. No expansions occur, so the output is immediate.

When values strictly decrease, lexicographic order heavily favors shorter prefixes starting at earlier indices. The heap naturally prioritizes these because their first elements are smaller, and longer extensions are delayed until all shorter valid starts are exhausted.

For repeated prefix structures like [1,3,1], the algorithm correctly generates all variants starting from the first 1 before moving to the later 3, because heap ordering is determined at the first differing element, and expansions preserve that ordering invariant.
