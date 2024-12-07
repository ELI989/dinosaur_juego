import unittest
import sys
import os

# Añadir la raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.dinosaur import Dinosaur


class TestDinosaur(unittest.TestCase):
    def setUp(self):
        self.dino = Dinosaur()

    def test_initial_position(self):
        self.assertEqual(self.dino.dino_rect.x, 80)
        self.assertEqual(self.dino.dino_rect.y, 310)

    def test_jump_velocity(self):
        self.assertEqual(self.dino.jump_vel, 8.5)

    def test_duck_logic(self):
        self.dino.dino_duck = True
        self.dino.update()
        self.assertTrue(self.dino.dino_duck)
        self.assertFalse(self.dino.dino_jump)

if __name__ == "__main__":
    unittest.main()
