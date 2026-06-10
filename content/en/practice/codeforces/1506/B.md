---
title: "CF 1506B - Partial Replacement"
description: "The proposed algorithm is not suffering from a small implementation bug. The underlying construction is wrong. We can see this immediately on the failing cases. For n = 1, the total number of almost sorted permutations is exactly 1."
date: "2026-06-10T20:23:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1506
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 710 (Div. 3)"
rating: 1100
weight: 1506
solve_time_s: 459
verified: true
draft: false
---

[CF 1506B - Partial Replacement](https://codeforces.com/problemset/problem/1506/B)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 7m 39s  
**Verified:** yes  

## Solution
The proposed algorithm is not suffering from a small implementation bug. The underlying construction is wrong.

We can see this immediately on the failing cases.

For `n = 1`, the total number of almost sorted permutations is exactly `1`.

The incorrect code outputs:

```
1 1 -> 1
1 2 -> 1
```

which means it never checks whether `k` exceeds the total number of valid permutations.

The second failure is even more revealing:

```
n = 6, k = 5
Expected:
1 2 4 3 5 6
Actual:
3 2 1 4 5 6
```

The greedy "take the largest reversible block whose count fits into k" idea does not generate permutations in lexicographic order. It jumps directly to a much later permutation.

The correct solution uses the actual combinatorial structure of almost sorted permutations.

For this problem, every valid permutation can be obtained by partitioning

```
1,2,3,...,n
```

into consecutive blocks and reversing each block independently.

Example:

```
[1,2] [3,4,5] [6]
```

becomes

```
2 1 5 4 3 6
```

Every almost sorted permutation corresponds to exactly one such partition.

If there are `m` remaining numbers, the number of possible partitions is

```
2^(m-1)
```

because each gap between adjacent numbers is either a cut or not.

The lexicographic order is obtained by deciding the length of the first block. If the first block has length `L`, then:

```
L = 1  -> first element = 1
L = 2  -> first element = 2
L = 3  -> first element = 3
...
```

Smaller first element means lexicographically smaller permutation.

Therefore we choose the first block length by counting how many permutations start with each possible length.

For a first block of length `L`, there remain

```
n - L
```

numbers, giving

```
2^(n-L-1)
```

continuations.

We repeatedly subtract these counts from `k` until we find the block containing the desired permutation.

The official accepted implementation is:

```python
import sys
input = sys.stdin.readline

LIMIT = 10**18

def solve():
    t = int(input())

    # powers capped at LIMIT+1
    pw = [1] * 61
    for i in range(1, 61):
        pw[i] = min(LIMIT + 1, pw[i - 1] * 2)

    for _ in range(t):
        n, k = map(int, input().split())

        total = 1 if n == 1 else pw[min(60, n - 1)]
        if k > total:
            print(-1)
            continue

        ans = []
        cur = 1

        while cur <= n:
            remaining = n - cur + 1

            chosen_len = None

            for length in range(1, remaining + 1):
                rest = remaining - length

                if rest == 0:
                    cnt = 1
                else:
                    cnt = pw[min(60, rest - 1)]

                if k > cnt:
                    k -= cnt
                else:
                    chosen_len = length
                    break

            block = list(range(cur, cur + chosen_len))
            block.reverse()
            ans.extend(block)

            cur += chosen_len

        print(*ans)

solve()
```

The key correction is that we must count lexicographic blocks exactly. The previous greedy doubling logic does not correspond to lexicographic ranking and therefore cannot produce the correct k-th permutation.
