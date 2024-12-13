class Formatter:
    @staticmethod
    def format_bytes(bytes_num: float) -> str:
        suffixes = ['B', 'KB', 'MG', 'GB']
        index = 0

        while bytes_num > 1024 and index < len(suffixes) - 1:
            bytes_num /= 1024
            index += 1

        return "{:.3} {}".format(bytes_num, suffixes[index])
