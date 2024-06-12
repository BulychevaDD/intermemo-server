from dotenv import dotenv_values


def get_environment_variable(name: str) -> str:
    return dotenv_values('.env').get(name)
