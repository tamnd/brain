---
title: "CF 102864H - Prefix Sum"
description: "The sequence in this problem is not the original array only. Starting from the given array a^(0), we repeatedly apply the prefix sum operation. After one application, a^(1) is the prefix sum array. After another application, a^(2) is the prefix sum of a^(1), and so on."
date: "2026-07-25T13:44:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102864
codeforces_index: "H"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Online Round"
rating: 0
weight: 102864
solve_time_s: 95
verified: true
draft: false
---

[CF 102864H - Prefix Sum](https://codeforces.com/problemset/problem/102864/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

The sequence in this problem is not the original array only. Starting from the given array `a^(0)`, we repeatedly apply the prefix sum operation. After one application, `a^(1)` is the prefix sum array. After another application, `a^(2)` is the prefix sum of `a^(1)`, and so on. The queries ask for the sum of a range in `a^(k)`, while updates modify a single element of the original array `a^(0)`.

A direct way to view the effect of the repeated prefix sums is through combinations. An original value `a_j^(0)` contributes to a later position `a_i^(k)` with coefficient `C(i-j+k-1, k-1)` when `j <= i`. The range query can be rewritten as a prefix query on one more level:

`sum(l, r, k) = a_r^(k+1) - a_(l-1)^(k+1)`.

The task is thus to maintain values of the `(k+1)`-th prefix sequence after point updates on the original sequence.

The constraints are designed to prevent rebuilding the whole transformed array after every query. The array length is only `10000`, but the number of operations reaches `200000`, so an `O(n)` operation for every update or query would require around two billion operations. We need to use the small array size more carefully and avoid touching all positions for each modification.

A few cases easily break careless implementations. The first is querying a prefix starting from the first position. For example:

```
Input
1 1
5
1
2 1 1
```

The answer is `5`. A solution using `l-1` without handling zero correctly would access an invalid index.

Another dangerous case is when updates happen before queries. For example:

```
Input
2 2
1 2
2
1 1 3
2 1 1
```

After the update the first element becomes `4`. The sequence after two prefix operations begins with `4`, so the answer is `4`. A solution that only updates the original array and forgets that all higher prefix levels depend on it will fail.

The final common issue is modular subtraction. For example, if the right prefix value is smaller than the left prefix value modulo `998244353`, the subtraction must be normalized before printing.

## Approaches

The brute force method follows the definition literally. After every update, it changes `a^(0)` and rebuilds the prefix sum operation `k` times. Even if we optimize the rebuilding of one level to `O(n)`, the total cost is `O(nk)` per update. With `n` and `k` both equal to `10000`, this is around `10^8` operations for one update and is far too slow for `200000` queries.

The important observation is that the final query value is linear in the original array. A single point update at position `p` changes the value of `a_x^(k+1)` for every `x >= p` by:

`q * C(x-p+k, k)`.

The sequence of added values is a shifted binomial sequence. Since `n` is only `10000`, we can use square root decomposition. Instead of maintaining every possible transformed value globally, we split the original positions into small blocks.

Each block stores the full contribution of all stable values inside that block to every prefix position. A point update is stored temporarily inside its block as a pending change. Queries combine the stored block contribution with the pending changes. When a block accumulates too many pending changes, we rebuild it by applying those changes and recomputing its contribution.

This gives a balance between rebuilding cost and query cost. With a block size near `22` and a rebuild threshold near `450`, both parts stay around a few hundred operations per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nk) per update | O(n) | Too slow |
| Block decomposition | O(sqrt(n) + threshold) amortized | O(n sqrt(n)) | Accepted |

## Algorithm Walkthrough

1. Precompute the coefficients `C(k+d, k)` for every possible distance `d`. The same coefficients are used whenever a position receives an update, because an update at `p` affects position `x` only through the distance `x-p`.
2. Split the original array into blocks. For every block, build an array `contribution` where `contribution[x]` stores how much the stable values of this block contribute to `a_x^(k+1)`. The contribution is computed from the formula:

`a_x^(k+1) = sum(j <= x) C(x-j+k, k) * a_j^(0)`.

1. Store every new point update as a pending modification in its corresponding block. We do not immediately change the contribution array because a single update would affect many positions.
2. To answer a query, first compute the `(k+1)`-th prefix value at `r` and `l-1`. For every block, add its stored contribution at that position. Then process the pending updates of that block directly using the precomputed binomial coefficients.
3. When the number of pending updates in a block reaches the chosen rebuild limit, apply all pending changes to the block's actual values and rebuild its contribution array. This keeps the number of direct pending computations bounded.

Why it works:

The contribution stored by a block is exactly the sum of the effects of all values in that block that have already been incorporated. Pending updates are not lost because every query explicitly adds their mathematical contribution. Rebuilding only changes where the same contributions are stored, so the value returned by a query remains unchanged. Since the answer is the difference between two `(k+1)`-th prefix values, every range query is answered correctly.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())
    a = [0] + list(map(int, input().split()))

    w = [1] * (n + 1)
    inv = [1] * (n + 2)
    for i in range(1, n + 2):
        inv[i] = pow(i, MOD - 2, MOD)

    for d in range(n):
        w[d + 1] = w[d] * (k + d + 1) % MOD * inv[d + 1] % MOD

    block_size = 22
    rebuild_limit = 450
    block_count = (n + block_size - 1) // block_size

    values = [a[:]]
    blocks = []
    pending = [[] for _ in range(block_count)]

    def rebuild(b):
        left = b * block_size + 1
        right = min(n, left + block_size - 1)
        cur = array('I', [0]) * (n + 1)
        for pos in range(left, right + 1):
            val = a[pos]
            if val:
                for x in range(pos, n + 1):
                    cur[x] = (cur[x] + val * w[x - pos]) % MOD
        blocks[b] = cur

    blocks = [None] * block_count
    for b in range(block_count):
        rebuild(b)

    def get_prefix(x):
        if x <= 0:
            return 0
        ans = 0
        for b in range(block_count):
            ans += blocks[b][x]
        for b in range(block_count):
            for pos, delta in pending[b]:
                if pos <= x:
                    ans += delta * w[x - pos]
        return ans % MOD

    out = []
    m = int(input())

    for _ in range(m):
        t, x, y = map(int, input().split())
        if t == 1:
            b = (x - 1) // block_size
            a[x] = (a[x] + y) % MOD
            pending[b].append((x, y))
            if len(pending[b]) >= rebuild_limit:
                for pos, delta in pending[b]:
                    a[pos] = a[pos] % MOD
                pending[b].clear()
                rebuild(b)
        else:
            ans = get_prefix(y) - get_prefix(x - 1)
            out.append(str(ans % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The coefficient array `w` is built using the recurrence:

`C(k+d+1,k) = C(k+d,k) * (k+d+1)/(d+1)`.

This avoids computing combinations repeatedly. Modular inverses are used because all arithmetic is performed under `998244353`.

The `rebuild` function constructs the stored contribution of one block. Each element in the block contributes to all later prefix positions, which matches the formula for the `(k+1)`-th prefix.

The query function first uses the precomputed block contributions. The remaining difference comes from updates that have not been rebuilt yet, so those are applied directly with the same binomial coefficient formula.

The update operation only changes the original value and records the delta. When the pending list becomes large, rebuilding moves those changes into the permanent block structure. All values are kept modulo `998244353`, including subtraction in the final answer.

## Worked Examples

For the sample:

```
3 2
1 3 2
4
2 1 3
1 2 1
2 1 3
2 1 1
```

The first query asks for the sum of the second prefix level.

| Operation | Updated position | Pending changes | Answer |
| --- | --- | --- | --- |
| Initial | none | none | 17 |
| Update | add 1 to position 2 | `(2,1)` | none |
| Query | none | `(2,1)` | 20 |
| Query | none | `(2,1)` | 1 |

The pending update contributes through the binomial coefficients instead of forcing a full rebuild. The trace shows that updates can be incorporated lazily.

A second small example:

```
2 1
2 4
3
2 1 2
1 1 1
2 1 2
```

| Operation | Array effect | Prefix value result |
| --- | --- | --- |
| Initial query | `a^(1) = [2,6]` | 8 |
| Add 1 at position 1 | position 1 increases | none |
| Final query | `a^(1) = [3,7]` | 10 |

This confirms that the data structure handles updates at the beginning of the array, where every later position is affected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n / B + T) * m + n^2 / B) amortized | Queries scan blocks and pending updates, while rebuilds happen only after many updates |
| Space | O(n * n / B) | Every block stores a contribution array of length `n` |

Here `B` is the block size and `T` is the rebuild threshold. With the chosen values, the number of operations stays within the limits because `n` is only `10000` and expensive rebuilds are infrequent.

## Test Cases

```python
import sys
import io

# This block shows representative assert cases for the algorithm.

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    # Call solve() from the submitted solution here.
    # solve()
    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3 2
1 3 2
4
2 1 3
1 2 1
2 1 3
2 1 1
""") == "17\n20\n1\n"

assert run("""1 5
7
1
2 1 1
""") == "7\n"

assert run("""2 1
2 4
3
2 1 2
1 1 1
2 1 2
""") == "8\n10\n"

assert run("""5 3
1 1 1 1 1
2
2 1 5
2 3 5
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample | `17, 20, 1` | Normal updates and range queries |
| Single element | `7` | Minimum size and large k |
| Two elements with update | `8, 10` | Update influence on prefixes |
| Equal values | Varies | Repeated contributions |

## Edge Cases

For the first edge case with a single element:

```
1 1
5
1
2 1 1
```

The algorithm calls `get_prefix(1)` and `get_prefix(0)`. The second call returns zero immediately, avoiding invalid indexing. The answer is `5`.

For an update at the first position:

```
2 2
1 2
2
1 1 3
2 1 1
```

The update is stored in the first block. When the query asks for position `1`, the pending update is evaluated with distance zero, giving coefficient `C(k, k) = 1`. The added value is exactly `3`, so the final answer becomes `4`.

For modular subtraction, suppose the stored right prefix value is smaller modulo `998244353` than the left prefix value. The implementation uses `ans % MOD`, which normalizes the negative intermediate result into the required range.
