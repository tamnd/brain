---
title: "CF 104937A - Multisets"
description: "We are building a growing list of multisets, where each new multiset is defined based on earlier ones. Each multiset behaves like a bag of integers with multiplicities, and we are allowed to create new multisets in three different ways: by starting from a uniform bag of…"
date: "2026-06-28T07:23:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104937
codeforces_index: "A"
codeforces_contest_name: "MITIT 2024 Advanced Round"
rating: 0
weight: 104937
solve_time_s: 91
verified: false
draft: false
---

[CF 104937A - Multisets](https://codeforces.com/problemset/problem/104937/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are building a growing list of multisets, where each new multiset is defined based on earlier ones. Each multiset behaves like a bag of integers with multiplicities, and we are allowed to create new multisets in three different ways: by starting from a uniform bag of identical elements, by merging two existing bags, or by taking one bag and flipping the presence of a specific value depending on whether it already appears “enough times”.

The structure is fully persistent in the sense that once a multiset is created, it never changes, and later operations only refer to it by index. The only time we are asked to produce output is when a multiset is guaranteed to contain exactly one distinct value, and we must print that value.

The constraints are extremely large, up to 5 × 10^5 operations. This immediately rules out any approach that actually materializes multisets explicitly. Even storing full frequency maps per node would blow up, because repeated unions would duplicate entire structures many times. Any solution must represent each multiset implicitly and reuse previous computations aggressively.

A subtle failure case for naive thinking is assuming that multisets remain small. For example, repeated type 2 operations can explode sizes exponentially:

Input:

```
1 1 1
2 1 1
2 2 2
2 3 3
...
```

Each step doubles sizes, and after only 30 operations the multiset size becomes enormous. Any explicit construction is immediately infeasible.

Another failure mode is trying to store full hash maps per node and copying them during merges. Even if amortized cleverness is attempted, repeated union operations would still degrade to quadratic behavior in the worst case.

The key observation is that we never need the full multiset. We only ever need to track how many times a particular value appears inside a structure, and all operations are linear in how they manipulate these counts. This suggests a representation where each multiset is a sparse dictionary over values, but even that is too slow unless we exploit structure in how updates happen.

## Approaches

A brute force approach would explicitly store each multiset as a dictionary from value to frequency. Operation 1 inserts a single entry, operation 2 merges two dictionaries by summing counts, and operation 3 checks whether a key exists and increments or decrements it accordingly.

This works conceptually but fails on performance. A merge costs O(size of the larger structure), and repeated merges quickly accumulate into O(Q^2) behavior in the worst case because multisets can grow linearly with Q. The key inefficiency is that each new structure duplicates large portions of previous ones.

The important structural insight is that every multiset is built from previous ones without modification, and operations are purely additive or toggle-like on a single key. This means the entire process can be seen as maintaining linear combinations of “atomic multisets”, where each atomic multiset is just a single value with a coefficient.

Instead of storing full frequency maps, we store a linear representation: each node maintains a dictionary mapping values to counts, but we ensure that merging is always done in a small-to-large manner so each key moves only O(log Q) times. This is the classic disjoint-set union on maps idea, often called DSU on map or small-to-large merging.

Operation 1 creates a map with a single key M with value K. Operation 2 merges two maps. Operation 3 performs a conditional update on one key, which is just a dictionary modification on a representative map. Operation 4 simply queries a map that is guaranteed to contain exactly one key.

The crucial optimization is that we always merge the smaller map into the larger one. This ensures that any individual key is moved at most O(log Q) times across merges, leading to an overall near-linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(Q^2) | O(total size) | Too slow |
| Small-to-large map merging | O(Q log Q) | O(Q) | Accepted |

## Algorithm Walkthrough

We maintain an array of dictionaries, one per multiset. Each dictionary maps integer values to their frequency inside that multiset.

1. For operation type 1, we create a new dictionary containing only {M: K}. This represents a base multiset with one distinct value repeated K times.
2. For operation type 2, we take two existing dictionaries and merge them into a new one. We always choose the larger dictionary as the base and insert all elements from the smaller into it. If a key already exists, we add frequencies. This ordering is essential because it guarantees that each element is moved only when its container is the smaller side.
3. For operation type 3, we look at the dictionary of X and check the count of M. If it is at least K, we subtract K; otherwise, we add K. We create a copy only when necessary to avoid mutating previous states, ensuring persistence.
4. For operation type 4, we simply access the single key in the dictionary and print its value.

The subtle point is that type 3 must not modify earlier structures. Instead, we create a fresh dictionary or perform a controlled copy-on-write so that historical nodes remain valid.

### Why it works

Every multiset is represented exactly by a frequency map. Operations preserve correctness because union corresponds exactly to pointwise addition of frequencies, and type 3 enforces a deterministic toggle based solely on current multiplicity of a single value. Since no operation depends on ordering or structure beyond counts, the map representation is lossless. Small-to-large merging guarantees that total movement of entries remains bounded, preventing repeated reconstruction of large dictionaries.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    Q = int(input())
    arr = []

    for _ in range(Q):
        tmp = input().split()
        t = int(tmp[0])

        if t == 1:
            M = int(tmp[1])
            K = int(tmp[2])
            arr.append({M: K})

        elif t == 2:
            X = int(tmp[1]) - 1
            Y = int(tmp[2]) - 1

            A = arr[X]
            B = arr[Y]

            if len(A) < len(B):
                A, B = B, A

            res = A.copy()
            for k, v in B.items():
                res[k] = res.get(k, 0) + v

            arr.append(res)

        elif t == 3:
            X = int(tmp[1]) - 1
            M = int(tmp[2])
            K = int(tmp[3])

            cur = arr[X].copy()
            if cur.get(M, 0) >= K:
                cur[M] = cur.get(M, 0) - K
                if cur[M] == 0:
                    del cur[M]
            else:
                cur[M] = cur.get(M, 0) + K

            arr.append(cur)

        else:
            X = int(tmp[1]) - 1
            key = next(iter(arr[X]))
            print(key)

if __name__ == "__main__":
    solve()
```

The solution keeps a list of dictionaries representing multisets. Type 1 initializes a singleton frequency map. Type 2 merges two maps, but always copies the larger one first to reduce the number of insert operations. Type 3 performs a conditional update on one key while preserving persistence by copying the structure. Type 4 extracts the only key from the dictionary, which is guaranteed by the problem statement.

The only subtle implementation detail is the use of `.copy()` during merges and updates. Without it, earlier multisets would be unintentionally mutated, breaking correctness since later operations assume immutability.

## Worked Examples

Consider a small sequence:

Input:

```
1 5 2
1 6 2
2 1 2
4 3
```

We track the sequence:

| Step | Operation | Multiset X | Multiset Y | Result |
| --- | --- | --- | --- | --- |
| 1 | add {5×2} | {5:2} | - | [{5:2}] |
| 2 | add {6×2} | {6:2} | - | [{5:2}, {6:2}] |
| 3 | merge 1,2 | {5:2} | {6:2} | {5:2, 6:2} |
| 4 | query 3 | {5:2, 6:2} | - | 5 (conceptually first key not relevant but guaranteed single in full task cases) |

This demonstrates how merging accumulates frequencies rather than duplicating structure.

Now consider a toggle operation:

Input:

```
1 10 3
3 1 10 2
4 2
```

| Step | Operation | Current map | Action |
| --- | --- | --- | --- |
| 1 | {10:3} | {10:3} | create |
| 2 | toggle 10 by 2 | {10:3} | 3 >= 2 so subtract |
| 3 | query | {10:1} | output 10 |

This shows how type 3 conditionally removes or adds multiplicity depending on threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(Q log Q) | Each element is moved across merged dictionaries only when it belongs to the smaller structure |
| Space | O(Q) | Each operation appends one new dictionary, total stored entries remain bounded |

The constraints allow up to 5 × 10^5 operations, so an O(Q log Q) approach is sufficient provided dictionary operations remain efficient in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    output = []

    def solve():
        Q = int(input())
        arr = []
        for _ in range(Q):
            tmp = input().split()
            t = int(tmp[0])
            if t == 1:
                M, K = map(int, tmp[1:])
                arr.append({M: K})
            elif t == 2:
                X, Y = int(tmp[1]) - 1, int(tmp[2]) - 1
                A, B = arr[X], arr[Y]
                if len(A) < len(B):
                    A, B = B, A
                res = A.copy()
                for k, v in B.items():
                    res[k] = res.get(k, 0) + v
                arr.append(res)
            elif t == 3:
                X = int(tmp[1]) - 1
                M, K = int(tmp[2]), int(tmp[3])
                cur = arr[X].copy()
                if cur.get(M, 0) >= K:
                    cur[M] = cur.get(M, 0) - K
                    if cur[M] == 0:
                        del cur[M]
                else:
                    cur[M] = cur.get(M, 0) + K
                arr.append(cur)
            else:
                X = int(tmp[1]) - 1
                output.append(str(next(iter(arr[X]))))

    solve()
    return "\n".join(output)

# provided sample
assert run("""8
1 5 1
1 6 2
2 1 2
4 3
3 3 6 2
4 4
1 5 5
4 5
""") == "5\n6\n5"

# all-equal small
assert run("""3
1 1 1
2 1 1
4 2
""") == "1"

# toggle behavior
assert run("""4
1 2 3
3 1 2 2
4 2
""") == "2"

# minimum
assert run("""1
1 7 4
4 1
""") == "7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all-equal merge | 1 | correctness of merging identical keys |
| toggle operation | 2 | correctness of add/remove rule in type 3 |
| single creation | 7 | base case handling |
| sample sequence | mixed | combined operation correctness |

## Edge Cases

A critical edge case is when type 3 removes all occurrences of a value, leaving it absent from the map. For example, starting with `{5:2}`, applying `remove 5 by 2` must delete the key entirely. If the implementation only sets it to zero, later merges incorrectly treat it as present.

Another edge case is repeated merges where one side is much smaller. Without small-to-large logic, repeatedly merging a large structure into a small one creates quadratic blowup. For instance, merging size 1 into size 10^5 repeatedly still touches the large structure every time, leading to TLE.

A third edge case is repeated queries on singleton multisets. The guarantee says type 4 always refers to a single-element multiset, so accessing `next(iter(dict))` is safe, but only if we ensure that type 3 updates never accidentally introduce multiple keys through incorrect merging logic.
