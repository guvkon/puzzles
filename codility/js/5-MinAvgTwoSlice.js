function solution(A) {
    const prefixSums = getPrefixSums(A);
    let minAverage = false,
        minAveragePosition;
    for (let p = 0; p < A.length - 1; p++) {
        for (let q = p + 1; q < A.length; q++) {
            const sum = prefixSums[q + 1] - prefixSums[p];
            const average = sum / (q - p + 1);
            if (false === minAverage || minAverage > average) {
                minAverage = average;
                minAveragePosition = p;
            }
        }
    }
    return minAveragePosition;
}

function getPrefixSums(A) {
    const prefixSums = new Array(A.length + 1);
    prefixSums[0] = 0;
    for (let i = 1; i < prefixSums.length; i++) {
        prefixSums[i] = prefixSums[i - 1] + A[i - 1];
    }
    return prefixSums;
}

