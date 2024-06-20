import pytest

from trcli.data_classes.data_parsers import MatchersParser


class TestMatchersParser:

    @pytest.mark.parametrize("case_name,expected_case_ids,expected_case_name_with_ids", [
        ("numbers but no test id 1234", [], "numbers but no test id 1234"),
        ("C12345 one id in name", [12345], "one id in name"),
        ("one id in name C12345", [12345], "one id in name"),
        ("C123_my_test_case", [123], "my_test_case"),
        ("my_test_case_C123", [123], "my_test_case"),
        ("module_1_C123_my_test_case", [123], "module_1_my_test_case"),
        ("[C123] my test case", [123], "my test case"),
        ("my test case [C123]", [123], "my test case"),
        ("module 1 [C123] my test case", [123], "module 1 my test case"),
        ("C12345 C2345 C789 three ids in name", [12345, 2345, 789], "three ids in name"),
        ("three ids in name C12345 C2345 C789", [12345, 2345, 789], "three ids in name"),
        ("three ids in name C12345, C2345, C789", [12345, 2345, 789], "three ids in name"),
        ("C123_C234_C789_my_test_case", [123, 234, 789], "my_test_case"),
        ("my_test_case_C123_C234_C789", [123, 234, 789], "my_test_case"),
        ("module_1_C123_C234_C789_my_test_case", [123, 234, 789], "module_1_my_test_case"),
        ("[C123, C234, C789] my test case", [123, 234, 789], "my test case"),
        ("my test case [C123 C234 C789]", [123, 234, 789], "my test case"),
        ("module 1 [C123,C234,C789] my test case", [123, 234, 789], "module 1 my test case"),
        ("module 1 [C123] 2 [C234, C789] my test case", [123, 234, 789], "module 1 2 my test case"),
        ("module 1 [C123] 2 [C234 messy name] my test case", [123, 234], "module 1 2 [messy name] my test case"),
    ])
    def test_parse_name_with_id(self, case_name, expected_case_ids, expected_case_name_with_ids):
        case_ids, result_case_name = MatchersParser.parse_name_with_id(case_name)
        assert case_ids == expected_case_ids
        assert result_case_name == expected_case_name_with_ids
