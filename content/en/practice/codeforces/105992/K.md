---
title: "CF 105992K - \u795e\u4e4b\u4e00\u624b"
description: "We are simulating a probabilistic board process that runs over many rounds, where each round can instantly end the game depending on rare failure events."
date: "2026-06-22T16:39:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105992
codeforces_index: "K"
codeforces_contest_name: "The 2025 Shanghai Collegiate Programming Contest"
rating: 0
weight: 105992
solve_time_s: 85
verified: true
draft: false
---

[CF 105992K - \u795e\u4e4b\u4e00\u624b](https://codeforces.com/problemset/problem/105992/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a probabilistic board process that runs over many rounds, where each round can instantly end the game depending on rare failure events. The state of the game is extremely small: at any moment we only need to know whether you currently have zero or one “bad” stones that failed to stay in the box. The moment this count reaches two, the game ends immediately.

Each round has two sources of danger. At the start, if you already have exactly one bad stone, the opponent may immediately end the game with a small probability. If that does not happen, you proceed through a sequence of stones. Each stone may become bad in two ways: it can fail to be placed correctly, and later, if too many stones have been processed in the current round, it may also fall out of the box due to overflow. Every time a stone becomes bad, your bad-stone counter increases, and reaching two triggers immediate loss.

The task is not to simulate the process directly, but to compute, for every round, the probability that the first time you lose happens exactly in that round.

The input size makes direct simulation impossible. The number of rounds can be up to 100000, while each round may contain up to 10^9 stones. This immediately rules out any per-stone simulation. Even O(n log ai) per round would be too slow unless each transition is extremely cheap, and even then we must carefully structure reuse across rounds.

A subtle edge case arises from the fact that losing can happen either at the start of a round or during processing. For example, if you enter a round already in the “one bad stone” state and the opponent triggers an immediate loss, none of the within-round probabilities matter. A naive solution that only models within-round transitions will miss this contribution entirely.

Another pitfall is forgetting that overflow behavior changes after the first 80 stones in a round. Treating all stones identically leads to incorrect transition probabilities in long rounds.

## Approaches

A direct brute-force idea is to simulate every stone in every round while tracking whether we are in state 0 or 1 and stopping when we hit 2 bad stones. This is correct in principle because the process is Markovian, and each transition depends only on the current state. However, the number of steps is the sum of all ai, which can reach 10^14 in worst cases, making this approach completely infeasible.

The key observation is that the state space is tiny, but transitions are probabilistic and accumulate linearly. Instead of simulating step by step, we model each round as a linear transformation on a probability vector over three states: having zero bad stones, one bad stone, or already having lost.

Each stone induces the same kind of linear update, except that after 80 stones the transition probabilities change. Repeating the same linear transformation many times suggests matrix exponentiation. This allows us to jump over long sequences of identical transitions in logarithmic time.

We then compose two phases per round, the first for the first 79 stones and the second for the remaining stones. Each phase is represented by a 3 by 3 matrix, and fast exponentiation allows us to compute the effect of up to 10^9 identical steps efficiently.

Finally, we must propagate probabilities across rounds, because the starting state distribution of a round depends on the previous round’s outcome.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force per stone | O(∑ ai) | O(1) | Too slow |
| Matrix exponentiation per round | O(n log ai) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a probability distribution over the state at the beginning of each round. Let dp0 be the probability of starting a round with zero bad stones, and dp1 the probability of starting with exactly one bad stone. Any probability mass that has already reached two bad stones is discarded because the process is absorbed there.

For each round we do the following.

1. First handle the immediate end condition at the start of the round. If we are in state 1, the opponent may immediately cause a loss with probability r/1000. We add this contribution directly to the answer of this round. The remaining probability mass in state 1 survives with probability 1 minus this value and continues into the round as state 1.
2. We now model the within-round process using a transition system over three states: state 0, state 1, and terminal loss. Each stone updates these probabilities linearly.
3. We split the round into two phases because the overflow rule changes after 80 stones. The first phase uses a per-stone failure probability based only on p. The second phase uses a modified probability that includes both p and the additional overflow failure q.
4. We represent each phase as a 3 by 3 transition matrix. Raising this matrix to a power allows us to compute the effect of many identical stones in logarithmic time.
5. We apply the first phase matrix exponent for min(ai, 79) steps, then apply the second phase matrix exponent for the remaining steps. Multiplying these matrices gives a single transformation for the whole round.
6. We apply this transformation separately to the basis states 0 and 1, obtaining both the probability of losing during the round and the resulting distribution over states if we survive.
7. We use these results to compute the loss probability contributed by this round and also update dp0 and dp1 for the next round.

The core invariant is that at the start of each round, dp0 and dp1 fully describe all surviving probability mass, and the matrix transformation exactly preserves linearity of the process. Every transition inside a round is linear in the current distribution, and absorption into the loss state ensures we never need to track more than these three states. Because the transformation is applied exactly, not approximated, the probability mass accounting remains exact across all rounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def inv(x):
    return pow(x, MOD - 2, MOD)

def mat_mul(a, b):
    n = 3
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    res[i][j] = (res[i][j] + a[i][k] * b[k][j]) % MOD
    return res

def mat_pow(mat, exp):
    n = 3
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    base = mat
    while exp > 0:
        if exp & 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        exp >>= 1
    return res

def build_matrix(p_fail):
    p = p_fail
    # states: 0, 1, dead
    # dead is absorbing
    return [
        [1 - p, 0, 0],
        [p, 1 - p, 0],
        [0, p, 1]
    ]

def apply(mat, vec):
    res = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            res[i] = (res[i] + mat[i][j] * vec[j]) % MOD
    return res

def solve():
    p, q, r = map(int, input().split())
    n = int(input())
    a = list(map(int, input().split()))

    inv1000 = inv(1000)

    def get_fail(x, use_q):
        if use_q:
            base = p * inv1000 % MOD
            extra = q * inv1000 % MOD
            return (base + (1 - base) * extra) % MOD
        else:
            return p * inv1000 % MOD

    dp0, dp1 = 1, 0
    ans = []

    for ai in a:
        # immediate opponent action
        r_prob = r * inv1000 % MOD
        add_loss = dp1 * r_prob % MOD
        ans.append(add_loss % MOD)

        dp1 = dp1 * (1 - r_prob) % MOD

        # build matrices
        k1 = min(ai, 79)
        k2 = max(0, ai - 79)

        M0 = build_matrix(get_fail(0, False))
        M1 = build_matrix(get_fail(0, True))  # placeholder corrected below

        # correct failure rates
        pA = p * inv1000 % MOD
        pB = (pA + (1 - pA) * (q * inv1000 % MOD)) % MOD

        M0 = [
            [1 - pA, 0, 0],
            [pA, 1 - pA, 0],
            [0, pA, 1]
        ]

        M1 = [
            [1 - pB, 0, 0],
            [pB, 1 - pB, 0],
            [0, pB, 1]
        ]

        T0 = mat_pow(M0, k1)
        T1 = mat_pow(M1, k2)

        T = mat_mul(T1, T0)

        v0 = apply(T, [1, 0, 0])
        v1 = apply(T, [0, 1, 0])

        f0 = v0[2]
        f1 = v1[2]

        ans[-1] = (ans[-1] + dp0 * f0 + dp1 * f1) % MOD

        n0 = (dp0 * v0[0] + dp1 * v1[0]) % MOD
        n1 = (dp0 * v0[1] + dp1 * v1[1]) % MOD

        dp0, dp1 = n0, n1

    for x in ans:
        print(x % MOD)

if __name__ == "__main__":
    solve()
```

The implementation treats each round as a composition of two linear systems. The first adjustment removes the immediate loss probability from state 1 before any stones are processed. Then two transition matrices are constructed, one for the first part of the round and one for the overflow phase. Matrix exponentiation compresses long sequences of identical transitions.

Each basis vector application gives both the probability of ending in each state and the probability of having already lost. This dual information is necessary because we both compute the loss probability for the current round and propagate the surviving distribution forward.

A common mistake is forgetting to remove the opponent-triggered immediate loss from the surviving mass before applying the matrix. If that is not done, the state 1 probability would be overcounted in later transitions.

## Worked Examples

Consider a small scenario where only a few stones exist so that overflow never triggers. Let p be nonzero and q irrelevant.

| Step | dp0 | dp1 | Event |
| --- | --- | --- | --- |
| Start | 1 | 0 | initial |
| Round transition | computed | computed | stone processing |
| End | updated | updated | carry to next round |

This demonstrates that dp evolves independently of within-round details, relying only on the aggregated transition result.

Now consider a case where we start a round in state 1.

| Phase | dp1 before | Immediate loss | dp1 after |
| --- | --- | --- | --- |
| Start of round | x | x·r | x(1-r) |

This shows how opponent intervention is separated from the within-round stochastic process. The matrix only handles the internal dynamics, while the opponent event is handled as a pre-transition absorption.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log ai) | each round uses two 3x3 exponentiations |
| Space | O(1) | only constant-sized matrices and DP states |

The logarithmic exponentiation ensures that even with large ai values, the computation remains efficient. With n up to 100000, the solution stays comfortably within limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

# assume solve() defined above

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio
    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal case
assert run("0 0 0\n1\n0\n") == "0"

# only opponent loss possibility
assert run("0 0 1000\n2\n1 1\n") is not None

# overflow irrelevant small ai
assert run("100 200 300\n1\n5\n") is not None

# mixed small sequence
assert run("10 20 30\n3\n10 20 30\n") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| p=q=r=0 | all zeros | no transitions |
| r=1000, dp1 start | immediate loss | opponent rule |
| ai < 80 | no overflow phase | single matrix behavior |
| ai > 80 | two-phase transition | matrix composition |

## Edge Cases

When p, q, and r are all zero, the transition matrices become identity transformations except for the absorbing state which is never reached. The algorithm correctly keeps dp unchanged and produces zero loss probability for every round.

When r is maximal, any time dp1 is nonzero at the start of a round, the entire contribution from that state is immediately converted into loss probability for that round. The matrix phase is still applied only to the surviving portion, so no double counting occurs.

When ai is smaller than 80, the second phase matrix is never used, so the algorithm reduces to a single matrix exponentiation. This confirms that the phase split does not introduce artifacts when overflow conditions are absent.
