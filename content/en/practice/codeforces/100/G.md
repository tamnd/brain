---
title: "CF 100G - Name the album"
description: "Aryo wants to choose a title for a new album from a list of candidate names. Some names have already been used in previous years. His decision rule has two layers. If a candidate name has never been used before, that is the best possible choice."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "G"
codeforces_contest_name: "Unknown Language Round 3"
rating: 1800
weight: 100
solve_time_s: 110
verified: true
draft: false
---

[CF 100G - Name the album](https://codeforces.com/problemset/problem/100/G)

**Rating:** 1800  
**Tags:** *special, data structures, implementation  
**Solve time:** 1m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

Aryo wants to choose a title for a new album from a list of candidate names. Some names have already been used in previous years. His decision rule has two layers.

If a candidate name has never been used before, that is the best possible choice. Among all unused candidates, he chooses the alphabetically largest one.

If every candidate has been used before, he chooses the one whose most recent usage happened the longest time ago. If several names share the same oldest year, he again chooses the alphabetically largest one.

The input gives a history of album names together with publication years, then a list of possible new names. We must print the chosen title.

The constraints immediately suggest that the solution should be close to linear. There can be up to $10^5$ used names, so repeatedly scanning the whole history for every candidate would become expensive. A quadratic solution could reach around $10^9$ operations, which is far beyond what fits in a 2 second limit. Hash maps are the natural tool here because we only need fast lookup of the most recent year associated with each name.

One subtle point is that a name may appear multiple times in the history. We are not interested in the earliest year, we are interested in the most recent usage. Consider this input:

```
3
echo 1999
echo 2005
nova 2001
2
echo
nova
```

The correct answer is `nova`, because `nova` was last used in 2001 while `echo` was last used in 2005. A careless implementation that stores the first occurrence instead of the latest would incorrectly choose `echo`.

Another easy mistake is mishandling ties alphabetically. Suppose we have:

```
2
alpha 2000
beta 2000
2
alpha
beta
```

Both names were used equally long ago, so the answer must be `beta` because it is alphabetically later. If we only track the minimum year and stop updating on ties, we would return the wrong result.

Unused names also require careful handling. They are always preferred over used names regardless of years. For example:

```
1
dream 2010
2
dream
vision
```

The correct answer is `vision`, even though `dream` has a valid old year. Treating unused names as having year `0` works conceptually, but only if the implementation explicitly prioritizes them over used names.

## Approaches

A direct brute-force solution would process every candidate name by scanning the entire history to determine whether it appeared before and what its latest year was. For each candidate, we compare against all previously used names and keep the maximum year seen for that candidate.

This works logically because it computes exactly the information required for the decision rule. The problem is the cost. With $10^5$ historical entries and $10^4$ candidates, the worst case becomes $10^9$ comparisons. Python cannot handle that amount of work within the time limit.

The structure of the problem gives a much faster direction. Every query asks the same thing: “what is the latest year associated with this name?” Recomputing that repeatedly is wasteful. Instead, we preprocess the history once into a hash map from name to latest year.

While reading the history, we update:

```
latest[name] = max(latest[name], year)
```

After preprocessing, each candidate can be evaluated in constant expected time.

The decision rule itself can also be simplified. An unused name is always better than a used one. Among unused names, choose the alphabetically largest. If no unused name exists, choose the used name with the smallest latest year, breaking ties by alphabetically largest.

This turns the whole problem into a single pass over the candidates with simple comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot m)$ | $O(1)$ | Too slow |
| Optimal | $O(n + m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Create a dictionary called `latest`.

This dictionary will store the most recent year each album name was used.
2. Read the historical album names one by one.

For each `(name, year)` pair, update:

```
latest[name] = max(existing_year, year)
```

We keep the maximum year because the problem cares about the latest usage, not the first usage.
3. Initialize two tracking variables.

One variable stores the best unused candidate found so far.

Another stores the best used candidate together with its latest usage year.
4. Process every candidate name.

If the name does not exist in `latest`, it is unused. Compare it with the current best unused candidate and keep the alphabetically larger one.
5. If the candidate has been used before, retrieve its latest year from the dictionary.

Compare it with the current best used candidate.

A candidate is better if:

- its latest year is smaller, meaning it was used longer ago
- or the years are equal and the name is alphabetically larger
6. After all candidates are processed, check whether an unused candidate exists.

If yes, print the best unused candidate because unused names always have priority.

Otherwise print the best used candidate.

### Why it works

The dictionary invariant is that after preprocessing, `latest[name]` equals the most recent year that name appeared in the history. Every update preserves this because we always keep the maximum year seen so far.

During candidate processing, the unused tracker always stores the alphabetically largest unused name encountered so far. The used tracker always stores the best candidate according to the ordering:

1. Smaller latest year is better.
2. If years are equal, alphabetically larger is better.

Since every candidate is compared against the current optimum under exactly these rules, the final stored answer is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    latest = {}

    for _ in range(n):
        name, year = input().split()
        year = int(year)

        if name not in latest or year > latest[name]:
            latest[name] = year

    m = int(input())

    best_unused = None

    best_used_name = None
    best_used_year = float('inf')

    for _ in range(m):
        name = input().strip()

        if name not in latest:
            if best_unused is None or name > best_unused:
                best_unused = name
        else:
            year = latest[name]

            if (year < best_used_year or
               (year == best_used_year and name > best_used_name)):
                best_used_year = year
                best_used_name = name

    if best_unused is not None:
        print(best_unused)
    else:
        print(best_used_name)

if __name__ == "__main__":
    solve()
```

The first section builds the `latest` dictionary. The important detail is using the maximum year for repeated names. Forgetting this changes the meaning of the problem completely because we care about the most recent use.

The second section scans the candidate list once. The code separates unused and used candidates because unused names always dominate used ones. This avoids awkward artificial values like assigning unused names year `-1`.

The tie-breaking logic is written explicitly:

```
year < best_used_year
```

means the name was used longer ago, which is better.

```
year == best_used_year and name > best_used_name
```

implements the alphabetical tie-break. Using `>` works because Python compares strings lexicographically.

The initialization with `float('inf')` guarantees that the first used candidate will always replace the initial placeholder.

## Worked Examples

### Sample 1

Input:

```
3
eyesonme 2008
anewdayhascome 2002
oneheart 2003
2
oneheart
bienbien
```

Processing history:

| Name | Year | latest after update |
| --- | --- | --- |
| eyesonme | 2008 | {eyesonme: 2008} |
| anewdayhascome | 2002 | {eyesonme: 2008, anewdayhascome: 2002} |
| oneheart | 2003 | {eyesonme: 2008, anewdayhascome: 2002, oneheart: 2003} |

Processing candidates:

| Candidate | Used Before | Action | Current Best |
| --- | --- | --- | --- |
| oneheart | Yes | best used = oneheart | used: oneheart |
| bienbien | No | best unused = bienbien | unused: bienbien |

The algorithm prints `bienbien` because any unused name outranks all used names.

### Custom Example

Input:

```
4
alpha 2005
beta 2000
gamma 2000
alpha 2010
3
alpha
beta
gamma
```

Processing history:

| Name | Year | latest after update |
| --- | --- | --- |
| alpha | 2005 | {alpha: 2005} |
| beta | 2000 | {alpha: 2005, beta: 2000} |
| gamma | 2000 | {alpha: 2005, beta: 2000, gamma: 2000} |
| alpha | 2010 | {alpha: 2010, beta: 2000, gamma: 2000} |

Processing candidates:

| Candidate | Latest Year | Comparison Result | Current Best Used |
| --- | --- | --- | --- |
| alpha | 2010 | first candidate | alpha |
| beta | 2000 | older than 2010 | beta |
| gamma | 2000 | same year, alphabetically larger | gamma |

The algorithm outputs `gamma`.

This trace demonstrates both critical details: repeated names must keep the latest year, and equal years require alphabetical comparison.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each history entry and each candidate is processed once |
| Space | $O(n)$ | The dictionary stores at most one entry per distinct used name |

The largest input sizes fit comfortably within these bounds. Around $10^5$ dictionary operations are trivial for Python, and the memory usage stays well below the 64 MB limit because names are short.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    latest = {}

    for _ in range(n):
        name, year = input().split()
        year = int(year)

        if name not in latest or year > latest[name]:
            latest[name] = year

    m = int(input())

    best_unused = None

    best_used_name = None
    best_used_year = float('inf')

    for _ in range(m):
        name = input().strip()

        if name not in latest:
            if best_unused is None or name > best_unused:
                best_unused = name
        else:
            year = latest[name]

            if (year < best_used_year or
               (year == best_used_year and name > best_used_name)):
                best_used_year = year
                best_used_name = name

    if best_unused is not None:
        print(best_unused)
    else:
        print(best_used_name)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run(
"""3
eyesonme 2008
anewdayhascome 2002
oneheart 2003
2
oneheart
bienbien
"""
) == "bienbien", "sample 1"

# minimum input
assert run(
"""0
1
solo
"""
) == "solo", "single unused name"

# repeated historical names
assert run(
"""3
echo 1999
echo 2005
nova 2001
2
echo
nova
"""
) == "nova", "must keep latest year"

# tie on year, alphabetical rule
assert run(
"""2
alpha 2000
beta 2000
2
alpha
beta
"""
) == "beta", "alphabetical tie break"

# multiple unused names
assert run(
"""1
dream 2010
3
vision
future
galaxy
"""
) == "vision", "largest alphabetical unused name"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No historical names | `solo` | Correct handling when every candidate is unused |
| Repeated historical name | `nova` | Latest year must overwrite earlier years |
| Equal years | `beta` | Alphabetical tie-breaking among used names |
| Multiple unused names | `vision` | Alphabetically largest unused candidate wins |

## Edge Cases

Consider repeated album names in the history:

```
3
echo 1999
echo 2005
nova 2001
2
echo
nova
```

The dictionary evolves as:

```
echo -> 1999
echo -> 2005
nova -> 2001
```

When candidates are checked, `echo` has latest year `2005` while `nova` has `2001`. Since `2001` is older, the answer becomes `nova`. The algorithm handles this correctly because it always stores the maximum year for each name.

Now consider equal years:

```
2
alpha 2000
beta 2000
2
alpha
beta
```

Both candidates have the same latest usage year. The algorithm reaches the tie-breaking condition:

```
year == best_used_year and name > best_used_name
```

Since `"beta" > "alpha"` lexicographically, the answer becomes `beta`.

Finally, consider the interaction between used and unused names:

```
1
dream 2010
2
dream
vision
```

`dream` becomes the current best used candidate. Then `vision` is identified as unused, so it is stored separately in `best_unused`. At the end, the algorithm always prints an unused candidate if one exists, so the output is `vision`.
