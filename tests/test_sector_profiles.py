from control_mapper.sector_profiles import Sector, get_sector_profile, list_sector_profiles


def test_all_sector_profiles_are_available() -> None:
    profiles = list_sector_profiles()
    assert len(profiles) == len(Sector)


def test_critical_infrastructure_has_highest_contextual_adjustment() -> None:
    critical = get_sector_profile(Sector.CRITICAL_INFRASTRUCTURE)
    general = get_sector_profile(Sector.GENERAL)
    assert critical.risk_adjustment > general.risk_adjustment
    assert "incident-response" in critical.priority_domains


def test_sector_profile_does_not_claim_applicability() -> None:
    profile = get_sector_profile("financial-services")
    assert "do not determine legal or regulatory applicability" in profile.disclaimer
