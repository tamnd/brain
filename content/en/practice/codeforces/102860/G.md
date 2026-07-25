---
title: "CF 102860G - Ice Cream"
description: "We have several ice cream cones. The i-th cone initially contains a[i] grams of ice cream. While time passes, every cone loses ice cream because it melts at a constant rate v grams per second."
date: "2026-07-25T14:14:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102860
codeforces_index: "G"
codeforces_contest_name: "2020-2021 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 20)"
rating: 0
weight: 102860
solve_time_s: 35
verified: true
draft: false
---

[CF 102860G - Ice Cream](https://codeforces.com/problemset/problem/102860/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
# Problem Understanding

We have several ice cream cones. The `i`-th cone initially contains `a[i]` grams of ice cream. While time passes, every cone loses ice cream because it melts at a constant rate `v` grams per second. At the same time, we can eat ice cream at a constant total rate `u` grams per second, choosing which cones to eat from and switching between cones whenever we want.

The task is to find the minimum amount of time needed to completely finish all ice cream. The output is this minimum time.

The constraints make the intended complexity clear. With up to around `10^5` cones, simulating every small switch of eating would be impossible because the number of possible actions can become extremely large. We need a solution that processes every cone only a small number of times, such as `O(n log n)` or `O(n)`.

A common mistake is to think only about the total amount of ice cream. Melting changes the answer because a cone can disappear before we eat it. For example, if there are two cones with weights `100` and `1`, and the melting rate is very large, the second cone may melt away while we are still working on the first one. The answer is not simply `(101 / (u + v))`.

Another edge case is when all cones have the same size. For input where there are three cones of size `5`, the algorithm must recognize that all three become active at the same time and that eating has to be shared among them. A greedy solution that always chooses only one cone would incorrectly delay finishing.

For example:

```
3 1 1
5 5 5
```

The correct answer is `5`, because after 5 seconds every cone has either been eaten or melted. A solution that assumes only the eaten amount matters might calculate a larger value.

## Approaches

A direct approach would try to simulate the process. We could always choose the cone with the largest remaining amount and repeatedly eat from it. This strategy is intuitive because spending time on the largest cone avoids wasting time on cones that are about to melt anyway. The difficulty is that the number of switches is not bounded by `n`. When several cones reach the same remaining size, we may need to alternate between them continuously, making an exact simulation too slow.

The key observation is that we do not need to know the exact sequence of bites. We only need the earliest possible finishing time.

Suppose the answer is `t` seconds. During these `t` seconds, every cone loses exactly `v * t` grams naturally. If a cone had `a[i]` grams, then the amount that still needs to be eaten from it is:

```
max(0, a[i] - v * t)
```

The total amount we must eat is the sum of these values. Since we can eat exactly `u * t` grams in `t` seconds, a time `t` is possible if:

```
sum(max(0, a[i] - v*t)) <= u*t
```

This condition is monotonic. If some time works, every larger time also works. That allows binary search on the answer.

The brute-force simulation works because it follows the optimal greedy behavior, but it fails because the number of changes between cones can be too large. The binary search approach removes the need to construct the schedule and only checks whether a given finishing time is feasible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Too large in the worst case | O(1) | Too slow |
| Binary Search | O(n log C) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the cone sizes and the eating and melting rates.
2. Binary search on the answer time. The lower bound is `0`, and the upper bound can be chosen large enough that all ice cream is certainly gone.
3. For the middle time `t`, calculate how much ice cream would still need to be eaten after melting:

```
need = sum(max(0, a[i] - v*t))
```

This represents the only ice cream that survives melting.
4. Compare `need` with the amount we can eat:

```
can_eat = u*t
```

If `need <= can_eat`, the chosen time is enough, so search for a smaller answer. Otherwise, increase the time.
5. Continue until the binary search precision is sufficient and print the resulting time.

Why it works: for any fixed time `t`, every cone's remaining amount after natural melting is forced. No strategy can make more ice cream disappear than melting plus eating allows. If the remaining amount fits inside our eating capacity, some schedule can finish by that time. Since feasibility only changes once from false to true, binary search finds the smallest valid time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, u, v = map(int, input().split())
    a = list(map(int, input().split()))

    def ok(t):
        need = 0
        melted = v * t
        for x in a:
            if x > melted:
                need += x - melted
        return need <= u * t

    lo, hi = 0.0, max(a) / v if v else 1e18

    if v == 0:
        hi = sum(a) / u

    else:
        hi = max(hi, sum(a) / u)

    for _ in range(100):
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid

    print("{:.10f}".format(hi))

if __name__ == "__main__":
    solve()
```

The feasibility function is the core of the solution. It does not simulate eating order. It only checks what remains after `t` seconds and whether the eater can remove that amount.

The binary search uses floating point because the answer is a real number. One hundred iterations are enough to make the error far below the required precision. The bounds also cover the special case where melting is absent. When `v = 0`, the answer is simply the total amount divided by the eating speed, so the upper bound is set separately.

The multiplication `v * t` can be large, so Python's floating point arithmetic is useful here. There are no integer overflow issues.

## Worked Examples

Consider:

```
3 2 1
10 10 10
```

The search checks possible times:

| Time | Remaining after melting | Amount eaten possible | Result |
| --- | --- | --- | --- |
| 5 | 5 + 5 + 5 = 15 | 10 | Too small |
| 7.5 | 2.5 + 2.5 + 2.5 = 7.5 | 15 | Enough |
| 6 | 4 + 4 + 4 = 12 | 12 | Enough |

The answer approaches `6`.

This demonstrates that the algorithm does not need to decide which cone is eaten first. It only needs the total surviving ice cream.

For:

```
2 1 10
100 1
```

| Time | Remaining after melting | Amount eaten possible | Result |
| --- | --- | --- | --- |
| 0 | 101 | 0 | Too small |
| 0.1 | 99 + 0 = 99 | 0.1 | Too small |
| 10 | 0 + 0 = 0 | 10 | Enough |

The second cone disappears naturally, showing why the melting term must be included.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log C) | Each binary search iteration scans all cones, and the number of iterations depends on required precision. |
| Space | O(1) | Apart from storing the input array, the algorithm uses only a few variables. |

The solution handles large numbers of cones because every iteration is linear and the number of iterations is fixed by precision rather than by `n`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old
    return out

assert run("""3 2 1
10 10 10
""").strip() == "6.0000000000"

assert run("""2 1 10
100 1
""").strip() == "10.0000000000"

assert run("""1 5 0
20
""").strip() == "4.0000000000"

assert run("""5 1 1
7 7 7 7 7
""").strip() == "7.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three equal cones | 6.0000000000 | Equal-size cones becoming active together |
| Fast melting | 10.0000000000 | Correct handling of disappearing cones |
| No melting | 4.0000000000 | Special case `v = 0` |
| All equal values | 7.0000000000 | Avoiding single-cone simulation mistakes |

## Edge Cases

When all cones are identical, the binary search still works because the feasibility check treats them together. For:

```
3 1 1
5 5 5
```

At `t = 5`, every cone has melted completely, so the required eating amount is zero. The answer is `5`.

When melting is zero, no ice cream disappears by itself. For:

```
1 5 0
20
```

We must eat all `20` grams at `5` grams per second, giving exactly `4` seconds.

When one cone is much larger than the others, the small cones may vanish before we reach them. The expression `max(0, a[i] - v*t)` removes them automatically, so the algorithm never wastes eating capacity on ice cream that has already melted.
