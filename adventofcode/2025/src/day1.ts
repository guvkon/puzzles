import { generateMain, getInputStrings } from "./framework";

// Puzzle config.
const DAY = 1;
const SAMPLE_ANSWER_1 = 3;
const SAMPLE_ANSWER_2 = 6;

// Types.
type Rotation = {
    direction: 'L' | 'R';
    number: number;
}

type Input = Rotation[];


// Parse input.
const parseInput = (input: string): Input =>
    input.split('\n').map((line) => {
        const match = /^([RL])(\d+)$/gm.exec(line);
        if (!match) return null;

        return {
            direction: match[1],
            number: Number(match[2]),
        } as Rotation;
    }).filter((value: Rotation | null): value is Rotation => value !== null)


// Solve.
const solve1 = (input: Input): number => {
    let count = 0;
    let current = 50;

    input.forEach(({ direction, number }) => {
        // Rotate
        current += (direction === 'R' ? 1 : -1) * number;
        current = current % 100;
        if (current < 0) {
            current += 100;
        }

        // Count
        if (current === 0) {
            count += 1;
        }
    })

    return count;
};

const solve2 = (input: Input): number => {
    let count = 0;
    let current = 50;

    let previous = current;
    input.forEach(({ direction, number }) => {
        const fullRotations = Math.floor(number / 100); // Full rotations.
        const leftOverRotations = number % 100;
        count += fullRotations;
        if (leftOverRotations == 0) {
            return;
        }

        // Rotate
        current += (direction === 'R' ? 1 : -1) * leftOverRotations;
        if (current > 99) {
            current -= 100;
            count += 1;
        } else if (current < 0) {
            current += 100;
            if (previous !== 0) {
                count += 1;
            }
        } else if (current === 0) {
            count += 1;
        }

        previous = current;
    })

    return count;
};


// Main.
generateMain(parseInput, solve1, solve2)(...await getInputStrings(DAY), SAMPLE_ANSWER_1, SAMPLE_ANSWER_2);
