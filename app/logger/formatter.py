import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'WARNING': '\033[93m',
        'INFO': '\033[92m',
        'DEBUG': '\033[94m',
        'CRITICAL': '\033[91m',
        'ERROR': '\033[91m',
        'RESET': '\033[0m'
    }

    def format(self, record):
        log_fmt = self._fmt
        color_start = self.COLORS.get(record.levelname, '')
        color_reset = self.COLORS['RESET']
        log_fmt = log_fmt.replace('%(levelname)s', f'{color_start}%(levelname)s{color_reset}')

        formatter = logging.Formatter(log_fmt, self.datefmt)
        return formatter.format(record)
