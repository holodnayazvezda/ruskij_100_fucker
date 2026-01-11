import logging
import sys

logging.basicConfig(
    filename='log',
    filemode='a',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)


def print_to_file(*args, sep=' ', end='\n', file=None, flush=False):
    """
    Перехватывает вызовы print и записывает их в лог.
    Если указан явный file, отличный от sys.stdout/sys.stderr, использует оригинальный print.
    """
    if file is not None and file is not sys.stdout and file is not sys.stderr:
        return print(*args, sep=sep, end=end, file=file, flush=flush)
    message = sep.join(map(str, args))
    print(message)
    # Убираем завершающий перенос, logging добавит метку времени
    logging.debug(message)
    if flush:
        for handler in logging.root.handlers:
            try:
                handler.flush()
            except Exception:
                pass
