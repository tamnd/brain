---
title: "CF 1439B - Graph Subset Problem"
description: "Ah, now the issue is clear. The previous solution is not implementing the correct logic for the minimum time. The code I provided only considered taking a fixed number k of personal pickups in descending order of b[i], which is not what the problem asks."
date: "2026-06-11T04:29:53+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1439
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 684 (Div. 1)"
rating: 2600
weight: 1439
solve_time_s: 370
verified: false
draft: false
---

[CF 1439B - Graph Subset Problem](https://codeforces.com/problemset/problem/1439/B)

**Rating:** 2600  
**Tags:** constructive algorithms, data structures, graphs  
**Solve time:** 6m 10s  
**Verified:** no  

## Solution
Ah, now the issue is clear. The previous solution is **not implementing the correct logic** for the minimum time. The code I provided only considered taking a fixed number `k` of personal pickups in descending order of `b[i]`, which is **not what the problem asks**. The actual decision is **for each dish individually**: either take delivery or pick up personally, and the overall time is `max(total pickup time, longest courier time)`. Sorting `b` and taking the largest is not enough - we must check **every combination of pickup and delivery counts** efficiently.

The correct approach is:

1. Each dish can either be delivered (`a[i]`) or picked up (`b[i]`).
2. If we pick up `k` dishes personally, the total pickup time is the sum of `k` chosen `b[i]`.
3. For the remaining dishes, the maximum delivery time is `max(a[i] for delivered dishes)`.
4. We want to **minimize the maximum** between pickup sum and maximum courier delivery time.

This leads to an **efficient greedy approach**:

- Sort dishes by `b[i]` in descending order.
- Let `prefix[k]` be sum of top `k` `b[i]` values (total pickup time if Petya picks these `k` dishes personally).
- For `k = 0..n`, the answer is `max(prefix[k], max(a))` because the largest courier time is always among `a[i]`.
- But **we must also consider that if we pick some dishes personally, the remaining ones delivered may still have large `a[i]`**. So, we need `max(max(a[i] for dishes delivered), prefix[k])`.

A much simpler and correct observation is: **the minimum total time is `min(max(prefix[k], max(a)))` over all `k`**. But we have to sort `a` and `b` properly:

- `a_sorted` descending
- `b_sorted` descending
- Then, for each `k = 0..n`, the largest among `prefix[k]` and `a_sorted[n - k - 1]` (the largest courier time among the remaining dishes) gives the total time.

Let's write the **correct solution**:

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        # sort both arrays descending
        a_sorted = sorted(a, reverse=True)
        b_sorted = sorted(b, reverse=True)
        
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + b_sorted[i]
        
        ans = float('inf')
        for k in range(n + 1):
            # pick k dishes personally: sum of top k b[i]
            pickup_time = prefix[k]
            # remaining dishes delivered: largest remaining a[i]
            if k < n:
                delivery_time = a_sorted[k]
            else:
                delivery_time = 0
            ans = min(ans, max(pickup_time, delivery_time))
        print(ans)

if __name__ == "__main__":
    solve()
```

### Why this works:

- We consider **all possibilities**: `k = 0..n` dishes picked up personally.
- `prefix[k]` is total pickup time if Petya takes top `k` `b[i]` personally.
- `a_sorted[k]` is the **maximum delivery time among remaining dishes**. Sorting descending ensures `a_sorted[k]` is the largest among remaining.
- `max(pickup_time, delivery_time)` gives the total time for that choice.
- Taking `min` over all `k` ensures the **optimal combination**.

### Test on your sample input:

Input:

```
4
4
3 7 4 5
2 1 2 4
4
1 2 3 4
3 3 3 3
2
1 2
10 10
2
10 10
1 2
```

Output:

```
5
3
2
3
```

This matches the expected output exactly.

This solution is `O(n log n)` per test case, which is acceptable given constraints.

If you want, I can provide a **detailed trace table for the first test case** to show exactly how `k` is chosen and why the answer is `5`. This is useful to verify correctness. Do you want me to do that?
