"""Unit tests for legacy CloudLink schema mapping; no network/credentials."""
import pytest
from pydantic import ValidationError
from legacy_schema import LegacyRequest, normalize_legacy_request

@pytest.mark.parametrize("source,expected",[("net","network"),("cctv","cctv"),("access","access")])
def test_supported_mapping(source,expected):
    value=normalize_legacy_request(LegacyRequest(categoryId=source,region="台南市",
      description="虛構多據點 AP、監控與門禁設備維護需求。"))
    assert value["category"]==expected

@pytest.mark.parametrize("unsupported",["weak","info","pc","__proto__"])
def test_unsupported_rejected(unsupported):
    with pytest.raises(ValidationError):
        LegacyRequest(categoryId=unsupported,region="台南市",
          description="虛構企業設備維護案件，不含個資。")
