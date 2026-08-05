---
title: "CF 102501B - Biodiversity"
description: "The input describes a census of animals in a garden. Each line after the first contains the name of one species. The task is to find whether one species has a population strictly larger than the combined population of every other species."
date: "2026-08-06T04:42:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 65
verified: true
draft: false
---

[CF 102501B - Biodiversity](https://codeforces.com/problemset/problem/102501/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a census of animals in a garden. Each line after the first contains the name of one species. The task is to find whether one species has a population strictly larger than the combined population of every other species. If such a species exists, we print its name. Otherwise, we print `NONE`.

The condition can be rewritten using counts. If a species appears `x` times among `N` animals, all other species together appear `N - x` times. We need a species where `x > N - x`, which is equivalent to `2x > N`. This means the answer must be a strict majority species.

The limit of `N` being up to `2 * 10^5` means every animal can be processed only a small number of times. An approach that compares every species against every other species could require around `N^2` operations, which is far too many at this size. We need a linear or near-linear solution.

A few cases are easy to mishandle. If the largest species appears exactly half of the animals, it is not enough because the requirement is strict. For example:

```
4
cat
dog
cat
dog
```

The correct output is:

```
NONE
```

A careless solution that checks `>=` instead of `>` would incorrectly choose `cat` or `dog`.

Another edge case is when there is only one animal. The only species appears more times than all other species combined because the other side has size zero.

```
1
lion
```

The correct output is:

```
lion
```

A solution that assumes there must be at least two different species could fail here.

A final subtle case is when several species exist but one of them barely crosses the threshold.

```
5
bird
bird
bird
fish
frog
```

The correct output is:

```
bird
```

The count is three, while every other species together has two animals. Solutions looking only for the most frequent species without checking the majority condition may produce an incorrect answer in cases where the maximum count is still not enough.

## Approaches

A direct approach is to count every species and then test each species separately. After building the counts, we could take each species and compare its count with the sum of all other counts. The method is correct because it checks the exact condition from the statement. However, if implemented poorly by scanning all species for every candidate, the number of comparisons can reach the square of the number of animals. With `N = 200000`, this can approach forty billion operations, which is not feasible.

The useful observation is that the condition depends only on the largest count. If some species has more animals than all others combined, that species must also be the most frequent species. We only need to know which species has the maximum frequency and whether its frequency is greater than `N / 2`.

This allows a simple two-pass solution. First, count how many times every species appears. Second, search for a species whose count satisfies `2 * count > N`. The dictionary handles the counting efficiently, and the total work is proportional to the number of animals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Too slow |
| Optimal | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read all species names and count their occurrences using a hash map. Each animal contributes exactly one increment to its species counter, so this step captures the complete population distribution.
2. Store the total number of animals as `N`. The majority condition for a species with frequency `c` is `c > N - c`, which is the same as `2 * c > N`.
3. Iterate through the frequency map and find any species satisfying `2 * count > N`. Since two different species cannot both have more than half of the total population, finding one valid species is enough.
4. If no species satisfies the condition, output `NONE`.

Why it works: the required species must have a count larger than every other species combined. That means its count must be larger than half of all animals. The algorithm checks exactly this property for every species after computing the correct frequencies. Any valid answer will pass the condition, and no invalid species can pass it because the inequality is precisely the definition of the required majority.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return

    n = int(n_line)
    count = {}

    for _ in range(n):
        species = input().strip()
        count[species] = count.get(species, 0) + 1

    for species, freq in count.items():
        if freq * 2 > n:
            print(species)
            return

    print("NONE")

if __name__ == "__main__":
    solve()
```

The dictionary stores the number of appearances for every species. Python dictionaries provide average constant-time insertion and lookup, so processing all input lines remains linear.

The final loop does not need to compare against other species. The expression `freq * 2 > n` already represents whether this species is larger than all remaining animals combined. Multiplication is used instead of division to avoid any boundary problems with integer division.

There is no integer overflow concern in Python because integers automatically grow when needed. The input reading uses `sys.stdin.readline`, which is suitable for the large number of lines.

## Worked Examples

For the first sample:

```
3
frog
fish
frog
```

The counting process is:

| Read animal | Current counts | Check |
| --- | --- | --- |
| frog | frog: 1 | continue |
| fish | frog: 1, fish: 1 | continue |
| frog | frog: 2, fish: 1 | continue |

The final counts are `frog = 2` and `fish = 1`. Since `2 * 2 > 3`, `frog` is a valid answer.

For the second sample:

```
4
cat
mouse
mouse
cat
```

The counting process is:

| Read animal | Current counts | Check |
| --- | --- | --- |
| cat | cat: 1 | continue |
| mouse | cat: 1, mouse: 1 | continue |
| mouse | cat: 1, mouse: 2 | continue |
| cat | cat: 2, mouse: 2 | continue |

Both species have frequency `2`. The majority test gives `2 * 2 > 4`, which is false, so the answer is `NONE`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each species name is read once and each stored frequency is checked once. |
| Space | O(N) | In the worst case every animal has a different species name, so the dictionary stores N entries. |

The maximum input size is `200000` animals. A linear pass easily fits the available time limit, and the dictionary size is within the memory limit.

## Test Cases

```python
import sys
import io

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    data = sys.stdin.readline
    n = int(data())
    count = {}

    for _ in range(n):
        s = data().strip()
        count[s] = count.get(s, 0) + 1

    ans = "NONE"
    for s, c in count.items():
        if c * 2 > n:
            ans = s
            break

    sys.stdin = old_stdin
    return ans

assert solution("3\nfrog\nfish\nfrog\n") == "frog", "sample 1"
assert solution("4\ncat\nmouse\nmouse\ncat\n") == "NONE", "sample 2"

assert solution("1\nlion\n") == "lion", "single animal"
assert solution("5\na\na\na\nb\nc\n") == "a", "bare majority"
assert solution("6\nx\nx\ny\ny\nz\nz\n") == "NONE", "exact half"
assert solution("200000\n" + "bird\n" * 200000) == "bird", "maximum size all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` animal with one species | `lion` | Handles the smallest possible input. |
| Three copies of one species among five animals | `a` | Checks a strict majority just above the boundary. |
| Three species with equal counts | `NONE` | Checks the exact half condition and prevents `>=` mistakes. |
| Two hundred thousand identical species | `bird` | Confirms the linear approach handles the maximum input size. |

## Edge Cases

The exact-half case is handled by the multiplication check. For:

```
4
cat
dog
cat
dog
```

the dictionary contains `cat: 2` and `dog: 2`. The algorithm checks `2 * 2 > 4`, which is false for both, so it prints `NONE`.

The one-animal case works because the only frequency is `1`, and the condition becomes `2 * 1 > 1`, which is true. The algorithm prints the only species without needing special handling.

The barely-majority case:

```
5
bird
bird
bird
fish
frog
```

produces `bird: 3`, `fish: 1`, and `frog: 1`. The check `2 * 3 > 5` succeeds, so `bird` is returned. The algorithm does not need to know the exact sum of the other species because the majority inequality already captures it.

I can also adapt this editorial into a shorter Codeforces-style version with less exposition and a more compact proof if you need one.
