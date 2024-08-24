class GeneralConfig:
    def __init__(self, args):
        # General arguments
        self.input_file = args.input_file
        self.output_folder = args.output_folder
        self.preview = args.preview
        self.output_text = args.output_text
        self.log = args.log
        self.no_prompt = args.no_prompt
        self.title_mode = args.title_mode

        # Book parser specific arguments
        self.newline_mode = args.newline_mode
        self.chapter_start = args.chapter_start
        self.chapter_end = args.chapter_end
        self.remove_endnotes = args.remove_endnotes

        # TTS provider: Coqui TTS specific arguments
        # Comment out or remove this if tts isn't needed
        # self.tts = args.tts

        self.language = args.language
        self.voice_name = args.voice_name  # Could be used to select different voices within a model
        self.output_format = args.output_format
        self.model_name = args.model_name  # For selecting the Coqui TTS model

    def __str__(self):
        return ', '.join(f"{key}={value}" for key, value in self.__dict__.items())
