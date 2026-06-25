---
title: "CF 106113I - Cristales M\u00e1gicos"
description: "We have N crystals. Each crystal belongs to a family identified by a color name and has a power value. We must select exactly K crystals, with the restriction that no two selected crystals can come from the same family. The objective is to maximize the sum of their powers."
date: "2026-06-25T11:39:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106113
codeforces_index: "I"
codeforces_contest_name: "Coding Cup TecNM 2025"
rating: 0
weight: 106113
solve_time_s: 51
verified: true
draft: false
---

[CF 106113I - Cristales M\u00e1gicos](https://codeforces.com/problemset/problem/106113/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have `N` crystals. Each crystal belongs to a family identified by a color name and has a power value.

We must select exactly `K` crystals, with the restriction that no two selected crystals can come from the same family. The objective is to maximize the sum of their powers.

If it is impossible because there are fewer than `K` distinct families, we print `IMPOSIBLE`.

If several selections achieve the same maximum total power, we must output the one whose sorted list of crystal indices is lexicographically smallest.

The input size is the main challenge. There can be up to `10^6` crystals, and family names can be long strings. Any solution that compares all pairs of crystals or repeatedly sorts large collections will be far too slow. The algorithm must process each crystal essentially once and keep only aggregated information per family.

A subtle detail is the lexicographic tie-breaking. Maximizing power alone is not enough. Two different optimal selections can have the same total power, and we must carefully choose the indices that produce the smallest lexicographic sorted sequence.

Consider this example:

```
4 1
RED 10
RED 10
BLUE 10
GREEN 5
```

The maximum power is `10`.

Possible optimal answers are selecting index `1`, `2`, or `3`.

The correct output is index `1`, because `[1]` is lexicographically smaller than `[2]` or `[3]`.

Another important case appears when several families have the same best power and compete for the last available slots.

```
5 2
A 10
B 10
C 10
D 5
E 1
```

Any two of `A`, `B`, and `C` give the same maximum sum `20`.

The correct answer uses indices `[1, 2]`, not `[1, 3]` or `[2, 3]`, because `[1, 2]` is lexicographically smallest.

A final edge case is when a family contains multiple crystals with the same maximum power.

```
4 2
RED 7
RED 7
BLUE 5
GREEN 1
```

For family `RED`, both indices `1` and `2` achieve the same contribution. Choosing index `1` is always at least as good lexicographically as choosing index `2`.

## Approaches

A brute-force solution would try every subset of `K` crystals, check whether all families are distinct, compute the total power, and keep the best valid selection. Even for `N = 50`, this is already hopeless because the number of subsets grows exponentially. With `N = 10^6`, such an approach is completely impossible.

The first observation is that, for any family, only its strongest crystal can ever appear in an optimal solution. If a family contains powers `3`, `8`, and `12`, selecting anything except the crystal with power `12` can only decrease the total power.

This allows us to compress every family into a single value:

`V = maximum power in that family`.

There is still one complication. A family may contain several crystals whose power equals `V`. Since all of them contribute the same amount, we should keep the smallest index among them. Any larger index can only make the final answer lexicographically worse.

After this compression, every family becomes:

```
(best_power, best_index)
```

Now the problem changes into:

Choose exactly `K` families.

Each chosen family contributes its `best_power`.

Among all maximum-power selections, return the lexicographically smallest sorted list of chosen indices.

To maximize power, we simply take the `K` largest family powers.

The only ambiguity occurs when several families share the cutoff power.

Suppose:

```
powers = [15, 12, 12, 12, 8]
K = 3
```

The family with power `15` must be selected.

The family with power `8` can never be selected.

Among the three families with power `12`, we need two more choices.

Since all these families contribute exactly the same power, the lexicographic rule becomes the deciding factor. We should choose the families whose representative indices are smallest.

That gives a clean strategy:

1. Compute each family's maximum power and smallest index achieving it.
2. Sort families by power.
3. Determine the cutoff power.
4. Select all families strictly above the cutoff.
5. Among families equal to the cutoff, choose as many as needed, preferring smaller representative indices.
6. Sort the resulting indices and print them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(N + F log F) | O(F) | Accepted |

Here `F` is the number of distinct families.

## Algorithm Walkthrough

1. Read all crystals and group them by family name.
2. For each family, maintain two values:

- The maximum power seen so far.
- The smallest index whose power equals that maximum.
3. After processing all crystals, let `F` be the number of distinct families.
4. If `F < K`, print `IMPOSIBLE` because selecting one crystal from each family still does not provide enough crystals.
5. Convert every family into a pair `(power, index)` where:

- `power` is the family's maximum power.
- `index` is the smallest index achieving that power.
6. Sort these pairs by decreasing power.
7. Let `T` be the power of the `K`-th family in this ordering. This is the cutoff power.
8. Select every family whose power is greater than `T`. Their inclusion is mandatory because replacing any of them would reduce the total power.
9. Count how many additional families are still needed.
10. Collect all families whose power equals `T`.
11. Sort those threshold families by their representative index and take exactly the required number.
12. Gather all chosen indices, sort them increasingly, and print them together with the total power.

### Why it works

Every family contributes independently to the total power. Replacing a chosen crystal by another crystal from the same family can never improve the sum beyond the family's maximum power, so every optimal solution must use a maximum-power crystal from each selected family.

After reducing each family to its maximum achievable contribution, maximizing the total power becomes equivalent to choosing the `K` largest family powers. Any family strictly above the cutoff must belong to every optimal solution, while any family strictly below the cutoff can never belong to an optimal solution.

The only freedom comes from families exactly at the cutoff power. Since all such families contribute the same amount, the total power remains unchanged regardless of which of them are chosen. To obtain the lexicographically smallest sorted index list, we select the smallest representative indices among those tied families. Any other choice would replace a smaller index by a larger one and make the sorted sequence lexicographically larger.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    families = {}

    for idx in range(1, n + 1):
        color, power = input().split()
        power = int(power)

        if color not in families:
            families[color] = [power, idx]
        else:
            best_power, best_idx = families[color]

            if power > best_power:
                families[color] = [power, idx]
            elif power == best_power and idx < best_idx:
                families[color][1] = idx

    if len(families) < k:
        print("IMPOSIBLE")
        return

    items = [(p, idx) for p, idx in families.values()]
    items.sort(key=lambda x: -x[0])

    threshold = items[k - 1][0]

    chosen_indices = []
    total_power = 0

    equal_group = []

    for power, idx in items:
        if power > threshold:
            chosen_indices.append(idx)
            total_power += power
        elif power == threshold:
            equal_group.append((idx, power))

    need = k - len(chosen_indices)

    equal_group.sort()

    for idx, power in equal_group[:need]:
        chosen_indices.append(idx)
        total_power += power

    chosen_indices.sort()

    print(total_power)
    print(*chosen_indices)

solve()
```

The dictionary stores only the best crystal for each family. When a larger power is found, the family record is replaced. When the same maximum power appears again, the smaller index is kept.

After all families are compressed, the algorithm never needs the original crystals again. The sorted family list determines the cutoff power. Families above the cutoff are fixed members of every optimal solution, while tied families are handled separately.

The threshold group is sorted by index because the tie-breaking rule depends on the final lexicographic order of selected indices, not on family names or powers.

Python integers safely handle the total power because the maximum possible sum is `10^6 × 10^9 = 10^15`, well within Python's arbitrary-precision integer range.

## Worked Examples

### Example 1

Input:

```
5 3
ROJO 5
AZUL 3
ROJO 4
VERDE 6
AZUL 2
```

Family compression produces:

| Family | Best Power | Representative Index |
| --- | --- | --- |
| ROJO | 5 | 1 |
| AZUL | 3 | 2 |
| VERDE | 6 | 4 |

Sorted by power:

| Power | Index |
| --- | --- |
| 6 | 4 |
| 5 | 1 |
| 3 | 2 |

`K = 3`, so all families are selected.

| Step | Chosen Indices | Total Power |
| --- | --- | --- |
| Select VERDE | [4] | 6 |
| Select ROJO | [4,1] | 11 |
| Select AZUL | [4,1,2] | 14 |

Sorted indices:

```
1 2 4
```

Output:

```
14
1 2 4
```

This example shows the basic case where every distinct family must be chosen.

### Example 2

Input:

```
5 2
A 10
B 10
C 10
D 5
E 1
```

Compressed families:

| Family | Power | Index |
| --- | --- | --- |
| A | 10 | 1 |
| B | 10 | 2 |
| C | 10 | 3 |
| D | 5 | 4 |
| E | 1 | 5 |

The cutoff power is `10`.

Three families tie at the cutoff, but only two can be chosen.

| Candidate Index | Selected? |
| --- | --- |
| 1 | Yes |
| 2 | Yes |
| 3 | No |

Final indices:

```
1 2
```

This demonstrates how lexicographic tie-breaking is resolved.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + F log F) | One pass over all crystals, then sorting distinct families |
| Space | O(F) | One record per distinct family |

`F` is at most `N`, so the worst case is `O(N log N)`. With `N = 10^6`, this is efficient enough for the contest limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    data = io.StringIO(inp)
    input = data.readline

    n, k = map(int, input().split())

    families = {}

    for idx in range(1, n + 1):
        color, power = input().split()
        power = int(power)

        if color not in families:
            families[color] = [power, idx]
        else:
            bp, bi = families[color]
            if power > bp:
                families[color] = [power, idx]
            elif power == bp and idx < bi:
                families[color][1] = idx

    out = []

    if len(families) < k:
        out.append("IMPOSIBLE")
        return "\n".join(out)

    items = [(p, idx) for p, idx in families.values()]
    items.sort(key=lambda x: -x[0])

    threshold = items[k - 1][0]

    chosen = []
    total = 0
    eq = []

    for p, idx in items:
        if p > threshold:
            chosen.append(idx)
            total += p
        elif p == threshold:
            eq.append((idx, p))

    need = k - len(chosen)

    eq.sort()

    for idx, p in eq[:need]:
        chosen.append(idx)
        total += p

    chosen.sort()

    out.append(str(total))
    out.append(" ".join(map(str, chosen)))
    return "\n".join(out)

# provided samples
assert run(
"""5 3
ROJO 5
AZUL 3
ROJO 4
VERDE 6
AZUL 2
"""
) == "14\n1 2 4"

assert run(
"""4 3
AMARILLO 4
GRIS 5
AMARILLO 6
GRIS 7
"""
) == "IMPOSIBLE"

# minimum size with one family
assert run(
"""3 1
A 5
A 7
A 6
"""
) == "7\n2"

# equal maximum power inside a family
assert run(
"""4 2
A 10
A 10
B 5
C 1
"""
) == "15\n1 3"

# cutoff tie between families
assert run(
"""5 2
A 10
B 10
C 10
D 5
E 1
"""
) == "20\n1 2"

# all families distinct
assert run(
"""4 4
A 1
B 2
C 3
D 4
"""
) == "10\n1 2 3 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One family, K=1 | Best crystal chosen | Basic correctness |
| Equal maxima in a family | Smallest index retained | Intra-family tie handling |
| Three-way cutoff tie | Smallest indices selected | Lexicographic rule |
| K equals number of families | All families selected | Boundary condition |
| Distinct families fewer than K | IMPOSIBLE | Feasibility check |

## Edge Cases

Consider:

```
4 3
AMARILLO 4
GRIS 5
AMARILLO 6
GRIS 7
```

Only two families exist: `AMARILLO` and `GRIS`.

The algorithm computes:

```
F = 2
K = 3
```

Since `F < K`, it immediately prints:

```
IMPOSIBLE
```

No further processing is needed.

Now consider:

```
4 2
RED 7
RED 7
BLUE 5
GREEN 1
```

Family compression gives:

| Family | Best Power | Index |
| --- | --- | --- |
| RED | 7 | 1 |
| BLUE | 5 | 3 |
| GREEN | 1 | 4 |

Even though index `2` has the same power as index `1`, the representative index becomes `1`.

The selected families are `RED` and `BLUE`.

Output:

```
12
1 3
```

The lexicographic requirement is satisfied automatically because the smallest index achieving the family maximum was stored during preprocessing.

Finally, consider:

```
5 2
A 10
B 10
C 10
D 5
E 1
```

The cutoff power is `10`. The threshold group contains indices `[1,2,3]`.

The algorithm needs two of them, so it takes the two smallest:

```
[1,2]
```

Any other choice would produce a lexicographically larger sorted sequence, while giving the same total power.
