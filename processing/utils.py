import logging
import re
from typing import Union

from geopy.geocoders import Nominatim
from pandas.core.series import Series

MSG_FORMAT = '%(asctime)s - %(levelname)s - %(module)s - %(message)s'

logging.basicConfig(format=MSG_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Utils:

    def is_row_empty(self, row: Series) -> bool:
        logger.debug('begin is_row_empty()')
        for cell in row:
            if cell[0] == cell[0]:
                return False
        return True

    def parse_dms(self, dms: str) -> Union[str, float]:
        logger.debug(f'begin parse_dms({dms})')
        if not dms:
            return 'NULL'
        parts = re.split(r'[^-?\d\w\.]', dms.replace(" ", "").replace("''", "\""))
        return self.__dms2dd(parts[0], parts[1], parts[2], parts[3])

    def get_country_by_lat_long(self, latitude: str, longitude: str) -> str:
        logger.debug(f'begin get_country_by_lat_long({latitude, longitude}')
        geolocator = Nominatim(user_agent="curl/7.64.1")
        coordinate = f'{self.parse_dms(latitude)}, {self.parse_dms(longitude)}'
        location = geolocator.reverse(coordinate)
        address = location.raw['address']
        country = address.get('country', '')
        logger.debug(f'enc get_country_by_lat_long. Found: {country}')
        return country

    def __dms2dd(self, degrees: str, minutes: str, seconds: str, direction: str) -> float:
        logger.debug(f'being __dms2dd({degrees}, {minutes}, {seconds}, {direction}')
        valid_directions = ("N", "S", "E", "W")
        if not direction.upper() in valid_directions:
            raise Exception(f"Invalid direction [{direction}]. Direction must be {valid_directions}")
        if direction.upper() in ("N", "S") and (int(degrees) < 0 or int(degrees) > 90):
            raise Exception(f"Invalid degrees supplied [{degrees}]. Degrees north or south cannot be less than 0° nor "
                            f"greater than 90°")
        if int(degrees) < 0 or int(degrees) > 180:
            raise Exception(f"Invalid degrees supplied [{degrees}]. Degrees east or west cannot be less than 0° nor "
                            f"greater than 180°")
        if int(minutes) < 0 or int(minutes) > 60:
            raise Exception(f"Invalid minutes supplied [{minutes}]. Minutes cannot be less than 0' nor greater than "
                            f"60'")
        if float(seconds) < 0 or float(seconds) > 60:
            raise Exception(f"Invalid seconds supplied [{seconds}]. Seconds cannot be less than 0\" nor greater than "
                            f"60\"")

        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd
