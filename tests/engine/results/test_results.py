import json
from typing import Union

import pytest

from prefect.engine.results import ConstantResult, PrefectResult
from prefect.tasks.core.constants import Constant


class TestConstantResult:
    def test_instantiates_with_value(self):
        constant_result = ConstantResult(5)
        assert constant_result.value == 5

        constant_result = ConstantResult(value=10)
        assert constant_result.value == 10

    def test_read_returns_self(self):
        constant_result = ConstantResult("hello world")
        assert constant_result.read("this param isn't used") is constant_result

    def test_write_doesnt_write_new_value(self):
        constant_result = ConstantResult("untouchable!")

        with pytest.raises(ValueError):
            constant_result.write("nvm")

    def test_write_returns_value(self):
        constant_result = ConstantResult("constant value")

        output = constant_result.write("constant value")
        assert output is output

    def test_handles_none_as_constant(self):
        constant_result = ConstantResult(None)
        assert constant_result.read("still not used") is constant_result
        output = constant_result.write(None)
        assert output is output

    @pytest.mark.parametrize(
        "constant_value", [3, "text", 5.0, Constant(3), Constant("text"), Constant(5.0)]
    )
    def test_exists(self, constant_value: Union[str, Constant]):

        result = ConstantResult(constant_value)
        result_exists = result.exists("")

        assert result_exists is True


class TestPrefectResult:
    def test_instantiates_with_value(self):
        result = PrefectResult(5)
        assert result.value == 5
        assert result.filepath == ""

        result = PrefectResult(value=10)
        assert result.value == 10
        assert result.filepath == ""

    def test_read_returns_new_result(self):
        result = PrefectResult("hello world")
        res = result.read('"bl00p"')

        assert res.filepath == '"bl00p"'
        assert res.value == "bl00p"
        assert result.value == "hello world"

    def test_write_doesnt_overwrite_value(self):
        result = PrefectResult(42)

        new_result = result.write(99)

        assert result.value == 42
        assert result.filepath == ""

        assert new_result.value == 99
        assert new_result.filepath == "99"

    @pytest.mark.parametrize(
        "value", [42, [0, 1], "x,y", (9, 10), dict(x=[55], y=None)]
    )
    def test_exists_for_json_objs(self, value):
        result = PrefectResult()
        assert result.exists(json.dumps(value)) is True
        assert result.exists(value) is False
