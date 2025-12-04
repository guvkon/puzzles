import { generateMain, getInputStrings } from './framework';

// Puzzle config.
const DAY = 2;
const SAMPLE_ANSWER_1 = 1227775554;
const SAMPLE_ANSWER_2 = 4174379265;

// Types.
type Range = [number, number];

type Input = Range[];

// Parse input.
const parseInput = (input: string): Input =>
    input
        .split(',')
        .map((line) => {
            const match = /^(\d+)-(\d+)$/gm.exec(line);
            if (!match) return null;

            return [Number(match[1]), Number(match[2])] as Range;
        })
        .filter((value: Range | null): value is Range => value !== null);

// Solve.
const solve1 = (input: Input): number => {
    return solve(isSilly1, input);
};

const solve2 = (input: Input): number => {
    return solve(isSilly2, input);
};

const solve = (isSilly: (id: number) => boolean, input: Input) => {
    let sum = 0;

    input.forEach((range) => {
        for (let id = range[0]; id <= range[1]; id++) {
            if (isSilly(id)) {
                sum += id;
            }
        }
    });

    return sum;
};

function isSilly1(id: number): boolean {
    const _id = String(id);

    if (_id.length % 2 !== 0) {
        return false;
    }

    return _id.slice(0, _id.length / 2) === _id.slice(_id.length / 2);
}

function isSilly2(id: number): boolean {
    const _id = String(id);

    for (
        let substringLength = 1;
        substringLength <= Math.floor(_id.length / 2);
        substringLength++
    ) {
        if (_id.length % substringLength !== 0) {
            continue;
        }

        const substring = _id.slice(0, substringLength);
        let constructed = '';
        for (let i = 0; i < _id.length / substringLength; i++) {
            constructed += substring;
        }

        if (constructed === _id) {
            return true;
        }
    }

    return false;
}

// Main.
generateMain(parseInput, solve1, solve2)(
    ...(await getInputStrings(DAY)),
    SAMPLE_ANSWER_1,
    SAMPLE_ANSWER_2
);
