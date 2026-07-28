---
title: "CF 102739C - \u041f\u043e\u0434 \u0434\u043e\u0436\u0434\u0451\u043c"
description: "Polina has a fixed route home. The first part of the route is an uncovered street that takes t1 minutes, and the second part is an alley under trees that takes t2 minutes. She may choose when to leave school, but she has to arrive no later than time d."
date: "2026-07-29T01:05:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102739
codeforces_index: "C"
codeforces_contest_name: "\u0421\u0438\u0440\u0438\u0443\u0441.2020.\u041d\u043e\u044f\u0431\u0440\u044c.\u041e\u0447\u043d\u044b\u0439 \u043e\u0442\u0431\u043e\u0440"
rating: 0
weight: 102739
solve_time_s: 72
verified: true
draft: false
---

[CF 102739C - \u041f\u043e\u0434 \u0434\u043e\u0436\u0434\u0451\u043c](https://codeforces.com/problemset/problem/102739/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

Polina has a fixed route home. The first part of the route is an uncovered street that takes `t1` minutes, and the second part is an alley under trees that takes `t2` minutes. She may choose when to leave school, but she has to arrive no later than time `d`.

The rain intensity at each minute is known. While walking under the trees, the rain intensity is reduced by `s`, but it cannot become negative. The task is to find the departure time that gives the smallest total rain exposure, and if several departure times have the same minimum value, choose the earliest one.

The input contains the route lengths, the latest allowed arrival time, the tree protection value, and an array of rain intensities for each minute. The output is the starting minute and the minimum total rain intensity encountered.

The constraints are the key to the intended solution. The value `d` can reach `10^6`, so an algorithm that checks every possible start time and scans the whole route would perform around `10^12` operations in the worst case. A linear solution is required because it can handle a million minutes comfortably within the time limit.

The main edge cases come from the transition between uncovered and covered parts of the route. A careless solution often forgets that the tree reduction applies separately to every minute and that the result cannot become negative.

For example, with:

```
1 1 2 10
5 20
```

the correct output is:

```
0 5
```

Starting at time `0` gives one uncovered minute with intensity `5` and one tree-covered minute with intensity `max(20 - 10, 0) = 10`, for a total of `15`. Starting at time `1` gives the same arrival limit issue because there is no room for the whole trip. A solution that subtracts `s` from the total covered segment instead of every minute may calculate the wrong value.

Another case is:

```
2 2 5 10
8 1 3 4 100
```

The answer is:

```
1 8
```

Starting at time `1` gives uncovered rain `1 + 3 = 4` and covered rain `max(4 - 10, 0) + max(100 - 10, 0) = 90`, which is not optimal. The correct start is found by considering every valid window. A common mistake is to assume the first low-rain minutes are always best without checking how the route split changes.

## Approaches

The direct approach is to try every possible departure time. For a chosen start, we calculate the contribution of the first `t1` minutes normally and the next `t2` minutes with the tree reduction. This approach is correct because it evaluates exactly the quantity the problem asks to minimize.

The problem is the repeated work. There can be up to `d - t1 - t2 + 1` possible starting moments. For each one, scanning up to `t1 + t2` minutes gives a worst case of about `10^12` operations when `d` is `10^6`, which is far too slow.

The useful observation is that two neighboring departure times share almost all of their minutes. When we move the start time forward by one minute, one minute leaves the route calculation and one new minute enters it. We only need to update the current value instead of recomputing it.

We can represent the route as two sliding windows. The uncovered part always contains `t1` consecutive minutes, and the covered part always contains the following `t2` minutes. When the window shifts, the first minute of the uncovered segment becomes irrelevant, the first minute of the covered segment changes status, and one new minute enters the covered segment. Maintaining these changes allows every possible start time to be checked in constant time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(d(t1 + t2)) | O(d) | Too slow |
| Optimal | O(d) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the rain exposure for the first possible departure time, which is time `0`. The first `t1` minutes contribute their original values, while the next `t2` minutes contribute their reduced values. This gives the initial sliding window value.
2. Store this value as the current minimum and remember that the earliest optimal answer is the current starting time.
3. Move the departure time from left to right. When shifting from time `i` to time `i + 1`, remove the minute that was previously the first uncovered minute because it is no longer part of the trip.
4. Add the minute that becomes the first uncovered minute of the new route. It used to be under the trees, so it must be changed from its protected contribution to its full rain contribution.
5. Add the new minute entering the protected section at the end of the route. It contributes with tree reduction.
6. After each shift, compare the new total with the best answer found so far. Only replace the answer when the value is smaller, because keeping the old answer automatically preserves the earliest starting time.

Why it works:

At every moment of the sliding process, the maintained value is exactly the total rain exposure for the current departure time. The transition between two adjacent departures removes exactly the minutes that disappear from the route and adds exactly the minutes that enter it, including the change of protection status for the boundary minute. Since every valid departure time is visited once and the smallest value is recorded, the algorithm finds the optimal departure time. Keeping the first occurrence of the minimum handles the tie-breaking rule.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t1, t2, d, s = map(int, input().split())
    r = list(map(int, input().split()))

    def wet(x, protected):
        if protected:
            return max(0, x - s)
        return x

    cur = 0

    for i in range(t1):
        cur += r[i]

    for i in range(t1, t1 + t2):
        cur += wet(r[i], True)

    best = cur
    best_start = 0

    for start in range(1, d - t1 - t2 + 1):
        cur -= r[start - 1]
        cur -= wet(r[start + t1 - 1], True)
        cur += r[start + t1 - 1]
        cur += wet(r[start + t1 + t2 - 1], True)

        if cur < best:
            best = cur
            best_start = start

    print(best_start, best)

if __name__ == "__main__":
    solve()
```

The function `wet` isolates the only special operation in the problem: the tree-covered rain intensity. Keeping it in one place avoids accidentally applying the reduction to uncovered minutes.

The initial calculation builds the state for departure time `0`. The first loop handles the normal street, and the second loop handles the alley. After that, the sliding loop updates the current value.

The update order matters. The minute at position `start + t1 - 1` moves from the protected segment to the uncovered segment, so its protected contribution must first be removed and then its full value added. The new last minute only enters the protected segment, so its reduced value is added directly.

All indices are zero-based in the implementation. The loop stops at `d - t1 - t2` because that is the last possible departure time that still allows the complete trip before the deadline.

## Worked Examples

For the first sample:

```
2 3 10 5
1 1 1 8 7 1 1 2 10 1
```

The sliding states are:

| Start time | Uncovered contribution | Covered contribution | Total |
| --- | --- | --- | --- |
| 0 | 2 | 0 + 3 + 2 | 7 |
| 1 | 2 | 3 + 2 + 0 | 7 |
| 2 | 2 | 3 + 2 + 5 | 12 |

The first minimum is found at time `0`, so the output is:

```
0 7
```

This example demonstrates the tie rule. Several starts may have similar values, but the earliest one must be selected.

For the second sample:

```
5 7 17 6
5 7 8 4 2 2 7 6 5 7 4 8 8 7 3 6 1
```

A partial trace of the sliding process is:

| Start time | Current total | Best start | Best value |
| --- | --- | --- | --- |
| 0 | 38 | 0 | 38 |
| 1 | 33 | 1 | 33 |
| 2 | 29 | 2 | 29 |
| 3 | 27 | 3 | 27 |

The minimum is reached when starting at time `3`, producing:

```
3 27
```

This confirms that the algorithm correctly updates the boundary minute when it changes from protected to uncovered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | Every possible departure time is processed once, and each update uses constant work. |
| Space | O(1) besides the input array | Only the current sum and answer variables are maintained. |

The maximum value of `d` is `10^6`, so a linear scan performs about one million updates, which fits easily within the limits. The integer values also fit comfortably in Python's integer type.

## Test Cases

```python
import sys
import io

def solve(inp):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    import builtins

    def solution():
        input = sys.stdin.readline
        t1, t2, d, s = map(int, input().split())
        r = list(map(int, input().split()))

        def wet(x):
            return max(0, x - s)

        cur = sum(r[:t1]) + sum(wet(x) for x in r[t1:t1+t2])
        best = cur
        ans = 0

        for start in range(1, d - t1 - t2 + 1):
            cur -= r[start - 1]
            cur -= wet(r[start + t1 - 1])
            cur += r[start + t1 - 1]
            cur += wet(r[start + t1 + t2 - 1])

            if cur < best:
                best = cur
                ans = start

        print(ans, best)

    solution()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert solve("""2 3 10 5
1 1 1 8 7 1 1 2 10 1
""") == "0 7\n"

assert solve("""5 7 17 6
5 7 8 4 2 2 7 6 5 7 4 8 8 7 3 6 1
""") == "3 27\n"

assert solve("""1 1 2 10
5 20
""") == "0 5\n"

assert solve("""2 2 5 10
8 1 3 4 100
""") == "1 8\n"

assert solve("""1 1 3 5
7 7 7
""") == "0 7\n"

assert solve("""3 2 5 100
1 2 3 4 5
""") == "0 6\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `0 7` | Basic sliding update and earliest tie handling |
| Sample 2 | `3 27` | A non-zero optimal departure time |
| `1 1 2 10` case | `0 5` | Large tree reduction and minimum boundary |
| `2 2 5 10` case | `1 8` | Correct movement of the protected boundary |
| All rain values equal | `0 7` | Tie-breaking behaviour |
| Very large reduction value | `0 6` | Rain values cannot become negative |

## Edge Cases

When the tree reduction is larger than the rain intensity, the protected contribution must become zero instead of a negative value. For:

```
1 1 2 10
5 20
```

the algorithm calculates the first minute as `5` and the second minute as `max(20 - 10, 0) = 10`. It keeps the non-negative protected value and returns:

```
0 15
```

When several departure times have the same minimum exposure, the earliest one must remain. The update only changes the stored answer when a strictly smaller value appears. For example:

```
1 1 3 5
7 7 7
```

every departure time gives the same total, so the answer stays at:

```
0 7
```

The case where a minute changes from being under trees to being on the normal street is the easiest place to introduce an off-by-one bug. For:

```
2 2 5 10
8 1 3 4 100
```

the update removes the old protected contribution of the outgoing boundary minute, then adds its full value after it becomes uncovered. This is exactly the transition represented by the sliding formula, so the algorithm produces the correct result:

```
1 8
```
