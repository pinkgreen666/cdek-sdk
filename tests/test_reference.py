"""Tests for reference data."""
import pytest
from cdek.reference import (
    get_service,
    list_services,
    get_packaging_services,
    suggest_box,
    get_order_type,
    list_order_types,
    get_additional_type,
    list_additional_types,
)
from cdek.reference.services import SERVICES


def test_services_loaded():
    """Test that services are loaded."""
    assert len(SERVICES) > 0
    assert "INSURANCE" in SERVICES
    assert "TRYING_ON" in SERVICES


def test_get_service():
    """Test getting service by code."""
    service = get_service("INSURANCE")
    assert service is not None
    assert service.code == "INSURANCE"
    assert service.name == "СТРАХОВАНИЕ"
    assert service.auto_added is True


def test_get_service_not_found():
    """Test getting non-existent service."""
    service = get_service("NON_EXISTENT")
    assert service is None


def test_list_services_no_filter():
    """Test listing all services."""
    services = list_services()
    assert len(services) > 0


def test_list_services_by_mode():
    """Test filtering services by delivery mode."""
    services = list_services(mode="warehouse-door")
    assert len(services) > 0

    # Check that filtered services either have no mode restriction or include the mode
    for service in services:
        if service.modes is not None:
            assert "warehouse-door" in service.modes


def test_list_services_by_weight():
    """Test filtering services by weight."""
    services = list_services(max_weight=5.0)

    # Check that all services with weight_limit can handle 5kg
    for service in services:
        if service.weight_limit is not None:
            assert service.weight_limit >= 5.0


def test_get_packaging_services():
    """Test getting packaging services."""
    services = get_packaging_services()
    assert len(services) > 0

    # Check that all are packaging-related
    packaging_keywords = ["коробка", "пакет", "конверт"]
    for service in services:
        assert any(kw in service.name.lower() for kw in packaging_keywords)


def test_suggest_box_small_package():
    """Test suggesting box for small package."""
    box = suggest_box(0.3, "warehouse-door")
    assert box is not None
    assert box.code == "CARTON_BOX_XS"
    assert box.max_weight >= 0.3


def test_suggest_box_medium_package():
    """Test suggesting box for medium package."""
    box = suggest_box(3.5, "warehouse-door")
    assert box is not None
    assert box.max_weight >= 3.5
    # Should suggest 5kg box, not larger
    assert box.max_weight <= 5.0


def test_suggest_box_large_package():
    """Test suggesting box for large package."""
    box = suggest_box(15.0, "warehouse-door")
    assert box is not None
    assert box.max_weight >= 15.0


def test_suggest_box_mode_restriction():
    """Test box suggestion respects delivery mode."""
    # 30kg box is only available for warehouse-warehouse and warehouse-door
    box_warehouse = suggest_box(25.0, "warehouse-warehouse")
    assert box_warehouse is not None

    # Should work for warehouse-door too
    box_door = suggest_box(25.0, "warehouse-door")
    assert box_door is not None


def test_suggest_box_too_heavy():
    """Test suggesting box for package that's too heavy."""
    box = suggest_box(50.0, "warehouse-door")
    # Should return None as no box can handle 50kg
    assert box is None


def test_service_with_restrictions():
    """Test service with restrictions."""
    service = get_service("TRYING_ON")
    assert service is not None
    assert service.restrictions is not None
    assert "ИМ" in service.restrictions


def test_service_requires_parameter():
    """Test service that requires parameter."""
    service = get_service("GET_UP_FLOOR_BY_HAND")
    assert service is not None
    assert service.requires_parameter is True
    assert service.weight_limit == 150.0


def test_get_order_type():
    """Test getting order type by ID."""
    order_type = get_order_type(1)
    assert order_type is not None
    assert order_type.id == 1
    assert order_type.name == "интернет-магазин"


def test_get_order_type_not_found():
    """Test getting non-existent order type."""
    order_type = get_order_type(999)
    assert order_type is None


def test_list_order_types():
    """Test listing all order types."""
    types = list_order_types()
    assert len(types) == 2
    assert any(t.id == 1 for t in types)
    assert any(t.id == 2 for t in types)


def test_get_additional_type():
    """Test getting additional type by ID."""
    add_type = get_additional_type(2)
    assert add_type is not None
    assert add_type.id == 2
    assert "LTL" in add_type.name


def test_get_additional_type_not_found():
    """Test getting non-existent additional type."""
    add_type = get_additional_type(999)
    assert add_type is None


def test_list_additional_types():
    """Test listing all additional types."""
    types = list_additional_types()
    assert len(types) == 9
    assert any(t.id == 2 for t in types)
    assert any(t.id == 14 for t in types)
