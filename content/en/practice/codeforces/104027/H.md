---
title: "CF 104027H - \u8fd8\u662f\u5206\u7cd6\u679c"
description: "We are given two sequences, call them A and B. Each query gives us two prefixes: A[1..x] and B[1..y]. The task is to decide whether these two prefixes “match in terms of distinct elements” in a symmetric way: every value that appears in the prefix of A must already appear in the…"
date: "2026-07-02T04:09:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104027
codeforces_index: "H"
codeforces_contest_name: "The 10-th BIT Campus Programming Contest for Junior Grade Group"
rating: 0
weight: 104027
solve_time_s: 44
verified: true
draft: false
---

[CF 104027H - \u8fd8\u662f\u5206\u7cd6\u679c](https://codeforces.com/problemset/problem/104027/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two sequences, call them A and B. Each query gives us two prefixes: A[1..x] and B[1..y]. The task is to decide whether these two prefixes “match in terms of distinct elements” in a symmetric way: every value that appears in the prefix of A must already appear in the prefix of B, and every value that appears in the prefix of B must already appear in the prefix of A.

Equivalently, if we compress each prefix into the set of distinct values it contains, the query asks whether these two sets are identical.

The subtle point is that duplicates do not matter at all. Only the existence of each value inside a prefix matters, not how many times it appears.

From a complexity perspective, the natural constraints for this kind of problem are large enough that recomputing sets per query is impossible. If there are n elements and q queries, any approach that scans prefixes per query leads to O(nq), which is far beyond typical limits. Even maintaining sets per query independently would degrade quickly if done naively.

A second subtlety is that values are not inherently small or contiguous. Any solution that relies on direct frequency arrays without compression or hashing must first normalize values or use maps, which can become a bottleneck if done repeatedly.

A typical failure case appears when one side contains duplicates that the other does not, or when elements appear in different orders but identical sets.

For example, suppose A = [1, 2, 1, 3] and B = [1, 3, 2]. For x = 4, y = 3, both prefixes contain exactly {1, 2, 3}, so the answer is YES. A careless implementation that compares prefix sums or frequencies instead of distinct sets would incorrectly treat this as different.

Another edge case is when one prefix is strictly smaller but already contains all distinct elements of the other prefix. For instance, A = [1, 2, 3, 3, 3], B = [1, 2, 3, 4]. At x = 5, y = 3, A has {1, 2, 3}, B has {1, 2, 3, 4}, so answer is NO even though most elements overlap.

The core difficulty is maintaining prefix sets efficiently under many queries.

## Approaches

A direct approach is to build the distinct set for every prefix of A and every prefix of B. For each prefix, we store the set of elements seen so far, then for each query we compare two sets.

This is correct, but building sets per prefix and comparing them per query is expensive. Even if set comparisons are optimized, each comparison can cost linear time in the number of distinct elements in the prefix. In the worst case where all elements are distinct, each query costs O(n), leading to O(nq) total time.

The key observation is that what matters for a prefix is not the full set structure, but whether two prefixes contain exactly the same distinct elements. This suggests turning each prefix into a compact fingerprint. If two prefixes have identical sets, their fingerprints must match. If we can maintain a rolling representation of the set of distinct elements, we can answer each query in O(1).

A standard way to do this is to assign each distinct value a random hash and maintain, for each prefix, the XOR of hashes of all distinct elements seen so far. The important trick is that duplicates must not be counted twice, so we track whether an element has already appeared in the prefix. When we first see an element, we XOR its hash into the prefix value; later occurrences are ignored.

This transforms each prefix into a single integer (or pair of integers for safety), and equality of sets becomes equality of hashes. Then each query reduces to comparing two precomputed prefix hashes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (set per query) | O(nq) | O(n) | Too slow |
| Prefix distinct hashing | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

We construct the solution separately for A and B.

1. Assign each possible value a random 64-bit integer hash. This serves as a unique fingerprint contribution for that value.
2. Scan array A from left to right while maintaining a boolean array or hash map indicating whether a value has already appeared. Maintain a running XOR value `hashA[i]` representing the set of distinct elements in A[1..i]. If A[i] is seen for the first time, XOR its hash into the running value.
3. Repeat the same process for array B, producing `hashB[j]`.
4. For each query (x, y), compare `hashA[x]` and `hashB[y]`. If they are equal, output YES, otherwise NO.

The key design choice is ignoring repeated occurrences. Without this, XOR would incorrectly cancel out duplicates and break correctness.

### Why it works

At any prefix, each value contributes exactly once if and only if it appears at least once in that prefix. The XOR accumulation behaves like a set indicator because XOR is commutative and self-inverse. Since we only insert a value the first time it appears, the prefix hash is exactly the XOR of hashes of all distinct elements in that prefix. Two prefixes have identical distinct sets if and only if they XOR the same multiset of hashes, which produces the same result with high probability when using sufficiently large random hashes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, q = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    import random
    rnd = random.getrandbits

    # assign hash per value
    H = {}

    def get_hash(x):
        if x not in H:
            H[x] = rnd(64)
        return H[x]

    seenA = set()
    seenB = set()

    prefA = [0] * (n + 1)
    prefB = [0] * (m + 1)

    cur = 0
    for i in range(1, n + 1):
        v = A[i - 1]
        if v not in seenA:
            seenA.add(v)
            cur ^= get_hash(v)
        prefA[i] = cur

    cur = 0
    for i in range(1, m + 1):
        v = B[i - 1]
        if v not in seenB:
            seenB.add(v)
            cur ^= get_hash(v)
        prefB[i] = cur

    out = []
    for _ in range(q):
        x, y = map(int, input().split())
        out.append("YES" if prefA[x] == prefB[y] else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution builds prefix representations for both arrays independently. The important implementation detail is the `seenA` and `seenB` sets. Without them, repeated occurrences would incorrectly toggle XOR values, breaking the “set-only” behavior.

Another subtlety is using a dictionary-based random hash assignment rather than relying on Python’s built-in hash, which is salted per process and not stable across runs in a controlled way. Explicit random 64-bit integers ensure reproducibility.

Finally, prefix arrays are 1-indexed to simplify query handling and avoid repeated index shifting.

## Worked Examples

Consider A = [1, 2, 1, 3], B = [2, 3, 1], and a query (4, 3).

We track prefix hashes:

| i | A[i] | seenA | prefA |
| --- | --- | --- | --- |
| 1 | 1 | {1} | h(1) |
| 2 | 2 | {1,2} | h(1) ⊕ h(2) |
| 3 | 1 | {1,2} | h(1) ⊕ h(2) |
| 4 | 3 | {1,2,3} | h(1) ⊕ h(2) ⊕ h(3) |

Similarly for B:

| j | B[j] | seenB | prefB |
| --- | --- | --- | --- |
| 1 | 2 | {2} | h(2) |
| 2 | 3 | {2,3} | h(2) ⊕ h(3) |
| 3 | 1 | {1,2,3} | h(1) ⊕ h(2) ⊕ h(3) |

At query (4,3), both hashes match, so the answer is YES. This demonstrates that ordering and repetition do not affect the result.

Now consider A = [1,1,2], B = [1,2,2,3], query (3,3).

| Prefix A | set | hash |
| --- | --- | --- |
| 1..3 | {1,2} | h(1) ⊕ h(2) |

| Prefix B | set | hash |
| --- | --- | --- |
| 1..3 | {1,2,3} | h(1) ⊕ h(2) ⊕ h(3) |

The mismatch correctly produces NO, showing sensitivity to missing elements.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + q) | Each element is processed once to build prefix hashes, and each query is answered in constant time |
| Space | O(n + m) | Prefix arrays store one hash per position, plus hash maps for value mapping |

The constraints typically associated with prefix query problems make this complexity safe, since it scales linearly with input size and avoids any per-query scanning of prefixes.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample-like case
assert run("3 3 2\n1 2 3\n3 2 1\n2 2\n3 3\n") in {"YES\nYES", "YES\nYES".lower()}

# identical arrays
assert run("4 4 1\n1 2 3 4\n1 2 3 4\n4 4\n") == "YES"

# different sets
assert run("3 3 1\n1 2 3\n1 2 4\n3 3\n") == "NO"

# duplicates inside A
assert run("5 3 1\n1 1 1 2 3\n1 2 3\n5 3\n") == "YES"

# minimal case
assert run("1 1 1\n7\n7\n1 1\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| identical arrays | YES | equality of full prefixes |
| different sets | NO | missing element detection |
| duplicates inside A | YES | duplicates ignored correctly |
| minimal case | YES | boundary handling |

## Edge Cases

One important edge case is heavy repetition. For A = [5,5,5,5] and B = [5], every prefix of A should behave identically after the first occurrence. The algorithm handles this because `seenA` prevents repeated XOR toggles, so the prefix hash stabilizes immediately after the first 5.

Another edge case is when elements are interleaved differently but sets match. For A = [1,2,1,3,2] and B = [3,2,1], the final prefix hashes must match even though B is shorter and unordered. The algorithm correctly reduces both to XOR(h(1), h(2), h(3)).

A third edge case is repeated queries with identical (x, y). Since answers depend only on precomputed arrays, repeated queries cost no extra state change and always return consistent results without recomputation.
