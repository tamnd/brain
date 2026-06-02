---
title: "CF 105A - Transmigration"
description: "The problem simulates a single transmigration process in a role-playing game. We start with a character who already possesses several skills. Each skill has a name and an experience level. When transmigration occurs, every existing skill has its level reduced by a coefficient k."
date: "2026-06-01T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 105
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 81"
rating: 1700
weight: 105
solve_time_s: 186
verified: true
draft: false
---

[CF 105A - Transmigration](https://codeforces.com/problemset/problem/105/A)

**Rating:** 1700  
**Tags:** implementation  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem simulates a single transmigration process in a role-playing game.

We start with a character who already possesses several skills. Each skill has a name and an experience level. When transmigration occurs, every existing skill has its level reduced by a coefficient `k`. The new level becomes the integer part of `k × level`.

After this reduction step, any skill whose resulting level is strictly less than `100` is forgotten and disappears completely.

Next, the character receives the skills that belong to the target class. If the character already has one of those skills after the reduction phase, nothing changes. If the skill is not currently present, it is added with level `0`.

The final task is to output all remaining skills after these transformations, sorted lexicographically by skill name.

The constraints are very small. Both the number of current skills and the number of target-class skills are at most `20`. Even a straightforward implementation that repeatedly scans collections would be easily fast enough. The challenge is not algorithmic complexity, but correctly following the sequence of transformations described in the statement.

Several subtle cases can produce incorrect answers if the rules are applied in the wrong order.

Consider:

```
1 1 0.50
fire 300
fire
```

The skill becomes `150` after reduction and survives. Since the class skill already exists, it must remain `150`.

Correct output:

```
1
fire 150
```

A careless implementation might overwrite it with `0`.

Another important case is when a class skill existed originally but was forgotten after reduction:

```
1 1 0.50
fire 180
fire
```

The reduced value is `90`, so the skill is forgotten. The class then grants `fire` again at level `0`.

Correct output:

```
1
fire 0
```

An implementation that checks class skills before removing forgotten skills would produce the wrong result.

The boundary value `100` is also important:

```
1 0 0.50
fire 200
```

The reduced value is exactly `100`, which survives because only values strictly less than `100` are removed.

Correct output:

```
1
fire 100
```

Using `<= 100` instead of `< 100` would incorrectly delete the skill.

## Approaches

A direct simulation immediately suggests itself. We can process every existing skill, compute its reduced level, and keep only those whose new level is at least `100`. After that, we process the target class skills and add any missing ones with level `0`.

Because there are at most twenty skills in either list, even a brute-force approach using nested scans would be completely acceptable. The worst case would involve only a few hundred operations.

A slightly cleaner approach uses a dictionary keyed by skill name. The dictionary naturally represents the set of skills currently possessed by the character. After applying the reduction and forgetting rules, adding class skills becomes a simple membership check.

The key observation is that the problem is purely a state transformation. There is no optimization, graph search, dynamic programming, or complex data structure involved. We only need to carefully follow the rules in the exact order given.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n + m)^2) | O(n + m) | Accepted |
| Optimal | O(n + m + z log z) | O(n + m) | Accepted |

Here `z` is the number of skills in the final answer, and the sorting step dominates the running time.

## Algorithm Walkthrough

1. Read `n`, `m`, and the coefficient `k`.
2. Create an empty dictionary that will store surviving skills after transmigration.
3. For each of the `n` current skills, compute:

```
new_level = floor(k × old_level)
```

The statement explicitly requires taking the integer part.
4. If `new_level` is at least `100`, insert the skill into the dictionary with that value.

Skills below `100` are forgotten and should not appear in the dictionary.
5. Read all `m` target-class skills one by one.
6. For each class skill, check whether it already exists in the dictionary.

If it does not exist, insert it with level `0`.

If it already exists, leave its current value unchanged.
7. Extract all dictionary entries and sort them lexicographically by skill name.
8. Print the number of skills and then print each `(name, level)` pair in sorted order.

### Why it works

After step 4, the dictionary contains exactly the skills that survive the reduction phase, because every original skill is transformed according to the coefficient and every skill below `100` is removed.

After step 6, every target-class skill is guaranteed to exist in the dictionary. Existing surviving skills retain their reduced level, while missing class skills are added at level `0`, exactly matching the rules of transmigration.

Since the final output is simply the lexicographically ordered version of this final skill set, the algorithm produces the unique correct result.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k_str = input().split()

    n = int(n)
    m = int(m)

    num, den = map(int, k_str.split('.'))
    k_num = num * 100 + den

    skills = {}

    for _ in range(n):
        name, exp = input().split()
        exp = int(exp)

        new_exp = (exp * k_num) // 100

        if new_exp >= 100:
            skills[name] = new_exp

    for _ in range(m):
        name = input().strip()

        if name not in skills:
            skills[name] = 0

    items = sorted(skills.items())

    out = [str(len(items))]
    for name, level in items:
        out.append(f"{name} {level}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the simulation directly.

A small detail is how the coefficient `k` is handled. Using floating-point arithmetic would usually work for these constraints, but integer arithmetic is cleaner and avoids any possibility of precision issues. Since `k` always contains exactly two decimal places, we convert it into an integer percentage. For example, `0.75` becomes `75`, and the reduced level is computed as:

```
floor(exp × 75 / 100)
```

using integer division.

The dictionary stores the current set of skills after the forgetting phase. When class skills are processed, a simple membership check determines whether a skill should be added at level `0`.

Finally, sorting the dictionary items produces the required lexicographical order.

## Worked Examples

### Sample 1

Input:

```
5 4 0.75
axe 350
impaler 300
ionize 80
megafire 120
magicboost 220
heal
megafire
shield
magicboost
```

After processing existing skills:

| Skill | Original | Reduced | Kept? |
| --- | --- | --- | --- |
| axe | 350 | 262 | Yes |
| impaler | 300 | 225 | Yes |
| ionize | 80 | 60 | No |
| megafire | 120 | 90 | No |
| magicboost | 220 | 165 | Yes |

Current dictionary:

| Skill | Level |
| --- | --- |
| axe | 262 |
| impaler | 225 |
| magicboost | 165 |

Now process class skills:

| Class Skill | Already Present? | Action |
| --- | --- | --- |
| heal | No | Add 0 |
| megafire | No | Add 0 |
| shield | No | Add 0 |
| magicboost | Yes | Keep 165 |

Final dictionary:

| Skill | Level |
| --- | --- |
| axe | 262 |
| heal | 0 |
| impaler | 225 |
| magicboost | 165 |
| megafire | 0 |
| shield | 0 |

Sorted output:

```
6
axe 262
heal 0
impaler 225
magicboost 165
megafire 0
shield 0
```

This example demonstrates that a skill can disappear during reduction and then be reintroduced as a class skill with level `0`.

### Additional Example

Input:

```
2 2 0.50
fire 300
ice 180
fire
wind
```

Reduction phase:

| Skill | Original | Reduced | Kept? |
| --- | --- | --- | --- |
| fire | 300 | 150 | Yes |
| ice | 180 | 90 | No |

Dictionary after reduction:

| Skill | Level |
| --- | --- |
| fire | 150 |

Class skill phase:

| Class Skill | Already Present? | Result |
| --- | --- | --- |
| fire | Yes | Keep 150 |
| wind | No | Add 0 |

Final state:

| Skill | Level |
| --- | --- |
| fire | 150 |
| wind | 0 |

Output:

```
2
fire 150
wind 0
```

This example shows that existing surviving skills are never overwritten by a class skill.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + z log z) | Processing skills is linear, sorting the final list costs `O(z log z)` |
| Space | O(n + m) | Dictionary stores all surviving and added skills |

Since `n` and `m` are both at most `20`, the running time is effectively instantaneous. The solution is far below the limits in both time and memory usage.

## Test Cases

```python
# helper: run solution on input string, return output string
import io
import sys

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    def solve():
        input = sys.stdin.readline

        n, m, k_str = input().split()
        n = int(n)
        m = int(m)

        num, den = map(int, k_str.split('.'))
        k_num = num * 100 + den

        skills = {}

        for _ in range(n):
            name, exp = input().split()
            exp = int(exp)

            val = (exp * k_num) // 100
            if val >= 100:
                skills[name] = val

        for _ in range(m):
            name = input().strip()
            if name not in skills:
                skills[name] = 0

        items = sorted(skills.items())

        print(len(items))
        for name, level in items:
            print(name, level)

    solve()

    sys.stdout = old_stdout
    return output.getvalue()

# sample 1
assert run(
"""5 4 0.75
axe 350
impaler 300
ionize 80
megafire 120
magicboost 220
heal
megafire
shield
magicboost
"""
) == """6
axe 262
heal 0
impaler 225
magicboost 165
megafire 0
shield 0
"""

# minimum input
assert run(
"""1 1 0.50
fire 200
fire
"""
) == """1
fire 100
"""

# forgotten then re-added
assert run(
"""1 1 0.50
fire 180
fire
"""
) == """1
fire 0
"""

# surviving class skill keeps level
assert run(
"""1 1 0.50
fire 300
fire
"""
) == """1
fire 150
"""

# all skills forgotten, class introduces new ones
assert run(
"""2 2 0.01
a 9999
b 5000
c
d
"""
) == """2
c 0
d 0
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | Official answer | Full simulation behavior |
| Single skill reduced to 100 | Skill survives | Correct `< 100` check |
| Forgotten then re-added | Level 0 skill | Correct operation order |
| Surviving class skill | Original reduced level | No accidental overwrite |
| Tiny coefficient | Only class skills remain | Complete forgetting behavior |

## Edge Cases

A skill whose reduced value becomes exactly `100` must survive. Consider:

```
1 0 0.50
fire 200
```

The reduced value is `100`. Since only values strictly below `100` are forgotten, the final output is:

```
1
fire 100
```

The implementation uses `>= 100`, which handles this boundary correctly.

A class skill may already exist after the reduction phase. Consider:

```
1 1 0.50
fire 300
fire
```

The reduced value is `150`, so the skill survives. When processing class skills, the dictionary already contains `"fire"`, so nothing is changed. The final result remains:

```
1
fire 150
```

This prevents accidental replacement with level `0`.

A skill can disappear and then be granted again by the new class:

```
1 1 0.50
fire 180
fire
```

The reduced value becomes `90`, so the skill is forgotten. The class skill processing then sees that `"fire"` is absent and inserts it with level `0`. The result is:

```
1
fire 0
```

This verifies that forgetting happens before adding class-specific skills, exactly as required by the statement.
