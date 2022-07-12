class WeatherStatus():
    @staticmethod
    def getEmojiStr(code):
        if code == 0:
            return " :sunny: "
        elif code == 1:
            return " :mostly_sunny: "
        elif code == 2:
            return " :partly_sunny: "
        elif code == 3:
            return " :cloud: "
        elif code == 45 or code == 48:
            return " :fog: "
        elif code == 51 or code == 53 or code == 55:
            return " :rain_cloud: "
        elif code == 56 or code == 53 or code == 66 or code == 67:
            return " :snow_cloud: "
        elif code == 61:
            return " :closed_umbrella: "
        elif code == 63:
            return " :umbrella: "
        elif code == 65:
            return " :umbrella_with_rain_drops: "
        elif code == 71 or code == 73:
            return " :snow_cloud: "
        elif code == 75 or code == 77:
            return " :snowman_without_snow: "
        elif code == 80 or code == 81 or code == 82:
            return " :ocean: "
        elif code == 85 or code == 86:
            return " :snowflake: "
        elif code == 96 or code == 99:
            return " :zap: "
        else:
            return " :t-rex: "