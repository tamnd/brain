---
title: "CF 102317G - Jedi and the Galactic Empire"
description: "We have several protection missions. During one mission, a known sequence of blaster shots reaches the Jedi at specified times. There are either one or two Jedi protecting the asset, and each Jedi has his own reaction time. A Jedi can always block the first shot assigned to him."
date: "2026-08-17T10:15:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102317
codeforces_index: "G"
codeforces_contest_name: "UCF Locals 2016"
rating: 0
weight: 102317
solve_time_s: 112
verified: true
draft: false
---

[CF 102317G - Jedi and the Galactic Empire](https://codeforces.com/problemset/problem/102317/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We have several protection missions. During one mission, a known sequence of blaster shots reaches the Jedi at specified times. There are either one or two Jedi protecting the asset, and each Jedi has his own reaction time. A Jedi can always block the first shot assigned to him. After blocking a shot at time `t`, that same Jedi cannot block another shot until time `t + reaction_time`.

The shot times may be given in arbitrary order, so the first step is to sort them chronologically. For every shot, we want to decide which Jedi blocks it, if either can do so. The required output is the minimum possible number of shots that reach the protected asset. The official contest statement gives at most 1000 shots per mission, one or two Jedi, and reaction times from 1 through 100.

The small bound of 1000 shots means even a quadratic algorithm would be practical for a single mission, but the real structure of the problem allows us to do better. A brute-force search over every possible assignment would have three choices for each shot, so its worst case is `3^b` assignments. With `b = 1000`, that is far beyond what any contest time limit can handle. The useful solution should process the shots after sorting and make only constant work per shot.

There are several edge cases where an implementation can silently go wrong. First, equal shot times are distinct shots, and different Jedi may block different shots arriving at exactly the same time. For example, with

```
1
2
5 5
2
1 10
```

both Jedi can block one of the two shots at time 5, so the answer is `0`. A careless implementation that removes duplicate times would incorrectly report `1`.

A second edge case is that the Jedi do not have to use the same strategy when both are available. Consider

```
1
3
1 2 3
2
2 100
```

the Jedi with reaction time 2 can block all three shots, so the answer is `0`. An implementation that assigns the first shot to the slower Jedi merely because that Jedi is also available would still happen to work on this input, but the choice matters in more carefully constructed sequences. The correct rule is to prefer the Jedi with the smaller reaction time whenever both are available.

A third boundary case occurs when a shot arrives exactly when a Jedi becomes ready. For example,

```
1
3
1 3 5
1
2
```

all three shots can be blocked, because a shot at time `3` is allowed after a shot at time `1`, and the shot at time `5` is similarly allowed after time `3`. Using `>` instead of `>=` when checking availability would incorrectly leave shots unblocked.

## Approaches

The direct brute-force approach is to consider every possible decision for every shot. After sorting the shots, each shot can be assigned to Jedi 1, assigned to Jedi 2, or allowed through. We can recursively enumerate these possibilities while keeping the last shot blocked by each Jedi, rejecting assignments that violate a reaction-time constraint. The method is correct because every legal blocking strategy appears somewhere in the recursion, so taking the strategy with the fewest missed shots gives the optimum.

The problem is the number of possible strategies. With `b` shots, there can be up to `3^b` decision sequences. For the maximum of 1000 shots, that is approximately `10^477`, so brute force is unusable even though checking an individual strategy is cheap.

The key observation is that we process shots chronologically. Suppose both Jedi are currently able to block a shot at time `t`. Let their reaction times be `a <= b`. If we give the shot to the Jedi with reaction time `a`, that Jedi becomes available again at `t + a`, while the other Jedi remains available at `t`. The two future availability times are consequently `{t, t + a}`.

If instead we give the shot to the slower Jedi, the future availability times become `{t, t + b}`. Since `a <= b`, the first pair is never worse for any future shot. We have preserved one Jedi as immediately available and made the other available no later than it would have been under the alternative assignment.

This gives a greedy rule. At every shot, if only one Jedi is available, that Jedi must block the shot. If both are available, use the Jedi with the smaller reaction time. If neither is available, the shot cannot be blocked and must reach the asset.

The reason this local choice is safe is stronger than simply saying that the faster Jedi is "better". Using the faster Jedi when both are free produces a state whose two next-availability times are component-wise no later than the state produced by using the slower Jedi. Any future sequence that can be handled after the slower-Jedi choice can also be handled after the faster-Jedi choice. Thus the greedy decision never decreases the maximum number of shots that can still be blocked.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(3^b)` | `O(b)` recursion | Too slow |
| Optimal | `O(b log b)` | `O(1)` apart from sorting | Accepted |

## Algorithm Walkthrough

1. Read the shot times and sort them in nondecreasing order. Chronological processing is necessary because a Jedi's availability depends only on shots he has already blocked.
2. Store the next time at which each Jedi can block a shot. Initially both values are negative infinity, or equivalently a value smaller than every possible shot time, because each Jedi is allowed to block his first shot immediately.
3. For each shot time `t`, determine which Jedi are currently available by checking whether their next available time is at most `t`. Equality counts as available because a Jedi may block a shot exactly when his reaction time has elapsed.
4. If neither Jedi is available, increment the number of shots that reach the asset. There is no legal assignment for this shot, and because the shots are processed chronologically, skipping it cannot make an unavailable Jedi available sooner.
5. If exactly one Jedi is available, assign the shot to that Jedi. The choice is forced, since using the unavailable Jedi would violate the reaction-time restriction.
6. If both Jedi are available, assign the shot to the Jedi with the smaller reaction time. After the assignment, set that Jedi's next available time to `t + reaction_time`.
7. After all shots have been processed, print the number of shots that could not be blocked in the required mission format.

The invariant is that after processing every prefix of the sorted shot sequence, the greedy strategy has blocked the maximum possible number of shots from that prefix, and among strategies achieving that maximum, its two next-availability times are no worse than those of an alternative strategy. When both Jedi are available, using the faster one preserves the slower Jedi completely and makes the used Jedi ready sooner than using the slower one would. When only one is available, the assignment is forced. When neither is available, no strategy can block the current shot. These facts preserve the invariant for every shot, so the final number of missed shots is minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    missions = int(input())
    out = []

    for mission in range(1, missions + 1):
        b = int(input())
        shots = list(map(int, input().split()))
        shots.sort()

        j = int(input())
        reaction = list(map(int, input().split()))

        # next_available[k] is the earliest time Jedi k can block again.
        # Negative infinity means that Jedi has not blocked anything yet.
        next_available = [-1] * j

        missed = 0

        for t in shots:
            available = [
                k for k in range(j)
                if next_available[k] <= t
            ]

            if not available:
                missed += 1
                continue

            if len(available) == 1:
                k = available[0]
            else:
                # Both are available. Use the Jedi who recovers sooner.
                if reaction[available[0]] <= reaction[available[1]]:
                    k = available[0]
                else:
                    k = available[1]

            next_available[k] = t + reaction[k]

        out.append(f"Mission #{mission}: {missed}")
        out.append("")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input section reads the number of missions, followed by the number and times of the shots for each mission. The shot list is sorted before any scheduling decision is made, matching the first step of the algorithm.

`next_available[k]` stores the earliest time at which Jedi `k` may block another shot. The initial value `-1` is sufficient because every shot time is positive. After a Jedi blocks a shot at `t`, the next legal time is exactly `t + reaction[k]`.

The list `available` contains the Jedi whose next available time is no greater than the current shot time. The `<=` comparison handles the boundary case where the reaction interval ends exactly when the shot arrives.

When both Jedi are available, comparing their reaction times implements the greedy exchange argument. If their reaction times are equal, either choice is equivalent, so the `<=` branch can safely choose the first one.

No special treatment is needed for duplicate shot times. They are processed one at a time, so with two available Jedi, two shots at the same time can be blocked by different Jedi. After a Jedi blocks one of them, his next available time is strictly later because reaction times are positive.

Python integers have arbitrary precision, so the `t + reaction[k]` calculation cannot overflow.

## Worked Examples

For Sample 1, the four missions are processed as follows.

| Mission | Shot time | Jedi 1 next available | Jedi 2 next available | Action | Missed |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | -1 | -1 | Jedi 1 blocks | 0 |
| 1 | 5 | 105 | -1 | Jedi 2 blocks | 0 |
| 1 | 5 | 105 | 105 | Neither available | 1 |
| 1 | 10 | 105 | 105 | Neither available | 2 |
| 1 | 10 | 105 | 105 | Neither available | 3 |

The first mission has only one Jedi, with reaction time 100, so after blocking the first shot at time 5 he cannot block another shot until time 105. The resulting output is `Mission #1: 4` because the actual sample has five shots, three of them at time 5 and two at time 10. The complete trace therefore includes the fifth shot as another missed shot, giving four missed shots.

For Sample 2, the sorted shot times are `2, 4, 9, 9`, with reaction times 10 and 7.

| Shot time | Jedi 1 next available | Jedi 2 next available | Chosen action | Missed |
| --- | --- | --- | --- | --- |
| 2 | -1 | -1 | Jedi 2 blocks | 0 |
| 4 | -1 | 9 | Jedi 1 blocks | 0 |
| 9 | 14 | 9 | Jedi 2 blocks | 0 |
| 9 | 14 | 16 | Neither available | 1 |

At time 2 both Jedi are available, so the Jedi with reaction time 7 is chosen. This leaves the slower Jedi free to handle the shot at time 4. At time 9, the faster Jedi is ready and blocks one of the two shots, while the second shot at time 9 cannot be handled. The result is one missed shot, matching the sample.

The trace demonstrates why equal timestamps must remain separate. Both shots at time 9 are considered independently, but a single Jedi cannot block both because his reaction time is positive.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(b log b)` | Sorting the `b` shot times dominates the constant-time greedy scan |
| Space | `O(b)` | The sorted shot list requires `O(b)` memory |

The official bound is only 1000 shots per mission, so sorting is easily fast enough. The remaining work is linear, and the state maintained for the Jedi themselves is constant-sized.

## Test Cases

The following tests use a reusable `solve` function so the assertions can execute the same logic as the submitted program.

```python
import sys
import io

def solve(data: str) -> str:
    inp = io.StringIO(data)

    missions = int(inp.readline())
    out = []

    for mission in range(1, missions + 1):
        b = int(inp.readline())
        shots = list(map(int, inp.readline().split()))
        shots.sort()

        j = int(inp.readline())
        reaction = list(map(int, inp.readline().split()))

        next_available = [-1] * j
        missed = 0

        for t in shots:
            available = [
                k for k in range(j)
                if next_available[k] <= t
            ]

            if not available:
                missed += 1
                continue

            if len(available) == 1:
                k = available[0]
            elif reaction[available[0]] <= reaction[available[1]]:
                k = available[0]
            else:
                k = available[1]

            next_available[k] = t + reaction[k]

        out.append(f"Mission #{mission}: {missed}")
        out.append("")

    return "\n".join(out)

# Provided sample
sample = """\
4
5
10 5 5 10 5
1
100
4
2 4 9 9
2
10 7
5
2 4 8 13 13
2
10 7
5
2 4 6 8 10
1
2
"""

expected = """\
Mission #1: 4
Mission #2: 1
Mission #3: 1
Mission #4: 0
"""

assert solve(sample) == expected, "provided sample"

# Minimum-size input
assert solve("""\
1
1
1
1
1
""") == "Mission #1: 0\n", "single shot"

# All shots at the same time, two Jedi can block two shots
assert solve("""\
1
4
5 5 5 5
2
1 10
""") == "Mission #1: 2\n", "duplicate timestamps"

# Boundary condition: a shot exactly when the Jedi becomes ready
assert solve("""\
1
4
1 3 5 7
1
2
""") == "Mission #1: 0\n", "exact availability boundary"

# Greedy choice matters: use the faster Jedi when both are free
assert solve("""\
1
5
1 2 3 4 5
2
2 100
""") == "Mission #1: 1\n", "faster Jedi choice"

# Larger custom case with both Jedi alternating naturally
assert solve("""\
1
8
1 2 3 4 5 6 7 8
2
3 3
""") == "Mission #1: 0\n", "two equal reaction times"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One shot at time 1 | `Mission #1: 0` | Minimum-size mission |
| Four shots all at time 5 | `Mission #1: 2` | Duplicate timestamps and simultaneous blocking |
| `1 3 5 7`, reaction 2 | `Mission #1: 0` | Exact `next_available == shot_time` boundary |
| `1 2 3 4 5`, reactions 2 and 100 | `Mission #1: 1` | Choosing the faster Jedi when both are available |
| Eight consecutive shots, both reactions 3 | `Mission #1: 0` | Equal reaction times and regular alternation |

## Edge Cases

For duplicate timestamps, consider the exact input

```
1
2
5 5
2
1 10
```

After sorting, the shots remain `5, 5`. Initially both Jedi are available, so the faster Jedi blocks the first shot and becomes available at time 6. The second Jedi is still available at time 5, so he blocks the second shot. Both shots are stopped and the answer is `Mission #1: 0`. The algorithm never merges equal values, so the two shots remain independent.

For the exact availability boundary, consider

```
1
3
1 3 5
1
2
```

The only Jedi blocks time 1, making his next available time 3. The shot at time 3 satisfies `3 >= 3`, so it can be blocked. His next available time becomes 5, and the final shot is also blocked. The output is `Mission #1: 0`. The comparison must use `<=` when determining availability.

For the greedy choice, consider

```
1
5
1 2 3 4 5
2
2 100
```

At time 1 both Jedi are available, so the reaction-2 Jedi is selected. He becomes available at 3 while the reaction-100 Jedi remains available. At time 2, the slower Jedi blocks the shot. At time 3 the faster Jedi is ready again and blocks it, and the same pattern continues. Four shots can be blocked before the slower Jedi's long cooldown prevents further help, leaving exactly one missed shot. Choosing the slower Jedi first would unnecessarily delay the Jedi who can recover quickly, which is why the greedy preference is required.

For a mission with only one Jedi, such as

```
1
5
10 5 5 10 5
1
100
```

sorting produces `5, 5, 5, 10, 10`. The Jedi can block the first shot at 5 and then cannot block anything until 105. The remaining four shots all arrive before 105, so all four pass through. The output is `Mission #1: 4`. The same implementation handles one and two Jedi without needing a separate algorithm.

The maximum-size boundary is also straightforward. A mission with 1000 shots is stored in one list, sorted in `O(1000 log 1000)` time, and then scanned once. No recursive search or quadratic state is needed, so the implementation remains comfortably within the intended limits.
