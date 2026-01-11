
def find_min_moves():
    degrees_in_circle = 360
    increment_40 = 360 // 40  # 9 degrees per move
    increment_45 = 360 // 45  # 8 degrees per move

    # Initialize a list to store the results
    results = [{"moves": float('inf'), "increments_40": 0, "increments_45": 0} for _ in range(degrees_in_circle)]
    results[0] = {"moves": 0, "increments_40": 0, "increments_45": 0}  # Start at 0° with no moves

    # Explore combinations of moves, including forward and backward
    for moves_40 in range(-40, 40):
        for moves_45 in range(-45, 45):
            # Calculate the net rotation
            net_degrees = (moves_40 * increment_40) + (moves_45 * increment_45)

            # Normalize to [0, 360)
            net_degrees %= degrees_in_circle

            # Calculate the total number of moves
            total_moves = abs(moves_40) + abs(moves_45)

            # If this is the first time or a better combination is found
            if total_moves < results[net_degrees]["moves"]:
                results[net_degrees] = {
                    "moves": total_moves,
                    "increments_40": moves_40,
                    "increments_45": moves_45,
                }

    return results

def main():
    results = find_min_moves()
    for degree, data in enumerate(results):
        direction_40 = "forward" if data["increments_40"] >= 0 else "backward"
        direction_45 = "forward" if data["increments_45"] >= 0 else "backward"
        print(
            f"Degree: {degree}° requires {data['moves']} moves "
            f"({abs(data['increments_40'])} increments of 40-side {direction_40}, "
            f"{abs(data['increments_45'])} increments of 45-side {direction_45})."
        )

if __name__ == "__main__":
    main()
