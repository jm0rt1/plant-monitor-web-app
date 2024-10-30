import unittest
from src.main.app.visualization.implementations.visualizer import Visualizer


class TestVisualizer(unittest.TestCase):
    def setUp(self):
        self.visualizer = Visualizer()

    def test_generate_plot_no_data(self):
        graph = self.visualizer.generate_plot([])
        self.assertIn("No data available", graph)

    def test_generate_plot_with_data(self):
        sensor_data = [
            {
                'device_id': 'device123',
                'timestamp': '2023-01-01T12:00:00',
                'data': {'temperature': 25, 'humidity': 50}
            }
        ]
        graph = self.visualizer.generate_plot(sensor_data)
        self.assertIn("<div", graph)  # Basic check to see if HTML is returned


if __name__ == '__main__':
    unittest.main()
