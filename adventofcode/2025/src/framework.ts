type ParseInput<Input> = (input: string) => Input;
type Solve<Input> = (input: Input) => number;

export function generateMain<Input>(
    parseInput: ParseInput<Input>,
    solve1: Solve<Input>,
    solve2: Solve<Input>,
    parseInput2: ParseInput<Input> | null = null
) {
    return (input: string, sampleInput: string, sampleAnswer1: number, sampleAnswer2: number) => {
        // Answers
        let answer: number;

        // Part 1.
        answer = solve1(parseInput(sampleInput));
        if (answer !== sampleAnswer1) {
            console.error(
                `Wrong sample answer for part 1! Got: ${answer}, correct: ${sampleAnswer1}`
            );
            return;
        }

        const preAnswer1 = performance.now();
        answer = solve1(parseInput(input));
        const postAnswer1 = performance.now();
        console.log(`Answer for part 1: ${answer}`);
        console.log(`It took ${(postAnswer1 - preAnswer1).toFixed(3)} ms.`);

        // Part 2.
        const _parseInput = parseInput2 || parseInput;
        answer = solve2(_parseInput(sampleInput));
        if (answer !== sampleAnswer2) {
            console.error(
                `Wrong sample answer for part 2! Got: ${answer}, correct: ${sampleAnswer2}`
            );
            return;
        }

        const preAnswer2 = performance.now();
        answer = solve2(_parseInput(input));
        const postAnswer2 = performance.now();
        console.log(`Answer for part 2: ${answer}`);
        console.log(`It took ${(postAnswer2 - preAnswer2).toFixed(3)} ms.`);
    };
}

export async function getInputStrings(day: number): Promise<[string, string]> {
    const inputs = (
        await Promise.allSettled([
            await Bun.file(`input/day${day}.txt`).text(),
            await Bun.file(`input/day${day}_sample.txt`).text(),
        ])
    )
        .filter((promise) => promise.status === 'fulfilled')
        .map((promise) => promise.value);

    return inputs as [string, string];
}
