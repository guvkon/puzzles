import { generateMain, getInputStrings } from './framework';

// Puzzle config.
const DAY = 6;
const SAMPLE_ANSWER_1 = 4277556;
const SAMPLE_ANSWER_2 = 4277556;

// Types.
type Problem = {
    numbers: number[];
    operation: '+' | '*';
};

type Input = Problem[];

// Parse input.
const parseInput = (input: string): Input => {
    const lines = input.split('\n').map((line) => line.split(' ').filter(Boolean));
    if (!lines[0] || !lines[1]) {
        return [];
    }

    const opIndex = lines.length - 1;
    const problemsCount = lines[0].length;

    const problems: Problem[] = [];
    for (let i = 0; i < problemsCount; i++) {
        const numbers = [];
        let operation: '+' | '*' = '+';

        for (let j = 0; j < lines.length; j++) {
            const value = lines[j]?.[i];
            if (!value)
                throw new Error(
                    `Unexpected value at ${j}:${i}. Value = ${value}, type = ${typeof value}`
                );

            if (j < opIndex) {
                numbers.push(Number(value));
            } else if (value === '*') {
                operation = '*';
            }
        }
        problems.push({ numbers, operation });
    }

    return problems;
};

// Solve.
const solve1 = (input: Input): number => input.reduce((prev, curr) => prev + solveProblem(curr), 0);

const solve2 = (input: Input): number => 0;

const solveProblem = ({ numbers, operation }: Problem): number => {
    switch (operation) {
        case '+':
            return numbers.reduce((prev, curr) => prev + curr, 0);
        case '*':
            return numbers.reduce((prev, curr) => prev * curr, 1);
    }
};

// Main.
generateMain(parseInput, solve1, solve2)(
    ...(await getInputStrings(DAY)),
    SAMPLE_ANSWER_1,
    SAMPLE_ANSWER_2
);
