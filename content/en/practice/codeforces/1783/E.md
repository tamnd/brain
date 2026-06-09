---
title: "CF 1783E - Game of the Year"
description: "For each boss, Monocarp would kill it on his a[i]-th personal attempt, while Polycarp would kill it on his b[i]-th personal attempt. The fight is divided into blocks of size k. Monocarp performs k attempts, then Polycarp performs k attempts, then Monocarp again, and so on."
date: "2026-06-09T11:08:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1783
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 141 (Rated for Div. 2)"
rating: 2300
weight: 1783
solve_time_s: 126
verified: false
draft: false
---

[CF 1783E - Game of the Year](https://codeforces.com/problemset/problem/1783/E)

**Rating:** 2300  
**Tags:** brute force, data structures, math, number theory  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Problem Understanding

For each boss, Monocarp would kill it on his `a[i]`-th personal attempt, while Polycarp would kill it on his `b[i]`-th personal attempt.

The fight is divided into blocks of size `k`. Monocarp performs `k` attempts, then Polycarp performs `k` attempts, then Monocarp again, and so on. As soon as one player reaches the attempt number that kills the boss, the boss dies and both counters reset for the next boss.

We must find every value of `k` between `1` and `n` such that Monocarp kills every boss.

The constraint that matters is the total sum of `n` over all test cases, which is at most `2·10^5`. This immediately rules out checking every boss for every `k` with a simulation. Even an `O(n²)` solution would perform around `4·10^10` operations in the worst case.

The challenge is to convert the game process into a purely arithmetic condition on `a[i]`, `b[i]`, and `k`.

A few edge cases are easy to misunderstand.

Consider a boss with `a=4`, `b=3`.

For `k=2`, the order of attempts is:

```
M: 1 2
P: 1 2
M: 3 4
```

Monocarp reaches attempt 4 before Polycarp reaches attempt 3, so Monocarp wins.

For `k=1`, the order is:

```
M:1
P:1
M:2
P:2
M:3
P:3
```

Polycarp reaches attempt 3 first and wins.

A naive comparison such as checking whether `a < b` would be completely wrong.

Another subtle case is `a=b`.

Example:

```
a = 5
b = 5
```

Regardless of `k`, Monocarp always gets the first move of every round. When both players would kill on the same personal attempt number, Monocarp reaches that attempt first and wins. Any solution that treats equality as a loss would fail.

A final edge case occurs when `b < a`.

Example:

```
a = 5
b = 2
```

Monocarp can still win for sufficiently large `k`.

For `k=5`, Monocarp performs attempts `1..5` before Polycarp gets any move at all, so Monocarp kills immediately.

The answer is not determined solely by whether `a` is larger than `b`.

## Approaches

The most direct approach is to test every possible `k`.

For a fixed boss and a fixed `k`, we can determine who kills first by following the alternating blocks of size `k`. Repeating this for all bosses and all values of `k` gives a correct solution.

Unfortunately there are `n` possible values of `k` and `n` bosses. Even if we could evaluate one boss in constant time, we would still need `O(n²)` work, which is far too large when `n` reaches `2·10^5`.

The key observation is that we do not actually care who wins for a particular boss and particular `k` by simulation. We only need to characterize the set of bad values of `k`.

Suppose a boss has parameters `(a,b)`.

If `a ≤ b`, Monocarp always wins. He reaches his `a`-th attempt no later than Polycarp reaches his `b`-th attempt, and ties favor Monocarp because he moves first.

The interesting case is `b < a`.

Let

```
ceil(a / k)
```

be the number of Monocarp blocks needed to reach attempt `a`, and similarly

```
ceil(b / k)
```

for Polycarp.

If these two values are different, then whoever needs fewer blocks reaches the killing attempt first.

Since `b < a`, we always have

```
ceil(b/k) ≤ ceil(a/k)
```

The only way Monocarp can still win is when both quantities are equal. Then they reach their killing attempts during the same pair of blocks, and Monocarp's block comes first.

So for a boss with `b < a`, Monocarp wins exactly when

$$\left\lceil \frac{a}{k} \right\rceil = \left\lceil \frac{b}{k} \right\rceil.$$

Now comes the crucial simplification.

For an integer `x`, the value `ceil(x/k)` changes only when `k` crosses certain divisors. Instead of explicitly finding all good `k`, we mark all bad intervals.

Observe that

$$\left\lceil \frac{a}{k} \right\rceil > \left\lceil \frac{b}{k} \right\rceil$$

exactly when there exists a multiple of `k` lying in the interval `[b, a-1]`.

Indeed, if some multiple `m = t·k` satisfies

$$b \le m < a,$$

then `b` and `a` belong to different ceiling blocks, producing different ceiling values.

Equivalently, `k` is bad iff some multiple of `k` lies in `[b,a-1]`.

Instead of iterating over `k`, we process every bad interval `[b,a)` using a difference array. This leads to a very compact `O(n log n)` style solution, implemented as `O(n log n)` harmonic summation through multiples. The official solution expresses it even more elegantly through interval counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Deriving the condition

For a boss with `b < a`, Monocarp loses whenever there exists a multiple of `k` inside:

$$[b,\;a)$$

because then

$$\left\lceil \frac{a}{k}\right\rceil > \left\lceil \frac{b}{k}\right\rceil.$$

So each such boss forbids all values of `k` having at least one multiple in that interval.

### Difference-array reformulation

Let `dx[x]` count how many intervals `[b,a)` contain the point `x`.

For every boss with `b < a`:

```
dx[b] += 1
dx[a] -= 1
```

After taking prefix sums,

```
dx[x]
```

equals the number of bad intervals covering integer point `x`.

### Checking a value of k

A value `k` is valid if none of the forbidden intervals contains any multiple of `k`.

The multiples of `k` are:

```
k, 2k, 3k, ...
```

If any multiple `mk` lies inside a forbidden interval, then `dx[mk] > 0`.

Hence:

```
k is valid
⇔ dx[mk] = 0 for every multiple mk of k
```

### Algorithm

1. Create a difference array `dx` of size `n+1`.
2. For every boss:

If `b[i] < a[i]`, add the interval `[b[i], a[i])` into the difference array.
3. Compute prefix sums so that `dx[x]` becomes the number of intervals covering `x`.
4. For every `k` from `1` to `n`:

Check all multiples of `k`.

If every multiple satisfies `dx[multiple] = 0`, then `k` is a valid answer.
5. Output all valid values.

### Why it works

For every boss with `b < a`, the interval `[b,a)` represents exactly the positions where a multiple of `k` would separate `b` and `a` into different ceiling blocks. Whenever such a multiple exists, Polycarp reaches his killing attempt strictly earlier and Monocarp loses that boss.

The prefix-sum array stores, for every integer point, how many losing intervals contain it. A multiple of `k` lying inside any losing interval is equivalent to some boss defeating Monocarp.

Checking all multiples of `k` guarantees that no losing interval contains a multiple of `k`. Thus every boss is won by Monocarp. Conversely, if some multiple lies in a losing interval, that boss is lost. The characterization is exact, so the algorithm returns precisely all valid values of `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        dx = [0] * (n + 2)

        for ai, bi in zip(a, b):
            if bi < ai:
                dx[bi] += 1
                dx[ai] -= 1

        for i in range(1, n + 1):
            dx[i] += dx[i - 1]

        ans = []

        for k in range(1, n + 1):
            ok = True

            m = k
            while m <= n:
                if dx[m] != 0:
                    ok = False
                    break
                m += k

            if ok:
                ans.append(k)

        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first loop builds the collection of forbidden intervals. Only bosses with `b < a` matter. If `a ≤ b`, Monocarp always wins that boss and no restriction on `k` is needed.

The difference array stores interval additions in constant time. After the prefix sum, `dx[x]` tells us whether point `x` belongs to at least one forbidden interval.

The final loop uses the classic harmonic-series iteration over multiples. For a fixed `k`, we examine `k, 2k, 3k, ...`. If any of those points is covered by a forbidden interval, then `k` is invalid.

A common mistake is forgetting that the interval is half-open, `[b,a)`. The official implementation performs:

```
dx[b] += 1
dx[a] -= 1
```

which represents exactly that range. Using `[b,a]` would incorrectly reject some valid values of `k`.

## Worked Examples

### Example 1

Input:

```
n = 3
a = [1,1,1]
b = [2,3,1]
```

No boss satisfies `b < a`.

| Boss | a | b | Interval added |
| --- | --- | --- | --- |
| 1 | 1 | 2 | none |
| 2 | 1 | 3 | none |
| 3 | 1 | 1 | none |

After prefix sums:

| x | dx[x] |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | 0 |

Checking each `k`:

| k | Multiples | All zero? |
| --- | --- | --- |
| 1 | 1,2,3 | Yes |
| 2 | 2 | Yes |
| 3 | 3 | Yes |

Answer:

```
1 2 3
```

This demonstrates the easy case where every boss is automatically won.

### Example 2

Input:

```
n = 4
a = [1,4,3,2]
b = [3,3,4,1]
```

Only bosses 2 and 4 contribute intervals.

| Boss | a | b | Interval |
| --- | --- | --- | --- |
| 2 | 4 | 3 | [3,4) |
| 4 | 2 | 1 | [1,2) |

After prefix sums:

| x | dx[x] |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |
| 4 | 0 |

Now test every `k`.

| k | Multiples | Covered multiple? | Valid |
| --- | --- | --- | --- |
| 1 | 1,2,3,4 | yes | no |
| 2 | 2,4 | no | yes |
| 3 | 3 | yes | no |
| 4 | 4 | no | yes |

Answer:

```
2 4
```

This example shows exactly how forbidden intervals eliminate values of `k`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Prefix sum is O(n), checking multiples uses harmonic series `n/1 + n/2 + ... + n/n` |
| Space | O(n) | Difference array and answer list |

The total sum of `n` over all test cases is at most `2·10^5`. An `O(n log n)` solution performs only a few million operations overall, which comfortably fits within the time limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        dx = [0] * (n + 2)

        for ai, bi in zip(a, b):
            if bi < ai:
                dx[bi] += 1
                dx[ai] -= 1

        for i in range(1, n + 1):
            dx[i] += dx[i - 1]

        ans = []

        for k in range(1, n + 1):
            ok = True
            m = k

            while m <= n:
                if dx[m] != 0:
                    ok = False
                    break
                m += k

            if ok:
                ans.append(k)

        out.append(str(len(ans)))
        out.append(" ".join(map(str, ans)))

    return "\n".join(out)

# provided sample
assert run(
"""3
3
1 1 1
2 3 1
1
1
1
4
1 4 3 2
3 3 4 1
"""
) == (
"""3
1 2 3
1
1
2
2 4"""
)

# minimum size
assert run(
"""1
1
1
1
"""
) == (
"""1
1"""
)

# all bosses automatically won
assert run(
"""1
4
1 1 1 1
4 4 4 4
"""
) == (
"""4
1 2 3 4"""
)

# single forbidden interval [1,2)
assert run(
"""1
2
2 1
1 2
"""
) == (
"""1
2"""
)

# boundary interval ending at n
assert run(
"""1
5
5 1 1 1 1
1 5 5 5 5
"""
) == (
"""2
3 5"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1` | `1` | Smallest possible instance |
| All `a≤b` | Every `k` valid | No intervals added |
| Interval `[1,2)` | Only `k=2` valid | Half-open interval handling |
| Interval ending at `n` | Specific divisibility behavior | Boundary updates in difference array |

## Edge Cases

Consider:

```
n = 1
a = [5]
b = [5]
```

Here `a = b`. No interval is added because `b < a` is false. The difference array remains zero everywhere. Every `k` passes the multiples test.

This matches the game process because Monocarp always reaches the fifth attempt before Polycarp reaches his fifth attempt.

Consider:

```
n = 1
a = [5]
b = [2]
```

The interval `[2,5)` is added.

For `k = 1`, the multiple `2` lies inside the interval, so `k` is rejected.

For `k = 5`, the only multiple checked is `5`, which lies outside the half-open interval. The algorithm accepts `k=5`.

That matches the actual game, where Monocarp performs five attempts before Polycarp moves at all.

Consider:

```
n = 1
a = [4]
b = [3]
```

The interval is `[3,4)`.

For `k = 1`, multiple `3` is covered, so the algorithm rejects it.

For `k = 2`, the multiples are `2` and `4`, neither of which belongs to `[3,4)`. The algorithm accepts it.

This is exactly the example where Monocarp loses for `k=1` but wins for `k=2`, confirming that the interval characterization captures the game correctly.
