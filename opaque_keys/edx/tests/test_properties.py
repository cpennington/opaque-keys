"""
TestCases that use property-based testing to validate properties that all
installed keys should have.
"""

from unittest import TestCase

import ddt
from hypothesis import strategies, given, assume
from six import text_type
from opaque_keys.edx.keys import CourseKey, UsageKey, DefinitionKey, BlockTypeKey, AssetKey
from opaque_keys import InvalidKeyError

KEY_TYPES = (CourseKey, UsageKey, DefinitionKey, BlockTypeKey, AssetKey)
KEY_CLASSES = set(
    extension.plugin
    for key_type in KEY_TYPES
    for extension in key_type._drivers()  # pylint: disable=protected-access
)


def insert(string, index, character):
    """
    Operation to insert a character in a string.

    Arguments:
        string: The string to insert into
        index: The index to insert the character at
        character: The character to insert
    """
    return string[:index] + character + string[index:]


def delete(string, index, character):  # pylint: disable=unused-argument
    """
    Operation to delete a character from a string.

    Arguments:
        string: The string to delete from
        index: The index to delete the character at
        character: This argument is ignored, but exists to match the signatures
            of insert and replace.
    """
    return string[:index - 1] + string[index:]


def replace(string, index, character):
    """
    Operation to replace a character in a string.

    Arguments:
        string: The string to replace in
        index: The index to replace the character at
        character: The character to insert
    """
    return string[:index - 1] + character + string[index:]


@ddt.ddt
class TestKeyProperties(TestCase):
    """
    Tests of properties that should hold true of all OpaqueKeys.
    """

    @ddt.data(*KEY_CLASSES)
    @given(
        data=strategies.data(),
        operation=strategies.sampled_from((insert, replace, delete)),
        index=strategies.floats(min_value=0, max_value=1),
        character=strategies.characters(),
    )
    def test_different_serializations_different_keys(self, key_class, data, operation, index, character):
        key = data.draw(key_class.key_strategy())
        serialized = text_type(key)
        perturbed = operation(serialized, int(len(serialized) * index), character)
        assume(serialized != perturbed)

        try:
            perturbed_key = key_class.from_string(perturbed)
        except InvalidKeyError:
            pass  # The perturbed serialization didn't parse. That's ok.
        else:
            self.assertNotEqual(
                key,
                perturbed_key,
                "String {!r} and {!r} parse to equal keys {!r} and {!r}".format(
                    serialized,
                    perturbed,
                    key,
                    perturbed_key,
                )
            )
