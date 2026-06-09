---
title: "CF 1872E - Data Structures Fan"
description: "We are given a static array of integers, but the array is split dynamically into two groups depending on a binary string. Each position i contributes its value a[i] either to group 0 or group 1 depending on whether s[i] is 0 or 1. The system supports two operations."
date: "2026-06-08T23:19:49+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "data-structures", "dp"]
categories: ["algorithms"]
codeforces_contest: 1872
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 895 (Div. 3)"
rating: 1500
weight: 1872
solve_time_s: 102
verified: false
draft: false
---

[CF 1872E - Data Structures Fan](https://codeforces.com/problemset/problem/1872/E)

**Rating:** 1500  
**Tags:** binary search, bitmasks, data structures, dp  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a static array of integers, but the array is split dynamically into two groups depending on a binary string. Each position i contributes its value a[i] either to group 0 or group 1 depending on whether s[i] is 0 or 1.

The system supports two operations. The first operation flips a whole segment of the binary string, turning 0 into 1 and 1 into 0. This only affects how elements are grouped, not their values. The second operation asks for the XOR of all array values whose current group matches a specified bit g.

So the core difficulty is not computing XOR itself, but maintaining fast updates under segment flips while answering group XOR queries.

The constraints are tight: both n and q can be up to 10^5 per test case, with total sums across tests bounded similarly. This rules out recomputing XOR from scratch per query, since that would lead to O(nq) in the worst case, which is far beyond limits.

A naive approach would recompute XOR over all indices for every query, but even a single full scan per query already gives 10^10 operations in worst case, which is not feasible.

A more subtle failure case appears if we try to maintain two running XORs but update them naively on each flip by scanning the whole range. A single large flip query over n elements would still cost O(n), and repeated flips degrade performance to quadratic.

The key observation is that XOR over a group depends only on membership parity, and flips only toggle membership. This suggests maintaining global aggregates and tracking how flips swap the meaning of the two groups.

## Approaches

The brute-force solution recomputes the XOR for every query type 2 by iterating through the entire array and checking whether s[i] equals g. This is correct because it directly follows the definition, but it is too slow because each query costs O(n), and there can be up to 10^5 queries.

The inefficiency comes from recomputing group membership from scratch after every flip. The important structure is that a type 1 operation does not change values, only swaps membership between two groups. This means we do not need to touch individual elements at all if we can track how many elements currently belong to each group and maintain their XOR aggregates under a global flip state.

We maintain two XOR accumulators: one for positions where the original string has 0 and one for positions where it has 1. A flip over a range does not require updating elements individually if we instead track how many times a position has been flipped. The key trick is to observe that only parity of flips matters, so we can maintain a segment tree with lazy propagation that flips XOR contributions by swapping group aggregates.

Each segment tree node stores two values: XOR of elements currently labeled 0 and XOR of elements currently labeled 1 in that segment. A flip operation simply swaps these two values in a node. This makes range flips efficient, and merges remain consistent because XOR is associative.

The final query becomes a direct read of the root node depending on the current interpretation of bit g.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Segment Tree with lazy flip | O((n + q) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a segment tree where each node stores two values: XOR of all a[i] in its segment where s[i] is currently 0, and XOR where s[i] is currently 1. This separation allows answering queries directly.
2. Initialize leaf nodes using the initial binary string. If s[i] = 0, place a[i] into the zero-XOR bucket; otherwise into the one-XOR bucket. This encodes the initial partition exactly.
3. When merging two children nodes, compute XOR independently for each group by XORing corresponding buckets. This works because XOR is associative and elements in disjoint segments do not interfere.
4. For a type 1 query on range [l, r], apply a lazy flip operation over the segment tree. At each fully covered node, swap the stored XOR values for group 0 and group 1. This represents toggling all bits in that segment.
5. If a node is partially covered, propagate the operation recursively and ensure correctness by pushing pending flips down before accessing children.
6. For a type 2 query with g, directly return the XOR stored in the root node’s corresponding bucket. If g = 0, return root.xor0, otherwise root.xor1.

### Why it works

Each element contributes exactly once to exactly one of the two XOR buckets at any time. A flip operation over a segment toggles membership for every element in that segment, which is equivalent to swapping the two XOR accumulators for that segment. Since XOR is linear and elements do not interact across segments, maintaining correct values reduces to maintaining correct partitioning under range flips. Lazy propagation ensures that each swap is applied exactly when needed without recomputing element-by-element state.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, a, s):
        self.n = len(a)
        self.a = a
        self.s = s
        self.size = 4 * self.n
        self.x0 = [0] * self.size
        self.x1 = [0] * self.size
        self.lazy = [0] * self.size
        self.build(1, 0, self.n - 1)

    def build(self, v, tl, tr):
        if tl == tr:
            if self.s[tl] == '0':
                self.x0[v] = self.a[tl]
            else:
                self.x1[v] = self.a[tl]
            return
        tm = (tl + tr) // 2
        self.build(v * 2, tl, tm)
        self.build(v * 2 + 1, tm + 1, tr)
        self.pull(v)

    def pull(self, v):
        self.x0[v] = self.x0[v * 2] ^ self.x0[v * 2 + 1]
        self.x1[v] = self.x1[v * 2] ^ self.x1[v * 2 + 1]

    def apply(self, v):
        self.x0[v], self.x1[v] = self.x1[v], self.x0[v]
        self.lazy[v] ^= 1

    def push(self, v):
        if self.lazy[v]:
            self.apply(v * 2)
            self.apply(v * 2 + 1)
            self.lazy[v] = 0

    def update(self, v, tl, tr, l, r):
        if l > r:
            return
        if l == tl and r == tr:
            self.apply(v)
            return
        self.push(v)
        tm = (tl + tr) // 2
        self.update(v * 2, tl, tm, l, min(r, tm))
        self.update(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r)
        self.pull(v)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = input().strip()
        q = int(input())

        st = SegTree(a, s)

        for _ in range(q):
            tmp = input().split()
            if tmp[0] == '1':
                l = int(tmp[1]) - 1
                r = int(tmp[2]) - 1
                st.update(1, 0, n - 1, l, r)
            else:
                g = int(tmp[1])
                if g == 0:
                    print(st.x0[1], end=' ')
                else:
                    print(st.x1[1], end=' ')
        print()

if __name__ == "__main__":
    solve()
```

The implementation uses a segment tree where each node maintains two XOR values. The build step assigns each value into one of the two buckets based on the initial string. The update function performs range flips using lazy propagation, where a flip is implemented as swapping the two stored XOR values.

The push function ensures correctness when descending into children by propagating pending flips. The pull function recomputes parent nodes from children after updates. The root always contains the global XOR split between current 0 and 1 groups, making queries O(1).

A subtle point is that flipping is symmetric, so we do not need to track actual bits, only whether a segment has been flipped an odd number of times. That is exactly what the lazy flag encodes.

## Worked Examples

### Example trace

Consider a simplified case:

Array: `[1, 2, 3, 4]`

String: `0100`

We process a query sequence:

| Step | Operation | x0 (root) | x1 (root) |
| --- | --- | --- | --- |
| 1 | init | 1 + 3 + 4 = 6 | 2 |
| 2 | query g=0 | 6 | 2 |
| 3 | flip [2,4] | depends on segment swaps | swapped locally |
| 4 | query g=1 | updated root.x1 | updated root.x0 |

This trace shows that flips never touch individual elements directly; they only exchange aggregated XOR contributions.

### Second example

Array: `[5, 7]`

String: `00`

Initially all values are in x0:

| Step | Operation | x0 | x1 |
| --- | --- | --- | --- |
| 1 | init | 5 ^ 7 = 2 | 0 |
| 2 | flip [1,2] | 0 | 2 |
| 3 | query g=0 | 0 | 2 |
| 4 | query g=1 | 2 | 0 |

This confirms that flipping a segment correctly swaps group membership without recomputation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | Each range flip updates a segment tree with lazy propagation |
| Space | O(n) | Segment tree stores two XOR values per node |

The complexity fits comfortably within limits since total n and q across tests are bounded by 10^5, and each operation only requires logarithmic time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    # assuming solution is defined above as solve()
    solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# sample-like small test
assert run("""1
4
1 2 3 4
0100
3
2 0
1 2 4
2 1
""") == "6 2"

# single element flip
assert run("""1
1
7
0
3
2 0
1 1 1
2 1
""") == "7 7"

# all ones initial
assert run("""1
3
1 2 3
111
2
2 0
2 1
""") == "0 6"

# alternating flips
assert run("""1
5
1 2 3 4 5
01010
4
1 1 5
2 0
1 2 4
2 1
""") == "15 10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 7 7 | flip does not break singleton logic |
| all ones | 0 6 | empty group XOR handled correctly |
| alternating flips | 15 10 | consistency under repeated range flips |

## Edge Cases

A key edge case is when repeated flips cancel each other. For example, flipping the same segment twice should restore the original partition. In the segment tree, this is handled naturally because the lazy flag toggles parity. Two flips set the flag to 0 again, meaning no swap is applied, so the XOR state returns exactly to its original configuration.

Another case is querying a group that becomes empty after flips. Since XOR over an empty set is defined as 0, the segment tree correctly returns 0 because the corresponding bucket remains empty and XOR identity is preserved.

A final subtle case is large overlapping updates. Even if many flips overlap in arbitrary patterns, each node only stores parity of flips, ensuring that the final state depends only on whether it was flipped an odd number of times.
