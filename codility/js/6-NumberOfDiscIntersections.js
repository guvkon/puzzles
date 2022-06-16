function solution(A) {
    const lines = Array(A.length);
    for (let i = 0; i < lines.length; i++) {
        lines[i] = [];
    }

    for (let center = 0; center < A.length; center++) {
        const radius = A[center];
        let left = center - radius;
        let length = 2 * radius;
        if (left < 0) {
            length += left;
            left = 0;
        }
        lines[left].push(length);
    }

    let counter = 0;
    for (let left = 0; left < lines.length; left++) {
        for (let j = 0; j < lines[left].length; j++) {
            const length = lines[left][j];
            counter += lines[left].length - 1 - j; // calculate number of unordered pairs on the same spot
            if (counter > 10000000) {
                return -1;
            }
            for (let k = left + 1; k <= left + length && k < lines.length; k++) {
                counter += lines[k].length;
                if (counter > 10000000) {
                    return -1;
                }
            }
        }
    }
    return counter;
}

