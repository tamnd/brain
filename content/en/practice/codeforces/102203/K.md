---
title: "CF 102203K - \u041f\u0435\u0440\u0435\u0445\u0432\u0430\u0442"
description: "There are (n) distinct agents and (m) distinct spaceports. Each agent must be assigned to exactly one spaceport, and every spaceport must receive at least one agent."
date: "2026-08-18T00:53:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "K"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 72
verified: true
draft: false
---

[CF 102203K - \u041f\u0435\u0440\u0435\u0445\u0432\u0430\u0442](https://codeforces.com/problemset/problem/102203/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) distinct agents and (m) distinct spaceports. Each agent must be assigned to exactly one spaceport, and every spaceport must receive at least one agent. Agents assigned to the same spaceport are allowed, so the task is to count all surjective functions from the set of agents to the set of spaceports.

The agents are distinct. For example, with (n=2) and (m=2), the two valid assignments are agent 1 to port 1 and agent 2 to port 2, or the other way around. The answer is thus 2.

We need the answer modulo (998244353). Both (n) and (m) can reach 250000, so an (O(nm)) dynamic programming solution would require about (6.25\cdot10^{10}) operations and is completely infeasible. Even (O(m^2)) is too large. With a one-second limit, the intended solution needs to be essentially linear apart from a small logarithmic factor.

There are several boundary cases that a careless implementation can mishandle. If there are more spaceports than agents, for example (n=2,m=3), no assignment can cover all three ports, so the answer is 0. A formula involving factorials or inclusion-exclusion must handle this before doing any division.

When there is exactly one spaceport, every agent has only one possible destination. Thus (n=5,m=1) has answer 1. An implementation that accidentally starts an inclusion-exclusion loop from the wrong endpoint can produce 0 here.

When (n=m), every spaceport must contain exactly one agent, so the answer is (n!). For (n=2,m=2), this gives 2. For (n=1,m=1), it gives 1. This case is also useful for checking whether the final inclusion-exclusion sign and binomial coefficients are handled correctly.

## Approaches

A direct brute-force solution could consider every possible destination of every agent. Each of the (n) agents has (m) choices, so there are (m^n) assignments to inspect. For every assignment we would then check whether all (m) spaceports were used. The number of generated assignments is already (250000^{250000}) in the largest case, so this approach fails before the checking cost even matters.

The brute-force works because it explicitly enumerates exactly the objects we want to count. The problem is that most of those objects are invalid, and there is no reason to inspect them individually.

The key observation is that the condition "every spaceport is used" can be handled by inclusion-exclusion. Start with all (m^n) assignments, without requiring any port to be occupied. Then subtract assignments where at least one particular port is empty. If two particular ports are forced to be empty, there are only (m-2) possible destinations for every agent, giving ((m-2)^n) assignments. Continuing this process gives an alternating sum.

If exactly (k) spaceports are chosen to be forbidden, there are (\binom{m}{k}) ways to choose them and ((m-k)^n) assignments avoiding them. Inclusion-exclusion consequently gives

[
\sum_{k=0}^{m}(-1)^k\binom{m}{k}(m-k)^n.
]

When (m>n), the answer is immediately zero. Otherwise, we need only (m+1) terms. Each power can be computed with modular exponentiation in (O(\log n)), while all binomial coefficients can be generated in linear time using factorials and inverse factorials.

Since the modulus is prime and (m<998244353), every integer from 1 through (m) has a modular inverse. We precompute factorials and inverse factorials, then obtain

\frac{m!}{k!(m-k)!}
\pmod {998244353}.
]

An even simpler implementation generates consecutive binomial coefficients from

\binom{m}{k}\frac{m-k}{k+1}.
]

For that recurrence we precompute modular inverses of (1,2,\ldots,m). This keeps the whole implementation linear in memory and avoids storing factorial arrays.

The comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m^n)) | (O(n+m)) | Too slow |
| Inclusion-exclusion | (O(m\log n)) | (O(m)) | Accepted |

## Algorithm Walkthrough

1. Read (n) and (m). If (m>n), output 0 immediately. There are not enough agents to place at least one agent in every spaceport.
2. Precompute modular inverses for all integers from 1 through (m). Since the modulus is prime, the inverse of (i) can be obtained using

MOD-\left\lfloor\frac{MOD}{i}\right\rfloor
\operatorname{inv}(MOD\bmod i)
\pmod {MOD}.
]

The whole array is computed in (O(m)) time.

1. Start with the binomial coefficient (\binom{m}{0}=1). For the current (k), compute

[
\binom{m}{k}(m-k)^n
]

using modular exponentiation.

1. Add the term when (k) is even and subtract it when (k) is odd. This is exactly the inclusion-exclusion sign, because choosing (k) forbidden spaceports means counting assignments that avoid all of them.
2. Update the binomial coefficient using

\binom{m}{k}(m-k)\operatorname{inv}(k+1)
\pmod {MOD}.
]

This avoids computing factorials separately for every term.

1. Continue through (k=m), maintaining the answer modulo (998244353). Since (n\ge1), the (k=m) term contains (0^n=0), so it contributes nothing. Including it anyway makes the formula uniform.

### Why it works

For every subset (S) of spaceports, consider assignments in which every port in (S) is empty. If (|S|=k), every agent has exactly (m-k) available destinations, so there are ((m-k)^n) such assignments. There are (\binom{m}{k}) choices for (S).

Inclusion-exclusion adds assignments avoiding zero specified ports, subtracts assignments where one port is empty, adds back assignments where two ports are empty, and so on. An assignment using every spaceport belongs only to the (k=0) term. Any assignment missing exactly (r>0) spaceports appears with total coefficient

# (1-1)^r

1. 

]

Thus every invalid assignment cancels completely, while every valid assignment remains exactly once. The resulting sum is precisely the required number of distributions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, m = map(int, input().split())

    if m > n:
        print(0)
        return

    # Modular inverses of 1..m.
    inv = [0] * (m + 1)
    if m >= 1:
        inv[1] = 1

    for i in range(2, m + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    # C(m, 0)
    comb = 1
    ans = 0

    for k in range(m):
        ways = pow(m - k, n, MOD)
        term = comb * ways % MOD

        if k & 1:
            ans -= term
        else:
            ans += term

        if ans >= MOD:
            ans -= MOD
        elif ans < 0:
            ans += MOD

        # C(m, k + 1) from C(m, k)
        comb = comb * (m - k) % MOD
        comb = comb * inv[k + 1] % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The first branch handles the structural impossibility (m>n). Returning immediately is also useful because the rest of the formula would require modular inverses only up to (m), while no valid distribution exists anyway.

The inverse array uses the standard prime-modulus recurrence. The expression `MOD % i` is always smaller than `i`, so its inverse has already been computed when processing `i`.

The variable `comb` stores the current value of (\binom{m}{k}). It starts at 1, corresponding to (k=0), and is updated only after processing the current term. The order matters because the current term must use (\binom{m}{k}), not (\binom{m}{k+1}).

The loop stops at `range(m)`, which processes (k=0,\ldots,m-1). The omitted (k=m) term is (0^n=0), because (n\ge1), so omitting it changes nothing. This also avoids relying on how a power implementation handles the special expression (0^n).

Python's `pow(base, exponent, MOD)` performs modular exponentiation directly, so the intermediate values never become as large as the ordinary integer (base^n). The answer and all binomial coefficients are reduced modulo `MOD` after every multiplication.

## Worked Examples

### Sample 1: (n=2,m=2)

The formula counts assignments of two agents to two ports while excluding assignments that leave a port empty.

| (k) | (\binom{2}{k}) | (2-k) | ((2-k)^2) | Signed term | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 2 | 4 | +4 | 4 |
| 1 | 2 | 1 | 1 | -2 | 2 |

The (k=2) term is (0^2=0). The final answer is 2, corresponding to the two permutations of the agents between the two ports. The inclusion-exclusion cancellation removes the two assignments in which both agents go to the same port.

### Sample 2: (n=3,m=7)

There are seven ports but only three agents.

| Stage | (n) | (m) | Decision | Answer |
| --- | --- | --- | --- | --- |
| Input | 3 | 7 | (m>n) | 0 |

The algorithm returns immediately. At least seven agents would be required to put one agent into each of seven distinct ports, so no assignment can satisfy the condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\log n)) | There are (O(m)) inclusion-exclusion terms, each using modular exponentiation in (O(\log n)), plus (O(m)) inverse preprocessing |
| Space | (O(m)) | The modular inverse array contains (m+1) integers |

With (m\le250000), the linear preprocessing is small, and modular exponentiation uses only logarithmically many multiplication steps per term. This is dramatically smaller than the (O(m^2)) or (O(mn)) work that the constraints rule out.

## Test Cases

```python
import sys
import io

MOD = 998244353

def solve():
    n, m = map(int, sys.stdin.readline().split())

    if m > n:
        print(0)
        return

    inv = [0] * (m + 1)
    inv[1] = 1

    for i in range(2, m + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    comb = 1
    ans = 0

    for k in range(m):
        term = comb * pow(m - k, n, MOD) % MOD

        if k & 1:
            ans -= term
        else:
            ans += term

        ans %= MOD

        comb = comb * (m - k) % MOD
        comb = comb * inv[k + 1] % MOD

    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("2 2\n") == "2", "sample 1"
assert run("3 7\n") == "0", "sample 2"

# Minimum-size input
assert run("1 1\n") == "1", "single agent and single port"

# More agents than ports
# Number of onto functions from 4 agents to 2 ports:
# 2^4 - C(2,1)*1^4 = 16 - 2 = 14.
assert run("4 2\n") == "14", "four agents, two ports"

# Exactly as many agents as ports: every agent must occupy
# a different port, so the answer is 5!.
assert run("5 5\n") == "120", "equal numbers"

# Maximum-size input.
# When n == m, the answer is n! modulo MOD.
expected = 1
for x in range(1, 250001):
    expected = expected * x % MOD

assert run("250000 250000\n") == str(expected), "maximum-size equal case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum input and the single-spaceport boundary |
| `4 2` | `14` | Nontrivial inclusion-exclusion with repeated assignments allowed |
| `5 5` | `120` | Boundary (n=m), where the answer becomes (n!) |
| `250000 250000` | (250000!\bmod 998244353) | Maximum input size and large modular arithmetic |

## Edge Cases

For (n=2,m=3), the algorithm enters the first condition because there are more ports than agents. It prints `0` without constructing the inverse array. This is the correct result because covering three distinct ports requires at least three agents.

For (n=5,m=1), the inverse array contains only `inv[1]=1`. The loop has one iteration, corresponding to (k=0). It adds (1^5=1), giving the correct answer `1`. Every agent must go to the only available port.

For (n=1,m=1), the same calculation gives (1^1=1). This confirms that the smallest possible input does not require a special formula beyond the general algorithm.

For (n=m=2), the inclusion-exclusion calculation is

# 4-2

1. 

]

The four unrestricted assignments consist of two valid assignments and two assignments where both agents use the same port. The second term removes exactly those two invalid assignments.

For (n=m) in general, every valid distribution has exactly one agent at each port. The agents can be permuted arbitrarily, giving (n!) valid assignments. The inclusion-exclusion formula produces exactly this value, so the (n=m) boundary also provides a strong check on the alternating signs and binomial recurrence.

The implementation also avoids an off-by-one problem at (k=m). That final term would contain (0^n), which is zero because (n\ge1), so processing only (k=0) through (m-1) is mathematically complete.
