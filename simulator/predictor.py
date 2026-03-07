import math

def predict_cooling_time(current_temp, set_temp, cooling_rate):

    if current_temp <= set_temp:
        return 0

    try:
        # Solve exponential equation
        t = (1 / cooling_rate) * math.log(
            (current_temp - set_temp) / 0.05
        )
        return max(t, 0)
    except:
        return 0
