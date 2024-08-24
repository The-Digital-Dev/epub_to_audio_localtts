import logging
import os

from audiobook_generator.book_parsers.base_book_parser import get_book_parser
from audiobook_generator.config.general_config import GeneralConfig
from audiobook_generator.core.audio_tags import AudioTags
from audiobook_generator.tts_providers.coqui_tts_provider import CoquiTTSProvider

logger = logging.getLogger(__name__)

def confirm_conversion():
    print("Do you want to continue? (y/n)")
    answer = input()
    if answer.lower() != "y":
        print("Aborted.")
        exit(0)

def get_total_chars(chapters):
    total_characters = 0
    for title, text in chapters:
        total_characters += len(text)
    return total_characters

class AudiobookGenerator:
    def __init__(self, config: GeneralConfig):
        self.config = config
        logger.setLevel(config.log)

    def __str__(self) -> str:
        return f"{self.config}"

    def run(self):
        try:
            book_parser = get_book_parser(self.config)
            tts_provider = CoquiTTSProvider(self.config)  # Pass config to CoquiTTSProvider

            os.makedirs(self.config.output_folder, exist_ok=True)
            chapters = book_parser.get_chapters("\n\n")  # Coqui TTS doesn't need a special break string
            chapters = [(title, text) for title, text in chapters if text.strip()]

            logger.info(f"Chapters count: {len(chapters)}.")

            # Validate chapter start and end indices
            if self.config.chapter_start < 1 or self.config.chapter_start > len(chapters):
                raise ValueError(
                    f"Chapter start index {self.config.chapter_start} is out of range. Check your input."
                )
            if self.config.chapter_end < -1 or self.config.chapter_end > len(chapters):
                raise ValueError(
                    f"Chapter end index {self.config.chapter_end} is out of range. Check your input."
                )
            if self.config.chapter_end == -1:
                self.config.chapter_end = len(chapters)
            if self.config.chapter_start > self.config.chapter_end:
                raise ValueError(
                    f"Chapter start index {self.config.chapter_start} is larger than chapter end index {self.config.chapter_end}. Check your input."
                )

            logger.info(f"Converting chapters from {self.config.chapter_start} to {self.config.chapter_end}.")

            total_characters = get_total_chars(chapters)
            logger.info(f"✨ Total characters in selected book: {total_characters} ✨")

            if self.config.no_prompt:
                logger.info(f"Skipping prompt as passed parameter no_prompt")
            elif self.config.preview:
                logger.info(f"Skipping prompt as in preview mode")
            else:
                confirm_conversion()

            for idx, (title, text) in enumerate(chapters, start=1):
                if idx < self.config.chapter_start:
                    continue
                if idx > self.config.chapter_end:
                    break
                logger.info(
                    f"Converting chapter {idx}/{len(chapters)}: {title}, characters: {len(text)}"
                )

                if self.config.output_text:
                    text_file = os.path.join(self.config.output_folder, f"{idx:04d}_{title}.txt")
                    with open(text_file, "w", encoding='utf-8') as file:
                        file.write(text)

                if self.config.preview:
                    continue

                output_file = os.path.join(self.config.output_folder,
                                           f"{idx:04d}_{title}.mp3")

                audio_tags = AudioTags(title, book_parser.get_book_author(), book_parser.get_book_title(), idx)
                tts_provider.text_to_speech(  # Updated method call to text_to_speech
                    text,
                    output_file,
                    audio_tags  # Pass audio_tags
                )
                logger.info(
                    f"✅ Converted chapter {idx}/{len(chapters)}: {title}"
                )
            logger.info(f"All chapters converted. 🎉🎉🎉")

        except KeyboardInterrupt:
            logger.info("Job stopped by user.")
            exit()
