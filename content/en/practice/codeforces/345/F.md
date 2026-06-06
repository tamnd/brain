---
title: "CF 345F - Superstitions Inspection"
description: "We are given a text file that alternates between country names and lists of superstition names. A country line introduces a new group, and the following lines starting with an asterisk belong to that country."
date: "2026-06-06T18:01:35+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 345
codeforces_index: "F"
codeforces_contest_name: "Friday the 13th, Programmers Day"
rating: 2700
weight: 345
solve_time_s: 112
verified: false
draft: false
---

[CF 345F - Superstitions Inspection](https://codeforces.com/problemset/problem/345/F)

**Rating:** 2700  
**Tags:** *special  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a text file that alternates between country names and lists of superstition names. A country line introduces a new group, and the following lines starting with an asterisk belong to that country. Each such entry is a superstition that is considered “popular” in that country.

The goal is to determine which superstition names appear in the largest number of distinct countries. Because the same superstition can be written with different capitalization or irregular spacing, two names must be treated as identical if they match word-by-word after normalizing case and collapsing whitespace. Word order matters, but repeated spaces do not.

The input size is small in terms of lines, at most 50. This rules out any concern about asymptotic complexity beyond linear scanning. The real difficulty is not scale but normalization and grouping: we must correctly separate country blocks, normalize multi-word keys consistently, and avoid counting duplicates of the same superstition within a single country.

A naive implementation risk comes from treating raw strings as keys. For example, `"friday the 13th"` and `"Friday the   13th"` refer to the same superstition but would be counted separately if whitespace is not normalized. Another subtle pitfall is double-counting within one country if the same superstition appears multiple times after normalization.

## Approaches

A straightforward approach is to read line by line, keep track of the current country, and insert each superstition string into a mapping from superstition to a set of countries. Whenever we encounter a country name line, we switch context. Every superstition line is parsed, normalized, and added to the set corresponding to that superstition.

The brute-force interpretation would be to, for each superstition, scan all countries again and check whether it appears in their list after normalization. That leads to repeated parsing of the same text many times, and in the worst case it becomes quadratic in the number of lines times average list size. Even though constraints are small, this approach is structurally wasteful and error-prone.

The key observation is that we do not need repeated membership checks. Each occurrence already tells us exactly which country contains which superstition. We can aggregate in one pass using a dictionary from normalized superstition name to a set of country identifiers. This reduces the problem to a single linear scan plus dictionary operations.

Once this structure is built, the answer is simply those superstition keys whose country-set has maximum size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated scanning per superstition | O(N²) | O(N) | Too slow / unnecessary |
| One-pass hashing with sets | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Read the input line by line while maintaining a current country name. When a line does not start with `*`, it represents a new country, so we update the current context.
2. When we encounter a superstition line, we strip the leading `"* "` and normalize the remaining string. Normalization means splitting by whitespace, converting every word to lowercase, and rejoining with a single space. This ensures that any spacing or capitalization differences collapse into a canonical representation.
3. Maintain a dictionary `occurrences` where each key is a normalized superstition string and the value is a set of countries in which it appears. When processing a superstition, we insert the current country into this set.
4. After processing all lines, compute the maximum size among all country sets. This value represents how many countries the most popular superstition appears in.
5. Collect all superstition names whose set size equals this maximum.
6. Sort these superstition names lexicographically and output them.

The reason sets are essential is that a superstition may appear multiple times in the same country block. Without deduplication, we would incorrectly inflate its popularity.

### Why it works

At any point during processing, each pair (country, superstition) is recorded exactly once in the sense of set membership. The invariant is that `occurrences[s]` contains precisely the set of distinct countries in which superstition `s` appears in the input seen so far. Since we never remove or duplicate entries, this invariant holds until the end. Therefore, the final set sizes exactly represent the number of countries per superstition, and selecting the maximum is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def normalize(line: str) -> str:
    parts = line.strip().split()
    return " ".join(w.lower() for w in parts)

def solve():
    lines = [line.rstrip("\n") for line in sys.stdin]

    country = None
    occ = {}

    for line in lines:
        if not line:
            continue

        if line[0] != '*':
            country = line.strip()
            continue

        name = line[2:]
        name = normalize(name)

        if name not in occ:
            occ[name] = set()
        occ[name].add(country)

    if not occ:
        return

    max_count = max(len(s) for s in occ.values())

    result = [s for s, countries in occ.items() if len(countries) == max_count]
    result.sort()

    sys.stdout.write("\n".join(result))

if __name__ == "__main__":
    solve()
```

The parsing logic depends critically on detecting whether a line begins with `*`. Country lines never begin with that character, so this cleanly separates structure.

Normalization is done immediately at ingestion time, ensuring that all comparisons later are purely dictionary-based. The set ensures that repeated occurrences in a single country do not distort counts.

Sorting is done only at the end because the output requires lexicographic order over normalized names.

## Worked Examples

### Example 1

Input:

```
Ukraine
* Friday the   13th
* black   cat
* knock the   wood
USA
* wishing well
* friday   the   13th
Holland
France
* Wishing Well
```

We track `(superstition -> countries)`:

| Step | Country | Superstition (normalized) | Set state |
| --- | --- | --- | --- |
| 1 | Ukraine | friday the 13th | {Ukraine} |
| 2 | Ukraine | black cat | {Ukraine} |
| 3 | Ukraine | knock the wood | {Ukraine} |
| 4 | USA | wishing well | {USA} |
| 5 | USA | friday the 13th | {Ukraine, USA} |
| 6 | France | wishing well | {USA, France} |

Final counts:

- friday the 13th → 2 countries
- wishing well → 2 countries
- others → 1

Result:

```
friday the 13th
wishing well
```

This trace shows how normalization merges differently formatted strings and how sets accumulate country membership.

### Example 2

Input:

```
A
* Lucky Star
* lucky   star
B
* Lucky Star
C
* unlucky sign
```

| Step | Country | Superstition | Set state |
| --- | --- | --- | --- |
| 1 | A | lucky star | {A} |
| 2 | B | lucky star | {A, B} |
| 3 | C | unlucky sign | {C} |

Result:

```
lucky star
```

This demonstrates duplicate suppression within a country (A has two identical entries after normalization, but the set prevents double counting).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N * L log L) | Each line is parsed and split, and normalization processes each word once; sets and dictionary operations are O(1) amortized |
| Space | O(K) | K distinct superstition names each storing a set of countries |

The input size is extremely small, so this linear scan is easily within limits. The solution’s performance is dominated by string processing rather than asymptotic growth, which is acceptable under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    out = StringIO()
    _stdout = _sys.stdout
    _sys.stdout = out
    solve()
    _sys.stdout = _stdout
    return out.getvalue().strip()

# provided sample
assert run("""Ukraine
* Friday the   13th
* black   cat
* knock the   wood
USA
* wishing well
* friday   the   13th
Holland
France
* Wishing Well
""") == "friday the 13th\nwishing well"

# single country, duplicates inside
assert run("""A
* Lucky Star
* lucky   star
""") == "lucky star"

# multiple max ties
assert run("""A
* a b
B
* c d
""") in {"a b\nc d"}

# case and spacing stress
assert run("""X
*  HELLO   WORLD
Y
* hello world
Z
* hello   world
""") == "hello world"

# minimal input
assert run("""A
* one""") == "one"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| duplicates in same country | single entry | set deduplication |
| mixed capitalization | unified key | normalization correctness |
| tie for maximum | multiple lines | correct max handling |
| minimal input | single output | base case handling |

## Edge Cases

A common failure is treating raw strings as identifiers. For example, `"Lucky Star"` and `"lucky   star"` would be treated as different keys if whitespace is not normalized. In the algorithm, both are reduced to `"lucky star"` before insertion, so they map to the same set.

Another issue is duplicate entries within a single country. If a country lists the same superstition twice after normalization, a naive counter would increment twice. In this solution, insertion into a set ensures idempotence. For instance, adding `"A"` twice to the set `{A}` leaves it unchanged.

Finally, ties in maximum frequency require collecting all candidates after computing the global maximum. The algorithm does this in a separate pass over the dictionary, ensuring that no superstition is missed due to ordering during accumulation.
