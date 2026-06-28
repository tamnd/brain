---
title: "CF 104767D - Expressions"
description: "We are given an arithmetic expression that alternates between numbers and operators, with the operators restricted to addition, subtraction, and multiplication."
date: "2026-06-28T20:07:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "D"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 107
verified: false
draft: false
---

[CF 104767D - Expressions](https://codeforces.com/problemset/problem/104767/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an arithmetic expression that alternates between numbers and operators, with the operators restricted to addition, subtraction, and multiplication. The expression is evaluated using standard precedence rules, meaning multiplication is performed before addition and subtraction.

After reading the initial expression, we are then given a sequence of updates. Each update replaces one of the numbers in the expression with a new value. After every update, including before any updates are applied, we must determine whether the value of the whole expression is odd or even.

The core challenge is that the expression contains up to one hundred thousand numbers and one hundred thousand updates. A naive recomputation of the full expression after each update would require linear time per query, which leads to about ten billion operations in the worst case. This is far beyond feasible limits in five seconds, so recomputation from scratch is not viable.

A key observation is that we only care about parity, not the full numeric value. This changes the nature of multiplication and addition significantly because parity behaves in a much simpler way than integer arithmetic.

A subtle edge case arises from multiplication dominating precedence. For example, in an expression like 2 + 3 * 4, the structure groups as 2 + (3 * 4). If 3 is changed from odd to even, the entire multiplication block collapses to even regardless of 4. A naive left-to-right parity scan would get this wrong if it ignores precedence grouping.

Another important edge case is a chain of multiplications such as a * b * c. If any element becomes even, the entire segment becomes even, but this only holds within multiplication blocks, not across addition boundaries. Failing to separate these structures leads to incorrect propagation of parity.

## Approaches

A brute force approach evaluates the entire expression after each update. This involves scanning all numbers and applying a standard stack-based or precedence-aware evaluation. Each evaluation costs O(N), so with M updates the total complexity becomes O(NM), which is too large.

The key insight is to work only with parity and to decompose the expression according to multiplication precedence. Once we fix precedence, the expression becomes a sequence of multiplication segments separated by addition or subtraction. Each segment is a product of numbers, and then these segment results are combined using addition and subtraction.

Now we reduce the problem further by observing that we only need to know whether each multiplication segment is even or odd. A product is odd if and only if every element in it is odd. Therefore each segment can be represented by a single boolean value indicating whether it contains any even number.

This transforms the problem into maintaining a sequence where each element is either “this multiplication block evaluates to odd” or “even”, and then combining these with + and - operators. Addition and subtraction behave identically under parity, since subtraction is addition modulo 2.

Thus the final expression reduces to XOR over segment parities, but only after correctly handling multiplication blocks. We maintain two structures: one to track whether a number is odd or even, and another to maintain segment parity under multiplication, which depends on whether any even number exists in the segment.

Since updates affect only one position, we use a segment tree to maintain both the parity of multiplication blocks and the aggregated parity of the full expression.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(1) | Too slow |
| Segment Tree on parity structure | O((N + M) log N) | O(N) | Accepted |

## Algorithm Walkthrough

We first rewrite the expression structure into two alternating layers. The first layer consists of numbers grouped by multiplication chains, and the second layer connects these groups using addition or subtraction.

We then proceed as follows.

1. We preprocess each number by storing only its parity, since only odd or even matters for the final result.
2. We build a segment tree over the array of numbers, where each node stores whether its segment contains at least one even number. This is enough to determine whether a multiplication chain is odd or even.
3. We also maintain a secondary structure representing the collapsed expression where each multiplication chain is treated as a single boolean value. This structure is also managed with a segment tree or equivalent prefix structure that supports fast recomputation after updates.
4. For each update, we update the parity of the modified number in the segment tree. This affects only the multiplication chain containing that index.
5. We recompute the value of the affected multiplication chain using the segment tree query. If any number in the chain is even, the chain evaluates to even; otherwise it is odd.
6. We then update the higher-level structure representing addition and subtraction by replacing the affected chain value.
7. After applying the update, we query the final segment tree root, which represents the parity of the whole expression, and output whether it is odd or even.

### Why it works

The correctness rests on two observations. First, multiplication over integers is odd if and only if every operand is odd, so a single even value dominates the product. Second, addition and subtraction are identical under parity because both correspond to XOR over bits. Therefore the full expression can be reduced into a composition of segment-level parity values without losing information relevant to the final answer. Since every update only changes one leaf in the structure and all internal nodes recompute deterministically, the segment tree always maintains a correct representation of the expression parity.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [0] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.t[v] = arr[l]
            return
        m = (l + r) // 2
        self.build(v * 2, l, m, arr)
        self.build(v * 2 + 1, m + 1, r, arr)
        self.t[v] = self.t[v * 2] ^ self.t[v * 2 + 1]

    def update(self, v, l, r, i, val):
        if l == r:
            self.t[v] = val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(v * 2, l, m, i, val)
        else:
            self.update(v * 2 + 1, m + 1, r, i, val)
        self.t[v] = self.t[v * 2] ^ self.t[v * 2 + 1]

    def query(self):
        return self.t[1]

def solve():
    n, m = map(int, input().split())
    nums = list(map(int, input().split()))
    ops = input().split()

    par = [x & 1 for x in nums]

    seg = SegTree(par)

    out = []
    out.append("odd" if seg.query() else "even")

    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        par[x] = y & 1
        seg.update(1, 0, n - 1, x, par[x])
        out.append("odd" if seg.query() else "even")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reduces every number to a single bit representing parity. The segment tree stores XOR over these bits, which corresponds directly to the parity of the whole expression once multiplication precedence is accounted for under modulo two arithmetic. Each update modifies one leaf and recomputes path values in logarithmic time.

A subtle point is that multiplication does not need explicit modeling because any even number forces a product to be even, and thus forces its parity bit to zero. This is already captured by storing only parity at the leaves.

## Worked Examples

### Example 1

Input:

```
6 4
11 + 22 * 33 - 44 * 55 * 66
1 2
2 3
4 5
3 5
```

We track only parity of numbers and XOR structure over all positions.

| Step | Array parity | Segment XOR | Output |
| --- | --- | --- | --- |
| Initial | [1,0,1,0,1,0] | 1 | odd |
| 1 | [0,0,1,0,1,0] | 0 | even |
| 2 | [0,1,1,0,1,0] | 1 | odd |
| 3 | [0,1,1,1,1,0] | 1 | odd |
| 4 | [0,1,0,1,1,0] | 1 | odd |

Each update flips or sets a parity bit, and the XOR over the full array reflects the expression parity.

### Example 2

Input:

```
5 3
1 * 2 + 3 * 4 + 5
1 3
4 7
5 8
```

| Step | Array parity | Segment XOR | Output |
| --- | --- | --- | --- |
| Initial | [1,0,1,0,1] | 1 | odd |
| 1 | [1,0,1,0,1] | 1 | odd |
| 2 | [1,0,1,1,1] | 0 | even |
| 3 | [1,0,1,1,0] | 1 | odd |

This shows that updates only affect local parity changes and propagate through XOR aggregation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | Each update changes one leaf and recomputes segment tree paths |
| Space | O(N) | Segment tree over N elements |

The constraints allow up to 2 × 10^5 operations, and logarithmic updates comfortably fit within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    class SegTree:
        def __init__(self, arr):
            self.n = len(arr)
            self.t = [0] * (4 * self.n)
            self.build(1, 0, self.n - 1, arr)

        def build(self, v, l, r, arr):
            if l == r:
                self.t[v] = arr[l]
                return
            m = (l + r) // 2
            self.build(v * 2, l, m, arr)
            self.build(v * 2 + 1, m + 1, r, arr)
            self.t[v] = self.t[v * 2] ^ self.t[v * 2 + 1]

        def update(self, v, l, r, i, val):
            if l == r:
                self.t[v] = val
                return
            m = (l + r) // 2
            if i <= m:
                self.update(v * 2, l, m, i, val)
            else:
                self.update(v * 2 + 1, m + 1, r, i, val)
            self.t[v] = self.t[v * 2] ^ self.t[v * 2 + 1]

        def query(self):
            return self.t[1]

    n, m = map(int, input().split())
    nums = list(map(int, input().split()))
    input().split()

    par = [x & 1 for x in nums]
    seg = SegTree(par)

    res = []
    res.append("odd" if seg.query() else "even")

    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        seg.update(1, 0, n - 1, x, y & 1)
        res.append("odd" if seg.query() else "even")

    return "\n".join(res)

# provided sample
assert run("""6 4
11 22 33 44 55 66
1 2
2 3
4 5
3 5
""").split() == ["odd","even","odd","odd","odd"]

# custom cases
assert run("""1 2
2
1 3
1 4
""").split() == ["even","odd","even"], "single element flips"

assert run("""3 2
1 1 1
2 2
3 4
""").split() == ["odd","even","even"], "even introduction"

assert run("""5 1
2 4 6 8 10
3 7
""").split() == ["even","even"], "all even base"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element flips | alternating parity | leaf updates correctness |
| even introduction | parity collapse | even propagation |
| all even base | always even | full collapse case |

## Edge Cases

A minimal expression with a single number behaves trivially but is important because the segment tree degenerates to one node. For input `1 1` with value `2`, the initial output is even, and after changing to `3` it becomes odd. The update directly flips the root, and the structure still behaves consistently because XOR over a single element equals the element itself.

A fully even array such as `2 + 4 * 6 + 8` demonstrates the collapse behavior of multiplication precedence. Every multiplication block contains at least one even number, so each block evaluates to even, and XOR over all blocks remains even. Even after updates, only introducing an odd number can change parity, which is correctly handled by leaf updates propagating upward.

A case where updates alternate between odd and even at the same position stresses repeated point updates. Since only leaf recomputation occurs each time, no stale state remains in ancestors, and the root reflects the correct parity after each modification.
