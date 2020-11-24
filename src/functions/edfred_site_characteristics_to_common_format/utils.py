import re


class Utils:
    def parse_dms(self, dms):
        parts = re.split('[^-?\d\w\.]', dms)
        return self._dms2dd(parts[0], parts[1], parts[2], parts[3])

    def _dms2dd(self, degrees, minutes, seconds, direction):
        valid_directions = ("N", "S", "E", "W")
        if not direction.upper() in valid_directions:
            raise Exception(f"Invalid direction [{direction}]. Direction must be {valid_directions}")
        if direction.upper() in ("N", "S") and (int(degrees) < 0 or int(degrees) > 90):
            raise Exception(f"Invalid degrees supplied [{degrees}]. Degrees north or south cannot be less than 0 nor"
                            f"greater than 90")
        if int(degrees) < 0 or int(degrees) > 180:
            raise Exception(f"Invalid degrees supplied [{degrees}]. Degrees east or west cannot be less than 0 nor "
                            f"greater than 180")
        if int(minutes) < 0 or int(minutes) > 60:
            raise Exception(f"Invalid minutes supplied [{minutes}]. Minutes cannot be less than 0 nor greater than 60")
        if float(seconds) < 0 or float(seconds) > 60:
            raise Exception(f"Invalid seconds supplied [{seconds}]. Seconds cannot be less than 0 nor greater than 60")

        dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60);
        if direction == 'S' or direction == 'W':
            dd *= -1
        return dd

    def striplist(self, l):
        return [x.strip() for x in l]
