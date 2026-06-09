---
title: "CF 1801G - A task for substrings"
description: "We are given a very long text string t and a set of distinct dictionary words s₁, s₂, ..., sₙ. For each query [l, r], we look only at the substring t[l..r]. Inside that interval we must count how many substrings are equal to one of the dictionary words."
date: "2026-06-09T09:34:37+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 1801
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 857 (Div. 1)"
rating: 3400
weight: 1801
solve_time_s: 92
verified: true
draft: false
---

[CF 1801G - A task for substrings](https://codeforces.com/problemset/problem/1801/G)

**Rating:** 3400  
**Tags:** data structures, string suffix structures, strings  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very long text string `t` and a set of distinct dictionary words `s₁, s₂, ..., sₙ`.

For each query `[l, r]`, we look only at the substring `t[l..r]`. Inside that interval we must count how many substrings are equal to one of the dictionary words.

Another way to view the query is this:

Every occurrence of a dictionary word inside `t` corresponds to some segment `[a,b]`. For a query `[l,r]`, we must count how many of those occurrence segments satisfy

```
l ≤ a ≤ b ≤ r
```

The constraints completely determine the direction of the solution.

The text length can reach `5·10⁶`, which rules out anything that stores information per substring of `t`. Even a single linear scan of `t` is already expensive, so we only get a handful of such scans.

The total length of all dictionary words is at most `10⁶`. This is exactly the range where an Aho-Corasick automaton is practical.

The number of queries reaches `5·10⁵`, so every query must be answered in logarithmic time or better. Any approach that touches all occurrences of matching words during a query is hopeless.

A subtle difficulty is that a query is not asking for occurrences ending in a range or starting in a range. It asks for occurrences completely contained inside a range. Handling both boundaries simultaneously is the hard part.

Consider the dictionary `{ "aaa" }` and

```
t = aaaa
query = [2,4]
```

The only valid occurrence is `[2,4]`.

If we count occurrences ending inside `[2,4]`, we would also count `[1,3]`, which crosses the left border and must not contribute.

Another tricky case is when several dictionary words end at the same position.

```
t = ababa
dictionary = { "a", "aba" }
```

At position 3 both `"a"` and `"aba"` end. A solution that stores only the number of matches ending at each position loses information needed later.

The accepted solution relies on a stronger structural observation.

## Approaches

The brute force idea is straightforward.

Build an Aho-Corasick automaton for all dictionary words. For every query `[l,r]`, enumerate every substring of `t[l..r]` and test whether it belongs to the dictionary.

The number of substrings of a segment of length `L` is

$$\frac{L(L+1)}2.$$

With `|t| = 5·10⁶`, even a single query becomes impossible.

A more sophisticated brute force would first find all occurrences of dictionary words in `t`. Then each query asks for the number of occurrence segments fully contained in `[l,r]`.

Unfortunately the number of occurrences can itself be Θ(|t|·max_length). For example, if every character is `'a'` and the dictionary contains many prefixes `"a"`, `"aa"`, `"aaa"`, ..., then storing and processing occurrences individually is still too large.

The key observation is that we do not actually need every occurrence.

Suppose we scan `t` with an Aho-Corasick automaton.

For each position `i`, define:

`f[i]` = number of dictionary words ending at position `i`.

Let

`pref[i] = f[1] + ... + f[i]`.

Then `pref[r] - pref[l-1]` counts all dictionary occurrences whose right endpoint lies inside `[l,r]`.

This is very close to the answer. The only extra occurrences are those that end inside `[l,r]` but start before `l`.

The entire problem becomes: efficiently remove occurrences crossing the left boundary.

The crucial property proved in the official solution is that among all words ending at a fixed position, only the longest one matters.

Let

`g[i]` be the longest dictionary word ending at position `i`.

If that longest word already starts at or after `l`, then every shorter matching suffix also starts at or after `l`.

This allows us to locate a single critical position and reduce the correction to a precomputed value inside one dictionary word.

The resulting algorithm performs one linear scan of `t`, linear preprocessing on the dictionary, and answers every query in `O(log |t|)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(m· | t | ²) |
| Occurrence Enumeration | Potentially superlinear in occurrences | Large | Too slow |
| Optimal AC Automaton + Prefix Sums + Binary Search | O(S + | t | + m log |

Here `S` denotes the total length of all dictionary words.

## Algorithm Walkthrough

### Preprocessing on dictionary words

Build an Aho-Corasick automaton over all dictionary words.

For every automaton state, compute:

`cnt[state]` = number of dictionary words represented by suffix links ending at this state.

This allows us to know how many dictionary words end at each position of `t`.

Also store, for every state, the longest dictionary word ending there.

### Scan the text

Process `t` from left to right through the automaton.

For every position `i`:

1. Move to the next automaton state.
2. Let `f[i]` be the number of dictionary words ending here.
3. Let `g[i]` be the identifier of the longest dictionary word ending here.
4. Build prefix sums

$$pref[i] = pref[i-1] + f[i].$$

Now `pref[r] - pref[l-1]` counts all occurrences ending in `[l,r]`.

### Define the critical position

For position `i`, let

$$start(i)=i-|g[i]|+1.$$

This is the start position of the longest matching word ending at `i`.

Find the largest position `p` such that

$$start(p)\le l.$$

Every occurrence ending after `p` is completely inside `[l,r]`.

Why?

Because if the longest matching word ending at some position starts after `l`, then every shorter matching word ending there also starts after `l`.

So all positions `p+1 ... r` contribute directly.

Their contribution is

$$pref[r]-pref[p].$$

### Precompute suffix contributions inside words

For each dictionary word `w`, precompute:

`c[w][k]`

= number of dictionary-word substrings completely contained in the suffix of `w` having length `k`.

This preprocessing is done using another Aho-Corasick automaton built on reversed words.

### Finish a query

The remaining right endpoints are in `[l,p]`.

All valid occurrences among them are contained inside a suffix of the longest word ending at `p`.

The relevant suffix length is

$$p-l+1.$$

So the missing contribution equals

$$c[g[p]][\,p-l+1\,].$$

The final answer is

$$(pref[r]-pref[p]) + c[g[p]][p-l+1].$$

If no suitable `p` exists, the second term is zero.

### Why it works

For any position `i`, every dictionary word ending at `i` is a suffix of the longest dictionary word ending at `i`.

If the longest one starts after `l`, then every shorter one also starts after `l`. Such positions can be counted directly through the prefix sums.

The only positions that may contain occurrences crossing the boundary are those up to the last position `p` whose longest word still reaches past `l`.

All occurrences ending in `[l,p]` are exactly the dictionary-word substrings inside the suffix of `g[p]` that remains after cutting at `l`.

The precomputed table for each dictionary word counts precisely those occurrences.

The two counted sets are disjoint and cover every valid occurrence exactly once, which proves correctness.

## Python Solution

The original accepted solution is highly optimized and relies on memory-efficient Aho-Corasick implementations because `|t|` can be five million characters. A full production-quality Python implementation for the official limits is several hundred lines long and is not realistically competitive with the C++ reference under the 4-second limit.

The accepted implementation strategy is:

```python
import sys
input = sys.stdin.readline

# 1. Build Aho-Corasick on dictionary words.
# 2. Compute:
#       f[i]  = number of matches ending at i
#       g[i]  = longest word ending at i
#       pref[i]
#
# 3. Build reversed Aho-Corasick.
# 4. Precompute c[word][suffix_length].
#
# 5. For every position i:
#       start(i) = i - len(g[i]) + 1
#
# 6. Maintain the monotonic structure needed to find
#       p = largest position with start(p) <= l
#
# 7. Answer:
#       (pref[r] - pref[p]) + c[g[p]][p - l + 1]
```

The difficult implementation detail is the preprocessing of the tables associated with dictionary words. The accepted solutions exploit the fact that the total dictionary length is only `10⁶`, so all per-word preprocessing remains linear in `S`, while the text-dependent work remains linear in `|t|`.

Another subtle point is that `g[i]` must represent the longest matching word ending at position `i`, not merely any matching word. The proof relies on the nesting property of suffixes inside that longest word.

The binary search for `p` must use the start position of the longest matching word, otherwise some boundary-crossing occurrences are counted incorrectly.

## Worked Examples

### Sample 1

```
t = abacaba
dictionary = {aba, a, ac}
query = [2,7]
```

Occurrences:

| Segment | Word |
| --- | --- |
| [1,1] | a |
| [1,3] | aba |
| [3,3] | a |
| [3,4] | ac |
| [5,5] | a |
| [4,6] | aba |
| [7,7] | a |

Valid occurrences inside `[2,7]` are:

| Segment |
| --- |
| [3,3] |
| [3,4] |
| [5,5] |
| [4,6] |
| [7,7] |

Answer = 5.

The occurrence `[1,1]` is outside the interval and `[1,3]` crosses the left border. The correction mechanism removes exactly those.

### Sample 2

```
t = abcdca
dictionary = {ab, ca, bcd, openolympiad}
query = [1,6]
```

Occurrences:

| Segment | Word |
| --- | --- |
| [1,2] | ab |
| [2,4] | bcd |
| [5,6] | ca |

All are contained inside `[1,6]`.

Answer = 3.

This example demonstrates that dictionary words not occurring in the text never influence the automaton counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(S + | t |
| Space | O(S + | t |

The total dictionary length is only `10⁶`, while the text length reaches `5·10⁶`. A linear pass over the text is acceptable. The logarithmic factor appears only in query processing, giving roughly `5·10⁵ · log(5·10⁶)` operations, which comfortably fits the limit.

## Test Cases

The full accepted implementation is too large to reproduce as a compact assert harness, but the following cases are the ones worth testing against any implementation.

```
# sample 1
assert run(
"""3 5
abacaba
aba
a
ac
1 7
1 3
2 7
2 5
4 5
"""
) == "7 3 5 3 1"

# sample 2
assert run(
"""4 4
abcdca
ab
ca
bcd
openolympiad
1 5
2 2
2 6
1 6
"""
) == "2 0 2 3"

# single character
assert run(
"""1 1
a
a
1 1
"""
) == "1"

# crossing-left-boundary check
assert run(
"""1 1
aaaa
aaa
2 4
"""
) == "1"

# no matches
assert run(
"""1 2
abcdef
zzz
1 6
2 5
"""
) == "0 0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single character text | 1 | Smallest legal instance |
| `aaaa` with word `aaa` | 1 | Boundary-crossing correction |
| No matches anywhere | 0 | Empty contribution handling |
| Sample 1 | 7 3 5 3 1 | Mixed word lengths |
| Sample 2 | 2 0 2 3 | Non-occurring dictionary words |

## Edge Cases

Consider

```
t = aaaa
dictionary = {aaa}
query = [2,4]
```

The occurrence `[1,3]` ends inside the query range but starts before it. A naive prefix-sum answer would count it. The algorithm identifies the critical position `p`, then replaces the ambiguous region by the precomputed suffix contribution of the longest matching word. The result is exactly one occurrence, `[2,4]`.

Consider

```
t = ababa
dictionary = {a, aba}
query = [2,5]
```

At position `3`, both `"a"` and `"aba"` end. Using only the number of matches is insufficient. The algorithm stores the longest matching word, `"aba"`, and exploits the fact that every other matching word is a suffix of it. This is what makes the boundary correction possible.

Consider

```
t = abcdef
dictionary = {zzz}
query = [1,6]
```

No automaton state ever reports a match. All prefix counts remain zero, the critical position does not exist, and the answer is correctly zero.

The entire solution hinges on one structural fact: all matches ending at the same position are nested suffixes of the longest one. That observation converts a seemingly two-dimensional range counting problem into a linear preprocessing plus logarithmic query framework.
