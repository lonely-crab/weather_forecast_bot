def _choose_emoji(current_weather: dict) -> dict:
    keys = [
        "cloudCover",
        "windSpeed",
        "rainAccumulation",
        "sleetAccumulation",
        "snowAccumulation",
        "precipitationProbability",
    ]
    weather_conditions = {
        "cloudCover": [0.1, 50.0, 100.0],
        "windSpeed": [1.0, 10.0, 20.0],
        "rainAccumulation": [0.0, 1.0, 2.0],
        "sleetAccumulation": [0.0, 1.0, 2.0],
        "snowAccumulation": [0.0, 1.0, 2.0],
    }
    weather_emojis = {
        "cloudCover": ["\u2600\uFE0F", "\U0001f325\uFE0F", "\u2601\uFE0F"],
        "windSpeed": ["\U0001f343", "\U0001f4a8", "\U0001f32c\uFE0F"],
        "rainAccumulation": ["\U0001f302", "\U0001f327\uFE0F", "\u26C8\uFE0F"],
        "sleetAccumulation": [
            "\u2744\uFE0F",
            "\u2603\uFE0F",
            "\U0001f328\uFE0F",
        ],
        "snowAccumulation": [
            "\u2744\uFE0F",
            "\u2603\uFE0F",
            "\U0001f328\uFE0F",
        ],
    }
    chosen_emojis = {}
    for key in keys:
        if key.endswith("Accumulation"):
            continue
        try:
            diff1 = abs(current_weather[key] - weather_conditions[key][0])
            diff2 = abs(current_weather[key] - weather_conditions[key][1])
            diff3 = abs(current_weather[key] - weather_conditions[key][2])
        except KeyError:
            continue

        min_diff = min(diff1, diff2, diff3)
        if min_diff == diff1:
            chosen_emojis[key] = weather_emojis[key][0]
        elif min_diff == diff2:
            chosen_emojis[key] = weather_emojis[key][1]
        else:
            chosen_emojis[key] = weather_emojis[key][2]

    max_key, max_accumulation = (
        "rainAccumulation",
        current_weather["rainAccumulation"],
    )

    for key in [key for key in keys if key.endswith("Accumulation")]:
        if current_weather[key] > max_accumulation:
            max_accumulation = current_weather[key]
            max_key = key

    diff1 = abs(current_weather[max_key] - weather_conditions[max_key][0])
    diff2 = abs(current_weather[max_key] - weather_conditions[max_key][1])
    diff3 = abs(current_weather[max_key] - weather_conditions[max_key][2])

    min_diff = min(diff1, diff2, diff3)
    if min_diff == diff1:
        chosen_emojis[max_key] = weather_emojis[max_key][0]
    elif min_diff == diff2:
        chosen_emojis[max_key] = weather_emojis[max_key][1]
    else:
        chosen_emojis[max_key] = weather_emojis[max_key][2]

    return chosen_emojis


class Conditions:
    @classmethod
    def choose_emoji(cls, current_weather: dict) -> dict:
        return _choose_emoji(current_weather)
