import collections
import collections.abc
from dataclasses import dataclass, field
import itertools
from typing import Any, Callable, Generator, Iterable, Self, overload


@dataclass(frozen=True)
class Affix:
    name: str = ""
    desired: bool = False
    exclusive: bool = False


class AffixBag[T: Affix = Affix](collections.abc.Iterable[T]):
    _affixes: collections.Counter[T]


    @overload
    def __init__(self, affixes: collections.Counter[T]):
        ...

    @overload
    def __init__(self, affixes: Iterable[T]):
        ...

    def __init__(self, affixes):
        if isinstance(affixes, collections.Counter):
            self._affixes = affixes
        else:
            self._affixes = +collections.Counter[T](affixes)
    
    def filter(self, function: Callable[[T], bool]) -> Self:
        return type(self)(filter(function, self))
    
    def __add__(self, value: object) -> Self:
        if isinstance(value, type(self)):
            return type(self)(self._affixes + value._affixes)
        raise NotImplemented
    
    def __sub__(self, value: object) -> Self:
        if isinstance(value, type(self)):
            return type(self)(+(self._affixes - value._affixes))
        raise NotImplemented
    
    def has_exclusive(self) -> bool:
        return any(map(lambda aff: aff.exclusive, self))

    def __iter__(self) -> Generator[T, Any, None]:
        for affix in self._affixes.keys():
            for x in range(self._affixes[affix]):
                yield affix

    def __len__(self) -> int:
        return sum(self._affixes.values())
        
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, type(self)):
            return False
        return self._affixes == value._affixes
    
    def __hash__(self) -> int:
        return hash(frozenset(self._affixes.items()))

    def affix_string(self, desired_id: str = "D", extra_id: str = "e") -> str:
        desired_count = sum(x.desired for x in self)
        extra_count = sum(not x.desired for x in self)
        desired_string = f"{desired_count}{desired_id}"
        extra_string = f"{extra_count}{extra_id}" if extra_count != 0 else ""
        return f"{desired_string}{extra_string}"
    
    def __repr__(self) -> str:
        return f"[{', '.join(repr(aff) for aff in self)}]"
    
    def __str__(self) -> str:
        return self.affix_string()
    
    def __format__(self, format_spec: str) -> str:
        if format_spec == "":
            return self.affix_string()
        
        ids = format_spec.split(",")
        desired_id = ids[0]

        if len(ids) == 1:
            return self.affix_string(desired_id)
        
        extra_id = ids[1]
        return self.affix_string(desired_id, extra_id)


@dataclass(frozen=True)
class Prefix(Affix):
    pass


class PrefixBag(AffixBag[Prefix]):
    pass


@dataclass(frozen=True)
class Suffix(Affix):
    pass


class SuffixBag(AffixBag[Suffix]):
    pass


def make_prefix_suffix_string(prefixes: PrefixBag, suffixes: SuffixBag) -> str:
    return f"{prefixes.affix_string(desired_id="p")}/{suffixes.affix_string(desired_id="s")}"


@dataclass(frozen=True)
class Item:
    base_name: str
    ilvl: int
    prefixes: PrefixBag = field(default_factory=lambda: PrefixBag([]))
    suffixes: SuffixBag = field(default_factory=lambda: SuffixBag([]))
    prefix_limit: int = 3
    suffix_limit: int = 3

    def __post_init__(self):
        if len(self.prefixes) > self.prefix_limit:
            raise ValueError("Illegal Item! (Too many prefixes)")
        if len(self.suffixes) > self.suffix_limit:
            raise ValueError("Illegal Item! (Too many suffixes)")
        
    def has_exclusive(self) -> bool:
        return any(map(lambda a: a.exclusive, self.prefixes)) or any(map(lambda a: a.exclusive, self.suffixes))

    def __str__(self) -> str:
        return f"{make_prefix_suffix_string(self.prefixes, self.suffixes)} ({self.base_name}[{self.ilvl}])"

    def __format__(self, format_spec: str) -> str:
        return str(self)
    
    def replace_prefixes(self, new_prefixes: PrefixBag) -> Self:
        return type(self)(self.base_name, self.ilvl, prefixes=new_prefixes, suffixes=self.suffixes, prefix_limit=self.prefix_limit, suffix_limit=self.suffix_limit)
    
    def replace_suffixes(self, new_suffixes: SuffixBag) -> Self:
        return type(self)(self.base_name, self.ilvl, prefixes=self.prefixes, suffixes=new_suffixes, prefix_limit=self.prefix_limit, suffix_limit=self.suffix_limit)
