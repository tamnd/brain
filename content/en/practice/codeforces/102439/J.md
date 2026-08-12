---
title: "CF 102439J - Boedium"
description: "Josya is the first participant in the input. Every athlete runs five identical laps and shoots at twenty targets in total. Ten targets are shot from the prone position and ten from the standing position. A hit costs no extra time, while every miss adds exactly 60 seconds."
date: "2026-08-12T08:14:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "J"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 150
verified: true
draft: false
---

[CF 102439J - Boedium](https://codeforces.com/problemset/problem/102439/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

Josya is the first participant in the input. Every athlete runs five identical laps and shoots at twenty targets in total. Ten targets are shot from the prone position and ten from the standing position. A hit costs no extra time, while every miss adds exactly 60 seconds.

For athlete (i), let (K_i) be the total number of missed targets. Then the race time, apart from the common shooting time that cancels in every comparison, is

[
5\cdot time_i + 60K_i.
]

The ten prone shots give a binomial random variable with 10 trials and miss probability (1-down_i). The ten standing shots give another binomial random variable with 10 trials and miss probability (1-up_i). Thus (K_i) can take only the 21 values from 0 through 20.

Josya is on the podium exactly when at most two other athletes finish strictly faster than her. Equality does not count as being faster, which is the main source of boundary cases in the comparison.

The input contains up to 50,000 athletes, and the lap time is at most 600 seconds. Since the number of possible miss counts is only 21, the large dimension is the number of athletes, not the range of possible race times. An (O(n^2)) method would already require about (2.5\cdot10^9) pairwise operations at the maximum size, which is far beyond a two-second limit. We need a method whose work per athlete is constant.

There are several edge cases where an apparently reasonable implementation can be wrong. First, ties must not count as faster athletes. For example,

```
4
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
```

has answer `1.000000000000`. Every athlete finishes at exactly the same time, so Josya has zero faster opponents. A comparison using `<=` instead of `<` would incorrectly count the three tied athletes.

The one-minute penalty also creates exact boundaries. Consider

```
4
10 0.500 0.500
22 1.000 1.000
22 1.000 1.000
22 1.000 1.000
```

Josya's base time is (50) seconds. With exactly one miss she finishes in (110) seconds, exactly the same time as every opponent. She is still on the podium in that case. With two or more misses, all three opponents are strictly faster. Since Josya has twenty independent shots with miss probability (1/2), the answer is

\frac{21}{1048576}.
]

A formula that accidentally treats equality as faster would lose the entire (K=1) contribution.

The smallest participant count is also special. With one, two, or three athletes, Josya can never have three athletes strictly ahead of her, so the answer is always 1. For example,

```
1
100 0.000 0.000
```

has answer `1.000000000000`, regardless of Josya's shooting distribution.

Finally, probabilities of exactly zero or one must work without division by a probability such as (1-p). An implementation based on a binomial recurrence containing `p / (1-p)` can divide by zero when an athlete has hit probability 1. Computing the binomial terms directly avoids this problem.

## Approaches

A direct brute-force solution would first compute the probability of every possible miss count for every athlete, then enumerate every combination of their miss counts. Each athlete has 21 possible totals, so for (n) athletes there are (21^n) possible race outcomes. Even ignoring the fact that each outcome also needs to be weighted by its probability, for (n=50000) this is hopelessly large.

The brute force works because a complete assignment of miss counts completely determines all race times. It fails because we do not actually need to know the exact outcome of every athlete. For a fixed Josya result, each competitor can be reduced to one Bernoulli event: did this competitor finish strictly faster than Josya?

That observation changes the problem completely. Fix Josya's number of misses to (k). For every other athlete (i), we can calculate

[
q_i(k)=P(\text{athlete }i\text{ finishes strictly faster than Josya}\mid K_J=k).
]

Once (k) is fixed, the events for different competitors are independent. We only care whether the number of successful Bernoulli events is 0, 1, or 2, because any value of 3 or more means that Josya misses the podium.

We can maintain a three-state dynamic programming array. Initially the probability of having zero faster athletes is 1. After processing a competitor with faster-than-Josya probability (q), the states are updated by either keeping the current count or increasing it by one. We discard states above two because they can never contribute to the answer.

The remaining question is how to calculate (q_i(k)) efficiently. Let Josya have lap time (T) and (k) misses, while competitor (i) has lap time (t_i) and (j) misses. The competitor is strictly faster when

[
5t_i+60j < 5T+60k.
]

Dividing by 5 gives

[
t_i+12j < T+12k.
]

For fixed (k), the largest allowed integer (j) is

[
m=\left\lfloor\frac{T+12k-t_i-1}{12}\right\rfloor.
]

Thus (q_i(k)) is simply the probability that athlete (i) has at most (m) misses. Since (m) is always between 0 and 20 when it is relevant, we can precompute the cumulative distribution function of every athlete's miss count.

There are only 21 possible values of (k). For each one, we process all (n-1) competitors and maintain three DP states. This gives an (O(21n)) final calculation. Computing the 21-value miss distribution for each athlete takes a constant amount of work as well, because it is the convolution of two binomial distributions of size 11.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(21^n)) | (O(n)) | Too slow |
| Optimal | (O(21n)) | (O(21n)) | Accepted |

## Algorithm Walkthrough

1. Read Josya's lap time and shooting probabilities, then read the remaining athletes. The first input line after (n) describes Josya, so she must be kept separate from the competitors.
2. For every athlete, build the probability distribution of their total number of misses. The prone part is a binomial distribution with 10 trials and miss probability (1-down_i), while the standing part has 10 trials and miss probability (1-up_i). Convolving these two distributions gives probabilities for 0 through 20 total misses.
3. Convert every competitor's miss distribution into a cumulative distribution. Store (F_i[x]=P(K_i\le x)) for every (x) from 0 through 20. The cumulative form is what lets us answer a faster-than-Josya query in constant time.
4. Compute Josya's own distribution (P_J[k]=P(K_J=k)) for all (k) from 0 through 20. We will condition on each possible value of (k) separately.
5. Fix a particular Josya miss count (k). Her effective race time, after removing the common shooting time, is (5T+60k). For competitor (i), calculate

[
m_i=\left\lfloor\frac{T+12k-t_i-1}{12}\right\rfloor.
]

The subtraction by one is what converts the strict inequality into an integer upper bound. Without it, an exact tie would incorrectly be counted as a faster finish.

1. If (m_i<0), competitor (i) cannot possibly be faster, so set (q_i=0). If (m_i\ge20), every possible miss count makes that competitor faster, so set (q_i=1). Otherwise use (q_i=F_i[m_i]).
2. Process the competitors one by one with a DP array `dp`. Its three entries represent the probability that exactly 0, 1, or 2 processed competitors are strictly faster than Josya. For a competitor with faster probability (q), the transition is

[
new_0=dp_0(1-q),
]

[
new_1=dp_1(1-q)+dp_0q,
]

[
new_2=dp_2(1-q)+dp_1q.
]

States with three or more faster competitors are omitted because they can never put Josya on the podium.

1. After all competitors have been processed, `dp[0] + dp[1] + dp[2]` is the conditional probability that Josya is on the podium given (K_J=k). Multiply this by (P_J[k]) and add it to the global answer.
2. Repeat the DP for all 21 possible Josya miss counts and print the resulting probability.

### Why it works

Fixing Josya's miss count (k) completely fixes her race time. For every competitor, the event of being faster is then a Bernoulli event whose probability is exactly the competitor's miss-count CDF at the derived threshold. Different athletes shoot independently, so these Bernoulli events are independent.

The DP invariant is that after processing some competitors, `dp[x]` is the probability that exactly (x) of those processed competitors are strictly faster than Josya, for (x\in{0,1,2}). Each new competitor either stays outside the faster set or joins it, giving exactly the stated transitions. Since only counts up to two can lead to a podium, discarding larger counts loses no valid outcome.

Finally, the 21 possible values of Josya's miss count are disjoint and exhaustive. Weighting each conditional podium probability by Josya's corresponding miss-count probability gives exactly the required total probability.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

C10 = [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]

def distribution(down, up):
    # Number of misses in the 10 prone shots.
    miss_down = 1.0 - down
    prone = [
        C10[k] * (miss_down ** k) * (down ** (10 - k))
        for k in range(11)
    ]

    # Number of misses in the 10 standing shots.
    miss_up = 1.0 - up
    standing = [
        C10[k] * (miss_up ** k) * (up ** (10 - k))
        for k in range(11)
    ]

    # Convolution: total misses range from 0 to 20.
    dist = [0.0] * 21
    for i in range(11):
        pi = prone[i]
        for j in range(11):
            dist[i + j] += pi * standing[j]

    return dist

def solve():
    n = int(input())

    t0, down0, up0 = input().split()
    t0 = int(t0)
    down0 = float(down0)
    up0 = float(up0)

    # Store competitors' lap times separately. Their CDFs are
    # stored transposed: cdfs[m][i] is competitor i's P(K <= m).
    times = []
    cdfs = [array('d') for _ in range(21)]

    for _ in range(n - 1):
        t, down, up = input().split()
        t = int(t)
        down = float(down)
        up = float(up)

        times.append(t)

        dist = distribution(down, up)
        cur = 0.0
        for k in range(21):
            cur += dist[k]
            cdfs[k].append(cur)

    josya = distribution(down0, up0)

    ans = 0.0
    competitors = n - 1

    for k in range(21):
        pj = josya[k]
        if pj == 0.0:
            continue

        dp0, dp1, dp2 = 1.0, 0.0, 0.0

        for i in range(competitors):
            # Competitor is faster iff
            # 5 * times[i] + 60 * misses
            # < 5 * t0 + 60 * k.
            #
            # Equivalent to
            # 12 * misses < t0 + 12*k - times[i].
            #
            # Maximum integer misses is floor((D - 1) / 12).
            D = t0 + 12 * k - times[i]
            m = (D - 1) // 12

            if m < 0:
                q = 0.0
            elif m >= 20:
                q = 1.0
            else:
                q = cdfs[m][i]

            nq = 1.0 - q

            ndp2 = dp2 * nq + dp1 * q
            ndp1 = dp1 * nq + dp0 * q
            ndp0 = dp0 * nq

            dp0, dp1, dp2 = ndp0, ndp1, ndp2

        ans += pj * (dp0 + dp1 + dp2)

    print(f"{ans:.12f}")

if __name__ == "__main__":
    solve()
```

The `distribution` function first creates the two binomial distributions. The exponent is the number of misses, while the remaining exponent is the number of hits. Writing the formula directly avoids a division by zero when the hit probability is exactly 0 or 1.

The convolution combines the ten prone and ten standing shots. There are only 11 terms in each distribution, so the 121 multiplications per athlete are constant work.

The cumulative distributions are stored in `array('d')` objects rather than nested Python lists of floats. There are at most (21\cdot49999) stored values, and a double occupies eight bytes, so this takes about 8.4 MB for the numerical data. This keeps the memory usage comfortably below the 256 MB limit.

The comparison uses `D = t0 + 12 * k - times[i]`. The expression `(D - 1) // 12` is deliberate. For example, if `D` is exactly 12, the condition is `12 * misses < 12`, so only zero misses are allowed. The formula gives `(12 - 1) // 12 = 0`. Using `D // 12` would incorrectly allow one miss and would turn a tie into a win for the competitor.

The DP keeps only three states because the desired event is having at most two faster athletes. A fourth state would never contribute to the answer, so storing it would only add unnecessary work.

No integer overflow is possible in Python, and all probability calculations use double-precision floating point. The required error is (10^{-9}), while the computation only involves small probability distributions and about one million DP transitions, so the resulting floating-point error is safely within the required tolerance.

## Worked Examples

The official sample is

```
4
45 0.700 0.700
60 0.800 0.800
90 0.900 0.900
120 1.000 1.000
```

and its output is

```
0.675394632273
```

For a competitor with lap time 60 and Josya with lap time 45, the faster condition becomes

[
60+12j < 45+12k.
]

The largest allowed competitor miss count is (k-2). For the athletes with lap times 90 and 120, the corresponding thresholds are (k-4) and (k-6). Negative thresholds give probability zero. The algorithm evaluates these CDFs for every possible Josya miss count and then runs the three-state DP.

A more transparent trace is obtained from an all-deterministic race:

```
4
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
```

Every athlete has zero misses with probability 1, so Josya has zero misses as well.

| Processed competitor | Faster probability (q) | `dp[0]` | `dp[1]` | `dp[2]` |
| --- | --- | --- | --- | --- |
| Start | 0 | 1 | 0 | 0 |
| 1 | 0 | 1 | 0 | 0 |
| 2 | 0 | 1 | 0 | 0 |
| 3 | 0 | 1 | 0 | 0 |

For Josya's only possible miss count (k=0), a competitor with the same lap time must have fewer than zero misses to be faster. Its threshold is (-1), so its faster probability is zero. The invariant is preserved after every competitor, and the conditional podium probability is 1.

For the boundary example

```
4
10 0.500 0.500
22 1.000 1.000
22 1.000 1.000
22 1.000 1.000
```

Josya's total number of misses follows a binomial distribution with 20 trials and probability (1/2).

| Josya misses (k) | (P(K_J=k)) | Competitor threshold (m) | Faster probability (q) | Conditional podium probability |
| --- | --- | --- | --- | --- |
| 0 | (1/2^{20}) | (-6) | 0 | 1 |
| 1 | (20/2^{20}) | (-1) | 0 | 1 |
| 2 | (190/2^{20}) | 4 | 1 | 0 |
| 3 through 20 | Remaining probability | At least 5 | 1 | 0 |

For (k=1), Josya's time is (50+60=110) seconds, exactly equal to each competitor's clean time (5\cdot22=110). The threshold is (-1), so no competitor is counted as faster. For (k=2), Josya needs 120 seconds, while all three competitors finish in 110 seconds, so the DP ends with three faster athletes and contributes zero.

The final answer is

\frac{21}{1048576}
\approx 0.0000200271606445.
]

This trace demonstrates why the strict inequality in the threshold calculation is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(21\cdot121\cdot n + 21n)) = (O(n)) | Each athlete's two 11-element binomial distributions are convolved, then every one of 21 Josya outcomes processes every competitor with three DP states. |
| Space | (O(21n)) | We store 21 cumulative probabilities for every competitor, plus the lap times. |

The constant factors are small because the maximum miss count is fixed at 20. With 50,000 athletes, the main DP performs only about one million competitor transitions, while the distribution construction performs about six million simple arithmetic operations. The compact `array('d')` storage also keeps the memory usage well below 256 MB.

## Test Cases

```python
import sys
import io
from array import array

C10 = [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]

def distribution(down, up):
    miss_down = 1.0 - down
    prone = [
        C10[k] * (miss_down ** k) * (down ** (10 - k))
        for k in range(11)
    ]

    miss_up = 1.0 - up
    standing = [
        C10[k] * (miss_up ** k) * (up ** (10 - k))
        for k in range(11)
    ]

    dist = [0.0] * 21
    for i in range(11):
        for j in range(11):
            dist[i + j] += prone[i] * standing[j]

    return dist

def solve():
    input = sys.stdin.readline
    n = int(input())

    t0, down0, up0 = input().split()
    t0 = int(t0)
    down0 = float(down0)
    up0 = float(up0)

    times = []
    cdfs = [array('d') for _ in range(21)]

    for _ in range(n - 1):
        t, down, up = input().split()
        t = int(t)
        down = float(down)
        up = float(up)

        times.append(t)

        dist = distribution(down, up)
        cur = 0.0
        for k in range(21):
            cur += dist[k]
            cdfs[k].append(cur)

    josya = distribution(down0, up0)

    ans = 0.0

    for k in range(21):
        pj = josya[k]
        if pj == 0.0:
            continue

        dp0, dp1, dp2 = 1.0, 0.0, 0.0

        for i in range(n - 1):
            D = t0 + 12 * k - times[i]
            m = (D - 1) // 12

            if m < 0:
                q = 0.0
            elif m >= 20:
                q = 1.0
            else:
                q = cdfs[m][i]

            nq = 1.0 - q

            ndp2 = dp2 * nq + dp1 * q
            ndp1 = dp1 * nq + dp0 * q
            ndp0 = dp0 * nq

            dp0, dp1, dp2 = ndp0, ndp1, ndp2

        ans += pj * (dp0 + dp1 + dp2)

    print(f"{ans:.12f}")

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

sample = """\
4
45 0.700 0.700
60 0.800 0.800
90 0.900 0.900
120 1.000 1.000
"""

assert abs(float(run(sample)) - 0.675394632273) < 1e-10, "provided sample"

assert abs(float(run("""\
1
100 0.000 0.000
""")) - 1.0) < 1e-12, "minimum size"

assert abs(float(run("""\
4
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
""")) - 1.0) < 1e-12, "all equal values"

assert abs(float(run("""\
4
9 1.000 1.000
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
""")) - 0.0) < 1e-12, "three strictly faster"

assert abs(float(run("""\
4
10 0.500 0.500
22 1.000 1.000
22 1.000 1.000
22 1.000 1.000
""")) - 21.0 / 1048576.0) < 1e-12, "strict tie boundary"

assert abs(float(run("""\
4
10 0.900 0.900
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
""")) - 0.9 ** 20) < 1e-12, "stochastic Josya"

maximum_input = "50000\n" + "\n".join(
    "1 1.000 1.000" for _ in range(50000)
) + "\n"

assert abs(float(run(maximum_input)) - 1.0) < 1e-12, "maximum size"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 100 0.000 0.000` | `1` | Minimum participant count and the fact that Josya cannot have three faster opponents. |
| Four identical deterministic athletes | `1` | Ties are not counted as faster. |
| Josya at 10 seconds, three competitors at 9 seconds | `0` | Exactly three strictly faster competitors must eliminate Josya. |
| Josya at 10 seconds with probability 0.5, competitors at 22 seconds | (21/1048576) | Exact one-minute boundary and strict inequality. |
| Josya with hit probability 0.9, three clean equal-time competitors | (0.9^{20}) | Correct construction of the 20-shot miss distribution. |
| 50,000 identical deterministic athletes | `1` | Maximum input size and linear-time behavior. |

## Edge Cases

The equal-time case is handled by the `D - 1` in the threshold formula. For

```
4
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
10 1.000 1.000
```

Josya has (k=0), and for every competitor (D=0). The formula gives (m=(-1)//12=-1), so every faster probability is zero. The DP remains `(1, 0, 0)` and the answer is exactly 1.

The exact one-minute boundary is handled similarly. For

```
4
10 0.500 0.500
22 1.000 1.000
22 1.000 1.000
22 1.000 1.000
```

when Josya has one miss, (D=0), giving (m=-1). The competitors are tied at 110 seconds, so their faster probability is correctly zero. When Josya has two misses, (D=60), giving (m=4), and every clean competitor is strictly faster. The algorithm consequently keeps exactly the (k=0) and (k=1) cases, producing (21/1048576).

For a single participant,

```
1
100 0.000 0.000
```

there are no competitor transitions at all. The DP starts at `(1, 0, 0)` for every possible Josya miss count, and the sum of the Josya distribution is 1. The answer is consequently 1 without requiring any special case in the main algorithm.

For deterministic shooting probabilities equal to 0 or 1, the direct binomial formula remains valid. If the hit probability is 1, every positive miss count receives probability zero. If the hit probability is 0, only the maximum miss count receives probability one. Since the implementation never divides by the hit or miss probability, both endpoints are handled without numerical exceptions.
