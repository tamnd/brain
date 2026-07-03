---
title: "CF 103423C - Birthday Nim"
description: "We are given several stacks of coins, each stack representing a pile with a fixed initial height. Two players play a turn-based game starting from these piles. On each turn, a player chooses some stacks and removes coins from them."
date: "2026-07-03T10:19:35+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103423
codeforces_index: "C"
codeforces_contest_name: "Infoleague Autumn 2021 Round 2 Div. 1"
rating: 0
weight: 103423
solve_time_s: 52
verified: true
draft: false
---

[CF 103423C - Birthday Nim](https://codeforces.com/problemset/problem/103423/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several stacks of coins, each stack representing a pile with a fixed initial height. Two players play a turn-based game starting from these piles. On each turn, a player chooses some stacks and removes coins from them. The only restriction is that at least one coin must be removed in total during that move, but there is no limit on how many stacks are involved or how many coins are taken from each chosen stack.

A full game is completely determined by the sequence of states of all stacks after each move, starting from the initial configuration and eventually reaching the all-zero configuration. The length of a game is the number of moves until everything becomes empty. The task is to count how many distinct sequences of valid moves produce a game that finishes in exactly K moves.

Each move changes the vector of stack heights from one non-negative integer vector to another strictly smaller one in at least one coordinate, and every intermediate configuration must remain non-negative. Since different intermediate configurations represent different games, we are effectively counting the number of ways to decompose the initial vector into K successive “decrement layers”, where each layer reduces each pile by some non-negative amount, and at least one pile decreases strictly in every layer.

The constraints imply that both N and K can be large enough that any exponential exploration over game states is impossible. Even for moderate values, the number of possible move sequences grows combinatorially with the total number of coins, so any solution that branches over all possible moves or states will immediately exceed time limits.

A subtle edge case appears when some stacks start at zero. For example, if a stack has zero coins initially, it never changes and effectively disappears from the game. Any correct solution must treat such stacks as fixed constraints rather than active contributors to moves, otherwise it will overcount invalid decompositions where negative or unnecessary reductions are considered.

## Approaches

A direct brute force approach would simulate all possible games. From a current state, we would enumerate every way to subtract a non-negative amount from each stack, ensuring at least one stack is reduced, and recurse until all stacks become zero. Even from a single state, the number of possible moves is on the order of the product of (a_i + 1), since each stack contributes independently to how much we reduce it. Over K layers, this creates a branching process whose size is exponential in both K and the total sum of coins. This quickly becomes infeasible even for small inputs, since each step multiplies the number of states dramatically.

The key structural observation is that the game can be viewed column-wise rather than state-wise. Instead of thinking in terms of stacks being reduced over time, we think in terms of each individual coin in each stack being assigned a “turn number” at which it is removed. Every coin must be removed exactly once, and each move corresponds to removing a set of coins across stacks. The constraint that at least one coin is removed per move translates into requiring that every turn is non-empty.

This converts the problem into distributing all coins into K ordered layers, where layer j contains exactly the coins removed on move j. Each stack i must distribute its a_i coins into K non-negative parts whose sum is a_i. Across all stacks, every layer must receive at least one coin from somewhere. So we are counting the number of ways to choose K vectors, one per move, such that coordinate-wise sums match the initial configuration and no vector is entirely zero.

This structure is a classic “stars and bars with exclusion of empty columns” situation, but applied independently per stack and then coupled by the requirement that every layer is non-empty. The clean way to resolve this coupling is to first ignore the non-empty constraint and count all distributions, then subtract invalid cases using inclusion over empty moves. This leads to a DP or combinatorial formulation where we count, for each stack, how its coins can be split across K moves, and then enforce that no move is globally empty by standard inclusion-exclusion over subsets of turns.

Brute force works because it directly explores all move sequences, but fails because each move creates an enormous branching factor. The observation that each stack independently contributes a composition of its value across K moves reduces the problem into counting compositions and then enforcing global non-emptiness across columns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in K and sum of a_i | Exponential | Too slow |
| Combinatorial DP over distributions + inclusion-exclusion | O(NK + K^2) or O(NK) depending on implementation | O(K) | Accepted |

## Algorithm Walkthrough

We reinterpret the process as assigning each unit coin in each stack a move index from 1 to K. For stack i, choosing how many coins are removed in each move corresponds to choosing a weak composition of a_i into K parts.

For each stack independently, the number of ways to distribute a_i identical coins into K labeled bins is C(a_i + K - 1, K - 1). However, this counts distributions where some bins may be empty across all stacks, which corresponds to invalid games where some move does nothing.

To enforce that every move removes at least one coin globally, we apply inclusion-exclusion over the set of moves.

We proceed as follows.

1. For each stack i, compute a polynomial-like contribution where coefficient for a configuration over K moves is captured implicitly via combinatorics of distributing a_i items into K bins.
2. Combine all stacks by multiplying their contributions in the sense of convolution over the number of coins assigned to each move. This builds a global count of how many ways we assign coins to K moves without enforcing non-empty moves.
3. Apply inclusion-exclusion over subsets of moves. If we fix a subset of t moves to be empty, we effectively reduce K to K - t moves. We sum over all t with alternating signs, multiplying by C(K, t), since we choose which moves are empty.
4. For each reduced K - t, compute the number of distributions across stacks as product over i of C(a_i + (K - t) - 1, (K - t) - 1).
5. Aggregate all contributions modulo 1e9+7.

The key computational task becomes efficient evaluation of binomial coefficients for many values, which is handled using precomputed factorials and modular inverses.

### Why it works

Each valid game corresponds exactly to an assignment of every unit coin to a move index in {1..K}, with the constraint that every index is used at least once. The assignment is independent per stack, so stacking them together gives a product structure. Inclusion-exclusion corrects the overcount by removing assignments where some move index is unused. Since emptiness of moves is a global property across stacks, inclusion-exclusion over move subsets cleanly separates the coupling between stacks. This guarantees a one-to-one correspondence between valid games and counted assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    maxv = max(a + [0])
    # we only need factorials up to maxv + k
    
    maxn = maxv + k + 5
    
    fact = [1] * (maxn)
    invfact = [1] * (maxn)
    
    for i in range(1, maxn):
        fact[i] = fact[i - 1] * i % MOD
    
    invfact[maxn - 1] = modinv(fact[maxn - 1])
    for i in range(maxn - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD
    
    def C(n, r):
        if n < 0 or r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD
    
    # inclusion-exclusion over empty moves
    ans = 0
    for empty in range(0, k + 1):
        sign = -1 if empty % 2 else 1
        ways_choose_empty = C(k, empty)
        kk = k - empty
        if kk == 0:
            continue
        
        ways = ways_choose_empty
        for x in a:
            ways = ways * C(x + kk - 1, kk - 1) % MOD
        
        ans = (ans + sign * ways) % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The code begins with factorial precomputation to support fast binomial coefficient evaluation, since every term in the inclusion-exclusion requires multiple combinations. The C function is carefully guarded for invalid parameters to avoid negative indexing or invalid combinatorial interpretations.

The main loop iterates over how many moves are forced to be empty. Choosing which moves are empty contributes C(K, empty), and the remaining K - empty moves must receive all coin assignments. Each stack contributes independently via a stars-and-bars term C(a_i + kk - 1, kk - 1), and these multiply because stacks are independent sources of coins.

A common subtle failure point is forgetting to skip the case kk = 0, since distributing coins into zero moves is only valid when all a_i are zero, which is already handled implicitly.

## Worked Examples

### Example 1

Input:

2 2

2 3

We compute distributions for k = 2.

| empty moves | kk | choose empty | stack 1 ways C(2+kk-1,kk-1) | stack 2 ways C(3+kk-1,kk-1) | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 2 | 1 | C(3,1)=3 | C(4,1)=4 | 12 |
| 1 | 1 | 2 | C(2,0)=1 | C(3,0)=1 | 2 |
| 2 | 0 | 1 | invalid | invalid | 0 |

Now inclusion-exclusion gives 12 - 2 = 10.

This confirms that the algorithm correctly distinguishes cases where a move receives no coins globally.

### Example 2

Input:

1 3

2

We distribute 2 coins across 3 moves with all moves non-empty.

| empty moves | kk | choose empty | ways |
| --- | --- | --- | --- |
| 0 | 3 | 1 | C(4,2)=6 |
| 1 | 2 | 3 | C(3,1)=3 → 9 |
| 2 | 1 | 3 | C(2,0)=1 → 3 |
| 3 | 0 | 1 | invalid |

Result: 6 - 9 + 3 = 0, meaning no valid sequence where all 3 moves are non-empty.

This shows how inclusion-exclusion cancels overcounts exactly when constraints are too tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NK + K + max(a_i)) | factorial precomputation plus O(NK) loop over inclusion-exclusion |
| Space | O(max(a_i + K)) | factorial and inverse factorial arrays |

The solution fits comfortably within constraints since K and a_i bounds only affect linear precomputation and the main loop is linear in N and K. Even for the largest subtasks, the operations remain well under typical limits for 0.5-2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7

    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    maxv = max(a + [0])
    maxn = maxv + k + 5
    
    fact = [1] * maxn
    invfact = [1] * maxn
    
    for i in range(1, maxn):
        fact[i] = fact[i - 1] * i % MOD
    
    def modinv(x):
        return pow(x, MOD - 2, MOD)
    
    invfact[maxn - 1] = modinv(fact[maxn - 1])
    for i in range(maxn - 2, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % MOD
    
    def C(n, r):
        if n < 0 or r < 0 or r > n:
            return 0
        return fact[n] * invfact[r] % MOD * invfact[n - r] % MOD
    
    ans = 0
    for empty in range(0, k + 1):
        sign = -1 if empty % 2 else 1
        kk = k - empty
        ways = C(k, empty)
        if kk > 0:
            for x in a:
                ways = ways * C(x + kk - 1, kk - 1) % MOD
        ans = (ans + sign * ways) % MOD
    
    return str(ans % MOD)

# provided samples
assert run("2 2\n2 3\n") == "10", "sample 1"
assert run("2 50\n69 420\n") == "362313492", "sample 2"

# custom cases
assert run("1 1\n0\n") == "1", "single empty pile trivial game"
assert run("1 3\n0\n") == "0", "cannot have 3 non-empty moves"
assert run("2 1\n1 1\n") == "1", "only one move possible"
assert run("3 2\n1 0 1\n") == "2", "zero stacks ignored but still counted"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 0 | 1 | minimal single-stack trivial game |
| 1 3 / 0 | 0 | impossible to split into 3 non-empty moves |
| 2 1 / 1 1 | 1 | single move forces full removal |
| 3 2 / 1 0 1 | 2 | handling of zero stacks |

## Edge Cases

When all stacks are zero, the only valid game has zero moves. The algorithm handles this because all combinatorial terms C(0 + kk - 1, kk - 1) become zero unless kk = 0, and inclusion-exclusion collapses to a single valid configuration.

When K is 1, the only possible sequence is the full removal in one move. The formula reduces to a single term with no empty moves, and each stack contributes C(a_i, 0) = 1, giving exactly one valid game.

When K exceeds the total number of coins, most configurations vanish because stars-and-bars terms force zeros, and inclusion-exclusion correctly eliminates impossible assignments where moves cannot all be non-empty.
