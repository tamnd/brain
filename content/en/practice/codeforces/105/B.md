---
title: "CF 105B - Dark Assembly"
description: "We have a small parliament of at most 8 senators. Every senator has two attributes. The first attribute is their level, which matters only if the proposal initially fails and the player must fight the opposing senators."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 105
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 81"
rating: 1800
weight: 105
solve_time_s: 167
verified: true
draft: false
---

[CF 105B - Dark Assembly](https://codeforces.com/problemset/problem/105/B)

**Rating:** 1800  
**Tags:** brute force, probabilities  
**Solve time:** 2m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a small parliament of at most 8 senators. Every senator has two attributes.

The first attribute is their level, which matters only if the proposal initially fails and the player must fight the opposing senators.

The second attribute is loyalty, a probability from 0% to 100% that the senator votes in favor of the proposal.

Before the vote starts, we may distribute at most `k` candies. Every candy increases one senator’s loyalty by 10%, capped at 100%.

After all loyalties are finalized, each senator independently votes yes or no according to their probability.

If strictly more than half of the senators vote yes, the proposal immediately succeeds.

Otherwise, the player fights all senators who voted no. Suppose the total level of these opposing senators is `B`. The probability of winning the fight is:

$$\frac{A}{A+B}$$

where `A` is fixed in the input.

The final success probability for one voting outcome is:

- `1` if the vote already passed.
- `A / (A + B)` otherwise.

Our task is to choose the candy distribution that maximizes the total probability of success.

The constraints completely shape the solution. Both `n` and `k` are at most 8, which is tiny. That means exponential enumeration over voting outcomes is absolutely fine because there are only `2^8 = 256` possible yes/no vote masks. Even trying all candy distributions is feasible because the total number of candies is also tiny.

A careless solution usually fails in two places.

The first mistake is forgetting that loyalty is capped at 100%.

Consider:

```
1 5 10
3 80
```

Giving all 5 candies does not produce 130% loyalty. The actual loyalty becomes 100%, so the answer is exactly `1.0`.

The second mistake is handling tied votes incorrectly.

The proposal succeeds only if the number of yes votes is strictly greater than half.

For example:

```
2 0 100
1 100
1 0
```

There is a 50% chance of a 1-1 tie. A tie is not approval, so we must use combat probability there. The correct answer is:

$$0.5 \cdot 1 + 0.5 \cdot \frac{100}{101}$$

A third subtle point is that the combat phase depends only on senators who voted no, not all senators.

Example:

```
3 0 10
100 100
1 0
1 0
```

If only one weak senator votes no, combat probability is `10 / 11`, not `10 / 112`.

## Approaches

The most direct brute-force idea is to try every possible way to distribute candies, then for each resulting loyalty configuration enumerate every voting outcome.

For one fixed loyalty configuration, every senator independently votes yes or no. Since `n ≤ 8`, there are at most 256 vote masks. For each mask we can compute:

- the probability that exactly this mask occurs,
- whether the proposal passes directly,
- otherwise the combat success probability.

Summing these values gives the total success probability for this candy distribution.

The only remaining challenge is enumerating candy distributions.

A naive approach would treat each candy independently and choose one of `n` senators for it. That gives `n^k` possibilities. Since both are at most 8, the worst case is:

$$8^8 = 16,777,216$$

For every distribution we would still evaluate 256 vote masks. That becomes far too large.

The key observation is that only the final number of candies given to each senator matters. The order of candies does not matter.

So instead of enumerating sequences of candy placements, we enumerate integer distributions:

$$c_1 + c_2 + \dots + c_n \le k$$

where `c_i` is how many candies senator `i` receives.

The number of such distributions is tiny for `n, k ≤ 8`. A simple DFS can generate all of them comfortably.

For each distribution we compute updated loyalties, capped at 100%, then evaluate all `2^n` voting masks.

This works because both dimensions are tiny:

- candy distributions are small enough to enumerate,
- vote outcomes are small enough to enumerate independently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over candy sequences | $O(n^k \cdot 2^n \cdot n)$ | $O(n)$ | Too slow |
| Enumerate candy distributions + vote masks | $O(\binom{n+k}{k} \cdot 2^n \cdot n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all senators’ levels and loyalties.
2. Use DFS to enumerate every valid candy distribution.

We recursively decide how many candies each senator receives. Since the total number of candies is at most 8, this search tree is very small.
3. For one distribution, compute updated loyalties.

If senator `i` originally has loyalty `l[i]` and receives `c[i]` candies, then:

$$p_i = \min(100, l_i + 10 \cdot c_i)$$
4. Enumerate all vote masks from `0` to `(1 << n) - 1`.

Bit `i` equals 1 if senator `i` votes yes.
5. Compute the probability of this exact vote mask.

Since votes are independent:

- multiply by `p_i / 100` if senator `i` votes yes,
- multiply by `(1 - p_i / 100)` otherwise.
6. Count how many senators voted yes.

If the number is strictly greater than `n / 2`, this mask contributes its full probability.
7. Otherwise compute the total level of all senators who voted no.

Let this sum be `B`. The proposal succeeds after combat with probability:

$$\frac{A}{A+B}$$

Multiply this by the probability of the vote mask and add it to the total.
8. After all masks are processed, we obtain the total success probability for this candy distribution.
9. Keep the maximum over all distributions.

### Why it works

The DFS enumerates every possible legal candy allocation exactly once, so no candidate strategy is missed.

For one fixed allocation, the vote-mask enumeration covers every possible voting outcome. Since senators vote independently, multiplying individual probabilities gives the exact probability of each mask.

The final answer for one mask is correct because the problem defines only two possibilities:

- direct approval if yes votes are a strict majority,
- otherwise combat against exactly the senators who voted no.

Summing over all masks gives the exact expected success probability for this allocation. Taking the maximum over all allocations gives the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k, A = map(int, input().split())

level = []
loyalty = []

for _ in range(n):
    b, l = map(int, input().split())
    level.append(b)
    loyalty.append(l)

best = 0.0
candies = [0] * n

def evaluate():
    global best

    probs = [
        min(100, loyalty[i] + candies[i] * 10) / 100.0
        for i in range(n)
    ]

    total = 0.0

    for mask in range(1 << n):
        prob = 1.0
        yes = 0
        bad_sum = 0

        for i in range(n):
            if (mask >> i) & 1:
                prob *= probs[i]
                yes += 1
            else:
                prob *= (1.0 - probs[i])
                bad_sum += level[i]

        if yes > n // 2:
            total += prob
        else:
            total += prob * (A / (A + bad_sum))

    best = max(best, total)

def dfs(idx, remaining):
    if idx == n:
        evaluate()
        return

    for take in range(remaining + 1):
        candies[idx] = take
        dfs(idx + 1, remaining - take)

dfs(0, k)

print(f"{best:.10f}")
```

The DFS generates all candy distributions. At position `idx`, we choose how many candies senator `idx` receives, from `0` up to the remaining amount.

One subtle detail is that we allow unused candies. The recursion handles this naturally because the final senators may receive zero candies.

The `evaluate()` function computes the exact probability for one distribution. The variable `prob` stores the probability of a specific voting mask occurring. Since all senators vote independently, probabilities multiply.

The tie condition is handled carefully:

```
if yes > n // 2:
```

Using `>=` here would be incorrect because ties do not approve the proposal.

Another easy mistake is computing combat strength incorrectly. We only add levels of senators who voted no:

```
bad_sum += level[i]
```

inside the `else` branch.

The probability cap is handled with:

```
min(100, loyalty[i] + candies[i] * 10)
```

Without this cap, probabilities larger than 1 would appear.

## Worked Examples

### Sample 1

Input:

```
5 6 100
11 80
14 90
23 70
80 30
153 70
```

One optimal distribution gives candies to the first three senators.

Updated loyalties become:

| Senator | Original | Candies | Final |
| --- | --- | --- | --- |
| 1 | 80 | 2 | 100 |
| 2 | 90 | 1 | 100 |
| 3 | 70 | 3 | 100 |
| 4 | 30 | 0 | 30 |
| 5 | 70 | 0 | 70 |

Now at least 3 senators always vote yes because senators 1, 2, and 3 are guaranteed yes votes.

| Yes votes | Result |
| --- | --- |
| 3 | Approved |
| 4 | Approved |
| 5 | Approved |

The proposal always passes directly, so the final probability is:

```
1.0000000000
```

This example demonstrates that maximizing direct majority can completely eliminate the combat phase.

### Sample 2

Consider:

```
2 0 100
1 100
1 0
```

Possible vote masks:

| Mask | Yes voters | Probability | Outcome |
| --- | --- | --- | --- |
| 00 | none | 0 | fight |
| 01 | senator 1 | 1.0 | tie, fight |
| 10 | senator 2 | 0 | tie, fight |
| 11 | both | 0 | approved |

The only real outcome is mask `01`.

The proposal is tied 1-1, so combat occurs against senator 2.

Combat success probability:

$$\frac{100}{101}$$

Final answer:

$$1 \cdot \frac{100}{101} = 0.9900990099$$

This example confirms that ties are not automatic approvals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\binom{n+k}{k} \cdot 2^n \cdot n)$ | enumerate all candy distributions and all vote masks |
| Space | $O(n)$ | recursion stack and candy array |

For `n, k ≤ 8`, the number of candy distributions is at most:

$$\binom{16}{8} = 12870$$

Each distribution evaluates only 256 vote masks, each touching at most 8 senators. This easily fits within the time limit in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n, k, A = map(int, input().split())

    level = []
    loyalty = []

    for _ in range(n):
        b, l = map(int, input().split())
        level.append(b)
        loyalty.append(l)

    best = 0.0
    candies = [0] * n

    def evaluate():
        nonlocal best

        probs = [
            min(100, loyalty[i] + candies[i] * 10) / 100.0
            for i in range(n)
        ]

        total = 0.0

        for mask in range(1 << n):
            prob = 1.0
            yes = 0
            bad_sum = 0

            for i in range(n):
                if (mask >> i) & 1:
                    prob *= probs[i]
                    yes += 1
                else:
                    prob *= (1.0 - probs[i])
                    bad_sum += level[i]

            if yes > n // 2:
                total += prob
            else:
                total += prob * (A / (A + bad_sum))

        best = max(best, total)

    def dfs(idx, remaining):
        if idx == n:
            evaluate()
            return

        for take in range(remaining + 1):
            candies[idx] = take
            dfs(idx + 1, remaining - take)

    dfs(0, k)

    print(f"{best:.10f}")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# provided sample
assert run(
"""5 6 100
11 80
14 90
23 70
80 30
153 70
"""
) == "1.0000000000", "sample 1"

# minimum size
assert run(
"""1 0 10
5 0
"""
) == "0.6666666667", "single senator, must fight"

# loyalty cap at 100
assert run(
"""1 5 10
3 80
"""
) == "1.0000000000", "probability cap"

# tie handling
assert run(
"""2 0 100
1 100
1 0
"""
) == "0.9900990099", "tie should not auto-pass"

# all already guaranteed yes
assert run(
"""3 8 1
5 100
5 100
5 100
"""
) == "1.0000000000", "always approved"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single senator with 0 loyalty | 0.6666666667 | combat-only scenario |
| Loyalty above 100 after candies | 1.0000000000 | probability cap |
| Two senators with one guaranteed yes | 0.9900990099 | strict majority rule |
| Everyone already loyal | 1.0000000000 | no unnecessary combat |

## Edge Cases

Consider the loyalty cap case:

```
1 5 10
3 80
```

The DFS explores distributions from 0 to 5 candies.

When all 5 candies are assigned, the raw loyalty would become 130, but the algorithm applies:

```
min(100, 130)
```

so the actual probability becomes exactly 1. The only senator always votes yes, producing answer `1.0000000000`.

Now consider the tie scenario:

```
2 0 100
1 100
1 0
```

The vote mask with exactly one yes vote has probability 1. The algorithm checks:

```
if yes > n // 2
```

Since `1 > 1` is false, the proposal does not pass directly. The algorithm correctly computes combat probability against the lone opposing senator.

Finally consider a case where combat depends only on no-voters:

```
3 0 10
100 100
1 0
1 0
```

If senator 1 votes yes and senators 2 and 3 vote no, then only levels `1 + 1` are included in `bad_sum`.

The algorithm never adds the level 100 senator because that senator voted yes. Combat probability becomes:

$$\frac{10}{12}$$

which matches the statement exactly.
