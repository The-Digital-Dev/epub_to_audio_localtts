import argparse
import logging
import os
import sys

from audiobook_generator.config.general_config import GeneralConfig
from audiobook_generator.core.audiobook_generator import AudiobookGenerator

# Print the received arguments for debugging
print("Received arguments:", sys.argv)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def handle_args():
    parser = argparse.ArgumentParser(description="Convert text book to audiobook")
    parser.add_argument("output_folder", help="Path to the output folder")
    parser.add_argument("input_file", nargs='?', help="Path to the EPUB file")
    
    parser.add_argument(
        "--log",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],  # Corrected
        default="INFO",
        help="Log level (default: INFO), can be DEBUG, INFO, WARNING, ERROR, CRITICAL",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Enable preview mode. In preview mode, the script will not convert the text to speech. Instead, it will print the chapter index, titles, and character counts.",
    )
    parser.add_argument(
        "--no_prompt",
        action="store_true",
        help="Don't ask the user if they wish to continue after processing. Useful for scripting.",
    )
    parser.add_argument(
        "--language",
        default="en-US",
        help="Language for the text-to-speech service (default: en-US). This helps in text splitting, especially for Chinese characters.",
    )
    parser.add_argument(
        "--newline_mode",
        choices=["single", "double", "none"],
        default="double",
        help="Choose the mode of detecting new paragraphs: 'single', 'double', or 'none'. 'single' means a single newline character, while 'double' means two consecutive newline characters. 'none' means all newline characters will be replaced with blanks so paragraphs will not be detected. (default: double, works for most ebooks but will detect fewer paragraphs for some ebooks)",
    )
    parser.add_argument(
        "--title_mode",
        choices=["auto", "tag_text", "first_few"],
        default="auto",
        help="Choose the parse mode for chapter title: 'tag_text' searches 'title','h1','h2','h3' tags for title, 'first_few' sets the first 60 characters as title, 'auto' automatically applies the best mode for the current chapter.",
    )
    parser.add_argument(
        "--chapter_start",
        default=1,
        type=int,
        help="Chapter start index (default: 1, starting from 1)",
    )
    parser.add_argument(
        "--chapter_end",
        default=-1,
        type=int,
        help="Chapter end index (default: -1, meaning to the last chapter)",
    )
    parser.add_argument(
        "--output_text",
        action="store_true",
        help="Enable Output Text. This will export a plain text file for each chapter specified and write the files to the output folder specified.",
    )
    parser.add_argument(
        "--remove_endnotes",
        action="store_true",
        help="This will remove endnote numbers from the end or middle of sentences. This is useful for academic books.",
    )
    parser.add_argument(
        "--voice_name",
        help="Specify the voice name for Coqui TTS.",
    )
    parser.add_argument(
        "--output_format",
        help="Output format for the text-to-speech service. Supported format depends on Coqui TTS settings.",
    )
    parser.add_argument(
        "--model_name",
        help="Specify the model name for Coqui TTS.",
    )

    args = parser.parse_args()

    # Ensure output folder exists
    if not os.path.isdir(args.output_folder):
        raise ValueError(f"The output folder '{args.output_folder}' does not exist.")

    # Automatically detect the EPUB file if not provided
    if not args.input_file:
        epub_files = [f for f in os.listdir(args.output_folder) if f.endswith('.epub')]
        if len(epub_files) == 1:
            args.input_file = os.path.join(args.output_folder, epub_files[0])
        elif len(epub_files) > 1:
            raise ValueError("Multiple EPUB files found in the output directory. Please specify one.")
        else:
            raise ValueError("No EPUB file found in the output directory.")

    return GeneralConfig(args)

def main():
    config = handle_args()
    logger.setLevel(config.log)
    AudiobookGenerator(config).run()

if __name__ == "__main__":
    main()
