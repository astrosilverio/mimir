import unittest

class TestHandleCommand(unittest.TestCase):

    def test_hc_calls_correct_checks(self):
        pass

    def test_hc_calls_verb_success_if_checks_pass(self):
        pass

    def test_hc_calls_verb_failure_if_checks_fail(self):
        pass

    def test_hc_returns_sane_output_if_checks_pass(self):
        pass

    def test_hc_returns_sane_output_if_checks_fail(self):
        pass

class TestLegilimensIntegration(unittest.TestCase):

    def test_good_simple_command_returns_sane_output(self):
        pass

    def test_bad_simple_command_returns_sane_output(self):
        pass

    def test_good_complex_command_returns_sane_output(self):
        pass

    def test_bad_complex_command_returns_sane_output(self):
        pass

class TestStateIntegration(unittest.TestCase):

    def test_hc_state_changing_command_changes_state(self):
        pass

    def test_hc_non_state_changing_command_does_not_change_state(self):
        pass
