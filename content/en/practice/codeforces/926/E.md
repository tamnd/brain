---
problem: 926E
contest_id: 926
problem_index: E
name: "Merge Equal Elements"
contest_name: "VK Cup 2018 - Wild-card Round 1"
rating: 1900
tags: ["constructive algorithms", "data structures"]
answer: passed_samples
verified: true
solve_time_s: 65
date: 2026-06-17
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a3270f4-c654-83ec-aadf-ab79419d4fc3
---

# CF 926E - Merge Equal Elements

**Rating:** 1900  
**Tags:** constructive algorithms, data structures  
**Model:** gpt-5-3-mini  
**Solve time:** 1m 5s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a3270f4-c654-83ec-aadf-ab79419d4fc3  

---

## Solution

## Problem Understanding

We are given a sequence of positive integers, arranged in a line. The process repeatedly looks for two identical numbers that sit next to each other. Whenever such a pair exists, the leftmost such pair is chosen, both elements are removed, and a single element equal to their value plus one is inserted in their place. This changes the sequence length by reducing it by one, and it can also create new adjacent equal pairs, so the process continues until no two neighboring elements are equal.

The task is to compute the final stable sequence after all possible merges have been performed.

The constraint that the sequence can have up to 200,000 elements immediately rules out any solution that repeatedly scans the array and performs deletions in linear time per operation. In the worst case, each merge reduces the length by one, so there can be O(n) operations, and a naive simulation that also scans for the leftmost pair each time can degrade to O(n²), which is too slow.

A more subtle issue is that merges can cascade. A single merge can produce a value that matches its new neighbor, forcing repeated chaining merges. For example, in a sequence like 1, 1, 2, 2, merging the first pair creates a 2, which may immediately form another merge. Any correct approach must account for these cascades without restarting full scans.

Another edge case is when equal values are not adjacent initially but become adjacent only after multiple merges. A naive greedy pointer strategy that only looks locally and never revisits earlier positions will fail on such cases.

## Approaches

A direct simulation would repeatedly scan the array from left to right to find the first occurrence of equal neighbors, perform the merge, and then restart scanning. This is correct because it matches the process definition exactly. However, each scan is O(n), and we may perform O(n) merges, leading to O(n²) behavior in worst cases such as long runs of identical elements that repeatedly collapse.

The key observation is that the process only ever modifies local structure around the most recent insertion point. Once we process elements from left to right, any potential merge involving earlier elements will always be triggered by the most recently formed value. This suggests maintaining a structure that represents the current reduced prefix and only reacts locally when a new element is appended.

A stack naturally encodes this idea. We process elements from left to right, pushing them into a stack. Whenever the top two elements become equal, we merge them into a single element with value incremented by one. This new element may again equal the previous element in the stack, so we must continue merging until stability is restored at the top. This repeated local collapsing simulates exactly what would happen if we always merged the leftmost available pair in the original sequence.

The important conceptual shift is that although the original rule refers to the leftmost pair globally, every merge only affects a contiguous region, and once we process elements in order, the leftmost active region is always at the top of our stack representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force simulation | O(n²) | O(n) | Too slow |
| Stack merging | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain a stack that represents the current reduced sequence after processing a prefix of the array.

1. Start with an empty stack. We will process the input from left to right.
2. For each element x in the array, push x onto the stack. This represents appending it to the current sequence.
3. After each push, check whether the last two elements in the stack are equal. If they are not, no merge is possible at this position, so we continue to the next input element.
4. If the last two elements are equal, remove both and replace them with a single element equal to their value plus one.
5. After performing this replacement, the new top element may now be equal to the previous element in the stack, so we repeat the check and merge again as long as the last two elements are equal.
6. Continue this process until the stack becomes stable at the top, then proceed to the next input element.
7. After all elements are processed, the stack represents the final sequence.

The repeated merging at the top is essential because each merge can create a new “carry” upward, similar to addition in a number system where identical adjacent digits combine and propagate.

### Why it works

The stack maintains the invariant that after processing the first k elements of the input, it represents the exact result of fully resolving all merges that can occur entirely within that prefix. Any merge in the full process must involve adjacent elements that, at the moment they become equal, correspond to the top of this structure. Since merges never depend on future elements and only collapse contiguous equal blocks upward, every valid operation in the original process is mirrored by a corresponding collapse at the top of the stack. This ensures that no merge is missed and no invalid merge is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    st = []
    
    for x in a:
        st.append(x)
        
        while len(st) >= 2 and st[-1] == st[-2]:
            x = st[-1]
            st.pop()
            st.pop()
            st.append(x + 1)
    
    print(len(st))
    print(*st)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the stack process. Each element is appended once, and every merge operation is handled immediately at the top of the stack. The variable reuse of `x` ensures that after merging two equal values, the incremented result is correctly fed into further potential merges.

A subtle point is that we never restart scanning from the beginning. All necessary propagation is handled by repeated checks at the stack top, which preserves correctness while keeping the complexity linear.

## Worked Examples

Consider the sequence 5, 2, 1, 1, 2, 2.

| Step | Input | Stack state |
| --- | --- | --- |
| 1 | 5 | [5] |
| 2 | 2 | [5, 2] |
| 3 | 1 | [5, 2, 1] |
| 4 | 1 | [5, 2, 2] → merge → [5, 3] |
| 5 | 2 | [5, 3, 2] |
| 6 | 2 | [5, 3, 3] → merge → [5, 4] |

This shows how a local merge triggers a cascade and how the stack naturally captures repeated compression without rescanning earlier parts of the sequence.

Now consider 1, 1, 1, 1.

| Step | Input | Stack state |
| --- | --- | --- |
| 1 | 1 | [1] |
| 2 | 1 | [2] |
| 3 | 1 | [2, 1] |
| 4 | 1 | [2, 2] → [3] |

This example shows a full chain reaction where multiple merges propagate upward, eventually collapsing the entire sequence into a single value.

The second example demonstrates that merges are not independent events, and that intermediate results must be repeatedly reconsidered at the boundary of the current structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is pushed once and popped at most once per merge event, and every merge reduces total stack size. |
| Space | O(n) | The stack stores at most all elements in the worst case before any merges occur. |

The linear behavior fits comfortably within constraints of 200,000 elements, since each operation is constant amortized time and no repeated scanning is performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("6\n5 2 1 1 2 2\n") == "2\n5 4"

# single element
assert run("1\n10\n") == "1\n10"

# no merges
assert run("4\n1 2 3 4\n") == "4\n1 2 3 4"

# full collapse
assert run("4\n1 1 1 1\n") == "1\n3"

# cascading carry chain
assert run("5\n1 1 2 2 3\n") == "2\n3 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 5 2 1 1 2 2 | 2 5 4 | standard cascade behavior |
| 1 10 | 1 10 | minimum size handling |
| 1 2 3 4 | 4 1 2 3 4 | no merge case |
| 4 1 1 1 1 | 1 3 | repeated cascading merges |
| 5 1 1 2 2 3 | 2 3 3 | mixed chain interactions |

## Edge Cases

A key edge case is when merges propagate multiple steps upward, creating a chain of consecutive equal values in the stack. For example, in the input 1, 1, 2, 2, 3, processing creates intermediate states where merging 1,1 produces 2, which then merges with adjacent 2s, and so on. The stack handles this correctly because after every merge, it rechecks the top pair, ensuring that any newly created equality is immediately resolved.

Another subtle case is when repeated increments cause values far apart in the original array to become equal after multiple merges. Since the algorithm never discards historical information beyond the stack boundary, all such potential interactions are naturally captured when those values become adjacent in the reduced structure.