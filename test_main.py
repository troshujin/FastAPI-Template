"""
Welcome to my test script.

I didn't get pytest to work so I wrote my own.
All the custom function required to run this are located in 'test_functions.py'

To run the script, run the command `python <file.py> stdout`
To see what was printed, run the command `python <file.py> stdout`
where <file.py> is your python file.

To create a new test:
1. Create a new async function. 
2. Add the '@results.add_test' decorator to it.
3. Name it something descriptive.
4. Test whatever needs to be tested.
5. Make sure you use 'assert' to do the test.
6. Profit

Use the tracker!
Whenever you add a "something" which needs to be deleted after the test is finished,
add it to the tracker.
It is added to the tracker by doing: tracker.add(<group>, <any data>)

After the test is done, it will display everything that is tracked and not deleted.

To delete the something from the tracker again, do: tracker.remove(<group>, <exact data>)
The <exact data> needs to match the data you want to remove.

So basicly

adding data
`
    data = create_data()
    tracker.add("some", data)
`

getting data and removing it
`
    data = tracker.get_latest("some")
    remove_data()
    tracker.remove("some", thing)
`

User the "Helper" class to write your own helper functions
"""


import asyncio
from test_functions import *
from main import app
from fastapi.testclient import TestClient
import json


client = TestClient(app)

tracker = Tracker()
results = TestResults()


@results.add_test
async def create_user():
    """Should create new user"""

    new_user = {
        "username": "Ya boi!",
    }

    response = client.post("/api/users", json={**new_user})
    user = json.loads(response.content.decode("utf-8"))

    tracker.add("user", user)

    assert response.status_code == 200, "User was not created"
    assert Helper.check_user(new_user, user), "Incorrect username was returned"


@results.add_test
async def create_item():
    """Should create new item"""

    new_item = {
        "name": "Testing Item",
        "description": "Description for the test.",
        "price": 12500,
        "is_hidden": False,
    }

    response = client.post("/api/items", json={**new_item})
    item = json.loads(response.content.decode("utf-8"))

    tracker.add("item", item)

    assert response.status_code == 200, "Item was not created"
    assert Helper.check_item(item, new_item), "Incorrect item was returned"


@results.add_test
async def read_item():
    """Should read item"""
    existing_item = tracker.get_latest("item")

    response = client.get("/api/items/" + str(existing_item.get("id")))
    item = json.loads(response.content.decode("utf-8"))

    assert response.status_code == 200, "Item was not found"
    assert Helper.check_item(item, existing_item), "Incorrect item was returned"
    assert item["view_count"] == 1, "No 'view' was added"


@results.add_test
async def update_item():
    """Should update item"""
    old_item = tracker.get_latest("item")

    update_item = {
        "id": old_item.get("id"),
        "name": "Testing Item but edited",
        "description": "Description for the test but edited.",
        "price": 15000,
        "is_hidden": True,
    }

    response = client.patch("/api/items", json={**update_item})
    item = json.loads(response.content.decode("utf-8"))

    tracker.remove("item", old_item)
    tracker.add("item", item)

    assert response.status_code == 200, "Item was not updated"
    assert Helper.check_item(item, update_item), "Item was incorrectly updated"


@results.add_test
async def create_items():
    """Should create new item"""

    new_item = {
        "name": "",
        "description": "",
        "price": 100,
        "is_hidden": False,
    }

    names = ["test2", "cheese", "geese", "pokémon"]
    descriptions = ["I enjoy testing", "test desc", "pokéball", "woof"]

    for (name, description) in zip(names, descriptions):
        new_item["name"] = name
        new_item["description"] = description

        response = client.post("/api/items", json={**new_item})
        item = json.loads(response.content.decode("utf-8"))

        assert response.status_code != 401, item["detail"]

        tracker.add("item", item)

        assert response.status_code == 200, "Item was not created"
        assert Helper.check_item(item, new_item), "Incorrect item was returned"


@results.add_test
async def search_items():
    """Should search correct item"""

    searches = [
        "test",
        "eese",
        "desc",
        "desc&is_hidden=true",
        "é",
        "",
        "&is_hidden=false",
    ]
    result_counts = [3, 2, 2, 1, 2, 5, 4]

    for (search, result_count) in zip(searches, result_counts):
        response = client.get(f"/api/items?search={search}")
        items = json.loads(response.content.decode("utf-8"))

        assert response.status_code != 401, items["detail"]
        assert response.status_code == 200, "Error while searching"
        assert len(items) == result_count, \
            f"Searchresult of '{len(items)}' was not the expected '{result_count}' while searching for '{search}'" \
            + f"\nThe reason for this error might be the fact that there is still data in the database, clear it by running 'python manage_db.py reset'"


@results.add_test
async def delete_all_items():
    """Should delete all tracked items"""

    items = tracker.get("item")

    for item in list(items):  # Create a copy of the list
        response = client.delete("/api/items/" + str(item.get("id")))

        assert response.status_code == 200, "Item was not deleted"

        tracker.remove("item", item)


@results.add_test
async def delete_user():
    """Should delete user"""

    user = tracker.get_latest("user")

    response = client.delete("/api/users/" + str(user.get("id")))

    assert response.status_code == 200, "User was not deleted"

    tracker.remove("user", user)


t = asyncio.run(main(results, tracker))
