---
problem: 1281A
contest_id: 1281
problem_index: A
name: "Suffix Three"
contest_name: "Codeforces Round 607 (Div. 2)"
rating: 800
tags: ["implementation"]
answer: passed_samples
verified: true
solve_time_s: 147
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2da53e-aedc-83ec-a672-425fbbff0c7c
---

# CF 1281A - Suffix Three

**Rating:** 800  
**Tags:** implementation  
**Model:** gpt-5-3-mini  
**Solve time:** 2m 27s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2da53e-aedc-83ec-a672-425fbbff0c7c  

---

## Solution

## Problem Understanding

We are given multiple independent sentences. Each sentence is a single string where words are joined using underscores instead of spaces. Our task is to classify each sentence into one of three languages by looking only at how the sentence ends.

The classification rule is purely suffix-based. If the sentence ends with certain fixed patterns, we map it to a language name. The sentence structure before the ending does not matter at all, only the final characters determine the answer.

The constraints are small: at most 30 sentences, each up to 1000 characters. This immediately tells us that any solution that inspects each character or performs constant-time suffix checks per test case is easily fast enough. Even a naive approach that checks all possible suffix matches per string is trivial under these limits because the total work is bounded by roughly 30,000 characters.

A subtle edge case to be careful about is ensuring we only match suffixes at the very end of the string and not accidentally inside the string. For example, a naive search for "po" anywhere would be wrong because only the ending matters. Another potential pitfall is overlapping suffix lengths. For instance, "masu" and "desu" both indicate Japanese, so the implementation must check both correctly without assuming a single fixed suffix length.

## Approaches

A brute-force interpretation would be to scan each sentence and check whether it ends with any of the known suffixes by comparing characters from the end manually. For each string, we could compare it against all suffixes by slicing and checking equality. Since there are only four suffix candidates, this approach performs at most four comparisons per test case, each comparison taking O(L) in the worst case where L is the suffix length. With L bounded by 1000, this is still extremely small.

The key observation is that we do not need any preprocessing or complex parsing. The problem reduces entirely to checking whether the string ends with one of a few fixed patterns. That means we can directly use suffix comparison operations. The structure of the input guarantees that exactly one suffix matches, so we do not need ambiguity handling or priority rules.

The transition from brute force to optimal is essentially recognizing that the decision space is constant-sized. Instead of scanning or parsing, we reduce each test case to a handful of string comparisons.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (manual scanning) | O(t · L) | O(1) | Accepted |
| Optimal (suffix checks) | O(t · L) | O(1) | Accepted |

## Algorithm Walkthrough

We process each sentence independently and determine its language using suffix checks.

1. Read the number of test cases. This defines how many independent classification operations we will perform.
2. For each sentence, check whether it ends with the suffix "mnida". If it does, output "KOREAN". This check is done first because it is unique and avoids unnecessary ambiguity with other suffixes.
3. If it does not end with "mnida", check whether it ends with "desu" or "masu". If either condition holds, output "JAPANESE". These two suffixes belong to the same language group, so they are combined logically using an OR condition.
4. If neither of the above matches, the sentence must end with "po", so output "FILIPINO". The problem guarantees that every input ends with one of the valid suffixes, so no fallback validation is needed.

The order of checks is not strictly necessary in this problem because suffixes do not overlap in a way that causes ambiguity, but writing them explicitly keeps the logic clear and avoids accidental misclassification if the rules are extended.

### Why it works

Each sentence is guaranteed to end with exactly one valid suffix from a fixed set. Since suffix equality is a deterministic property, checking the final characters directly is sufficient to uniquely identify the language. The algorithm relies on the invariant that no valid sentence can match more than one language suffix at the end, so the first matching condition is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()

    if s.endswith("mnida"):
        print("KOREAN")
    elif s.endswith("desu") or s.endswith("masu"):
        print("JAPANESE")
    else:
        print("FILIPINO")
```

The solution uses Python’s built-in `endswith` method, which directly implements suffix comparison efficiently. Each check runs in time proportional to the suffix length, which is constant and very small.

The order of conditions mirrors the logical grouping of suffixes. Korean is checked first because it is a distinct single-suffix category. Japanese is handled next using a combined OR condition. Filipino becomes the default case because the problem guarantees completeness of the suffix set.

The use of `strip()` ensures that newline characters do not interfere with suffix matching, which is a common implementation detail mistake in contest settings.

## Worked Examples

We trace two representative cases to see how suffix detection determines the output.

### Example 1

Input:

```
kamusta_po
genki_desu
```

| Step | String | Ends with "mnida"? | Ends with "desu"/"masu"? | Output |
| --- | --- | --- | --- | --- |
| 1 | kamusta_po | No | No | FILIPINO |
| 2 | genki_desu | No | Yes | JAPANESE |

The first string ends in "po", so it fails all earlier checks and defaults to Filipino. The second string matches the Japanese suffix "desu", triggering the second condition.

### Example 2

Input:

```
annyeong_hashimnida
si_roy_mustang_ay_namamasu
```

| Step | String | Ends with "mnida"? | Ends with "desu"/"masu"? | Output |
| --- | --- | --- | --- | --- |
| 1 | annyeong_hashimnida | Yes | - | KOREAN |
| 2 | si_roy_mustang_ay_namamasu | No | Yes | JAPANESE |

The first sentence clearly matches the Korean suffix "mnida", which immediately determines the output without needing further checks. The second matches "masu", confirming Japanese.

These examples confirm that suffix matching alone is sufficient and unambiguous under the given guarantees.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · L) | Each test case performs a constant number of suffix comparisons, each scanning at most the last few characters of the string |
| Space | O(1) | No additional data structures are used beyond input storage |

The constraints allow up to 30 strings of length 1000, so at most 30,000 character checks are performed, which is trivial within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        s = input().strip()
        if s.endswith("mnida"):
            out.append("KOREAN")
        elif s.endswith("desu") or s.endswith("masu"):
            out.append("JAPANESE")
        else:
            out.append("FILIPINO")
    return "\n".join(out)

# provided sample
assert run("""8
kamusta_po
genki_desu
ohayou_gozaimasu
annyeong_hashimnida
hajime_no_ippo
bensamu_no_sentou_houhou_ga_okama_kenpo
ang_halaman_doon_ay_sarisari_singkamasu
si_roy_mustang_ay_namamasu
""") == """FILIPINO
JAPANESE
JAPANESE
KOREAN
FILIPINO
FILIPINO
JAPANESE
JAPANESE"""

# custom: single character string edge (invalid but structurally safe)
assert run("""1
po
""") == "FILIPINO"

# custom: all Japanese variants
assert run("""2
a_desu
b_masu
""") == """JAPANESE
JAPANESE"""

# custom: Korean dominance check
assert run("""1
xmnida
""") == "KOREAN"

# custom: mixed unrelated prefix, Filipino fallback
assert run("""1
very_long_sentence_about_nothing_po
""") == "FILIPINO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `po` | FILIPINO | minimal valid Filipino suffix |
| `a_desu / b_masu` | JAPANESE | both Japanese suffix variants |
| `xmnida` | KOREAN | Korean suffix detection correctness |
| long `_po` sentence | FILIPINO | suffix correctness independent of prefix |

## Edge Cases

One edge case is when the sentence is extremely short and consists only of the suffix itself. For example, input `po` should still correctly be classified as Filipino. The algorithm handles this naturally because `endswith("po")` is true even when the entire string is exactly two characters.

Another edge case is when multiple suffix patterns might appear as substrings earlier in the sentence. For example, `po_desu_mnida_po` contains all three tokens internally, but only the final suffix matters. The implementation is correct because it never scans the whole string, only the tail.

A final edge case is overlapping suffix lengths. Since `"desu"` and `"masu"` share the same language but different endings, both must be checked explicitly. The OR condition ensures both are treated equally, and no precedence issue arises because only the final match matters.