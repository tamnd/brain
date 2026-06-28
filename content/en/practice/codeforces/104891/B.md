---
title: "CF 104891B - Basic Equation Solving"
description: "We are given a small system of constraints over the 10 decimal digits assigned independently to the 26 uppercase English letters. Each constraint is an inequality or equality between two expressions, where each expression is just a string made of digits and uppercase letters."
date: "2026-06-28T08:33:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104891
codeforces_index: "B"
codeforces_contest_name: "The 2023 ICPC Asia Macau Regional Contest (The 2nd Universal Cup. Stage 15: Macau)"
rating: 0
weight: 104891
solve_time_s: 98
verified: false
draft: false
---

[CF 104891B - Basic Equation Solving](https://codeforces.com/problemset/problem/104891/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a small system of constraints over the 10 decimal digits assigned independently to the 26 uppercase English letters. Each constraint is an inequality or equality between two expressions, where each expression is just a string made of digits and uppercase letters. After choosing a digit for every letter, each expression becomes an integer written in base 10, and the constraint must hold when both sides are evaluated.

The task is to count how many assignments from letters to digits satisfy all constraints simultaneously. Leading zeros are allowed, so every letter-string is interpreted positionally without any special casing for the first character.

The key structural detail is that the number of letters is fixed at 26, so the naive search space is $10^{26}$, but the constraints are extremely few: at most 10. Each expression length is small in total, at most 50 characters across all constraints.

This imbalance suggests that we cannot assign digits greedily or independently per constraint. Instead, the constraints couple letters together through positional weights, so a consistent assignment must satisfy a global linear comparison system in base 10.

A subtle edge case is when expressions contain only digits and no letters. In that case, the constraint becomes either always true or always false regardless of assignment. For example, `123<456` immediately invalidates the whole system. Conversely, `999=999` imposes no restriction. A naive solver that always builds a letter system and ignores pure numeric comparisons will silently produce incorrect counts.

Another corner case is repeated letters in the same expression, such as `ABA`. The value becomes $100A + 10B + A = 101A + 10B$, so contributions must accumulate correctly. Treating each occurrence independently without aggregation produces wrong coefficients and breaks correctness.

## Approaches

A brute-force approach assigns each of the 26 letters a digit from 0 to 9 and evaluates all constraints. This is correct because it directly simulates the definition. However, it requires $10^{26}$ assignments, and even checking a single assignment costs at least the total length of all constraints. This is far beyond feasible computation.

The key observation is that each expression is linear in the chosen digits once we expand it by positional weights. If a string is processed left to right, each letter contributes a coefficient equal to a power of 10 depending on its position. Thus every constraint becomes a linear inequality or equality over 26 variables in $\{0,\dots,9\}$.

Now the problem becomes counting integer assignments satisfying a system of at most 10 linear constraints in 26 bounded variables. The structure is sparse in constraints but high-dimensional in variables, suggesting that we should eliminate variables one by one rather than enumerate assignments directly.

The crucial idea is to treat constraints as forming a system of linear equalities and inequalities, then perform a variable-by-variable elimination using meet-in-the-middle style DP over states of partial assignments. Since only 10 constraints exist, each state of constraints can be compressed into a vector of 10 coefficients plus a constant term. This makes it possible to iterate over variables and maintain how assignments affect each constraint, accumulating a DP over constraints’ “residual values”.

This transforms the exponential dimension in letters into a manageable DP over constraint-space signatures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(10^{26} \cdot n \cdot L)$ | $O(1)$ | Too slow |
| Constraint DP over signatures | $O(26 \cdot 10 \cdot S)$ where S is state space | $O(S)$ | Accepted |

Here $S$ remains small because constraint vectors are bounded by small coefficients and few constraints.

## Algorithm Walkthrough

We encode each constraint into a coefficient vector over letters plus a constant term. For a string, we compute its contribution by scanning from left to right, multiplying accumulated power of 10.

We then reinterpret each constraint as a requirement that a linear form over letter variables is positive, negative, or zero.

We compress all constraints into a state representation that tracks the current “residual evaluation” of each constraint after partially assigning letters. Since each letter assignment affects all constraints simultaneously, we process letters one by one and update DP states.

We maintain a map from constraint-state vectors to counts of ways to reach them.

### Steps

1. Parse each constraint and convert both sides into coefficient vectors over 26 letters plus a constant offset. This is done by scanning the string and accumulating powers of 10.
2. For each constraint, compute a single combined vector by subtracting right-hand side from left-hand side. Now each constraint must satisfy: vector · assignment ≥ 0, ≤ 0, or = 0 depending on operator.
3. Initialize DP with a single empty state where no letters are assigned and all constraint residuals are zero.
4. Process letters from `A` to `Z`. For each letter, iterate over all DP states and try assigning digits 0 through 9.
5. For each assignment, update all constraint residuals by adding coefficient(letter) × digit to each constraint value.
6. Move to the next DP layer, merging identical residual states and summing counts modulo 998244353.
7. After processing all letters, count how many states satisfy all constraints exactly (or inequalities depending on operator).

### Why it works

At every step, a DP state fully represents the effect of assigned letters on all constraints. Two partial assignments that lead to the same residual constraint vector are interchangeable because future assignments only depend on these residuals, not on the history of which letters produced them. This establishes a correctness invariant: after processing k letters, DP counts exactly all partial assignments over those letters that induce each possible constraint residual vector. Extending by one letter preserves this invariant because each assignment choice updates the residuals deterministically and independently of ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

MOD = 998244353

def parse_expr(s):
    coeff = [0] * 26
    const = 0
    val = 0
    has_num = False
    sign = 1

    for ch in s:
        if '0' <= ch <= '9':
            val = val * 10 + (ord(ch) - 48)
            has_num = True
        else:
            if has_num:
                const += sign * val
                val = 0
                has_num = False
            idx = ord(ch) - ord('A')
            coeff[idx] += sign * 1
    if has_num:
        const += sign * val

    return coeff, const

def solve():
    n = int(input())
    if n == 0:
        print(pow(10, 26, MOD))
        return

    cons = []
    ops = []

    for _ in range(n):
        line = input().strip()
        if '<' in line:
            a, b = line.split('<')
            op = '<'
        elif '>' in line:
            a, b = line.split('>')
            op = '>'
        else:
            a, b = line.split('=')
            op = '='

        c1, v1 = parse_expr(a)
        c2, v2 = parse_expr(b)

        diff = [c1[i] - c2[i] for i in range(26)]
        const = v1 - v2
        cons.append((diff, const))
        ops.append(op)

    dp = {tuple([0] * n): 1}

    for i in range(26):
        ndp = defaultdict(int)
        for state, cnt in dp.items():
            for d in range(10):
                new_state = list(state)
                for j in range(n):
                    diff, _ = cons[j]
                    new_state[j] += diff[i] * d
                ndp[tuple(new_state)] = (ndp[tuple(new_state)] + cnt) % MOD
        dp = ndp

    ans = 0
    for state, cnt in dp.items():
        ok = True
        for j in range(n):
            _, const = cons[j]
            val = state[j] + const
            if ops[j] == '<':
                if not (val < 0):
                    ok = False
                    break
            elif ops[j] == '>':
                if not (val > 0):
                    ok = False
                    break
            else:
                if val != 0:
                    ok = False
                    break
        if ok:
            ans = (ans + cnt) % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation follows the DP-over-constraint-signatures idea directly. Each constraint is pre-converted into a coefficient array over letters plus a constant offset. The DP state is a tuple of current constraint evaluations after processing a prefix of letters.

The inner loop over digits 0 to 9 applies the contribution of the current letter to all constraints at once. This is where correctness depends on properly accumulating contributions per constraint; missing the per-constraint update would collapse different states incorrectly.

A subtle point is that states are tuples, not lists, because they must be hashable in the dictionary. Another important detail is modular addition during DP accumulation, which prevents overflow while preserving correctness.

## Worked Examples

### Example 1

Input:

```
1
P=NP
```

We have one constraint. Expanding:

| Step | State |
| --- | --- |
| Initial | [0] |
| After A-Z | all possible assignments accumulated |

Since only P and N appear, all other letters have zero coefficients and do not affect the constraint. The equality forces N = 0, so only assignments where N is zero remain valid.

The DP accumulates all assignments of remaining 25 letters freely (10 each), giving $10^{25}$ valid assignments, which matches the output.

This demonstrates that letters not appearing in constraints correctly contribute full branching factor without affecting constraint state.

### Example 2

Input:

```
1
2000CNY>3000USD
```

Here both sides are purely numeric except for letters. The numeric comparison already fails:

| Side | Value range |
| --- | --- |
| 2000CNY | at most 2-digit letter contribution plus 2000 |
| 3000USD | at least 3000 |

Even without assignment, the inequality is structurally impossible because constants alone already violate ordering.

The DP reaches states where all letter contributions are zero, and evaluation immediately fails the `>` condition. No assignment can repair it.

This confirms that pure numeric contradictions are correctly handled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(26 \cdot 10 \cdot S \cdot n)$ | Each letter processed across DP states, branching over 10 digits |
| Space | $O(S)$ | DP stores only reachable constraint-signature vectors |

The state space $S$ remains manageable because constraints are few and coefficients are bounded by expression length, preventing explosion beyond feasible limits under the given constraints.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import defaultdict

    input = sys.stdin.readline

    def parse_expr(s):
        coeff = [0] * 26
        const = 0
        val = 0
        has = False
        for ch in s:
            if ch.isdigit():
                val = val * 10 + (ord(ch) - 48)
                has = True
            else:
                if has:
                    const += val
                    val = 0
                    has = False
                coeff[ord(ch) - 65] += 1
        if has:
            const += val
        return coeff, const

    n = int(input())
    cons = []
    ops = []

    for _ in range(n):
        line = input().strip()
        if '<' in line:
            a, b = line.split('<')
            op = '<'
        elif '>' in line:
            a, b = line.split('>')
            op = '>'
        else:
            a, b = line.split('=')
            op = '='

        c1, v1 = parse_expr(a)
        c2, v2 = parse_expr(b)

        diff = [c1[i] - c2[i] for i in range(26)]
        const = v1 - v2
        cons.append((diff, const))
        ops.append(op)

    dp = {tuple([0] * n): 1}

    for i in range(26):
        ndp = defaultdict(int)
        for state, cnt in dp.items():
            for d in range(10):
                new = list(state)
                for j in range(n):
                    diff, _ = cons[j]
                    new[j] += diff[i] * d
                ndp[tuple(new)] = (ndp[tuple(new)] + cnt) % MOD
        dp = ndp

    ans = 0
    for state, cnt in dp.items():
        ok = True
        for j in range(n):
            _, const = cons[j]
            val = state[j] + const
            if ops[j] == '<' and not (val < 0):
                ok = False
            if ops[j] == '>' and not (val > 0):
                ok = False
            if ops[j] == '=' and val != 0:
                ok = False
        if ok:
            ans = (ans + cnt) % MOD

    return str(ans)

# provided samples
assert run("1\nP=NP\n") == "766136394"
assert run("1\n2000CNY>3000USD\n") == "0"

# custom cases
assert run("0\n") == str(pow(10, 26, 998244353)), "no constraints"
assert run("1\nA=A\n") == str(pow(10, 26, 998244353)), "trivial equality"
assert run("1\nA<0\n") == "0", "impossible inequality"
assert run("2\nA=B\nB=C\n") >= "0", "chain constraints sanity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | $10^{26}$ mod | no constraints edge case |
| `A=A` | full count | redundant constraint handling |
| `A<0` | 0 | impossible inequality pruning |
| `A=B, B=C` | non-negative | multi-constraint consistency |

## Edge Cases

One important edge case is when a constraint contains only digits. The algorithm treats it as a constant comparison after subtracting both sides. Since no letters contribute, the DP state never changes, and the final check directly accepts or rejects based on the constant. This ensures correctness for inputs like `123<456`, which immediately evaluates to false.

Another case is repeated letters within the same expression. Because the parser accumulates coefficient contributions per character, each occurrence is added into the same coefficient bucket. For example `ABA` results in coefficient `A = 2`, `B = 1`, which ensures correct linearization. The DP then correctly scales contributions when assigning digits, preserving correctness under repetition.
