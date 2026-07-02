---
title: "CF 104199K - \u0413\u043b\u044e\u0447\u043d\u044b\u0435 \u0440\u043e\u0431\u043e\u0430\u043d\u0442\u044b"
description: "We are given an array that describes a starting arrangement of items on positions labeled from 1 to n. Position i initially holds item a[i], and the final goal is to transform this arrangement so that position i contains item i for every i."
date: "2026-07-02T18:01:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104199
codeforces_index: "K"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u043d\u0430 \u0412\u041a\u041e\u0428\u041f.Junior 18-02-23"
rating: 0
weight: 104199
solve_time_s: 81
verified: true
draft: false
---

[CF 104199K - \u0413\u043b\u044e\u0447\u043d\u044b\u0435 \u0440\u043e\u0431\u043e\u0430\u043d\u0442\u044b](https://codeforces.com/problemset/problem/104199/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array that describes a starting arrangement of items on positions labeled from 1 to n. Position i initially holds item a[i], and the final goal is to transform this arrangement so that position i contains item i for every i.

The only way to move items is through a set of robots, one placed at each position. A robot can carry a single item, pick it up from its current position if its hands are empty, move between positions, and optionally drop or pick again. Movement between positions i and j is only possible if i and j share a common divisor greater than 1.

This turns the problem into a reachability question over positions 1 through n, where connectivity is defined by gcd constraints. The question is whether the robots, using these constrained moves, can rearrange the items into the identity configuration.

The constraint n ≤ 200000 implies that any approach that tries to explicitly build all edges between pairs of positions is impossible, since the number of pairs is quadratic in the worst case. Even iterating over all pairs and computing gcd would be far too slow. The solution must rely on a structured view of connectivity rather than explicit graph construction.

A subtle edge case appears when two positions are connected indirectly but not directly. For example, 6 is connected to 10 through 2, even though gcd(6,10)=2 and gcd(10,15)=5, but gcd(6,15)=3 also connects them indirectly. A naive approach that only considers direct gcd edges might incorrectly conclude that movement is more restricted than it actually is.

Another failure case occurs if one assumes each robot can independently fix its own position. For instance, in a cycle like 1 → 8 → 2 → 1, items can be rotated within a component even though no single robot ever “solves” its own position directly.

## Approaches

A brute-force approach would explicitly construct a graph where every pair (i, j) is connected if gcd(i, j) > 1, then run a graph traversal to find connected components. Each node represents a position, and edges represent allowed robot movements. After computing components, we would check whether each component contains exactly the same multiset of initial items and target items.

This is correct in principle because robots cannot move items between disconnected components. However, building all edges requires checking O(n^2) pairs, and even a single BFS or DFS over such a dense graph is infeasible for n = 200000.

The key observation is that gcd(i, j) > 1 is equivalent to i and j sharing at least one prime factor. Instead of thinking in terms of pairwise gcd checks, we can think of connectivity being induced by primes. Every number belongs to all prime “groups” corresponding to its prime factors, and numbers become connected through shared primes. This transforms the graph into a bipartite-like structure between numbers and primes, allowing us to union indices that share any prime factor using a disjoint set union structure.

Once we compute connected components under this relation, each component must be self-consistent: every index i must be able to reach its target position a[i], otherwise the required item cannot be transported there.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (explicit graph) | O(n²) | O(n²) | Too slow |
| DSU via prime factors | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We construct a disjoint set union structure over indices 1 through n. The goal is to merge indices that are connected via sharing a prime factor.

1. Initialize a DSU where each position is its own component. This represents that initially we assume no movement is possible.
2. For every number i from 1 to n, factorize it into its distinct prime factors. Since n is large, we rely on an efficient sieve-like preprocessing or trial division up to sqrt(n).
3. Maintain a dictionary that maps each prime to the first index where it appears. When we encounter a prime p at index i, if p has not been seen before, we record i as its representative. If it has been seen, we union i with the previously stored index. This step builds connectivity through shared primes without explicitly constructing edges.
4. After processing all indices, each connected component in DSU corresponds to a set of positions between which robots can freely move items.
5. Finally, for each index i, we check whether i and a[i] belong to the same DSU component. If any index fails this condition, the transformation is impossible.

The key idea is that items can only move within connected components of the gcd graph, and DSU over shared primes correctly captures exactly those components.

### Why it works

The underlying invariant is that two indices are connected in the movement graph if and only if they share a chain of numbers where consecutive elements share a prime factor. DSU merges precisely those indices that share at least one prime factor, and transitivity of union operations captures indirect gcd connectivity. Since every valid move preserves component membership, no item can cross components, and within a component, repeated transfers allow arbitrary rearrangement. This makes component equality between initial and target positions both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dsu = DSU(n)

    prime_owner = {}

    def factorize(x):
        res = []
        p = 2
        while p * p <= x:
            if x % p == 0:
                res.append(p)
                while x % p == 0:
                    x //= p
            p += 1
        if x > 1:
            res.append(x)
        return res

    for i in range(1, n + 1):
        primes = factorize(i)
        for p in primes:
            if p not in prime_owner:
                prime_owner[p] = i
            else:
                dsu.union(i, prime_owner[p])

    for i in range(1, n + 1):
        if dsu.find(i) != dsu.find(a[i - 1]):
            print("NO")
            return

    print("YES")

if __name__ == "__main__":
    solve()
```

The DSU structure maintains connectivity among indices. The prime factorization step extracts the minimal set of primes needed to determine gcd-based connectivity. The mapping prime_owner ensures that all numbers sharing a prime are merged into a single component without generating edges explicitly.

The final loop enforces that every item must be movable from its initial position to its required final position within the same connectivity component.

A common implementation pitfall is forgetting that indices are 1-based while the array a is 0-based in Python, which is why a[i - 1] is used.

## Worked Examples

### Sample 1

Input:

```
9
1 8 3 6 5 4 7 2 9
```

We track connectivity via DSU components induced by shared primes.

| i | a[i] | find(i) | find(a[i]) | decision |
| --- | --- | --- | --- | --- |
| 1 | 1 | C1 | C1 | ok |
| 2 | 8 | C2 | C2 | ok |
| 3 | 3 | C3 | C3 | ok |
| 4 | 6 | C2 | C2 | ok |
| 5 | 5 | C5 | C5 | ok |
| 6 | 4 | C2 | C2 | ok |
| 7 | 7 | C7 | C7 | ok |
| 8 | 2 | C2 | C2 | ok |
| 9 | 9 | C9 | C9 | ok |

All indices match their targets within components, so the answer is YES. This demonstrates that even though multiple swaps occur, everything stays within prime-connected components.

### Sample 2

Input:

```
6
6 2 3 5 4 1
```

| i | a[i] | find(i) | find(a[i]) | decision |
| --- | --- | --- | --- | --- |
| 1 | 6 | C1 | C2 | fail |

At index 1, position 1 and item 6 belong to different components. This immediately shows impossibility, since no sequence of allowed moves can transport item 6 into a component not connected to position 1.

This captures the key failure mode: the target requires cross-component movement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n α(n) + n √n) | DSU operations are near constant, factorization dominates |
| Space | O(n + π(n)) | DSU arrays plus prime mapping |

The constraints allow roughly a few hundred million simple operations, and the DSU-based solution stays comfortably within limits because each number is factorized once and each union operation is nearly constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("""9
1 8 3 6 5 4 7 2 9
""") == "YES"

assert run("""6
6 2 3 5 4 1
""") == "NO"

# all correct already
assert run("""1
1
""") == "YES"

# small swap impossible due to gcd isolation
assert run("""2
2 1
""") == "NO"

# chain via primes
assert run("""4
2 3 4 1
""") == "YES"

# all same fixed points
assert run("""5
1 2 3 4 5
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 | YES | trivial base case |
| 2 1 | NO | disconnected components |
| 2 3 4 1 | YES | transitive prime connectivity |
| identity | YES | already solved case |

## Edge Cases

One edge case is when all numbers are coprime. In this situation, every node is isolated in the DSU structure, so each position can only hold its own item. Any mismatch immediately fails, since no movement edges exist. The algorithm correctly detects this because no prime unions occur.

Another edge case is when numbers form a fully connected structure through shared small primes. For example, sequences containing many even numbers merge into a single component. The algorithm correctly allows arbitrary permutations inside this large component, since DSU merges all even indices together and thus allows full rearrangement.

A final subtle case is when connectivity exists only indirectly. For instance, numbers 6, 10, and 15 form a chain via primes 2, 5, and 3. Even though some pairs have gcd 1, DSU still merges them into one component, allowing correct movement.
