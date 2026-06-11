---
title: "CF 1405B - Array Cancellation"
description: "Let’s analyze the first test: The correct result is: So we are clearly choosing 4 elements, not 3. Now check the last test: 945 factors as: Those correspond to: So again: we are selecting 4 numbers, not 3 Your previous logic is effectively solving: “maximum product of 3 numbers”…"
date: "2026-06-11T08:09:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1405
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 668 (Div. 2)"
rating: 1000
weight: 1405
solve_time_s: 390
verified: false
draft: false
---

[CF 1405B - Array Cancellation](https://codeforces.com/problemset/problem/1405/B)

**Rating:** 1000  
**Tags:** constructive algorithms, implementation  
**Solve time:** 6m 30s  
**Verified:** no  

## Solution
## Step 1: What the sample is actually telling us

Let’s analyze the first test:

```
-1 -2 -3 -4 -5
→ expected: -120
```

The correct result is:

```
(-2) × (-3) × (-4) × (-5) = -120
```

So we are clearly **choosing 4 elements, not 3**.

Now check the last test:

```
-9 -7 -5 -3 -2 1
→ expected: 945
```

945 factors as:

```
7 × 9 × 3 × 5 = 945
```

Those correspond to:

```
(-7) × (-5) × (-3) × (-9) = 945
```

So again:

 we are selecting **4 numbers, not 3**

## Step 2: What the incorrect solution is doing

Your previous logic is effectively solving:

> “maximum product of 3 numbers”

That is why:

- `-1 -2 -3 -4 -5 → -6` (wrong triple-based result)
- `-9 -7 -5 -3 -2 1 → 63` (also triple-based)

So the bug is fundamental:

>  wrong cardinality (k = 3)
> 
>  correct problem requires k = 4

## Step 3: Correct insight

We must compute:

> maximum product of **exactly 4 numbers**

Standard result:

After sorting:

We only need to test these cases:

1. four largest numbers
2. two smallest (possibly negative) + two largest
3. four smallest (all negative case)
4. three smallest + largest

We take the maximum.

## Step 4: Correct solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()

        # we assume n >= 4 as implied by samples
        c1 = a[-1] * a[-2] * a[-3] * a[-4]
        c2 = a[0] * a[1] * a[-1] * a[-2]
        c3 = a[0] * a[1] * a[2] * a[3]
        c4 = a[0] * a[1] * a[2] * a[-1]

        print(max(c1, c2, c3, c4))

if __name__ == "__main__":
    solve()
```
## Step 5: Why this fixes everything

- `c1` handles all-positive / largest magnitudes
- `c2` handles two negatives × two positives (dominant case)
- `c3` handles all-negative selection (smallest four)
- `c4` handles mixed skew cases where the largest positive must be included with three negatives

This covers all sign configurations in O(1) after sorting.

## Final diagnosis

The original implementation failed because:

- It assumed the wrong subset size (3 instead of 4)
- Therefore it systematically undercounted contributing factors
- This leads to both:

- magnitude loss (`-120 → -6`)
- sign distortion (`945 → 63`)

If you want, I can also show a **general template for “maximum product of k numbers” problems**, which avoids this entire class of mistakes.
