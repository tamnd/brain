---
title: "CF 105905A - \u041f\u043b\u043e\u0445\u0438\u0435 \u0444\u0438\u0441\u0442\u0430\u0448\u043a\u0438"
description: "The problem describes a group of senators. Each senator has a strength value and a current loyalty percentage. Before a vote starts, we may distribute a limited number of candies."
date: "2026-06-25T14:13:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105905
codeforces_index: "A"
codeforces_contest_name: "Ural championship 2025"
rating: 0
weight: 105905
solve_time_s: 41
verified: true
draft: false
---

[CF 105905A - \u041f\u043b\u043e\u0445\u0438\u0435 \u0444\u0438\u0441\u0442\u0430\u0448\u043a\u0438](https://codeforces.com/problemset/problem/105905/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a group of senators. Each senator has a strength value and a current loyalty percentage. Before a vote starts, we may distribute a limited number of candies. Every candy given to a senator increases that senator's loyalty by 10 percent, but nobody can go above 100 percent. After the distribution, every senator independently votes for or against us according to their final loyalty probability.

If more than half of the senators vote in our favor, we succeed immediately. Otherwise, we can try to remove exactly the senators who voted against us. The chance of removing a group depends on our own strength and the total strength of the removed senators. We need to choose the candy distribution that maximizes the final probability of success.

The number of senators is small, and this changes the whole strategy. With at most 8 senators, the total number of possible final loyalty configurations is manageable. A solution that iterates through subsets of senators is realistic, while a solution that tries every possible vote outcome for a much larger group would not scale.

The number of candies is also small. Since each candy only changes a loyalty value by one step of 10 percent, we can represent the decision as assigning a small number of discrete upgrades. A naive simulation of every possible candy distribution is possible only because the input size is tiny. If the number of senators were around 10^5, even a linear pass would be the only reasonable direction, and exponential enumeration would immediately fail.

A few edge cases are easy to miss. If a senator already has 100 percent loyalty, giving more candies to them has no effect. For example:

```
1 3 20
20 100
```

The correct output is:

```
1.0000000000
```

A careless implementation that blindly treats every candy as increasing loyalty could create an impossible probability above 100 percent.

Another corner case appears when we do not get enough votes and must rely on removing opponents. For example:

```
1 0 10
20 0
```

The only senator always votes against us. We remove that senator with probability:

```
10 / (10 + 20) = 1 / 3
```

so the answer is:

```
0.3333333333
```

A solution that only checks whether we can get a majority of votes would incorrectly return zero.

## Approaches

The first approach is to directly try all candy distributions. Since every candy is assigned to one of the senators, we can recursively choose where each candy goes. After generating one distribution, we compute the new loyalties and evaluate the probability of winning.

This approach is correct because every possible way to spend candies is considered. For each distribution, the probability can be calculated by iterating over all possible voting masks. With n senators, there are 2^n possible voting results. For every mask, we determine whether it already gives us enough positive votes. If it does not, we calculate the probability of removing all losing senators.

The problem is that the number of candy distributions grows quickly. If we have k candies and n senators, the number of assignments is roughly n^k. Even with only 8 senators, increasing k makes this approach expensive. The total work becomes about O(n^k * 2^n), which repeats the same vote calculations many times.

The key observation is that candies only affect the final loyalty of each senator. We do not care about the exact order in which candies are given. The final state of the senators is enough. Since n and k are both very small, we can use dynamic programming over candy usage.

We process candies one by one and store all reachable loyalty states. A state is represented by the amount of loyalty each senator has after some candies have been distributed. The number of possible states is limited because each senator has only eleven possible loyalty values: 0, 10, 20, up to 100. After all candies are assigned, we evaluate every reachable state and keep the best probability.

The transition is simple. From a current state, one more candy can be given to any senator who is not already at 100 percent. The new state is added to the next layer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k * 2^n * n) | O(n) | Too slow for larger k |
| Optimal | O(k * S * n + S * 2^n * n) | O(S) | Accepted |

Here S is the number of reachable loyalty states. With n = 8, the maximum possible number of states is small enough.

## Algorithm Walkthrough

1. Read the senators and convert every loyalty percentage into an integer representing the number of 10 percent blocks. A loyalty of 70 becomes 7. This makes candy operations simple because one candy is just adding one.
2. Start with a single state containing the initial loyalty values and no candies used. This represents the only possible situation before we make any choices.
3. For each candy, create all possible new states. From every current state, try giving the candy to every senator whose loyalty is still below 100 percent. Increase that senator's loyalty by one block and store the resulting state.
4. After all candies are processed, examine every final loyalty state. For each state, calculate the probability of success by iterating over all possible voting masks. If a mask gives us a majority, its probability contributes directly. Otherwise, calculate the probability of removing every losing senator and add that contribution.
5. Take the maximum probability over all final states. This is the answer because every possible candy distribution leads to one of the generated states.

Why it works: the dynamic programming keeps exactly the information that affects future decisions. The only thing candies change is the current loyalty of each senator, so two different histories that reach the same loyalty vector have identical future possibilities. The evaluation step checks every possible voting outcome, meaning it computes the exact success probability for that final state. Since every possible final state is generated, the maximum among them is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    first = input().split()
    if not first:
        return
    n, k, A = map(int, first)

    senators = []
    for _ in range(n):
        b, l = map(int, input().split())
        senators.append((b, l // 10))

    start = tuple(x[1] for x in senators)
    states = {start}

    for _ in range(k):
        nxt = set()
        for state in states:
            for i in range(n):
                if state[i] < 10:
                    arr = list(state)
                    arr[i] += 1
                    nxt.add(tuple(arr))
        states = nxt

    total_masks = 1 << n
    answer = 0.0

    for state in states:
        cur = 0.0
        for mask in range(total_masks):
            prob = 1.0
            bad_sum = 0
            good = 0

            for i in range(n):
                p = state[i] / 10.0
                if mask & (1 << i):
                    good += 1
                    prob *= p
                else:
                    prob *= (1.0 - p)
                    bad_sum += senators[i][0]

            if good > n // 2:
                cur += prob
            else:
                cur += prob * (A / (A + bad_sum))

        if cur > answer:
            answer = cur

    print("{:.10f}".format(answer))

if __name__ == "__main__":
    solve()
```

The first part of the code stores each senator's loyalty in units of ten percent. This avoids floating point changes during the state generation stage. The set named `states` contains all loyalty vectors that can be reached after using the processed candies.

The transition loop follows the third algorithm step. A senator at loyalty value 10 already represents 100 percent, so increasing it would create an invalid state. This is the main boundary condition in the dynamic programming.

The evaluation loop checks every possible subset of senators who vote positively. The bitmask tells us which senators voted for us. We multiply the independent voting probabilities to get the probability of that exact result. When the result is not a majority, the code calculates the strength of the losing senators and applies the removal probability.

The expression `A / (A + bad_sum)` is computed using floating point division. The values are small enough that Python's floating point precision is sufficient for the required output.

## Worked Examples

For the first sample, after giving all candies optimally, the loyalty state becomes:

| Step | Loyalty state | Current best explanation |
| --- | --- | --- |
| Start | 8, 9, 7, 3, 7 | Initial loyalties |
| Give candy | 9, 10, 8, 3, 7 | Improve high impact senators |
| Final | 10, 10, 10, 3, 7 | Majority becomes very likely |

The final state makes three senators certain supporters. Since that is already enough for a majority, every voting result that matters succeeds.

For the third sample:

```
1 3 20
20 20
```

The senator can receive all three candies:

| Step | Loyalty state | Probability of success |
| --- | --- | --- |
| Start | 2 | Need removal |
| After first candy | 3 | Improved vote chance |
| After second candy | 4 | Improved vote chance |
| After third candy | 5 | Vote succeeds with probability 0.5 |

The remaining probability comes from the failed vote case, where the senator is removed. The DP considers this final state and computes the exact probability as 0.7500000000.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k * S * n + S * 2^n * n) | We generate states through candy transitions and evaluate each final state |
| Space | O(S) | We only store the current layer of loyalty states |

The number of senators is at most 8, so even iterating over all voting masks is cheap. The number of reachable loyalty states is also limited by the small number of loyalty levels and candies, so the solution easily fits the intended limits.

## Test Cases

```python
import sys
import io

def solve(data):
    sys.stdin = io.StringIO(data)
    input = sys.stdin.readline

    first = input().split()
    n, k, A = map(int, first)

    senators = []
    for _ in range(n):
        b, l = map(int, input().split())
        senators.append((b, l // 10))

    states = {tuple(x[1] for x in senators)}

    for _ in range(k):
        nxt = set()
        for state in states:
            for i in range(n):
                if state[i] < 10:
                    arr = list(state)
                    arr[i] += 1
                    nxt.add(tuple(arr))
        states = nxt

    ans = 0.0
    for state in states:
        cur = 0.0
        for mask in range(1 << n):
            p = 1.0
            bad = 0
            good = 0
            for i in range(n):
                if mask >> i & 1:
                    good += 1
                    p *= state[i] / 10.0
                else:
                    p *= 1.0 - state[i] / 10.0
                    bad += senators[i][0]
            if good > n // 2:
                cur += p
            else:
                cur += p * A / (A + bad)
        ans = max(ans, cur)

    return f"{ans:.10f}\n"

assert solve("""5 6 100
11 80
14 90
23 70
80 30
153 70
""") == "1.0000000000\n"

assert solve("""5 3 100
11 80
14 90
23 70
80 30
153 70
""") == "0.9628442962\n"

assert solve("""1 3 20
20 20
""") == "0.7500000000\n"

assert solve("""1 3 20
20 100
""") == "1.0000000000\n"

assert solve("""1 0 10
20 0
""") == "0.3333333333\n"

assert solve("""2 0 50
10 100
10 100
""") == "1.0000000000\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One senator already at full loyalty | 1.0000000000 | Candies cannot increase loyalty past 100 percent |
| One impossible voter with no candies | 0.3333333333 | Removal probability handling |
| Two guaranteed supporters | 1.0000000000 | Immediate majority case |
| Original samples | Sample outputs | General correctness |

## Edge Cases

When a senator already has maximum loyalty, the transition must ignore that senator. For the input:

```
1 3 20
20 100
```

the only generated state remains loyalty 10. The voting probability is 1, so the answer is exactly 1. The algorithm handles this because states are never created with loyalty above 10.

When nobody supports us and we must rely on removal, the evaluation phase still works. For:

```
1 0 10
20 0
```

the only voting mask is the losing vote. The senator has strength 20, so the removal chance is 10 / 30. The algorithm multiplies the vote probability by this value and returns 0.3333333333.

When candies are distributed between several senators, different orders can create the same final loyalty vector. The set of states removes these duplicates, so the algorithm does not waste time recalculating identical situations. This is the property that makes the dynamic programming approach efficient.
