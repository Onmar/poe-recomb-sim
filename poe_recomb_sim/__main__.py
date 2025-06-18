from .model import Item, Prefix, PrefixBag, Suffix, SuffixBag
from .simulation import simulate_recombinator_outcomes


def main():
    item1 = Item(
        base_name="A", 
        ilvl=84, 
        prefixes=PrefixBag([
            Prefix(desired=False, exclusive=True),  # Crafted Named
            Prefix(desired=False, exclusive=True),  # Crafted Named
            # Prefix(desired=False, exclusive=False),  # Not possible
        ]), 
        suffixes=SuffixBag([
            Suffix(desired=True, exclusive=False), 
            Suffix(desired=True, exclusive=False), 
            Suffix(desired=False, exclusive=True),  # Multimod
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
            Prefix(desired=False, exclusive=True),  # Crafted Named
        ]), 
        suffixes=SuffixBag([
            Suffix(desired=False, exclusive=True),  # Multimod
            Suffix(desired=False, exclusive=True),  # Crafted Named
            # Suffix(desired=False, exclusive=True),  # Aspect
        ]),
        prefix_limit=3,
        suffix_limit=3,
    )
    base_matters = False

    simulate_recombinator_outcomes(item1, item2, base_matters)


if __name__ == "__main__":
    main()
