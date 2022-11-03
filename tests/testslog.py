from tkinter.filedialog import test
import unittest
import pandas as pd


class TestGetInformations(unittest.TestCase):
    def test_load_store(self):
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
