---
title: "CF 2222A - A Wonderful Contest"
description: "Each problem in the contest is worth at most 100 points. If a problem has $ai$ subtasks, then every solved subtask contributes $$frac{100}{ai}$$ points, and $ai$ is guaranteed to divide 100."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "A"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 269
verified: false
draft: false
---

[CF 2222A - A Wonderful Contest](https://codeforces.com/problemset/problem/2222/A)

**Rating:** -  
**Tags:** brute force, dp, math  
**Solve time:** 4m 29s  
**Verified:** no  

## Solution
## Problem Understanding

Each problem in the contest is worth at most 100 points. If a problem has $a_i$ subtasks, then every solved subtask contributes

$$\frac{100}{a_i}$$

points, and $a_i$ is guaranteed to divide 100. This means every problem contributes one of the values

$$0,\ \frac{100}{a_i},\ 2\cdot\frac{100}{a_i},\ \ldots,\ 100.$$

For a contestant, the final score is the sum of the contributions from all problems.

The question is not about a particular contestant. We must determine whether the set of all possible total scores contains every integer from 0 up to $100n$. If even one integer score is impossible to obtain, the answer is "No".

The constraints are very small. There are at most 10 problems, and each problem contributes at most 101 different scores. The maximum total score is $100 \cdot 10 = 1000$. Whenever a problem has a small maximum sum and the task asks which totals are achievable, subset-sum style dynamic programming becomes a natural candidate.

A common mistake is to focus only on the greatest common divisor of score increments. Having score step sizes whose gcd is 1 is necessary, but not sufficient.

Consider:

```
1
2
100 100
```

Each problem contributes either 0 through 100 in steps of 1. Every score from 0 to 200 is reachable, so the answer is:

```
Yes
```

Now consider:

```
1
1
2
```

The only possible scores are 0, 50, and 100. The gcd of achievable differences is 50, and many integers are missing. The answer is:

```
No
```

Another subtle case is when some small scores are achievable but gaps remain in the middle.

Example:

```
1
2
2 2
```

Possible totals are only multiples of 50 between 0 and 200. Score 75 is impossible, so the answer is:

```
No
```

A careless solution that checks only the minimum score increment or only the endpoints would incorrectly accept such cases.

## Approaches

The most direct approach is brute force over all possible choices of solved subtasks. For problem $i$, there are $a_i + 1$ possibilities for $x_i$. Since $a_i$ can be as large as 100, one test case could require exploring

$$101^{10}$$

combinations, which is astronomically large.

The reason brute force is conceptually correct is that every combination corresponds to exactly one achievable score. If we enumerated all of them, we could mark every reachable total and check whether all integers appear. The difficulty is purely the number of states.

The key observation is that the total score never exceeds 1000. Whenever the target sum is small, it is usually better to track reachable sums instead of tracking all choices that produce them.

For each problem, the set of scores it can contribute is known:

$$\{0, s_i, 2s_i, \ldots, 100\},$$

where $s_i = \frac{100}{a_i}$.

We can build a dynamic programming table where `dp[t]` indicates whether score `t` is reachable after processing some prefix of problems. For every currently reachable total and every score contribution of the next problem, we mark the new total as reachable.

The number of totals is only 1001, and each problem has at most 101 possible contributions. That makes the state space tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(\prod (a_i+1))$ | $O(\prod (a_i+1))$ | Too slow |
| Optimal DP | $O(n \cdot 1000 \cdot 101)$ | $O(1000)$ | Accepted |

## Algorithm Walkthrough

1. For every problem, compute its score step:

$$s_i = \frac{100}{a_i}.$$

The possible contributions of this problem are $0, s_i, 2s_i, \ldots, 100$.
2. Create a boolean DP array of size $100n + 1$.

Set `dp[0] = True` because a score of 0 is reachable before processing any problems.
3. Process the problems one by one.

For the current problem, create a fresh array `ndp`.
4. For every reachable total score `cur`, try every contribution of the current problem.

If the contribution is `k * s_i`, mark

$$cur + k \cdot s_i$$

as reachable in `ndp`.
5. Replace `dp` with `ndp`.

After processing the first $i$ problems, `dp[t]` represents exactly the totals achievable using those $i$ problems.
6. After all problems have been processed, check every score from 0 to $100n$.

If any score is unreachable, print `"No"`.
7. If all scores are reachable, print `"Yes"`.

### Why it works

The DP maintains a simple invariant.

After processing the first $i$ problems, `dp[t]` is true if and only if there exists a valid choice of solved subtasks for those $i$ problems whose total score is exactly $t$.

The invariant is true initially because only score 0 is achievable with zero problems. During a transition, every reachable score from the previous stage is combined with every legal contribution of the next problem. This generates exactly all totals achievable after adding that problem, neither missing any valid total nor introducing an invalid one.

After all problems are processed, the DP contains precisely the set of achievable contest scores. Checking whether every value from 0 to $100n$ appears directly answers the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        max_score = 100 * n

        dp = [False] * (max_score + 1)
        dp[0] = True

        for ai in a:
            step = 100 // ai

            ndp = [False] * (max_score + 1)

            for cur in range(max_score + 1):
                if not dp[cur]:
                    continue

                for solved in range(ai + 1):
                    nxt = cur + solved * step
                    if nxt <= max_score:
                        ndp[nxt] = True

            dp = ndp

        ok = all(dp[s] for s in range(max_score + 1))
        print("Yes" if ok else "No")

solve()
```

The DP array stores reachable total scores. Initially only score 0 is reachable.

For each problem, we build a new layer. If a problem has `ai` subtasks, then solving `solved` subtasks contributes `solved * (100 // ai)` points. Every such contribution is tried against every previously reachable total.

The fresh array `ndp` is important. Using the same array for both reading and writing would allow the current problem to be counted multiple times, which would corrupt the state.

The maximum score is only `100 * n`, so the array size never exceeds 1001. All calculations stay comfortably within integer limits.

## Worked Examples

### Example 1

Input:

```
1
2
100 20
```

Problem 1 contributes every score from 0 to 100.

Problem 2 contributes:

```
0, 5, 10, ..., 100
```

| Step | Reachable scores |
| --- | --- |
| Initial | {0} |
| After problem 1 | {0,1,2,...,100} |
| After problem 2 | {0,1,2,...,200} |

Every integer from 0 to 200 becomes reachable.

Output:

```
Yes
```

This example shows how a problem with step size 1 immediately fills all gaps, and adding the second problem extends the interval continuously.

### Example 2

Input:

```
1
2
2 10
```

The contributions are:

```
Problem 1: {0, 50, 100}
Problem 2: {0, 10, 20, ..., 100}
```

| Current total | Added contribution | New total |
| --- | --- | --- |
| 0 | 0,10,20,...,100 | 0,10,20,...,100 |
| 50 | 0,10,20,...,100 | 50,60,70,...,150 |
| 100 | 0,10,20,...,100 | 100,110,120,...,200 |

The union contains only multiples of 10.

Score 95 never appears.

Output:

```
No
```

This trace demonstrates that covering a large numeric range is not enough. Every individual integer must be reachable.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \cdot 1000 \cdot 101)$ | At most 10 problems, at most 1001 totals, at most 101 contributions per problem |
| Space | $O(1000)$ | Two DP arrays of length at most 1001 |

The worst case is roughly one million transitions per test case, which is easily within the limits. The memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        max_score = 100 * n
        dp = [False] * (max_score + 1)
        dp[0] = True

        for ai in a:
            step = 100 // ai
            ndp = [False] * (max_score + 1)

            for cur in range(max_score + 1):
                if not dp[cur]:
                    continue

                for solved in range(ai + 1):
                    nxt = cur + solved * step
                    if nxt <= max_score:
                        ndp[nxt] = True

            dp = ndp

        out.append("Yes" if all(dp) else "No")

    return "\n".join(out)

# sample-style cases
assert run("1\n2\n100 20\n") == "Yes"

# minimum size
assert run("1\n1\n1\n") == "No"

# single problem with step size 1
assert run("1\n1\n100\n") == "Yes"

# all scores multiples of 50
assert run("1\n2\n2 2\n") == "No"

# many divisors, contains a step size of 1
assert run("1\n8\n1 2 4 5 10 20 25 100\n") == "Yes"

# boundary case with gap at 95
assert run("1\n2\n2 10\n") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 1` | `No` | Minimum size, only scores 0 and 100 exist |
| `1 / 1 / 100` | `Yes` | Every score 0..100 is directly reachable |
| `1 / 2 / 2 2` | `No` | Large gaps remain between reachable scores |
| `1 / 8 / 1 2 4 5 10 20 25 100` | `Yes` | Many different step sizes, full coverage |
| `1 / 2 / 2 10` | `No` | Missing middle values such as 95 |

## Edge Cases

### A single problem with coarse scoring

Input:

```
1
1
2
```

The score step is 50, so the only contributions are:

```
0, 50, 100
```

After processing the problem, the DP marks exactly those three totals. Scores such as 1, 2, and 99 remain unreachable. The final coverage check fails and the algorithm outputs:

```
No
```

### A single problem with unit scoring

Input:

```
1
1
100
```

The score step is 1. The problem contributes every value from 0 to 100.

After the DP transition, every position in `dp[0..100]` becomes true. The coverage check succeeds and the output is:

```
Yes
```

### Multiple problems whose scores are all multiples of the same number

Input:

```
1
2
2 2
```

Each problem contributes only multiples of 50.

The reachable totals become:

```
0, 50, 100, 150, 200
```

The DP correctly leaves scores such as 25 and 75 unreachable. Since not all integers appear, the answer is:

```
No
```

### Presence of a problem with step size 1

Input:

```
1
2
100 100
```

After the first problem, every score from 0 to 100 is reachable.

Adding the second problem shifts that interval by every value from 0 to 100, producing all scores from 0 to 200 without gaps. The DP marks every total and the answer is:

```
Yes
```

This case confirms that the algorithm checks actual reachability rather than relying on heuristic conditions such as gcd calculations.
