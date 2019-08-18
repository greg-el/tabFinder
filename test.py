import unittest
import main

class Test(unittest.TestCase):
    def test_get_song_data(self):
        with open("test_song_json_data", "r") as f:
            data = f.read()

        self.assertEqual("test content with tags", main.get_song_data(data))


    def test_get_songs_list(self):
        with open("test_song_list_json_data", "r") as f:
            data = f.read()

        test_data = main.get_songs_list(data)
        self.assertEqual(test_data[0]["index"], 0)
        self.assertEqual(test_data[0]["song_name"], "test_song")
        self.assertEqual(test_data[0]["artist"], "test_artist")
        self.assertEqual(test_data[0]["url"], "test_tab_url")
        self.assertEqual(test_data[0]["type"], "test_type")

        self.assertEqual(test_data[1]["index"], 1)
        self.assertEqual(test_data[1]["song_name"], "test_song_marketing")
        self.assertEqual(test_data[1]["artist"], "test_artist_marketing")
        self.assertEqual(test_data[1]["url"], "test_tab_url_marketing")
        self.assertEqual(test_data[1]["type"], "test_type_marketing")



if __name__ == "__main__":
    unittest.main()