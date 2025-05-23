import math

class Value:
    """Represents a modifiable numeric value with base, multiplicative, and flat modifiers.

    The effective value is calculated as:
    (base_value + sum(base_modifiers)) * product(mult_modifiers) + sum(flat_modifiers)
    """
    
    def __init__(self, value=None, base=None, mult=None, flat=None, transform=lambda x: x):
        """Initialize a Value instance from a number, existing Value, or None."""
        self.transform = transform
        if isinstance(value, (int, float)):
            self._from_number(value, base, mult, flat)
        elif isinstance(value, Value):
            self._from_Value(value)
        elif value is None:
            self._from_number(0, base, mult, flat)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")
    
    def _from_number(self, value, base, mult, flat):
        """Initialize from a numeric value with optional modifiers."""
        self.value = value
        self.base = base.copy() if base else []
        self.mult = mult.copy() if mult else []
        self.flat = flat.copy() if flat else []
    
    def _from_Value(self, other):
        """Copy initialization from another Value instance."""
        self.value = other.value
        self.base = other.base.copy()
        self.mult = other.mult.copy()
        self.flat = other.flat.copy()
    
    def add_mod(self, base=None, mult=None, flat=None) -> None:
        """Add multiple modifiers in one call."""
        if base is not None:
            self.add_base(base)
        if mult is not None:
            self.add_mult(mult)
        if flat is not None:
            self.add_flat(flat)
    
    def add_base(self, modifier: float) -> None:
        """Add a base additive modifier."""
        self.base.append(modifier)
    
    def add_mult(self, modifier: float) -> None:
        """Add a multiplicative modifier."""
        self.mult.append(modifier)

    def add_flat(self, modifier: float) -> None:
        """Add a flat additive modifier."""
        self.flat.append(modifier)
    
    def _get_comparable(self, other) -> float:
        """Convert supported types to float for comparison."""
        if isinstance(other, Value):
            return float(other)
        if isinstance(other, (int, float)):
            return float(other)
        raise TypeError(f"Comparison with type {type(other)} not supported")
    
    # Comparison operators
    def __eq__(self, other) -> bool:
        try:
            return float(self) == self._get_comparable(other)
        except TypeError:
            return False

    def __ne__(self, other) -> bool:
        try:
            return float(self) != self._get_comparable(other)
        except TypeError:
            return True

    def __lt__(self, other) -> bool:
        return float(self) < self._get_comparable(other)

    def __le__(self, other) -> bool:
        return float(self) <= self._get_comparable(other)

    def __gt__(self, other) -> bool:
        return float(self) > self._get_comparable(other)

    def __ge__(self, other) -> bool:
        return float(self) >= self._get_comparable(other)
    
    # Arithmetic operators (existing)
    def __add__(self, other) -> float:
        """Add this Value to another numeric value."""
        return self.transform(float(self) + float(other))

    def __radd__(self, other) -> float:
        """Handle right-side addition."""
        return self.transform(self.__add__(other))

    def __sub__(self, other) -> float:
        """Subtract another numeric value from this Value."""
        return self.transform(float(self) - float(other))

    def __rsub__(self, other) -> float:
        """Handle right-side subtraction."""
        return self.transform(float(other) - float(self))

    def __float__(self) -> float:
        """Calculate the effective float value."""
        base_sum = self.value + sum(self.base)
        mult_product = math.prod(self.mult) if self.mult else 1.0
        flat_sum = sum(self.flat)
        return float(base_sum * mult_product + flat_sum)

    def __int__(self) -> int:
        """Get the effective value as integer."""
        return int(float(self))

    def __bool__(self) -> bool:
        """Boolean evaluation of the effective value."""
        return bool(float(self))
    
    def __repr__(self) -> str:
        """Developer-friendly string representation."""
        base = f"({self.value} + {sum(self.base)})" if self.base else str(self.value)
        mult = f" * {math.prod(self.mult)}" if self.mult else ""
        flat = f" + {sum(self.flat)}" if self.flat else ""
        return f"Value<{base}{mult}{flat}>"