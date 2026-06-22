---
title: "CF 105321F - Fixture"
description: "We are given a chronological record of tennis matches played by a single player. Each match results in either a win or a loss, encoded as a binary array where 1 represents a win and 0 represents a loss. The scoring system has two independent components."
date: "2026-06-22T10:52:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105321
codeforces_index: "F"
codeforces_contest_name: "2024 Argentinian Programming Tournament (TAP)"
rating: 0
weight: 105321
solve_time_s: 43
verified: true
draft: false
---

[CF 105321F - Fixture](https://codeforces.com/problemset/problem/105321/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a chronological record of tennis matches played by a single player. Each match results in either a win or a loss, encoded as a binary array where 1 represents a win and 0 represents a loss.

The scoring system has two independent components. The first is straightforward: every win contributes +1 point and every loss contributes −1 point. The second depends on streaks: whenever a match ends and the player is currently in a streak of at least three consecutive wins that includes this match, they receive an additional +1 point for that moment.

The key subtlety is that this streak bonus is evaluated after each match, not just at the end. So a streak of four wins contributes multiple bonuses, one for each position where the suffix ending at that match has length at least three.

The input size is small, with N up to 100, which immediately allows a direct linear scan without any concern for optimization beyond O(N). Even an O(N^2) simulation would be acceptable, but the structure of the problem clearly allows O(N).

A naive mistake would be to only check whether there exists any streak of length at least three and add a single bonus per streak. For example, for input `1 1 1 1`, the correct bonus is 2 (at positions 3 and 4), but a naive implementation might incorrectly add only 1.

Another common mistake is to count streaks globally rather than per position. For example, in `1 1 1 0 1 1 1`, the second streak again contributes multiple bonuses independently of the first.

The correct interpretation is strictly local: after each match i, we check whether the last three matches (i-2 to i) are all wins, and if so we add one bonus point.

## Approaches

A brute-force way to think about the problem is to simulate the scoring rule literally. For each position i, we compute the current streak of consecutive wins ending at i by scanning backwards until a loss is encountered. If that streak length is at least 3, we add a bonus.

This works because it directly matches the definition, but it can degrade to O(N^2) in the worst case when all matches are wins. Each position would scan back O(N) steps.

However, the observation that changes everything is that we do not actually need the full streak length. The bonus condition depends only on whether the last three matches are wins. If positions i, i−1, and i−2 exist and are all 1, then the player receives exactly one bonus at position i. This converts a potentially unbounded backward scan into a constant-time check per position.

So the problem reduces to a simple sliding window of size three over a binary array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force backward scan | O(N^2) | O(1) | Too slow (unnecessary) |
| Optimal sliding check | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We process the matches from left to right while maintaining the total score.

1. Initialize the answer to zero. This variable accumulates both win/loss points and streak bonuses.
2. Iterate over each match i from 0 to N−1. For each match, update the score by adding +1 if the result is a win and −1 if it is a loss. This directly encodes the base scoring rule.
3. If i ≥ 2, check whether Ri, Ri−1, and Ri−2 are all equal to 1. This check determines whether the current match completes a streak of at least three consecutive wins ending at i.
4. If the condition holds, add an additional +1 point to the answer. This corresponds exactly to the rule that each qualifying endpoint contributes one bonus independently.

After processing all matches, the accumulated value is the final score.

### Why it works

The algorithm relies on the fact that the bonus rule depends only on whether a window of length three ending at position i consists entirely of wins. Any longer streak automatically triggers this condition at every suffix endpoint starting from the third win onward. Therefore, counting each valid length-3 window exactly once is equivalent to counting all eligible streak endpoints. The base score is independent of this condition, so separating the two contributions preserves correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    ans = 0
    
    for i in range(n):
        if a[i] == 1:
            ans += 1
        else:
            ans -= 1
        
        if i >= 2 and a[i] == 1 and a[i-1] == 1 and a[i-2] == 1:
            ans += 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution keeps a single running accumulator. The first update inside the loop handles the linear scoring rule directly. The second conditional block is the sliding-window check for three consecutive wins, applied only when there are at least three matches processed.

The critical implementation detail is the order: we first apply the base score for the current match, then evaluate the streak ending at that position. This ensures that the streak check always includes the current match.

## Worked Examples

### Example 1: alternating results

Input:

```
8
1 0 1 0 1 0 1 0
```

We track score evolution:

| i | result | base change | streak (last 3) | bonus | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | +1 | no | 0 | 1 |
| 1 | 0 | −1 | no | 0 | 0 |
| 2 | 1 | +1 | no | 0 | 1 |
| 3 | 0 | −1 | no | 0 | 0 |
| 4 | 1 | +1 | no | 0 | 1 |
| 5 | 0 | −1 | no | 0 | 0 |
| 6 | 1 | +1 | no | 0 | 1 |
| 7 | 0 | −1 | no | 0 | 0 |

Final answer is 0.

This confirms that isolated wins never trigger the bonus, even if there are multiple separated occurrences.

### Example 2: full win streak

Input:

```
5
1 1 1 1 1
```

| i | result | base change | streak (last 3) | bonus | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | +1 | no | 0 | 1 |
| 1 | 1 | +1 | no | 0 | 2 |
| 2 | 1 | +1 | yes | +1 | 4 |
| 3 | 1 | +1 | yes | +1 | 6 |
| 4 | 1 | +1 | yes | +1 | 8 |

This demonstrates that once a streak reaches length 3, every subsequent match inside the streak contributes an additional bonus.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Single pass over the array with constant-time checks per index |
| Space | O(1) | Only a few scalar variables are used beyond the input array |

The constraints N ≤ 100 make this easily within limits, but the solution is already optimal and scales far beyond the given bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("8\n1 0 1 0 1 0 1 0\n") == "0"
assert run("5\n0 0 0 0 0\n") == "-5"
assert run("5\n1 1 1 1 1\n") == "8"

# custom tests
assert run("3\n1 1 1\n") == "4", "single minimal streak"
assert run("2\n1 1\n") == "2", "no bonus possible"
assert run("4\n1 1 1 0\n") == "2", "streak breaks early"
assert run("6\n1 1 1 1 0 1\n") == "4", "multiple streak interaction"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 ones | 4 | minimal triggering of bonus |
| 2 ones | 2 | boundary where bonus cannot apply |
| 3 ones then loss | 2 | early termination of streak |
| mixed sequence | 4 | reset behavior after break |

## Edge Cases

For the minimal input `N = 1`, say input `1`, the algorithm sets base score to +1 and never enters the streak check since i < 2. The output is 1, which is correct because no streak of length 3 can exist.

For a full loss sequence like `0 0 0 0`, each position contributes −1 and there are no streaks. The score becomes −4, matching the rule since the bonus condition is never triggered.

For a long win streak such as `1 1 1 1 1`, the implementation correctly adds bonuses at indices 2, 3, and 4. Tracing explicitly, at i = 2, 3, 4 the triple-window condition holds, producing exactly three bonus increments. This confirms that overlapping streak contributions are handled independently per position rather than being grouped into a single event.
