def calculate_score_small(rolls):
    # 10 frames + space to store up to 2 bonus throws = 12 "frames" (if first bonus throw is a strike)
    frame_rolls = [0] * (2 * (10 + 2))

    # Clean up and normalize input
    # 1. Translate 'X' to 'X-', so each frame is 2 characters
    # 2. Translate '-' to '0', so we can use int() for those
    # 3. Remove all characters outside of the (cleaned up) input alphabet
    rolls = ''.join(roll for roll in rolls.replace('X', 'X-').replace('-', '0') if roll in 'X/0123456789')

    # Translate characters into numbers, resolving spare scores
    for i, roll in enumerate(rolls):
        if roll == 'X':
            frame_rolls[i] = 10
        elif roll == '/':
            frame_rolls[i] = (10 - frame_rolls[i-1])
        else:
            frame_rolls[i] = int(roll)

    score = 0

    # Only the first 10 frames are scored (rest is bonus rolls)
    for frame in range(10):
        i = 2 * frame

        # Base score, first and second roll of frame
        score += frame_rolls[i] + frame_rolls[i+1]

        # This frame was a strike or a spare, add next roll (= always first of next frame)
        if frame_rolls[i] + frame_rolls[i+1] == 10:
            score += frame_rolls[i+2]

        # This frame was a strike, add second-next roll (depends on what the next roll was)
        if frame_rolls[i] == 10:
            if frame_rolls[i+2] == 10:
                # Next was a strike, second-next roll is first roll of second-next frame
                score += frame_rolls[i+2+2]
            else:
                # Next was not a strike, second-next roll is second roll of next frame
                score += frame_rolls[i+2+1]

    return score
