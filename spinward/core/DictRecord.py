"""
Dictionary with dict-style and attribute-style access.
"""
import logging
import sys
from .dict_util import dict_get_nested, dict_set_nested, dict_update_recursive

logger = logging.getLogger(__name__)


class DictRecord(dict):
    """
    Dictionary with dict-style and attribute-style access.
    """

    def __init__(self, *args, **kwargs):
        super(DictRecord, self).__init__(*args, **kwargs)


    def __setattr__(self, key, value):
        super(DictRecord, self).__setitem__(key, value)


    def __getattr__(self, key):
        return super(DictRecord, self).__getitem__(key)


    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, super(DictRecord, self).__repr__())


    @staticmethod
    def from_dict(source, normalize=True):
        """
        Return a new DictRecord created from a dict.

        @param source:      Source dict.
        @param normalize:   If True, make sure all contained dicts are converted, as well.
        """
        rec = DictRecord(source)
        if normalize:
            rec.normalize()
        return rec


    def as_dict(self):
        """
        Return dict version (copy) of DictRecord.

        @return dict version of DictRecord, with all nested DictRecords also converted to dicts.
        """
        return self._convert_dict_records_to_dict(dict(self))


    def get_nested(self, keys, default=None):
        """
        Return value from nested path within dict.

        @param keys:        Nested path keys
        @param default:     Default value to return if item is not found

        @return value at nested path
        """
        return dict_get_nested(self, keys, default)


    def set_nested(self, keys, value, extend=True):
        """
        Return value from nested path within dict.

        @param keys:        Nested path keys
        @param default:     Default value to return if item is not found
        @param extend:      If True, create missing intermediate levels as needed.
                            If False, raise KeyError if an intermediate level is missing.
        """
        return dict_set_nested(self, keys, value, extend=extend)


    @classmethod
    def _convert_dict_records_to_dict(cls, target):
        """
        Recursively convert DictRecord elements to dicts in a dict.

        @param target:   dict in which to convert DictRecords to dicts.

        @return original dict with all nested DictRecords converted to dicts.
        """
        for key, val in target.items():
            if isinstance(val, DictRecord):
                # Convert to dict and recurse
                target[key] = val.as_dict()
            elif isinstance(val, dict):
                # recurse into sub-dict
                cls._convert_dict_records_to_dict(val)
            # else:
            #     target[key] = val
        return target


    def normalize(self):
        """
        Recursively convert all contained dicts to DictRecords.
        """
        for key, value in self.items():
            if isinstance(value, dict) and not isinstance(value, DictRecord):
                value = DictRecord(value)
                value.normalize()
                self[key] = value


    def update_recursive(self, source_dict, normalize=True):
        """
        Recursively update DictRecord, so that sub-dicts are updated instead of replaced.

        @param source_dict: dict from which to copy values
        @param normalize:   If True, normalize the DictRecord (see `normalize` method).
                            Defaults to True (principle of least surprise).
        """
        dict_update_recursive(self, source_dict)
        if normalize:
            self.normalize()


    def dump(self, delimiter=':', keys=None, file=sys.stdout):
        """
        dump DictRecord elements to output.

        @param delimiter:       Column delimiter
        @param keys:            Top-level keys to include in output
        @param file:            Output destination (default = stdout)
        """
        print(self.pretty_string_recursive(delimiter, keys), file=file)


    def dump_recursive(self, delimiter=':', keys=None, file=sys.stdout):
        """
        dump indented text representation of the DictRecord elements to output.

        @param delimiter:       Column delimiter
        @param keys:            Top-level keys to include in output
        @param file:            Output destination (default = stdout)
        """
        print(self.pretty_string_recursive(delimiter, keys), file=file)


    def pretty_string(self, delimiter=':', keys=None):
        """
        Generate formatted text from the DictRecord.
        Format is `<key> <delimiter> <value>` for each element in record.

        @param delimiter:   Column delimiter
        @param keys:        Keys to include in output. Defaults to all keys.

        @return a string
        """
        keys = list(self.keys()) if not keys else list(keys)
        if not keys:
            return ""
        w1 = max(*[len(str(key)) for key in keys])
        tmpl = "%%-%ds %s %%r" % (w1, delimiter)
        return '\n'.join([tmpl % (str(key), self[key]) for key in keys])


    def pretty_string_recursive(self, delimiter=':', keys=None, return_rows=False):
        """
        Generate formatted text from the DictRecord.
        Format is `<name> <delimiter> <value>` for each element in record.
        Each nested DictRecord is indented relative to the one above it.

        @param delimiter:       Column delimiter
        @param keys:            Top-level keys to include in output
        @param return_rows:     If True, return a list of rows instead of the final text.

        @return string
        """
        return self._pretty_string_recursive(delimiter, keys, return_rows)


    def _pretty_string_recursive(self, delimiter=':', keys=None, return_rows=False, indent=""):
        """
        Generate formatted text from the DictRecord.
        Format is `<name> <delimiter> <value>` for each element in record.
        Each nested DictRecord is indented relative to the one above it.

        @param delimiter:       Column delimiter
        @param keys:            Top-level keys to include in output
        @param indent:          String by which to indent each row
        @param return_rows:     If True, return a list of rows instead of the final text.

        @return string
        """
        keys = list(self.keys()) if not keys else list(keys)
        if len(keys) == 0:
            return ""
        keys.sort()
        w1 = max(*[len(str(key)) for key in keys])
        tmpl = "%s%%-%ds %s %%r" % (indent, w1, delimiter)
        next_indent_width = len(indent) + w1 + len(delimiter) + 2
        next_indent = " " * next_indent_width

        rows = []
        for key in keys:
            value = self[key]
            if isinstance(value, dict) and not isinstance(value, DictRecord):
                value = DictRecord.fromDict(value, recurse=True)
            if isinstance(value, DictRecord):
                # Do not pass keys to lower levels of tree
                sub_rows = value._pretty_string_recursive(delimiter=delimiter, indent=next_indent, return_rows=True)
                if sub_rows:
                    rows.append(tmpl.replace('%r', '%s') % (key, sub_rows[0][next_indent_width:]))
                else:
                    rows.append(tmpl.replace('%r', '%s') % (key, ""))
                rows.extend(sub_rows[1:])
            else:
                rows.append(tmpl % (key, value))
        if return_rows:
            return rows
        return '\n'.join(rows)


class DictRecordRO(DictRecord):
    """
    Read-only DictRecord.
    """
    def __init__(self, *args, **kwargs):
        super(DictRecordRO, self).__init__(*args, **kwargs)


    def __setattr__(self, key, value):
        raise AttributeError("%s is read-only" % (self.__class__.__name__,))


    def __setitem__(self, key, value):
        raise KeyError("%s is read-only" % (self.__class__.__name__,))
