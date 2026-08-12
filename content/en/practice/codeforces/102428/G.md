---
title: "CF 102428G - Gluing Pictures"
description: "The city name is a string C. A picture can capture any contiguous section of C, so every substring of C is a possible picture. We may arrange the pictures in any order and concatenate their contents to obtain a friend's name."
date: "2026-08-12T07:15:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102428
codeforces_index: "G"
codeforces_contest_name: "2019-2020 ACM-ICPC Latin American Regional Programming Contest"
rating: 0
weight: 102428
solve_time_s: 118
verified: true
draft: false
---

[CF 102428G - Gluing Pictures](https://codeforces.com/problemset/problem/102428/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

The city name is a string `C`. A picture can capture any contiguous section of `C`, so every substring of `C` is a possible picture. We may arrange the pictures in any order and concatenate their contents to obtain a friend's name. The characters inside an individual picture cannot be changed, reversed, or rearranged.

For each friend's string `P`, we need the smallest number of substrings of `C` whose concatenation is exactly `P`. A picture may be taken for any section that appears in the city name, so the same section can be used again when necessary.

For example, with `C = MONTEVIDEO`, the string `DEMONIO` can be split as `DE | MON | I | O`. Every piece is a contiguous substring of `C`, and the pieces can appear in an order different from their positions in the city name. The answer is four.

The total length of all friend strings is at most `2 * 10^5`. The city string itself is the fixed text from which all possible pieces are taken. The official judge gives a 2 second time limit and 1024 MB of memory. A solution that examines every possible substring of every friend is quadratic in the friend length, which can mean about `2 * 10^10` candidate substrings for one friend of length `2 * 10^5`. That is far beyond what can be processed in the time limit. We need essentially linear work in the total input size.

There are several edge cases that can make a seemingly reasonable implementation wrong.

Consider

```
A
2
A
B
```

The answers are `1` and `-1`. A friend is impossible as soon as some required character cannot begin any substring of the city. An implementation that blindly increments the number of pieces after a failed match can accidentally count an impossible piece instead of reporting `-1`.

Consider

```
ABA
1
ABAB
```

The answer is `2`, using `ABA | B`. A greedy implementation must allow the next picture to start at any character of the friend, including a character that was also part of a picture used earlier. Restricting pictures to non-overlapping locations in the city would solve a different problem.

Consider

```
ABC
1
CBA
```

The answer is `3`, using `C | B | A`. The order of the pictures is unrestricted, but the characters inside a picture are not. Reversing `ABC` to obtain `CBA` is not allowed, so the whole friend cannot be made with one picture.

Finally,

```
AAA
1
AAAA
```

has answer `2`, using `AAA | A`. The same section of the city can be photographed again, so the fact that the first picture already used `AAA` does not remove it from the set of possible pictures.

## Approaches

The direct approach is dynamic programming. Let `dp[i]` be the minimum number of pictures needed to construct the first `i` characters of a friend. From position `i`, we could try every ending position `j`, check whether `P[i:j]` occurs somewhere inside `C`, and update `dp[j]`.

This is correct because every valid construction has some final picture, and the DP considers every possible choice for that final substring. The problem is the number of substrings we have to examine. A friend of length `m` has exactly `m(m+1)/2` non-empty substrings. For `m = 200000`, that is `20000100000`, about twenty billion candidates, before even considering the cost of checking whether each candidate occurs in the city.

We could preprocess all substrings of the city into a set, but that creates the same quadratic obstacle on the city side. A city of length `L` has `L(L+1)/2` substring occurrences to consider. Even with constant-time hash-set lookups afterward, the preprocessing is already too large when `L` is large.

The useful observation is that we do not actually need to consider every possible next piece. Suppose we are currently trying to construct the suffix `P[i:]`. Let `G` be the longest prefix of `P[i:]` that occurs as a substring of `C`.

Choosing `G` is always at least as good as choosing a shorter first picture. Take any optimal construction whose first picture has length `k`, where `k <= |G|`. Since `G` itself is a substring of `C`, it can replace the first several pictures of that construction. If `G` ends inside one of those pictures, the unused suffix of that picture is itself a substring of `C`, because every substring of a substring is also a substring of `C`. Thus the construction can be adjusted without using more pictures.

This gives a greedy rule: at every position in the friend, take the longest prefix that occurs in the city.

The remaining task is to find that longest prefix quickly. A suffix automaton is exactly a compact representation of all substrings of a string. Starting at its initial state and following transitions for the characters of the friend tells us how long the current prefix continues to occur in the city. When a transition is missing, the current prefix is the longest possible picture.

The brute-force method works because it explicitly explores all possible segmentations. It fails because there are quadratically many candidate pieces. The observation that a longest possible first piece can always replace shorter initial pieces reduces the problem to repeatedly finding one longest occurring prefix. A suffix automaton performs those substring checks directly in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DP with all substrings | O(L² + M²) with substring preprocessing | O(L²) | Too slow |
| Optimal greedy + suffix automaton | O(L + M) | O(L) | Accepted |

Here `L = |C|` and `M` is the sum of lengths of all friend strings.

## Algorithm Walkthrough

1. Build a suffix automaton for the city string `C`.

A suffix automaton has at most `2L - 1` states and recognizes exactly the set of substrings of `C`. From its initial state, following a sequence of character transitions is possible exactly when that sequence is a substring of `C`.
2. For each friend string `P`, start at position `pos = 0` and set the answer to zero.

At this point `P[pos:]` is the part that has not been constructed yet. We always want to choose one picture that covers as much of this suffix as possible.
3. Starting from the automaton's initial state, follow transitions using `P[pos]`, `P[pos + 1]`, and so on until either the friend ends or a required transition does not exist.

Suppose the traversal consumes `len` characters. Then `P[pos:pos+len]` is a substring of the city, while the next character cannot extend it to a longer substring. Thus this is exactly the longest possible first picture.
4. If `len` is zero, output `-1`.

No substring of the city starts with `P[pos]`, so there is no possible picture that can produce the next required character. Since every construction must produce that character next, the friend cannot be formed.
5. Otherwise, increase the answer by one and advance `pos` by `len`.

The consumed prefix is now represented by one picture. We restart the suffix-automaton traversal from its initial state because the next picture is an independent substring of the city.
6. Repeat until all characters of the friend have been consumed.

Every iteration consumes at least one friend character, so there can be at most `|P|` iterations.

### Why it works

Consider one greedy iteration beginning at position `pos`. Let `G` be the longest prefix of `P[pos:]` that is a substring of `C`. Any valid construction must begin with some substring `X` of `C`, and `X` cannot be longer than `G`.

If an optimal construction begins with `X`, then continue through its subsequent pictures until at least `|G|` characters have been covered. Replace that whole initial part with the single picture `G`. If `G` ends in the middle of a picture, the remaining suffix of that picture is still a substring of `C`, so it can become the next picture. The number of pictures does not increase.

Thus there always exists an optimal solution whose first picture is exactly the greedy choice `G`. After removing `G`, the same argument applies independently to the remaining suffix. By induction over the greedy iterations, the algorithm produces the minimum possible number of pictures.

The suffix automaton gives the exact `G` because every successful transition extends a substring of `C`, while the first missing transition proves that no longer prefix can occur in `C`.

## Python Solution

```python
import sys
input = sys.stdin.readline

class SuffixAutomaton:
    def __init__(self, s):
        self.next = [{}]
        self.link = [-1]
        self.length = [0]
        self.last = 0

        for ch in s:
            self.extend(ch)

    def extend(self, ch):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)

        p = self.last

        while p != -1 and ch not in self.next[p]:
            self.next[p][ch] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][ch]

            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])

                while p != -1 and self.next[p].get(ch) == q:
                    self.next[p][ch] = clone
                    p = self.link[p]

                self.link[q] = clone
                self.link[cur] = clone

        self.last = cur

    def longest_prefix(self, s, start):
        state = 0
        pos = start

        while pos < len(s):
            nxt = self.next[state].get(s[pos])
            if nxt is None:
                break
            state = nxt
            pos += 1

        return pos - start

def solve():
    city = input().strip()
    n = int(input())

    sam = SuffixAutomaton(city)

    out = []

    for _ in range(n):
        friend = input().strip()
        pos = 0
        pieces = 0

        while pos < len(friend):
            length = sam.longest_prefix(friend, pos)

            if length == 0:
                pieces = -1
                break

            pos += length
            pieces += 1

        out.append(str(pieces))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The suffix automaton stores three pieces of information for every state. `length[v]` is the maximum length represented by that state, `link[v]` is its suffix link, and `next[v]` contains outgoing character transitions. The construction follows the standard suffix automaton extension procedure, including cloning a state when the new transition would otherwise violate the automaton's structure.

The `longest_prefix` function always starts from state zero. This is necessary because every picture is an arbitrary substring of the city, not necessarily a prefix of the city. Starting from the initial state means that every possible substring is available.

The loop stops at the first missing transition. If the loop consumed several characters, that entire prefix is known to occur in the city. The missing transition proves that extending it by one more character is impossible, so the matched length is maximal.

The most subtle boundary case is when the very first transition is missing. Then `length == 0`, and advancing `pos` would make the algorithm loop forever or incorrectly count a picture. The code immediately returns `-1` for that friend.

When a match succeeds, `pos` advances by the entire matched length before the next iteration. We do not advance one character at a time because the whole matched prefix has already been covered by one picture.

There is no integer-overflow concern in Python. The answer is at most the friend's length, so even a 32-bit integer would be sufficient for the answer itself.

The implementation uses dictionaries for transitions. The alphabet contains only uppercase English letters, so each state has at most 26 outgoing transitions. A fixed 26-element array could reduce dictionary overhead in a lower-level language, but dictionaries keep the Python implementation substantially simpler while retaining linear asymptotic complexity.

## Worked Examples

For the first sample, the city is `MONTEVIDEO`. The official sample has four friends and the answers are `4`, `1`, `4`, and `-1`.

For `DEMONIO`, the greedy process is:

| Position | Remaining suffix | Longest city substring | Pieces |
| --- | --- | --- | --- |
| 0 | `DEMONIO` | `DE` | 1 |
| 2 | `MONIO` | `MON` | 2 |
| 5 | `IO` | `I` | 3 |
| 6 | `O` | `O` | 4 |

The first match is `DE`, even though `D` appears later in the city. The next match is `MON`, which comes earlier in the city. This confirms that pictures may be rearranged freely. The automaton only cares whether each piece occurs somewhere in the city.

For `EDIT`, the first greedy match is `E`. From the remaining `DIT`, the longest possible match is `D`, then `I`, then `T`. The resulting trace is:

| Position | Remaining suffix | Longest city substring | Pieces |
| --- | --- | --- | --- |
| 0 | `EDIT` | `E` | 1 |
| 1 | `DIT` | `D` | 2 |
| 2 | `IT` | `I` | 3 |
| 3 | `T` | `T` | 4 |

So the answer is `4`. This also demonstrates why the greedy algorithm does not need to know where a substring occurs in the city. It only needs to know that it occurs.

For the second sample, the city is `SANTIAGO`, and the official answers are `3`, `1`, and `3`.

For `TITA`, the greedy matches are:

| Position | Remaining suffix | Longest city substring | Pieces |
| --- | --- | --- | --- |
| 0 | `TITA` | `T` | 1 |
| 1 | `ITA` | `I` | 2 |
| 2 | `TA` | `TA` | 3 |

The result is `3`. The final `TA` is contiguous inside `SANTIAGO`, even though the two letters are separated from some other letters that were used earlier in the friend. Pictures are independent, so that causes no restriction.

For `SANTIAGO` itself, the whole friend is the city string, so the automaton follows every character successfully:

| Position | Remaining suffix | Longest city substring | Pieces |
| --- | --- | --- | --- |
| 0 | `SANTIAGO` | `SANTIAGO` | 1 |

The answer is `1`, demonstrating that the automaton can recognize the entire city string as one picture.

## Complexity Analysis

Let `L = |C|` and let `M` be the sum of the lengths of all friend strings.

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L + M) | The suffix automaton takes O(L) to build, and every friend character is consumed by exactly one successful greedy match, with at most one failed transition per piece |
| Space | O(L) | A suffix automaton has fewer than `2L` states, and the total number of stored transitions is O(L) |

The total friend length is at most `2 * 10^5`, so the query processing is linear in the bounded part of the input. The automaton construction is also linear in the city length. This is comfortably within the official 2 second and 1024 MB limits.

## Test Cases

The following test harness contains the same suffix-automaton solution logic and checks the two official samples together with custom cases.

```python
import sys
import io

input = sys.stdin.readline

class SuffixAutomaton:
    def __init__(self, s):
        self.next = [{}]
        self.link = [-1]
        self.length = [0]
        self.last = 0

        for ch in s:
            self.extend(ch)

    def extend(self, ch):
        cur = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)

        p = self.last

        while p != -1 and ch not in self.next[p]:
            self.next[p][ch] = cur
            p = self.link[p]

        if p == -1:
            self.link[cur] = 0
        else:
            q = self.next[p][ch]

            if self.length[p] + 1 == self.length[q]:
                self.link[cur] = q
            else:
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])

                while p != -1 and self.next[p].get(ch) == q:
                    self.next[p][ch] = clone
                    p = self.link[p]

                self.link[q] = clone
                self.link[cur] = clone

        self.last = cur

    def longest_prefix(self, s, start):
        state = 0
        pos = start

        while pos < len(s):
            nxt = self.next[state].get(s[pos])
            if nxt is None:
                break
            state = nxt
            pos += 1

        return pos - start

def solve():
    city = input().strip()
    n = int(input())

    sam = SuffixAutomaton(city)
    out = []

    for _ in range(n):
        friend = input().strip()
        pos = 0
        pieces = 0

        while pos < len(friend):
            length = sam.longest_prefix(friend, pos)

            if length == 0:
                pieces = -1
                break

            pos += length
            pieces += 1

        out.append(str(pieces))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        input = sys.stdin.readline

        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

# Provided sample 1
assert run(
    """MONTEVIDEO
4
DEMONIO
MONTE
EDIT
WON
"""
) == "4\n1\n4\n-1", "sample 1"

# Provided sample 2
assert run(
    """SANTIAGO
3
TITA
SANTIAGO
NAS
"""
) == "3\n1\n3", "sample 2"

# Minimum-size city, impossible character, and exact match
assert run(
    """A
3
A
AA
B
"""
) == "1\n2\n-1", "minimum size and impossible character"

# Repeated characters and repeated use of the same picture
assert run(
    """AAA
3
AAAA
AAAAAA
B
"""
) == "2\n2\n-1", "repeated characters"

# Reordering pictures and greedy longest-prefix behavior
assert run(
    """ABC
4
CBA
ABAB
BCAB
ACAC
"""
) == "3\n2\n2\n4", "reordering and boundaries"

# Maximum-size linear test
city = "A" * 200000
large_input = city + "\n2\n" + ("A" * 200000) + "\n" + ("B" * 1) + "\n"
assert run(large_input) == "1\n-1", "maximum-size test"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `A`, friends `A`, `AA`, `B` | `1`, `2`, `-1` | Minimum size, repeated use, impossible character |
| `AAA`, friends `AAAA`, `AAAAAA`, `B` | `2`, `2`, `-1` | All-equal characters and reuse of the same city section |
| `ABC`, friends `CBA`, `ABAB`, `BCAB`, `ACAC` | `3`, `2`, `2`, `4` | Arbitrary picture order and greedy longest-prefix choices |
| `A * 200000`, friends `A * 200000`, `B` | `1`, `-1` | Maximum-size input and linear processing |

## Edge Cases

For an impossible first character, consider

```
ABC
1
D
```

The automaton starts at the initial state and immediately looks for transition `D`. There is none, so the longest prefix has length zero. The algorithm outputs `-1`. It does not count `D` as a one-character picture because `D` does not occur in the city.

For a friend that is longer than the city but consists entirely of repeatable pieces, consider

```
AAA
1
AAAA
```

The first traversal consumes `AAA`, because that is the longest prefix occurring in the city. The remaining suffix is `A`, which is itself a substring of the city. The answer is `2`. The automaton is rebuilt only once, and the same automaton can be used repeatedly because pictures are not resources that disappear after being selected.

For arbitrary picture ordering, consider

```
ABC
1
CBA
```

The first traversal finds `C`, then the next starts from the automaton's initial state and finds `B`, then the final traversal finds `A`. The answer is `3`. The algorithm never attempts to preserve the positions of the selected pictures inside the city, which is exactly what the problem allows.

For the greedy boundary case, consider

```
ABA
1
ABAB
```

The first traversal takes `ABA`, since it is a substring of the city and no longer prefix is possible. The remaining friend is `B`, which takes one more picture. The answer is `2`. A shorter first choice such as `AB` would also lead to a valid construction, but it cannot improve the answer, which is precisely the property behind the greedy proof.

For a friend equal to the city itself,

```
SANTIAGO
1
SANTIAGO
```

the automaton follows every character without encountering a missing transition. The longest prefix has length eight, so the entire friend is consumed in one iteration and the answer is `1`. This checks the boundary where a match reaches the end of the query rather than ending because a transition is missing.
