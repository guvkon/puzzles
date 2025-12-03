import { generateMain, getInputStrings } from "./framework";

// Puzzle config.
const DAY = 3;
const SAMPLE_ANSWER_1 = 357;
const SAMPLE_ANSWER_2 = 3121910778619;

// Types.
type BatteryBank = number[];

type Input = BatteryBank[];


// Parse input.
const parseInput = (input: string): Input =>
    input.split('\n').map((line) => line.split('').map(Number));


// Solve.
const solve1 = (input: Input): number => {
    return solve(input);
};

const solve2 = (input: Input): number => {
    return solve(input);
};

const solve = (input: Input) => {
    return input.reduce((prev, curr) => prev + findMaxJoltageOfBatteryBank1(curr), 0);
}

function findMaxJoltageOfBatteryBank1(bank: BatteryBank): number {
    if (!bank.length) {
        return 0;
    }

    if (bank.length < 3) {
        return Number(bank.join(''));
    }

    let max = 0;
    for (let i = 0; i < bank.length - 1; i++) {
        for (let j = i + 1; j < bank.length; j++) {
            const joltage = Number([bank[i], bank[j]].join(''));
            if (joltage > max) {
                max = joltage;
            }
        }
    }

    return max;
}


// Main.
generateMain(parseInput, solve1, solve2)(...(await getInputStrings(DAY)), SAMPLE_ANSWER_1, SAMPLE_ANSWER_2);
