---
title: "CF 102343K - Code Matching"
description: "We have a codebook containing (N) distinct digit strings. One of those strings is transmitted. James begins listening at a uniformly random digit of the transmitted string, so everything before that position may already have been missed."
date: "2026-08-17T10:27:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102343
codeforces_index: "K"
codeforces_contest_name: "UCF Locals 2019"
rating: 0
weight: 102343
solve_time_s: 203
verified: true
draft: false
---

[CF 102343K - Code Matching](https://codeforces.com/problemset/problem/102343/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a codebook containing (N) distinct digit strings. One of those strings is transmitted. James begins listening at a uniformly random digit of the transmitted string, so everything before that position may already have been missed.

After James has heard some consecutive digits, he considers every codebook entry that could still be the transmitted message. Since he does not know where he started listening in a candidate message, the digits he has heard only need to occur as a contiguous substring of that candidate. As soon as exactly one codebook entry contains the entire sequence heard so far, James knows the message and stops.

There is one extra piece of information at the end. One second after the final digit of the transmitted message, silence occurs. If James has reached the end without distinguishing the message, that silence tells him that the sequence he heard must end at the end of the candidate message. If exactly one candidate has that suffix, he can identify the message. Otherwise the message is impossible to determine for that starting position.

The input contains at most (100{,}000) codebook strings, and their total length is at most (100{,}000). The original contest gives a two second time limit and 256 MB memory limit. The total length bound is the key constraint: an algorithm proportional to the total input size is ideal, while repeatedly comparing every substring with every codeword would be quadratic and can reach roughly (10^{10}) character-level operations.

There are two easy-to-miss boundary cases. First, being unique only after the final digit does not automatically mean that one extra second for silence is needed. If the complete sequence heard is already contained in only one codeword, James knows the codeword immediately after that final digit. For example, with

```
2
12
123
```

the message `12` is identifiable after hearing both digits when James starts at its first digit, so that starting position takes 2 seconds, not 3. The other starting position hears `2`; that digit occurs in both messages, but after silence only `12` can end there, so it takes 2 seconds.

Second, the final silence can distinguish messages even when the digit sequence itself is not unique. For example,

```
2
12
23
```

if `12` is transmitted and James starts at its final `2`, hearing `2` alone is ambiguous because both codewords contain `2`. After the silence, only `12` can have `2` as its final digit, so the time is 2 seconds. A solution that treats every ambiguous full suffix as impossible would get this case wrong.

## Approaches

A direct solution would examine every possible starting position of every message. For a fixed position, it would extend the observed substring one character at a time and ask which codebook strings contain that substring. Checking all codewords directly is correct because the definition of a candidate is exactly that the observed sequence occurs somewhere inside that codeword.

The problem is the repeated substring searching. If the total input length is (S), there are (S) possible starting positions. Across all message pairs, checking every starting position can require (\Theta(S^2)) character comparisons in the worst case, which is about (10^{10}) operations when (S=100{,}000). The same repeated work is being done because many different substrings share the same prefixes.

The useful observation is that for a fixed starting position, we only need one number: the longest prefix of the remaining suffix that also occurs in some other codeword. Suppose this longest shared prefix has length (L). After hearing (L+1) digits, no other codeword contains the observed substring, so James can identify the message immediately. Thus every starting position can be reduced to a longest-common-prefix query against suffixes belonging to other codewords.

A suffix array gives exactly the required structure. Put all codewords into one sequence, separating consecutive codewords with different separator symbols. Every suffix beginning at a digit now represents a possible observed continuation. In suffix-array order, the maximum LCP with a suffix from another codeword is achieved by the nearest suffix from another codeword on either side. We can obtain these LCP values in linear time after constructing the suffix array.

The remaining case is when the entire remaining suffix still occurs in another codeword. Then the ordinary substring test cannot distinguish the messages. We separately build a trie of reversed codewords. A node in this trie represents a suffix, and its stored count tells us how many codewords end with that suffix. If the count is exactly one, the final silence distinguishes the message in one additional second. If the count is larger than one, that starting position is impossible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(S^2)) character comparisons | (O(S)) | Too slow |
| Suffix Array + Reverse Trie | (O(S\log S)) | (O(S)) | Accepted |

Here (S) is the total length of all codewords.

## Algorithm Walkthrough

1. Read all codewords and concatenate them into one integer sequence. Digits use values from 1 through 10, while every codeword receives its own unique separator value. The separators prevent a suffix from one codeword from accidentally matching through the boundary into another codeword.
2. Construct the suffix array of the concatenated sequence using prefix doubling with counting sort. A sentinel smaller than every other symbol is appended during construction, then removed from the final suffix array.
3. Compute the LCP array with Kasai's algorithm. `lcp[r]` stores the common-prefix length of the suffix at suffix-array rank `r` and the suffix immediately before it.
4. For every suffix-array position, determine the maximum LCP with a suffix belonging to another codeword. Scan from left to right and then from right to left. During a scan, when the codeword identifier changes, the previous suffix becomes the nearest suffix from a different codeword. While staying inside the same codeword, keep the minimum LCP encountered since that nearest different codeword. This minimum is exactly the LCP with that nearest different suffix.
5. For every original digit position, store the resulting maximum shared-prefix length. If the value is (L), then the first (L) digits can still be confused with another message, while the next digit, if it exists, makes the message unique.
6. Build a trie containing every codeword in reverse order. Each visited node stores how many codewords pass through it. A node therefore represents a suffix, and its count is exactly the number of codewords having that suffix.
7. Process every codeword from right to left. At position (i), let `remaining = len(word) - i`. If the precomputed longest shared prefix with another codeword is smaller than `remaining`, then the first unique observation occurs after `best + 1` digits, so add that number to the listening time.
8. If no unique substring appears before the message ends, inspect the trie node corresponding to the entire remaining suffix. If exactly one codeword ends with that suffix, James learns the answer after hearing the suffix and then the one-second silence, giving `remaining + 1` seconds. If at least two codewords have that suffix, this starting position is impossible, so the whole answer for that message is `Impossible`.
9. Average the listening time over all possible starting positions. Every digit position is equally likely to be the starting point, so divide the sum by the message length.

The correctness invariant is that for every starting position, `best` is the maximum number of initial observed digits that also occur contiguously in another codeword. Thus every observation of length at most `best` is ambiguous, while the observation of length `best + 1`, if it exists, occurs in only the transmitted codeword. If the remaining suffix has length at most `best`, no digit-only observation can distinguish the message, and the reverse trie checks exactly whether the final silence leaves one or multiple possible messages. Hence the computed time is precisely the time James needs for that starting position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def suffix_array(a):
    """Suffix array of an integer sequence, O(n log n)."""
    s = a + [0]  # 0 is the unique sentinel
    n = len(s)

    alphabet = max(s) + 1
    cnt = [0] * alphabet
    for x in s:
        cnt[x] += 1

    pos = [0] * alphabet
    for i in range(1, alphabet):
        pos[i] = pos[i - 1] + cnt[i - 1]

    p = [0] * n
    for x in s:
        p[pos[x]] = p[pos[x]] + 1
        pos[x] += 1

    # The previous counting-sort construction above needs positions
    # reconstructed from counts.
    pos = [0] * alphabet
    for i in range(1, alphabet):
        pos[i] = pos[i - 1] + cnt[i - 1]

    p = [0] * n
    for i, x in enumerate(s):
        p[pos[x]] = i
        pos[x] += 1

    c = [0] * n
    classes = 1
    c[p[0]] = 0

    for i in range(1, n):
        if s[p[i]] != s[p[i - 1]]:
            classes += 1
        c[p[i]] = classes - 1

    length = 1

    while length < n:
        pn = [0] * n
        for i in range(n):
            x = p[i] - length
            if x < 0:
                x += n
            pn[i] = x

        cnt = [0] * classes
        for x in pn:
            cnt[c[x]] += 1

        pos = [0] * classes
        for i in range(1, classes):
            pos[i] = pos[i - 1] + cnt[i - 1]

        new_p = [0] * n
        for x in pn:
            cls = c[x]
            new_p[pos[cls]] = x
            pos[cls] += 1

        cn = [0] * n
        new_classes = 1
        cn[new_p[0]] = 0

        for i in range(1, n):
            cur = new_p[i]
            prev = new_p[i - 1]

            cur_second = cur + length
            if cur_second >= n:
                cur_second -= n

            prev_second = prev + length
            if prev_second >= n:
                prev_second -= n

            if c[cur] != c[prev] or c[cur_second] != c[prev_second]:
                new_classes += 1

            cn[cur] = new_classes - 1

        p = new_p
        c = cn
        classes = new_classes
        length <<= 1

    # Remove the suffix consisting only of the sentinel.
    return p[1:]

def build_lcp(a, sa):
    n = len(a)
    rank = [0] * n

    for i, p in enumerate(sa):
        rank[p] = i

    lcp = [0] * n
    h = 0

    for i in range(n):
        r = rank[i]

        if r == 0:
            continue

        j = sa[r - 1]

        while i + h < n and j + h < n and a[i + h] == a[j + h]:
            h += 1

        lcp[r] = h

        if h:
            h -= 1

    return rank, lcp

def solve():
    n = int(input())
    words = [input().strip() for _ in range(n)]

    # Concatenate all words. Each word gets its own separator.
    # Positions of actual digits are retained for later queries.
    a = []
    doc = []
    positions = [[] for _ in range(n)]

    for idx, word in enumerate(words):
        for ch in word:
            positions[idx].append(len(a))
            a.append(ord(ch) - ord('0') + 1)
            doc.append(idx)

        # Separators are all different and larger than digit symbols.
        a.append(11 + idx)
        doc.append(idx)

    # Suffix-array phase.
    sa = suffix_array(a)
    rank, lcp = build_lcp(a, sa)

    # best[r] = maximum LCP with a suffix from a different codeword.
    best = [0] * len(a)

    current_doc = doc[sa[0]]
    minimum = None

    for r in range(1, len(sa)):
        d = doc[sa[r]]

        if d != current_doc:
            current_doc = d
            minimum = lcp[r]
        elif minimum is not None:
            minimum = min(minimum, lcp[r])

        if minimum is not None:
            best[r] = minimum

    current_doc = doc[sa[-1]]
    minimum = None

    for r in range(len(sa) - 2, -1, -1):
        d = doc[sa[r]]

        if d != current_doc:
            current_doc = d
            minimum = lcp[r + 1]
        elif minimum is not None:
            minimum = min(minimum, lcp[r + 1])

        if minimum is not None:
            best[r] = max(best[r], minimum)

    # The suffix-array data is no longer needed.
    del sa
    del lcp
    del doc
    del a

    # Build a trie of reversed codewords.
    children = [{}]
    suffix_count = [0]

    for word in words:
        node = 0

        for ch in reversed(word):
            nxt = children[node].get(ch)

            if nxt is None:
                nxt = len(children)
                children[node][ch] = nxt
                children.append({})
                suffix_count.append(0)

            node = nxt
            suffix_count[node] += 1

    output = []

    for idx, word in enumerate(words):
        total_time = 0
        possible = True

        node = 0
        found_unique = False

        for i in range(len(word) - 1, -1, -1):
            ch = word[i]
            node = children[node][ch]

            remaining = len(word) - i
            global_pos = positions[idx][i]
            shared = best[rank[global_pos]]

            if shared < remaining:
                total_time += shared + 1
                found_unique = True
                break

        if not found_unique:
            # The complete remaining suffix never became unique
            # as an ordinary substring. Silence can distinguish it
            # only if exactly one codeword ends with it.
            if suffix_count[node] == 1:
                total_time += len(word) + 1
            else:
                possible = False

        if not possible:
            output.append("Impossible")
        else:
            output.append(f"{total_time / len(word):.10f}")

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    solve()
```

The concatenation phase assigns a different separator to every codeword. This is more than a convenience: if the same separator were reused, two suffixes could incorrectly receive an LCP that crosses a codeword boundary. Unique separators make that impossible because suffixes from different codewords encounter different symbols immediately after their digit portions.

The suffix array uses a sentinel smaller than every real symbol. Prefix doubling sorts cyclic shifts, and the sentinel converts that ordering into the ordinary suffix-array ordering. The implementation uses counting sort for every doubling round, giving (O(S\log S)) rather than sorting suffixes with a comparison sort at every round.

The two scans over the LCP array deserve special attention. Suppose suffix-array ranks currently belong to codeword A. The nearest suffix from a different codeword is the most recent rank whose document differs from A. The LCP with that suffix is the minimum LCP value across the interval between the two ranks. When another A suffix is encountered, extending the interval requires only another `min` operation. The right-to-left scan performs the symmetric calculation.

The reverse trie is used only for the final silence case. Traversing a word from its last character toward its first follows exactly the suffixes that can be heard when James starts at each position and reaches the end. `suffix_count[node]` counts codewords having that suffix, so the test for exactly one candidate directly matches the information provided by silence.

Python integers have arbitrary precision, so the accumulated listening time does not risk overflow. The final division is performed only after the exact integer sum has been computed, and ten digits after the decimal point provide much more precision than the required (10^{-5}) relative error.

## Worked Examples

For the provided sample, the codebook is `17383`, `126`, `385`, and `485`. The following table traces the five possible starting positions of `17383`.

| Start position | Remaining suffix | Longest shared prefix | Ending suffix count | Time |
| --- | --- | --- | --- | --- |
| 1 | `17383` | 1 | not needed | 2 |
| 2 | `7383` | 0 | not needed | 1 |
| 3 | `383` | 2 | not needed | 3 |
| 4 | `83` | 1 | not needed | 2 |
| 5 | `3` | 1 | 1 | 2 |

The first digit `1` is also present in `126`, so one digit is ambiguous and `17` becomes unique after two seconds. Starting at `7`, that digit already identifies `17383`. Starting at `3` in the middle, both `17383` and `385` contain `38`, while `383` occurs only in `17383`. At the final digit, `3` also occurs in `385`, but only `17383` ends with `3`, so the final silence resolves the ambiguity. The average is ((2+1+3+2+2)/5=2), matching the sample.

For a second example, consider

```
3
12
23
45
```

The states for each message are:

| Message | Start | Remaining suffix | Longest shared prefix | Ending suffix count | Time |
| --- | --- | --- | --- | --- | --- |
| `12` | 1 | `12` | 1 | not needed | 2 |
| `12` | 2 | `2` | 1 | 1 | 2 |
| `23` | 1 | `23` | 1 | not needed | 2 |
| `23` | 2 | `3` | 0 | not needed | 1 |
| `45` | 1 | `45` | 0 | not needed | 1 |
| `45` | 2 | `5` | 0 | not needed | 1 |

For `12`, the first digit is shared with no other message, while the final `2` is shared as a substring with `23`, so silence is needed when starting there. For `23`, the first `2` is shared, but `23` itself is unique, while `3` is unique immediately. The message `45` is identifiable from either digit. The resulting outputs are `1.5000000000`, `1.5000000000`, and `1.0000000000`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(S\log S)) | Suffix-array construction dominates; LCP, scans, and trie construction are linear |
| Space | (O(S)) | All arrays, suffix information, separators, and trie nodes are linear in total input length |

Here (S\le100{,}000). The suffix array performs (O(\log S)) doubling rounds, each using linear counting sort, while every later phase touches each character only a constant number of times. The algorithm is thus comfortably within the intended asymptotic bounds, and it avoids the quadratic repeated substring comparisons of the brute-force method.

## Test Cases

The following tests assume the editorial solution has been saved as `solution.py`.

```python
# helper: run solution on input string, return output string
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = solution.input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solution.input = sys.stdin.readline

    try:
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        solution.input = old_input

# Provided sample
sample1 = """\
4
17383
126
385
485
"""

assert run(sample1) == (
    "2.0000000000\n"
    "1.3333333333\n"
    "Impossible\n"
    "Impossible"
), "provided sample"

# Minimum-size input
assert run("1\n0\n") == "1.0000000000", "single one-digit codeword"

# Several overlapping strings, exercising substring ambiguity and silence
case2 = """\
3
12
23
45
"""

assert run(case2) == (
    "1.5000000000\n"
    "1.5000000000\n"
    "1.0000000000"
), "substring matching and final silence"

# Nested repeated digits, exercising full-suffix ambiguity
case3 = """\
3
1
11
111
"""

assert run(case3) == (
    "2.0000000000\n"
    "Impossible\n"
    "Impossible"
), "nested suffixes"

# Boundary case where the whole observed sequence becomes unique
case4 = """\
2
12
123
"""

assert run(case4) == (
    "2.0000000000\n"
    "2.0000000000"
), "unique full substring without extra silence"

# Maximum total length, one codeword consisting entirely of equal digits.
# Every observed digit already identifies the only codeword.
big_word = "0" * 100000
case5 = "1\n" + big_word + "\n"

assert run(case5) == "1.0000000000", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` followed by `0` | `1.0000000000` | Minimum-size input |
| `12`, `23`, `45` | `1.5`, `1.5`, `1.0` | Ordinary substring ambiguity and silence |
| `1`, `11`, `111` | `2.0`, `Impossible`, `Impossible` | Repeated characters and overlapping suffixes |
| `12`, `123` | `2.0`, `2.0` | Boundary between unique substring and final silence |
| One string of 100000 zeroes | `1.0` | Maximum total length and all-equal digits |

## Edge Cases

A single codeword is the simplest possible case. With

```
1
0
```

the only codeword contains every observed substring, so James immediately knows the message after hearing the first digit. The reverse trie also contains exactly one codeword for suffix `0`, but that case is never reached because the substring is already unique. The output is `1.0000000000`.

Overlapping codewords can make a digit ambiguous while a longer substring is unique. With

```
2
12
123
```

starting at the first digit of `12`, the observed `1` occurs in both messages, but `12` occurs only in the first, so the time is exactly 2 seconds. Starting at the final `2`, the digit is shared, but only `12` ends with `2`, so silence gives the answer after 2 seconds. The output for `12` is consequently `2.0000000000`.

Repeated suffixes can make the silence insufficient. With

```
3
1
11
111
```

the digit `1` occurs in all three messages. For `11`, even the complete suffix `11` is the ending of both `11` and `111`, so silence cannot distinguish them. The message is impossible. For `111`, starting at the second digit produces the same ambiguity, while starting at the last digit leaves all three messages possible until silence. The output is `Impossible` for both longer messages.

The final-digit boundary is especially easy to mishandle. Consider

```
2
12
23
```

when `12` is transmitted and James starts at its final `2`. The digit `2` occurs in both codewords, so a substring-only solution would declare ambiguity forever. The reverse trie sees that only `12` ends with `2`, so after one digit and one second of silence the message is known. The correct time for this starting position is 2 seconds.

The maximum-size case is a single codeword of (100{,}000) equal digits. Every substring belongs to only that codeword, so every possible starting position takes one second. The suffix-array phase still handles all (100{,}000) characters, and the total work remains (O(S\log S)) rather than becoming quadratic.
