import os
import logging
from glob import glob


def fill_date_template(template_str, date_str):

    yyyy_str, mm_str, dd_str, ddd_str = tuple(date_str.split('-'))

    if 'DDD' in template_str:
        return template_str.replace(
            'YYYY', yyyy_str).replace('DDD', ddd_str)
    else:
        return template_str.replace(
            'YYYY', yyyy_str).replace('MM', mm_str).replace('DD', dd_str)


def find_file(datadir, filestr):

    pattern = os.path.join(os.path.expandvars(datadir), filestr)
    files = glob(pattern)

    if len(files) == 0:
        raise Exception('no file matches for %s' % pattern)
    if len(files) > 1:
        raise Exception('more than one file match %s' % pattern)

    filename = files[0]
    logging.info(filename)

    return filename


