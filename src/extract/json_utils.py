import json

def parse_json_response(response: str):
    response = response.strip()

    if response.startswith("```json"):
        response = response.removeprefix("```json").strip()

    if response.endswith("```"):
        response = response.removesuffix("```").strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError as e:
        print("\nJSON PARSE ERROR")
        print(e)
        print("\nResponse was:")
        print(response)
        raise