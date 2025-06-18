import pytest
from poe_recomb_sim.model import Affix, AffixBag, Prefix, Suffix
from poe_recomb_sim.simulation import *


def test_make_affix_selection():
    sel = make_affix_selections(2, AffixBag([
        Affix(desired=True),
        Affix(),
    ]))
    assert sel == pytest.approx({
        AffixBag([
            Affix(desired=True),
            Affix(),
        ]): 1,
    })

    sel = make_affix_selections(2, AffixBag([
        Affix(desired=True),
        Affix(),
        Affix(),
    ]))
    assert sel == pytest.approx({
        AffixBag([
            Affix(desired=True),
            Affix(),
        ]): 2/3,
        AffixBag([
            Affix(),
            Affix(),
        ]): 1/3,
    })

    sel = make_affix_selections(2, AffixBag([
        Affix(desired=True),
        Affix(),
        Affix(exclusive=True),
    ]))
    assert sel == pytest.approx({
        AffixBag([
            Affix(desired=True),
            Affix(exclusive=True),
        ]): 1/3,
        AffixBag([
            Affix(),
            Affix(exclusive=True),
        ]): 1/3,
        AffixBag([
            Affix(),
            Affix(desired=True),
        ]): 1/3,
    })

    sel = make_affix_selections(2, AffixBag([]))
    assert sel == pytest.approx({
        AffixBag([]): 1,
    })


def test_select_affixes():
    first_affixes = AffixBag([
        Affix(),
        Affix(exclusive=True),
    ])
    second_affixes = AffixBag([
        Affix(),
        Affix(exclusive=True),
    ])
    expected = {
        (
            AffixBag([
                Affix(),
                Affix(exclusive=True),
            ]),
            AffixBag([
                Affix(),
            ]),
        ): 0.33,
        (
            AffixBag([
                Affix(),
            ]),
            AffixBag([
                Affix(),
            ]),
        ): 0.67 * 0.5 * 0.67 * 0.5,
        (
            AffixBag([
                Affix(),
            ]),
            AffixBag([
                Affix(exclusive=True),
            ]),
        ): 0.67 * 0.5 * 0.67 * 0.5,
        (
            AffixBag([
                Affix(),
            ]),
            AffixBag([
                Affix(),
                Affix(exclusive=True),
            ]),
        ): 0.67 * 0.5 * 0.33,
        (
            AffixBag([
                Affix(exclusive=True),
            ]),
            AffixBag([
                Affix(),
            ]),
        ): 0.67 * 0.5,
    }

    selected = select_affixes(first_affixes, second_affixes)

    assert selected == pytest.approx(expected)

def test_debug():
    item1 = Item(
        base_name="A", 
        ilvl=84, 
        prefixes=PrefixBag([
            Prefix(desired=False, exclusive=True), 
            Prefix(desired=False, exclusive=True), 
            # Prefix(desired=False, exclusive=False),
        ]), 
        suffixes=SuffixBag([
            Suffix(desired=True, exclusive=False), 
            Suffix(desired=True, exclusive=False), 
            Suffix(desired=False, exclusive=True),
        ]),
        prefix_limit=3,
        suffix_limit=3,
    )
    item2 = Item(
        base_name="B", 
        ilvl=86, 
        prefixes=PrefixBag([
            Prefix(desired=True, exclusive=False), 
            Prefix(desired=True, exclusive=False), 
            Prefix(desired=False, exclusive=True),
        ]), 
        suffixes=SuffixBag([
            Suffix(desired=False, exclusive=True), 
            Suffix(desired=False, exclusive=True), 
            # Suffix(desired=False, exclusive=False),
        ]),
        prefix_limit=3,
        suffix_limit=3,
    )
    simulate_recombinator_outcomes(item1, item2, False)
