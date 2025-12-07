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
type Beam = {
    count: number;
    x: number;
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
    return placeBeams(input).count();
};

class BeamCollection {
    beams: Beam[] = [];

    add({ x, count }: Beam) {
        const existing = this.beams.find((b) => b.x === x);
        if (existing) {
            existing.count += count;
        } else {
            this.beams.push({ x, count });
        }
    }

    count() {
        return this.beams.reduce((prev, curr) => prev + curr.count, 0);
    }
}

const placeBeams = (grid: Grid): BeamCollection => {
    const step = (grid: Grid, y: number, beams: BeamCollection): BeamCollection => {
        const newBeams = new BeamCollection();

        for (const { x, count } of beams.beams) {
            const cell = grid.getCell(x, y);
            switch (cell) {
                case '^':
                    grid.drawBeam(x - 1, y) && newBeams.add({ x: x - 1, count });
                    grid.drawBeam(x + 1, y) && newBeams.add({ x: x + 1, count });
                    break;
                default:
                    grid.drawBeam(x, y) && newBeams.add({ x, count });
            }
        }

        return newBeams;
    };

    let beams: BeamCollection = new BeamCollection();
    beams.add({ x: findStart(grid)[0], count: 1 });

    for (let y = 0; y < grid.height; y++) {
        beams = step(grid, y, beams);
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
