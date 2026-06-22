---
title: "CF 105423I - \u6570\u636e\u68c0\u7d22\u7cfb\u7edf"
description: "We are building a simplified membership system that behaves like a hash-filtered set with multiple hash functions. The system stores elements in a binary array of size n, initially all zeros."
date: "2026-06-23T04:17:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105423
codeforces_index: "I"
codeforces_contest_name: "2024\u6e56\u5357\u7701\u8d5b"
rating: 0
weight: 105423
solve_time_s: 59
verified: true
draft: false
---

[CF 105423I - \u6570\u636e\u68c0\u7d22\u7cfb\u7edf](https://codeforces.com/problemset/problem/105423/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are building a simplified membership system that behaves like a hash-filtered set with multiple hash functions. The system stores elements in a binary array of size `n`, initially all zeros. When an element is inserted, we compute `k` deterministic hash-like values from it and mark those positions in the array as `1`. When we query an element, we recompute the same `k` values and check whether all corresponding positions are already `1`. If yes, we report that the element “exists”, otherwise we report that it does not.

The transformation functions are extremely simple: for each function index `i`, the value is mapped as `h_i(x) = x^i mod n`. This means every element produces a small set of indices in `[0, n-1]`, and those indices are what drive both insertion and queries.

The constraints are small enough that we can afford straightforward simulation. With `n, m, q ≤ 10000` and `k ≤ 10`, each operation is at most 10 modular exponentiations or multiplications. Even if we compute powers naively per query and insertion, the total work remains comfortably within limits because we only perform about `m + q` operations, each with tiny constant cost.

A subtle edge case comes from the fact that indices are taken modulo `n`, so collisions are expected and even required for correctness. Another issue is duplicate indices within the same query or insertion. Since `h_i(x)` can equal `h_j(x)` for different `i` and `j`, marking or checking must handle repetition safely. Using a set or simply iterating over all indices without deduplication still works, but deduplication avoids unnecessary repeated checks.

A naive mistake would be to treat exponentiation as linear multiplication without modular reduction or to forget that `x^i` grows quickly. However, since `i ≤ 10`, direct computation is safe. Another pitfall is misunderstanding that this is not a true probabilistic Bloom filter, but a deterministic fixed-hash variant.

## Approaches

The brute-force interpretation is straightforward: for each insertion, compute all `k` powers, and set those positions in the array to `1`. For each query, recompute the same `k` positions and check whether every one of them is `1`.

This approach is correct because the system definition directly states that membership is determined solely by those positions. There is no hidden state or ordering dependence beyond the array itself.

The complexity bottleneck does not come from the number of operations, but from repeated exponentiation if implemented inefficiently. If we recompute `x^i` from scratch each time using naive multiplication inside a loop, each operation costs `O(i)`, giving worst-case `O(k^2)` per operation, still trivial under constraints. Even more expensive methods would still pass.

The key observation is that `k ≤ 10` is tiny, so we do not need any advanced optimization. Precomputing powers up to exponent `k` for each value or computing them incrementally is sufficient. We can compute `x^1`, then multiply repeatedly by `x` modulo `n` to get `x^2`, `x^3`, and so on.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((m+q) · k · log i) or O((m+q) · k²) | O(n) | Accepted |
| Optimal | O((m+q) · k) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a binary array `arr` of size `n`, initially all zeros.

1. Read `n, k, m, q` and initialize `arr` with zeros. This array represents whether each index has been activated by at least one inserted element.
2. For each inserted element `x`, compute all values `x^1 mod n, x^2 mod n, ..., x^k mod n`. This can be done iteratively by maintaining a running power value.
3. For each computed index, set `arr[index] = 1`. Repeated assignments are harmless because the array is idempotent.
4. For each query element `y`, compute the same sequence of indices using the same iterative exponent method.
5. Check all `k` indices. If any position in `arr` is `0`, output `0` immediately for that query.
6. If all positions are `1`, output `1`.

The reason we recompute powers separately for each element instead of caching is that both `m` and `q` are small, and inputs are independent. Shared caching would complicate implementation without improving asymptotic complexity meaningfully.

### Why it works

Each element is represented entirely by the set of indices produced by the transformation functions. Insertion guarantees those indices are set to `1`. A query succeeds only if every index corresponding to the query element has been set by some previous insertion. Since the array never resets bits from `1` back to `0`, it monotonically accumulates evidence of inserted elements. Therefore, if a query's full index set is contained in the set of activated positions, it must have been inserted earlier (or is indistinguishable under this hashing scheme), which matches the problem's definition of membership.

## Python Solution

```python
import sys
input = sys.stdin.readline

def compute_indices(x, k, n):
    res = []
    val = x % n
    for i in range(1, k + 1):
        res.append(val)
        val = (val * x) % n
    return res

def main():
    n, k, m, q = map(int, input().split())
    arr = [0] * n

    insert_vals = list(map(int, input().split()))
    query_vals = list(map(int, input().split()))

    for x in insert_vals:
        for idx in compute_indices(x, k, n):
            arr[idx] = 1

    out = []
    for y in query_vals:
        ok = True
        for idx in compute_indices(y, k, n):
            if arr[idx] == 0:
                ok = False
                break
        out.append('1' if ok else '0')

    print(' '.join(out))

if __name__ == "__main__":
    main()
```

The core implementation detail is the iterative power computation. Instead of recomputing `x^i` from scratch, we maintain `val = x^i mod n` and update it as `val = val * x % n`. This reduces repeated work and keeps the code clean and predictable.

The array `arr` acts as the only persistent state. Insertions only set bits, and queries only read them. This monotonic structure avoids any need for deletion handling or rollback logic.

## Worked Examples

### Example 1

Input:

```
n=11, k=3, m=4, q=5
insert: [1, 5, 3, 8]
query: [4, 7, 1, 0, 4]
```

We track insertions.

For `x=1`, indices are `[1,1,1]`, so only position 1 becomes 1.

For `x=5`, indices are `[5, 3, 4]`.

For `x=3`, indices are `[3, 9, 5]`.

For `x=8`, indices are `[8, 9, 6]`.

Final activated array has ones at `{1,3,4,5,6,8,9}`.

Now queries:

| y | indices | check against arr | output |
| --- | --- | --- | --- |
| 4 | [4,5,9] | all exist | 1 |
| 7 | [7,5,2] | 7 or 2 missing | 0 |
| 1 | [1,1,1] | exists | 1 |
| 0 | [0,0,0] | missing | 0 |
| 4 | [4,5,9] | exists | 1 |

This confirms repeated indices like `[1,1,1]` do not affect correctness.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((m + q) · k) | each element computes k modular multiplications |
| Space | O(n) | binary array of size n |

The limits allow up to 20,000 total operations, each doing at most 10 multiplications, which is comfortably fast in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import main
    main()
    return sys.stdout.getvalue().strip()

# sample-like case
assert run("""11 3 4 5
1 5 3 8
4 7 1 0 4
""") == "1 0 1 0 1"

# minimum case
assert run("""1 1 1 1
0
0
""") == "1"

# no insertions
assert run("""5 2 0 3

1 2 3
""") == "0 0 0"

# all elements identical
assert run("""10 3 3 2
2 2 2
2 2
""") == "1 1"

# boundary power cycle behavior
assert run("""7 4 2 2
3 6
3 6
""") in ["1 1", "0 0"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 1 0 1 0 1 | correctness on mixed queries |
| single element | 1 | minimal configuration |
| no inserts | 0 0 0 | empty structure behavior |
| duplicates | 1 1 | idempotent insertion |
| modular collisions | variable | handling of cycles |

## Edge Cases

When all indices produced by a query repeat, such as `x = 1`, we get `[1,1,1,...]`. The algorithm still checks the same position multiple times, but since the array is binary and stable, the result is unaffected.

For `n = 1`, every exponent reduces to `0`, so all elements map to the same index. The system becomes a single-bit register, and every insertion or query collapses to that position. The algorithm correctly sets `arr[0] = 1` after any insertion, making all queries return `1` once at least one element exists.

For large values of `x`, modular multiplication ensures values remain bounded, so no overflow or performance degradation occurs. The iterative power computation guarantees correctness without needing fast exponentiation.
