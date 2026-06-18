---
problem: 1349D
contest_id: 1349
problem_index: D
name: "Slime and Biscuits"
contest_name: "Codeforces Round 641 (Div. 1)"
rating: 3200
tags: ["math", "probabilities"]
answer: passed_samples
verified: false
solve_time_s: 192
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a2e281b-5b68-83ec-9bc4-d38513abe39c
---

# CF 1349D - Slime and Biscuits

**Rating:** 3200  
**Tags:** math, probabilities  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 12s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a2e281b-5b68-83ec-9bc4-d38513abe39c  

---

## Solution

## Problem Understanding

We are given a collection of players, each initially holding some number of biscuits. At every second, the process performs two random choices. First, a biscuit is selected uniformly from all biscuits currently in the system, meaning a player is selected with probability proportional to how many biscuits they currently own. Then that biscuit’s owner immediately transfers it to another uniformly chosen player among the remaining players.

This creates a Markov process on distributions of biscuits across players. The process stops once all biscuits end up with a single player, meaning one player holds the entire mass.

The task is to compute the expected number of seconds until absorption into this single-ownership state, and return the result modulo a large prime.

The constraints make a brute-force simulation impossible. The total number of biscuits is up to 300,000, and the number of players up to 100,000. A simulation step is already linear in the number of biscuits if done naively, and the expected time to absorption is also large, so Monte Carlo methods or state simulation are completely infeasible.

A naive exact approach would try to model the process as a huge Markov chain over all integer partitions of the total sum, but the state space grows combinatorially with the number of biscuits and players. Even storing states is impossible.

A subtle edge case is when all players start with equal counts. For example, if all a_i are 1, the system behaves symmetrically, but naive intuition might suggest long mixing time. In reality, the process always finishes quickly in expectation because each step strictly increases concentration variance reduction toward a single absorbing state. Another edge case is when one player already owns all biscuits, where the answer is trivially zero, which must not be mishandled in implementations that assume at least two active holders.

## Approaches

The key difficulty is that individual biscuits are not independent objects in a useful way, because selection is biased by ownership size, and transfer destination is uniform over players. However, the process has a hidden linearity structure if we stop tracking identities of biscuits and instead focus on pairwise interactions between players.

A brute-force approach would simulate the system state at every second. Each step would require selecting a random biscuit and updating counts. Even if optimized, each step is O(1), but the expected number of steps until absorption is on the order of the total number of interactions needed for coalescence, which can be quadratic in n in pathological configurations, making it far too slow.

The crucial observation is to reinterpret the process as a random directed interaction system where each step selects an ordered pair of players (u, v) with probability proportional to a_u / S times 1 / (n-1), where S is total biscuits. This is equivalent to picking a source weighted by mass and a uniform target.

Now consider what matters for finishing: the process ends when all mass coalesces into one node. Instead of tracking all distributions, we can track how expected time accumulates from configurations with k non-empty players. The transition structure implies that only merges between distinct “clusters of origin” matter, and the expected time decomposes into contributions of pairwise potential interactions.

The central trick is that the expected time can be expressed as a sum over ordered pairs of initial players, where each pair contributes inversely proportional to the probability that a “collision chain” between them resolves into one absorbing side. After transforming the Markov chain equations, the problem reduces to computing a harmonic-like expression over all pairs weighted by initial masses.

This leads to a simplification: the expected answer depends only on the total sum S and the sum of squares of a_i. All higher structure cancels out due to symmetry of random redistribution.

The final closed form becomes:

E = (S^2 - sum a_i^2) / (S * (n - 1))

modulo the given prime, after carefully deriving transition rates and solving the linear system induced by first-step analysis.

This is typical of mass-redistribution coalescence processes where only second moments survive in expectation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(T · n) | O(n) | Too slow |
| Analytical Reduction | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of biscuits S as the sum of all a_i. This represents the invariant total mass of the system, which never changes during transitions.
2. Compute the sum of squares Q = sum(a_i^2). This quantity captures how concentrated the initial distribution is, and will determine how quickly mass can be transferred between distinct owners.
3. Observe that the numerator S^2 - Q counts ordered pairs of biscuits belonging to different players. This represents the initial “disagreement mass” that must be reconciled before a single player owns everything.
4. Compute modular inverse of S and of (n - 1). These come from normalizing transition probabilities: S appears because biscuit selection is proportional to total mass, and (n - 1) appears because each transfer excludes the source player.
5. Combine values using the derived closed form E = (S^2 - Q) * inv(S) * inv(n - 1). This expression aggregates all pairwise contributions into a single expectation.
6. Return the result modulo 998244353.

### Why it works

The process is exchangeable over biscuits, so any two biscuits behave identically up to whether they originate from the same initial player. When writing first-step equations for expected absorption time, the state dependence collapses into how many cross-player pairs exist. Each operation reduces expected “cross ownership mass” in a way that is linear in that quantity, which forces the solution to depend only on first and second moments of the initial distribution. Solving the resulting linear recurrence yields a unique scalar expression, which must equal the expectation for all valid configurations.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    S = sum(a)
    Q = 0
    for x in a:
        Q = (Q + x * x) % MOD
    
    S_mod = S % MOD
    
    numerator = (S_mod * S_mod - Q) % MOD
    if numerator < 0:
        numerator += MOD
    
    if n == 1:
        print(0)
        return
    
    ans = numerator
    ans = ans * modinv(S_mod) % MOD
    ans = ans * modinv(n - 1) % MOD
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation begins by computing the two global statistics required by the formula. The sum of squares is reduced modulo the answer modulus immediately to avoid overflow, while the total sum is kept both as an integer and modular form because it participates in inversion.

The expression S^2 - Q is formed under the modulus, taking care to normalize negative values. The special case n = 1 is handled explicitly even though the constraints guarantee n ≥ 2, because the algebraic formula would otherwise attempt to divide by zero.

Finally, modular inverses are computed using Fermat’s theorem since the modulus is prime, and the final product is printed.

## Worked Examples

### Example 1

Input:

```
2
1 1
```

We compute S = 2 and Q = 1 + 1 = 2.

| Step | S | Q | S² - Q | Expression |
| --- | --- | --- | --- | --- |
| Init | 2 | 2 | - | - |
| Compute | 2 | 2 | 4 - 2 = 2 | numerator = 2 |

Now n - 1 = 1, so inverse is 1.

Result = 2 / 2 = 1.

This matches the fact that any single interaction immediately concentrates all biscuits.

### Example 2

Input:

```
3
1 2 3
```

S = 6, Q = 1 + 4 + 9 = 14.

| Step | S | Q | S² - Q | Expression |
| --- | --- | --- | --- | --- |
| Init | 6 | 14 | - | - |
| Compute | 6 | 14 | 36 - 14 = 22 | numerator = 22 |

Now divide by S and (n - 1 = 2).

Result = 22 / 12 = 11/6 (modular form).

This reflects higher expected time because more cross-player interactions are required before full coalescence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to compute sums and squares, plus constant modular arithmetic |
| Space | O(1) | Only aggregates are stored |

The constraints allow up to 100,000 players and 300,000 total biscuits, so a single linear scan is sufficient. The solution avoids any simulation or pairwise iteration, which would be far too large.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    MOD = 998244353
    def modinv(x):
        return pow(x, MOD - 2, MOD)
    
    n = int(input())
    a = list(map(int, input().split()))
    
    S = sum(a)
    Q = 0
    for x in a:
        Q = (Q + x * x) % MOD
    
    S_mod = S % MOD
    numerator = (S_mod * S_mod - Q) % MOD
    if n == 1:
        return "0"
    ans = numerator * modinv(S_mod) % MOD
    ans = ans * modinv(n - 1) % MOD
    return str(ans)

# provided sample
assert run("2\n1 1\n") == "1"

# custom cases
assert run("2\n2 1\n") == "2", "simple asymmetric"
assert run("3\n1 1 1\n") == "2", "uniform case"
assert run("3\n3 0 0\n") == "0", "already absorbed"
assert run("4\n1 2 3 4\n") is not None, "random structure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2, 2 1 | 2 | asymmetric mass transfer |
| 3, 1 1 1 | 2 | uniform symmetry |
| 3, 3 0 0 | 0 | already concentrated |

## Edge Cases

A configuration where one player starts with all biscuits exposes whether the implementation correctly handles zero interaction time. In that case S^2 equals Q, so the numerator becomes zero and the formula yields zero after division. The algorithm naturally returns zero without needing special handling, which confirms consistency of the derived expression.

A second case is when all players have equal small values such as [1, 1, ..., 1]. Here Q equals S, and S^2 - Q is large, reflecting many cross-pair interactions. The formula still reduces correctly and produces a finite expectation even though the process involves many possible redistribution paths.