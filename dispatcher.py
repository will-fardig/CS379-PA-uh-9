"""
PA 8: The VTable Dispatcher -- starter.

Complete VTable, build_vtable, USIObject, and dispatch below. See
PA_08_The_VTable_Dispatcher.md, Part B, for the full requirements.

Each table entry follows PA 7's Closure.call(args, caller_env) interface.
The harness supplies small closure-like methods so it can test dispatch
without adding string literals to the earlier interpreter grammar. Your
dispatch implementation must invoke .call with the receiver as the first
argument, followed by the explicit method arguments.
"""

from typing import Dict, Optional, Protocol


class MethodLike(Protocol):
    def call(self, args: list, caller_env) -> object:
        """PA 7 Closure-compatible call interface."""


class ClassDecl:
    """Given: a minimal class declaration -- just a name and its own (non-inherited) methods."""

    __slots__ = ("name", "methods")

    def __init__(self, name: str, methods: Dict[str, MethodLike]) -> None:
        self.name = name
        self.methods = methods


class VTable:
    def __init__(self, entries: Dict[str, MethodLike], owning_class_name: str = "?") -> None:
        """`owning_class_name` is just for error messages -- store it alongside entries."""
        self.entries: Dict[str, MethodLike] = dict(entries)
        self.owning_class_name = owning_class_name

    def resolve(self, method_name: str) -> MethodLike:
        """
        Return the method object bound to `method_name`. Raise a clear
        error (e.g. AttributeError) whose message names BOTH the
        owning class and the missing method if it doesn't exist.
        """
        try:
            return self.entries[method_name]
        except KeyError:
            raise AttributeError(
                f"class '{self.owning_class_name}' has no method '{method_name}' "
                f"(not declared on it or on any ancestor)"
            ) from None

    def __repr__(self) -> str:
        return f"VTable({self.owning_class_name}: {sorted(self.entries)})"


def build_vtable(class_node: ClassDecl, parent_vtable: Optional[VTable] = None) -> VTable:
    """
    Start from a copy of parent_vtable's entries (inherited methods),
    then overwrite only the slots class_node itself redeclares. A
    method class_node does NOT override must resolve to the EXACT SAME
    method object the parent uses -- don't wrap or duplicate it.
    Pass class_node.name as the new VTable's owning_class_name.
    """
    entries: Dict[str, MethodLike] = dict(parent_vtable.entries) if parent_vtable is not None else {}
    for name, method in class_node.methods.items():
        entries[name] = method
    return VTable(entries, class_node.name)


class USIObject:
    def __init__(self, class_descriptor: VTable, fields: dict) -> None:
        self.class_descriptor = class_descriptor
        self.fields = fields

    @property
    def class_name(self) -> str:
        return self.class_descriptor.owning_class_name

    def __repr__(self) -> str:
        return f"<{self.class_name} object fields={self.fields}>"


def dispatch(obj: USIObject, method_name: str, args: list, caller_env) -> object:
    """
    Resolve method_name through obj's OWN VTable (never a declared/
    static type), then call the resolved method via PA 7's interface:
    resolved_method.call([obj, *args], caller_env).
    """
    if not isinstance(obj, USIObject):
        raise TypeError(
            f"cannot call method '{method_name}' on non-object value {obj!r}"
        )
    method = obj.class_descriptor.resolve(method_name)
    return method.call([obj, *args], caller_env)