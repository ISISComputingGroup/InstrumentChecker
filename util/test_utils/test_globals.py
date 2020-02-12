import unittest
from util.globals import GlobalsUtils
from mock import Mock


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

    def test_GIVEN_a_definition_where_ioc_name_is_not_present_WHEN_syntax_check_THEN_valid(self):
        # Arrange
        line = "ADDR1=1.2.3.4"

        # Act
        result = self.utils.check_syntax(line)

        # Assert
        self.assertTrue(result)

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
        line = "OOPS_TWO__DOUBLE__UNDERSCORES=GALIL_01__ADDR1=YES"

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
        line = "# OOPS_TWO__DOUBLE__UNDERSCORES=HELLO"

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

    def test_GIVEN_a_line_WHEN_macro_requested_for_correct_ioc_name_THEN_key_and_value_matches_input(self):
        # Arrange
        ioc_name = "MYIOC_01"
        macro = "macro"
        value = "01"
        line = "{}__{}={}".format(ioc_name, macro, value)

        self.utils.get_lines = Mock(return_value=[line])

        # Act
        result = self.utils.get_macros(ioc_name)

        # Assert
        self.assertEqual(len(list(result.keys())), 1)
        self.assertTrue(macro in result)
        self.assertEqual(result[macro], value)

    def test_GIVEN_a_line_WHEN_macro_requested_for_non_existant_ioc_THEN_no_macros_returned(self):
        # Arrange
        ioc_name = "MYIOC_01"
        macro = "macro"
        value = "01"
        line = "{}__{}={}".format(ioc_name, macro, value)

        self.utils.get_lines = Mock(return_value=[line])

        # Act
        result = self.utils.get_macros("not_" + ioc_name)

        # Assert
        self.assertEqual(len(list(result.keys())), 0)

    def test_GIVEN_a_line_WHEN_value_requested_for_correct_macro_name_THEN_key_and_value_matches_input(self):
        # Arrange
        ioc_name = "MYIOC_01"
        macro = "macro"
        value = "01"
        line = "{}__{}={}".format(ioc_name, macro, value)

        self.utils.get_lines = Mock(return_value=[line])

        # Act
        result = self.utils.get_values_of_macro(macro)

        # Assert
        self.assertEqual(len(list(result.keys())), 1)
        self.assertTrue(macro in result)
        self.assertEqual(result[macro], value)

    def test_GIVEN_a_line_WHEN_value_requested_for_incorrect_macro_name_THEN_no_values_returned(self):
        # Arrange
        ioc_name = "MYIOC_01"
        macro = "macro"
        value = "01"
        line = "{}__{}={}".format(ioc_name, macro, value)

        self.utils.get_lines = Mock(return_value=[line])

        # Act
        result = self.utils.get_values_of_macro("not_" + ioc_name)

        # Assert
        self.assertEqual(len(list(result.keys())), 0)

    def test_GIVEN_a_line_WHEN_sim_flag_is_set_on_THEN_return_true(self):
        #Arrange
        ioc_name = "MYIOC_01"
        macro = "DEVSIM"
        value = "1"
        line = "{}__{}={}".format(ioc_name, macro, value)

        self.utils.get_lines = Mock(return_value=[line])

        # Act
        result = self.utils.is_any_ioc_in_sim_mode()

        # Assert
        self.assertTrue(result)

    def test_GIVEN_a_line_WHEN_sim_flag_is_set_off_THEN_return_false(self):
        # Arrange
        ioc_name = "MYIOC_01"
        macro = "DEVSIM"
        value = "0"
        line = "{}__{}={}".format(ioc_name, macro, value)

        self.utils.get_lines = Mock(return_value=[line])

        # Act
        result = self.utils.is_any_ioc_in_sim_mode()

        # Assert
        self.assertFalse(result)
