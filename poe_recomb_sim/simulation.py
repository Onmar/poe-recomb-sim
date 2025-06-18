from collections import defaultdict
import math
from .model import AffixBag, Item, PrefixBag, SuffixBag


# AFFIX_CHANCES[Total affixes, new affixes] = chance
AFFIX_CHANCES = (
    #0mod  1mod  2mod  3mod
    (1.00, 0.00, 0.00, 0.00),  # 0 affixes
    (0.41, 0.59, 0.00, 0.00),  # 1 affix
    (0.00, 0.67, 0.33, 0.00),  # 2 affixes
    (0.00, 0.39, 0.52, 0.10),  # 3 affixes
    (0.00, 0.11, 0.59, 0.31),  # 4 affixes
    (0.00, 0.00, 0.43, 0.57),  # 5 affixes
    (0.00, 0.00, 0.28, 0.72),  # 6 affixes
)


def simulate_recombinator_outcomes(item1: Item, item2: Item, base_matters: bool):
    all_prefixes = item1.prefixes + item2.prefixes
    all_suffixes = item1.suffixes + item2.suffixes

    print(f"Item 1: {item1}")
    print(f"Item 2: {item2}")
    print(f"Total: {len(all_prefixes)}TP/{len(all_suffixes)}TS")
    print("")

    bases = step_make_base(item1, item2)
    if not base_matters:
        print(f"Ilvl: {', '.join(f"{base.base_name}[{base.ilvl}]" for base in bases)}")
        bases = { Item("X", 100): 1.0 }

    for base, base_chance in bases.items():
        possible_items = step_make_affixes(base, all_prefixes, all_suffixes)
        for item, item_chance in possible_items.items():
            print(f"{base_chance * item_chance * 100.0: >5.02f}%: {item}")
        print("")


def calc_ilvl(ilvl1: int, ilvl2: int):
    return math.floor(min((ilvl1 + ilvl2) / 2 + 2, max(ilvl1, ilvl2)))


def step_make_base(item1: Item, item2: Item) -> dict[Item, float]:
    new_ilvl = calc_ilvl(item1.ilvl, item2.ilvl)
    return {
        Item(item1.base_name, new_ilvl, prefix_limit=item1.prefix_limit, suffix_limit=item1.suffix_limit): 0.5,
        Item(item2.base_name, new_ilvl, prefix_limit=item2.prefix_limit, suffix_limit=item2.suffix_limit): 0.5,
    }


def step_make_affixes(base: Item, prefixes: PrefixBag, suffixes: SuffixBag) -> dict[Item, float]:
    final_items: defaultdict[Item, float] = defaultdict(lambda: 0.0)

    # Prefixes first
    pre_first_affixes: dict[tuple[PrefixBag, SuffixBag], float] = select_affixes(prefixes, suffixes)
    for (prefix_sel, suffix_sel), chance in pre_first_affixes.items():
        item = Item(base.base_name, base.ilvl, prefix_sel, suffix_sel, base.prefix_limit, base.suffix_limit)
        final_items[item] += 0.5 * chance
    
    # Suffixes first
    suf_first_affixes: dict[tuple[SuffixBag, PrefixBag], float] = select_affixes(suffixes, prefixes)
    for (suffix_sel, prefix_sel), chance in suf_first_affixes.items():
        item = Item(base.base_name, base.ilvl, prefix_sel, suffix_sel, base.prefix_limit, base.suffix_limit)
        final_items[item] += 0.5 * chance
    
    return final_items


def select_affixes[T1: AffixBag, T2: AffixBag](first_affixes: T1, second_affixes: T2) -> dict[tuple[T1, T2], float]:
    # First affixes
    first_selections: defaultdict[T1, float] = defaultdict(lambda: 0.0)
    count_chances = AFFIX_CHANCES[len(first_affixes)]
    for i in range(4):
        count_chance = count_chances[i]
        if count_chance == 0.0:
            continue
        possible_affixes = first_affixes
        affix_selections = make_affix_selections(i, possible_affixes)
        for affix_sel, affix_chance in affix_selections.items():
            first_selections[affix_sel] += count_chance * affix_chance

    # Second affixes
    second_selections: defaultdict[tuple[T1, T2], float] = defaultdict(lambda: 0.0)
    count_chances = AFFIX_CHANCES[len(second_affixes)]
    for i in range(4):
        count_chance = count_chances[i]
        if count_chance == 0.0:
            continue
        for first_affixes, first_chance in first_selections.items():
            possible_affixes = second_affixes
            if first_affixes.has_exclusive():
                possible_affixes = possible_affixes.filter(lambda aff: not aff.exclusive)
            affix_selections = make_affix_selections(i, possible_affixes)
            for affix_sel, affix_chance in affix_selections.items():
                second_selections[(first_affixes, affix_sel)] += first_chance * count_chance * affix_chance
    
    return second_selections


def make_affix_selections[T: AffixBag](count: int, affixes: T) -> dict[T, float]:
    if count == 0 or len(affixes) == 0:
        return {type(affixes)([]): 1.0}
    
    if count == 1:
        retval = defaultdict(lambda: 0.0)
        for a in affixes:
            retval[type(affixes)([a])] += 1.0 / len(affixes)
        return retval

    # Multiple Affixes remaining
    retval = defaultdict(lambda: 0.0)
    for affix in affixes:
        remaining_affixes = affixes - type(affixes)([affix])
        if affix.exclusive:
            remaining_affixes = remaining_affixes.filter(lambda aff: not aff.exclusive)
        next_sel = make_affix_selections(count - 1, remaining_affixes)
        for bag, chance in next_sel.items():
            total_bag = type(affixes)([affix]) + bag
            retval[total_bag] += chance / len(affixes)
    return retval
