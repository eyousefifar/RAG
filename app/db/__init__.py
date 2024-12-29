from .mongodb import get_database


if __name__ == "__main__":
    # create_user()
    # Get the database
    db = get_database()


__all__ = ["get_database"]
