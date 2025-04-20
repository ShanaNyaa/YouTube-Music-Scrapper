from bs4 import BeautifulSoup
import requests
import os
import argparse

def get_youtube_music_info(url):
    """
    Extracts the song title and artist name from a YouTube Music URL.

    Args:
        url: The YouTube Music URL (e.g., "https://music.youtube.com/watch?v=DO_aopUeFnw&si=Lna4_RZmKaInFqUi").

    Returns:
        A tuple containing the song title and artist name, or (None, None) if extraction fails.
    """
    try:
        # Use BeautifulSoup and requests to extract information
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup.prettify())  # For debugging: print the HTML content

        # Look for meta tags that often contain title and artist info
        title_element = soup.find("meta", attrs={"name": "title"})
        if title_element:
            title = title_element["content"]
            # Remove " - YouTube Music" suffix if present
            if title.endswith(" - YouTube Music"):
                title = title[:-len(" - YouTube Music")]
        else:
            title = None  # if can't find a title, assign as None

        # Attempt to get the artist name from the "og:video:tag" meta tag
        artist_element = soup.find("meta", property="og:video:tag")
        if artist_element:
            artist = artist_element["content"]
        else:
            artist = "Unknown Artist" # Fallback if artist tag not found

        if title:
            return title, artist

        return None, None  # if soup can't find anything

    except requests.exceptions.RequestException as e:
        print(f"Error during requests: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

# Main execution block
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--format", help="Specify output format", choices=["txt", "csv"], default="txt")
    parser.add_argument("-o", "--output", help="Specify output file name", default="urls_results")

    args = parser.parse_args()
    output_format = args.format

    if output_format == "csv":
        output_file = args.output + ".csv"
    else:
        output_file = args.output + ".txt"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(script_dir, 'urls.txt')
    output_file_path = os.path.join(script_dir, output_file) # Define output file path

    print(f"Looking for URL file at: {input_file_path}")

    try:
        # Specify encoding='utf-8' for both input and output files
        with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
            urls = infile.readlines()

            if not urls:
                print(f"The file '{input_file_path}' is empty.")
            else:
                print(f"\nProcessing URLs from '{input_file_path}'...")

                if output_format == "csv":
                    outfile.write("URL,Title,Artist\n")
                else:
                    outfile.write("URL | Title | Artist\n") # Write header to output file
                    outfile.write("---|---|---\n")

                for url in urls:
                    url = url.strip()
                    if url:
                        print(f"\nProcessing URL: {url}")
                        title, artist = get_youtube_music_info(url)
                        if title and artist:
                            print(f"  Song Title: {title}")
                            print(f"  Artist: {artist}")
                            # Write result to output file

                            if output_format == "csv":
                                outfile.write(f"{url},{title},{artist}\n")
                            else:
                                outfile.write(f"{url} | {title} | {artist}\n")
                        else:
                            print("Could not extract song information for this URL.")

                            # Write error to output file
                            if output_format == "csv":
                                outfile.write(f"{url},Error,Could not extract info\n")
                            else:
                                outfile.write(f"{url} | Error | Could not extract info\n") # Log errors too

                print(f"\nResults saved to: {output_file_path}") # Inform user about output file

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file_path}'. Please ensure 'urls.txt' exists in the same directory as the script.")
    except Exception as e:
        print(f"An error occurred: {e}")
