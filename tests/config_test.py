from sastadev.conf import settings


def test_settings_change():
    assert settings.ALPINO_PORT == 7001
    settings.ALPINO_PORT = 7002
    assert settings.ALPINO_PORT == 7002
    settings.ALPINO_PORT = 7001
