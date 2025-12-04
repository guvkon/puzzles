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
    return input.reduce((prev, curr) => prev + findMaxJoltageOfBatteryBank(curr, 2), 0);
};

const solve2 = (input: Input): number => {
    return input.reduce((prev, curr) => prev + findMaxJoltageOfBatteryBank(curr, 12), 0);
};

function findMaxJoltageOfBatteryBank(bank: BatteryBank, length: number): number {
    if (!bank.length) {
        return 0;
    }

    if (bank.length <= length) {
        return Number(bank.join(''));
    }

    return Number(findSequence(bank, length, []).join(''));
}

function findSequence(bank: BatteryBank, length: number, sequence: BatteryBank): BatteryBank {
    if (sequence.length >= length) {
        return sequence;
    }

    const remainingLength = length - sequence.length;

    const order = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0];
    for (const digit of order) {
        const index = bank.indexOf(digit);
        if (index === -1 || index + remainingLength > bank.length) {
            continue;
        }

        return findSequence(bank.slice(index + 1), length, [...sequence, digit]);
    }

    throw new Error('Cannot find any digit?!');
}


// Main.
generateMain(parseInput, solve1, solve2)(...(await getInputStrings(DAY)), SAMPLE_ANSWER_1, SAMPLE_ANSWER_2);
