import logging
import os
import subprocess
import time

from TTS.api import TTS

from audiobook_generator.core.audio_tags import AudioTags
from audiobook_generator.config.general_config import GeneralConfig
from audiobook_generator.core.utils import split_text, set_audio_tags
from audiobook_generator.tts_providers.base_tts_provider import BaseTTSProvider

logger = logging.getLogger(__name__)

class CoquiTTSProvider(BaseTTSProvider):
    def __init__(self, config: GeneralConfig):
        logger.setLevel(config.log)
        self.model_name = config.model_name or "tts_models/en/ljspeech/vits"
        self.output_format = config.output_format or "mp3"
        self.language = config.language  # Ensure language is passed to split_text
        super().__init__(config)

        self.model = TTS(self.model_name)  # Initialize Coqui TTS model

    def __str__(self) -> str:
        return f"CoquiTTSProvider using model: {self.model_name}"

    def text_to_speech(self, text: str, output_file: str, audio_tags: AudioTags):
        # Coqui TTS doesn't have strict character limits, but we'll split the text for consistency
        text_chunks = split_text(text, max_chars=5000, language=self.language)  # Pass required arguments

        audio_segments = []

        for i, chunk in enumerate(text_chunks, 1):
            logger.debug(
                f"Processing chunk {i} of {len(text_chunks)}, length={len(chunk)}, text=[{chunk}]"
            )
            logger.info(
                f"Processing chapter-{audio_tags.idx} <{audio_tags.title}>, chunk {i} of {len(text_chunks)}"
            )

            logger.debug(f"Text: [{chunk}], length={len(chunk)}")

            # Generate audio for each chunk
            temp_output_file = f"{output_file}_part_{i}.wav"
            self.model.tts_to_file(text=chunk, file_path=temp_output_file)

            audio_segments.append(temp_output_file)

        # Combine all chunks into a single file
        if len(audio_segments) > 1:
            combined_output = f"{output_file}.wav"
            os.system(f"sox {' '.join(audio_segments)} {combined_output}")
            for segment in audio_segments:
                os.remove(segment)  # Clean up temporary files
        else:
            combined_output = audio_segments[0]

        final_output = f"{output_file}.{self.output_format}"

        # Introduce a 5-second delay before automatically confirming the overwrite
        logger.info(f"Waiting 10 seconds before overwriting the file {final_output}...")
        time.sleep(10)  # Wait for 10 seconds
        
        # Use the -y flag to automatically confirm the overwrite
        ffmpeg_command = f"ffmpeg -y -i {combined_output} {final_output}"
        subprocess.call(ffmpeg_command, shell=True)
        
        os.remove(combined_output)  # Clean up the combined WAV file

        set_audio_tags(final_output, audio_tags)

    def get_break_string(self):
        return "\n\n"  # Simple break string

    def get_output_file_extension(self):
        return self.output_format

    def validate_config(self):
        # Coqui TTS doesn't require strict validation as in the OpenAI example
        pass

    def estimate_cost(self, total_chars):
        # Coqui TTS is free, so no cost estimation needed
        return 0.0