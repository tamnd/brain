---
title: "CF 102185G - \u0413\u0438\u0440\u043b\u044f\u043d\u0434\u0430"
description: "The garland is controlled by two parameters. After being switched on at an integer time (S), it stays lit for (A) minutes, then stays dark for (A) minutes, and repeats this cycle forever. Before time (S), it is dark because the garland has not been switched on yet."
date: "2026-08-20T00:39:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102185
codeforces_index: "G"
codeforces_contest_name: "Southern Russia Open Championship \u2013 ContestSFedU 2019, Team Final."
rating: 0
weight: 102185
solve_time_s: 306
verified: true
draft: false
---

[CF 102185G - \u0413\u0438\u0440\u043b\u044f\u043d\u0434\u0430](https://codeforces.com/problemset/problem/102185/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The garland is controlled by two parameters. After being switched on at an integer time (S), it stays lit for (A) minutes, then stays dark for (A) minutes, and repeats this cycle forever. Before time (S), it is dark because the garland has not been switched on yet.

The holiday occupies the interval ([0,T]). During this interval at least half of the time must be lit. At the same time, the grandfather is at home during several disjoint intervals ([L_i,R_i]), and we want to minimize the total length of their intersection with the lit portions of the garland.

The answer consists of the minimum unavoidable overlap, the chosen (A), and the switching time (S). Among equal overlaps we prefer the smaller (A), and among equal (A) we prefer the later switching time.

All endpoints are integers, so we can regard each minute ([t,t+1)) as one discrete position. A grandfather interval ([L,R]) then occupies exactly the positions (L,L+1,\ldots,R-1).

The bound (T\le 5000) is the main clue. An (O(T^2)) solution is realistic, while an approach that scans all (T) minutes for every pair ((A,S)) is far too expensive. The number of grandfather intervals is at most (T/2), so an (O(NT)) component is also acceptable as part of an (O(T^2)) solution.

There are several boundary cases that can easily break a seemingly correct implementation. The first is that the garland does not run periodically before it is switched on. For example,

```
4 0
```

has answer

```
0 1 1
```

because with (A=1) and (S=1), the garland is lit during ([1,2)) and ([3,4)), exactly half the holiday. Treating the pattern as periodic before (S) would incorrectly consider (S=1) equivalent to (S=-1).

A second edge case is a switching time before the holidays. For

```
8 2
1 3
5 7
```

the answer is

```
0 2 -1
```

With (A=2) and (S=-1), the garland is lit during ([0,1)), ([3,5)), and ([7,8)), giving exactly four lit minutes while avoiding both grandfather intervals. A solution that only considers (S\ge0) misses the optimum.

A third edge case occurs when the switching time is exactly at the beginning of a grandfather interval. For

```
4 1
1 2
```

the answer is

```
0 2 2
```

The garland is lit on ([2,4)), giving two lit minutes and zero overlap. The common mistake here is to treat the endpoint (2) as belonging to the interval ([1,2]). These are time intervals, so their intersection has length zero.

Finally, (A) does not need to be considered beyond (T). If (A>T), at most one lit segment can intersect the holidays. Such a segment is either a prefix, a suffix, or the whole holiday, and the same lit segment can be reproduced with (A=T). Since smaller (A) wins ties, considering (A\le T) is sufficient.

## Approaches

The direct brute force is conceptually simple. We can try every (A) from (1) through (T), every relevant integer switching time (S), simulate the garland minute by minute, count its lit duration, and separately count how many lit minutes belong to grandfather intervals. Every candidate is checked exactly, so the method is correct.

For a fixed (A), negative switching times only need representatives from ([-2A,-1]), because shifting (S) by (2A) does not change the periodic pattern after the garland has already been switched on. For nonnegative (S), a feasible solution cannot have (S>\lfloor T/2\rfloor), because at most (T-S) minutes remain. This gives (O(2A+T)) candidate starts for one (A). If every candidate scans all (T) minutes, the worst case is about

[
T\left(\sum_{A=1}^{T} (2A+T/2)\right)
]

operations, which is about (1.9\cdot10^{11}) operations at (T=5000). That is nowhere near the one-second limit.

The key observation is that for a fixed (A), the infinite periodic pattern depends only on (S\bmod 2A). If we know, for every residue modulo (2A), how many holiday minutes and how many grandfather minutes have that residue, then moving (S) by one only removes one residue class from the lit half-cycle and adds another. A complete correlation value can thus be updated in (O(1)).

There is one complication. For (S\ge0), the periodic formula would incorrectly illuminate times before (S). We handle this by maintaining the amount of lit weight that lies in the prefix ([0,S)). When (S) increases by one, the set of lit residue classes shifts by one, so that prefix contribution can also be updated in (O(1)) using residue sums accumulated for the already processed prefix.

There is an additional simplification for (2A>T). The period (2A) is then longer than the entire holiday, so the holiday can contain only one lit segment. The problem for that (A) becomes a simple interval intersection problem, which can be evaluated directly from a prefix sum of grandfather occupancy.

The resulting approach is (O(T^2)), with only (O(T)) memory.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(T^3)) | (O(T)) | Too slow |
| Optimal | (O(T^2)) | (O(T)) | Accepted |

## Algorithm Walkthrough

1. Build an array `g[t]` for (0\le t<T), where `g[t]=1` exactly when the grandfather is home during minute ([t,t+1)). Also build its prefix sum. This lets us find the grandfather overlap of any ordinary interval in (O(1)).
2. Consider every (A) from (1) through (T). Values above (T) are unnecessary because any feasible pattern produced by such an (A) can be reproduced with (A=T).
3. If (2A>T), the period is longer than the holiday. The lit part inside ([0,T]) is a single interval. For every feasible switching time (S), intersect ([S,S+A)) with ([0,T]), compute its length, and compute its grandfather overlap with the prefix sum. For negative (S), the left endpoint is clipped to zero because the garland has already been switched on before the holidays.
4. For (2A\le T), let (P=2A). Build `cnt[r]`, the number of holiday minutes whose time is congruent to (r\pmod P), and `home[r]`, the number of grandfather minutes with the same residue. The lit part of the periodic pattern beginning at residue (S\bmod P) consists of exactly (A) consecutive residues.
5. Construct the periodic lit duration and periodic grandfather overlap for (S=0). These are the sums over residues (0,\ldots,A-1). When (S) changes from (S) to (S+1), residue (S\bmod P) leaves the lit half and residue ((S+A)\bmod P) enters it. Both totals therefore change with just two array accesses.
6. Enumerate the negative switching times using the representatives (S=-P+1,\ldots,-1). A negative start means the garland has already begun, so the periodic calculation is the actual behavior on the holidays. The representative (-P) has the same holiday pattern as (0) but is earlier, so it can be skipped.
7. Process nonnegative switching times (S=0,\ldots,\lfloor T/2\rfloor). The periodic totals still describe a hypothetical pattern extending before (S), so subtract the part of that pattern lying in ([0,S)). Maintain this prefix contribution incrementally. When moving from (S) to (S+1), the old prefix loses the residue (S\bmod P), gains the residue ((S+A)\bmod P), and the newly added minute (S) is not lit in the new pattern because its relative time is zero.
8. For every candidate, require `2 * lit >= T`. If it is feasible, compare its grandfather overlap with the current answer. The comparison first minimizes overlap, then (A), then maximizes (S).
9. Print the best triple.

The invariant behind the periodic part is that `period_lit` and `period_home` always equal the sums obtained by applying the infinite periodic pattern with the current switching phase to the entire holiday interval. The prefix variables always equal the same sums restricted to minutes before the actual switching time. Their difference is exactly the behavior of the real garland, which is dark before it is switched on. Since every relevant phase is enumerated and every relevant nonnegative switching time is processed, the best feasible candidate is guaranteed to be found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve(data=None):
    if data is None:
        T, N = map(int, input().split())
        intervals = [tuple(map(int, input().split())) for _ in range(N)]
    else:
        it = iter(map(int, data.split()))
        T = next(it)
        N = next(it)
        intervals = [(next(it), next(it)) for _ in range(N)]

    # g[t] = 1 iff the grandfather is home during minute [t, t+1).
    diff_g = [0] * (T + 1)
    for l, r in intervals:
        diff_g[l] += 1
        diff_g[r] -= 1

    g = [0] * T
    cur = 0
    for t in range(T):
        cur += diff_g[t]
        g[t] = 1 if cur else 0

    # Prefix sum of grandfather occupancy.
    pref_g = [0] * (T + 1)
    for t in range(T):
        pref_g[t + 1] = pref_g[t] + g[t]

    half_floor = T // 2
    half_ceil = (T + 1) // 2

    best_cost = T + 1
    best_a = 0
    best_s = 0

    def consider(cost, a, s):
        nonlocal best_cost, best_a, best_s
        if cost < best_cost:
            best_cost = cost
            best_a = a
            best_s = s
        elif cost == best_cost and a == best_a and s > best_s:
            best_s = s

    for A in range(1, T + 1):
        # If the period is longer than the holiday, there can be
        # only one lit segment inside [0, T].
        if 2 * A > T:
            lo = half_ceil - A

            for s in range(lo, half_floor + 1):
                left = max(0, s)
                right = min(T, s + A)

                lit = right - left
                if 2 * lit < T:
                    continue

                cost = pref_g[right] - pref_g[left]
                consider(cost, A, s)

            continue

        P = 2 * A

        # home[r] = number of grandfather minutes t with t % P == r.
        #
        # Each grandfather interval contributes q to every residue,
        # plus one to a cyclic range of length rem.
        home_diff = [0] * (P + 1)
        base = 0

        for l, r in intervals:
            length = r - l
            q, rem = divmod(length, P)
            base += q

            if rem:
                start = l % P
                end = start + rem

                if end <= P:
                    home_diff[start] += 1
                    home_diff[end] -= 1
                else:
                    home_diff[start] += 1
                    home_diff[P] -= 1
                    home_diff[0] += 1
                    home_diff[end - P] -= 1

        home = [0] * P
        cur = 0
        for r in range(P):
            cur += home_diff[r]
            home[r] = cur + base

        # cnt[r] = number of holiday minutes with t % P == r.
        q, rem = divmod(T, P)
        cnt = [q + (1 if r < rem else 0) for r in range(P)]

        # Phase S = 0, whose lit residues are [0, A).
        period_lit = sum(cnt[:A])
        period_home = sum(home[:A])

        # Negative starts. For s < 0 the periodic pattern is real,
        # because the garland has already been switched on.
        cur_lit = period_lit
        cur_home = period_home

        for r in range(1, P):
            cur_lit += cnt[(r + A - 1) % P] - cnt[r - 1]
            cur_home += home[(r + A - 1) % P] - home[r - 1]

            s = -P + r

            if 2 * cur_lit >= T:
                consider(cur_home, A, s)

        # Nonnegative starts.
        cur_lit = period_lit
        cur_home = period_home

        # pref_cnt[r] and pref_home[r] contain the already processed
        # prefix [0, s), grouped by residue modulo P.
        pref_cnt = [0] * P
        pref_home = [0] * P

        # s = 0: nothing has to be removed from the periodic pattern.
        if 2 * cur_lit >= T:
            consider(cur_home, A, 0)

        for s in range(half_floor):
            r1 = s % P
            r2 = (s + A) % P

            # Shift the infinite periodic phase by one.
            cur_lit += cnt[r2] - cnt[r1]
            cur_home += home[r2] - home[r1]

            # Shift the part lying before the actual switch time.
            removed_lit = pref_cnt[r2] - pref_cnt[r1]
            removed_home = pref_home[r2] - pref_home[r1]

            pref_cnt[r1] += 1
            pref_home[r1] += g[s]

            actual_lit = cur_lit - removed_lit
            actual_home = cur_home - removed_home

            ns = s + 1

            if 2 * actual_lit >= T:
                consider(actual_home, A, ns)

    return f"{best_cost} {best_a} {best_s}"

if __name__ == "__main__":
    sys.stdout.write(solve() + "\n")
```

The first part constructs the minute-level grandfather occupancy and its prefix sum. Because all interval endpoints are integers, this representation is exact, not an approximation of continuous time.

The branch `2 * A > T` uses the fact that the period (2A) is longer than the entire holiday. There can be no second lit segment inside the holiday, so the garland is represented by a single interval. The candidate range starts at `half_ceil - A`, which is the earliest negative switch time whose lit intersection can reach half of the holiday.

For `2 * A <= T`, the code builds residue counts modulo `P = 2 * A`. The grandfather residue array is constructed with difference-array range updates. An interval of length `q * P + rem` contributes `q` to every residue and one additional unit to `rem` consecutive cyclic residues. This avoids scanning all (T) minutes for every value of (A).

The two variables `period_lit` and `period_home` describe the hypothetical infinite pattern. The negative-start loop can use them directly because the garland was already switched on before time zero.

The positive-start loop is more subtle. `pref_cnt` and `pref_home` describe the part of the periodic pattern that lies before the actual switch. The update occurs before inserting minute `s` into these arrays. That order matters because minute `s` is not before the new switching time `s+1`, but it is also not lit by the new phase at relative time zero.

The feasibility test uses `2 * lit >= T` instead of floating-point division. This handles odd values of (T) exactly. For example, if (T=5), at least three lit minutes are required.

The tie-breaking code relies on iterating (A) in increasing order. For equal cost, a larger (A) never replaces an already stored solution. For the same (A), a candidate replaces the current one only when its switching time is later.

## Worked Examples

### Sample 1

The input is

```
10 2
1 4
7 10
```

Consider (A=1). Its period is (2), so every other minute is lit in the periodic pattern.

| Start (S) | Periodic lit | Removed prefix lit | Actual lit | Grandfather overlap | Feasible |
| --- | --- | --- | --- | --- | --- |
| -1 | 5 | 0 | 5 | 4 | Yes |
| 0 | 5 | 0 | 5 | 2 | Yes |
| 1 | 5 | 0 | 5 | 4 | Yes |
| 2 | 5 | 1 | 4 | 2 | No |

The best candidate for (A=1) is (S=0), with overlap (2). Larger (A) cannot improve the answer, so the final result is

```
2 1 0
```

The important detail here is the difference between (S=-1) and (S=1). Their periodic phases are related, but the real garland is dark before its actual switching time. The prefix subtraction captures that distinction.

### Sample 2

The input is

```
8 2
1 3
5 7
```

For (A=2), the period is (4). The negative phase (S=-1) lights minutes (0,3,4,7), exactly four minutes.

| Start (S) | Periodic lit | Removed prefix lit | Actual lit | Grandfather overlap | Feasible |
| --- | --- | --- | --- | --- | --- |
| -1 | 4 | 0 | 4 | 0 | Yes |
| 0 | 4 | 0 | 4 | 2 | Yes |
| 1 | 4 | 0 | 4 | 4 | Yes |
| 2 | 4 | 1 | 3 | 2 | No |

The negative start avoids both grandfather intervals completely while still lighting exactly half of the holiday. Hence the answer is

```
0 2 -1
```

This example exercises the part of the algorithm that must preserve genuinely negative switching times rather than replacing them with nonnegative phase representatives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(T^2)) | For each (A), residue construction and all candidate updates take (O(N+T)), and (N\le T/2). |
| Space | (O(T)) | All residue arrays have length at most (2A\le T) in the periodic branch. |

The largest value of (T) is only (5000), so (O(T^2)) means roughly (25) million scale operations for the dominant parts of the algorithm. The solution never scans all (T) minutes for every individual switching time, which is the distinction between the accepted approach and the brute force.

## Test Cases

```python
import io
import sys

def solve(data=None):
    if data is None:
        T, N = map(int, input().split())
        intervals = [tuple(map(int, input().split())) for _ in range(N)]
    else:
        it = iter(map(int, data.split()))
        T = next(it)
        N = next(it)
        intervals = [(next(it), next(it)) for _ in range(N)]

    diff_g = [0] * (T + 1)
    for l, r in intervals:
        diff_g[l] += 1
        diff_g[r] -= 1

    g = [0] * T
    cur = 0
    for t in range(T):
        cur += diff_g[t]
        g[t] = 1 if cur else 0

    pref_g = [0] * (T + 1)
    for t in range(T):
        pref_g[t + 1] = pref_g[t] + g[t]

    half_floor = T // 2
    half_ceil = (T + 1) // 2

    best_cost = T + 1
    best_a = 0
    best_s = 0

    def consider(cost, a, s):
        nonlocal best_cost, best_a, best_s
        if cost < best_cost:
            best_cost = cost
            best_a = a
            best_s = s
        elif cost == best_cost and a == best_a and s > best_s:
            best_s = s

    for A in range(1, T + 1):
        if 2 * A > T:
            lo = half_ceil - A

            for s in range(lo, half_floor + 1):
                left = max(0, s)
                right = min(T, s + A)
                lit = right - left

                if 2 * lit < T:
                    continue

                cost = pref_g[right] - pref_g[left]
                consider(cost, A, s)

            continue

        P = 2 * A

        home_diff = [0] * (P + 1)
        base = 0

        for l, r in intervals:
            length = r - l
            q, rem = divmod(length, P)
            base += q

            if rem:
                start = l % P
                end = start + rem

                if end <= P:
                    home_diff[start] += 1
                    home_diff[end] -= 1
                else:
                    home_diff[start] += 1
                    home_diff[P] -= 1
                    home_diff[0] += 1
                    home_diff[end - P] -= 1

        home = [0] * P
        cur = 0
        for r in range(P):
            cur += home_diff[r]
            home[r] = cur + base

        q, rem = divmod(T, P)
        cnt = [q + (1 if r < rem else 0) for r in range(P)]

        period_lit = sum(cnt[:A])
        period_home = sum(home[:A])

        cur_lit = period_lit
        cur_home = period_home

        for r in range(1, P):
            cur_lit += cnt[(r + A - 1) % P] - cnt[r - 1]
            cur_home += home[(r + A - 1) % P] - home[r - 1]

            s = -P + r
            if 2 * cur_lit >= T:
                consider(cur_home, A, s)

        cur_lit = period_lit
        cur_home = period_home

        pref_cnt = [0] * P
        pref_home = [0] * P

        if 2 * cur_lit >= T:
            consider(cur_home, A, 0)

        for s in range(half_floor):
            r1 = s % P
            r2 = (s + A) % P

            cur_lit += cnt[r2] - cnt[r1]
            cur_home += home[r2] - home[r1]

            removed_lit = pref_cnt[r2] - pref_cnt[r1]
            removed_home = pref_home[r2] - pref_home[r1]

            pref_cnt[r1] += 1
            pref_home[r1] += g[s]

            actual_lit = cur_lit - removed_lit
            actual_home = cur_home - removed_home

            ns = s + 1

            if 2 * actual_lit >= T:
                consider(actual_home, A, ns)

    return f"{best_cost} {best_a} {best_s}"

def run(inp: str) -> str:
    return solve(inp)

assert run("""10 2
1 4
7 10
""") == "2 1 0", "sample 1"

assert run("""8 2
1 3
5 7
""") == "0 2 -1", "sample 2"

assert run("""6 1
0 4
""") == "1 3 3", "sample 3"

assert run("""5 1
0 5
""") == "3 1 0", "sample 4"

assert run("""4 0
""") == "0 1 1", "sample 5"

assert run("""1 0
""") == "0 1 0", "minimum-size input"

assert run("""4 1
1 2
""") == "0 2 2", "boundary endpoint"

assert run("""6 2
0 2
4 6
""") == "2 1 1", "equal intervals"

assert run("""5000 0
""") == "0 1 1", "maximum T"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `0 1 0` | Smallest possible holiday and switching-time boundary |
| `4 1 / 1 2` | `0 2 2` | Exact interval endpoints and a switch after the grandfather leaves |
| `6 2 / 0 2 / 4 6` | `2 1 1` | Equal-length grandfather intervals and tie-breaking by latest start |
| `5000 0` | `0 1 1` | Maximum holiday length and late-start tie-breaking |

## Edge Cases

For the minimum input

```
1 0
```

the only minute must be lit for at least half of the one-minute holiday, which means one full minute. With (A=1), switching at (S=0) lights ([0,1)), giving zero grandfather overlap. Switching at (S=1) would light nothing during the holiday, so the answer is

```
0 1 0
```

The algorithm reaches the (2A>T) branch immediately, tests (S=0), and rejects (S=1) because its lit duration is zero.

For the negative-start case

```
8 2
1 3
5 7
```

the relevant candidate is (A=2,S=-1). Since (2A=T), the periodic branch is used. The phase lights residues (0) and (3) modulo (4), giving four lit minutes at times (0,3,4,7). None belongs to the grandfather intervals, so the cost is zero. The negative-phase enumeration finds this candidate directly.

For the endpoint case

```
4 1
1 2
```

the candidate (A=2,S=2) produces the lit interval ([2,4)). Its intersection with the grandfather interval ([1,2)) is empty, while the holiday contains exactly two lit minutes. The large-period branch computes `left=2`, `right=4`, and obtains cost `pref_g[4] - pref_g[2] = 0`.

For the equal-interval case

```
6 2
0 2
4 6
```

the best solution is (A=1,S=1). The garland is lit during minutes (1,3,5), giving exactly three lit minutes, which satisfies the half-holiday condition. It intersects the grandfather intervals during minutes (1) and (5), so the cost is two. Switching at (S=0) also gives cost two, but the tie-breaking rule selects the later start (S=1).

For the maximum holiday length

```
5000 0
```

there is no grandfather, so the objective is zero. The smallest possible (A) is (1). With (S=1), the garland is lit during every other minute from (1) through (4999), giving exactly (2500) lit minutes. A later start would leave fewer than half of the holiday lit. The resulting answer is

```
0 1 1
```

This last case also exercises the tie-breaking rule when many configurations have zero cost: the algorithm keeps (A=1), then chooses the latest feasible switching time for that (A).
