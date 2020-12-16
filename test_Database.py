from unittest import TestCase
import unittest
from Database import Database


class TestDatabase(unittest.TestCase):
    def test_get_by_url(self):
        result = BddConnection.get_by_url(
            "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3"
            "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1")
        self.assertTrue(result)

        result = BddConnection.get_by_url(
            "GTX 360")
        self.assertFalse(result)

    def test_start(self):
        result = BddConnection.start()
        self.assertTrue(result)

    def test_new_categories(self):
        result = BddConnection.new_categories("Bendo")
        self.assertIsNone(result)

        result = BddConnection.new_categories(13456)
        self.assertFalse(result)

    def test_select_product(self):
        result = BddConnection.select_product()
        self.assertTrue(result)

    def test_get_cat_nom(self):
        result = BddConnection.get_cat_name()
        self.assertTrue(result)

    def test_select_categories(self):
        result = BddConnection.select_categories()
        self.assertTrue(result)

    def test_new_product(self):
        result = BddConnection.new_product(123, "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                                "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                                "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", "proc",
                                           186)
        self.assertFalse(result)

        result = BddConnection.new_product("nom", 123, "proc", 186)
        self.assertFalse(result)

        result = BddConnection.new_product("nom", "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                                  "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                                  "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", 123,
                                           186)
        self.assertFalse(result)

        result = BddConnection.new_product("nom", "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                                  "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                                  "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", "proc",
                                           "186")
        self.assertFalse(result)

        result = BddConnection.new_product("nom", "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                                  "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                                  "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", "proc",
                                           186)
        self.assertIsNone(result)

    def test_update_product(self):
        result = BddConnection.update_product("65", "nom",
                                              "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                              "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                              "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", "proc", 186)
        self.assertFalse(result)

        result = BddConnection.update_product(65, "nom", 123, "proc", 186)
        self.assertFalse(result)

        result = BddConnection.update_product(65, "nom",
                                              "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                              "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                              "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", 123,
                                              186)
        self.assertFalse(result)

        result = BddConnection.update_product(65, "nom",
                                              "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                              "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                              "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", "proc",
                                              "186")
        self.assertFalse(result)

        result = BddConnection.update_product(65, "nom",
                                              "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                              "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                              "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1", "proc",
                                              186)
        self.assertIsNone(result)

        result = BddConnection.update_product(1.5, "nom",
                                              "https://www.amazon.fr/MSI-GeForce-RTX-3060-TI/dp/B08NW32F74/ref"
                                              "=sr_1_1?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3 "
                                              "%95%C3%91&dchild=1&keywords=rtx+3060&qid=1608063810&sr=8-1",
                                              "proc",
                                              186)
        self.assertFalse(result)

    def test_update_cat(self):
        result = BddConnection.update_cat("65", "nom")
        self.assertFalse(result)

        result = BddConnection.update_cat(65, 123)
        self.assertFalse(result)

        result = BddConnection.update_cat(5000, 123)
        self.assertFalse(result)

        result = BddConnection.update_cat(65, "nom")
        self.assertIsNone(result)

    def test_delete_categories(self):
        result = BddConnection.delete_categories("65")
        self.assertFalse(result)

        result = BddConnection.delete_categories(355555)
        self.assertFalse(result)

        result = BddConnection.delete_categories(60)
        self.assertIsNone(result)

    def test_delete_product(self):
        result = BddConnection.delete_product("65")
        self.assertFalse(result)

        result = BddConnection.delete_product(355555)
        self.assertFalse(result)

        result = BddConnection.delete_product(60)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
