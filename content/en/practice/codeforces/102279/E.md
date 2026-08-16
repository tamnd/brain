---
title: "CF 102279E - Elevate To Dominate"
description: "We have (N) attack sets. Set (i) contains (Ai) attacks, and after a set is completed, the time needed for each future attack can only decrease, becoming the minimum of the current time and (Bi). Set 1 has already been completed, so the initial attack time is (B1)."
date: "2026-08-16T19:14:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102279
codeforces_index: "E"
codeforces_contest_name: "HCW 19 Team Round (ICPC format)"
rating: 0
weight: 102279
solve_time_s: 125
verified: true
draft: false
---

[CF 102279E - Elevate To Dominate](https://codeforces.com/problemset/problem/102279/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (N) attack sets. Set (i) contains (A_i) attacks, and after a set is completed, the time needed for each future attack can only decrease, becoming the minimum of the current time and (B_i). Set 1 has already been completed, so the initial attack time is (B_1). We may choose the order in which the remaining sets are completed.

The goal is to minimize the total time spent completing sets (2) through (N). Since (B_N=0), once set (N) is completed, every remaining attack takes zero time. Thus the real problem is to decide which sets should be completed before set (N), and in what order, so that set (N) itself becomes as cheap as possible.

The arrays have a particularly useful structure. The attack counts strictly increase, (A_1<A_2<\dots<A_N), while the times strictly decrease, (B_1>B_2>\dots>B_N). With (N\le 10^5), an (O(N^2)) dynamic program would require

[
\frac{N(N-1)}2
]

transitions, which is (4,999,950,000) transitions at the maximum input size. That is far beyond what a one-second limit can tolerate. We need an (O(N)) or (O(N\log N)) solution.

There are several boundary cases where the interpretation of the already completed first set and the final zero-cost set matters. For (N=1),

```
1
1
0
```

the answer is `0`, because there is nothing left to complete. A solution that adds the cost of the initial set as part of the answer is modeling the process incorrectly.

For

```
2
1 2
5 0
```

the answer is `10`. Set 1 is already finished, and set 2 requires two attacks at the current speed of 5. Its own (B_2=0) only affects the speed after set 2 is completed, so it cannot make those two attacks free.

A third edge case is that completing set (N) immediately is not always optimal. For the first sample, completing set 5 immediately costs (6\cdot5=30), but completing set 4 first costs (4\cdot5=20), after which set 5 costs (6\cdot1=6). The total is 26, so the optimal strategy deliberately pays for an intermediate set to lower the speed before handling the final set.

Finally, the answer can exceed 32-bit integer range. With (N=100000), (A_i=i), and (B_i=N-i), the answer is (N(N-1)=9,999,900,000). Python integers have arbitrary precision, so this does not require special handling in the implementation.

## Approaches

The brute-force dynamic program comes directly from considering the last set that is completed before set (i). Suppose that set (j<i) is the last set completed before (i). By that point the attack time has been reduced to (B_j), so completing set (i) costs (A_iB_j). If (dp[j]) is the minimum cost needed to reach that state, the candidate cost is

[
dp[j]+B_jA_i.
]

Thus

[
dp[i]=\min_{1\le j<i}\left(dp[j]+B_jA_i\right),
]

with (dp[1]=0). The answer is (dp[N]). This reduction is the standard form used for this monotone dynamic program.

The recurrence is correct because an optimal schedule can be represented by the indices of the sets that actually reduce the current attack time. Those indices are increasing. If (j) is the previous such index and (i) is the next one, all sets skipped between them can be completed later, after the attack time has become even smaller. In particular, after set (N) is completed the speed is zero, so those skipped sets contribute nothing. The entire cost of reaching (i) is consequently captured by one previous state (j) and the transition (B_jA_i).

Computing this recurrence directly checks every (j<i) for every (i). The exact number of transition evaluations is (N(N-1)/2), which is about five billion for (N=10^5). The brute-force formulation is useful because it exposes the structure of the optimal solution, but it cannot be used directly.

The key observation is that every candidate transition has the form

[
dp[j]+B_jA_i.
]

For a fixed (j), regard this as a line

[
y=B_jx+dp[j].
]

When computing (dp[i]), we query these lines at (x=A_i). The input guarantees that the slopes (B_j) are strictly decreasing, while the query coordinates (A_i) are strictly increasing. This is exactly the setting where a monotone Convex Hull Trick can maintain only the lines that can become optimal.

Because the queries move only to the right, once the second line in the hull becomes no worse than the first at the current query point, the first line can never become optimal again. Likewise, when a new line makes the middle line redundant between its two neighbors, that middle line can be discarded permanently.

The resulting algorithm inserts every line once, removes every line at most once, and processes every query once. The total work is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(N)) | Too slow |
| Optimal Convex Hull Trick | (O(N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Define (dp[i]) as the minimum time required to reach a state where set (i) has just been completed and its attack time is (B_i). Set 1 is already completed, so (dp[1]=0). The final answer is (dp[N]), because completing set (N) makes every later attack take zero time.
2. Rewrite the transition as

[
dp[i]=\min_{j<i}\left(B_jA_i+dp[j]\right).
]

For every fixed (j), this is a line with slope (B_j) and intercept (dp[j]). Computing (dp[i]) means finding the minimum line value at (x=A_i).

1. Store the candidate lines in a deque. The slopes arrive in strictly decreasing order because (B_1>B_2>\dots>B_N). The query positions arrive in strictly increasing order because (A_1<A_2<\dots<A_N).
2. Before querying (A_i), compare the first two lines in the deque. If the second line gives a value no larger than the first at (A_i), remove the first line. Since the first line has a larger slope and all future (A) values are even larger, it can never become better again.
3. After removing all obsolete lines from the front, evaluate the first remaining line at (A_i). This value is (dp[i]), because the deque contains exactly the candidate lines that can still be optimal.
4. Construct the new line

[
y=B_ix+dp[i].
]

Before appending it, inspect the last two lines and the new line. If the middle line lies above the lower envelope, it can never be the minimum for any future query, so remove it. This test is performed using cross multiplication, avoiding floating-point intersection calculations.

1. Append the new line and continue. Each line is inserted once and can be removed from either end only once, so the total number of deque operations is (O(N)).

Why it works: the invariant is that the deque contains the lower envelope of all lines generated so far, in the order in which they become optimal as (x) increases. The front-query rule removes a line only after a later line is already at least as good at the current (x), and the later line has a smaller slope, so it remains at least as good for every future (x). The back-removal rule discards a line whose interval of optimality has disappeared between its neighboring lines. Consequently, the front line always represents an optimal transition for the current (A_i), so the computed value is exactly the dynamic-programming optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if n == 1:
        print(0)
        return

    # Each line is represented as (slope, intercept).
    # We need minimum values, slopes are strictly decreasing,
    # and query x-values are strictly increasing.
    hull = [(b[0], 0)]
    head = 0

    dp = [0] * n

    def value(line, x):
        m, c = line
        return m * x + c

    for i in range(1, n):
        x = a[i]

        # Remove lines that can never be optimal again.
        while head + 1 < len(hull) and value(hull[head], x) >= value(hull[head + 1], x):
            head += 1

        dp[i] = value(hull[head], x)

        new_line = (b[i], dp[i])

        # Remove redundant lines from the back.
        while len(hull) - head >= 2:
            l1 = hull[-2]
            l2 = hull[-1]
            l3 = new_line

            m1, c1 = l1
            m2, c2 = l2
            m3, c3 = l3

            # Intersection(l1, l2) >= Intersection(l2, l3)
            # means l2 can never be the minimum on a future query.
            if (c2 - c1) * (m2 - m3) >= (c3 - c2) * (m1 - m2):
                hull.pop()
            else:
                break

        hull.append(new_line)

    print(dp[-1])

if __name__ == "__main__":
    solve()
```

The input arrays are stored directly because all transitions use the original (A_i) and (B_i) values. The first line is initialized as `(B1, 0)`, which corresponds exactly to (dp[1]=0).

The main loop starts from index 1, representing set 2. This is necessary because set 1 has already been completed and must not be charged again. At iteration (i), the current query coordinate is `a[i]`, and the front of the hull gives the optimal previous set.

The front pointer `head` avoids physically deleting lines from the front. Once a line becomes obsolete, advancing `head` is enough. Lines removed from the back are physically popped because they are redundant regardless of future queries.

The back condition compares intersections without division:

[
\frac{c_2-c_1}{m_1-m_2}
\ge
\frac{c_3-c_2}{m_2-m_3}.
]

The slope differences are positive because the slopes are strictly decreasing. Cross multiplication is exact, and Python's integers cannot overflow. Using floating-point intersection coordinates here would introduce unnecessary precision risks.

The final line for set (N) has slope (B_N=0). Its value is precisely the minimum total cost of reaching set (N). Once that set is completed, every remaining set is free, so no additional term is required.

## Worked Examples

For Sample 1,

```
5
1 2 3 4 6
5 4 3 1 0
```

the dynamic-programming states are as follows.

| Set (i) | (A_i) | (B_i) | Best previous set | (dp[i]) | Hull decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | already completed | 0 | insert (5x) |
| 2 | 2 | 4 | 1 | 10 | insert (4x+10) |
| 3 | 3 | 3 | 1 | 15 | line 2 becomes redundant |
| 4 | 4 | 1 | 1 | 20 | line 3 becomes redundant |
| 5 | 6 | 0 | 4 | 26 | insert final line |

For set 5, choosing set 4 as the previous speed-changing set gives

[
dp[4]+B_4A_5=20+1\cdot6=26.
]

The corresponding schedule is to complete set 4 first, then set 5. Sets 2 and 3 can be postponed until after set 5, when their cost is zero.

For Sample 2,

```
6
1 2 3 8 9 10
5 4 3 2 1 0
```

the states are:

| Set (i) | (A_i) | (B_i) | Best previous set | (dp[i]) | Hull decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 5 | already completed | 0 | insert (5x) |
| 2 | 2 | 4 | 1 | 10 | insert (4x+10) |
| 3 | 3 | 3 | 1 | 15 | remove redundant line |
| 4 | 8 | 2 | 3 | 39 | remove obsolete front lines |
| 5 | 9 | 1 | 3 | 42 | keep relevant envelope |
| 6 | 10 | 0 | 3 | 45 | final answer |

The final transition uses set 3:

[
dp[6]=dp[3]+B_3A_6
=15+3\cdot10
=45.
]

This corresponds to the sample's strategy of completing set 3, then set 6. Once set 6 is complete, every remaining set can be completed at zero cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N)) | Each line is inserted once and removed at most once, while each query advances the front pointer monotonically. |
| Space | (O(N)) | The hull and the input arrays contain (O(N)) values. |

With (N\le10^5), the linear solution performs only a constant number of arithmetic operations per element apart from amortized deque removals. It comfortably avoids the roughly five billion transitions of the quadratic dynamic program. Python's arbitrary-precision integers also safely handle products and answers larger than 32-bit range.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    if n == 1:
        print(0)
        return

    hull = [(b[0], 0)]
    head = 0
    dp = [0] * n

    def value(line, x):
        return line[0] * x + line[1]

    for i in range(1, n):
        x = a[i]

        while head + 1 < len(hull) and value(hull[head], x) >= value(hull[head + 1], x):
            head += 1

        dp[i] = value(hull[head], x)

        new_line = (b[i], dp[i])

        while len(hull) - head >= 2:
            m1, c1 = hull[-2]
            m2, c2 = hull[-1]
            m3, c3 = new_line

            if (c2 - c1) * (m2 - m3) >= (c3 - c2) * (m1 - m2):
                hull.pop()
            else:
                break

        hull.append(new_line)

    print(dp[-1])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run(
    "5\n"
    "1 2 3 4 6\n"
    "5 4 3 1 0\n"
) == "26", "sample 1"

assert run(
    "6\n"
    "1 2 3 8 9 10\n"
    "5 4 3 2 1 0\n"
) == "45", "sample 2"

# Minimum-size input
assert run(
    "1\n"
    "1\n"
    "0\n"
) == "0", "only the already-completed set exists"

# Boundary case: the first set must not be charged again
assert run(
    "2\n"
    "1 2\n"
    "5 0\n"
) == "10", "set 1 is already completed"

# All A values equal, outside the official constraints.
# This checks that equal query coordinates do not break the hull logic.
assert run(
    "3\n"
    "1 1 1\n"
    "2 1 0\n"
) == "2", "equal query coordinates"

# Maximum-size case and large answer.
# A[i] = i, B[i] = n-i, so the answer is n*(n-1).
n = 100000
a = " ".join(map(str, range(1, n + 1)))
b = " ".join(map(str, range(n - 1, -1, -1)))
expected = str(n * (n - 1))

assert run(f"{n}\n{a}\n{b}\n") == expected, "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 0` | `0` | Minimum-size input and already completed first set |
| `2 / 1 2 / 5 0` | `10` | Boundary between the initial state and the first actual transition |
| `3 / 1 1 1 / 2 1 0` | `2` | Equal query coordinates, outside the official constraints |
| (N=100000,\ A_i=i,\ B_i=N-i) | `9999900000` | Maximum size and large integer arithmetic |

The all-equal test is deliberately marked as outside the official input guarantees. A valid problem instance cannot have all (A_i) equal because the (A_i) values must be strictly increasing, and it cannot have all (B_i) equal because the (B_i) values must be strictly decreasing and (B_N=0). It is still useful as an implementation robustness check because the query logic remains valid for nondecreasing (A_i).

## Edge Cases

For the minimum case,

```
1
1
0
```

the algorithm enters the `n == 1` branch and prints `0`. There is no transition to compute because the only set has already been completed. The hull is never needed.

For the initial-state boundary,

```
2
1 2
5 0
```

the hull starts with the line (5x), representing set 1 with (dp[1]=0). The query for set 2 is at (x=2), so the value is (5\cdot2=10). The algorithm prints `10`. It never adds (1\cdot5), because set 1 is not part of the remaining work.

For the case where going directly to the final set is not optimal,

```
5
1 2 3 4 6
5 4 3 1 0
```

the relevant transition for set 5 is through set 4. The algorithm computes (dp[4]=20), then evaluates the line for set 4 at (A_5=6):

[
20+1\cdot6=26.
]

The direct transition from set 1 would cost (0+5\cdot6=30), so the hull correctly chooses set 4 and produces `26`.

For the large-value case with (N=100000), (A_i=i), and (B_i=N-i), the first line represents (dp[1]=0). For every (i), using set 1 gives

[
dp[1]+B_1A_i=(N-1)i.
]

For this particular construction, every later transition is no better, so

[
dp[N]=N(N-1)=9,999,900,000.
]

The result is larger than (2^{31}-1), which catches implementations using 32-bit arithmetic. Python's integer representation handles the value directly.

For equal query coordinates, such as

```
3
1 1 1
2 1 0
```

the first transition gives (dp[2]=2). At the third query, both the line (2x) and the line (x+2) evaluate to 2 at (x=1). The front-query condition allows the older line to be discarded on equality, and the answer remains `2`. This test is outside the official strict-increasing condition, but it confirms that the implementation does not depend on floating-point intersection comparisons or strictly distinct query coordinates.
