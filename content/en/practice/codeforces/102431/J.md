---
title: "CF 102431J - Wire-compatible Protocol buffer"
description: "A protobuf message is a sequence of encoded fields. The field name never appears on the wire. What identifies a field is its numeric tag, and the wire type tells the decoder how many bytes belong to that field."
date: "2026-08-09T00:07:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102431
codeforces_index: "J"
codeforces_contest_name: "2019 China Collegiate Programming Contest Final (CCPC-Final 2019)"
rating: 0
weight: 102431
solve_time_s: 842
verified: true
draft: false
---

[CF 102431J - Wire-compatible Protocol buffer](https://codeforces.com/problemset/problem/102431/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 14m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

A protobuf message is a sequence of encoded fields. The field name never appears on the wire. What identifies a field is its numeric tag, and the wire type tells the decoder how many bytes belong to that field. In this simplified problem, a `double` uses wire type 1, while both a `string` and an embedded message use wire type 2.

For two message descriptors to be wire-format compatible, they must accept exactly the same kinds of serialized field sequences. That immediately gives us several local requirements. A field with a particular tag must exist in both messages. Its rule must match, because `required`, `optional`, and `repeated` permit different numbers of occurrences. Its wire-level type must also match. A `double` cannot be replaced by a string or a message, and a string cannot be replaced by an embedded message merely because both use wire type 2.

For embedded messages there is one more condition. Suppose both messages have an optional field numbered 3 whose type is another message. The two outer messages are compatible only when the two nested message types are themselves compatible. This creates a recursive graph of compatibility requirements. The graph may contain cycles, as shown by a message containing an optional field of its own type.

The descriptor is given as a number of text lines, followed by up to 50,000 queries. There are at most 1,000 message types, and every message contains at most 16 fields. The small number of messages is the key constraint. It allows us to spend roughly quadratic time in the number of messages, but the large number of queries means we cannot perform a fresh expensive recursive comparison for every query.

A useful way to view a message is as a labeled directed graph node. Every field is an outgoing edge labeled by its tag, rule, and wire-level kind. For primitive fields the edge ends at a fixed terminal type such as `string` or `double`; for a message field it ends at another message node. Two message nodes are compatible exactly when their outgoing labeled edges match and corresponding message edges lead to compatible nodes.

Several edge cases are easy to mishandle.

Consider different field names with the same tag:

```
message A {
optional string first = 1 ;
}
message B {
optional string second = 1 ;
}
2
A B
```

The correct output is:

```
Wire-format compatible.
```

A careless solution that compares field names would reject this pair, but field names are not serialized.

Now consider the same field name with different tags:

```
message A {
optional string value = 1 ;
}
message B {
optional string value = 2 ;
}
1
A B
```

The correct output is:

```
Wire-format incompatible.
```

The decoder looks up fields by numeric tag, so equal names do not help.

The field rule also matters:

```
message A {
optional string value = 1 ;
}
message B {
repeated string value = 1 ;
}
1
A B
```

The correct output is:

```
Wire-format incompatible.
```

A repeated field may occur more than once, while an optional field may occur at most once. A decoder cannot interpret every valid instance of one schema as a valid instance of the other.

Finally, embedded messages cannot simply be treated as strings because both use wire type 2:

```
message Empty {
}
message Holder {
optional Empty value = 1 ;
}
message Text {
optional string value = 1 ;
}
1
Holder Text
```

The correct output is:

```
Wire-format incompatible.
```

A string can contain arbitrary valid UTF-8 data, whereas the payload of `Empty` must be a serialized `Empty` message, which is much more restricted.

The bound of 1,000 messages and 16 fields per message makes an (O(M^2F)) preprocessing algorithm practical, where (M) is the number of messages and (F) is the maximum number of fields. At the maximum size this is about 16 million field-level operations per refinement pass structure, rather than doing comparable work separately for 50,000 queries. The 50,000 query bound is precisely what rules out solving each query independently.

## Approaches

The direct approach is to recursively compare two message types. First compare their sets of field numbers, rules, and primitive types. Whenever both sides contain a message field, recursively compare the two referenced message types. A memo table for pairs of messages prevents infinite recursion when the descriptor contains cycles.

This is correct because compatibility of a message is completely determined by the compatibility of its corresponding fields. However, the state of such a comparison is a pair of message types, so there can be up to (M^2) different states. With (M=1000), a single difficult query can visit up to one million message pairs. With at most 16 fields per pair, that can require about 16 million field comparisons. Repeating this for 50,000 queries gives a worst case around 800 billion field checks.

The brute-force method works because the compatibility relation is recursive, but it fails because the same pair of message types can be rediscovered independently for many queries. The observation that unlocks the faster solution is that compatibility is an equivalence relation determined by the complete labeled neighborhood of every message. We can compute all equivalence classes once.

Start by putting messages into classes according to their immediate wire-level structure. A field contributes its tag, its rule, and whether its value is a `double`, a `string`, or another message. For a message-valued field, the identity of the target is temporarily ignored.

Then repeatedly refine the classes. When a field points to another message, replace the target message by its current class number. Two messages remain in the same class only if their fields have identical tags and rules, identical primitive kinds, and their corresponding message fields point to the same current classes.

This process is partition refinement. Every iteration can only split classes, never merge two messages that were already separated. There are only (M) messages, so after at most (M-1) strict refinements the partition must stabilize. At that point, two messages have the same class exactly when they are wire-format compatible. Cyclic definitions are handled naturally because every iteration uses only the classes computed in the previous iteration.

With 1,000 messages and at most 16 fields each, even the simple refinement implementation is fast enough. After preprocessing, every query is just a comparison of two integer class identifiers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(QM^2F)) worst case with memoization per query | (O(M^2)) per query | Too slow |
| Optimal | (O(M^2F)) worst case | (O(MF)) | Accepted |

Here (M) is the number of messages, (F) is the maximum number of fields in a message, and (Q) is the number of queries.

## Algorithm Walkthrough

1. Parse every message and assign it an integer ID. For each field, store its tag, its rule, and its type. If the type is another message, store the referenced message ID.
2. Represent each message as its fields sorted by tag. The source descriptor may list fields in any order, but field order has no meaning in protobuf serialization, so sorting by tag gives us a canonical local ordering.
3. Give every message the same initial class. We are intentionally ignoring the identities of nested message types at first. The first refinement will distinguish messages using everything that can already be determined locally.
4. Build a signature for every message using the current classes. For a primitive field, the signature contains its tag, rule, and primitive type. For a message field, it contains its tag, rule, the marker saying that it is a message, and the current class of its target.
5. Assign equal integer IDs to equal signatures. These IDs form the new partition of the messages. If two messages have different signatures, they cannot be compatible because some field-level wire behavior differs. If they have the same signature, they remain candidates for compatibility.
6. Repeat the signature construction until the class assignment stops changing. Every refinement either separates at least one previously equal pair or reaches a fixed point. Since there are only (M) messages, there can be at most (M-1) strict refinements.
7. For each query, look up the class IDs of its two message names. Equal IDs mean that the messages have identical recursively defined wire behavior, so print `Wire-format compatible.` Otherwise print `Wire-format incompatible.`

### Why it works

The invariant is that after every refinement, messages in different classes cannot be wire-format compatible. A difference in tag, rule, primitive wire type, or the current class of a nested message gives a concrete difference in the serialized data that the two descriptors can accept.

When the process stabilizes, every pair of messages in the same class has matching fields, and every corresponding nested message field points to the same stable class. Thus the two messages satisfy exactly the same recursive compatibility conditions. Conversely, two compatible messages can never be separated by a refinement, because compatible fields must have the same tag, rule, primitive kind, or compatible nested target. The stable classes are consequently exactly the wire-format compatibility classes.

The use of previous iteration classes is what makes cycles safe. For example, if `A` contains an optional `A`, its signature refers to the class of `A` from the previous iteration. It does not require recursively expanding the message forever. A mutually recursive group such as `B -> C -> B` can consequently settle into the same class when their observable wire structures are equivalent.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    tokens = []

    for _ in range(n):
        tokens.extend(input().split())

    pos = 0
    messages = []
    name_to_id = {}

    while pos < len(tokens):
        assert tokens[pos] == "message"
        pos += 1

        name = tokens[pos]
        pos += 1

        mid = len(messages)
        name_to_id[name] = mid
        messages.append({
            "name": name,
            "fields": []
        })

        assert tokens[pos] == "{"
        pos += 1

        while tokens[pos] != "}":
            label = tokens[pos]
            typ = tokens[pos + 1]
            field_name = tokens[pos + 2]
            assert tokens[pos + 3] == "="
            tag = int(tokens[pos + 4])
            assert tokens[pos + 5] == ";"
            pos += 6

            messages[mid]["fields"].append(
                [tag, label, typ]
            )

        pos += 1

    # Resolve message type names to integer IDs.
    for msg in messages:
        fields = []
        for tag, label, typ in msg["fields"]:
            if typ == "double":
                fields.append((tag, label, 0, -1))
            elif typ == "string":
                fields.append((tag, label, 1, -1))
            else:
                fields.append((tag, label, 2, name_to_id[typ]))

        fields.sort(key=lambda x: x[0])
        msg["fields"] = fields

    m = len(messages)

    # Initially all messages are in one class.
    cls = [0] * m

    while True:
        signatures = []

        for msg in messages:
            sig = []

            for tag, label, kind, target in msg["fields"]:
                if kind == 2:
                    sig.append((tag, label, kind, cls[target]))
                else:
                    sig.append((tag, label, kind))

            signatures.append(tuple(sig))

        ids = {}
        new_cls = [0] * m

        for i, sig in enumerate(signatures):
            if sig not in ids:
                ids[sig] = len(ids)
            new_cls[i] = ids[sig]

        if new_cls == cls:
            break

        cls = new_cls

    q = int(input())
    out = []

    for _ in range(q):
        a, b = input().split()

        if cls[name_to_id[a]] == cls[name_to_id[b]]:
            out.append("Wire-format compatible.")
        else:
            out.append("Wire-format incompatible.")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The parser first reads all descriptor tokens from the first `n` lines. This is convenient because braces, semicolons, field names, and type names are already separated by spaces according to the input format. A field therefore always occupies exactly six tokens after its label begins.

The first representation keeps message type names as strings so that all message names can be registered before resolving references. Once parsing is complete, every message reference is converted into an integer ID. This avoids dictionary lookups during the refinement loop.

The fields are sorted by tag. This is necessary because the descriptor order does not affect the wire format. Without sorting, two otherwise identical messages could receive different signatures simply because their declarations appeared in different orders.

The integer `kind` distinguishes the three possible field value categories. `0` represents `double`, `1` represents `string`, and `2` represents an embedded message. A message field includes the current class of its target, while primitive fields do not have a target class.

The refinement loop starts with every message in class zero. On each iteration, every message receives a complete signature describing its current observable structure. Equal signatures receive equal class IDs. If the new class array is identical to the previous one, the partition has reached a fixed point.

The comparison `new_cls == cls` is safe because class IDs are assigned deterministically by scanning messages in ID order. If the partition has not changed, the corresponding signatures have not changed either, so another iteration cannot refine anything.

There is no integer overflow issue in Python. Field numbers can be as large as 536,870,911, which is easily handled by Python integers. The maximum field count is only 16, so each signature remains small.

The query phase is deliberately trivial. All recursive work has already been performed during preprocessing, so each of the up to 50,000 queries takes constant time.

## Worked Examples

### Sample 1

The relevant message structures are:

```
Test1:       tag 1, optional, string
Test2:       tag 1, optional, string
Test3:       tag 2, optional, string
Test4:       tag 1, required, string
StringMessage: tag 1, optional, string
Test5:       tag 1, optional, message StringMessage
```

The refinement state can be summarized as follows. The exact numeric class IDs depend on the order in which signatures are assigned, but equality between IDs is what matters.

| Iteration | Message | Signature shape | Class |
| --- | --- | --- | --- |
| Initial | Test1 | all messages initially equal | 0 |
| Initial | Test2 | all messages initially equal | 0 |
| Initial | Test3 | all messages initially equal | 0 |
| Initial | Test4 | all messages initially equal | 0 |
| Initial | StringMessage | all messages initially equal | 0 |
| Initial | Test5 | all messages initially equal | 0 |
| 1 | Test1 | `(1, optional, string)` | 0 |
| 1 | Test2 | `(1, optional, string)` | 0 |
| 1 | Test3 | `(2, optional, string)` | 1 |
| 1 | Test4 | `(1, required, string)` | 2 |
| 1 | StringMessage | `(1, optional, string)` | 0 |
| 1 | Test5 | `(1, optional, message, class(Test1))` | 3 |
| 2 | Test1 | unchanged | 0 |
| 2 | Test2 | unchanged | 0 |
| 2 | Test3 | unchanged | 1 |
| 2 | Test4 | unchanged | 2 |
| 2 | StringMessage | unchanged | 0 |
| 2 | Test5 | unchanged | 3 |

The queries consequently give `Test1` and `Test2` the same class, while `Test3`, `Test4`, and `Test5` each differ. The first query is compatible even though the field names are different, because names never occur in the signature.

### Sample 2

Here the nested structure is:

```
A -> B -> C
D -> E
C and E are empty
```

The refinement process behaves as follows.

| Iteration | Message | Field signature | Class |
| --- | --- | --- | --- |
| 1 | A | `(1, optional, message, 0)` | 0 |
| 1 | B | `(1, optional, message, 0)` | 0 |
| 1 | C | empty | 1 |
| 1 | D | `(1, optional, message, 0)` | 0 |
| 1 | E | empty | 1 |
| 2 | A | `(1, optional, message, 0)` | 0 |
| 2 | B | `(1, optional, message, 1)` | 1 |
| 2 | C | empty | 2 |
| 2 | D | `(1, optional, message, 1)` | 1 |
| 2 | E | empty | 2 |
| 3 | A | `(1, optional, message, 1)` | 0 |
| 3 | B | `(1, optional, message, 2)` | 1 |
| 3 | C | empty | 2 |
| 3 | D | `(1, optional, message, 2)` | 1 |
| 3 | E | empty | 2 |

`B` and `D` eventually receive the same class because both contain the same optional message field whose target is an empty message. `A` is different because its nested `B` is not equivalent to the empty message.

This gives the two requested answers:

```
B D
```

is compatible, while

```
A D
```

is incompatible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(M^2F + Q)) | At most (M-1) strict refinements, each scanning (M) messages and at most (F) fields, followed by constant-time queries |
| Space | (O(MF)) | The descriptor and one signature per message contain at most (MF) field entries |

With (M \le 1000) and (F \le 16), the preprocessing bound is at most on the order of 16 million field entries across all possible refinement iterations. The query phase handles 50,000 queries with only two array lookups per query, so the large query count does not change the asymptotic preprocessing cost.

## Test Cases

```python
import sys
import io

def solve_text(inp: str) -> str:
    data = inp.split()
    p = 0

    n = int(data[p])
    p += 1

    messages = []
    name_to_id = {}

    for _ in range(n):
        assert data[p] == "message"
        p += 1

        name = data[p]
        p += 1

        mid = len(messages)
        name_to_id[name] = mid
        messages.append([])

        assert data[p] == "{"
        p += 1

        while data[p] != "}":
            label = data[p]
            typ = data[p + 1]
            p += 2

            p += 1  # field name

            assert data[p] == "="
            p += 1

            tag = int(data[p])
            p += 1

            assert data[p] == ";"
            p += 1

            messages[mid].append((tag, label, typ))

        p += 1

    for i in range(len(messages)):
        converted = []

        for tag, label, typ in messages[i]:
            if typ == "double":
                converted.append((tag, label, 0, -1))
            elif typ == "string":
                converted.append((tag, label, 1, -1))
            else:
                converted.append((tag, label, 2, name_to_id[typ]))

        converted.sort()
        messages[i] = converted

    m = len(messages)
    cls = [0] * m

    while True:
        groups = {}
        new_cls = [0] * m

        for i in range(m):
            sig = []

            for tag, label, kind, target in messages[i]:
                if kind == 2:
                    sig.append((tag, label, kind, cls[target]))
                else:
                    sig.append((tag, label, kind))

            sig = tuple(sig)

            if sig not in groups:
                groups[sig] = len(groups)

            new_cls[i] = groups[sig]

        if new_cls == cls:
            break

        cls = new_cls

    q = int(data[p])
    p += 1

    ans = []

    for _ in range(q):
        a = data[p]
        b = data[p + 1]
        p += 2

        if cls[name_to_id[a]] == cls[name_to_id[b]]:
            ans.append("Wire-format compatible.")
        else:
            ans.append("Wire-format incompatible.")

    return "\n".join(ans)

def run(inp: str) -> str:
    return solve_text(inp)

sample1 = """18
message Test1 {
optional string field = 1 ;
}
message Test2 {
optional string field_string = 1 ;
}
message Test3 {
optional string field = 2 ;
}
message Test4 {
required string field = 1 ;
}
message StringMessage {
optional string field = 1 ;
}
message Test5 {
optional StringMessage field = 1 ;
}
4
Test1 Test2
Test1 Test3
Test1 Test4
Test1 Test5
"""

assert run(sample1) == """Wire-format compatible.
Wire-format incompatible.
Wire-format incompatible.
Wire-format incompatible.""", "sample 1"

sample2 = """5
message A { optional B nest = 1 ; }
message B { optional C nest = 1 ; }
message C { }
message D { optional E nest = 1 ; }
message E { }
2
B D
A D
"""

assert run(sample2) == """Wire-format compatible.
Wire-format incompatible.""", "sample 2"

sample3 = """1
message A { }
1
A A
"""

assert run(sample3) == """Wire-format compatible.""", "minimum empty message"

sample4 = """3
message A {
optional string x = 536870911 ;
}
message B {
optional string y = 536870911 ;
}
message C {
optional string z = 536870910 ;
}
3
A B
A C
B C
"""

assert run(sample4) == """Wire-format compatible.
Wire-format incompatible.
Wire-format incompatible.""", "maximum field number"

sample5 = """2
message A {
repeated string a = 1 ;
repeated string b = 2 ;
repeated string c = 3 ;
repeated string d = 4 ;
}
message B {
repeated string x = 1 ;
repeated string y = 2 ;
repeated string z = 3 ;
repeated string w = 4 ;
}
2
A B
A A
"""

assert run(sample5) == """Wire-format compatible.
Wire-format compatible.""", "all matching repeated fields"

# A larger generated case, close to the maximum number of messages.
parts = ["1000"]
for i in range(1000):
    parts.append(
        f"message M{i} {{ optional string value = 1 ; }}"
    )
parts.append("3")
parts.append("M0 M999")
parts.append("M123 M456")
parts.append("M0 M0")

large_input = "\n".join(parts) + "\n"

assert run(large_input) == """Wire-format compatible.
Wire-format compatible.
Wire-format compatible.""", "large descriptor"

# Recursive cycle case.
cycle_input = """3
message A { optional A next = 1 ; }
message B { optional C next = 1 ; }
message C { optional B next = 1 ; }
3
A B
A C
B C
"""

assert run(cycle_input) == """Wire-format compatible.
Wire-format compatible.
Wire-format compatible.""", "recursive cycles"
```

The minimum-size case checks that an empty descriptor body produces an ordinary message with an empty signature and that a message is always compatible with itself.

The maximum-tag case checks that the largest legal field number is treated as an ordinary integer and that changing it by one changes the wire-level field identity.

The all-repeated case checks that field names are ignored and that repeated rules remain compatible when the declarations use completely different names.

The generated 1,000-message case exercises the largest message-count dimension and verifies that preprocessing produces one class for all structurally identical messages.

The recursive cycle case checks the central reason for using iterative refinement rather than naive recursive expansion. The algorithm reaches a stable partition even though there is no finite expansion of the nested message definitions.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `message A { }`, query `A A` | Compatible | Empty message and minimum descriptor |
| Tags `536870911` versus `536870910` | Compatible, then incompatible | Maximum legal field number and tag sensitivity |
| Two messages with four repeated string fields | Compatible | Field names ignored and repeated rules preserved |
| 1,000 structurally equal messages | All queried pairs compatible | Maximum message count and preprocessing |
| Three mutually recursive messages | All three pairs compatible | Cyclic message references |

## Edge Cases

Different field names are handled by excluding the field name from every signature. For

```
message A { optional string first = 1 ; }
message B { optional string second = 1 ; }
```

both messages produce exactly the same signature, `(1, optional, string)`, so they enter the same class. The algorithm correctly follows the wire format rather than the descriptor's source-level names.

Different tags are handled directly by the first element of every field signature. For

```
message A { optional string value = 1 ; }
message B { optional string value = 2 ; }
```

the signatures are `(1, optional, string)` and `(2, optional, string)`. They are separated during the first refinement and can never become compatible later.

Different rules are similarly visible without looking inside nested messages. An optional field contributes `optional` to its signature, while a repeated field contributes `repeated`. Consequently

```
message A { optional string value = 1 ; }
message B { repeated string value = 1 ; }
```

are separated immediately. This avoids the common mistake of checking only tags and wire types while forgetting multiplicity.

A string and an embedded message both use wire type 2, but the signatures retain the distinction between `string` and `message`. A message field also carries the current class of its nested target. Thus a declaration such as

```
message Empty { }
message Holder { optional Empty value = 1 ; }
message Text { optional string value = 1 ; }
```

gives `Holder` a message-valued field and `Text` a string-valued field, so they receive different classes even though their wire type numbers are both 2.

Recursive definitions are handled without recursion in the Python implementation. For

```
message A { optional A next = 1 ; }
```

the first refinement sees the common shape `(1, optional, message, 0)`. Subsequent iterations continue to see the same target class, so the partition stabilizes. The algorithm never tries to construct an infinitely nested representation of `A`.

Mutually recursive definitions work for the same reason. In

```
message B { optional C next = 1 ; }
message C { optional B next = 1 ; }
```

both targets initially belong to the same class. Their signatures consequently remain equal, and the pair stays together through every refinement. The fixed point captures the recursive equivalence directly rather than requiring a special cycle-detection case.
