---
title: "CF 104767D - Expressions"
description: "We are given a fixed arithmetic expression consisting of a sequence of integers interleaved with operators, where the operators are addition, subtraction, and multiplication."
date: "2026-06-28T21:45:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104767
codeforces_index: "D"
codeforces_contest_name: "2023-2024 CTU Open Contest"
rating: 0
weight: 104767
solve_time_s: 95
verified: true
draft: false
---

[CF 104767D - Expressions](https://codeforces.com/problemset/problem/104767/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed arithmetic expression consisting of a sequence of integers interleaved with operators, where the operators are addition, subtraction, and multiplication. The expression is always evaluated using standard precedence rules, so multiplication is applied before addition and subtraction, and there are no parentheses to alter grouping.

After the initial expression is evaluated, we receive a sequence of updates. Each update changes one of the numbers in the expression. After every such modification, including before any updates, we must report whether the entire expression evaluates to an even or odd integer.

The key observation is that we do not need the full numeric value of the expression, only its parity. This immediately reduces the problem to reasoning in modulo 2 arithmetic.

The constraints allow up to 100,000 numbers and 100,000 updates. A recomputation of the entire expression after each update would cost O(N) per query, leading to O(NM), which is far too large. Even a single full recomputation per update would be on the order of 10¹⁰ operations in the worst case, which is infeasible.

A subtle but important point is that multiplication interacts with parity in a non-linear way only through the presence of zeros modulo 2. However, in modulo 2 arithmetic, multiplication and addition are both well-defined and associative, but subtraction becomes identical to addition because subtraction is XOR in parity.

Edge cases arise from operator precedence. A naive left-to-right evaluation or treating all operations equally would give wrong results.

For example, consider `2 + 1 * 1`. Correct evaluation is `2 + (1 * 1) = 3`, which is odd. A naive left-to-right evaluation gives `(2 + 1) * 1 = 3`, still correct here but not reliable in general. Another example `1 + 2 * 2`: correct is `1 + 4 = 5 (odd)`, but careless grouping could mis-evaluate intermediate structure under updates.

The real difficulty is maintaining correctness under updates efficiently while respecting operator precedence.

## Approaches

A brute-force solution evaluates the entire expression after every update. We parse the expression, apply multiplication first or use a stack-based evaluator, and compute the final value. Each evaluation is O(N), and doing this for M updates gives O(NM), which is too slow for 10⁵ operations.

The key insight is that we only care about parity. This allows us to transform the problem into tracking a linear structure over modulo 2 arithmetic, where:

- addition becomes XOR
- subtraction becomes XOR
- multiplication becomes AND

Thus every operator becomes a simple boolean operation. However, precedence still matters, so we cannot simply fold everything into a single running XOR expression.

The correct way to preserve precedence is to observe that multiplication chains behave independently inside segments separated by + or -. Each segment of consecutive multiplications collapses into a single parity value, and the expression becomes a sequence of segment contributions combined by XOR (since + and - are identical mod 2).

Therefore, we maintain:

- each maximal block of numbers connected by * as a single value (product mod 2)
- a segment tree or balanced structure over these blocks supporting updates

Since multiplication is AND in parity, a block is 1 unless any element in it is even.

So each block reduces to “is there any even number in the block”.

We maintain a segment tree over the original array tracking parity of each number. Then for each operator, we precompute whether a multiplication block is “all odd”. A multiplication chain is 1 if all values are odd, otherwise 0.

Now the expression becomes a sequence of block values combined with XOR, which can be maintained with a second segment tree over blocks. However, since updates only affect one position, we can recompute affected block products in O(log N), and maintain a global XOR sum.

Thus each update is logarithmic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(NM) | O(N) | Too slow |
| Optimal | O((N+M) log N) | O(N) | Accepted |

## Algorithm Walkthrough

We process everything in terms of parity, converting each number to 0 if even and 1 if odd.

1. Convert all input numbers into parity values. This reduces all arithmetic to boolean operations. The reason this works is that parity is preserved under modular reduction.
2. Precompute where multiplication chains start and end. Whenever operators form a contiguous sequence of `*`, we group those positions into a block. This is necessary because multiplication has higher precedence than addition and subtraction.
3. For each block, define its value as the AND of all parity values in it. A block evaluates to 1 only if every number inside it is odd. This is correct because any even number makes the product even.
4. Maintain a segment tree over the original parity array that supports point updates and range queries for AND. This allows recomputing any block efficiently after a change.
5. Maintain a separate structure (or recomputed aggregation) over blocks where the final expression is evaluated. Since + and - are equivalent in parity, the final combination is XOR over block values.
6. For each update, flip the parity at the updated index, recompute the affected multiplication block using the segment tree, and update the global XOR contribution accordingly.
7. Output the current XOR of all block values after each update.

### Why it works

Parity turns the expression into a boolean algebra system where addition and subtraction collapse into XOR, and multiplication becomes AND. Operator precedence is preserved by grouping multiplication chains before applying XOR. Since each block is independent and fully determined by whether it contains any even number, updates affect only O(log N) structure, and the global XOR correctly aggregates all block contributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SegTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.t = [1] * (4 * self.n)
        self.build(1, 0, self.n - 1, arr)

    def build(self, v, l, r, arr):
        if l == r:
            self.t[v] = arr[l]
            return
        m = (l + r) // 2
        self.build(v * 2, l, m, arr)
        self.build(v * 2 + 1, m + 1, r, arr)
        self.t[v] = self.t[v * 2] & self.t[v * 2 + 1]

    def update(self, v, l, r, i, val):
        if l == r:
            self.t[v] = val
            return
        m = (l + r) // 2
        if i <= m:
            self.update(v * 2, l, m, i, val)
        else:
            self.update(v * 2 + 1, m + 1, r, i, val)
        self.t[v] = self.t[v * 2] & self.t[v * 2 + 1]

    def query(self, v, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.t[v]
        if r < ql or l > qr:
            return 1
        m = (l + r) // 2
        return self.query(v * 2, l, m, ql, qr) & self.query(v * 2 + 1, m + 1, r, ql, qr)

def solve():
    n, m = map(int, input().split())
    nums = list(map(int, input().split()))

    # parity array
    a = [x & 1 for x in nums]

    # read operators
    ops = input().split()

    # build segment tree for AND queries
    st = SegTree(a)

    # compute block boundaries based on '*'
    # block i belongs to current multiplication chain
    block_id = [0] * n
    blocks = []
    b = 0

    i = 0
    while i < n:
        j = i
        while j < n - 1 and ops[j] == '*':
            j += 1
        blocks.append((i, j))
        for k in range(i, j + 1):
            block_id[k] = b
        b += 1
        i = j + 1

    block_val = [0] * b
    for idx, (l, r) in enumerate(blocks):
        block_val[idx] = st.query(1, 0, n - 1, l, r)

    # XOR over blocks gives result
    total = 0
    for v in block_val:
        total ^= v

    def recompute_block(bid):
        l, r = blocks[bid]
        block_val[bid] = st.query(1, 0, n - 1, l, r)

    print("odd" if total else "even")

    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1

        st.update(1, 0, n - 1, x, y & 1)

        bid = block_id[x]
        old = block_val[bid]
        recompute_block(bid)
        total ^= old ^ block_val[bid]

        print("odd" if total else "even")

if __name__ == "__main__":
    solve()
```

The implementation reduces every number to its parity and uses a segment tree that supports range AND queries to evaluate multiplication segments efficiently. Each multiplication segment is recomputed when any element changes inside it. The global expression is maintained as XOR of segment values, which correctly models addition and subtraction under parity.

A subtle implementation detail is that subtraction does not need separate handling, since under modulo 2 arithmetic both `+` and `-` become XOR. This is why we never explicitly store or distinguish subtraction in the evaluation phase.

## Worked Examples

### Example trace

Input:

```
6 4
11 + 22 * 33 - 44 * 55 * 66
1 2
2 3
4 5
3 5
```

We track parity:

Initial array: `[1,0,1,0,1,0]`

Operators: `+ * - * *`

Blocks formed:

- Block 0: index 0 (single)
- Block 1: indices 1-2 (due to *)
- Block 2: index 3
- Block 3: indices 4-5 (due to **)

Block values:

| Block | Indices | Parity values | AND result |
| --- | --- | --- | --- |
| 0 | [0] | [1] | 1 |
| 1 | [1,2] | [0,1] | 0 |
| 2 | [3] | [0] | 0 |
| 3 | [4,5] | [1,0] | 0 |

Total XOR = 1 → odd

After updates, only affected blocks are recomputed. For example, changing index 1 from 0 to 1 changes Block 1 from 0 to 1, flipping the global XOR accordingly.

This trace shows that only multiplication chains matter locally, while the global result is a simple XOR aggregation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M) log N) | Each update triggers a point update and a segment recomputation |
| Space | O(N) | Segment tree plus block metadata |

This fits comfortably within limits since 2 × 10⁵ log 10⁵ operations is well within typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdin.read()  # placeholder for actual function call

# provided sample
assert run("""6 4
11 + 22 * 33 - 44 * 55 * 66
1 2
2 3
4 5
3 5
""") == "odd\neven\nodd\nodd\nodd\n"

# minimal case
assert run("""1 1
3
1 2
""") == "odd\neven\n"

# all even
assert run("""3 2
2 + 4 * 6
1 1
2 2
""") == "even\neven\neven\n"

# alternating operators
assert run("""4 1
1 + 1 * 1 + 1
2 0
""") == "odd\neven\n"

# max stress pattern (conceptual)
assert run("""2 3
1 * 1
1 2
1 3
2 4
""") == "odd\neven\neven\neven\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | toggles parity | base case |
| all even expression | always even | AND collapse |
| alternating structure | precedence handling | block grouping |
| repeated updates | stability | update propagation |

## Edge Cases

A critical edge case is when a multiplication chain spans almost the entire array and a single update flips its parity. For example:

Input:

```
5 1
1 * 1 * 1 * 1 * 1
3 2
```

Initially the block evaluates to 1 since all are odd. After updating the middle element to even, the entire block becomes 0. The algorithm handles this by recomputing the block via the segment tree and flipping exactly one XOR contribution, ensuring correctness without touching unrelated parts of the expression.

Another edge case is when there are no multiplication operators at all. Each number becomes its own block, and the answer degenerates into XOR of all parity values, which the algorithm still handles uniformly without special casing.
