---
title: "GoPy"
description: "Specification series for gopy — a port of CPython's Python/ runtime to Go with 100% behavioural compatibility."
tags: ["gopy", "spec"]
weight: 1600
---

Port of CPython's `Python/` (and related `Objects/`, `Parser/`) runtime to Go. Each spec file maps directly to one or more CPython C source files and defines the Go package, types, and functions that replace them.

| # | Spec | Topic |
|---|---|---|
| 1600 | [1600_gopy_overview](1600_gopy_overview/) | gopy overview |
| 1601 | [1601_gopy_naming](1601_gopy_naming/) | gopy naming conventions |
| 1602 | [1602_gopy_filemap](1602_gopy_filemap/) | gopy file map |
| 1603 | [1603_gopy_roadmap](1603_gopy_roadmap/) | gopy roadmap |
| 1604 | [1604_gopy_arena](1604_gopy_arena/) | gopy arena spec |
| 1605 | [1605_gopy_pythread](1605_gopy_pythread/) | gopy pythread spec |
| 1606 | [1606_gopy_pysync](1606_gopy_pysync/) | gopy pysync spec |
| 1607 | [1607_gopy_hashsecret](1607_gopy_hashsecret/) | gopy hash secret spec |
| 1611 | [1611_gopy_errors](1611_gopy_errors/) | gopy errors |
| 1613 | [1613_gopy_gc](1613_gopy_gc/) | gopy gc, weakrefs, finalizers |
| 1620 | [1620_gopy_compile_pipeline](1620_gopy_compile_pipeline/) | gopy compile pipeline |
| 1621 | [1621_gopy_bytecodes_dsl](1621_gopy_bytecodes_dsl/) | gopy bytecodes DSL |
| 1622 | [1622_gopy_lifecycle](1622_gopy_lifecycle/) | gopy lifecycle |
| 1624 | [1624_gopy_pythonrun](1624_gopy_pythonrun/) | gopy pythonrun |
| 1625 | [1625_gopy_compile_testing](1625_gopy_compile_testing/) | gopy v0.5 testing strategy |
| 1626 | [1626_gopy_codegen](1626_gopy_codegen/) | gopy codegen |
| 1627 | [1627_gopy_flowgraph](1627_gopy_flowgraph/) | gopy flowgraph |
| 1628 | [1628_gopy_assemble](1628_gopy_assemble/) | gopy assemble |
| 1629 | [1629_gopy_compile_goldens](1629_gopy_compile_goldens/) | gopy compile golden tests |
| 1630 | [1630_gopy_vm_overview](1630_gopy_vm_overview/) | gopy vm overview |
| 1635 | [1635_gopy_intrinsics](1635_gopy_intrinsics/) | gopy intrinsics |
| 1636 | [1636_gopy_eval_loop](1636_gopy_eval_loop/) | gopy eval loop |
| 1637 | [1637_gopy_frame](1637_gopy_frame/) | gopy frame |
| 1638 | [1638_gopy_stackref](1638_gopy_stackref/) | gopy stackref |
| 1639 | [1639_gopy_eval_gil](1639_gopy_eval_gil/) | gopy eval GIL |
| 1640 | [1640_gopy_parser_overview](1640_gopy_parser_overview/) | gopy parser overview |
| 1641 | [1641_gopy_lexer_tokenizer](1641_gopy_lexer_tokenizer/) | gopy lexer tokenizer |
| 1642 | [1642_gopy_pegen](1642_gopy_pegen/) | gopy pegen |
| 1643 | [1643_gopy_parser_errors](1643_gopy_parser_errors/) | gopy parser errors |
| 1644 | [1644_gopy_string_parser](1644_gopy_string_parser/) | gopy string parser |
| 1645 | [1645_gopy_myreadline](1645_gopy_myreadline/) | gopy myreadline |
| 1651 | [1651_gopy_modules](1651_gopy_modules/) | gopy modules |
| 1660 | [1660_gopy_strings_numbers](1660_gopy_strings_numbers/) | gopy strings and numbers |
| 1661 | [1661_gopy_hash](1661_gopy_hash/) | gopy hash |
| 1662 | [1662_gopy_hamt](1662_gopy_hamt/) | gopy HAMT |
| 1663 | [1663_gopy_context](1663_gopy_context/) | gopy context |
| 1664 | [1664_gopy_time](1664_gopy_time/) | gopy time |
| 1665 | [1665_gopy_tokenize](1665_gopy_tokenize/) | gopy tokenize |
| 1668 | [1668_gopy_runtime_helpers](1668_gopy_runtime_helpers/) | gopy runtime helpers |
| 1670 | [1670_gopy_objects_overview](1670_gopy_objects_overview/) | gopy objects overview |
| 1671 | [1671_gopy_object_protocol](1671_gopy_object_protocol/) | gopy object protocol |
| 1672 | [1672_gopy_type](1672_gopy_type/) | gopy type |
| 1673 | [1673_gopy_long](1673_gopy_long/) | gopy long |
| 1674 | [1674_gopy_float_complex](1674_gopy_float_complex/) | gopy float complex |
| 1675 | [1675_gopy_bool_none](1675_gopy_bool_none/) | gopy bool none |
| 1676 | [1676_gopy_bytes](1676_gopy_bytes/) | gopy bytes |
| 1677 | [1677_gopy_unicode](1677_gopy_unicode/) | gopy unicode |
| 1678 | [1678_gopy_tuple](1678_gopy_tuple/) | gopy tuple |
| 1679 | [1679_gopy_list](1679_gopy_list/) | gopy list |
| 1680 | [1680_gopy_dict](1680_gopy_dict/) | gopy dict |
| 1681 | [1681_gopy_set](1681_gopy_set/) | gopy set |
| 1682 | [1682_gopy_slice_range](1682_gopy_slice_range/) | gopy slice range |
| 1683 | [1683_gopy_abstract](1683_gopy_abstract/) | gopy abstract |
| 1684 | [1684_gopy_call](1684_gopy_call/) | gopy call |
| 1685 | [1685_gopy_descr_method](1685_gopy_descr_method/) | gopy descr method |
| 1686 | [1686_gopy_exceptions](1686_gopy_exceptions/) | gopy exceptions |
| 1687 | [1687_gopy_code_frame_gen](1687_gopy_code_frame_gen/) | gopy code frame gen |
| 1688 | [1688_gopy_module_misc](1688_gopy_module_misc/) | gopy module misc |
| 1689 | [1689_gopy_obj_misc](1689_gopy_obj_misc/) | gopy obj misc |
| 1690 | [1690_gopy_marshal](1690_gopy_marshal/) | gopy marshal |
| 1691 | [1691_gopy_import](1691_gopy_import/) | gopy import |
| 1692 | [1692_gopy_codecs](1692_gopy_codecs/) | gopy codecs |
| 1693 | [1693_gopy_vm_remaining](1693_gopy_vm_remaining/) | gopy vm remaining |
