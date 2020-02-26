"""Configuration for the job."""


class Config(dict):
    """Configuration for all environments."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    MODELS = [
        {
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }
    ]


class ProdConfig(Config):
    """Configuration for the prod environment."""

    DEBUG = False


class BetaConfig(Config):
    """Configuration for the beta environment."""

    DEVELOPMENT = True
    DEBUG = True


class TestConfig(Config):
    """Configuration for the test environment."""

    DEVELOPMENT = True
    DEBUG = True


class DevConfig(Config):
    """Configuration for the dev environment."""

    TESTING = True
    DEBUG = True
