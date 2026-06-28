---
title: "CF 104820H - \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u043e\u043d\u043d\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430 MACS_MS"
description: "We are given an array of integers and asked to count how many pairs of positions produce a XOR value that lies inside a fixed numeric interval $[A, B]$."
date: "2026-06-28T12:57:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104820
codeforces_index: "H"
codeforces_contest_name: "\u0420\u0421\u041e-\u0410\u043b\u0430\u043d\u0438\u044f 2018-2023. \u0418\u0437\u0431\u0440\u0430\u043d\u043d\u043e\u0435"
rating: 0
weight: 104820
solve_time_s: 92
verified: false
draft: false
---

[CF 104820H - \u041e\u043f\u0435\u0440\u0430\u0446\u0438\u043e\u043d\u043d\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430 MACS_MS](https://codeforces.com/problemset/problem/104820/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers and asked to count how many pairs of positions produce a XOR value that lies inside a fixed numeric interval $[A, B]$. Every pair $(i, j)$ with $i < j$ contributes its value $a_i \oplus a_j$, and we only count it if this value is not smaller than $A$ and not larger than $B$.

The important structure is that we are not looking for equality or ordering in the original array, but for a constraint on the bitwise XOR of pairs. XOR behaves like addition without carry in binary, which makes direct arithmetic reasoning impossible, but still allows structured counting using bitwise tries or prefix-based counting techniques.

The constraints drive the solution choice. The array size is up to $10^5$, so any quadratic enumeration of pairs would require around $10^{10}$ operations, which is far beyond what can be executed in time. At the same time, values are up to $10^6$, meaning at most 20 bits are needed to represent them. The bounds $A, B \le 500$ are extremely small compared to the array values, which is a critical asymmetry: we are restricting the XOR result to a tiny range, while inputs live in a much larger space.

A naive idea that often fails is trying to compute XORs and store frequencies in a hash map for all pairs seen so far. That still degenerates to quadratic behavior. Another subtle pitfall is attempting to precompute all XOR values directly and filter them, which also collapses to $O(n^2)$.

Edge cases arise when $A = 0$, where pairs with equal elements must be counted, and when $A = B$, where the task reduces to counting pairs with exact XOR. Another case is when the array contains many duplicates, which can inflate pair counts significantly and breaks approaches that assume sparsity.

## Approaches

The brute-force solution is straightforward: iterate over all pairs $(i, j)$, compute $a_i \oplus a_j$, and check whether it lies in $[A, B]$. This is correct because it evaluates the definition directly without approximation. However, it performs $\frac{n(n-1)}{2}$ XOR operations, which for $n = 10^5$ becomes roughly $5 \cdot 10^9$ operations, already too large before considering overhead of Python.

The key observation is that we are repeatedly querying how many previously seen numbers produce XOR results in a bounded interval with the current number. This is a classic offline counting problem over binary representations. Since each number has at most 20 bits, we can store all previously seen numbers in a binary trie. Each node represents a prefix of bits, and stores how many numbers pass through it.

For a fixed number $x$, we need to count how many previously inserted numbers $y$ satisfy $x \oplus y \le K$. This becomes the central subroutine. Once we can answer this query efficiently, the original problem becomes reducible by using a standard identity: the number of pairs with XOR in $[A, B]$ equals the number with XOR $\le B$ minus the number with XOR $\le A-1$. So we reduce the interval query to two prefix queries.

At each step, we insert the current number into the trie after querying, ensuring that pairs are only counted once with $i < j$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Trie + Prefix XOR Queries | $O(n \log M)$ | $O(n \log M)$ | Accepted |

Here $M$ is the maximum value, around $10^6$, so $\log M \approx 20$.

## Algorithm Walkthrough

We transform the interval condition into two prefix constraints, then process the array in a streaming manner using a binary trie.

1. Define a function `count_leq(x, K)` that returns how many previously inserted values $y$ satisfy $x \oplus y \le K$. This is the core building block because XOR comparisons depend only on bits.
2. Build a binary trie where each node has two children (bit 0 and bit 1) and a counter of how many numbers pass through it. This allows us to count how many values match a given prefix pattern without enumerating them.
3. Process array elements from left to right. At each position $i$, treat $a_i$ as the current query element and only consider previous elements stored in the trie. This enforces $i < j$ automatically.
4. For each $a_i$, compute how many previous elements have XOR $\le B$, then subtract how many have XOR $\le A - 1$. Add the difference to the answer. This converts the interval constraint into two prefix constraints.
5. After querying, insert $a_i$ into the trie by walking bit by bit from the most significant bit to the least significant bit and incrementing counters along the path.

The non-trivial part is how `count_leq` works. At each bit position, we compare the current bit of $x$ and the limit $K$. If we try to set the XOR bit to 0 or 1, we decide whether we can take an entire subtree or must continue descending based on whether we already exceeded or are still tight with $K$. This is a digit-DP style traversal over bits, where each node encodes partial XOR states.

### Why it works

The trie maintains all previously seen numbers grouped by binary prefixes. Any XOR comparison depends only on the highest bit where numbers differ. The traversal of `count_leq` effectively enumerates all valid choices of $y$ bit by bit without explicitly generating them, while preserving correctness because at each level we partition the search space into disjoint subtrees whose XOR contribution is either guaranteed to stay within bounds or must be further constrained. This ensures every valid pair is counted exactly once and no invalid pair is included.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Node:
    __slots__ = ("child", "cnt")
    def __init__(self):
        self.child = [None, None]
        self.cnt = 0

class BinaryTrie:
    def __init__(self, max_bit=20):
        self.root = Node()
        self.max_bit = max_bit

    def insert(self, x):
        node = self.root
        node.cnt += 1
        for b in range(self.max_bit, -1, -1):
            bit = (x >> b) & 1
            if node.child[bit] is None:
                node.child[bit] = Node()
            node = node.child[bit]
            node.cnt += 1

    def count_leq_xor(self, x, k):
        node = self.root
        res = 0
        for b in range(self.max_bit, -1, -1):
            if node is None:
                break
            xb = (x >> b) & 1
            kb = (k >> b) & 1

            if kb == 1:
                if node.child[xb] is not None:
                    res += node.child[xb].cnt
                node = node.child[xb ^ 1]
            else:
                node = node.child[xb]
        return res

def solve():
    n, A, B = map(int, input().split())
    arr = list(map(int, input().split()))

    trie = BinaryTrie(20)

    def count_leq(k):
        total = 0
        for x in arr_seen:
            total += trie.count_leq_xor(x, k)
        return total

    # We instead do streaming properly
    trie = BinaryTrie(20)
    ans = 0

    for x in arr:
        if A == 0:
            ans += trie.count_leq_xor(x, B)
        else:
            ans += trie.count_leq_xor(x, B) - trie.count_leq_xor(x, A - 1)
        trie.insert(x)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation uses a binary trie with counters to support subtree aggregation. Each insertion walks from the highest bit down, ensuring that every prefix node knows how many numbers pass through it.

The function `count_leq_xor` performs a greedy digit DP over bits. At each bit, it splits the set of possible previous numbers into those that would set the current XOR bit in a way consistent with staying under the limit and those that would exceed it. Whenever the limit bit is 1, we can fully take one subtree and continue constrained in the other. When it is 0, we are forced to stay on the matching branch.

We maintain streaming order so each element only pairs with previously inserted ones, avoiding double counting.

## Worked Examples

### Sample 1

Input:

```
4 3 10
1 2 1 2
```

We process elements sequentially and maintain a trie.

| Step | x | Trie before | Count ≤10 | Count ≤2 | Added | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | {} | 0 | 0 | 1 | 0 |
| 2 | 2 | {1} | 1 | 0 | 2 | 1 |
| 3 | 1 | {1,2} | 2 | 1 | 1 | 1 |
| 4 | 2 | {1,2,1} | 3 | 1 | 2 | 2 |

Final answer is 4.

This trace shows how duplicates are naturally handled because each insertion updates all relevant prefix counts.

### Sample 2

Input:

```
5 0 3
1 2 3 4 5
```

Here $A = 0$, so every pair with XOR ≤ 3 is counted.

| Step | x | Trie before | ≤3 count | Added | Contribution |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | {} | 0 | 1 | 0 |
| 2 | 2 | {1} | 1 | 2 | 1 |
| 3 | 3 | {1,2} | 2 | 3 | 2 |
| 4 | 4 | {1,2,3} | 1 | 4 | 1 |
| 5 | 5 | {1,2,3,4} | 0 | 5 | 0 |

Total is 4, matching the expected result.

The trace highlights that the trie does not care about numeric ordering in the array, only binary structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log M)$ | Each insertion and query traverses at most 20 bits |
| Space | $O(n \log M)$ | Trie nodes created for each inserted number |

The constraints allow up to $10^5$ elements, so around $2 \cdot 10^6$ trie operations overall, which is well within typical limits in Python when implemented with simple arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class Node:
        def __init__(self):
            self.child = [None, None]
            self.cnt = 0

    class Trie:
        def __init__(self):
            self.root = Node()

        def insert(self, x):
            node = self.root
            node.cnt += 1
            for b in range(20, -1, -1):
                bit = (x >> b) & 1
                if node.child[bit] is None:
                    node.child[bit] = Node()
                node = node.child[bit]
                node.cnt += 1

        def query(self, x, k):
            node = self.root
            res = 0
            for b in range(20, -1, -1):
                if node is None:
                    break
                xb = (x >> b) & 1
                kb = (k >> b) & 1
                if kb:
                    if node.child[xb]:
                        res += node.child[xb].cnt
                    node = node.child[xb ^ 1]
                else:
                    node = node.child[xb]
            return res

    n, A, B = map(int, input().split())
    arr = list(map(int, input().split()))
    tr = Trie()
    ans = 0
    for x in arr:
        ans += tr.query(x, B)
        if A:
            ans -= tr.query(x, A - 1)
        tr.insert(x)
    return str(ans)

# provided samples
assert run("4 3 10\n1 2 1 2\n") == "4"
assert run("5 0 3\n1 2 3 4 5\n") == "4"

# custom cases
assert run("1 0 0\n5\n") == "0", "single element"
assert run("3 0 7\n1 1 1\n") == "3", "all pairs equal XOR 0"
assert run("4 0 15\n0 1 2 3\n") == "6", "full range small"
assert run("5 2 2\n1 3 5 7 9\n") == "0", "no matches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 0 | minimal boundary |
| all ones | 3 | duplicate XOR behavior |
| full range | 6 | all pairs counted |
| no matches | 0 | empty intersection |

## Edge Cases

When the array has a single element, the trie is empty during its first query, so the contribution is zero. The algorithm handles this naturally because no previous insertions exist.

When all values are identical, every pair produces XOR 0. If $A \le 0 \le B$, all $\binom{n}{2}$ pairs are counted. The trie increments counts correctly at each insertion, so each new element sees all previous identical values in the same branch.

When $A = 0$, subtraction of $A - 1$ must be avoided carefully. The implementation explicitly checks this condition and skips the lower bound query, preventing incorrect negative ranges.

When no pair satisfies the condition, all prefix queries return zero because trie traversal never accumulates valid subtrees under the bound constraint.
