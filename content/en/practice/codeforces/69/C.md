---
title: "CF 69C - Game"
description: "Each player owns a multiset of artifacts. Some artifacts are basic and can be purchased directly. Some are composite and can be crafted from several basic artifacts in fixed quantities. Whenever a player buys a basic artifact, it is added to their inventory."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 69
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 63 (Div. 2)"
rating: 2000
weight: 69
solve_time_s: 135
verified: true
draft: false
---

[CF 69C - Game](https://codeforces.com/problemset/problem/69/C)

**Rating:** 2000  
**Tags:** implementation  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

Each player owns a multiset of artifacts. Some artifacts are basic and can be purchased directly. Some are composite and can be crafted from several basic artifacts in fixed quantities.

Whenever a player buys a basic artifact, it is added to their inventory. Immediately after that purchase, it may become possible to craft exactly one composite artifact. Crafting consumes the required quantities of its ingredients and adds one copy of the composite artifact. The statement guarantees that after every purchase there is at most one craftable composite artifact, so we never need to choose between multiple recipes.

The task is to simulate all purchases and finally print every player's inventory. Only artifacts with positive quantity should appear, and names must be printed in lexicographical order.

The constraints are small enough that direct simulation is feasible. There are at most 100 players, at most 50 recipes, and at most 500 purchases. Even a solution that scans all recipes after every purchase performs only about 500 × 50 = 25,000 recipe checks, which is tiny.

The main difficulty is not performance, but correct bookkeeping. Crafting removes components, so inventories must behave like multisets rather than simple sets. Another subtle point is that composite artifacts themselves can remain in inventories and coexist with basic artifacts.

A common mistake is forgetting to subtract ingredients after crafting. Consider this input:

```
1 2 1 2
wood
stone
axe: wood 1, stone 1
1 wood
1 stone
```

The correct final inventory is:

```
1
axe 1
```

A buggy implementation might output both `wood`, `stone`, and `axe`, because it crafts the item but forgets to consume the ingredients.

Another easy mistake is checking recipes only once globally instead of after every purchase for the corresponding player. Example:

```
1 1 1 2
gem
crown: gem 2
1 gem
1 gem
```

The first purchase does nothing. The second purchase creates `crown`. The correct output is:

```
1
crown 1
```

If we do not re-check after every purchase, the recipe is never triggered.

There is also a subtle parsing issue. Recipe lines contain commas and colons in a free-form textual format:

```
sword: iron 2, wood 1
```

A fragile parser that splits only on spaces will leave punctuation attached to names like `"2,"` or `"sword:"`. The safest approach is to first split around the colon, then split the ingredient list around commas.

## Approaches

The brute-force idea is straightforward simulation.

For every purchase, add the bought artifact to the player's inventory. Then scan every recipe and check whether the player owns enough of every required ingredient. If some recipe is craftable, subtract the required counts and add one copy of the composite artifact.

This is correct because the statement guarantees that after each purchase at most one recipe can become craftable. We never face conflicting choices.

The brute-force method already fits comfortably within the limits. Let `q` be the number of purchases, `m` the number of recipes, and `n` the maximum number of ingredients in a recipe. The worst-case work is roughly `q × m × n`, which is at most `500 × 50 × 50 = 1,250,000` ingredient checks.

Since the constraints are tiny, there is no need for advanced graph processing or dependency tracking. The real work lies in implementing the simulation carefully.

The key observation is that crafting only depends on the current inventory of a single player. Purchases never interact across players, so each inventory can be stored independently. Once we represent each player's inventory as a frequency map, recipe checking becomes a direct comparison of required counts against owned counts.

The optimal solution is essentially the same simulation, but implemented cleanly with hash maps for inventories and parsed recipe structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q × m × n) | O(k × A) | Accepted |
| Optimal | O(q × m × n) | O(k × A) | Accepted |

Here `A` is the total number of distinct artifact names.

## Algorithm Walkthrough

1. Read all basic artifact names.

We do not actually need to distinguish basic and composite artifacts during simulation, but reading the names establishes the universe of artifact identifiers.
2. Parse every composite recipe.

Each recipe contains a resulting artifact and a list of ingredient-count pairs. Store them as:

```
result_name -> list of (ingredient, required_count)
```

Parsing carefully matters because commas and colons are part of the input format.
3. Create one inventory map for each player.

Each inventory stores:

```
artifact_name -> quantity
```
4. Process purchases one by one.

For a purchase `(player, artifact)`:

- Increase that player's count of the bought artifact.
- Scan all recipes.
- For each recipe, check whether the player owns enough of every ingredient.
- If a recipe is craftable:

- Subtract all ingredient counts.
- Add one copy of the composite artifact.
- Stop scanning recipes.

We stop immediately because the statement guarantees that at most one recipe can become available after a purchase.
5. After all purchases, print every player's inventory.

Only artifacts with positive counts should be printed. The output must be sorted lexicographically by artifact name.

### Why it works

The invariant is that after processing each purchase, every player's inventory exactly matches the game rules.

When a purchase occurs, we first add the bought artifact. Then we check all recipes. If some recipe is craftable, we consume exactly the required ingredients and add exactly one resulting artifact. Because the statement guarantees uniqueness of the newly available recipe, stopping after the first successful craft matches the intended game behavior.

Since inventories are updated immediately after every event, the state before the next purchase is always correct. By induction over all purchases, the final inventories are correct.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    k, n, m, q = map(int, input().split())

    basic = [input().strip() for _ in range(n)]

    recipes = []

    for _ in range(m):
        line = input().strip()

        result, rest = line.split(": ")

        ingredients = []

        parts = rest.split(", ")

        for part in parts:
            name, cnt = part.rsplit(" ", 1)
            ingredients.append((name, int(cnt)))

        recipes.append((result, ingredients))

    inventories = [defaultdict(int) for _ in range(k)]

    for _ in range(q):
        player, artifact = input().split()
        player = int(player) - 1

        inventories[player][artifact] += 1

        for result, ingredients in recipes:
            ok = True

            for name, need in ingredients:
                if inventories[player][name] < need:
                    ok = False
                    break

            if ok:
                for name, need in ingredients:
                    inventories[player][name] -= need

                inventories[player][result] += 1
                break

    out = []

    for inv in inventories:
        items = []

        for name in sorted(inv.keys()):
            if inv[name] > 0:
                items.append((name, inv[name]))

        out.append(str(len(items)))

        for name, cnt in items:
            out.append(f"{name} {cnt}")

    print("\n".join(out))

solve()
```

The solution follows the simulation directly.

Recipes are stored as pairs of result name and ingredient list. The parsing uses `split(": ")` first because the colon separates the crafted artifact from its requirements. Then the ingredient section is split by `", "` to isolate each requirement. Finally, `rsplit(" ", 1)` separates the ingredient name from its numeric quantity. Using `rsplit` is safer because artifact names are arbitrary strings.

Each player's inventory is a `defaultdict(int)`, which automatically treats missing artifacts as quantity zero.

After every purchase, we scan recipes in input order. For each recipe, we verify whether every ingredient count is available. If so, we subtract the required quantities and add the crafted artifact.

One subtle implementation detail is stopping immediately after crafting. The statement guarantees that no more than one recipe becomes available after a purchase. Continuing the scan could incorrectly allow multiple crafts from a single event.

When printing results, we filter out zero counts because ingredients consumed during crafting may still remain as keys in the dictionary.

## Worked Examples

### Example 1

Input:

```
2 3 2 5
desolator
refresher
perseverance
vanguard: desolator 1, refresher 1
maelstorm: perseverance 2
1 desolator
2 perseverance
1 refresher
2 desolator
2 perseverance
```

### Trace

| Step | Player | Purchase | Inventory Before Craft | Crafted | Inventory After |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | desolator | desolator=1 | none | desolator=1 |
| 2 | 2 | perseverance | perseverance=1 | none | perseverance=1 |
| 3 | 1 | refresher | desolator=1, refresher=1 | vanguard | vanguard=1 |
| 4 | 2 | desolator | perseverance=1, desolator=1 | none | perseverance=1, desolator=1 |
| 5 | 2 | perseverance | perseverance=2, desolator=1 | maelstorm | maelstorm=1, desolator=1 |

Final output:

```
1
vanguard 1
2
desolator 1
maelstorm 1
```

This example demonstrates ingredient consumption. After crafting `vanguard`, both `desolator` and `refresher` disappear from player 1's inventory.

### Example 2

Input:

```
1 2 1 4
wood
stone
axe: wood 2, stone 1
1 wood
1 stone
1 wood
1 wood
```

### Trace

| Step | Purchase | Inventory Before Craft | Crafted | Inventory After |
| --- | --- | --- | --- | --- |
| 1 | wood | wood=1 | none | wood=1 |
| 2 | stone | wood=1, stone=1 | none | wood=1, stone=1 |
| 3 | wood | wood=2, stone=1 | axe | axe=1 |
| 4 | wood | axe=1, wood=1 | none | axe=1, wood=1 |

Final output:

```
2
axe 1
wood 1
```

This trace shows that crafting happens immediately when requirements become satisfied, and only the exact required quantities are consumed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q × m × n) | Each purchase scans all recipes and all recipe ingredients |
| Space | O(k × A) | Each player stores counts of owned artifacts |

The maximum work is around 1.25 million ingredient checks, which is very small for Python within a 2 second limit. Memory usage is also tiny because the total number of distinct artifact names is at most 100.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out_capture = io.StringIO()

    k, n, m, q = map(int, input().split())

    basic = [input().strip() for _ in range(n)]

    recipes = []

    for _ in range(m):
        line = input().strip()

        result, rest = line.split(": ")

        ingredients = []

        for part in rest.split(", "):
            name, cnt = part.rsplit(" ", 1)
            ingredients.append((name, int(cnt)))

        recipes.append((result, ingredients))

    inventories = [defaultdict(int) for _ in range(k)]

    for _ in range(q):
        player, artifact = input().split()
        player = int(player) - 1

        inventories[player][artifact] += 1

        for result, ingredients in recipes:
            ok = True

            for name, need in ingredients:
                if inventories[player][name] < need:
                    ok = False
                    break

            if ok:
                for name, need in ingredients:
                    inventories[player][name] -= need

                inventories[player][result] += 1
                break

    ans = []

    for inv in inventories:
        items = []

        for name in sorted(inv.keys()):
            if inv[name] > 0:
                items.append((name, inv[name]))

        ans.append(str(len(items)))

        for name, cnt in items:
            ans.append(f"{name} {cnt}")

    return "\n".join(ans)

# provided sample
assert run(
"""2 3 2 5
desolator
refresher
perseverance
vanguard: desolator 1, refresher 1
maelstorm: perseverance 2
1 desolator
2 perseverance
1 refresher
2 desolator
2 perseverance
"""
) == (
"""1
vanguard 1
2
desolator 1
maelstorm 1"""
), "sample 1"

# minimum input
assert run(
"""1 1 0 1
a
1 a
"""
) == (
"""1
a 1"""
), "minimum case"

# repeated crafting
assert run(
"""1 1 1 4
gem
crown: gem 2
1 gem
1 gem
1 gem
1 gem
"""
) == (
"""1
crown 2"""
), "multiple crafts over time"

# leftover ingredients
assert run(
"""1 2 1 3
wood
stone
axe: wood 2, stone 1
1 wood
1 stone
1 wood
"""
) == (
"""1
axe 1"""
), "exact consumption"

# independent player inventories
assert run(
"""2 1 1 2
gem
crown: gem 2
1 gem
2 gem
"""
) == (
"""1
gem 1
1
gem 1"""
), "players separated"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Minimum input | Single artifact owned | Base initialization |
| Repeated crafting | `crown 2` | Crafting can happen multiple times across purchases |
| Leftover ingredients | Only `axe 1` | Ingredients are consumed correctly |
| Independent inventories | Each player keeps own gem | No accidental shared state |

## Edge Cases

Consider the case where crafting consumes all ingredients exactly:

```
1 2 1 2
wood
stone
axe: wood 1, stone 1
1 wood
1 stone
```

After the second purchase, the inventory becomes:

```
wood=1, stone=1
```

The recipe is craftable, so both counts are reduced to zero and `axe=1` is added. During output, zero-count entries are skipped. The final result is:

```
1
axe 1
```

Now consider delayed crafting:

```
1 1 1 3
gem
crown: gem 2
1 gem
1 gem
1 gem
```

After the first purchase, crafting is impossible. After the second, the inventory reaches `gem=2`, so `crown` is crafted and both gems disappear. After the third purchase, the inventory becomes:

```
crown=1, gem=1
```

The algorithm checks recipes after every purchase, so the timing is handled correctly.

Finally, consider multiple players:

```
2 1 1 2
gem
crown: gem 2
1 gem
2 gem
```

Player 1 owns one gem and player 2 owns one gem. Neither can craft `crown`, because inventories are independent. The algorithm stores a separate dictionary for each player, so counts are never mixed across players.
