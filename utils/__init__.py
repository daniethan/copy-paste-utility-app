def pretty_print_dict(d: dict):
    pretty_dict = ""
    for k, v in d.items():
        pretty_dict += f"\n{k}: "
        if type(v) == dict:
            for value in v:
                pretty_dict += f"\n {value}: {v[value]}"
            else:
                pretty_dict += "\n"
        else:
            pretty_dict += f"{v}\n"

    return pretty_dict.strip()


def pretty_print_list(l: list) -> None:
    for item in l:
        print(item)
    else:
        print("----" * 30)
