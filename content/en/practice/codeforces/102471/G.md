---
title: "CF 102471G - Happiness"
description: "Pang is one of n teams in a ten-problem ICPC contest. The other n - 1 teams have fixed final results. Pang knows a subset of the ten problems, and solving a known problem takes a fixed amount of time and incurs a fixed number of rejected submissions before acceptance."
date: "2026-08-09T15:53:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "G"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 670
verified: true
draft: false
---

[CF 102471G - Happiness](https://codeforces.com/problemset/problem/102471/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

Pang is one of `n` teams in a ten-problem ICPC contest. The other `n - 1` teams have fixed final results. Pang knows a subset of the ten problems, and solving a known problem takes a fixed amount of time and incurs a fixed number of rejected submissions before acceptance.

Pang must solve problems one after another. If a problem takes `x` minutes, then its accepted submission happens at the current elapsed time plus `x`. That completion time is what enters the team's solution-time list. The same completion time, plus `20` minutes for every previous rejection on that problem, contributes to the team's total penalty. Pang may stop at any point, but every accepted submission must happen no later than minute `300`.

The order affects Pang's result because later problems receive larger completion times. The final rank is determined first by the number of solved problems, then by total penalty, and finally by the descending list of completion times. Pang wins a complete tie against every other team.

Happiness is a function of this rank, plus several independent bonuses. A medal depends only on the rank. Each problem contributes `800` if Pang's completion time for that problem is no later than every other team's completion time for that problem. There is also a `700` bonus for having the earliest solution time in the entire contest and a `500` bonus for having the latest one. Equal times count as Pang winning the corresponding bonus.

The input contains `n - 1` fixed team descriptions followed by Pang's description. A solved status contains its accepted time and rejection count, while `-` means that the problem was not solved. The output is the maximum happiness Pang can obtain by choosing both which known problems to solve and their order. The official statement and sample are available on Codeforces.

The small number of problems is the key constraint. There are only ten problems, so subset dynamic programming is realistic. The potentially large part is `n`, which can reach `300`. That means we should avoid doing work proportional to `n` for millions of possible Pang schedules. A solution around `O(n * 2^10 * poly(10))` is easily small enough, while enumerating millions of schedules and comparing each one against all `300` teams is not.

There are several edge cases that matter because they change the ranking or bonus calculation. Pang may solve no problems at all. For example, with ten teams and every status equal to `-`, Pang has zero solved problems and ties every team, so Pang is rank `1` and receives `5000` happiness. A solution that assumes Pang must solve something would miss the optimum.

The boundary at exactly minute `300` is also significant. Consider ten teams where every team solves only problem 1 at time `300` with zero rejected runs, and Pang has the same status. Pang is rank `1`, the solution is considered first because ties favor Pang, and the solution is both the earliest and latest solution. The answer is `5000 + 1200 + 800 + 700 + 500 = 8200`. Treating `300` as forbidden instead of allowed would discard the only solution.

Ties must also favor Pang when calculating rank. If Pang's ranking key is identical to several other teams, those teams do not count as strictly better. This is why the implementation uses a lower bound in the sorted list of other teams. Using an upper bound would place Pang behind equal teams.

The rejection penalty must be kept separate from the solution-time list. A problem solved at time `100` with three rejected runs contributes `160` to total penalty, but its solution time for the lexicographic comparison is still `100`. Confusing these two values can change the rank even when the number of solved problems is correct.

Finally, the latest-solution bonus is based on Pang's final elapsed time, which is the sum of the solving durations of all selected problems. It is not based on the duration of the final problem alone. The earliest-solution bonus is similarly based on the first completion time.

## Approaches

A direct approach would enumerate every possible ordered sequence of known problems. A sequence can stop after any length, because Pang is allowed to stop solving. With ten problems, the number of nonempty ordered sequences is

`P(10,1) + P(10,2) + ... + P(10,10) = 9,864,100`.

For every such sequence, we could calculate Pang's ranking key and compare it with every other team. In the worst case, with `n = 300`, that means about `9,864,100 * 299 = 2,949,365,900` team comparisons before even considering the cost of comparing solution-time lists. The brute force is correct because every legal schedule appears explicitly, but it is far too expensive.

The first useful observation is that the other teams never change. We can sort all other teams once according to the exact ranking rule. Pang's rank can then be found by binary search instead of comparing against every team.

A team's ranking can be represented by one tuple:

`(-solved_count, total_penalty, descending_solution_times)`.

Smaller tuples represent better teams. Negating the solved count turns "more solved problems is better" into ordinary tuple ordering. The descending solution-time list already has the correct lexicographic direction.

Pang's rank is then one plus the number of other teams whose tuple is strictly smaller. Since Pang wins ties, `bisect_left` gives exactly the required position.

That removes the factor of `n` from schedule evaluation, but enumerating nearly ten million schedules is still unnecessary.

The second observation is that the number of problems is only ten, so the set of already solved problems can be represented by a bitmask. For a fixed subset, the final elapsed time is fixed because it is simply the sum of the solving durations. The only order-dependent ranking quantity is the sum of completion times.

There is another important property. For a fixed subset, the number of problem-first bonuses can be used as a small DP dimension. If two orders solve exactly the same subset, obtain the same number of problem-first bonuses, and have different total penalties, the order with the smaller penalty is always preferable. Every happiness component depending on rank is monotone with rank, so a worse total penalty can never compensate for a better order when all other bonuses are identical.

If the penalties are also equal, only the lexicographically smaller descending completion-time list matters. Thus one DP state only needs the best pair consisting of total penalty and solution-time list.

The only bonus that depends on the first problem itself is the `700` earliest-solution bonus. We can handle this cleanly by fixing the first problem and running a subset DP for each possible first problem. There are only ten choices. Once the first problem is fixed, its completion time and the earliest-solution bonus are known for every state.

The resulting DP explores subsets rather than ordered sequences. A transition appends one unsolved problem. If the current elapsed time is `T` and problem `j` takes `x[j]`, its completion time becomes `T + x[j]`. The transition is legal only if this value is at most `300`.

The problem-first bonus is particularly convenient. For every problem, precompute the earliest solution time achieved by any other team. If Pang completes that problem no later than this threshold, he gets its `800` bonus. The equality case belongs to Pang.

For the global bonuses, precompute the minimum and maximum solution times among all other teams. Once Pang solves at least one problem, his first completion time determines the `700` bonus and his final completion time determines the `500` bonus.

The brute-force method works because it directly considers every order. It fails because the same subset contains many redundant prefixes. The observation that all relevant order-dependent information can be summarized by a subset, a small bonus count, and the best ranking key lets us collapse those schedules into only a few thousand states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(P(10,1)+...+P(10,10)) * O(n)` | `O(10)` | Too slow |
| Optimal | `O(10 * 2^10 * 10 * 11 * log n)` | `O(2^10 * 11 * 10)` | Accepted |

## Algorithm Walkthrough

1. Parse every other team's ten problem statuses and build its ranking key. Count its solved problems, calculate its total penalty as `t + 20w` for every solved problem, and store its solved times in descending order. Sort all `n - 1` keys.
2. While parsing the other teams, also compute four thresholds. For each problem, store the smallest solution time any other team achieved. Store the smallest solution time over the entire contest and the largest solution time over the entire contest. If nobody solved a particular problem, its threshold can be set to `301`, because every legal Pang solution is at most `300`. If nobody solved anything, use `301` for the global minimum and `0` for the global maximum.
3. Evaluate the possibility that Pang solves nothing. Its ranking key is `(0, 0, ())`, and no time-based bonuses apply. This candidate must be considered because solving a problem can actually reduce Pang's rank without necessarily compensating through bonuses.
4. Fix one known problem `first` as Pang's first problem. Initialize a subset DP containing only this problem. The elapsed time is its solving duration, its penalty contribution is its completion time plus `20` times its rejection count, and its solution-time list contains that completion time.
5. For every mask containing `first`, maintain one state for every possible number of problem-first bonuses. A state stores the smallest total penalty achievable with that mask and bonus count. If two states have equal penalty, keep the lexicographically smaller descending completion-time tuple, because that state has the better rank.
6. Try appending every known problem not already present in the mask. The new completion time is the current subset's total duration plus the new problem's duration. Reject the transition if this exceeds `300`, because Pang cannot submit after the contest ends.
7. Add the new problem's rejection penalty and completion time to the total penalty. If its completion time is no later than the best other team's time for that problem, increase the problem-first bonus count by one. Since the new completion time is later than every previous completion time, prepend it to the descending solution-time tuple.
8. After all masks have been processed for the fixed first problem, evaluate every reachable state as a possible stopping point. Its ranking key is formed directly from the subset size, its stored penalty, and its stored descending solution-time tuple. Use `bisect_left` in the sorted list of other teams to obtain Pang's rank.
9. Add the rank-based happiness and medal happiness. Add `800` times the stored problem-first bonus count. Since the first problem is fixed, add `700` when its completion time is no later than the global minimum solution time of the other teams. Add `500` when the final elapsed time is at least the global maximum solution time of the other teams.
10. Repeat the DP for every possible first problem and keep the largest happiness value. Every legal nonempty Pang schedule has exactly one first problem, so it appears in exactly one of these ten DP runs.

The correctness invariant is that, for every fixed first problem, subset mask, and problem-first bonus count, the retained DP state is the best possible ranking state among all orders producing exactly that information. A larger penalty can never improve rank, while equal penalties are decided solely by the solution-time list, so discarding every other state is safe. Every legal schedule is built one problem at a time through these transitions, and every stopping point is evaluated. The ranking key exactly matches the contest's ranking rule, with `bisect_left` implementing Pang's advantage on ties. Since every possible schedule is represented and every discarded state is dominated for all remaining happiness components, the maximum evaluated happiness is the true optimum.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def parse_team(line):
    result = []
    for item in line.strip().split(","):
        if item == "-":
            result.append(None)
        else:
            t, w = map(int, item.split())
            result.append((t, w))
    return result

def solve_parsed(n, rows):
    other_rows = rows[:n - 1]
    pang_row = rows[n - 1]

    other_keys = []

    first_limit = [301] * 10
    global_min = 301
    global_max = 0

    for line in other_rows:
        team = parse_team(line)

        solved = 0
        penalty = 0
        times = []

        for j, status in enumerate(team):
            if status is None:
                continue

            t, w = status
            solved += 1
            penalty += t + 20 * w
            times.append(t)

            if t < first_limit[j]:
                first_limit[j] = t
            if t < global_min:
                global_min = t
            if t > global_max:
                global_max = t

        times.sort(reverse=True)
        other_keys.append((-solved, penalty, tuple(times)))

    other_keys.sort()

    pang = parse_team(pang_row)

    x = [None] * 10
    y = [0] * 10
    known = []

    for i, status in enumerate(pang):
        if status is not None:
            x[i], y[i] = status
            known.append(i)

    # Rank of Pang. Pang wins a complete tie, so equal keys
    # must be placed after Pang, which is exactly bisect_left.
    def get_rank(solved, penalty, times):
        key = (-solved, penalty, times)
        return bisect_left(other_keys, key) + 1

    def rank_happiness(rank):
        h = 5000 // rank
        q = n // 10

        if rank <= q:
            h += 1200
        elif rank <= 3 * q:
            h += 800
        elif rank <= 6 * q:
            h += 400

        return h

    # Pang solves nothing.
    best = rank_happiness(get_rank(0, 0, ()))

    size = 1 << 10

    # Sum of solving durations for every mask.
    sum_time = [0] * size
    for mask in range(1, size):
        bit = mask & -mask
        j = bit.bit_length() - 1
        sum_time[mask] = sum_time[mask ^ bit]
        if x[j] is not None:
            sum_time[mask] += x[j]

    for first in known:
        first_mask = 1 << first
        first_completion = x[first]
        first_bonus = 1 if first_completion <= first_limit[first] else 0
        first_penalty = first_completion + 20 * y[first]

        # dp[mask] is a dictionary:
        # bonus_count -> (minimum_penalty, descending_solution_times)
        dp = [None] * size
        dp[first_mask] = {
            first_bonus: (first_penalty, (first_completion,))
        }

        for mask in range(size):
            states = dp[mask]
            if not states or not (mask & first_mask):
                continue

            elapsed = sum_time[mask]

            for bonus_count, state in list(states.items()):
                penalty, times = state

                for j in known:
                    bit = 1 << j
                    if mask & bit:
                        continue

                    new_elapsed = elapsed + x[j]
                    if new_elapsed > 300:
                        continue

                    add_bonus = 1 if new_elapsed <= first_limit[j] else 0
                    new_bonus = bonus_count + add_bonus

                    new_penalty = penalty + new_elapsed + 20 * y[j]
                    new_times = (new_elapsed,) + times

                    new_mask = mask | bit
                    if dp[new_mask] is None:
                        dp[new_mask] = {}

                    old = dp[new_mask].get(new_bonus)

                    if old is None or (
                        new_penalty < old[0]
                        or (
                            new_penalty == old[0]
                            and new_times < old[1]
                        )
                    ):
                        dp[new_mask][new_bonus] = (
                            new_penalty,
                            new_times,
                        )

        # Every reachable state is a legal point at which Pang may stop.
        for mask in range(size):
            states = dp[mask]
            if not states:
                continue

            solved = mask.bit_count()
            final_elapsed = sum_time[mask]

            for bonus_count, (penalty, times) in states.items():
                rank = get_rank(solved, penalty, times)

                happiness = rank_happiness(rank)
                happiness += 800 * bonus_count

                # The first problem is fixed in this DP run.
                if first_completion <= global_min:
                    happiness += 700

                if final_elapsed >= global_max:
                    happiness += 500

                if happiness > best:
                    best = happiness

    return best

def main():
    n = int(input())
    rows = [input().strip() for _ in range(n)]
    print(solve_parsed(n, rows))

if __name__ == "__main__":
    main()
```

The parsing code converts every solved status into `(time, rejected_runs)` and represents `-` by `None`. For other teams, the ranking key is constructed immediately after parsing. The solution-time list is sorted in descending order because that is exactly the order used by the final tie-break.

The four thresholds are collected during the same pass, so no separate scan over the teams is necessary. A threshold of `301` is safe because Pang can never have a legal completion time larger than `300`.

The `get_rank` function is one of the most delicate parts. The tuple uses `-solved` because Python's ordinary tuple comparison treats smaller values as better. After sorting all other teams, `bisect_left` returns the number of strictly smaller keys. Equal keys are not counted as better because Pang wins those ties.

The subset duration array lets every transition obtain the current elapsed time in constant time. For a transition from `mask` to `mask | (1 << j)`, the new completion time is simply `sum_time[mask] + x[j]`.

The DP stores only the best penalty for each bonus count. The rejection term `20 * y[j]` is added when problem `j` is solved, while its completion time is also added because that is part of the contest penalty. The completion-time tuple does not include rejection penalties.

Prepending the new completion time to the tuple is correct because every later problem has a strictly larger completion time. Thus, if the completion times in chronological order are `t1, t2, t3`, the ranking list is `(t3, t2, t1)`.

The `300` boundary uses `<=`, not `<`. A problem completing exactly at minute `300` is legal. The earliest and latest bonuses also use inclusive comparisons because Pang wins ties.

Python integers have arbitrary precision, so no overflow handling is required. The largest penalty is tiny compared with Python's integer range anyway.

## Worked Examples

The official sample has Pang knowing six problems, but their solving durations make only a few two-problem schedules feasible within `300` minutes. One optimal schedule solves problem 1 first, taking `38` minutes, and then problem 8, taking another `254` minutes. The important DP states for that schedule are shown below. The official sample output is `1800`.

| Step | Solved problems | Elapsed | Penalty | Descending solution times | Problem-first bonuses |
| --- | --- | --- | --- | --- | --- |
| Start | `{}` | `0` | `0` | `()` | `0` |
| Solve problem 1 | `{1}` | `38` | `238` | `(38,)` | `1` |
| Solve problem 8 | `{1,8}` | `292` | `670` | `(292,38)` | `1` |

The other teams contain a team with two solved problems and penalty `397`, so Pang's penalty `670` leaves him at rank `10` among the ten teams. The earliest other solution is at minute `4`, so Pang does not receive the `700` earliest-solution bonus. The latest other solution is at minute `290`, while Pang finishes at `292`, so he receives the `500` latest-solution bonus. Problem 1 is solved first because Pang's `38` is earlier than every other team's solution for that problem. The resulting happiness is `500 + 800 + 500 = 1800`.

A second example isolates the exact `300` boundary. Suppose all nine other teams solve only problem 1 at minute `300`, and Pang has the same single problem.

| Step | Solved problems | Elapsed | Rank | Problem-first bonuses | Earliest bonus | Latest bonus |
| --- | --- | --- | --- | --- | --- | --- |
| Start | `{}` | `0` | `1` | `0` | `0` | `0` |
| Solve problem 1 | `{1}` | `300` | `1` | `1` | `1` | `1` |

Pang wins the complete ranking tie, because his key is identical to every other team's key and ties belong to Pang. The completion at exactly `300` is legal, and equality is enough for all three time-based bonuses. The final happiness is `5000 + 1200 + 800 + 700 + 500 = 8200`.

This trace demonstrates why the DP must allow stopping at a state whose elapsed time is exactly `300`, why ranking must use `bisect_left`, and why all time comparisons are inclusive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n * 10 + 10 * 2^10 * 10 * 11 * log n)` | Parsing is linear in the number of statuses. Each first problem runs a subset DP with at most ten transitions and eleven bonus-count states, and every retained state can be ranked with binary search. |
| Space | `O(n * 10 + 2^10 * 11 * 10)` | The fixed team ranking keys are stored, while each DP state stores a penalty and a solution-time tuple of length at most ten. |

With only ten problems, `2^10 = 1024`. Even after multiplying by ten possible first problems and eleven possible bonus counts, the state space remains small. The contest can contain `300` teams, but those teams are processed once and then represented by sorted ranking keys. The solution comfortably fits the `2` second and `256 MB` limits.

## Test Cases

The following tests assume the solution is saved as `solution.py`, exposing the `solve_parsed` function shown above.

```
from solution import solve_parsed

def run(inp: str) -> str:
    lines = inp.strip().splitlines()
    n = int(lines[0])
    return str(solve_parsed(n, lines[1:]))

# Official sample
sample1 = """\
10
233 1,-,-,7 7,257 4,173 5,117 1,-,-,85 3
-,231 0,167 0,257 7,-,-,122 4,283 0,215 4,-
41 1,-,290 8,-,-,-,-,246 7,120 3,184 9
142 8,243 7,69 0,-,41 9,-,279 1,264 4,-,74 9
53 8,-,187 9,60 1,48 8,99 10,-,-,55 7,259 5
250 0,-,-,-,166 0,16 3,-,82 4,73 0,184 3
-,-,-,-,105 3,-,-,-,152 4,-
-,84 5,98 8,-,120 8,241 3,94 1,-,28 7,109 8
280 6,246 5,58 9,-,-,-,-,-,-,-
38 10,-,227 10,187 9,182 1,-,203 9,254 7,-,-
"""
assert run(sample1) == "1800", "official sample"

# Minimum-size contest, everyone solves nothing.
sample2 = """\
10
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
-,-,-,-,-,-,-,-,-,-
"""
assert run(sample2) == "5000", "zero solved problems"

# Exact 300-minute boundary, with a complete tie.
sample3 = """\
10
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
300 0,-,-,-,-,-,-,-,-,-
"""
assert run(sample3) == "8200", "exactly 300 and Pang wins ties"

# Ranking is worse, but time bonuses and one first-solved bonus remain.
sample4 = """\
10
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
120 0,80 0,-,-,-,-,-,-,-,-
50 0,100 0,-,-,-,-,-,-,-,-
"""
assert run(sample4) == "2500", "order-dependent first-solved bonus"

# Maximum n, repeated Pang durations, and the 300-minute final boundary.
other = "-,-,-,-,-,-,-,-,-,-"
pang = "30 0,30 0,30 0,30 0,30 0,30 0,30 0,30 0,30 0,30 0"

sample5 = "300\n" + "\n".join([other] * 299 + [pang]) + "\n"
assert run(sample5) == "15400", "maximum n and repeated durations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Official sample | `1800` | Complete ranking and bonus interaction |
| Ten teams with no solved problems | `5000` | Empty Pang schedule |
| Nine identical `300`-minute teams | `8200` | Exact `300` boundary and Pang's tie advantage |
| Two problems with thresholds `120` and `80` | `2500` | Order-dependent first-solved bonuses and ranking |
| `n = 300`, ten problems taking `30` each | `15400` | Maximum `n`, repeated durations, all problem bonuses, and final time `300` |

## Edge Cases

When Pang solves nothing, the algorithm evaluates the empty ranking key before entering any DP. For ten teams with all statuses equal to `-`, every team has key `(0, 0, ())`. `bisect_left` returns position `0`, giving Pang rank `1`, and `5000` happiness. No time bonus is added because Pang has no solution. This prevents an incorrect implementation from forcing Pang to choose a known problem.

For a solution exactly at minute `300`, the transition condition is `new_elapsed > 300`, so `new_elapsed == 300` remains legal. If every other team solves problem 1 at `300` and Pang does the same, the ranking key is identical for everyone. `bisect_left` gives Pang rank `1`. The problem-first comparison uses `<=`, so Pang gets `800`; the global minimum and maximum comparisons are also inclusive, giving both `700` and `500`. The result is `8200`.

For a ranking tie with multiple equal teams, the key itself contains no team identifier. This is deliberate. Pang is not merely tied with those teams, he is defined to rank before them. If five other teams have exactly the same key as Pang, `bisect_left` places Pang before all five. Using `bisect_right` would incorrectly place him after them and could also change his medal and rank-based happiness.

For problem-first bonuses, the DP compares the completion time, not the raw solving duration. Suppose Pang first solves a `50`-minute problem and then a `100`-minute problem. Their completion times are `50` and `150`, not `50` and `100`. The second problem's first-solved bonus must be checked against `150`. The transition computes this cumulative completion time explicitly, so later problems cannot accidentally receive a bonus based only on their own solving durations.

For the latest-solution bonus, every selected problem contributes its solving duration to the final elapsed time. If Pang solves problems taking `50` and `100` minutes, the final solution time is `150` regardless of which problem is second. The DP uses `sum_time[mask]` for this value, so the `500` bonus is evaluated against the actual final submission time.

For equal total penalties, the DP compares the stored descending completion-time tuples. This is necessary because the contest uses that list as the third ranking criterion. For example, two schedules may both have penalty `300`, but one can produce `(200, 100)` while another produces `(190, 110)`. The latter is better because `190 < 200` at the first differing position. The state comparison uses ordinary Python tuple ordering, which matches exactly the required lexicographic rule.

For a problem that nobody else solved, its first-solved threshold remains `301`. Every legal Pang completion is at most `300`, so Pang automatically receives the `800` bonus for that problem. The same idea applies to the global minimum threshold when no other team solved anything. Using `301` rather than a very large sentinel also makes the boundary argument explicit.

For the global maximum, the default threshold is `0` when no other team solved any problem. Any nonempty Pang schedule finishes at a positive time, so Pang receives the `500` latest-solution bonus. The empty schedule is evaluated separately and does not receive it, because the bonus requires at least one solution.

A small implementation detail to keep in mind when submitting is that the sample shown in the statement is visually wrapped across lines, while the actual judge input has exactly one team description per line.
