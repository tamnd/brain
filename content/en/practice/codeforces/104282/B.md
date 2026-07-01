---
title: "CF 104282B - Emoji Master BSQ"
description: "We are given a fixed dictionary of word replacements. Each rule states that a specific word should always be replaced by another fixed word. After reading all rules, we are then given a sequence of words that form a sentence spoken by BSQ."
date: "2026-07-01T21:05:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104282
codeforces_index: "B"
codeforces_contest_name: "The 20th Hangzhou City University Programming Contest"
rating: 0
weight: 104282
solve_time_s: 55
verified: true
draft: false
---

[CF 104282B - Emoji Master BSQ](https://codeforces.com/problemset/problem/104282/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a fixed dictionary of word replacements. Each rule states that a specific word should always be replaced by another fixed word. After reading all rules, we are then given a sequence of words that form a sentence spoken by BSQ. Every word in that sentence is guaranteed to appear as a left-hand side in exactly one replacement rule, so each word maps to exactly one output word.

The task is to transform the sentence by replacing each word independently using the given rules and printing the resulting sequence.

The constraints are small, with both the number of rules and the number of words in the sentence up to 100, and each word length up to 10. This immediately tells us that any solution that is at least linear or quadratic in the input size will be fast enough. Even a direct scan over all rules for every word would only perform at most 10,000 string comparisons, which is trivial.

There are no hidden structural complexities like chaining transformations or multi-step rewriting; each word is replaced exactly once using the provided mapping.

A few edge cases are still worth being explicit about:

A naive implementation might incorrectly assume that replacement is iterative. For example, if one rule says "a → b" and another says "b → c", a mistaken solution might repeatedly apply rules and turn "a" into "c". However, the problem never asks for transitive closure. Only direct substitution is required.

Another potential pitfall is forgetting that words are space-separated tokens. If one tries to process the input as a raw string and replace substrings, accidental partial matches could corrupt results. For instance, replacing "wo" inside "wow" would be incorrect in a substring-based approach, though token-based processing avoids this entirely.

## Approaches

The straightforward way to solve the problem is to interpret the rules as a lookup process. For each word in the sentence, we scan through all rules until we find the one whose left-hand side matches the word, then output its corresponding right-hand side.

This brute-force method is correct because the rules form a simple association list. However, its cost is proportional to the number of sentence words multiplied by the number of rules. In the worst case, this results in 100 × 100 = 10,000 string comparisons, which is still acceptable here but becomes wasteful if constraints scale up.

The key observation is that we are repeatedly searching for the same key in a static dataset. This is exactly what a hash map is designed for. By precomputing a dictionary from each source word to its replacement, we reduce each query to O(1) average lookup time. This transforms the problem from repeated linear scans into a direct mapping problem.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan | O(nm) | O(n) | Accepted but unnecessary |
| Hash Map Lookup | O(n + m) | O(n) | Accepted |

## Algorithm Walkthrough

We first construct a mapping structure that stores every rule. Each key is a source word, and each value is its replacement word.

1. Read the integers n and m, which define how many mapping rules and how many words appear in the sentence.
2. Initialize an empty dictionary.
3. For each of the n rules, read the pair (si, ti) and store it in the dictionary as si → ti. This step ensures constant-time lookup later.
4. Read the m words of the sentence.
5. For each word in the sentence, retrieve its mapped value from the dictionary and append it to the output sequence.
6. Print all transformed words in order, separated by spaces.

The reason we can safely rely on direct lookup is that the problem guarantees every input word appears as a key in the mapping, so no missing-key handling is needed.

### Why it works

The algorithm constructs a function f defined on the set of input words, where each word has exactly one image. Since the problem guarantees total coverage and uniqueness of the left-hand side, f is a well-defined mapping. The output sentence is simply the pointwise application of f to each token in the input sequence. Because no rule depends on previous replacements, each transformation is independent and order-preserving.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    mp = {}

    for _ in range(n):
        s, t = input().split()
        mp[s] = t

    words = input().split()
    res = []

    for w in words:
        res.append(mp[w])

    print(" ".join(res))

if __name__ == "__main__":
    main()
```

The solution begins by building a dictionary `mp` that stores all replacement rules. Each input pair is inserted directly, overwriting is not a concern because the problem guarantees all `si` are distinct.

The sentence is then read as a list of tokens using `split()`, ensuring we treat words as atomic units rather than substrings. Each word is translated via a dictionary lookup and appended to the result list. Finally, the output is joined with spaces to reconstruct the transformed sentence.

A subtle but important detail is avoiding repeated string concatenation during output construction. Using a list and `" ".join()` ensures linear time behavior instead of quadratic growth from repeated string appends.

## Worked Examples

### Example 1

Input:

```
3 4
wo i
qiu ball
ni you
wo qiu qiu ni
```

| Step | Word | Lookup | Output so far |
| --- | --- | --- | --- |
| 1 | wo | i | i |
| 2 | qiu | ball | i ball |
| 3 | qiu | ball | i ball ball |
| 4 | ni | you | i ball ball you |

This shows that repeated words are handled independently, with each occurrence triggering the same dictionary lookup.

Output:

```
i ball ball you
```

### Example 2

Input:

```
2 5
a x
b y
a b a b a
```

| Step | Word | Lookup | Output so far |
| --- | --- | --- | --- |
| 1 | a | x | x |
| 2 | b | y | x y |
| 3 | a | x | x y x |
| 4 | b | y | x y x y |
| 5 | a | x | x y x y x |

This demonstrates correctness under alternating repeated patterns.

Output:

```
x y x y x
```

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each rule is inserted once and each word is translated once using O(1) average dictionary lookup |
| Space | O(n) | The dictionary stores one mapping per rule |

The constraints allow up to 100 rules and 100 words, so this solution is comfortably within limits even with naive overhead. The hash map approach is still the cleanest and most scalable interpretation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    mp = {}

    for _ in range(n):
        s, t = input().split()
        mp[s] = t

    words = input().split()
    res = [mp[w] for w in words]
    return " ".join(res)

# provided sample
assert run("""3 4
wo i
qiu ball
ni you
wo qiu qiu ni
""") == "i ball ball you"

# single mapping
assert run("""1 3
a b
a a a
""") == "b b b"

# alternating pattern
assert run("""2 4
x y
y x
x y x y
""") == "y x y x"

# minimum size
assert run("""1 1
a z
a
""") == "z"

# all same mapping
assert run("""2 3
a b
c d
c a c
""") == "d b d"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single rule repeated | b b b | repeated lookup consistency |
| alternating mapping | y x y x | independent token handling |
| minimum case | z | boundary correctness |
| mixed rules | d b d | multiple mappings correctness |

## Edge Cases

One subtle case is repeated occurrence of the same word in the sentence. For example:

```
2 3
a x
b y
a a b
```

The algorithm processes each token independently. First "a" becomes "x", second "a" becomes "x" again, and "b" becomes "y". Since dictionary lookup does not depend on position or history, repetition causes no issues.

Another case is ensuring that we never attempt partial replacements. Because we split the sentence using whitespace, each token is treated atomically. Even if words share prefixes, such as "ab" and "a", they are distinct keys in the dictionary and are not confused.

Finally, since every input word is guaranteed to exist in the mapping, there is no need for fallback handling. A direct dictionary access is always valid, and no KeyError cases need to be considered under the problem constraints.
