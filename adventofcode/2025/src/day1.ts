// Types.
type Rotation = {
    direction: 'L' | 'R';
    number: number;
}

type Input = Rotation[];


// Parse input.
const parseInput = (input: string): Rotation[] =>
    input.split('\n').map((line) => {
        const match = /^([RL])(\d+)$/gm.exec(line);
        if (!match) return null;

        return {
            direction: match[1],
            number: Number(match[2]),
        } as Rotation;
    }).filter((value: Rotation | null): value is Rotation => value !== null)


// Solve 1.
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


// Solve 1.
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
const main = (input: string, sampleInput: string, sampleAnswer1: number, sampleAnswer2: number) => {
    // Parse inputs.
    const parsedSampleInput = parseInput(sampleInput);
    const parsedInput = parseInput(input);

    // Answers
    let answer: number;

    // Part 1.
    answer = solve1(parsedSampleInput);
    if (answer !== sampleAnswer1) {
        console.error(`Wrong sample answer for part 1! Got: ${answer}, correct: ${sampleAnswer1}`);
        return;
    }

    answer = solve1(parsedInput);
    console.log(`Answer for part 1: ${answer}`);

    // Part 2.
    answer = solve2(parsedSampleInput);
    if (answer !== sampleAnswer2) {
        console.error(`Wrong sample answer for part 2! Got: ${answer}, correct: ${sampleAnswer2}`);
        return;
    }

    answer = solve2(parsedInput);
    console.log(`Answer for part 2: ${answer}`);
};


// Execute main.
main(
    await Bun.file("input/day1.txt").text(),
    await Bun.file("input/day1_sample.txt").text(),
    3,
    6
);
