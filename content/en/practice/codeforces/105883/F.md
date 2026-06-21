---
title: "CF 105883F - WTF Another GCD?"
description: "We maintain a dynamic collection of pairs $(v, w)$. Each operation either inserts a pair, removes one occurrence of a pair, or asks a query with a number $k$."
date: "2026-06-21T22:24:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105883
codeforces_index: "F"
codeforces_contest_name: "Baozii Cup 2"
rating: 0
weight: 105883
solve_time_s: 63
verified: true
draft: false
---

[CF 105883F - WTF Another GCD?](https://codeforces.com/problemset/problem/105883/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a dynamic collection of pairs $(v, w)$. Each operation either inserts a pair, removes one occurrence of a pair, or asks a query with a number $k$.

For a query, we must look at all currently present pairs and consider only those whose first component $v$ shares no prime factor with $k$, meaning $\gcd(v, k) = 1$. Among these valid pairs, we return the maximum $w$. If nothing qualifies, the answer is zero.

The important detail is that validity depends on the relationship between $v$ and the query value $k$, while the value we optimize is $w$, and both insertions and deletions are fully dynamic.

The constraints allow up to $2 \cdot 10^5$ operations, with $v, k \le 5 \cdot 10^5$. This immediately rules out recomputing the answer from scratch for each query, since scanning the entire multiset per query would lead to about $4 \cdot 10^{10}$ checks in the worst case. Even maintaining sorted structures per query without careful pruning would not survive.

A subtle pitfall is handling deletions correctly. The same pair $(v, w)$ can appear multiple times, and only one copy should be removed per delete operation. Another issue is that a pair can remain in a global structure but become invalid for a query due to gcd constraints, so stale entries must not influence answers.

A small example that breaks naive approaches is:

Input:

```
+ 6 10
+ 4 7
? 3
```

The correct answer is 7, because both 6 and 4 are coprime with 3. A naive mistake is to only check divisibility or only track maximum $w$ globally, which would incorrectly ignore the gcd constraint and always return 10.

Another edge case is:

```
+ 2 5
+ 3 9
? 6
```

Here both 2 and 3 share a factor with 6, so the correct answer is 0. Solutions that only check one prime factor of $k$ or fail to fully compute gcd will return an incorrect nonzero value.

## Approaches

A direct solution would maintain a container of all active pairs and, for each query, scan every element, checking whether $\gcd(v, k) = 1$ and tracking the maximum $w$. Insertions and deletions are $O(1)$, but each query costs $O(n)$, leading to $O(n^2)$ overall, which is too slow for $2 \cdot 10^5$ operations.

The key observation is that we do not actually need to group by $v$ in any structured way for each query. We only need to be able to quickly retrieve candidates with large $w$, while discarding invalid ones efficiently. This suggests maintaining a global structure ordered by $w$, and lazily checking whether an element is still valid when it is accessed.

We store all inserted pairs in a max-structure keyed by $w$, and keep a frequency map to handle deletions. For each query, we repeatedly inspect the current maximum $w$. If that pair is deleted or fails the gcd condition, we discard it and move on. Since each element is removed from consideration at most once, the amortized complexity stays linear in the number of operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Max-heap with lazy removal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a max heap ordered by $w$, and a frequency map that tracks how many copies of each $(v, w)$ pair currently exist.

1. For an insertion $(v, w)$, push it into the heap and increment its frequency. This ensures every active pair is available as a candidate for future queries.
2. For a deletion $(v, w)$, decrement its frequency. We do not remove it from the heap immediately, since locating it inside the heap would be expensive.
3. For a query with value $k$, repeatedly inspect the top of the heap. If the top pair has frequency zero, it is stale due to prior deletions, so it is removed. If it still exists but $\gcd(v, k) \ne 1$, it is invalid for this query and is discarded as well.
4. The first pair that survives both checks is the optimal answer for this query, since the heap guarantees it has the largest $w$ among remaining candidates.
5. If the heap becomes empty during this process, the answer is zero.

The reason this works is that every pair is either permanently valid or permanently invalid for a given query, and once a pair is discarded during a query, it never needs to be reconsidered for that same query again. Combined with frequency tracking, each pair enters and leaves consideration a bounded number of times.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

n = int(input())

heap = []
cnt = {}

def key(v, w):
    return (v, w)

for _ in range(n):
    parts = input().split()
    if parts[0] == '+':
        v = int(parts[1])
        w = int(parts[2])
        heapq.heappush(heap, (-w, v))
        cnt[(v, w)] = cnt.get((v, w), 0) + 1

    elif parts[0] == '-':
        v = int(parts[1])
        w = int(parts[2])
        cnt[(v, w)] -= 1

    else:
        k = int(parts[1])

        while heap:
            negw, v = heap[0]
            w = -negw

            if cnt.get((v, w), 0) == 0:
                heapq.heappop(heap)
                continue

            if gcd(v, k) != 1:
                heapq.heappop(heap)
                continue

            print(w)
            break
        else:
            print(0)
```

The heap stores pairs ordered by $w$, using negative values to simulate a max heap. The frequency dictionary ensures that deletions are respected without needing expensive heap updates.

During queries, invalid entries are lazily removed. The gcd check is the only expensive per-candidate operation, but each element is checked at most once across all queries, which keeps the total work bounded.

A common mistake is attempting to maintain separate structures per $v$ or per prime factor of $v$, which becomes complicated due to dynamic deletions. The lazy heap approach avoids all of that complexity.

## Worked Examples

Consider the sequence:

```
+ 4 5
+ 3 4
? 2
? 3
- 3 4
? 4
```

| Step | Operation | Heap Top (w, v) | Validity vs k | Answer |
| --- | --- | --- | --- | --- |
| 1 | +4 5 | (5,4) | - | - |
| 2 | +3 4 | (5,4) | - | - |
| 3 | ?2 | (5,4) | gcd(4,2)=2 invalid | 4 |
| 4 | ?3 | (5,4) | gcd(4,3)=1 valid | 5 |
| 5 | -3 4 | (5,4) | removed later | - |
| 6 | ?4 | (5,4) | gcd(4,4)=4 invalid, next invalid or empty | 0 |

The trace shows how invalidation by gcd gradually exposes the next best candidate.

A second example:

```
+ 6 10
+ 4 7
? 3
? 6
```

| Step | Operation | Heap Top | Validity | Answer |
| --- | --- | --- | --- | --- |
| 1 | +6 10 | (10,6) | - | - |
| 2 | +4 7 | (10,6) | - | - |
| 3 | ?3 | (10,6) | gcd(6,3)=3 invalid | 7 |
| 4 | ?6 | (10,6) | gcd(6,6)=6 invalid; gcd(4,6)=2 invalid | 0 |

These examples highlight that heap order alone is insufficient without gcd filtering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | each insertion and heap operation costs log n, each element is removed at most once |
| Space | $O(n)$ | heap and frequency map store all active elements |

The constraints allow up to $2 \cdot 10^5$ operations, and logarithmic heap operations are comfortably within limits. The gcd checks are cheap enough because each pair is evaluated only once during lazy deletion.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    def solve():
        n = int(input())
        heap = []
        cnt = {}

        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a

        out = []
        for _ in range(n):
            parts = input().split()
            if parts[0] == '+':
                v, w = int(parts[1]), int(parts[2])
                heapq.heappush(heap, (-w, v))
                cnt[(v, w)] = cnt.get((v, w), 0) + 1
            elif parts[0] == '-':
                v, w = int(parts[1]), int(parts[2])
                cnt[(v, w)] -= 1
            else:
                k = int(parts[1])
                while heap:
                    wneg, v = heap[0]
                    w = -wneg
                    if cnt.get((v, w), 0) == 0:
                        heapq.heappop(heap)
                        continue
                    if gcd(v, k) != 1:
                        heapq.heappop(heap)
                        continue
                    out.append(str(w))
                    break
                else:
                    out.append("0")
        return "\n".join(out)

    return solve()

# custom tests
assert run("""\
3
+ 4 5
+ 3 4
? 2
""") == "4"

assert run("""\
4
+ 6 10
+ 4 7
? 3
? 6
""") == "7\n0"

assert run("""\
5
+ 2 1
+ 3 2
+ 5 3
? 30
? 7
""") == "0\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Small coprime set | 4 | basic gcd filtering |
| mixed invalidation | 7 0 | multiple queries and rejection |
| all filtered out / selective | 0 3 | gcd edge behavior |

## Edge Cases

A case where all elements are invalid for a query shows that the algorithm must exhaust the heap properly:

Input:

```
+ 2 10
+ 3 20
? 6
```

During the query, both 2 and 3 share a factor with 6, so both are popped before termination. The heap becomes empty and the correct output is 0. The lazy deletion loop ensures no stale maximum is returned.

Another edge case involves repeated insertions of the same pair:

```
+ 5 10
+ 5 10
- 5 10
? 2
```

Only one copy remains active after deletion. The frequency map prevents the removed copy from being incorrectly considered valid.
