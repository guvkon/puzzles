import { generateMain, getInputStrings } from './framework';

// Puzzle config.
const DAY = 7;
const SAMPLE_ANSWER_1 = 21;
const SAMPLE_ANSWER_2 = 40;

// Types.
type Cell = 'S' | '.' | '^' | '|' | ' ';
type Coords = [number, number];
type Grid = {
    getCell: (x: number, y: number) => Cell;
    drawBeam: (x: number, y: number) => boolean;
    width: number;
    height: number;
};

type Input = Grid;

// Parse input.
const parseInput = (input: string): Input => {
    const cells = input.split('\n').map((line) => line.split(''));
    if (!cells[0]) throw new Error('Unexpected result');
    const height = cells.length;
    const width = cells[0].length;
    const getCell = (x: number, y: number): Cell => {
        const cell = cells[y]?.[x];
        if (!cell || !['S', '.', '^', '|'].includes(cell)) return ' ';
        return cell as Cell;
    };
    const drawBeam = (x: number, y: number): boolean => {
        if (cells[y] && cells[y][x]) {
            cells[y][x] = '|';
            return true;
        }
        return false;
    };
    return { height, width, getCell, drawBeam };
};

// Solve.
const solve1 = (input: Input): number => {
    placeBeams(input);
    let countSplits = 0;
    for (let y = 0; y < input.height; y++) {
        for (let x = 0; x < input.width; x++) {
            const cell = input.getCell(x, y);
            if (cell !== '^') continue;
            if (input.getCell(x, y - 1) === '|') {
                countSplits++;
            }
        }
    }

    return countSplits;
};

const solve2 = (input: Input): number => {
    return placeBeams(input).length;
};

const placeBeams = (grid: Grid): number[] => {
    const step = (grid: Grid, position: number, beams: number[]): number[] => {
        const newBeams = [];
        const y = position + 1;
        for (const x of beams) {
            const cell = grid.getCell(x, y);
            switch (cell) {
                case '^':
                    grid.drawBeam(x - 1, y) && newBeams.push(x - 1);
                    grid.drawBeam(x + 1, y) && newBeams.push(x + 1);
                    break;
                default:
                    grid.drawBeam(x, y) && newBeams.push(x);
            }
        }
        return newBeams;
    };

    const start = findStart(grid);
    let beams: number[] = [start[0]];
    for (let y = 0; y < grid.height; y++) {
        beams = step(grid, y, beams);
        console.debug({ y, beams: beams.length });
    }

    return beams;
};

const findStart = ({ getCell, height, width }: Grid): Coords => {
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            if (getCell(x, y) === 'S') {
                return [x, y];
            }
        }
    }

    throw new Error('Cannot find start!');
};

// Main.
generateMain(parseInput, solve1, solve2)(
    ...(await getInputStrings(DAY)),
    SAMPLE_ANSWER_1,
    SAMPLE_ANSWER_2
);
