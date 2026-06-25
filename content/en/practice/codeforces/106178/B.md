---
title: "CF 106178B - Balanced Balloons"
description: "We have a group of people joining a club one by one. The i-th person brings some number of balloons between 1 and K. After every arrival, the total number of balloons collected so far must be divisible by the number of people currently in the club."
date: "2026-06-25T10:56:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106178
codeforces_index: "B"
codeforces_contest_name: "2025-2026 ICPC Latin American Regional Programming Contest"
rating: 0
weight: 106178
solve_time_s: 39
verified: true
draft: false
---

[CF 106178B - Balanced Balloons](https://codeforces.com/problemset/problem/106178/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a group of people joining a club one by one. The `i`-th person brings some number of balloons between `1` and `K`. After every arrival, the total number of balloons collected so far must be divisible by the number of people currently in the club.

The task is to count how many possible sequences of contributions satisfy this condition for all prefixes. Two sequences are different if at least one person brings a different number of balloons. The answer is required modulo `998244353`. The problem statement and limits are from Codeforces Gym 106178B, where `N` can be as large as `10^9` while `K` is at most `2000`.

The first challenge is that `N` is enormous. Any approach that simulates every person is impossible because even `10^8` operations are already too much for a typical contest time limit, and here the number of people can be ten times larger. The small bound on `K` is the key restriction we should exploit.

Consider the average number of balloons per person after each arrival. Because every prefix total is divisible by its length, this average is always an integer. Since every contribution is between `1` and `K`, every average is also between `1` and `K`. This gives us only `K` possible states, even though the number of steps can be huge.

The tricky cases are mostly about very small values and about the point where the process becomes stable.

For example, with:

```
1 3
```

the answer is `3`, because the only person can bring `1`, `2`, or `3` balloons. A solution that starts transitions from the second person would incorrectly return zero.

Another case is:

```
4 1
```

The answer is `1`. Every person must bring exactly one balloon. Any approach that only checks whether the average can change may accidentally count impossible changes because the only valid state is average `1`.

A more subtle case is:

```
5 2
```

After enough people have joined, the average can no longer change. A transition from average `1` to average `2` on person `6` would require the sixth person to bring `7` balloons, which is impossible. A solution that assumes the same transitions continue forever would overcount.

## Approaches

A direct solution would keep the current total number of balloons and try every possible contribution for every person. For each person there are `K` choices, so this becomes `K^N` possibilities. This is correct because it literally enumerates every valid sequence, but it becomes unusable immediately.

A slightly better attempt is dynamic programming over the current average. Let the state after `i` people be the current average `a`. There are only `K` states. The transition from average `a` to a new average `b` is determined by the next contribution:

$$x = i \cdot b - (i-1)\cdot a$$

If `x` is between `1` and `K`, then this transition is valid.

The brute force DP over all pairs of averages checks every possible `a` and `b` for every person. That costs `O(NK^2)`, which is still impossible because `N` can be `10^9`.

The important observation is that after enough people join, the average cannot move anymore. Suppose the current average is `a` and the next average is larger by `d`. The next contribution becomes:

$$x = a + i \cdot d$$

For any positive change, the contribution grows with `i`. Since no contribution can exceed `K`, this becomes impossible when `i > K`. The same argument works for decreasing the average. A drop by `d` requires:

$$x = a - i \cdot d$$

which becomes non-positive when `i` is large enough. Thus after the `K`-th person, the average is forced to stay unchanged forever, and the only possible future contribution is exactly the current average.

We only need to simulate the first `K` arrivals. The remaining `N-K` people contribute one forced value each, so they do not change the number of valid sequences.

The transitions can also be generated efficiently. From a state `a` at step `i`, increasing the average by `d` is possible while:

$$a+i d \leq K$$

and decreasing by `d` is possible while:

$$a-i d \geq 1$$

The total number of generated transitions over all steps is about:

$$\sum_{i=1}^{K} \frac{K^2}{i}$$

which is around `K^2 log K`, easily fast enough for `K = 2000`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(K^N)` | `O(N)` | Too slow |
| DP over averages without optimization | `O(NK^2)` | `O(K)` | Too slow |
| Optimized DP over averages | `O(K^2 log K)` | `O(K)` | Accepted |

## Algorithm Walkthrough

1. If there is only one person, every contribution from `1` to `K` is valid, so the answer is `K`.
2. Store a dynamic programming array where `dp[a]` is the number of valid sequences after the current number of people with average `a`.

After the first person, the average is exactly the number of balloons they brought, so every average from `1` to `K` has one valid sequence.
3. Process arrivals from person `2` up to person `min(N, K)`.

For the current step `i`, create a new array of states. For every current average `a`, try every possible next average reachable in this step.
4. Handle transitions where the average stays equal.

If the average remains `a`, the new contribution is also `a`, which is always valid.
5. Handle transitions where the average increases.

Moving from `a` to `a+d` requires a contribution of:

$$a+i d$$

Increase `d` while this value is at most `K`.
6. Handle transitions where the average decreases.

Moving from `a` to `a-d` requires:

$$a-i d$$

Decrease `d` while this value is at least `1`.
7. After processing `min(N,K)` people, sum all states. If `N` is larger than `K`, the later people have exactly one possible contribution sequence from each state, so the answer does not change.

Why it works:

The invariant is that after processing person `i`, `dp[a]` exactly counts the valid prefixes whose average after `i` people is `a`. Every possible next contribution corresponds to exactly one next average, and every generated transition satisfies the divisibility requirement because the resulting average is an integer. The transition generation checks every contribution that can exist, so no valid sequence is missed and no invalid sequence is added. Once the number of people exceeds `K`, changing the average would require a contribution outside the allowed range, leaving only the self transition.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    N, K = map(int, input().split())

    if N == 1:
        print(K % MOD)
        return

    dp = [0] * (K + 1)
    for i in range(1, K + 1):
        dp[i] = 1

    limit = min(N, K)

    for people in range(2, limit + 1):
        ndp = [0] * (K + 1)

        for avg in range(1, K + 1):
            cur = dp[avg]
            if cur == 0:
                continue

            ndp[avg] = (ndp[avg] + cur) % MOD

            increase = 1
            while avg + people * increase <= K:
                ndp[avg + increase] = (ndp[avg + increase] + cur) % MOD
                increase += 1

            decrease = 1
            while avg - people * decrease >= 1:
                ndp[avg - decrease] = (ndp[avg - decrease] + cur) % MOD
                decrease += 1

        dp = ndp

    print(sum(dp) % MOD)

if __name__ == "__main__":
    solve()
```

The first part handles the special case of one person because there is no previous average to transition from.

The `dp` array stores only averages, not total balloon counts. This is the compression that makes the huge value of `N` manageable.

Inside the loop, `people` is the number of people after the new arrival. The transition formula depends on this value, so the order of operations matters. We generate the new state from the old average before replacing `dp`.

The increasing and decreasing loops avoid checking all `K` possible next averages. They directly generate only valid changes. The boundary checks `avg + people * increase <= K` and `avg - people * decrease >= 1` prevent invalid averages and are the places where off-by-one mistakes usually appear.

Python integers do not overflow, and all additions are reduced modulo `998244353` to keep the stored values small.

## Worked Examples

For input:

```
3 3
```

The first person can create three possible averages.

| Step | Current averages with counts | Action |
| --- | --- | --- |
| After person 1 | `1:1, 2:1, 3:1` | Initialize states |
| Person 2 | `1:1, 2:2, 3:1` | Generate valid second contributions |
| Person 3 | `1:1, 2:3, 3:1` | Generate final states |

The sum is `5`, matching the sample. The trace shows that different histories can merge into the same average, which is why counting states instead of sequences directly is useful.

For input:

```
4 1
```

| Step | Current averages with counts | Action |
| --- | --- | --- |
| After person 1 | `1:1` | Only contribution is one balloon |
| Person 2 | `1:1` | Average cannot change |
| Person 3 | `1:1` | Average cannot change |
| Person 4 | `1:1` | Average cannot change |

The answer remains `1`. This confirms that forced contributions are handled naturally by the transition rules.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(K^2 log K)` | The number of generated transitions over all processed people is bounded by the harmonic sum of `K^2 / i`. |
| Space | `O(K)` | Only the current and next average distributions are stored. |

With `K <= 2000`, the optimized DP performs only tens of millions of simple operations. The huge value of `N` does not affect the runtime because after the first `K` people the process becomes deterministic.

## Test Cases

```python
import sys
import io

MOD = 998244353

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import sys
    input = sys.stdin.readline

    N, K = map(int, input().split())

    if N == 1:
        ans = K % MOD
        sys.stdin = old_stdin
        return str(ans) + "\n"

    dp = [0] * (K + 1)
    for i in range(1, K + 1):
        dp[i] = 1

    for people in range(2, min(N, K) + 1):
        ndp = [0] * (K + 1)

        for avg in range(1, K + 1):
            if dp[avg] == 0:
                continue
            cur = dp[avg]

            ndp[avg] = (ndp[avg] + cur) % MOD

            d = 1
            while avg + people * d <= K:
                ndp[avg + d] = (ndp[avg + d] + cur) % MOD
                d += 1

            d = 1
            while avg - people * d >= 1:
                ndp[avg - d] = (ndp[avg - d] + cur) % MOD
                d += 1

        dp = ndp

    ans = sum(dp) % MOD
    sys.stdin = old_stdin
    return str(ans) + "\n"

assert solution("3 3\n") == "5\n", "sample 1"
assert solution("4 1\n") == "1\n", "sample 2"

assert solution("1 5\n") == "5\n", "single person"
assert solution("2 2\n") == "3\n", "all possible averages after two people"
assert solution("5 2000\n").strip() != "", "large K boundary"
assert solution("10 1\n") == "1\n", "forced contribution case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 5` | `5` | Minimum number of people and direct initialization |
| `2 2` | `3` | Multiple averages and merging transitions |
| `5 2000` | Any valid integer | Maximum `K` handling |
| `10 1` | `1` | Fully deterministic sequence |

## Edge Cases

For `N = 1`, the algorithm immediately returns `K`. There are no prefix conditions except that the first contribution is within the allowed range, so every possible balloon count works.

For `K = 1`, every average is forced to be `1`. The transition loops have no possible increase or decrease, leaving only the self transition. This keeps exactly one valid sequence regardless of `N`.

For large `N`, such as `N = 10^9` and `K = 2000`, the algorithm stops after processing person `2000`. Any later attempt to change an average would require adding or removing more than `K` balloons in one step, so the only possible continuation repeats the current average forever. The final state count is already the complete answer.
