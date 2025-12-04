type ParseInput<Input> = (input: string) => Input;
type Solve<Input> = (input: Input) => number;

export function generateMain<Input>(parseInput: ParseInput<Input>, solve1: Solve<Input>, solve2: Solve<Input>) {
    return (input: string, sampleInput: string, sampleAnswer1: number, sampleAnswer2: number) => {
        // Answers
        let answer: number;

        // Part 1.
        answer = solve1(parseInput(sampleInput));
        if (answer !== sampleAnswer1) {
            console.error(`Wrong sample answer for part 1! Got: ${answer}, correct: ${sampleAnswer1}`);
            return;
        }

        answer = solve1(parseInput(input));
        console.log(`Answer for part 1: ${answer}`);

        // Part 2.
        answer = solve2(parseInput(sampleInput));
        if (answer !== sampleAnswer2) {
            console.error(`Wrong sample answer for part 2! Got: ${answer}, correct: ${sampleAnswer2}`);
            return;
        }

        answer = solve2(parseInput(input));
        console.log(`Answer for part 2: ${answer}`);
    };
}

export async function getInputStrings(day: number): Promise<[string, string]> {
    const inputs = (await Promise.allSettled([
        await Bun.file(`input/day${day}.txt`).text(),
        await Bun.file(`input/day${day}_sample.txt`).text()
    ]))
        .filter((promise) => promise.status === 'fulfilled')
        .map((promise) => promise.value);

    return inputs as [string, string];
}
