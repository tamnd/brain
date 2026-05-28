---
title: "CF 44A - Indian Summer"
description: "Each leaf is described by two strings: the tree species and the leaf color. Alyona only keeps a leaf if she does not already have another leaf with the exact same pair of values. The task is simply to count how many distinct (species, color) combinations appear in the input."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 44
codeforces_index: "A"
codeforces_contest_name: "School Team Contest 2 (Winter Computer School 2010/11)"
rating: 900
weight: 44
solve_time_s: 83
verified: true
draft: false
---

[CF 44A - Indian Summer](https://codeforces.com/problemset/problem/44/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

Each leaf is described by two strings: the tree species and the leaf color. Alyona only keeps a leaf if she does not already have another leaf with the exact same pair of values.

The task is simply to count how many distinct `(species, color)` combinations appear in the input. If the same pair appears multiple times, it should only be counted once.

The constraints are very small. There are at most 100 leaves, and each string has length at most 10. Even an $O(n^2)$ comparison-based solution would easily fit within the time limit because the worst case would only perform about 10,000 comparisons. This means the problem is more about correct implementation than algorithmic optimization.

The main source of mistakes is misunderstanding what counts as a duplicate. Two leaves are considered identical only if both the species and the color match.

Consider this example:

```
3
birch yellow
birch green
birch yellow
```

The correct answer is:

```
2
```

A careless implementation that only tracks species would incorrectly return `1`.

Another easy mistake is counting colors independently from species.

```
3
maple red
birch red
oak red
```

The correct answer is:

```
3
```

All three leaves have the same color, but they come from different trees.

A final edge case is when every leaf is identical.

```
4
oak green
oak green
oak green
oak green
```

The correct answer is:

```
1
```

The algorithm must avoid counting repeated pairs multiple times.

## Approaches

The most direct solution is brute force. We can process leaves one by one and maintain a list of unique leaves found so far. For every new leaf, we scan the list and check whether the same `(species, color)` pair already exists. If not, we add it.

This works because the problem only asks whether a pair has appeared before. Since there are at most 100 leaves, the worst case performs about:

$$1 + 2 + 3 + \dots + 99 \approx 5000$$

pair comparisons, which is completely fine.

The limitation of the brute-force approach is that it repeatedly scans previously seen elements. If the input size were much larger, this repeated searching would become expensive.

The key observation is that a leaf description naturally behaves like a unique key. Python sets are designed exactly for this purpose. A set automatically removes duplicates, so if we insert every `(species, color)` pair into a set, the final set size is exactly the number of distinct leaves.

This changes the repeated linear search into average $O(1)$ insertion and lookup operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Accepted |
| Optimal | $O(n)$ average | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of leaves.
2. Create an empty set called `seen`.

The set will store pairs of `(species, color)`. Sets automatically ignore duplicates.
3. Repeat `n` times:

Read the species and color strings from input.
4. Insert the pair `(species, color)` into the set.

If the pair already exists, the set remains unchanged. If it is new, the set grows by one.
5. After processing all leaves, print the size of the set.

The number of elements in the set is exactly the number of distinct leaf descriptions.

### Why it works

The algorithm maintains the invariant that `seen` contains every unique `(species, color)` pair encountered so far.

Whenever a new leaf is processed, inserting it into the set preserves this invariant. Duplicate pairs do not create additional entries, while new pairs are added exactly once.

After all leaves are processed, every distinct leaf description appears exactly once in the set. The size of the set is therefore the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    seen = set()
    
    for _ in range(n):
        species, color = input().split()
        seen.add((species, color))
    
    print(len(seen))

solve()
```

The solution follows the algorithm directly.

The set `seen` stores tuples of `(species, color)`. Tuples are hashable in Python, so they can be inserted into a set safely and efficiently.

The line:

```
seen.add((species, color))
```

is the core of the solution. If the pair already exists, nothing changes. This avoids manual duplicate checking.

Using `input().split()` is safe because each line always contains exactly two strings separated by spaces.

There are no tricky boundary conditions in the implementation. Even when all leaves are identical or all are unique, the set behaves correctly automatically.

## Worked Examples

### Example 1

Input:

```
5
birch yellow
maple red
birch yellow
maple yellow
maple green
```

| Step | Current Leaf | Set Contents | Set Size |
| --- | --- | --- | --- |
| 1 | `(birch, yellow)` | `{(birch, yellow)}` | 1 |
| 2 | `(maple, red)` | `{(birch, yellow), (maple, red)}` | 2 |
| 3 | `(birch, yellow)` | `{(birch, yellow), (maple, red)}` | 2 |
| 4 | `(maple, yellow)` | `{(birch, yellow), (maple, red), (maple, yellow)}` | 3 |
| 5 | `(maple, green)` | `{(birch, yellow), (maple, red), (maple, yellow), (maple, green)}` | 4 |

Final output:

```
4
```

This trace shows how duplicate insertions do not change the set.

### Example 2

Input:

```
4
oak green
oak green
oak green
oak green
```

| Step | Current Leaf | Set Contents | Set Size |
| --- | --- | --- | --- |
| 1 | `(oak, green)` | `{(oak, green)}` | 1 |
| 2 | `(oak, green)` | `{(oak, green)}` | 1 |
| 3 | `(oak, green)` | `{(oak, green)}` | 1 |
| 4 | `(oak, green)` | `{(oak, green)}` | 1 |

Final output:

```
1
```

This example demonstrates that repeated identical leaves are counted only once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ average | Each set insertion is average $O(1)$ |
| Space | $O(n)$ | The set may store all leaves if all are unique |

With $n \le 100$, the solution is easily fast enough. Memory usage is also tiny because only at most 100 pairs are stored.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    
    seen = set()
    
    for _ in range(n):
        species, color = input().split()
        seen.add((species, color))
    
    print(len(seen))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""5
birch yellow
maple red
birch yellow
maple yellow
maple green
"""
) == "4\n", "sample 1"

# minimum input size
assert run(
"""1
oak red
"""
) == "1\n", "minimum case"

# all leaves identical
assert run(
"""4
oak green
oak green
oak green
oak green
"""
) == "1\n", "all equal"

# same color but different species
assert run(
"""3
oak red
birch red
maple red
"""
) == "3\n", "species matters"

# same species but different colors
assert run(
"""4
oak red
oak green
oak yellow
oak red
"""
) == "3\n", "color matters"

# maximum distinct small-style case
inp = "100\n"
for i in range(100):
    inp += f"tree{i} color{i}\n"

assert run(inp) == "100\n", "many unique pairs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single leaf | `1` | Minimum input size |
| All identical leaves | `1` | Duplicate removal |
| Same color, different species | `3` | Species is part of the key |
| Same species, different colors | `3` | Color is part of the key |
| 100 unique leaves | `100` | Handles maximum distinct entries |

## Edge Cases

Consider the case where only the species matches:

```
3
oak red
oak green
oak red
```

The algorithm processes the pairs in order.

After reading `(oak, red)`, the set contains one element.

After reading `(oak, green)`, the pair is different because the color changed, so the set size becomes two.

The final `(oak, red)` already exists in the set, so the size stays two.

The output is:

```
2
```

This confirms that the algorithm compares both fields together.

Now consider leaves with identical colors but different species:

```
3
birch yellow
maple yellow
oak yellow
```

Each insertion creates a new pair because the species differs every time.

The set evolves as:

```
{(birch, yellow)}
{(birch, yellow), (maple, yellow)}
{(birch, yellow), (maple, yellow), (oak, yellow)}
```

The output becomes:

```
3
```

This prevents the mistake of treating color alone as the identity.

Finally, consider the fully duplicated case:

```
5
pine green
pine green
pine green
pine green
pine green
```

The first insertion adds `(pine, green)` to the set. Every later insertion is ignored because the pair already exists.

The final set size is:

```
1
```

This confirms that duplicates are counted exactly once.
