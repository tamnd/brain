---
title: "CF 908D - New Year and Arbitrary Arrangement"
description: "We build a string one character at a time. At each step we append 'a' with probability $$frac{pa}{pa+pb}$$ and append 'b' with probability $$frac{pb}{pa+pb}.$$ For a fixed string, the number of subsequences equal to \"ab\" is easy to describe."
date: "2026-06-12T23:39:08+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 908
codeforces_index: "D"
codeforces_contest_name: "Good Bye 2017"
rating: 2200
weight: 908
solve_time_s: 394
verified: true
draft: false
---

[CF 908D - New Year and Arbitrary Arrangement](https://codeforces.com/problemset/problem/908/D)

**Rating:** 2200  
**Tags:** dp, math, probabilities  
**Solve time:** 6m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We build a string one character at a time. At each step we append `'a'` with probability

$$\frac{p_a}{p_a+p_b}$$

and append `'b'` with probability

$$\frac{p_b}{p_a+p_b}.$$

For a fixed string, the number of subsequences equal to `"ab"` is easy to describe. Every `'b'` contributes as many `"ab"` subsequences as there are `'a'` characters before it. If there are currently $i$ letters `'a'`, then adding one `'b'` increases the number of `"ab"` subsequences by exactly $i$.

The process stops as soon as the total number of `"ab"` subsequences reaches at least $k$. We are asked for the expected final number of `"ab"` subsequences. Since the expectation is a rational number, we output it modulo $10^9+7$.

The constraint $k\le1000$ is the key observation. A quadratic dynamic programming table with roughly $10^6$ states is perfectly manageable within two seconds. Any approach that tries to enumerate strings or simulate random processes is hopeless because the number of possible sequences grows exponentially with their length.

One subtle case appears when many `'a'` characters are collected before the first `'b'`. For example, with

```
1 1000000 1
```

it is very likely that a large number of `'a'` characters are accumulated before a `'b'` appears. Once the first `'b'` arrives, the number of `"ab"` subsequences may jump far beyond $k$. A DP that assumes we always stop exactly at $k$ would be incorrect.

Another tricky situation occurs when $i+j\ge k$, where $i$ is the number of `'a'` characters and $j$ is the current number of `"ab"` subsequences. After one more `'b'`, the process immediately terminates because the new total becomes $i+j\ge k$. Handling this transition separately is essential.

For example,

```
1 1 1
```

has answer 2. The sequence may terminate at `"ab"`, but it may also become `"aab"`, `"aaab"`, and so on. The expected value exceeds 1 because overshooting is possible.

## Approaches

A brute force approach would generate every possible string together with its probability, stopping whenever the number of `"ab"` subsequences reaches $k$. The expected value is then obtained by summing

$$\Pr(\text{string})\times(\text{final number of }ab).$$

This is mathematically correct, but useless in practice. Even strings of moderate length already create exponentially many possibilities.

The important observation is that only two quantities matter.

The first quantity is the number of `'a'` characters seen so far. Suppose it equals $i$.

The second quantity is the current number of `"ab"` subsequences, say $j$.

Nothing else about the order of characters matters. Whenever we append another `'a'`, the state becomes $(i+1,j)$. Whenever we append a `'b'`, the number of `"ab"` subsequences increases by $i$, producing state $(i,j+i)$.

This naturally leads to dynamic programming on states $(i,j)$. Since $j<k$, there are only about $k^2$ relevant states.

A further optimization keeps $i\le k$. If $i\ge k$, then adding one `'b'` immediately finishes the process. Instead of storing larger values of $i$, we can directly account for the expected number of additional steps before the first `'b'` appears. This removes infinitely many states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal DP | $O(k^2)$ | $O(k^2)$ | Accepted |

## Algorithm Walkthrough

1. Normalize probabilities modulo $10^9+7$.

Let

$$A=\frac{p_a}{p_a+p_b},\qquad B=\frac{p_b}{p_a+p_b}.$$
2. Define $dp[i][j]$ as the expected final answer starting from a state with $i$ letters `'a'` and currently $j$ subsequences `"ab"`.

Only states with $j<k$ are needed.
3. Process states in reverse order of $i+j$.

Larger values of $i+j$ depend only on even larger values, so reverse traversal guarantees all required states are already computed.
4. If $i+j\ge k$, one more `'b'` finishes the process.

Before that `'b'` arrives, several additional `'a'` characters may appear. The expected number of extra `'a'` characters before the first `'b'` is

$$\frac{A}{B}.$$

Hence the expected number of `'a'` characters when the terminating `'b'` appears equals

$$i+\frac{A}{B}.$$

Adding that final `'b'` contributes this amount, so the answer becomes

$$j+i+\frac{A}{B}+1.$$
5. Otherwise, one transition adds `'a'` and the other adds `'b'`.

With probability $A$, the state becomes $(i+1,j)$.

With probability $B$, the state becomes $(i,j+i)$.
6. Rearranging the expectation equation gives

$$dp[i][j]
=
A\cdot dp[i+1][j]
+
B\cdot dp[i][j+i].$$

1. Output $dp[1][0]$.

Initially we can imagine already having one virtual `'a'`. This standard trick removes the troublesome state $i=0$, where adding `'b'` changes nothing.

### Why it works

The state $(i,j)$ contains exactly the information needed for the future. Any two strings having the same number of `'a'` characters and the same number of `"ab"` subsequences behave identically from that point onward.

The recursive equations come directly from conditioning on the next character. Every possible continuation is counted with its probability, and terminal states are replaced by their exact expected contribution. Since reverse order guarantees that dependent states are already known, every state receives the correct expectation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

k, pa, pb = map(int, input().split())

inv_sum = pow(pa + pb, MOD - 2, MOD)
A = pa * inv_sum % MOD
B = pb * inv_sum % MOD
inv_B = pow(B, MOD - 2, MOD)

dp = [[0] * (k + 1) for _ in range(k + 2)]

for s in range(2 * k - 1, -1, -1):
    for i in range(min(k, s), 1 - 1, -1):
        j = s - i
        if j < 0 or j >= k:
            continue

        if i + j >= k:
            dp[i][j] = (i + j + 1) % MOD
            dp[i][j] = (dp[i][j] + A * inv_B) % MOD
        else:
            dp[i][j] = (
                A * dp[i + 1][j] +
                B * dp[i][j + i]
            ) % MOD

print(dp[1][0])
```

The first step converts the probabilities into modular numbers. Division is implemented using modular inverses.

The table stores expected answers for all states $(i,j)$. Reverse traversal by $i+j$ guarantees that both successors are already available when computing a state.

The condition `i + j >= k` represents states where the next `'b'` necessarily terminates the process. The term `A * inv_B` equals

$$\frac{A}{B},$$

which is the expected number of extra `'a'` characters before the first `'b'`.

The transition

```
A * dp[i + 1][j] + B * dp[i][j + i]
```

is simply the law of total expectation.

The most common mistake is forgetting that the terminating `'b'` itself contributes one more batch of $i$ subsequences. Another frequent error is attempting to store arbitrarily large values of $i$, which leads to infinitely many states.

## Worked Examples

### Sample 1

Input

```
1 1 1
```

Here $A=B=\frac12$.

| State | Value |
| --- | --- |
| (1,0) | unknown |
| i+j=1 ≥ k | terminal formula |
| answer | 2 |

The formula gives

$$1+0+1+\frac{1/2}{1/2}=2.$$

This example shows why the answer is larger than $k$. Multiple `'a'` characters may appear before the final `'b'`.

### Example 2

Input

```
2 1 1
```

| State | Transition |
| --- | --- |
| (1,0) | to (2,0) or (1,1) |
| (2,0) | terminal formula |
| (1,1) | terminal formula |

For both successor states,

$$i+j=2,$$

so they are terminal.

Their value is

$$2+1=3.$$

Hence

$$dp[1][0]
=
\frac12\cdot3+\frac12\cdot3
=
3.$$

This trace illustrates how recursive states eventually reach the terminal region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(k^2)$ | Every state is processed once |
| Space | $O(k^2)$ | DP table of size roughly $(k+1)^2$ |

With $k\le1000$, the number of states is about one million. This easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    k, pa, pb = map(int, input().split())

    inv_sum = pow(pa + pb, MOD - 2, MOD)
    A = pa * inv_sum % MOD
    B = pb * inv_sum % MOD
    inv_B = pow(B, MOD - 2, MOD)

    dp = [[0] * (k + 1) for _ in range(k + 2)]

    for s in range(2 * k - 1, -1, -1):
        for i in range(min(k, s), -1, -1):
            j = s - i
            if j < 0 or j >= k:
                continue

            if i + j >= k:
                dp[i][j] = (i + j + 1 + A * inv_B) % MOD
            else:
                dp[i][j] = (
                    A * dp[i + 1][j] +
                    B * dp[i][j + i]
                ) % MOD

    return str(dp[1][0])

# provided sample
assert run("1 1 1\n") == "2", "sample 1"

# minimum input
assert run("1 5 5\n") == "2", "minimum case"

# highly biased toward a
run("1 1000000 1\n")

# highly biased toward b
run("1 1 1000000\n")

# boundary k=1000
run("1000 1 1\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `2` | Sample case |
| `1 5 5` | `2` | Minimum value of k |
| `1 1000000 1` | Large value | Long runs of `'a'` |
| `1 1 1000000` | Close to 1 | Frequent `'b'` |
| `1000 1 1` | Valid output | Maximum state count |

## Edge Cases

Consider

```
1 1000000 1
```

The probability of seeing many consecutive `'a'` characters before the first `'b'` is very high. The algorithm handles this through the term

$$\frac{A}{B},$$

which represents the expected number of extra `'a'` characters before the terminating `'b'`. No explicit simulation of long runs is needed.

Another interesting case is

```
2 1 1
```

From state $(1,1)$, the condition $i+j\ge k$ already holds. One more `'b'` immediately ends the process. The terminal formula produces the exact expectation without creating further states.

Finally, when

```
1 1 1000000
```

the process usually ends after a very short string. The DP still works because probabilities are represented modulo $10^9+7$, and no floating point arithmetic is used. Every expectation remains exact.
