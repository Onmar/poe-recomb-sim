from typing import Any

import pytest

from poe_recomb_sim import *


affix_testdata = [
    (AffixBag([Affix(desired=True), Affix(desired=True), Affix()]), {}, "2D1e"),
    (AffixBag([Affix(), Affix(desired=True), Affix()]), {}, "1D2e"),
    (AffixBag([Affix(desired=True)]), {}, "1D"),
    (AffixBag([Affix(desired=True), Affix(desired=True)]), {}, "2D"),
    (AffixBag([Affix()]), {}, "0D1e"),
    (AffixBag([]), {}, "0D"),
    (AffixBag([Affix(desired=True), Affix(desired=True), Affix()]), { "desired_id": "s", "extra_id": "asd" }, "2s1asd"),
]


@pytest.mark.parametrize("affixes,kwargs,expected", affix_testdata)
def test_affix_string(affixes: AffixBag, kwargs: dict[str, Any], expected: str):
    assert affixes.affix_string(**kwargs) == expected

    if len(kwargs) == 0:
        assert f"{affixes}" == expected

    if len(kwargs) > 0:
        assert f"{affixes:{kwargs["desired_id"]},{kwargs["extra_id"]}}"


pre_suf_testdata = [
    (PrefixBag([Prefix(desired=True)]), SuffixBag([Suffix(desired=True)]), "1p/1s"),
    (PrefixBag([Prefix(desired=True)]), SuffixBag([]), "1p/0s"),
    (PrefixBag([]), SuffixBag([Suffix(desired=True)]), "0p/1s"),
    (PrefixBag([Prefix(desired=True), Prefix(desired=True), Prefix()]), SuffixBag([Suffix(desired=True), Suffix(desired=True), Suffix(desired=True)]), "2p1e/3s"),
    (PrefixBag([Prefix(desired=True), Prefix(), Prefix()]), SuffixBag([Suffix(desired=True)]), "1p2e/1s"),
    (PrefixBag([]), SuffixBag([]), "0p/0s"),
]


@pytest.mark.parametrize("prefixes,suffixes,expected", pre_suf_testdata)
def test_prefix_suffix_string(prefixes, suffixes, expected):
    assert make_prefix_suffix_string(prefixes, suffixes) == expected


def test_affix_bag_base():
    bag1 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
    ])
    bag2 = AffixBag([
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(),
    ])

    assert bag1 == bag2
    assert hash(bag1) == hash(bag2)
    assert str(bag1) == str(bag2)


def test_affix_bag_filter():
    bag1 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
    ])
    expected = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
    ])
    assert bag1.filter(lambda aff: not aff.exclusive) == expected


def test_affix_bag_math():
    bag1 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
    ])
    bag2 = AffixBag([
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(),
    ])
    bag3 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(),
    ])

    assert bag1 + bag2 == bag3
    assert bag1 - bag2 == AffixBag([])
    assert bag3 - bag1 == bag2
    assert bag3 - bag2 == bag1

def test_affix_bag_iadd():
    bag1 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
    ])
    bag2 = AffixBag([
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(),
    ])
    bag3 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
        Affix(),
    ])

    bag1 += bag2
    assert bag1 == bag3

def test_affix_bag_isub():
    bag1 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
    ])
    bag2 = AffixBag([
        Affix(desired=True, exclusive=False),
    ])
    bag3 = AffixBag([
        Affix(desired=True, exclusive=True),
        Affix(),
    ])

    bag1 -= bag2
    assert bag1 == bag3

    bag1 = AffixBag([
        Affix(),
        Affix(desired=True, exclusive=False),
        Affix(desired=True, exclusive=True),
    ])
    bag2 = AffixBag([
        Affix(desired=True, exclusive=False),
    ])
    bag3 = AffixBag([])

    bag2 -= bag1
    assert bag2 == bag3


item_testdata = [
    (Item("base1", 50, PrefixBag([]), SuffixBag([])), "0p/0s (base1[50])"),
    (Item("base2", 60, PrefixBag([Prefix()]), SuffixBag([Suffix()])), "0p1e/0s1e (base2[60])"),
    (Item("base3", 75, PrefixBag([Prefix(desired=True)]), SuffixBag([Suffix(desired=True)])), "1p/1s (base3[75])"),
]

@pytest.mark.parametrize("item,expected", item_testdata)
def test_item_string(item: Item, expected: str):
    assert str(item) == expected
    assert f"{item}" == expected
