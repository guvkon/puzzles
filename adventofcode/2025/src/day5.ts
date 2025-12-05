import { generateMain, getInputStrings } from './framework';

// Puzzle config.
const DAY = 5;
const SAMPLE_ANSWER_1 = 3;
const SAMPLE_ANSWER_2 = 14;

// Types.
type Range = [number, number];

type Input = {
    freshRanges: Range[];
    available: number[];
};

// Parse input.
const parseInput = (input: string): Input => {
    const parts = input.split('\n\n') as [string, string];
    const freshRanges: Range[] = parts[0].split('\n').map((line) => {
        return (line.split('-') as [string, string]).map(Number) as [number, number];
    });
    const available = parts[1].split('\n').map(Number);

    return { freshRanges, available };
};

// Solve.
const solve1 = (input: Input): number => countFreshFromAvailable(input);

const solve2 = ({ freshRanges }: Input): number =>
    countFreshFromAll(combineFreshRanges(freshRanges));

const countFreshFromAvailable = ({ available, freshRanges }: Input): number =>
    available.reduce((prev, curr) => prev + (isFresh(curr, freshRanges) ? 1 : 0), 0);

const countFreshFromAll = (combinedRanges: Range[]): number => {
    return combinedRanges.reduce((prev, curr) => prev + curr[1] - curr[0] + 1, 0);
};

const combineFreshRanges = (uncombinedRanges: Range[]): Range[] => {
    const combinedRanges: Range[] = [];

    for (const rawRange of uncombinedRanges) {
        const index = combinedRanges.findIndex((range) => isTwoRangesOverlapping(range, rawRange));
        if (index === -1) {
            combinedRanges.push(rawRange);
        } else {
            const rangeWithOverlap = combinedRanges[index] as Range;
            combinedRanges[index] = combineTwoOverlappingRanges(rawRange, rangeWithOverlap);
        }
    }

    return combinedRanges.length === uncombinedRanges.length
        ? combinedRanges
        : combineFreshRanges(combinedRanges);
};

const isTwoRangesOverlapping = (a: Range, b: Range): boolean => getOverlappingRange(a, b) !== null;

const combineTwoOverlappingRanges = (a: Range, b: Range): Range => {
    const overlapping = getOverlappingRange(a, b);
    if (overlapping === null) {
        throw new Error('Trying to combine non-overlapping ranges!');
    }

    return overlapping;
};

const getOverlappingRange = (a: Range, b: Range): null | Range => {
    const [aLeft, aRight] = a;
    const [bLeft, bRight] = b;

    if (aRight >= bLeft && aRight <= bRight) {
        return [Math.min(aLeft, bLeft), bRight];
    }
    if (bRight >= aLeft && bRight <= aRight) {
        return [Math.min(bLeft, aLeft), aRight];
    }

    return null;
};

const isFresh = (id: number, freshRanges: Range[]): boolean =>
    freshRanges.reduce((prev, curr) => prev || (curr[0] <= id && curr[1] >= id), false);

// Main.
generateMain(parseInput, solve1, solve2)(
    ...(await getInputStrings(DAY)),
    SAMPLE_ANSWER_1,
    SAMPLE_ANSWER_2
);
