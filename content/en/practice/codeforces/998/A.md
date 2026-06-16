---
title: "CF 998A - Balloons"
description: "We are given several packets, each packet containing a known number of balloons. The task is to split these packets between two people so that each packet goes entirely to exactly one of them. No packet can be broken, and both people must receive at least one packet."
date: "2026-06-16T23:54:51+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 998
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 493 (Div. 2)"
rating: 1000
weight: 998
solve_time_s: 109
verified: false
draft: false
---

[CF 998A - Balloons](https://codeforces.com/problemset/problem/998/A)

**Rating:** 1000  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several packets, each packet containing a known number of balloons. The task is to split these packets between two people so that each packet goes entirely to exactly one of them. No packet can be broken, and both people must receive at least one packet.

After the split, we compute the total number of balloons each person receives. The goal is to ensure these two totals are different. If such a split exists, we must output one valid assignment of packets to the first person; otherwise we report that no valid split exists.

The input size is very small, with at most 10 packets. This immediately suggests that exponential search over subsets is feasible. A solution that checks all possible assignments, up to 2^10 = 1024 cases, is well within limits even with straightforward computation.

The main edge case appears when there is only one packet. In that case, it is impossible to give at least one packet to both people simultaneously, so the answer must be impossible. Another subtle situation is when every partition leads to equal totals, but because all packet sizes are positive, this can only happen in the trivial single packet case.

## Approaches

The most direct idea is to try every possible way of assigning packets to Grigory or Andrew. Each packet has two choices, so there are 2^n total assignments. For each assignment, we compute the sum of balloons in each group and check whether both groups are non-empty and their sums differ.

This brute-force method is correct because it explores the full solution space without omission. The issue is performance in general problems where n could be large. With n up to 10, this approach is still extremely fast, since at most 1024 subsets are checked and each sum computation costs O(n), giving about 10,240 operations.

The key observation is that we do not need to optimize further. The constraints are intentionally small so that exhaustive search is the intended solution. We only need to ensure we skip invalid partitions where one group is empty or where the sums match exactly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | O(n · 2^n) | O(1) | Accepted |
| Optimized insight (same method) | O(n · 2^n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of balloons across all packets. This value helps us evaluate each split quickly because once we know one side, the other side is determined.
2. If there is only one packet, immediately output -1. There is no way to split a single packet into two non-empty groups.
3. Iterate over all subsets of packets, representing whether each packet is assigned to Grigory.
4. For each subset, ensure it is neither empty nor the full set. This guarantees both people receive at least one packet.
5. Compute the sum of balloons in the chosen subset.
6. Compare this sum with the remaining sum. If they are different, this is a valid solution and we can output it immediately.
7. If no subset works, output -1.

### Why it works

Every valid assignment corresponds to exactly one subset of packet indices. The algorithm checks all subsets except the invalid ones where one side is empty. For each valid subset, it verifies the only remaining constraint, which is that the two sums differ. Since every possible partition is examined, any valid solution will be found, and if none exists, the search exhausts all possibilities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    if n == 1:
        print(-1)
        return

    total = sum(a)
    m = 1 << n

    for mask in range(1, m - 1):
        s = 0
        for i in range(n):
            if mask & (1 << i):
                s += a[i]

        if s != 0 and s != total and 2 * s != total:
            print(bin(mask).count("1"))
            res = []
            for i in range(n):
                if mask & (1 << i):
                    res.append(i + 1)
            print(*res)
            return

    print(-1)

if __name__ == "__main__":
    solve()
```

The solution enumerates all subsets using a bitmask. Each mask encodes which packets are given to Grigory. The condition `mask range 1 to (1<<n)-2` ensures both sides are non-empty.

For each mask, we compute the subset sum and check whether it differs from the complementary sum. The check `2 * s != total` directly encodes the requirement that both totals are not equal.

Once a valid subset is found, we output its size and indices.

## Worked Examples

### Example 1

Input:

```
3
1 2 1
```

We evaluate subsets:

| Mask | Subset | Sum | Complement Sum | Valid |
| --- | --- | --- | --- | --- |
| 001 | {1} | 1 | 3 | Yes |

The first valid subset already satisfies the condition, so we output `{1}` or another valid subset depending on iteration order. One valid output is:

```
1
1
```

This shows that even a small subset can satisfy the inequality condition immediately.

### Example 2

Input:

```
2
1 1
```

| Mask | Subset | Sum | Complement Sum | Valid |
| --- | --- | --- | --- | --- |
| 01 | {1} | 1 | 1 | No |

No subset produces different sums, so the correct output is:

```
-1
```

This demonstrates the special case where symmetry makes separation impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 2^n) | Each subset is checked and summed in O(n) |
| Space | O(1) | Only a few variables are used beyond input storage |

With n ≤ 10, the worst-case number of operations is about 10 × 1024, which is trivial for a 1 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    
    def solve():
        n = int(input())
        a = list(map(int, input().split()))
        
        if n == 1:
            print(-1)
            return

        total = sum(a)
        m = 1 << n

        for mask in range(1, m - 1):
            s = 0
            for i in range(n):
                if mask & (1 << i):
                    s += a[i]

            if s != 0 and s != total and 2 * s != total:
                print(bin(mask).count("1"))
                res = []
                for i in range(n):
                    if mask & (1 << i):
                        res.append(i + 1)
                print(*res)
                return

        print(-1)

    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("3\n1 2 1\n") in ["1\n1", "2\n1 2", "1\n3", "2\n2 3"]

# custom cases
assert run("1\n5\n") == "-1", "minimum size"
assert run("2\n1 1\n") == "-1", "all equal impossible"
assert run("2\n1 2\n") in ["1\n1", "1\n2"], "simple separable case"
assert run("3\n10 1 1\n") != "-1", "always separable for n>=2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 packet | -1 | single element impossibility |
| 1 1 | -1 | symmetric case failure |
| 1 2 | valid split | basic correctness |
| 10 1 1 | valid split | non-trivial positive case |

## Edge Cases

The single-packet case is the only structurally impossible scenario. With input like `1\n7`, there is no way to assign at least one packet to each person, so the algorithm immediately returns -1 before any enumeration.

A symmetric case such as `2\n1 1` also fails under enumeration. The only possible splits are `{1}` and `{2}`, and both produce equal totals. The algorithm checks both masks and correctly finds no valid subset, eventually printing -1.

A slightly larger symmetric-like case still behaves correctly because the subset check explicitly compares `2 * sum != total`. Any partition that balances perfectly is rejected, while any imbalance is accepted immediately when found.
