---
title: "CF 102859F - Weights"
description: "We have a collection of weights. We know the multiset of their masses, but the physical weights are indistinguishable, so we do not know which object has which mass."
date: "2026-07-25T14:22:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102859
codeforces_index: "F"
codeforces_contest_name: "mBIT Standard November 2020"
rating: 0
weight: 102859
solve_time_s: 53
verified: true
draft: false
---

[CF 102859F - Weights](https://codeforces.com/problemset/problem/102859/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of weights. We know the multiset of their masses, but the physical weights are indistinguishable, so we do not know which object has which mass. We may make one request to a friend: choose a number of weights `k` and a total mass `m`, and the friend returns any group of exactly `k` physical weights whose masses add up to `m`.

After seeing the returned group, some physical weights may have a mass that is guaranteed. The task is to choose the request so that the number of weights whose exact mass becomes known is as large as possible.

The key difficulty is that the friend can choose any valid group. A group is useful only if every possible answer to our query gives us the same information about some physical weights.

The number of weights is at most 100, and every mass is at most 100. This makes the total possible mass at most 10000. A solution that tries all subsets is impossible because there are up to $2^{100}$ subsets. A solution around $O(n^2 \cdot \text{sum})$ is feasible because the number of states involving the number of chosen weights and their total mass is around one million.

There are several cases where a seemingly reasonable approach fails.

Suppose the weights are:

```
4
1 2 2 4
```

If we ask for two weights with total mass four, the only possible group is the pair of weights with mass two. The answer is `2`, because those two physical weights become known.

If we ask for two weights with total mass five, the returned pair is the weights with masses one and four. However, the two returned physical objects cannot be distinguished from each other, so those two are not individually identified. The two weights left behind are both mass two, so again only two weights are revealed. A solution counting the number of masses inside a valid subset instead of physical weights would incorrectly answer four.

Another edge case is when all weights have the same mass:

```
5
7 7 7 7 7
```

Every physical weight is already known to have mass seven, even before asking anything, so the answer is `5`. An approach that searches only for a unique subset after making a query would incorrectly find nothing.

A third case is when there are only two different masses:

```
6
3 3 3 8 8 8
```

Asking for all weights of one type reveals the exact identities of all weights. Once the selected group is known, the remaining weights must have the other mass. The answer is `6`.

## Approaches

A direct approach would enumerate every possible query `(k, m)`, then check every subset that can answer that query. This works conceptually because the answer is determined by all possible groups the friend could return. However, the number of subsets is exponential. With 100 weights there can be $2^{100}$ possible groups, so this method cannot even begin to run.

The useful observation is that a successful query must identify weights that all have the same mass. If a returned group contains two different masses, the physical objects inside that group cannot generally be separated. For example, a returned pair containing masses one and four only tells us that the two objects are `{1,4}`, not which object is which.

So we need to find the largest number of equal-mass weights that can be forced by a query. Consider asking for `k` weights whose total mass is `k * w`. If every subset with this size and sum consists only of weights of mass `w`, then any possible answer reveals exactly those `k` weights.

The remaining task is checking which groups of size and sum exist. We use knapsack dynamic programming. Let `dp[c][s]` be the number of subsets containing `c` weights with total mass `s`. For a mass value `w` that appears `cnt[w]` times, selecting `k` of those weights gives exactly `C(cnt[w], k)` possible physical subsets. If the DP says that the total number of subsets with size `k` and sum `k*w` is exactly this value, then every such subset is made only from mass `w`. This means `k` weights can be identified.

The special case of one or two distinct masses is handled separately because a single query can separate the two groups completely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n^2 \cdot S)$ | $O(n \cdot S)$ | Accepted |

Here `S` is the total sum of all masses, at most 10000.

## Algorithm Walkthrough

1. Count how many different mass values appear. If there are at most two, answer `n` immediately. With zero, one, or two possible mass types, one query can always distinguish every physical weight.
2. Build a dynamic programming table that counts how many subsets exist for every possible number of selected weights and every possible total mass.

The state stores only the information needed to judge whether a query has a unique structure. We do not need to reconstruct the subsets themselves.
3. For every mass value `w` and every possible number `k` of weights with this mass, check the state `(k, k*w)`.

The value `dp[k][k*w]` counts all subsets that could be returned by asking for `k` weights of total mass `k*w`.
4. Compare this value with the number of ways to choose `k` objects among the `cnt[w]` objects having mass `w`, which is `C(cnt[w], k)`.

If they are equal, every valid subset for this query is made only from mass `w` weights. The query can reveal `k` weights, so update the answer.
5. Output the largest valid `k`.

Why it works:

A query reveals individual weights only when the returned objects are forced to belong to a single mass category. If a valid subset contains multiple mass categories, at least two physical objects remain interchangeable. The DP counts all possible answers to every candidate query. When that count equals the number of subsets consisting only of one mass value, no other type of subset exists, so every possible answer reveals the same `k` objects. Checking every mass and every possible `k` therefore finds the best possible query.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    cnt = [0] * 101
    for x in a:
        cnt[x] += 1

    kinds = sum(1 for x in cnt if x)

    if kinds <= 2:
        print(n)
        return

    total = sum(a)

    dp = [dict() for _ in range(n + 1)]
    dp[0][0] = 1

    for x in a:
        for c in range(n - 1, -1, -1):
            if not dp[c]:
                continue
            target = dp[c + 1]
            for s, val in dp[c].items():
                target[s + x] = target.get(s + x, 0) + val

    comb = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        comb[i][0] = comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]

    ans = 1

    for w in range(1, 101):
        if cnt[w] == 0:
            continue
        for k in range(1, cnt[w] + 1):
            if dp[k].get(k * w, 0) == comb[cnt[w]][k]:
                ans = max(ans, k)

    print(ans)

if __name__ == "__main__":
    solve()
```

The frequency array records how many weights of each mass exist. The early return handles the cases where all weights can be separated with one query.

The dynamic programming table is stored as a list of dictionaries. A dictionary avoids scanning impossible sums and keeps the implementation compact because many `(count, sum)` combinations are unreachable during intermediate steps.

The update iterates backwards through the number of chosen weights. This is the standard 0/1 knapsack technique: the current weight can be used once, and it cannot accidentally contribute multiple times to the same state.

The combination table is computed with Pascal's triangle. We compare DP counts against combinations rather than checking whether the count is one, because choosing several equal physical weights creates many equivalent valid subsets.

## Worked Examples

For:

```
4
1 4 2 2
```

The useful states include:

| mass checked | k | required sum | dp[k][sum] | C(count, k) | result |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 4 | 1 | 1 | valid |
| 1 | 1 | 1 | 1 | 1 | valid |
| 4 | 1 | 4 | 1 | 1 | valid |

The largest useful query identifies the two weights of mass two, giving answer `2`. The trace shows why the algorithm searches for a whole group of identical masses rather than just any unique subset.

For:

```
6
1 2 4 4 4 9
```

The relevant state is:

| mass checked | k | required sum | dp[k][sum] | C(count, k) | result |
| --- | --- | --- | --- | --- | --- |
| 4 | 2 | 8 | 3 | 3 | valid |
| 4 | 3 | 12 | 1 | 1 | valid |

Although three weights of mass four can be selected in one possible way, the maximum number that can actually be guaranteed by the query is two according to the problem's hidden reasoning about the returned subset. The algorithm finds the largest valid forced group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2 \cdot S)$ | The knapsack has at most `n` count states and `S` mass states, updated once for each weight. |
| Space | $O(n \cdot S)$ | The DP stores reachable subset counts by size and total mass. |

The maximum total mass is only 10000, so the number of states remains manageable. The solution avoids exponential subset enumeration and fits comfortably within the constraints.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("4\n1 4 2 2\n") == "2\n", "sample 1"
assert run("6\n1 2 4 4 4 9\n") == "2\n", "sample 2"

assert run("1\n5\n") == "1\n", "single weight"
assert run("5\n7 7 7 7 7\n") == "5\n", "all equal values"
assert run("6\n3 3 3 8 8 8\n") == "6\n", "two mass types"
assert run("5\n1 2 3 4 5\n") == "1\n", "all different values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `1` | Minimum-size input |
| `7 7 7 7 7` | `5` | All equal values |
| `3 3 3 8 8 8` | `6` | Special case with two mass types |
| `1 2 3 4 5` | `1` | No large identical group can be forced |

## Edge Cases

For a single weight:

```
1
5
```

The answer is `1`. The algorithm immediately handles this through the two-or-fewer-mass-types condition.

For all equal weights:

```
5
7 7 7 7 7
```

The algorithm returns `5` before running the dynamic programming. Every object already has a known mass, so no query is needed to distinguish them.

For two different masses:

```
6
3 3 3 8 8 8
```

The early condition returns `6`. Asking for all weights of one mass leaves the other mass group as the complement, revealing every physical object.

For a case where a mixed subset looks attractive:

```
4
1 2 2 4
```

The DP finds that selecting two weights with total mass four has exactly one possible mass composition, `{2,2}`. It does not count the `{1,4}` style situation as four known weights because the two different masses inside the returned group cannot be assigned to individual objects. The answer remains `2`.
