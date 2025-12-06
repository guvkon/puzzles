import { generateMain, getInputStrings } from './framework';

// Puzzle config.
const DAY = 6;
const SAMPLE_ANSWER_1 = 4277556;
const SAMPLE_ANSWER_2 = 3263827;

// Types.
type Operation = '+' | '*';
type Problem = {
    numbers: number[];
    operation: Operation;
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

const parseInput2 = (input: string): Input => {
    const lines = input.split('\n');
    if (!lines[0] || !lines[1]) {
        return [];
    }

    const problems: Problem[] = [];

    const paperWidth = lines.reduce((prev, curr) => Math.max(prev, curr.length), 0);
    const operationsLine = (lines.pop() as string).split('');

    let index = 0;
    do {
        const operation = operationsLine[index] as Operation;
        const startIndex = index;
        index = operationsLine.findIndex(
            (value, index) => index > startIndex && ['*', '+'].includes(value)
        );
        const endIndex = index === -1 ? paperWidth : index;

        const numbers: number[] = [];
        for (let column = startIndex; column < endIndex; column++) {
            let number = '';
            for (const line of lines) {
                number += line[column] || '';
            }
            number = number.replaceAll(' ', '');
            if (!number) continue;
            numbers.push(Number(number));
        }
        numbers.reverse();

        problems.push({ operation, numbers });
    } while (index !== -1);

    return problems;
};

// Solve.
const solve1 = (input: Input): number => input.reduce((prev, curr) => prev + solveProblem(curr), 0);

const solve2 = solve1;

const solveProblem = ({ numbers, operation }: Problem): number => {
    switch (operation) {
        case '+':
            return numbers.reduce((prev, curr) => prev + curr, 0);
        case '*':
            return numbers.reduce((prev, curr) => prev * curr, 1);
    }
};

// Main.
generateMain(
    parseInput,
    solve1,
    solve2,
    parseInput2
)(...(await getInputStrings(DAY)), SAMPLE_ANSWER_1, SAMPLE_ANSWER_2);
