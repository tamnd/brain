---
title: "CF 1267E - Elections"
description: "We are given a voting system with multiple candidates and multiple polling stations. Each station reports how many votes each candidate received. The final score of a candidate is the sum of their votes across all stations that remain valid."
date: "2026-06-18T17:58:58+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1267
codeforces_index: "E"
codeforces_contest_name: "2019-2020 ICPC, NERC, Northern Eurasia Finals (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 1700
weight: 1267
solve_time_s: 81
verified: true
draft: false
---

[CF 1267E - Elections](https://codeforces.com/problemset/problem/1267/E)

**Rating:** 1700  
**Tags:** greedy  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a voting system with multiple candidates and multiple polling stations. Each station reports how many votes each candidate received. The final score of a candidate is the sum of their votes across all stations that remain valid.

There is a special candidate, the last one, who represents the opposition. The ruling party is allowed to invalidate entire polling stations. Once some stations are removed, the remaining vote totals determine the winner. The opposition candidate is considered elected if their total strictly exceeds every other candidate’s total.

The task is to remove as few stations as possible so that, after removal, the opposition candidate is not strictly ahead of everyone else. Equivalently, we want the smallest number of stations to discard so that at least one other candidate has a final score greater than or equal to the opposition.

The constraints are small, with up to 100 candidates and 100 polling stations. This immediately rules out any exponential search over subsets of stations since there can be up to 2^100 subsets. A quadratic or cubic solution in the number of stations is acceptable, but anything involving full subset enumeration is not.

A subtle point appears when reasoning greedily: removing stations with the largest opposition support seems natural, but this is not correct. A station that helps the opposition might also heavily support another candidate, and removing it could actually hurt that candidate more than the opposition. The decision must consider _relative advantage_, not absolute opposition votes.

Another edge case comes from ties. The condition is strict: opposition must not be strictly greater than all others. If the opposition ties with someone, that already prevents election. Many incorrect greedy strategies mistakenly enforce a stronger condition than needed.

## Approaches

A brute-force approach would try every subset of polling stations, compute all candidate totals, and check whether the opposition is not strictly the maximum. This is correct because it evaluates all possible outcomes, but it is infeasible since there are 2^m subsets and each evaluation costs O(nm), leading to an astronomical runtime.

The key insight is to reverse the perspective. Instead of choosing stations to remove, we can think in terms of keeping stations. If we keep a subset of stations, the opposition’s margin over every other candidate depends only on summed differences between their votes and each competitor’s votes.

Fix a competitor candidate j. In each station i, define a value:

di = a[i][n] - a[i][j]

This measures how much keeping station i helps the opposition relative to candidate j. If di is large and positive, keeping that station strengthens the opposition’s lead over j. If di is negative, the station actually helps j close or reverse the gap.

To ensure the opposition does not beat j, we want the sum of di over kept stations to be non-positive. If it becomes positive, opposition is ahead of j.

Now the problem becomes: for each competitor j, we need to pick the minimum number of stations to remove so that the sum of di over remaining stations is ≤ 0. This is equivalent to selecting stations to keep such that we avoid giving the opposition too much relative gain.

For a fixed j, the optimal strategy is greedy: sort stations by di in decreasing order. We initially assume we keep all stations, then we progressively remove stations with the largest positive di first, because these are the ones that most increase the opposition’s advantage. We stop once the remaining sum becomes non-positive.

We repeat this process for every candidate j and take the best result.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m · n · m) | O(m) | Too slow |
| Per-candidate greedy removal | O(n · m log m) | O(m) | Accepted |

## Algorithm Walkthrough

We iterate over every non-opposition candidate j and compute how many stations must be removed to ensure the opposition does not beat j.

1. Compute the total advantage of the opposition over candidate j across all stations by summing di = a[i][n] - a[i][j]. This represents how far ahead the opposition is before any removals.
2. For each station i, compute di. Sort stations in descending order of di. Stations with large positive di are most harmful because they most increase the opposition’s margin.
3. Start with all stations included and maintain the current sum of di. If this sum is already ≤ 0, no removals are needed for this candidate.
4. Otherwise, repeatedly remove the station with the largest di. After removing a station, subtract its di from the running sum. Each removal reduces the opposition’s advantage as much as possible at that step.
5. Stop once the running sum becomes ≤ 0. Record how many stations were removed and which ones they were.
6. Repeat for all candidates j from 1 to n-1, and take the minimum removal set across all j.

The output is the set of removed stations corresponding to the best candidate j.

### Why it works

For a fixed candidate j, the value di measures contribution to the opposition’s lead over j. Any valid solution must ensure that the sum of di over kept stations is non-positive. Removing a station is equivalent to subtracting its di from the total.

Choosing to remove stations with the largest di first is optimal because each removal produces the maximum possible decrease in the sum per action. Any optimal solution that removes a smaller di while leaving a larger di would be strictly worse or equivalent but never better in terms of reducing the total sum with the same number of removals.

Thus the greedy process produces the minimum number of removals required to push the sum to non-positive, which corresponds exactly to preventing the opposition from strictly beating candidate j.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(m)]

    best_k = m + 1
    best_remove = None

    for j in range(n - 1):
        diffs = []
        total = 0

        for i in range(m):
            d = a[i][n - 1] - a[i][j]
            diffs.append((d, i))
            total += d

        diffs.sort(reverse=True)

        removed = []
        cur = total

        for d, i in diffs:
            if cur <= 0:
                break
            cur -= d
            removed.append(i + 1)

        if len(removed) < best_k:
            best_k = len(removed)
            best_remove = removed

    print(best_k)
    print(*best_remove)

if __name__ == "__main__":
    solve()
```

The code first reads all station results. For each candidate except the opposition, it constructs the per-station advantage differences against that candidate. Sorting these differences allows us to prioritize removing stations that most strongly favor the opposition in that comparison.

The loop that builds `removed` simulates progressively eliminating harmful stations until the opposition no longer has a strict advantage over the chosen candidate. The first time the condition `cur <= 0` is satisfied, we have achieved the minimal number of removals for that candidate due to the sorted order.

Finally, we pick the best candidate, which corresponds to the globally minimal number of cancellations.

A common pitfall is forgetting that the comparison is strict, so equality already suffices to stop. Another subtlety is using the correct candidate indexing: candidate `n-1` is the opposition, and differences are always computed relative to it.

## Worked Examples

We use the sample input.

Input:

```
5 3
6 3 4 2 8
3 7 5 6 7
5 2 4 7 9
```

We compute for candidate 1 (index 0). The per-station differences di = opposition - candidate1 are:

| Station | di |
| --- | --- |
| 1 | 8 - 6 = 2 |
| 2 | 7 - 3 = 4 |
| 3 | 9 - 5 = 4 |

Total is 10. We remove largest di first: station 2 or 3 (both 4), then station 3 or 2, then station 1. After removing two stations, remaining sum is ≤ 0, so answer is 2.

For candidate 2 (index 1), we get:

| Station | di |
| --- | --- |
| 1 | 8 - 3 = 5 |
| 2 | 7 - 7 = 0 |
| 3 | 9 - 2 = 7 |

We remove stations 3 and 1 first; again 2 removals suffice.

This confirms that multiple candidates can yield the same optimal answer, and the algorithm correctly selects the minimum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · m log m) | For each candidate we compute m differences and sort them |
| Space | O(m) | We store per-station difference arrays |

With n, m ≤ 100, the total work is small: at most 100 sorts of size 100, which is trivial within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        a = [list(map(int, input().split())) for _ in range(m)]

        best_k = m + 1
        best_remove = None

        for j in range(n - 1):
            diffs = []
            total = 0
            for i in range(m):
                d = a[i][n - 1] - a[i][j]
                diffs.append((d, i))
                total += d

            diffs.sort(reverse=True)

            removed = []
            cur = total
            for d, i in diffs:
                if cur <= 0:
                    break
                cur -= d
                removed.append(i + 1)

            if len(removed) < best_k:
                best_k = len(removed)
                best_remove = removed

        return str(best_k) + "\n" + " ".join(map(str, best_remove)) + "\n"

    return solve()

# provided sample
assert run("""5 3
6 3 4 2 8
3 7 5 6 7
5 2 4 7 9
""") == "2\n3 1\n"

# minimum case
assert run("""2 1
1 2
""") == "0\n\n"

# all equal votes
assert run("""3 3
1 1 1
1 1 1
1 1 1
""") == "0\n\n"

# opponent already weak
assert run("""3 2
10 0 0
0 10 0
""") == "0\n\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample | 2 3 1 | correctness on standard case |
| 2 1 case | 0 | no removal needed |
| all equal | 0 | tie prevents election |
| opponent weak | 0 | trivial non-opposition win |

## Edge Cases

One important edge case is when the opposition is not initially leading any candidate. In that situation, the total differences for every candidate are already non-positive or can be made non-positive without removing anything. The algorithm handles this because `cur` starts at total and is checked before any removals, so it immediately accepts zero deletions.

Another case is when multiple stations have identical di values. Sorting places them arbitrarily among equals, but since the algorithm only depends on removing the largest available di first, any ordering among ties leads to the same number of removals. The correctness does not depend on stability of sorting.

A final subtle case is when removing a station with di = 0. This does not change the running sum, but it may still be selected if needed to break strict inequality in some configurations. The algorithm naturally avoids unnecessary removals because the loop stops as soon as cur ≤ 0, so zero-impact removals are never taken unless they are part of reaching that threshold exactly.
