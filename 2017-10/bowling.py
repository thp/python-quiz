def parse_frames(rolls):
    frames = [[0, 0] for _ in range(12)]

    frame = 0
    roll_in_frame = 0

    for roll in rolls:
        if roll == 'X':
            assert roll_in_frame == 0
            frames[frame][0] = 10
            frame += 1
        else:
            if roll == '/':
                assert roll_in_frame == 1
                value = 10 - frames[frame][0]
            elif roll == '-':
                value = 0
            else:
                try:
                    value = int(roll)
                except ValueError:
                    continue

            frames[frame][roll_in_frame] = value

            roll_in_frame += 1
            if roll_in_frame == 2:
                frame += 1
                roll_in_frame = 0

    return frames


def score_base(frames):
    return sum(sum(frame) for frame in frames[:10])


def is_spare(frame):
    return frame[0] != 10 and sum(frame) == 10


def is_strike(frame):
    return frame[0] == 10


def score_spare_bonus(frames):
    score = 0
    for idx, frame in enumerate(frames[:10]):
        if is_spare(frame):
            score += frames[idx+1][0]
    return score


def score_strike_bonus(frames):
    score = 0
    for idx, frame in enumerate(frames[:10]):
        if is_strike(frame):
            score += frames[idx+1][0]
            if is_strike(frames[idx+1]):
                score += frames[idx+2][0]
            else:
                score += frames[idx+1][1]
    return score


def calculate_score(rolls):
    frames = parse_frames(rolls)
    return score_base(frames) + score_spare_bonus(frames) + score_strike_bonus(frames)
