from dotenv import load_dotenv


def pytest_configure(config):
    """Load environment variables before tests run"""
    load_dotenv(".env.test", override=True)
    print("Loaded .env.test for testing environment")
