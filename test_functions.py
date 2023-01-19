from uuid import UUID
import os, sys, math


class Helper:
    """Write your own helper functions here"""

    def check_user(user1, user2):
        """Check if 2 users are equal enough"""

        assert user1["username"] == user2["username"], "Incorrect username"

        return True

    def check_item(item1, item2):
        """Check if 2 items are equal enough"""

        assert item1["name"] == item2["name"], "Incorrect name"
        assert item1["description"] == item2["description"], "Incorrect description"
        assert item1["price"] == item2["price"], "Incorrect price"
        assert item1["is_hidden"] == item2["is_hidden"], "Incorrect is_hidden"

        return True


class TestResults:
    """
    An object to keep track of tests.
    ---
     Methods
    ------
    `add_test()`
    Usable as decorator.
    A function is passed in and added to the tests list.

    Parameters:
    - `func`: function object
    ---
    `add_fail()`
    A function and an error message is passed in.

    Parameters:
    - `func`: function object
    - `error`: str
    ---
    `display()`
    Prints out all contained data pretty fancily to the console.
    ---
     Extra
    ------
    `bcolors`
    Has colors for printing
    """

    tests = []
    tests_success = 0
    tests_failed = []

    def add_test(self, func):
        self.tests.append(func)
        return func

    def add_fail(self, func, error):
        class Fail:
            def __init__(self, func, error) -> None:
                self.func = func
                self.error = error

        self.tests_failed.append(Fail(func, error))

    class bcolors:
        HEADER = "\033[95m"
        OKBLUE = "\033[94m"
        OKCYAN = "\033[96m"
        OKGREEN = "\033[92m"
        WARNING = "\033[93m"
        FAIL = "\033[91m"
        ENDC = "\033[0m"
        BOLD = "\033[1m"
        UNDERLINE = "\033[4m"

    def display(self):
        percent = round(self.tests_success / len(self.tests) * 100)
        chars = progress_bar(percent, sep="|")

        print(f"\n{len(self.tests)}\ttotal tests.")
        print(f"{self.tests_success}\tsuccessful tests.\n")
        print(
            self.bcolors.BOLD, f"\t{percent}%", self.bcolors.ENDC, " successful", sep=""
        )
        print(
            "[ ",
            self.bcolors.OKGREEN,
            chars[0],
            self.bcolors.FAIL,
            chars[1],
            self.bcolors.ENDC,
            " ]",
            sep="",
        )

        if len(self.tests_failed) > 0:
            print(
                "\n",
                self.bcolors.FAIL,
                self.bcolors.BOLD,
                "ERRORS:",
                self.bcolors.ENDC,
                sep="",
            )
            for fail in self.tests_failed:
                print(
                    f"{self.bcolors.BOLD}{fail.func.__name__}"
                    + f"{self.bcolors.WARNING} -> "
                    + f"{self.bcolors.ENDC}{self.bcolors.FAIL}{fail.error}{self.bcolors.ENDC}"
                )


class Tracker:
    """
    An object to keep track of items created.
    With the reason to make sure the test does not leave any rubbish behind.

    With a type you can group data together for overview purposes.
    ---
     Methods
    ------
    `add()`
    Add a tracker.

    Parameters:
    - `type`: str
    - `data`: any
    ---
    `remove()`
    Remove a tracker from type where data matches completely.

    Parameters:
    - `type`: str
    - `data`: any

    Returns: `list`
    ---
    `get()`
    Get all trackers in a group.

    Parameters:
    - `type`: str

    Returns: `list`
    ---
    `get_latest()`
    Get latest trackers in a group.

    Parameters:
    - `type`: str

    Returns: `any`
    ---
    `display()`
    Prints out all contained data pretty fancily to the console.

    """

    tracking = {}

    def add(self, type, data):
        if not any(key == type for key in self.tracking.keys()):
            self.tracking[type] = []
        self.tracking[type].append(data)

    def remove(self, type, data):
        self.tracking[type].remove(data)

    def get(self, type):
        if not any(key == type for key in self.tracking.keys()):
            return None
        return self.tracking[type]

    def get_latest(self, type):
        if not any(key == type for key in self.tracking.keys()):
            return None
        return self.tracking[type][-1]

    def display(self, screen):
        if not any(len(self.tracking[key]) > 0 for key in self.tracking.keys()):
            print(
                f"\n{TestResults.bcolors.BOLD}All clear: {TestResults.bcolors.ENDC}Nothing left to track"
            )
            return

        print("\n\nDisplaying tracked objects which are remaining after the test.")

        max_width = screen - 20
        for key in self.tracking.keys():

            if len(self.tracking[key]) == 0:
                print(
                    f"   No more trackable {TestResults.bcolors.BOLD}{key}s{TestResults.bcolors.ENDC}",
                )
                continue

            print(
                f"\n   {TestResults.bcolors.BOLD}{key}(s):{TestResults.bcolors.ENDC}\n---"
            )

            for i in self.tracking[key]:
                i = str(i)
                print(
                    f"{TestResults.bcolors.WARNING}  ->{TestResults.bcolors.ENDC}\t"
                    + i[0:max_width]
                    + ("..." if len(i) > max_width else "")
                )
            print()


def progress_bar(percent: int, prog: str = "=", sep: str = ">", end: str = "-") -> list:
    """
    Creates a progressbar based on a percentage.

    Parameters:
    - `percent`: int (should be between 0 and 100)
    - `prog`: str, single character [Optional]
    - `sep`: str, single character [Optional]
    - `end`: str, single character [Optional]

    Returns: `list` of 2 items with a total of 100 characters for printing a progressbar.
    """
    if any(len(i) > 1 for i in [prog, sep, end]):
        raise Exception("Characters must only be 1 character long.")
    chars = [prog * percent, end * (100 - percent)]

    if percent > 0:
        chars[0] = chars[0][0:-1] + sep

    return chars


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID. https://stackoverflow.com/a/33245493/10795192

     Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

     Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

     Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


async def main(results, tracker):
    # Try-Except because github action does not have a terminal and will throw an error 
    try:
        screen = os.get_terminal_size().columns
    except:
        screen = 150

    line = "- " * math.floor(screen / 2)

    title = " TESTING "
    side_len = round((screen - len(title)) / 2) - 1
    text_in_line = (
        "- " * math.floor(side_len / 2)
        + TestResults.bcolors.HEADER
        + title
        + TestResults.bcolors.ENDC
        + " -" * (math.floor(side_len / 2) + 1)
    )

    sys.stdout.write(f"\r{text_in_line}\n")
    sys.stdout.flush()

    print_info = len(sys.argv) > 1 and sys.argv[1] == "stdout"

    for func in results.tests:

        chars = progress_bar(
            round((results.tests.index(func) + 1) / len(results.tests) * 100)
        )

        sys.stdout.write(
            f"\r[ {results.bcolors.OKGREEN}{chars[0]}{results.bcolors.FAIL}{chars[1]}{results.bcolors.ENDC} ] "
            + f"test {(results.tests.index(func) + 1)} / {len(results.tests)} {func.__name__}                                            "
            + ("\n" if print_info else "")
        )
        sys.stdout.flush()

        x = sys.stdout
        sys.stdout = None

        if print_info:
            sys.stdout = x

        try:
            await func()
            results.tests_success += 1

        except AssertionError as e:
            results.add_fail(func, e)

        except Exception as e:
            results.add_fail(func, e)

        sys.stdout = x

    sys.stdout.write(
        f"\r[ {results.bcolors.OKGREEN}{progress_bar(100)[0]}{results.bcolors.ENDC} ] "
        + f"test {(results.tests.index(func) + 1)} / {len(results.tests)} Done!                                           "
    )
    sys.stdout.flush()
    tracker.display(screen)
    results.display()
    print(f"\n{line}")
