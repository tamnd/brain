---
title: "CF 28C - Bath Queue"
description: "Every student independently chooses one of the bathroom rooms uniformly at random. A room may contain several wash basins, so students entering that room are split into several queues."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 28
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 28 (Codeforces format)"
rating: 2200
weight: 28
solve_time_s: 104
verified: true
draft: false
---
[CF 28C - Bath Queue](https://codeforces.com/problemset/problem/28/C)

**Rating:** 2200  
**Tags:** combinatorics, dp, probabilities  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

Every student independently chooses one of the bathroom rooms uniformly at random. A room may contain several wash basins, so students entering that room are split into several queues. The queues are balanced as evenly as possible, because the students arrange themselves to minimize the largest queue length in that room.

If a room contains `x` students and `a[i]` basins, then the largest queue size inside that room becomes:

$$\left\lceil \frac{x}{a[i]} \right\rceil$$

The global value for one random assignment is the maximum queue size among all rooms. We must compute the expected value of this maximum.

The constraints are small enough to allow dynamic programming, but too large for brute force enumeration. There are at most 50 students and 50 rooms. The number of possible assignments is:

$$m^n$$

With `n = m = 50`, this becomes `50^50`, which is completely impossible to enumerate directly.

The small bounds hint that a state-based probability DP is intended. Any algorithm around `O(n^3 m)` or `O(n^4)` is fine inside a 2 second limit. Something exponential in `n` or `m` is not.

The most dangerous part of the problem is understanding what exactly determines the largest queue size in a room. A careless implementation may incorrectly use floor division.

Consider:

```
2 1
3
```

There are 2 students and 3 basins. The largest queue size is not `0`, even though `2 // 3 = 0`. Each student simply occupies a separate basin, so the answer is `1`.

Another subtle case appears when students distribute unevenly.

```
5 1
2
```

With 5 students and 2 basins, the optimal split is queues of sizes `3` and `2`. The largest queue is `3`, not `2`.

A more probabilistic edge case is when many rooms have large basin counts.

```
2 2
100 100
```

No matter how students choose rooms, every occupied room has largest queue size `1`. The expected value is exactly `1`. A naive simulation or incorrect transition may accidentally count empty queues and produce something smaller.

The hardest conceptual mistake is assuming rooms are independent after fixing the maximum. They are not independent because the student counts across rooms must sum to `n`. The DP must track how many students have already been assigned.

## Approaches

The brute force approach is straightforward. For every student, choose one of the `m` rooms. After constructing a complete assignment, count how many students entered each room. For room `i`, compute:

$$\left\lceil \frac{cnt_i}{a_i} \right\rceil$$

Then take the maximum across rooms and average over all assignments.

This works because every assignment is equally likely. The problem is the number of assignments:

$$m^n$$

For the maximum constraints this is astronomically large.

The key observation is that we do not care about the exact identities of students. Only the number of students entering each room matters.

Suppose room `i` receives `k` students. The probability of this event is binomial:

$$\binom{n}{k}\left(\frac1m\right)^k$$

More importantly, the largest queue size produced by that room depends only on `k` and `a[i]`.

This suggests reframing the problem. Instead of directly computing the expected maximum, compute:

$$P(\text{maximum queue size} \le t)$$

for every threshold `t`.

For a fixed threshold `t`, room `i` can accept at most:

$$a_i \cdot t$$

students, otherwise its largest queue exceeds `t`.

Now the problem becomes counting the probability that every room stays within its allowed capacity.

This transforms the problem into a classic multinomial DP. We process rooms one by one and track how many students have already been distributed.

For each room, we try assigning `k` students to it, provided:

$$\left\lceil \frac{k}{a_i} \right\rceil \le t$$

Equivalently:

$$k \le a_i t$$

The probability contribution for assigning exactly `k` students to this room comes from combinatorics. We choose which remaining students go into this room.

Once we can compute:

$$P(\max \le t)$$

the expected value follows from:

$$E[\max] = \sum_{t \ge 1} P(\max \ge t)$$

or equivalently:

$$E[\max] = \sum_{t=1}^{n} \left(1 - P(\max \le t-1)\right)$$

The second formulation is convenient because the maximum queue size is always between `1` and `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m^n \cdot (n+m)) | O(m) | Too slow |
| Optimal | O(m \cdot n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Precompute binomial coefficients `C[n][k]` for all `0 ≤ n,k ≤ 50`.

These coefficients represent how many ways we can choose which students enter a particular room.
2. Precompute powers of `m`.

Since every assignment has probability:

$$\frac1{m^n}$$

we repeatedly divide by powers of `m`.
3. For every threshold `t` from `0` to `n`, compute:

$$P_t = P(\max \le t)$$

This means every room must have largest queue size at most `t`.
4. Use dynamic programming over rooms.

Define:

$$dp[i][j]$$

as the number of valid ways to distribute exactly `j` students among the first `i` rooms while respecting the threshold `t`.
5. Initialize:

$$dp[0][0] = 1$$

Before processing any room, zero students have been assigned in one valid way.
6. Process rooms one by one.

Suppose we are at room `i` and already assigned `j` students. Try placing `k` additional students into this room.

This transition is allowed only if:

$$\left\lceil \frac{k}{a_i} \right\rceil \le t$$

which is equivalent to:

$$k \le a_i t$$
7. Add the transition:

$$dp[i+1][j+k] += dp[i][j] \cdot \binom{n-j}{k}$$

We choose which `k` of the remaining students go into this room.
8. After all rooms are processed, `dp[m][n]` equals the number of assignments where the maximum queue size is at most `t`.
9. Divide by:

$$m^n$$

to obtain the probability:

$$P_t$$
10. Recover the expectation using:

$$E = \sum_{x=1}^{n} \left(1 - P_{x-1}\right)$$

The term `1 - P_{x-1}` is exactly the probability that the maximum queue size is at least `x`.

### Why it works

For a fixed threshold `t`, the DP counts exactly the assignments where every room respects the limit. The transition chooses how many students enter the current room and counts all possible subsets of remaining students that could do so.

Every full assignment corresponds to exactly one path through the DP, because each room receives a uniquely determined student count. Conversely, every DP path constructs a valid assignment.

The expectation formula works because for any nonnegative integer random variable:

$$E[X] = \sum_{x \ge 1} P(X \ge x)$$

Here `X` is the maximum queue size.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXN = 55

# binomial coefficients
C = [[0] * MAXN for _ in range(MAXN)]

for n in range(MAXN):
    C[n][0] = C[n][n] = 1
    for k in range(1, n):
        C[n][k] = C[n - 1][k - 1] + C[n - 1][k]

n, m = map(int, input().split())
a = list(map(int, input().split()))

total = float(m ** n)

# prob[t] = P(max <= t)
prob = [0.0] * (n + 1)

for t in range(n + 1):
    dp = [[0.0] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = 1.0

    for i in range(m):
        limit = a[i] * t

        for used in range(n + 1):
            if dp[i][used] == 0:
                continue

            for take in range(n - used + 1):
                if take > limit:
                    break

                ways = C[n - used][take]
                dp[i + 1][used + take] += dp[i][used] * ways

    prob[t] = dp[m][n] / total

ans = 0.0

for x in range(1, n + 1):
    ans += 1.0 - prob[x - 1]

print(f"{ans:.15f}")
```

The first section precomputes binomial coefficients with Pascal's triangle. We only need values up to 50, so this costs almost nothing.

The DP is rebuilt independently for every threshold `t`. The state `dp[i][used]` stores how many valid assignments exist after processing the first `i` rooms and assigning `used` students.

The transition is the core combinatorial step. Suppose `used` students are already assigned. There are `n - used` students still free. Choosing exactly `take` of them for the current room can be done in:

$$\binom{n-used}{take}$$

ways.

The condition `take <= a[i] * t` guarantees that the largest queue inside the room does not exceed `t`.

A common mistake is trying to use multinomial coefficients directly. The incremental binomial construction is simpler and avoids overcounting because each student is assigned exactly once while processing rooms sequentially.

Another subtle point is the meaning of `t = 0`. This threshold is impossible unless there are no students. Since `n ≥ 1`, `prob[0]` becomes zero automatically. Keeping this case simplifies the expectation formula.

The final summation uses:

$$E[X] = \sum_{x \ge 1} P(X \ge x)$$

implemented as:

```
ans += 1 - prob[x - 1]
```

## Worked Examples

### Example 1

Input:

```
1 1
2
```

There is one student and one room with two basins.

For threshold `t = 0`:

| Room processed | Students assigned | Valid ways |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 1 | 0 |

The room cannot accept even one student because `2 * 0 = 0`.

So:

$$P(\max \le 0) = 0$$

For threshold `t = 1`:

| Room processed | Students assigned | Valid ways |
| --- | --- | --- |
| 0 | 0 | 1 |
| 1 | 1 | 1 |

Now the room may accept up to `2` students, so the assignment is valid.

$$P(\max \le 1) = 1$$

Expectation:

$$1 - P(\max \le 0) = 1$$

Output:

```
1.000000000000000
```

This confirms that even with more basins than students, the largest queue size is still at least `1`.

### Example 2

Input:

```
2 2
1 1
```

Each room has one basin, so queue size equals number of students in the room.

For threshold `t = 1`, each room may contain at most one student.

| Room | Used students before | Students added | Resulting state |
| --- | --- | --- | --- |
| 1 | 0 | 0 | dp[1][0] += 1 |
| 1 | 0 | 1 | dp[1][1] += 2 |
| 2 | 0 | 0 | dp[2][0] += 1 |
| 2 | 1 | 1 | dp[2][2] += 2 |

There are `2^2 = 4` total assignments.

Exactly two assignments split students evenly across rooms.

So:

$$P(\max \le 1) = \frac{2}{4} = \frac12$$

The maximum queue size is either `1` or `2`.

Hence:

$$E = 1 \cdot \frac12 + 2 \cdot \frac12 = 1.5$$

Output:

```
1.500000000000000
```

This example demonstrates why counting probabilities directly is harder than counting threshold-valid assignments.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m \cdot n^3) | For every threshold, we iterate over rooms, used students, and added students |
| Space | O(m \cdot n) | DP table over rooms and assigned students |

With `n,m ≤ 50`, the total number of operations is comfortably below the limit. The memory usage is tiny, only a few thousand floating point values.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    MAXN = 55

    C = [[0] * MAXN for _ in range(MAXN)]

    for n in range(MAXN):
        C[n][0] = C[n][n] = 1
        for k in range(1, n):
            C[n][k] = C[n - 1][k - 1] + C[n - 1][k]

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    total = float(m ** n)

    prob = [0.0] * (n + 1)

    for t in range(n + 1):
        dp = [[0.0] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = 1.0

        for i in range(m):
            limit = a[i] * t

            for used in range(n + 1):
                for take in range(n - used + 1):
                    if take > limit:
                        break

                    dp[i + 1][used + take] += (
                        dp[i][used] *
                        C[n - used][take]
                    )

        prob[t] = dp[m][n] / total

    ans = 0.0

    for x in range(1, n + 1):
        ans += 1.0 - prob[x - 1]

    print(f"{ans:.15f}")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("1 1\n2\n") == "1.000000000000000"

# single basin, everyone forced together
assert run("5 1\n1\n") == "5.000000000000000"

# many basins, queues always size 1
assert run("2 2\n100 100\n") == "1.000000000000000"

# symmetric split case
res = float(run("2 2\n1 1\n"))
assert abs(res - 1.5) < 1e-9

# off-by-one ceiling division check
res = float(run("5 1\n2\n"))
assert abs(res - 3.0) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 2` | `1.0` | Minimum nontrivial case |
| `5 1 / 1` | `5.0` | Single room, single basin |
| `2 2 / 100 100` | `1.0` | Large basin counts |
| `2 2 / 1 1` | `1.5` | Probabilistic branching |
| `5 1 / 2` | `3.0` | Correct ceiling division |

## Edge Cases

Consider:

```
2 1
3
```

The room has more basins than students. For threshold `t = 0`, the room may accept at most `0` students, so the DP cannot place both students. Thus:

$$P(\max \le 0)=0$$

For threshold `t = 1`, the room may accept up to `3` students, so all assignments become valid:

$$P(\max \le 1)=1$$

The expectation becomes exactly `1`. The algorithm handles this correctly because it uses the condition:

$$k \le a_i t$$

which corresponds to ceiling division, not floor division.

Now consider:

```
5 1
2
```

There is only one room with two basins. Every assignment sends all five students there.

For threshold `t = 2`, the room may accept at most `4` students because:

$$2 \cdot 2 = 4$$

The DP rejects the assignment.

For threshold `t = 3`, the room may accept up to `6` students, so the assignment becomes valid.

Hence the maximum queue size is exactly `3`. The DP captures this transition point precisely.

Finally, consider:

```
2 2
100 100
```

Every room can hold arbitrarily many students while keeping queue size `1`.

For threshold `t = 1`, each room limit becomes `100`, so every possible assignment is valid. The DP counts all `2^2 = 4` assignments and computes:

$$P(\max \le 1)=1$$

Thus the expectation is exactly `1`. Empty rooms cause no issues because assigning zero students is always allowed.
