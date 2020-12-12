from typing import Dict, Callable, Union, List, Generator


def get_all(parameters: Dict, get_response: Callable[[], Dict[str, Union[int, List[Dict]]]]) \
        -> Generator[Dict, None, None]:
    parameters = parameters.copy()
    total = 0

    while True:
        parameters["offset"] = total

        # noinspection PyArgumentList
        response = get_response(**parameters)

        assert "items" in response
        assert "count" in response

        descriptions_chunk = response["items"]
        count = response["count"]

        total += len(descriptions_chunk)

        for desc in descriptions_chunk:
            yield desc

        if count == total:
            break
