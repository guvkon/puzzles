import { generateMain, getInputStrings } from "./framework";

// Puzzle config.
const DAY = 4;
const SAMPLE_ANSWER_1 = 13;
const SAMPLE_ANSWER_2 = 43;

// Types.
type Cell = '@' | '.';
type Grid = {
    getCell: (x: number, y: number) => Cell;
    removeRoll: (x: number, y: number) => void;
    height: number;
    width: number;
};

type Input = Grid;


// Parse input.
const parseInput = (input: string): Input => {
    const cells = input.split('\n').map((line) => line.split('').map((cell) => cell as Cell));
    if (!cells.length || !cells[0]?.length) throw new Error('Unexpected input');

    const getCell = (x: number, y: number) => cells[y] ? (cells[y][x] ?? '.') : '.';
    const removeRoll = (x: number, y: number) => {
        if (!cells[y] || !cells[y][x]) return;
        cells[y][x] = '.';
    }
    const height = cells.length;
    const width = cells[0].length;

    return { height, width, getCell, removeRoll }
}


// Solve.
const solve1 = (input: Input): number => {
    return countRolls(input, false);
};

const solve2 = (input: Input): number => {
    return countRolls(input, true);
};

const countRolls = ({ getCell, height, removeRoll, width }: Input, withDeletion: boolean, count: number = 0): number => {
    const initialCount = count;

    for (let x = 0; x < width; x++) {
        for (let y = 0; y < height; y++) {
            const cell = getCell(x, y);
            if (cell === '.') continue;

            const surroundingCoordinates = [
                [x - 1, y],
                [x + 1, y],
                [x, y - 1],
                [x, y + 1],
                [x + 1, y - 1],
                [x + 1, y + 1],
                [x - 1, y - 1],
                [x - 1, y + 1],
            ] as const;
            const rollsCount = surroundingCoordinates.map((coord) => getCell(coord[0], coord[1])).filter((cell) => cell === '@').length;

            if (rollsCount < 4) {
                count++;
                if (withDeletion) {
                    removeRoll(x, y);
                }
            }
        }
    }

    if (!withDeletion) {
        return count;
    }

    return initialCount === count ? count : countRolls({ getCell, height, removeRoll, width }, withDeletion, count);
}


// Main.
generateMain(parseInput, solve1, solve2)(...(await getInputStrings(DAY)), SAMPLE_ANSWER_1, SAMPLE_ANSWER_2);
