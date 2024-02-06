def get_instance_changes(pre_instance: dict, post_instance: dict) -> dict:
    changes = {}

    keys = set(pre_instance.keys()) | set(post_instance.keys())

    for key in keys:
        pre_value = pre_instance.get(key)
        post_value = post_instance.get(key)

        if isinstance(pre_value, dict) and isinstance(post_value, dict):
            changes[key] = get_instance_changes(pre_value, post_value)

        elif pre_value != post_value:
            changes[key] = {'pre': pre_value, 'post': post_value}

    return changes
