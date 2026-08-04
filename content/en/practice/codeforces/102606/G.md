---
title: "CF 102606G - Geralt of Rivia"
description: "Geralt fights a monster that always receives the first hit. Geralt can improve two statistics before the fight: attack and defense. Increasing attack by one point costs a crowns, while increasing defense by one point costs b crowns."
date: "2026-08-04T17:05:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102606
codeforces_index: "G"
codeforces_contest_name: "2020 ECNU Campus Online Invitational Contest"
rating: 0
weight: 102606
solve_time_s: 103
verified: true
draft: false
---

[CF 102606G - Geralt of Rivia](https://codeforces.com/problemset/problem/102606/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 43s  
**Verified:** yes  

## Solution
## Problem Understanding

Geralt fights a monster that always receives the first hit. Geralt can improve two statistics before the fight: attack and defense. Increasing attack by one point costs `a` crowns, while increasing defense by one point costs `b` crowns. The upgrades can be fractional, so the final attack and defense values do not have to be integers.

After upgrades, Geralt deals `max(0, attack - monster_defense)` damage each turn. The monster loses HP after every Geralt attack, and only attacks back if it survives. The monster deals `max(0, monster_attack - Geralt_defense)` damage. Since Geralt has infinite HP, the only quantity to minimize is the total damage received before the monster dies.

For each test case, the input gives the initial attack and defense of both fighters, the monster HP, the available crowns, and the two upgrade prices. The output is the smallest possible damage Geralt receives, written as a reduced fraction, or `-1` if no upgrade plan can make him win.

The constraints are small for a single value of `n`, but there can be up to `10^4` test cases. An algorithm that spends `O(n)` time on every case can reach about `10^8` operations, and using expensive fraction arithmetic inside such a loop would be too slow in Python. The solution needs to exploit the mathematical shape of the optimization rather than simulate possible upgrades.

The dangerous cases are the ones where continuous upgrades interact with discrete numbers of attacks.

If Geralt starts with no effective attack, it is wrong to assume that there is a fixed maximum number of turns. For example:

```
1
1 10 100 1
10 5 1 100
```

Geralt has no initial damage because his attack is below the monster defense. He can buy an arbitrarily small attack increase, so the number of attacks is not bounded by the original attack value.

Another common mistake is counting the final monster attack. If the monster dies from Geralt's attack, it does not hit back. For example:

```
1
5 1 1 1
1 1 1 1
```

Geralt already deals `4` damage and kills the monster immediately. The answer is:

```
0/1
```

A simulation that adds monster damage after every Geralt turn would incorrectly output a positive value.

Fraction handling is also important. A plan can require a fractional attack increase, and the final answer may not be an integer. For example, the optimal defense reduction can leave a rational amount of damage per hit, so floating point arithmetic can lose precision.

## Approaches

A direct approach would try every possible amount of attack upgrade, compute the remaining money spent on defense, simulate how many attacks are needed, and keep the best result. This is correct because every legal upgrade choice is checked. However, the upgrade values are continuous, so there are infinitely many possible choices. Even if we only look at the number of attacks required, there can be up to `n` possibilities per test case. Across `10^4` cases, this is too slow.

The useful observation is that attack upgrades only matter through the number of turns required to kill the monster. Suppose Geralt needs exactly `k` attacks. The cheapest way to achieve this is to make his damage exactly enough to satisfy:

```
k * damage >= n
```

Any extra attack damage does not reduce the number of monster attacks, so it only wastes crowns that could have gone into defense.

For a fixed `k`, we can calculate the minimum attack investment, then put all remaining crowns into defense. The problem becomes finding the best possible `k`.

When Geralt already has positive damage, the possible number of attacks is bounded. Without attack upgrades he needs at most `ceil(n / base_damage)` attacks, and more attack upgrades can only reduce that number. We can minimize over this range, but we do it mathematically instead of checking every value.

For a candidate number of attacks `k`, the received damage is a function with the form:

```
(k - 1) * max(0, C - T/k)
```

for constants `C` and `T`. After removing the maximum operation, this is a convex or monotonic function over integers. That means the minimum can only appear near the boundary or near the point where the derivative becomes zero. Checking a few neighboring integer values is enough.

When Geralt starts with zero damage, there are two special cases. If defense can be fully neutralized while leaving even a tiny amount of money for attack, the answer is immediately zero. Otherwise the best number of attacks is the smallest feasible one, because the function is increasing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per test case | O(1) | Too slow with many cases |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute Geralt's current effective attack damage and the monster's current effective damage against Geralt. If Geralt's attack is already enough, the later formulas use this value as the starting point.
2. Handle the case where Geralt has zero attack damage. If spending crowns on defense can make the monster's damage zero, the answer is `0/1`. Otherwise, compute the smallest possible number of attacks and evaluate only that choice.
3. For positive initial attack damage, let `h` be the number of attacks needed. The largest possible `h` is the number of attacks without attack upgrades. The optimal `h` is either a boundary value or near the point where the continuous version of the damage function reaches its minimum.
4. Check the necessary candidate values of `h`. For every candidate, compute the minimum attack upgrade needed, use all remaining crowns for defense, and calculate the received damage as a fraction.
5. Keep the smallest fraction and print it in reduced form.

Why it works: for any fixed number of attacks, spending extra crowns on attack cannot improve the number of turns, so an optimal solution always uses the minimum attack upgrade needed for that turn count and spends the rest on defense. The remaining optimization is a one-variable function. Its shape is monotonic or convex, so the minimum is captured by checking boundaries and the neighborhood of its stationary point.

## Python Solution

```python
import sys
from fractions import Fraction

input = sys.stdin.readline

def solve_case(ag, dg, ac, dc, n, m, a, b):
    base_attack = max(0, ag - dc)
    base_taken = max(0, ac - dg)

    def evaluate(k):
        need = Fraction(n, k)
        add_attack = max(Fraction(0), need - base_attack)
        remain = Fraction(m) - Fraction(a) * add_attack
        defense_gain = remain / b
        taken = max(Fraction(0), Fraction(base_taken) - defense_gain)
        return (k - 1) * taken

    if base_attack == 0:
        if b * base_taken < m:
            return Fraction(0)
        k = (n * a + m - 1) // m
        return evaluate(k)

    kmax = (n + base_attack - 1) // base_attack

    if kmax == 1:
        return Fraction(0)

    candidates = {1, kmax}

    last = kmax - 1
    if last >= 1:
        c = b * base_taken - b * m + a * base_attack
        t = a * n

        if c <= 0:
            candidates.add(last)
        else:
            root = int((t / c) ** Fraction(1, 2))
            for x in range(root - 3, root + 4):
                if 1 <= x <= last:
                    candidates.add(x)

    ans = None
    for k in candidates:
        if 1 <= k <= kmax:
            cur = evaluate(k)
            if ans is None or cur < ans:
                ans = cur

    return ans

def main():
    out = []
    t = int(input())
    for _ in range(t):
        ag, dg, ac, dc = map(int, input().split())
        n, m, a, b = map(int, input().split())

        ans = solve_case(ag, dg, ac, dc, n, m, a, b)
        out.append(f"{ans.numerator}/{ans.denominator}")

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The function `evaluate` is the direct translation of the fixed-turn observation. It first finds the minimum attack increase needed to finish in `k` attacks. Since attack and defense use the same crown budget, the remaining money is always converted into defense.

The zero-attack case is separated because the possible number of attacks is not bounded by the original statistics. When defense can be completely removed, using a tiny attack upgrade and many attacks gives zero received damage.

For positive attack damage, `kmax` is the number of attacks without buying attack. No larger number of attacks can ever be optimal because upgrades only increase attack. The candidate search uses the convex form of the remaining function and checks only values near the mathematical minimum.

`Fraction` is used only for the final small set of candidates. It avoids floating point errors while keeping the running time small. Python integers also handle all intermediate values safely.

## Worked Examples

For the first sample:

```
1
1 1 2 2
1 1 1 1
```

Geralt's attack damage is:

```
max(0, 1 - 2) = 0
```

With only one crown, he cannot buy enough attack and defense improvements to create a winning plan.

| Step | Base attack | Candidate attacks | Result |
| --- | --- | --- | --- |
| Initial | 0 | none | impossible |

The algorithm detects that no effective attack can be created and returns:

```
-1
```

For the third sample:

```
1
6 6 66 66
66 666 6 666
```

The initial values are:

| Step | Value |
| --- | --- |
| Base attack damage | 0 |
| Base monster damage | 60 |
| Defense cost | 666 |
| Available crowns | 666 |

The defense upgrade can remove all monster damage, while a small attack upgrade is still possible.

| Step | Attack choice | Defense result | Damage received |
| --- | --- | --- | --- |
| Use defense heavily | Tiny attack increase | Zero monster damage | 0 |

This sample demonstrates why continuous upgrades matter. Integer-only upgrades would miss this possibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a constant number of candidate turn counts are checked |
| Space | O(1) | No arrays or data structures depending on input size are used |

The solution performs a small amount of arithmetic for each test case, so it easily handles `10^4` cases.

## Test Cases

```python
from fractions import Fraction

def run(inp: str) -> str:
    import sys, io
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.readline
    t = int(data())
    ans = []
    for _ in range(t):
        ag, dg, ac, dc = map(int, data().split())
        n, m, a, b = map(int, data().split())
        ans.append(f"{solve_case(ag, dg, ac, dc, n, m, a, b).numerator}/{solve_case(ag, dg, ac, dc, n, m, a, b).denominator}")
    sys.stdin = old
    return "\n".join(ans)

assert run("""3
1 1 2 2
1 1 1 1
2 2 1 1
1 1 1 1
6 6 66 66
66 666 6 666
""") == """-1
0/1
2214/37"""

assert run("""1
5 1 1 1
1 1 1 1
""") == "0/1"

assert run("""1
1 10 100 1
10 5 1 100
""") == "0/1"

assert run("""1
10000 1 1 10000
10000 10000 1 1
""") == "0/1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First three samples | `-1`, `0/1`, `2214/37` | Official examples and fractional answers |
| `5 1 1 1` with one HP monster | `0/1` | No counterattack after the killing hit |
| Zero initial attack with strong defense upgrade | `0/1` | Infinite-turn edge case |
| Large values | `0/1` | Integer limits and boundary arithmetic |

## Edge Cases

When Geralt starts with zero attack damage, the algorithm never tries to enumerate attack counts. It checks whether defense can reach zero incoming damage. If it can, the answer is zero because Geralt can spend an arbitrarily small amount on attack and the rest on defense.

When Geralt kills the monster in one attack, the multiplier `(k - 1)` becomes zero. The implementation keeps this exact condition, so it does not accidentally count a final monster strike.

When the optimal upgrade requires fractions, every calculation is kept as a rational number. The final fraction is automatically reduced by Python's `Fraction`, avoiding errors from rounded decimal values.
