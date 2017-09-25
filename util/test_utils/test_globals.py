import unittest
from util.globals import GlobalsUtils


class GlobalsTests(unittest.TestCase):

    def setUp(self):
        self.utils = GlobalsUtils("")

    def test_GIVEN_a_blank_line_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = ""

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_comment_line_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "# This is a comment."

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_correct_macro_definition_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "GALIL_01__ADDR1=1.2.3.4"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_definition_where_ioc_name_is_missing_WHEN_syntax_check_THEN_invalid(self):
        # Arrange
        line = "ADDR1=1.2.3.4"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertFalse(result)

    def test_GIVEN_a_definition_where_equals_sign_is_missing_WHEN_syntax_check_THEN_invalid(self):
        # Arrange
        line = "IOCNAME__ADDR1 1.2.3.4"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertFalse(result)

    def test_GIVEN_a_definition_where_there_is_more_than_one_double_underscore_WHEN_syntax_check_THEN_invalid(self):
        # Arrange
        line = "IOCNAME__ADDR1__YES=1.2.3.4"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertFalse(result)

    def test_GIVEN_a_definition_where_there_are_lots_of_single_underscores_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "A_B_C_T_H_I_N_G__M_A_C_R_O=1.2.3.4"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_macro_value_is_empty_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "GALIL_01__ADDR1="

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_macro_value_looks_like_a_valid_macro_definition_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "GALIL_01__ADDR1=GALIL_01__ADDR1=YES"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_macro_definition_is_invalid_but_value_contains_valid_definition_WHEN_syntax_check_THEN_invalid(self):
        # Arrange
        line = "OOPS_NO_DOUBLE_UNDERSCORE=GALIL_01__ADDR1=YES"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertFalse(result)

    def test_GIVEN_a_macro_definition_contains_inline_comment_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "GALIL_01__ADDR1=1.2.3.4 # Here is a comment"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_an_invalid_macro_definition_that_is_commented_out_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "# OOPS_NO_DOUBLE_UNDERSCORE=HELLO"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_macro_value_has_special_characters_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "VALID__MACRO=!$%^&*()-=+_[]{}#~'@;:/?.>,<"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_line_with_a_triple_underscore_WHEN_syntax_check_THEN_invalid(self):
        # Arrange
        line = "VALID___MACRO=thing"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertFalse(result)
