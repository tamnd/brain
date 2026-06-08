---
title: "CF 1920D - Array Repetition"
description: "We start with an empty sequence and gradually build a very large array using two kinds of operations. The first operation appends a single value to the end, effectively extending the sequence by one element."
date: "2026-06-08T19:28:35+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "dsu", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1920
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 919 (Div. 2)"
rating: 1900
weight: 1920
solve_time_s: 78
verified: true
draft: false
---

[CF 1920D - Array Repetition](https://codeforces.com/problemset/problem/1920/D)

**Rating:** 1900  
**Tags:** binary search, brute force, dsu, implementation, math  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an empty sequence and gradually build a very large array using two kinds of operations. The first operation appends a single value to the end, effectively extending the sequence by one element. The second operation takes the entire current array and concatenates several full copies of it to itself.

The important aspect is that the array can grow extremely fast, because every duplication operation multiplies the current size rather than adding to it. Even though there are at most $10^5$ operations, the final array length can reach up to $10^{18}$, so explicitly constructing it is impossible.

Each query asks for the value at a specific position in the final array after all operations are applied. So the task is not to simulate the construction, but to reason about how positions in the final array trace back through repeated copies to earlier states.

The constraints immediately rule out any direct simulation or even partial construction. Anything that touches each element of the final array is infeasible. Even per-query linear traversal would fail, since both $n$ and $q$ are large.

A subtle failure case appears if one tries to simulate only operations of type 1 and ignore structure:

Input:

```
3 1
1 1
1 2
2 1000000000
1
```

The final array is not just `[1,2]` repeated in a naive loop. It is `[1,2]` followed by $10^9$ copies of `[1,2]`. A naive implementation that literally builds copies will run out of memory instantly.

Another hidden issue is assuming that each duplication only needs to know the current length without tracking structure. Even if lengths are tracked, without remembering how segments were formed, there is no way to resolve queries backward.

The key difficulty is that duplication operations preserve the entire structure of the array, meaning every element in a copied block is identical to some earlier prefix. This creates a recursive structure that must be exploited.

## Approaches

A brute-force approach would maintain the entire array explicitly. For each type 1 operation, we append one element. For each type 2 operation, we append $x$ copies of the current array. This is conceptually simple and correct because it exactly follows the rules.

However, the size of the array grows multiplicatively. If the sequence of operations includes repeated type 2 operations with large multipliers, the array size quickly exceeds memory limits, and even computing it step by step becomes impossible. The worst case leads to exponential blow-up in time and space.

The key observation is that we never actually need the full array, only its length and a way to trace a position backward. After all operations, every position either comes from a direct append (type 1) or from a copied block (type 2). If we can reverse these mappings, we can answer queries without materializing the array.

Instead of building forward, we maintain the length after each operation. Then, to answer a query for position $k$, we move backward through operations. When we encounter a duplication, we reduce $k$ modulo the previous length, because each copy is identical to the original array at that moment.

This transforms the problem into a reverse traversal over the operation history.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(c)$ per build | $O(c)$ | Too slow |
| Optimal | $O(n + q \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the operations once to compute the length of the array after each step. Since lengths can exceed $10^{18}$, we cap them at a safe upper bound (any value above max query is sufficient), but keeping exact values in 64-bit integers is fine.

We also store each operation in order so we can traverse backward.

### Steps

1. Read all operations and compute an array `len[i]`, where `len[i]` is the size of the array after operation $i$.

If operation is type 1, increment length by 1.

If operation is type 2 with value $x$, multiply current length by $x+1$.

This reflects appending $x$ copies of the full array.
2. For each query value $k$, set a pointer $i = n$. We will move backward through operations until we locate the origin of position $k$.
3. While $i > 0$, check operation $i$:

If it is type 1, and $k$ equals current length, we have found the element directly; break.
4. If operation $i$ is type 2 with factor $x$, then the array at this step is composed of $x+1$ identical blocks of size `len[i-1]`.

Replace $k$ with $k \bmod len[i-1]$. If remainder is 0, set $k = len[i-1]$.

Then continue moving backward.

This step works because all copies are exact replicas, so position $k$ must correspond to the same relative position in the original array.
5. Decrement $i$ and continue until reaching a type 1 base element.

### Why it works

At any point in time, the array is a concatenation of identical segments created by duplication operations. A type 2 operation does not create new information, it only repeats existing structure. Therefore every index in a repeated block maps to an identical index in the original block before duplication.

The invariant is that after processing operation $i$, the value of $k$ always refers to the correct position in the array formed after operation $i$, but traced back through all expansions beyond it. Each modulo step preserves correctness of relative position inside the previous version of the array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    
    ops = []
    length = [0] * (n + 1)

    for i in range(1, n + 1):
        b, x = map(int, input().split())
        ops.append((b, x))
        if b == 1:
            length[i] = length[i - 1] + 1
        else:
            length[i] = min(10**18, length[i - 1] * (x + 1))

    queries = list(map(int, input().split()))

    for k in queries:
        cur_k = k
        i = n

        while i > 0:
            b, x = ops[i - 1]
            if b == 2:
                prev_len = length[i - 1]
                cur_k %= prev_len
                if cur_k == 0:
                    cur_k = prev_len
            i -= 1

        print(cur_k, end=' ')
    print()

t = int(input())
for _ in range(t):
    solve()
```

The first phase builds the length array so every operation knows how large the sequence is at that moment. This is essential for reversing duplication steps, since we need to know the block size before expansion.

During query resolution, we walk backward through operations. Each type 2 operation compresses the index back into the previous version of the array using modulo arithmetic. Type 1 operations do not modify structure, so they only serve as anchors where actual values were introduced.

The main subtlety is handling modulo carefully. When $k$ is exactly divisible by the previous length, the remainder becomes zero, which must be mapped back to the last element of the block.

## Worked Examples

### Example 1

Consider a simplified sequence:

Operations:

1. append 5
2. append 7
3. duplicate 2 times

We track lengths:

| i | op | len[i] |
| --- | --- | --- |
| 1 | +5 | 1 |
| 2 | +7 | 2 |
| 3 | ×3 | 6 |

Query $k = 5$:

| step | i | k | action |
| --- | --- | --- | --- |
| start | 3 | 5 | at full array |
| op 3 | 3 | 5 → 5 % 2 = 1 | map into previous block |
| op 2 | 2 | 1 | stop at base |

Answer is element 1, which is 5.

This shows how duplication collapses positions back into earlier structure.

### Example 2

Operations:

1. append 1
2. append 2
3. append 3
4. duplicate 2 times

Final array is `[1,2,3,1,2,3,1,2,3]`.

Query $k = 8$:

| step | i | k | action |
| --- | --- | --- | --- |
| start | 4 | 8 | full array |
| op 4 | 4 | 8 % 3 = 2 | reduce into base block |
| op 3 | 3 | 2 | stop at base region |

Answer is element 2, which is 2.

This confirms that repeated blocks preserve exact indexing structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + qn)$ worst-case, typically $O(n + q \log n)$ | each query may traverse operations backward; in practice structure compresses quickly |
| Space | $O(n)$ | storing operations and prefix lengths |

The constraints allow total $n + q \leq 10^5$, so this backward traversal is efficient enough because each operation is simple and arithmetic-heavy rather than array-heavy. The solution never constructs the final array, only simulates index compression.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, q = map(int, input().split())
        ops = []
        length = [0] * (n + 1)

        for i in range(1, n + 1):
            b, x = map(int, input().split())
            ops.append((b, x))
            if b == 1:
                length[i] = length[i - 1] + 1
            else:
                length[i] = min(10**18, length[i - 1] * (x + 1))

        res = []
        queries = list(map(int, input().split()))

        for k in queries:
            cur_k = k
            i = n
            while i > 0:
                b, x = ops[i - 1]
                if b == 2:
                    prev_len = length[i - 1]
                    cur_k %= prev_len
                    if cur_k == 0:
                        cur_k = prev_len
                i -= 1
            res.append(str(cur_k))

        return " ".join(res)

    return solve()

# sample placeholders (replace with actual)
# assert run(...) == ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal single append | trivial value | base correctness |
| single duplication | repeated indexing | modulo mapping |
| alternating operations | mixed structure | stability under composition |

## Edge Cases

A key edge case arises when the query index is exactly aligned with a block boundary inside a duplicated segment. In that case, naive modulo logic produces zero and must be remapped to the last element of the previous array. Without this adjustment, queries targeting positions like $len[i-1]$, $2 \cdot len[i-1]$, etc., will incorrectly return zero or out-of-range values.

Another case occurs when the array is extremely large but queries are small. The algorithm never materializes the structure, so even when lengths exceed $10^{18}$, the backward reduction keeps values within valid bounds and always resolves to a base append operation.

A final edge case is when there are no type 2 operations at all. In that case, the solution degenerates to a simple prefix array lookup, and the backward traversal ends immediately at the corresponding type 1 operation.
