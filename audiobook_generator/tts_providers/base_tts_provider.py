from typing import List

from audiobook_generator.config.general_config import GeneralConfig

TTS_COQUI = "coqui"

class BaseTTSProvider:  # Base interface for TTS providers
    # Base provider interface
    def __init__(self, config: GeneralConfig):
        self.config = config
        self.validate_config()

    def __str__(self) -> str:
        return f"{self.config}"

    def validate_config(self):
        raise NotImplementedError

    def text_to_speech(self, *args, **kwargs):
        raise NotImplementedError

    def estimate_cost(self, total_chars):
        return 0.0  # Coqui TTS is free

    def get_break_string(self):
        return "\n\n"  # Simple break string for text processing

    def get_output_file_extension(self):
        raise NotImplementedError

# Common support methods for all TTS providers
def get_supported_tts_providers() -> List[str]:
    return [TTS_COQUI]

def get_tts_provider(config) -> BaseTTSProvider:
    from audiobook_generator.tts_providers.coqui_tts_provider import CoquiTTSProvider
    return CoquiTTSProvider(config)
