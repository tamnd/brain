---
title: "CF 102386I - \u041f\u0435\u0440\u0441\u0435\u0430\u043d\u0442\u043e\u0432\u043a\u0430"
description: "We are given a sentence whose words may have had their internal letters rearranged. For every word, the first and last letters were kept fixed, while any permutation of the letters between them was allowed."
date: "2026-08-15T08:10:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102386
codeforces_index: "I"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0442\u0443\u0440 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0447\u0435\u0442\u0432\u0435\u0440\u0442\u044c\u0444\u0438\u043d\u0430\u043b\u0430 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u043c\u0438\u0440\u0430 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e 2019"
rating: 0
weight: 102386
solve_time_s: 1746
verified: false
draft: false
---

[CF 102386I - \u041f\u0435\u0440\u0441\u0435\u0430\u043d\u0442\u043e\u0432\u043a\u0430](https://codeforces.com/problemset/problem/102386/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 29m 6s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sentence whose words may have had their internal letters rearranged. For every word, the first and last letters were kept fixed, while any permutation of the letters between them was allowed. Alongside the corrupted sentence, we receive a dictionary containing every word that could have appeared in the original sentence.

For each word in the corrupted sentence, we need to find any dictionary word that could turn into it by permuting only its internal letters. A dictionary word is compatible exactly when it has the same first letter, the same last letter, and the same number of occurrences of every letter. If at least one compatible dictionary word exists for every sentence word, we can output any such reconstruction. If even one sentence word has no compatible dictionary word, the answer is `No solution`.

The total number of characters in the sentence is at most (5\cdot10^5), and the total number of characters in the dictionary is also at most (5\cdot10^5). The number of dictionary entries can reach (5\cdot10^5). These bounds rule out doing a full scan of the dictionary for every word in the sentence. A sentence can contain hundreds of thousands of words, so an (O(Wn)) search, where (W) is the number of sentence words, can reach roughly (1.25\cdot10^{11}) candidate checks under the individual bounds (W\le250000) and (n\le500000). We need processing proportional to the total amount of input instead.

There are several boundary cases that a careless implementation can mishandle. A one-letter word has no internal letters, so it can only match a dictionary word with exactly the same single character. For example, with input

```
a.
1
a
```

the answer is `a.`. Treating the first and last characters as two separate positions without handling the one-character case can accidentally index an empty middle incorrectly.

Different dictionary words can have exactly the same signature. For example,

```
tihs.
2
this
hits
```

has only `this` as a valid answer, because `hits` has different first and last letters. On the other hand,

```
scret.
2
secret
serect
```

would allow either compatible word if the observed word had the same length and letter counts. The problem explicitly permits any valid answer, so storing only one word for each signature is sufficient.

A word can also have the correct length but still be impossible to reconstruct because one internal letter has the wrong multiplicity. For example,

```
wlrd.
1
world
```

has no solution. The observed word contains only four letters, while the dictionary word contains five, so comparing only the first and last letters would incorrectly accept it.

Finally, the period belongs to the sentence syntax rather than to any word. For

```
hello wolrd.
2
hello
world
```

the second word is `wolrd`, not `wolrd.`. A parser that includes the period in the word signature will fail to find `world`.

## Approaches

The direct approach is to take every word from the corrupted sentence and compare it with every dictionary word. For a candidate pair, we can check the first and last characters and then compare the character frequencies in the two words. The method is correct because these conditions are exactly the definition of being obtainable by permuting internal letters.

The problem is the repeated dictionary scan. If the sentence has (W) words and the dictionary has (n) entries, there can be (Wn) candidate checks. From the input bounds, (W) can be about (250000) and (n) can be (500000), giving an upper bound of (125000000000) candidate inspections. Even a constant-time rejection for most candidates is far beyond what is reasonable.

The key observation is that the order of the internal letters does not matter at all. Every word can be represented by a canonical signature consisting of its first letter, its last letter, and the frequency of each of the 26 lowercase letters. Two words are compatible if and only if their signatures are equal.

We can compute this signature once for every dictionary word and put it into a hash table. Then each sentence word is converted to the same signature and looked up directly. The expensive repeated search disappears, leaving only one pass over the dictionary and one pass over the sentence.

The brute-force method works because it tests exactly the right condition, but it repeatedly rediscovers the same information. The observation that compatibility is completely determined by a small canonical signature lets us replace repeated comparisons with hash-table lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Wn)) candidate checks, with additional word comparison cost | (O(n)) | Too slow |
| Optimal | (O(S+D+26n+26W)), effectively (O(S+D)) | (O(D+26n)) | Accepted |

Here (S) is the total length of the sentence words and (D) is the total length of the dictionary words. Since both are at most (5\cdot10^5), the linear terms dominate.

## Algorithm Walkthrough

1. Read the corrupted sentence and remove its final period. Splitting the remaining string by spaces gives exactly the sequence of corrupted words, because the input guarantees a single space between neighboring words.
2. For every dictionary word, build a signature containing its first character, its last character, and a 26-element frequency vector. The frequency vector counts all letters in the word, including the endpoints. Including the endpoints in the count is safe because those characters are fixed as well.
3. Store one dictionary word for every signature in a hash table. Several different dictionary words may share one signature, but that causes no problem because the statement accepts any valid reconstruction.
4. For every corrupted sentence word, compute its signature and look it up in the table. If the signature is absent, no dictionary word can produce this observed word, so the entire sentence has no valid reconstruction.
5. If the signature is present, append the stored dictionary word to the reconstructed sentence. Repeat this independently for every word.
6. Join the reconstructed words with single spaces and append the final period. The resulting string has exactly the same word boundaries and punctuation as the input sentence.

### Why it works

The invariant is that every stored signature represents exactly the set of dictionary words whose letters can be rearranged into the corresponding observed word without changing its first or last letter. If an observed word has the same signature as a dictionary word, the two words contain exactly the same multiset of letters and have identical endpoints, so the internal letters can be permuted to transform one into the other. If their signatures differ, at least one endpoint or letter frequency differs, making such a permutation impossible. Consequently, every selected dictionary word is valid, and failure to find a signature proves that no valid reconstruction exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def signature(word):
    cnt = [0] * 26
    for ch in word:
        cnt[ord(ch) - 97] += 1
    return (word[0], word[-1], tuple(cnt))

def solve():
    text = input().rstrip('\n')
    n = int(input())

    dictionary = {}

    for _ in range(n):
        word = input().strip()
        key = signature(word)
        if key not in dictionary:
            dictionary[key] = word

    words = text[:-1].split(' ')
    answer = []

    for word in words:
        key = signature(word)
        original = dictionary.get(key)

        if original is None:
            print("No solution")
            return

        answer.append(original)

    print(' '.join(answer) + '.')

if __name__ == "__main__":
    solve()
```

The `signature` function constructs a fixed-size frequency vector. Its running time is linear in the word length because every character is processed exactly once. The tuple makes the vector immutable, so it can safely be used as part of a dictionary key.

The dictionary is filled before processing the sentence. When two dictionary words have the same signature, the first one is retained. This is deliberate because the output only requires one valid original text.

The sentence is parsed with `text[:-1]`, which removes exactly the final period. The guarantees about the input mean that no other punctuation needs special handling. Splitting by a single space then gives the original word sequence.

The lookup uses `dictionary.get(key)` rather than indexing directly. A missing signature produces `None`, which lets the program immediately report `No solution`. Every valid dictionary word is a nonempty lowercase string, so `None` cannot be confused with a legitimate stored value.

The final period is added only after all words have been reconstructed. This avoids accidentally treating it as part of a word signature.

Python integers do not overflow here. The largest frequency is at most (5\cdot10^5), which is far below any practical integer limit.

## Worked Examples

For Sample 1, the dictionary contains `hello` and `world`. The observed words are `hello` and `wolrd`.

| Word | First | Last | Letter counts | Lookup result |
| --- | --- | --- | --- | --- |
| `hello` | `h` | `o` | `e:1, h:1, l:2, o:1` | `hello` |
| `wolrd` | `w` | `d` | `d:1, l:1, o:1, r:1, w:1` | `world` |

The first word is already in dictionary form, so its signature finds `hello`. The second word has the same character multiset and endpoints as `world`, so its signature finds `world`. The reconstructed result is `hello world.`.

For Sample 2, the only dictionary word that could potentially match the second sentence word is `world`, but the observed word is `wlrd`.

| Word | First | Last | Length | Lookup result |
| --- | --- | --- | --- | --- |
| `hello` | `h` | `o` | 5 | `hello` |
| `wlrd` | `w` | `d` | 4 | absent |

The second signature cannot equal the signature of `world`, because the letter `o` is missing and the total number of characters differs. The lookup fails, so the algorithm immediately prints `No solution`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(S+D+26(W+n))), effectively (O(S+D)) | Every input character is counted once, and each signature has exactly 26 counters |
| Space | (O(D+26(W+n))), effectively (O(D+W+n)) | The hash table stores one representative word and one fixed-size signature per dictionary signature |

The total sentence length and total dictionary length are both bounded by (5\cdot10^5). The alphabet has only 26 letters, so the fixed 26-element part of each signature is small. The algorithm consequently performs a linear amount of character processing plus hash-table operations, which fits the intended constraints.

## Test Cases

```python
import sys
import io

def signature(word):
    cnt = [0] * 26
    for ch in word:
        cnt[ord(ch) - 97] += 1
    return (word[0], word[-1], tuple(cnt))

def solve():
    input = sys.stdin.readline

    text = input().rstrip('\n')
    n = int(input())

    dictionary = {}

    for _ in range(n):
        word = input().strip()
        key = signature(word)
        if key not in dictionary:
            dictionary[key] = word

    words = text[:-1].split(' ')
    answer = []

    for word in words:
        original = dictionary.get(signature(word))
        if original is None:
            print("No solution")
            return
        answer.append(original)

    print(' '.join(answer) + '.')

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided samples
assert run("""hello wolrd.
2
hello
world
""") == "hello world.", "sample 1"

assert run("""hello wlrd.
2
hello
world
""") == "No solution", "sample 2"

assert run("""tihs is vrey sceret txet.
7
text
secret
serect
scret
is
very
this
""") == "this is very secret text.", "sample 3"

# Minimum-size input
assert run("""a.
1
a
""") == "a.", "single-letter word"

# One-letter observed word must not match another letter
assert run("""b.
1
a
""") == "No solution", "single-letter mismatch"

# Same endpoints and letter multiset, but dictionary has several valid choices
result = run("""scret.
2
secret
serect
""")
assert result in {"secret.", "serect."}, "multiple valid dictionary words"

# Boundary case where the last letter matters
assert run("""abcda.
1
abcdb
""") == "No solution", "different last letter"

# Large input close to the sentence-size limit
long_word = "a" * 499999
large_input = long_word + ".\n1\n" + long_word + "\n"
assert run(large_input) == long_word + ".", "large word"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a.` with dictionary `a` | `a.` | Smallest possible word and empty internal part |
| `b.` with dictionary `a` | `No solution` | Endpoint mismatch |
| `scret.` with `secret`, `serect` | Either compatible dictionary word | Multiple dictionary words with the same signature |
| `abcda.` with `abcdb` | `No solution` | Last-character boundary |
| A 499999-character word with itself in the dictionary | The same large word | Near-maximum input size and linear processing |

## Edge Cases

A one-letter word is handled without special branching because the signature counts the only character and records it as both the first and last character. For

```
a.
1
a
```

the signature of the sentence word is exactly the signature stored for `a`, so the output is `a.`. For

```
b.
1
a
```

the frequency vector and endpoints differ, so the lookup fails and the output is `No solution`.

Multiple dictionary words can represent the same corrupted word. Consider

```
scret.
2
secret
serect
```

Both dictionary words have first letter `s`, last letter `t`, and the same letter frequencies. The hash table keeps one representative. Whichever one is retained can reconstruct `scret`, so the output is valid regardless of which dictionary entry was stored.

A wrong internal letter count cannot be repaired by rearrangement. Consider

```
wlrd.
1
world
```

The observed word has one `w`, one `l`, one `r`, and one `d`, while `world` additionally contains `o` and has length five. Their signatures differ, so the dictionary lookup fails. The algorithm prints `No solution` rather than accepting a word merely because its endpoints agree.

The final period must not participate in the signature. For

```
hello wolrd.
2
hello
world
```

the parser removes the final period before splitting the sentence. It processes `hello` and `wolrd`, finds `hello` and `world`, then restores the period after joining the reconstructed words. This keeps punctuation separate from the letter-frequency condition.
