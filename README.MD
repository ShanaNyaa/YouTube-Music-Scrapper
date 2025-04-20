# YouTube Music Scraper

This script extracts song title and artist information from a list of YouTube Music URLs provided in a text file.

## Prerequisites

-   Python 3.x
-   `requests` library: Used for making HTTP requests to fetch the content of the YouTube Music pages.
-   `beautifulsoup4` library: Used for parsing the HTML content and extracting the desired information.

## Installation

1.  Make sure you have Python 3.x installed.
2.  Install the required libraries using pip:

    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

1.  Create a text file named `urls.txt` in the same directory as the `youtube_scraper.py` script.
2.  Add the YouTube Music URLs you want to extract information from to the `urls.txt` file, one URL per line.
3.  Run the `youtube_scraper.py` script:

    ```bash
    python youtube_scraper.py
    ```

4.  The script will read the URLs from `urls.txt`, extract the song title and artist information, and save the results to a file named `urls_results.txt` in the same directory.

## Output

The `urls_results.txt` file will contain the extracted information in the following format:

```
URL | Title | Artist
---|---|---
https://music.youtube.com/watch?v=xxxxxxxxxxx | Song Title 1 | Artist Name 1
https://music.youtube.com/watch?v=yyyyyyyyyyy | Song Title 2 | Artist Name 2
...
```

If the script encounters an error while extracting information from a URL, it will log the error in the output file.

## Notes

-   The script assumes that the `urls.txt` file is located in the same directory as the `youtube_scraper.py` script.
-   The script uses UTF-8 encoding for both input and output files to handle a wide range of characters.
-   The script extracts the song title from the `<meta name="title" content="...">` tag and the artist name from the `<meta property="og:video:tag" content="...">` tag in the HTML source code of the YouTube Music page.