---
title: "CF 102824G - Gemstones"
description: "We have a collection of rocks, where each rock is described by a string of lowercase letters. A letter represents a mineral type that appears inside that rock."
date: "2026-07-26T22:39:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102824
codeforces_index: "G"
codeforces_contest_name: "mBIT Advanced November 2020"
rating: 0
weight: 102824
solve_time_s: 33
verified: true
draft: false
---

[CF 102824G - Gemstones](https://codeforces.com/problemset/problem/102824/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of rocks, where each rock is described by a string of lowercase letters. A letter represents a mineral type that appears inside that rock. The same mineral can appear many times in one rock, but for a mineral to be considered a gemstone, it must appear in every rock at least once.

The task is to count how many different mineral types satisfy this condition. The input gives the number of rocks followed by the mineral descriptions of each rock. The output is the number of lowercase letters that are common to all descriptions.

The main constraint is that the alphabet is fixed: there are only 26 possible mineral types. Even if the number of rocks or the length of the descriptions grows large, the number of possible answers remains constant. This means we should avoid comparing every pair of rocks or scanning all characters repeatedly when a simple frequency or presence tracking method is enough. A solution that depends on the square of the number of rocks would become unnecessary work, while a solution that processes each character once is easily fast enough.

The subtle cases come from the difference between appearing in a rock and appearing multiple times in a rock. For example, if the input is:

```
3
aaa
a
aa
```

the answer is:

```
1
```

The mineral `a` is a gemstone because it appears in all three rocks. A careless solution that counts total occurrences instead of checking presence in each rock could overcount it.

Another edge case is when no mineral is shared by all rocks. For example:

```
2
abc
def
```

the correct output is:

```
0
```

A solution that starts with all letters as valid and only removes missing letters must handle this case correctly.

A final boundary case is a single rock:

```
1
xyz
```

The output is:

```
3
```

Every mineral appearing in the only rock is automatically present in every rock. Solutions that assume at least two rocks may incorrectly return zero.

## Approaches

The direct approach is to check every possible mineral and test whether it appears in every rock. Since there are only 26 letters, this is already much better than comparing every pair of strings. For each letter, we scan all rocks and mark it invalid if any rock does not contain that letter. The work is proportional to the number of rocks multiplied by 26, plus the cost of checking membership inside each string. If membership is implemented by searching the string every time, the total work can reach about `26 * n * m`, where `m` is the average rock length.

A more natural solution comes from the fact that the alphabet size is tiny. Instead of repeatedly asking whether a letter exists in a rock, we summarize each rock once. For every rock, we record the set of letters that appear in it. Then we intersect these sets. After processing all rocks, only letters that survived every intersection are gemstones.

The brute-force method works because there are only a few possible mineral types, but it repeats the same existence checks many times. The key observation is that a rock only contributes information about which letters are present, not how many times they appear. Representing each rock as a set of present letters removes unnecessary repeated work.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26 * n * m) | O(1) | Accepted for small inputs, but unnecessary work |
| Optimal | O(total length of all strings + 26 * n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Initialize the set of possible gemstones with all 26 lowercase letters. At the beginning, every mineral could still be present in every rock.
2. Read each rock one by one and build the set of letters that occur in that rock. Repeated occurrences of the same letter do not change the set because only existence matters.
3. Intersect the current candidate set with the letters found in the current rock. Any letter missing from this rock can never be a gemstone, so it must be removed.
4. After all rocks are processed, count the remaining letters. These are exactly the minerals that appeared in every rock.

Why it works:

The maintained set always represents the minerals that have appeared in every rock processed so far. Initially, before seeing any rocks, all letters satisfy this condition. When a new rock is processed, only letters present in that rock can continue satisfying the condition, so the intersection operation preserves the invariant. After the final rock, the set contains exactly the letters present in all rocks, which is the definition of a gemstone.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    common = set("abcdefghijklmnopqrstuvwxyz")

    for _ in range(n):
        rock = input().strip()
        common &= set(rock)

    print(len(common))

if __name__ == "__main__":
    solve()
```

The solution first creates the candidate set containing every lowercase letter. This corresponds to the initial state where no rock has been checked yet.

For each rock, `set(rock)` converts the description into a collection of minerals that appear at least once. This removes duplicate occurrences automatically, which is exactly the information needed for this problem. The intersection operator keeps only minerals that were already possible and are also present in the current rock.

The final size of `common` is the answer. There are no indexing concerns because the algorithm works directly with character values. Integer overflow is not a concern because the largest value printed is only 26.

## Worked Examples

Consider the input:

```
3
abcdde
baccd
eeabg
```

The trace is:

| Step | Current rock | Letters in rock | Remaining gemstones |
| --- | --- | --- | --- |
| Start | none | all letters | abcdefghijklmnopqrstuvwxyz |
| 1 | abcdde | abcde | abcde |
| 2 | baccd | abcd | abcd |
| 3 | eeabg | abeg | ab |

The answer is `2`. The trace shows that only letters surviving every intersection remain.

For another example:

```
2
abc
def
```

| Step | Current rock | Letters in rock | Remaining gemstones |
| --- | --- | --- | --- |
| Start | none | all letters | abcdefghijklmnopqrstuvwxyz |
| 1 | abc | abc | abc |
| 2 | def | def | empty |

The answer is `0`. This demonstrates the case where no mineral appears in every rock.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total length of all strings) | Each character is processed once while building the sets |
| Space | O(26) | Only the current set of possible gemstones is stored |

The algorithm depends linearly on the total input size and uses only constant extra memory. Since the alphabet never grows beyond 26 letters, the method remains efficient even when the rock descriptions are large.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)
    common = set("abcdefghijklmnopqrstuvwxyz")
    for _ in range(n):
        common &= set(input().strip())
    print(len(common))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("3\nabcdde\nbaccd\neeabg\n") == "2\n", "sample 1"
assert run("2\nabc\ndef\n") == "0\n", "no common minerals"
assert run("1\nxyz\n") == "3\n", "single rock"
assert run("3\naaa\na\naa\n") == "1\n", "duplicate occurrences"
assert run("4\nabcdefghijklmnopqrstuvwxyz\nabcdefghijklmnopqrstuvwxyz\nabc\nabc\n") == "3\n", "large alphabet boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / abcdde / baccd / eeabg` | `2` | Standard intersection case |
| `2 / abc / def` | `0` | No shared mineral |
| `1 / xyz` | `3` | Single rock behavior |
| `3 / aaa / a / aa` | `1` | Duplicate letters are counted once |
| Four rocks containing the full alphabet and reduced subsets | `3` | Correct handling of larger descriptions and boundaries |

## Edge Cases

For the first edge case:

```
3
aaa
a
aa
```

The first rock leaves only `a` as a candidate. The second rock still contains `a`, and the third rock also contains `a`, so the final set has one element. The algorithm outputs `1` because it tracks presence rather than frequency.

For the second edge case:

```
2
abc
def
```

After processing the first rock, the candidates are `{a, b, c}`. Intersecting with `{d, e, f}` removes everything, leaving an empty set. The algorithm correctly outputs `0`.

For the single-rock case:

```
1
xyz
```

The initial set of all letters is intersected with `{x, y, z}` once. The remaining set has three elements, so the output is `3`. This works because every mineral inside the only rock is present in all rocks.

For a case where letters repeat heavily:

```
3
aaaaab
bbbbba
ababab
```

The first rock contributes `{a, b}`, the second also contributes `{a, b}`, and the third contributes `{a, b}`. The answer is `2`. The algorithm ignores duplicate occurrences because they do not affect whether a mineral exists in a rock.
