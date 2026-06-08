---
title: "CF 2022A - Bus to P\u00e9njamo"
description: "Each bus row contains exactly two seats. We have several families, and family i contains ai people. A person is happy in one of two situations. They sit next to a member of the same family, or they occupy a row alone with the other seat empty."
date: "2026-06-08T12:36:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2022
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 978 (Div. 2)"
rating: 800
weight: 2022
solve_time_s: 138
verified: true
draft: false
---

[CF 2022A - Bus to P\u00e9njamo](https://codeforces.com/problemset/problem/2022/A)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, implementation, math  
**Solve time:** 2m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

Each bus row contains exactly two seats. We have several families, and family `i` contains `a_i` people.

A person is happy in one of two situations. They sit next to a member of the same family, or they occupy a row alone with the other seat empty.

We must place every person on the bus and maximize the total number of happy people.

The constraints are very small. Each family size is at most 10, `n` is at most 100, and there are at most 1000 test cases. Even an `O(n)` or `O(n log n)` solution is more than enough. The challenge is not performance, it is finding the right counting argument.

A common mistake is to focus on constructing the seating arrangement explicitly. The answer can be computed directly from a few counts.

Consider the input

```
1
2 2
3 1
```

The family of size 3 contributes one same-family pair and one leftover person. We can seat the pair together and then the two remaining people must share a row. The correct answer is 2, not 3. A greedy strategy that counts every odd leftover person as happy would overestimate.

Another tricky case is

```
1
4 5
1 1 1 1
```

There are no family pairs at all. We have four people and five rows, so each person can sit alone. The answer is 4. Any approach that only counts same-family pairs would incorrectly return 0.

A third edge case is

```
1
2 3
3 3
```

Each family contributes one pair and one leftover person. We get two happy pairs, giving 4 happy people immediately. The two leftovers must share the remaining row, so neither is happy. The answer is 4. The leftover people are not automatically happy just because there is a free row available.

## Approaches

A brute-force solution would try to enumerate seating arrangements and evaluate how many people end up happy. Even for a small number of rows, the number of possible seat assignments grows explosively. Since people are distinguishable by family membership and rows can be arranged in many ways, this quickly becomes infeasible.

The key observation is that happiness comes from only two row patterns.

The first pattern is a row containing two members of the same family. Such a row creates two happy people and uses one row completely. Since two family members seated together are always better than separating them, every possible same-family pair should be used.

For a family of size `a_i`, we can form `a_i // 2` such pairs. Summing over all families gives

```
pairs = Σ(a_i // 2)
```

Each pair contributes exactly two happy people.

After placing all these pairs, every family has at most one unpaired member remaining. Let

```
odd = Σ(a_i % 2)
```

be the number of remaining people.

The number of unused rows is

```
free_rows = r - pairs
```

because each family pair occupies one full row.

Now focus only on the leftover people. If a leftover person gets a row alone, they are happy. If two leftover people share a row, neither is happy because they come from different families.

Initially, we can place one leftover person into each free row, creating `free_rows` happy people. If there are more leftovers than free rows, every extra leftover person must sit beside one of those happy singletons. When that happens, the previously happy singleton loses their happiness. Each extra person reduces the happy count among leftovers by exactly one.

This leads directly to the final counting formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute `pairs = Σ(a_i // 2)`.

Every such pair can occupy a row together and contributes two happy people.
2. Start the answer with `ans = 2 * pairs`.

These happy people are guaranteed.
3. Compute `odd = Σ(a_i % 2)`.

These are the people left after all possible same-family pairs are formed.
4. Compute `free_rows = r - pairs`.

Since `Σ a_i ≤ 2r`, we always have `pairs ≤ r`.
5. If `odd ≤ free_rows`, every leftover person can sit alone.

Add `odd` to the answer.
6. Otherwise, place one leftover person in every free row.

This gives `free_rows` happy people initially.

There are `odd - free_rows` extra people still unseated. Each of them must sit next to one of those singletons, destroying one previously happy person.

The number of happy leftovers becomes

```
free_rows - (odd - free_rows)
= 2 * free_rows - odd
```

Add that value to the answer.

### Why it works

Every happy row containing two people must contain members of the same family. Splitting a possible family pair across different rows can never increase happiness, because the best alternative is making at most one of them happy as a singleton. So using all available family pairs is always optimal.

After all pairs are used, every remaining family contributes at most one person. No additional same-family pair can be created. The only way for these people to become happy is to sit alone. Each free row can support at most one happy singleton. Whenever a second leftover person is inserted into such a row, exactly one happy person is lost. The formula above counts that effect precisely, which proves the optimality of the algorithm.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n, r = map(int, input().split())
    a = list(map(int, input().split()))

    pairs = sum(x // 2 for x in a)
    odd = sum(x % 2 for x in a)

    ans = 2 * pairs
    free_rows = r - pairs

    if odd <= free_rows:
        ans += odd
    else:
        ans += 2 * free_rows - odd

    print(ans)
```

The first loop counts how many same-family pairs can be formed. Each such pair immediately contributes two happy people.

The second count tracks how many unpaired people remain. These are the only people whose happiness is still undecided.

`free_rows` is the number of rows not already occupied by family pairs. The final branch handles the two possible situations. Either every leftover person gets their own row, or there are more leftovers than available rows and some singletons must be paired together.

No special handling is needed for large values because all numbers are tiny. The expression `2 * free_rows - odd` is never negative in valid states because the total number of people fits in the bus.

## Worked Examples

### Example 1

Input:

```
3 3
2 3 1
```

| Family Size | Pairs Added | Odd Added |
| --- | --- | --- |
| 2 | 1 | 0 |
| 3 | 1 | 1 |
| 1 | 0 | 1 |

After processing all families:

| Variable | Value |
| --- | --- |
| pairs | 2 |
| odd | 2 |
| free_rows | 1 |
| initial answer | 4 |

Since `odd > free_rows`:

| Calculation | Value |
| --- | --- |
| happy leftovers | 2 * 1 - 2 = 0 |
| final answer | 4 |

The two family pairs already account for all happy people. The two leftovers must share a row.

### Example 2

Input:

```
3 3
2 2 2
```

| Family Size | Pairs Added | Odd Added |
| --- | --- | --- |
| 2 | 1 | 0 |
| 2 | 1 | 0 |
| 2 | 1 | 0 |

After processing all families:

| Variable | Value |
| --- | --- |
| pairs | 3 |
| odd | 0 |
| free_rows | 0 |
| initial answer | 6 |

Since there are no leftover people, the answer remains 6.

This example demonstrates that when every person can be placed into same-family pairs, everyone becomes happy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass over the family sizes |
| Space | O(1) | Only a few counters are stored |

The largest test case contains only 100 family sizes, so a linear scan is trivial. Even with 1000 test cases, the total work is far below the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n, r = map(int, input().split())
        a = list(map(int, input().split()))

        pairs = sum(x // 2 for x in a)
        odd = sum(x % 2 for x in a)

        ans = 2 * pairs
        free_rows = r - pairs

        if odd <= free_rows:
            ans += odd
        else:
            ans += 2 * free_rows - odd

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run(
"""4
3 3
2 3 1
3 3
2 2 2
4 5
1 1 2 2
4 5
3 1 1 3
"""
) == "4\n6\n6\n6", "samples"

# minimum size
assert run(
"""1
1 1
1
"""
) == "1", "single person sits alone"

# all equal values
assert run(
"""1
4 4
2 2 2 2
"""
) == "8", "everyone paired with family"

# leftover people exceed free rows
assert run(
"""1
2 3
3 3
"""
) == "4", "two leftovers must share a row"

# boundary case, bus exactly full
assert run(
"""1
2 2
1 3
"""
) == "2", "only one family pair contributes happiness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum possible instance |
| `2 2 2 2` | `8` | All people can be paired with family |
| `3 3` and `3 3` | `4` | Leftovers forced to share rows |
| `1 3` with `r=2` | `2` | Bus completely filled, mixed row unavoidable |

## Edge Cases

Consider

```
1
2 2
3 1
```

We have `pairs = 1`, `odd = 2`, and `free_rows = 1`.

The algorithm starts with `ans = 2`. Since `odd > free_rows`, it adds `2 * 1 - 2 = 0`. The final answer is 2. One leftover person can initially sit alone, but the second leftover must join that row and remove the singleton happiness. The result is correct.

Consider

```
1
4 5
1 1 1 1
```

We have `pairs = 0`, `odd = 4`, and `free_rows = 5`.

Since `odd <= free_rows`, every person can occupy a row alone. The algorithm returns 4. This correctly handles cases with no family pairs at all.

Consider

```
1
2 3
3 3
```

We have `pairs = 2`, `odd = 2`, and `free_rows = 1`.

The algorithm computes

```
ans = 2 * 2 = 4
happy leftovers = 2 * 1 - 2 = 0
```

giving a final answer of 4. The two leftovers cannot both be happy because only one row remains, so they must sit together. The counting matches the optimal seating arrangement exactly.
