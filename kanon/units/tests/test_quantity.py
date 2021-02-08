import pytest
from astropy.units import Quantity, arcminute, degree

from histropy.units.radices import BasedQuantity, Sexagesimal


class TestQuantity:
    def test_init_basedquantity(self):
        q = Sexagesimal(1) * degree
        assert isinstance(q, BasedQuantity)
        assert q.unit == degree
        assert q.value.equals(Sexagesimal(1))
        q = Sexagesimal(1) / degree
        assert isinstance(q, BasedQuantity)
        assert q.unit == 1 / degree
        assert q.value.equals(Sexagesimal(1))

        assert type(BasedQuantity(1, degree)) is Quantity

    def test_attribute_forwarding(self):
        q = Sexagesimal("1;0,1,31") * degree

        with pytest.raises(AttributeError):
            q._from_string()
        with pytest.raises(AttributeError):
            q.does_not_exist()

        assert q.truncate(2).value.equals(q.value.truncate(2))
        assert q.left == (1,)

        assert round(q, 2).value.equals(round(q.value, 2))

    def test_shifting(self):
        q = Sexagesimal("1;0,1,31") * degree

        assert (q << 2).value.equals(q.value << 2)
        assert (q >> 2).value.equals(q.value >> 2)

        arcmq = q << 1 * arcminute
        assert arcmq.unit == arcminute
        assert arcmq.value.equals(Sexagesimal("1,0;1,31,0"))

        with pytest.raises(TypeError):
            q >> 1 * arcminute