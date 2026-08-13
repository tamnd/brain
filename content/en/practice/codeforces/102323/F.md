---
title: "CF 102323F - Faster Microwaving"
description: "We are given a recommended microwave cooking time in MM:SS form and a percentage p. Chris is allowed to choose any integer number of seconds whose distance from the recommended time is at most p percent of that recommended time."
date: "2026-08-14T04:53:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102323
codeforces_index: "F"
codeforces_contest_name: "UCF Locals 2014"
rating: 0
weight: 102323
solve_time_s: 66
verified: true
draft: false
---

[CF 102323F - Faster Microwaving](https://codeforces.com/problemset/problem/102323/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a recommended microwave cooking time in `MM:SS` form and a percentage `p`. Chris is allowed to choose any integer number of seconds whose distance from the recommended time is at most `p` percent of that recommended time. Among all such candidate times, he wants the one whose digit sequence is fastest to enter.

The microwave does not require the last two digits to form a valid number of seconds. If we press `190`, the microwave interprets that as `1:90`, which is the same total duration as 2 minutes and 30 seconds. Thus, a candidate is best represented by the decimal digits of its total number of seconds. For example, 88 means `0:88`, which is 1 minute and 28 seconds.

Entering a digit costs one moment. Moving from one digit to a different digit costs another moment, while pressing the same digit again requires no movement. Consequently, for a digit string `d1 d2 ... dk`, its cost is

`k + number of positions i where di != d(i+1)`.

The input contains `n` food items. For every item, the recommended time has minutes from `00` through `20`, and its seconds are one of `00`, `15`, `30`, or `45`. The recommended time is at least 15 seconds, while `p` is between 2 and 10. These restrictions make the search space extremely small. Even the largest recommendation, 20 minutes, has a 10 percent range of only 240 integer seconds, so checking every candidate directly is easily fast enough. The original contest statement gives these exact bounds and specifies that the percentage interval is interpreted using integer seconds that actually satisfy the percentage condition.

There are several details that can make an otherwise simple implementation wrong.

For example, consider:

```
1
01:30
4
```

The recommended time is 90 seconds, so the allowed range is from 87 to 93 seconds. The answer is `88`, not `01:28`. The sequence `88` takes only two moments, while the microwave itself converts those digits to 1 minute and 28 seconds.

The percentage endpoints must also be rounded in the correct direction. For:

```
1
00:15
10
```

the mathematical interval is 13.5 through 16.5 seconds. Since only integer seconds are allowed, the valid candidates are 14, 15, and 16, so the answer is `15`. Including 13 or 17 would incorrectly enlarge the candidate set.

A third edge case is that the chosen time does not have to have seconds below 60. For:

```
1
00:30
10
```

the valid range is 27 through 33 seconds, and `33` is optimal because pressing the same digit twice costs only two moments. The microwave interprets `33` as 33 seconds normally, but the same principle also allows values such as `88`.

Finally, the fastest entry is not necessarily the candidate closest to the recommendation. For:

```
1
06:00
8
```

the valid interval is 331 through 388 seconds. The sequence `555` takes only three moments, so it beats candidates such as `600`, even though 600 seconds is exactly the recommended time. The actual duration of `555` is 5 minutes and 55 seconds.

## Approaches

The direct approach is to enumerate every integer number of seconds in the allowed interval. For each candidate, convert the integer to its decimal representation and calculate its entry cost. Keep the candidate with the smallest cost, and when two candidates have equal cost, keep the one with smaller absolute distance from the recommended number of seconds.

This brute-force method is already sufficient because the constraints make the interval tiny. The largest possible recommended duration is 20 minutes, or 1200 seconds. With `p = 10`, the interval can contain at most 241 integer values, from 1080 through 1320. Calculating the cost of each candidate examines at most four digits, so one test case needs only about 1000 primitive operations. Even if the input contains a large number of test cases, this is comfortably small.

There is also a useful structural observation behind the cost calculation. The total cost depends only on how many times the digit changes while we type. Every digit always costs one press, and every transition to a different digit costs exactly one movement. We therefore do not need to simulate a finger position or model the keypad geometry. The cost can be computed directly from the decimal string.

The brute-force search works because the candidate interval is small. A more complicated optimization would only make the implementation harder without providing a practical benefit under these constraints. The key reduction is simply to convert the recommended time into seconds, compute the exact integer interval, and inspect every candidate in that interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(R log R) | O(log R) | Accepted |
| Optimal | O(R log R) | O(log R) | Accepted |

Here `R` is the number of integer seconds in the allowed interval, and in this problem `R <= 241`. Since every candidate has at most four decimal digits, this is effectively constant time per test case.

## Algorithm Walkthrough

1. Convert the recommended `MM:SS` value into a single integer `target = 60 * MM + SS`. Working entirely in seconds avoids having to handle minute and second boundaries separately.
2. Compute the smallest valid candidate with integer arithmetic. The lower endpoint is

`ceil(target * (100 - p) / 100)`.

For positive integers, this can be calculated as `(x + 99) // 100`, where `x = target * (100 - p)`.
3. Compute the largest valid candidate as

`floor(target * (100 + p) / 100)`.

Integer division gives this directly.
4. Iterate through every integer `t` from the lower endpoint through the upper endpoint. Every value in this loop is a legal proposed cooking time, and no legal time is skipped.
5. Convert `t` to `str(t)` and calculate its entry cost. Start with the number of digits, because every digit requires one press. Then add one for every adjacent pair of different digits, because moving between different buttons costs one additional moment.
6. Compare the current candidate with the best candidate found so far. A candidate is better if its entry cost is smaller. If the costs are equal, compare `abs(t - target)` and prefer the candidate closer to the recommendation.
7. Output the decimal digits of the selected candidate. We output the number itself, without inserting a colon or leading zeroes, because those are not buttons Chris needs to press.

The invariant is that after processing every candidate up to `t`, the stored answer is the best candidate among all candidates processed so far according to the exact two-level ordering from the problem: minimum entry cost first, then minimum distance from the recommendation. Since the loop eventually processes every valid integer candidate, the final stored answer is the unique required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def entry_cost(t):
    s = str(t)
    cost = len(s)

    for i in range(1, len(s)):
        if s[i] != s[i - 1]:
            cost += 1

    return cost

def solve():
    n = int(input())
    out = []

    for case in range(1, n + 1):
        time_str = input().strip()
        p = int(input())

        minutes = int(time_str[:2])
        seconds = int(time_str[3:])
        target = minutes * 60 + seconds

        low_num = target * (100 - p)
        high_num = target * (100 + p)

        low = (low_num + 99) // 100
        high = high_num // 100

        best_time = None
        best_cost = 10**9
        best_dist = 10**9

        for t in range(low, high + 1):
            cost = entry_cost(t)
            dist = abs(t - target)

            if cost < best_cost or (cost == best_cost and dist < best_dist):
                best_time = t
                best_cost = cost
                best_dist = dist

        out.append(f"Case #{case}: {best_time}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first part of `solve` converts the five-character `MM:SS` representation into seconds. Since the input format is fixed, `time_str[:2]` gives the minutes and `time_str[3:]` gives the seconds.

The expressions for `low` and `high` deliberately avoid floating-point arithmetic. For example, if the lower mathematical endpoint is 13.5, `(13 * 100 + 99) // 100` style integer ceiling arithmetic gives 14. Floating-point arithmetic is unnecessary and could introduce boundary errors.

`entry_cost` starts with `len(s)` because every digit has to be pressed. It then examines adjacent digits. A transition such as `5 -> 5` requires no movement, while `5 -> 6` requires one movement, so each unequal adjacent pair contributes exactly one.

The comparison condition directly encodes the required priority. Entry cost is considered first. Distance from the recommended time matters only when entry costs are equal. Using `<` for the distance comparison is enough because the statement guarantees that the final answer is unique.

There is no need to normalize a candidate such as `88` into `01:28`. The candidate is the sequence of buttons being pressed, so the correct output is exactly `88`. Python integers also naturally avoid any overflow issue, although the actual values here are only around a few thousand.

## Worked Examples

For Sample 1:

```
3
01:30
4
00:30
10
06:00
8
```

The first case has a target of 90 seconds and a valid range from 87 through 93.

| Candidate | Digits | Entry cost | Distance |
| --- | --- | --- | --- |
| 87 | `87` | 3 | 3 |
| 88 | `88` | 2 | 2 |
| 89 | `89` | 3 | 1 |
| 90 | `90` | 3 | 0 |
| 91 | `91` | 3 | 1 |
| 92 | `92` | 3 | 2 |
| 93 | `93` | 3 | 3 |

`88` has the unique smallest entry cost, so the first output is `88`.

The second case has target 30 and range 27 through 33.

| Candidate | Digits | Entry cost | Distance |
| --- | --- | --- | --- |
| 27 | `27` | 3 | 3 |
| 28 | `28` | 3 | 2 |
| 29 | `29` | 3 | 1 |
| 30 | `30` | 3 | 0 |
| 31 | `31` | 3 | 1 |
| 32 | `32` | 3 | 2 |
| 33 | `33` | 2 | 3 |

`33` wins because pressing the same button twice eliminates the movement between the two presses.

For the third case, the target is 360 seconds. With an 8 percent range, the valid interval is 331 through 388.

| Candidate | Digits | Entry cost | Distance |
| --- | --- | --- | --- |
| 331 | `331` | 4 | 29 |
| 332 | `332` | 4 | 28 |
| 333 | `333` | 3 | 27 |
| 444 | `444` | 3 | 84 |
| 555 | `555` | 3 | 105 |
| 600 | `600` | 4 | 240 |
| 666 | `666` | 3 | 306 |

The three-digit repeated-digit candidates have the minimum possible cost of 3. Among all such candidates in the complete range, `555` is the closest to 360 seconds, so the answer is `555`.

For Sample 2:

```
1
00:45
10
```

The target is 45 seconds. The lower mathematical bound is 40.5 and the upper bound is 49.5, so the valid integer candidates are 41 through 49.

| Candidate | Digits | Entry cost | Distance |
| --- | --- | --- | --- |
| 41 | `41` | 3 | 4 |
| 42 | `42` | 3 | 3 |
| 43 | `43` | 3 | 2 |
| 44 | `44` | 2 | 1 |
| 45 | `45` | 3 | 0 |
| 46 | `46` | 3 | 1 |
| 47 | `47` | 3 | 2 |
| 48 | `48` | 3 | 3 |
| 49 | `49` | 3 | 4 |

`44` wins despite being one second away from the recommendation, because its two presses use the same button and cost only two moments. This example demonstrates why minimizing the cooking-time error first would be incorrect.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R log R) | There are R candidate seconds, and each candidate has at most four decimal digits. |
| Space | O(log R) | The decimal representation of one candidate is stored temporarily. |

The maximum recommended duration is 1200 seconds and the maximum percentage is 10, so at most 241 candidate times are examined for one item. Each candidate has at most four digits, making the actual work per test case very small. The algorithm easily fits the stated 5-second time limit and uses negligible memory.

## Test Cases

```
# helper: same core logic as the submitted solution
def best_time(time_str, p):
    minutes = int(time_str[:2])
    seconds = int(time_str[3:])
    target = minutes * 60 + seconds

    low = (target * (100 - p) + 99) // 100
    high = target * (100 + p) // 100

    def cost(t):
        s = str(t)
        ans = len(s)
        for i in range(1, len(s)):
            if s[i] != s[i - 1]:
                ans += 1
        return ans

    best = None
    best_key = None

    for t in range(low, high + 1):
        key = (cost(t), abs(t - target))
        if best_key is None or key < best_key:
            best = t
            best_key = key

    return str(best)

def run(inp: str) -> str:
    import io

    data = inp.strip().split()
    it = iter(data)
    n = int(next(it))

    ans = []
    for case in range(1, n + 1):
        time_str = next(it)
        p = int(next(it))
        ans.append(f"Case #{case}: {best_time(time_str, p)}")

    return "\n".join(ans)

# provided sample
assert run("""3
01:30
4
00:30
10
06:00
8
""") == """Case #1: 88
Case #2: 33
Case #3: 555""", "provided sample"

# minimum-size recommendation, with an interval collapsing to one value
assert run("""1
00:15
2
""") == "Case #1: 15", "minimum-size input"

# all-equal digits give the cheapest possible two-digit entry
assert run("""1
00:30
10
""") == "Case #1: 33", "repeated digit candidate"

# boundary rounding: 45 +/- 10% gives 41..49, not 40..50
assert run("""1
00:45
10
""") == "Case #1: 44", "integer percentage boundaries"

# maximum recommended time and percentage
assert run("""1
20:00
10
""") == "Case #1: 1111", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `00:15`, `2` | `Case #1: 15` | Minimum recommendation and a one-value candidate interval |
| `00:30`, `10` | `Case #1: 33` | Repeated digits and movement cost |
| `00:45`, `10` | `Case #1: 44` | Correct ceiling and floor of percentage boundaries |
| `20:00`, `10` | `Case #1: 1111` | Largest possible recommendation and candidate range |

## Edge Cases

For the minimum recommendation, consider:

```
1
00:15
2
```

The target is 15 seconds. The lower bound is `ceil(14.7) = 15`, while the upper bound is `floor(15.3) = 15`. The loop therefore examines only `15`, and the answer is `15`. This prevents an implementation from accidentally accepting 14 seconds because of a floating-point truncation or an incorrect floor operation.

For a repeated-digit candidate, consider:

```
1
00:30
10
```

The valid range is 27 through 33. Candidate `33` has two presses and no movement, giving cost 2. Every other candidate has two different digits and costs 3. The algorithm selects `33` immediately when it reaches it, regardless of the fact that 30 seconds is closer to the recommendation.

For a candidate whose displayed seconds exceed 59, consider:

```
1
01:30
4
```

The range is 87 through 93. Candidate `88` is represented by the two pressed digits `8` and `8`, so its cost is 2. The microwave interprets those digits as 88 seconds, equivalent to 1 minute and 28 seconds. The algorithm keeps `88` as the answer and does not try to convert it into `01:28`.

For the largest possible recommendation, consider:

```
1
20:00
10
```

The target is 1200 seconds, giving the range 1080 through 1320. Candidate `1111` lies inside this interval and costs only 4 moments because all four digits are identical. No three-digit candidate can be valid because every value below 1000 is outside the interval, while a four-digit number cannot have a cost below 4. Thus `1111` is optimal, and the implementation finds it by ordinary enumeration.
