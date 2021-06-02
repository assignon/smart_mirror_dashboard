def remove_whitespace(json_data):
    for key, value in json_data.items():
        if type(value) == str:
            json_data[key] = value.strip()