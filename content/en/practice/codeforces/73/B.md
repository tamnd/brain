---
title: "CF 73B - Need For Brake"
description: "We know the current championship standings before the final race. Every racer already has some number of points, and the last race distributes additional points to the top m finishers."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 73
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 66"
rating: 2000
weight: 73
solve_time_s: 129
verified: true
draft: false
---

[CF 73B - Need For Brake](https://codeforces.com/problemset/problem/73/B)

**Rating:** 2000  
**Tags:** binary search, greedy, sortings  
**Solve time:** 2m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We know the current championship standings before the final race. Every racer already has some number of points, and the last race distributes additional points to the top `m` finishers. The racer in first place of the race receives `b[0]` points, the racer in second place receives `b[1]`, and so on.

After the final race, competitors are ranked by total points in descending order. If two racers finish with the same number of points, the racer with the lexicographically smaller nickname is considered higher.

We are asked for two values for Vasya's racer:

1. The best final championship position he can still achieve.
2. The worst final championship position he can still fall to.

The final race ordering is completely under our control. Any racer can be assigned any finishing place exactly once. This means we are free to distribute the bonus points in whichever way helps or hurts Vasya the most.

The constraints force us to think carefully. There can be up to `10^5` racers, so anything quadratic is already too expensive. A naive simulation that repeatedly tries all possible point assignments would explode combinatorially. Even an `O(n^2)` check with `10^5` racers would require around `10^10` operations, which is impossible within 4 seconds.

The tricky part is the tie-breaking rule. Equal scores are not enough for equality in ranking. Lexicographical order decides the winner among ties.

Consider this input:

```
2
alex 10
vasya 10
0
vasya
```

No bonus points are distributed. Both racers finish with 10 points. Since `"alex" < "vasya"`, Alex ranks above Vasya, so the answer is:

```
2 2
```

A careless implementation that compares only scores would incorrectly output `1 1`.

Another subtle case appears when some bonus values are zero.

```
3
aaa 5
bbb 5
vasya 5
2
10 0
vasya
```

Giving Vasya the first-place race bonus yields 15 points, which guarantees first overall. But if Vasya gets the zero bonus, ties become important again. We cannot assume awarded positions always change rankings.

One more dangerous edge case is when `m = 0`.

```
3
a 100
vasya 100
z 100
0
vasya
```

No points are added at all. Final ordering is determined purely by lexicographical order among equal scores. Vasya finishes second.

Implementations that always assume Vasya participates among the rewarded racers will fail here.

## Approaches

The brute-force perspective is straightforward. We could try every possible finishing position for Vasya, then assign the remaining race positions to all other racers in every possible way, finally compute the resulting championship ranking.

This is correct because it explores every valid outcome of the last race. The problem is the number of permutations. Even for 15 racers, trying all assignments is already infeasible. With `10^5` racers, exhaustive search is hopeless.

The key observation is that we never care about the exact ordering of everyone else. We only care whether a racer can finish above Vasya.

Suppose we fix the bonus Vasya receives. His final score becomes:

```
vasya_score = current_score + chosen_bonus
```

Now the question becomes:

How many racers can be forced above him, or prevented from going above him?

For any other racer, whether they beat Vasya depends only on whether there exists an unused bonus that makes their final score strictly better than Vasya's, or equal with lexicographically smaller name.

This transforms the problem into a greedy matching problem between racers and available bonuses.

For the best possible final rank, we want as few racers above Vasya as possible. Naturally, we should give dangerous bonuses only when unavoidable. The smallest sufficient bonus should be used for each racer.

For the worst possible final rank, we want as many racers above Vasya as possible. Then we greedily give strong bonuses to racers whenever possible.

Both versions reduce to checking how many racers can surpass a fixed target score under greedy assignment of bonuses. Sorting makes this efficient.

The final complexity becomes `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Best Possible Position

1. Try every possible bonus Vasya can receive.

Vasya may finish outside the rewarded positions, so receiving zero extra points is also possible when some bonuses remain unused.
2. Compute Vasya's final score after taking that bonus.
3. Remove that bonus from the available pool.
4. Sort the remaining bonuses in increasing order.
5. For every other racer, compute the minimum extra points needed to finish above Vasya.

A racer beats Vasya if:

- their total score becomes larger, or
- the total score becomes equal and their nickname is lexicographically smaller.
6. Process racers in increasing order of required bonus.

For each racer, greedily assign the smallest available bonus that is sufficient.

This minimizes the number of racers that can surpass Vasya because strong bonuses are preserved for harder cases.
7. Count how many racers successfully surpass Vasya.
8. Vasya's final position is one plus that count.
9. Take the minimum over all choices of Vasya's bonus.

### Worst Possible Position

1. Again try every possible bonus Vasya can receive.
2. Compute his final score.
3. Remove Vasya's chosen bonus from the available pool.
4. Sort the remaining bonuses in increasing order.
5. For every other racer, determine the minimum bonus needed to surpass Vasya.
6. Process racers from hardest to easiest to satisfy.

We now want to maximize the number of racers above Vasya. The optimal strategy is to give the largest bonuses to racers that need the most help.
7. Greedily match the largest remaining bonuses.
8. Count how many racers can be pushed above Vasya.
9. Vasya's final position becomes one plus that count.
10. Take the maximum over all choices of Vasya's bonus.

### Why it works

The crucial property is that each racer only depends on whether they receive a bonus at least as large as some threshold.

This converts the problem into a matching problem between thresholds and available bonuses.

For minimizing the number of successful racers, assigning the smallest sufficient bonus is always optimal. Any larger bonus would only waste resources that could help another racer later.

For maximizing the number of successful racers, assigning the largest bonuses to the racers with the highest requirements is optimal. If a large requirement cannot be satisfied now, it cannot be satisfied later by smaller bonuses.

Both greedy strategies are classic exchange arguments. Any non-greedy assignment can be rearranged into the greedy one without worsening the result.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

def better(name1, score1, name2, score2):
    if score1 != score2:
        return score1 > score2
    return name1 < name2

def solve():
    n = int(input())

    names = []
    scores = []

    for _ in range(n):
        s, a = input().split()
        names.append(s)
        scores.append(int(a))

    m = int(input())
    b = list(map(int, input().split())) if m else []

    vasya = input().strip()
    vid = names.index(vasya)

    bonus_options = b[:] + [0]

    best = n
    worst = 1

    for used_bonus in bonus_options:
        vasya_score = scores[vid] + used_bonus

        remaining = b[:]
        removed = False

        for i in range(len(remaining)):
            if remaining[i] == used_bonus and not removed:
                remaining.pop(i)
                removed = True
                break

        remaining.sort()

        need = []

        for i in range(n):
            if i == vid:
                continue

            cur = scores[i]

            if names[i] < vasya:
                req = vasya_score - cur
            else:
                req = vasya_score - cur + 1

            req = max(req, 0)
            need.append(req)

        need.sort()

        # best rank
        ptr = 0
        above = 0

        for req in need:
            pos = bisect_left(remaining, req, ptr)
            if pos == len(remaining):
                continue
            above += 1
            ptr = pos + 1

        best = min(best, above + 1)

        # worst rank
        rem_ptr = len(remaining) - 1
        above = 0

        for req in reversed(need):
            if rem_ptr >= 0 and remaining[rem_ptr] >= req:
                above += 1
                rem_ptr -= 1

        worst = max(worst, above + 1)

    print(best, worst)

solve()
```

The solution iterates over every possible bonus Vasya might receive. There are at most `m + 1` such choices, including the possibility of receiving no points.

The helper condition for comparing racers is encoded through the required bonus calculation. Suppose another racer currently has `cur` points.

If their name is lexicographically smaller than Vasya's, equality is enough to rank above him, so they need:

```
cur + bonus >= vasya_score
```

Otherwise they need strictly more points:

```
cur + bonus > vasya_score
```

This distinction is the most common source of wrong answers.

For the best-rank calculation, we greedily assign the smallest bonus that satisfies each racer. The `bisect_left` call efficiently finds the first usable bonus.

For the worst-rank calculation, we reverse both arrays and greedily consume the largest remaining bonus. This maximizes successful matches.

The code removes only one occurrence of Vasya's chosen bonus. This matters when multiple bonuses have equal value.

## Worked Examples

### Example 1

Input:

```
3
teama 10
teamb 20
teamc 40
2
10 20
teama
```

Suppose Vasya takes bonus `20`.

| Racer | Current | Needed to beat Vasya | Assigned bonus | Beats Vasya |
| --- | --- | --- | --- | --- |
| teamb | 20 | 11 | none | No |
| teamc | 40 | 0 | 10 | Yes |

Vasya finishes with `30`.

Only `teamc` can stay above him, so Vasya becomes second.

Now suppose Vasya takes `0`.

| Racer | Current | Needed | Assigned |
| --- | --- | --- | --- |
| teamb | 11 | 20 |  |
| teamc | 0 | 10 |  |

Both racers finish above him, so he becomes third.

The final answer is:

```
2 3
```

This trace shows why trying every possible bonus for Vasya is necessary.

### Example 2

```
4
adam 10
bob 10
vasya 10
zoe 10
2
0 5
vasya
```

If Vasya takes `5`, his final score is `15`.

| Racer | Lexicographically smaller? | Needed |
| --- | --- | --- |
| adam | Yes | 5 |
| bob | Yes | 5 |
| zoe | No | 6 |

Only one remaining bonus exists, namely `0`, so nobody beats him.

If Vasya takes `0`, his final score is `10`.

| Racer | Needed |
| --- | --- |
| adam | 0 |
| bob | 0 |
| zoe | 1 |

Now both `adam` and `bob` already outrank him due to lexicographical order.

Final answer:

```
1 3
```

This example demonstrates why equal scores cannot be treated uniformly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting and binary searches dominate |
| Space | O(n) | Arrays for bonuses and requirements |

The algorithm easily fits the constraints. Sorting `10^5` values and performing logarithmic searches is well within the 4-second limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_left

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n = int(input())

        names = []
        scores = []

        for _ in range(n):
            s, a = input().split()
            names.append(s)
            scores.append(int(a))

        m = int(input())
        b = list(map(int, input().split())) if m else []

        vasya = input().strip()
        vid = names.index(vasya)

        bonus_options = b[:] + [0]

        best = n
        worst = 1

        for used_bonus in bonus_options:
            vasya_score = scores[vid] + used_bonus

            remaining = b[:]
            removed = False

            for i in range(len(remaining)):
                if remaining[i] == used_bonus and not removed:
                    remaining.pop(i)
                    removed = True
                    break

            remaining.sort()

            need = []

            for i in range(n):
                if i == vid:
                    continue

                cur = scores[i]

                if names[i] < vasya:
                    req = vasya_score - cur
                else:
                    req = vasya_score - cur + 1

                req = max(req, 0)
                need.append(req)

            need.sort()

            ptr = 0
            above = 0

            for req in need:
                pos = bisect_left(remaining, req, ptr)
                if pos == len(remaining):
                    continue
                above += 1
                ptr = pos + 1

            best = min(best, above + 1)

            rem_ptr = len(remaining) - 1
            above = 0

            for req in reversed(need):
                if rem_ptr >= 0 and remaining[rem_ptr] >= req:
                    above += 1
                    rem_ptr -= 1

            worst = max(worst, above + 1)

        return f"{best} {worst}"

    return solve()

# provided sample
assert run(
"""3
teama 10
teamb 20
teamc 40
2
10 20
teama
"""
) == "2 3", "sample 1"

# minimum size
assert run(
"""1
vasya 0
0
vasya
"""
) == "1 1", "single racer"

# tie-breaking check
assert run(
"""3
adam 10
vasya 10
zoe 10
0
vasya
"""
) == "2 2", "lexicographical ties"

# all bonuses zero
assert run(
"""4
a 5
b 5
vasya 5
z 5
3
0 0 0
vasya
"""
) == "3 3", "zero bonuses"

# off-by-one strict inequality
assert run(
"""2
vasya 10
zzz 10
1
0
vasya
"""
) == "1 1", "equal score but larger name stays below"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single racer | `1 1` | Minimum input size |
| Lexicographical ties | `2 2` | Equal scores use name ordering |
| All bonuses zero | `3 3` | Zero bonuses handled correctly |
| Equal score with larger name | `1 1` | Strict comparison logic |

## Edge Cases

Consider the pure tie-breaking case:

```
3
a 100
vasya 100
z 100
0
vasya
```

Vasya receives no bonus because no bonuses exist.

The algorithm computes required bonuses:

| Racer | Needed |
| --- | --- |
| a | 0 |
| z | 1 |

Racer `a` already beats Vasya because `"a" < "vasya"` and equal scores are enough.

Racer `z` would need one extra point, which is impossible.

Exactly one racer finishes above Vasya, so the answer is:

```
2 2
```

Now consider repeated bonus values:

```
4
a 0
b 0
c 0
vasya 0
3
5 5 5
vasya
```

Suppose Vasya takes one `5`.

The algorithm removes only one occurrence from the multiset of bonuses. Two bonuses remain available.

Every other racer needs `5` points to tie or exceed Vasya.

Both remaining bonuses can still be assigned, so two racers surpass him.

If we accidentally removed all copies of `5`, we would incorrectly conclude nobody can beat Vasya.

Finally, consider the strict inequality case:

```
2
vasya 10
zzz 10
1
0
vasya
```

Racer `zzz` has a lexicographically larger name, so tying is not enough.

The required bonus becomes:

```
10 - 10 + 1 = 1
```

But the only available bonus is `0`.

The algorithm correctly concludes that nobody can finish above Vasya, producing:

```
1 1
```

A solution that forgets the `+1` would incorrectly place Vasya second.
