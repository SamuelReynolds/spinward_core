"""
Utility scripts for manipulating dicts
"""


def dict_update_recursive(target_dict, source_dict):
    """
    Recursively update dict, so that sub-dicts are updated instead of replaced.
    Target dict is updated in place.

    @param target_dict: dict to update
    @param source_dict: dict from which to copy values
    """
    for key, val in source_dict.items():
        if isinstance(val, dict) and key in target_dict and isinstance(target_dict[key], dict):
            dict_update_recursive(target_dict[key], val)
        else:
            target_dict[key] = val


_NOTHING = object

# def dict_get_nested(target_dict, keys, default=None, extend=False):
#     """
#     Return value from nested path within dict.
#
#     @param keys:        Nested path keys
#     @param default:     Default value to return if item is not found
#
#     @return value at nested path
#     """
#     if not keys:
#         raise KeyError("No key specified")
#     cur = target_dict
#     keys = list(reversed(keys))
#     while keys:
#         key = keys.pop()
#         if extend:
#             val = cur.setdefault(key, {})
#         else:
#             val = cur.get(key, _NOTHING)
#         if keys:
#             # if val is _NOTHING and extend:
#             #     cur[key] = val = dict()
#             #     # cur = val
#             #     # continue
#             if keys and isinstance(val, dict):
#                 cur = val
#                 continue
#             # elif val is _NOTHING and extend:
#             #     cur[key] = dict()
#             #     cur = cur[key]
#             #     continue
#             else:
#                 break
#         # if val is _NOTHING:
#         #     return default
#         # break
#     return default if val is _NOTHING else val


def dict_get_nested(target_dict, keys, default=None):
    """
    Return value from nested path within dict.

    @param target_dict: Dict from which to retrieve value
    @param keys:        Nested path keys
    @param default:     Default value to return if item is not found

    @return value at nested path
    """
    if not keys:
        raise KeyError("No key specified")
    cur = target_dict
    keys = list(reversed(keys))
    while keys:
        key = keys.pop()
        val = cur.get(key, _NOTHING)
        if keys:
            # if val is _NOTHING and extend:
            #     cur[key] = val = dict()
            #     # cur = val
            #     # continue
            if keys and isinstance(val, dict):
                cur = val
                continue
            # elif val is _NOTHING and extend:
            #     cur[key] = dict()
            #     cur = cur[key]
            #     continue
            else:
                break
        # if val is _NOTHING:
        #     return default
        # break
    return default if val is _NOTHING else val


def dict_set_nested(target_dict, keys, value, extend=True):
    """
    Set value at nested path within dict. Optionally build out parent path.

    @param target_dict: Dict to update
    @param keys:        Nested path keys
    @param value:       Value to set in target tict
    @param extend:      If True, create missing intermediate levels as needed.
                        If False, raise KeyError if an intermediate level is missing.
    """
    if not keys:
        raise KeyError("No key specified")
    cur = target_dict
    term_key = keys.pop()
    consumed = []
    while keys:
        key = keys.pop(0)
        child = cur.get(key, _NOTHING)
        consumed.append(key)
        if child is _NOTHING:
            if extend:
                cur[key] = child = {}
                cur = child
            else:
                raise KeyError("Item at %s not found" % ('.'.join(consumed),))
        elif not isinstance(child, dict):
            raise KeyError("Item at %s not a dict" % ('.'.join(consumed),))
        else:
            cur = child
    cur[term_key] = value

