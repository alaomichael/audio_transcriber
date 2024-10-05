import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import requests
import zipfile

# Assuming the download_ffmpeg function is in a file named 'app.py'
from app import download_ffmpeg

class TestDownloadFFmpeg(unittest.TestCase):

    @patch('requests.get')  # Mock the requests.get call
    @patch('builtins.open', new_callable=mock_open)  # Mock the open() call
    @patch('zipfile.is_zipfile')  # Mock the zipfile.is_zipfile call
    @patch('zipfile.ZipFile')  # Mock the zipfile.ZipFile class
    @patch('os.remove')  # Mock the os.remove call
    @patch('os.chmod')  # Mock the os.chmod call
    def test_download_ffmpeg(self, mock_chmod, mock_remove, mock_zipfile, mock_is_zipfile, mock_open_file, mock_requests_get):
        # Mock the response from requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'fake-content'
        mock_requests_get.return_value = mock_response

        # Mock the zipfile check to return True
        mock_is_zipfile.return_value = True

        # Mock the behavior of ZipFile's extractall
        mock_zipfile_instance = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zipfile_instance

        # Call the function to test
        download_ffmpeg()

        # Assertions to check if the mocks were called correctly
        mock_requests_get.assert_called_once_with("https://drive.google.com/uc?export=download&id=1gKl_HiRnh8nKOrfm1FQyhHPoANA8GumK")
        mock_open_file.assert_called_once_with("ffmpeg.zip", "wb")
        mock_is_zipfile.assert_called_once_with("ffmpeg.zip")
        mock_zipfile_instance.extractall.assert_called_once_with("ffmpeg_binaries")
        mock_remove.assert_called_once_with("ffmpeg.zip")

        # Ensure chmod is only called on non-Windows systems
        if os.name != 'nt':
            mock_chmod.assert_called_once_with("ffmpeg_binaries/ffmpeg", 0o755)
        else:
            mock_chmod.assert_not_called()

if __name__ == '__main__':
    unittest.main()
