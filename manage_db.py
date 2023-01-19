import time
from dotenv import load_dotenv

load_dotenv()

import sys, os, shutil
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, ProgrammingError
from database import Session, engine
import database.models as mo
import database.model_enums as me
import src.crud as crud


def init_db() -> None:
    """Initialise db and fill database, with data for easy start"""

    print("Initializing database...")
    mo.Base.metadata.create_all(engine)
    print("Initialized database.\n")


def seed_db() -> None:
    print("Seeding database...")
    with Session() as session:

        try:
            user_admin = crud.UserCRUD(session).create_user(
                mo.User(username="admin")
            )

            item_1 = crud.ItemCRUD(session).create_item(
                user_admin,
                mo.Item(
                    description="Test item",
                    name="Item one",
                    price=1000,
                )
            )

            item_2 = crud.ItemCRUD(session).create_item(
                user_admin,
                mo.Item(
                    description="Test item, but it has a cooler description!",
                    name="Item two",
                    price=600,
                )
            )
            
            session.commit()

        except IntegrityError as e:
            print("\n\nSomething went wrong quite badly :(\n\n")
            print(e)
        
        else:
            print("Seeded database")


def check_db() -> bool:
    with Session() as session:

        print("Checking database...")

        try:
            stmt = select(mo.User)
            session.execute(stmt).all()

        except ProgrammingError:
            print("Not initialized.\n")
            return False

        except Exception as e:
            print(e)
            print("A failure occured, restarting script. This was attempt number", attempt)
            os.execv(sys.argv[0], sys.argv[1] + " " + str(attempt+1))

        print("Already initialized.\n")
        return True


def delete_db() -> None:
    print("Dropping all tables...")
    mo.Base.metadata.drop_all(engine)

    print("Dropped all tables.\n")


def reset() -> None:
    delete_db()

    if not check_db():
        init_db()


if len(sys.argv) > 3:
    print("You have specified too many arguments")
    sys.exit()

if len(sys.argv) < 2:
    print(
        "You need to specify the function to execute, 3 options: delete, init,  reset"
    )
    sys.exit()

fun = sys.argv[1]
attempt = int(sys.argv[2]) if len(sys.argv) == 3 else 1

if attempt > 5: 
    print("failed too many times.")
    sys.exit()

if fun == "reset":
    reset()

elif fun == "delete":
    delete_db()

elif fun == "init":
    if not check_db():
        mo.Base.metadata.create_all(engine)
        init_db()

elif fun == "seed":
    if not check_db():
        print("No data base, cannot seed!")
    seed_db()
    


else:
    print("This option does not exist, please use either 'delete', 'init' or 'reset'")
    sys.exit()
