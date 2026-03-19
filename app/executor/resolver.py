def resolve_input(input_data, results: dict):
    if not isinstance(input_data, (dict, list)):
        return input_data

    if isinstance(input_data, list):
        return [resolve_input(item, results) for item in input_data]

    # Strict source reference handling
    if isinstance(input_data, dict) and "source" in input_data:
        allowed_keys = {"source", "path"}
        extra_keys = set(input_data.keys()) - allowed_keys

        if extra_keys:
            raise ValueError(
                f"resolve_input: invalid keys in source reference: {extra_keys}"
            )

        source = input_data["source"]

        if not isinstance(source, str):
            raise ValueError("resolve_input: 'source' must be a string")

        if source not in results:
            raise ValueError(f"resolve_input: source {source!r} not found in results")

        value = results[source]

        if "path" in input_data:
            path = input_data["path"]

            if not isinstance(path, str):
                raise ValueError("resolve_input: 'path' must be a string")

            for key in path.split("."):
                if not isinstance(value, dict) or key not in value:
                    raise ValueError(
                        f"resolve_input: invalid path {path!r} on source {source!r}"
                    )
                value = value[key]

        return value

    # Regular dict: recurse
    return {k: resolve_input(v, results) for k, v in input_data.items()}