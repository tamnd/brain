---
title: "CF 230A - Dragons"
description: "Kirito starts with some initial strength and must defeat every dragon on the level. Each dragon has two values: the minimum strength needed to beat it, and the bonus strength Kirito gains afterward."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 230
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 142 (Div. 2)"
rating: 1000
weight: 230
solve_time_s: 208
verified: true
draft: false
---

[CF 230A - Dragons](https://codeforces.com/problemset/problem/230/A)

**Rating:** 1000  
**Tags:** greedy, sortings  
**Solve time:** 3m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Kirito starts with some initial strength and must defeat every dragon on the level. Each dragon has two values: the minimum strength needed to beat it, and the bonus strength Kirito gains afterward.

A fight is only possible if Kirito's current strength is strictly greater than the dragon's strength. Equal strength is not enough. After winning, Kirito immediately becomes stronger and may be able to defeat tougher dragons later.

The order of fights is not fixed. We must decide whether there exists some ordering of dragons such that Kirito defeats all of them without ever losing.

The constraints are very small. There are at most $10^3$ dragons, so even $O(n^2)$ or $O(n^3)$ solutions would comfortably fit within the limit. That means the real challenge is not optimization, it is recognizing the correct greedy strategy.

The dangerous part of the problem is the strict comparison. Kirito must have strength strictly greater than the dragon's strength. A careless implementation using `>=` instead of `>` silently produces wrong answers.

Consider this input:

```
5 1
5 10
```

The correct output is:

```
NO
```

Kirito's strength equals the dragon's strength, so he loses immediately. Using `>=` would incorrectly accept this case.

Another subtle case is choosing dragons in the wrong order.

```
3 2
2 1
4 100
```

The correct output is:

```
YES
```

If Kirito fights the stronger dragon first, he loses. If he fights the weaker dragon first, his strength becomes $4$, which is still not enough because the comparison is strict. So this example is actually:

```
NO
```

Changing the first bonus slightly gives:

```
3 2
2 2
4 100
```

Now the correct output is:

```
YES
```

After defeating the first dragon, Kirito's strength becomes $5$, which is enough to beat the second dragon.

A naive approach that does not think carefully about fight order can easily fail on these boundary transitions.

## Approaches

The brute-force idea is to try every possible order of dragons. For each permutation, we simulate the fights and check whether Kirito survives all of them.

This works because the outcome of a fixed ordering is easy to simulate. We simply walk through the dragons in that order, maintaining Kirito's current strength.

The problem is the number of permutations. With $n$ dragons, there are $n!$ possible orders. Even for $n = 15$, this is already enormous. With $n = 1000$, brute force is completely impossible.

The key observation is that fighting weaker dragons earlier is always at least as good as fighting stronger dragons earlier.

Suppose Kirito can defeat two dragons, one with strength 3 and one with strength 10. If he defeats the weaker one first, he gains extra strength sooner, making future fights easier. Delaying easy fights gives no advantage because bonuses are non-negative.

This turns the problem into a simple greedy strategy:

1. Sort dragons by strength.
2. Fight them from weakest to strongest.
3. If Kirito ever cannot defeat the current dragon, the answer is impossible.

Why does this greedy order work? Because at every moment it minimizes the required current strength. If Kirito cannot defeat the weakest remaining dragon, then he also cannot defeat any stronger remaining dragon.

Sorting completely removes the need to explore different permutations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read Kirito's initial strength and the list of dragons.
2. Store each dragon as a pair `(strength, bonus)`.
3. Sort the dragons by their strength in increasing order.

The weakest dragon is always the safest available fight. Beating easier dragons first gives bonus strength earlier.
4. Iterate through the sorted dragons one by one.
5. For each dragon, compare Kirito's current strength with the dragon's strength.

If Kirito's strength is less than or equal to the dragon's strength, he loses immediately and the answer is `"NO"`.
6. Otherwise, Kirito defeats the dragon and gains the bonus strength.

Update:

$$s = s + bonus$$
7. If all dragons are defeated successfully, print `"YES"`.

### Why it works

The invariant is that before every fight, Kirito has achieved the maximum possible strength obtainable after defeating all weaker dragons.

Suppose the weakest remaining dragon cannot be defeated. Every other remaining dragon is at least as strong, so none of them can be defeated either. That means the game is already lost regardless of ordering.

If the weakest dragon can be defeated, taking it immediately is always safe because bonuses are non-negative. Fighting it earlier only increases future strength and never blocks any future option.

Because of this property, sorting by dragon strength produces an optimal order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s, n = map(int, input().split())

    dragons = []
    for _ in range(n):
        x, y = map(int, input().split())
        dragons.append((x, y))

    dragons.sort()

    for x, y in dragons:
        if s <= x:
            print("NO")
            return
        s += y

    print("YES")

solve()
```

The first part reads the initial strength and all dragons. Each dragon is stored as a tuple where the first value is the dragon's strength and the second value is the reward after defeating it.

The call to `sort()` is the core greedy step. Python sorts tuples lexicographically, so dragons are ordered by increasing strength automatically.

The loop simulates the fights in that order. The condition `s <= x` is critical. The problem requires strictly greater strength, so equality still means defeat.

After winning a fight, the bonus is added immediately. This updated strength is then used for later dragons.

The solution exits early as soon as Kirito loses a fight. There is no reason to continue simulation after failure.

Python integers are arbitrary precision, so overflow is never a concern here.

## Worked Examples

### Example 1

Input:

```
2 2
1 99
100 0
```

Sorted dragons:

```
(1, 99), (100, 0)
```

| Step | Current Strength | Dragon Strength | Bonus | Result |
| --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 99 | Win, strength becomes 101 |
| 2 | 101 | 100 | 0 | Win, strength remains 101 |

Final output:

```
YES
```

This trace shows why defeating weaker dragons first is valuable. The first dragon gives a huge strength increase that makes the second fight possible.

### Example 2

Input:

```
5 1
5 10
```

Sorted dragons:

```
(5, 10)
```

| Step | Current Strength | Dragon Strength | Bonus | Result |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 10 | Lose immediately |

Final output:

```
NO
```

This example demonstrates the strict comparison rule. Equal strength is not enough.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates the runtime |
| Space | $O(n)$ | The dragon list stores all pairs |

With at most 1000 dragons, this solution is far below the time limit. Sorting 1000 elements is extremely fast, and the simulation afterward is linear.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        s, n = map(int, input().split())

        dragons = []
        for _ in range(n):
            x, y = map(int, input().split())
            dragons.append((x, y))

        dragons.sort()

        for x, y in dragons:
            if s <= x:
                return "NO"
            s += y

        return "YES"

    return solve()

# provided sample
assert run(
    "2 2\n"
    "1 99\n"
    "100 0\n"
) == "YES", "sample 1"

# minimum-size losing case
assert run(
    "1 1\n"
    "1 0\n"
) == "NO", "strict inequality"

# minimum-size winning case
assert run(
    "2 1\n"
    "1 0\n"
) == "YES", "single easy dragon"

# requires sorting to succeed
assert run(
    "3 2\n"
    "4 100\n"
    "2 2\n"
) == "YES", "correct greedy ordering"

# impossible even after smaller fights
assert run(
    "3 2\n"
    "2 1\n"
    "4 100\n"
) == "NO", "boundary transition"

# many equal dragons
assert run(
    "10 4\n"
    "1 0\n"
    "1 0\n"
    "1 0\n"
    "1 0\n"
) == "YES", "all equal weak dragons"

# large bonuses chain correctly
assert run(
    "2 3\n"
    "1 100\n"
    "50 100\n"
    "120 0\n"
) == "YES", "strength accumulation"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 0` | `NO` | Equality is losing |
| `2 1 / 1 0` | `YES` | Simplest successful fight |
| Unsorted solvable case | `YES` | Sorting is necessary |
| Boundary transition case | `NO` | Small bonus may still be insufficient |
| Multiple equal weak dragons | `YES` | Repeated easy fights |
| Large bonus chain | `YES` | Strength accumulation across fights |

## Edge Cases

A common mistake is allowing equal strength to win.

Input:

```
5 1
5 10
```

The dragons are already sorted. Kirito starts with strength 5. The algorithm checks:

```
5 <= 5
```

This condition is true, so the algorithm immediately prints `"NO"`.

That matches the problem rules because Kirito must be strictly stronger.

Another subtle case is when sorting changes the outcome.

Input:

```
3 2
4 100
2 2
```

After sorting:

```
(2, 2), (4, 100)
```

Simulation:

1. Kirito defeats strength-2 dragon, strength becomes 5.
2. Kirito defeats strength-4 dragon.

The answer is `"YES"`.

Without sorting, Kirito would fight the strength-4 dragon first and lose immediately. This demonstrates why the greedy ordering matters.

A final edge case is when smaller dragons still do not provide enough growth.

Input:

```
3 2
2 1
4 100
```

After sorting, the order stays the same.

1. Kirito defeats the first dragon and reaches strength 4.
2. The second dragon also has strength 4.

Because the comparison is strict, Kirito still loses. The algorithm correctly prints `"NO"` instead of incorrectly treating equality as success.
